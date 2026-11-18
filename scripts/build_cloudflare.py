"""Build a referenced-assets-only Cloudflare Pages release without altering source.

Published URLs are extensionless, as required by Pages' native HTML redirects.
Assets are fingerprinted and only explicitly referenced public files are shipped.
"""
from __future__ import annotations

from hashlib import sha256
from html import escape, unescape
from html.parser import HTMLParser
import json
from pathlib import Path, PurePosixPath
import posixpath
import re
import shutil
import tempfile
from urllib.parse import unquote, urlsplit, urlunsplit

ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/'dist'
ARTIFACTS=ROOT/'artifacts'
MANIFEST=ARTIFACTS/'cloudflare-build-manifest.json'
HOSTS={'al-marwaco.com','www.al-marwaco.com'}
ORIGIN='https://al-marwaco.com'
PUBLIC_ROOT={'robots.txt','sitemap.xml','llms.txt','LICENSE.txt','README.txt'}
CSS_URL=re.compile(r'url\(\s*([\"\']?)(.*?)\1\s*\)',re.I)
SITE_URL=re.compile(r'https?://(?:www\.)?al-marwaco\.com(?:/[^\s\"\'<>\\)]*)?')
ATTRIBUTE=re.compile(r'\b(href|src|poster|action|srcset)\s*=\s*([\"\'])(.*?)\2',re.I|re.S)


class References(HTMLParser):
    def __init__(self):super().__init__();self.urls=[]
    def handle_starttag(self,tag,attrs):
        for name,value in attrs:
            if not value:continue
            if name in {'href','src','poster'}:self.urls.append(value)
            elif name=='srcset':self.urls.extend(item.strip().split()[0] for item in value.split(',') if item.strip())


def source_reference(value,context):
    value=unescape(value.strip())
    if not value or value.startswith(('#','data:','blob:')):return None
    parts=urlsplit(value)
    if parts.netloc and parts.hostname not in HOSTS:return None
    if parts.scheme and parts.scheme not in {'http','https'}:return None
    path=unquote(parts.path)
    if not path and parts.netloc:path='/'
    if not path:return None
    relative=posixpath.normpath(path.lstrip('/') if path.startswith('/') or parts.netloc else str(PurePosixPath(context).parent/path))
    if relative in {'.',''}:relative='index.html'
    candidate=ROOT/relative
    if not candidate.exists() and not PurePosixPath(relative).suffix and (ROOT/(relative+'.html')).is_file():relative+='.html';candidate=ROOT/relative
    if not candidate.is_file():raise ValueError(f'{context}: missing referenced file {value}')
    if not candidate.resolve().is_relative_to(ROOT):raise ValueError(f'Reference leaves the website workspace: {value}')
    if '/' not in relative:
        if relative not in PUBLIC_ROOT and candidate.suffix!='.html':raise ValueError(f'Non-public root file referenced: {value}')
    else:
        directory=PurePosixPath(relative).parts[0]
        if directory not in {'assets','images','videos','downloads'}:raise ValueError(f'Non-public directory referenced: {value}')
        if directory=='videos' and candidate.suffix.lower() not in {'.mp4','.webm'}:raise ValueError(f'Only referenced media is publishable from videos/: {value}')
    return relative


def references(context):
    path=ROOT/context
    if path.suffix.lower() not in {'.html','.css','.js','.svg','.txt','.xml'}:return set()
    source=path.read_text(encoding='utf-8')
    values=[match[2] for match in CSS_URL.finditer(source)] if path.suffix.lower() in {'.html','.css','.svg'} else []
    values.extend(match[0] for match in SITE_URL.finditer(source))
    if path.suffix.lower() in {'.html','.svg'}:
        parser=References();parser.feed(source);values.extend(parser.urls)
    result=set()
    for value in values:
        ref=source_reference(value,context)
        if ref is not None:result.add(ref)
    return result


def collect_public_files():
    pending={p.name for p in ROOT.glob('*.html')}|PUBLIC_ROOT
    pending.update(p.relative_to(ROOT).as_posix() for p in (ROOT/'assets/webfonts').glob('*.txt'))
    found=set()
    while pending:
        item=pending.pop()
        if item in found:continue
        found.add(item);pending.update(references(item)-found)
    return found


def page_url(name):return '/' if name=='index.html' else '/'+name.removesuffix('.html')


def build():
    pages={p.name for p in ROOT.glob('*.html')}
    files=collect_public_files();mapping={};output={};active=set()

    def rewrite(value,context):
        if not value or value.startswith(('#','data:','blob:')):return value
        parts=urlsplit(value)
        if parts.netloc and parts.hostname not in HOSTS:return value
        if parts.scheme and parts.scheme not in {'http','https'}:return value
        ref=source_reference(value,context)
        if ref is None:return value
        if ref in pages:path=page_url(ref)
        else:
            materialize(ref)
            path='/'+mapping[ref]
        if parts.netloc:return urlunsplit(('https','al-marwaco.com',path,parts.query,parts.fragment))
        if PurePosixPath(context).suffix=='.css':
            path=posixpath.relpath(path.lstrip('/'),str(PurePosixPath(context).parent))
        return urlunsplit(('','',path,parts.query,parts.fragment))

    def transform(source,context):
        suffix=PurePosixPath(context).suffix.lower()
        if suffix=='.html':
            # Use the existing small PNG favicon instead of redundant full-size JPEGs.
            if 'favicon-32x32.png' in source:
                source=re.sub(r'<link\b(?=[^>]*\brel=[\"\'](?:shortcut icon|icon)[\"\'])(?=[^>]*\bhref=[\"\'][^\"\']+\.jpe?g[\"\'])[^>]*>','',source,flags=re.I)
            # Large service footage loads only after the visitor chooses to play it.
            source=re.sub(r'(<video\b[^>]*\bpreload=)([\"\'])metadata\2',lambda m:m[1]+m[2]+'none'+m[2],source,flags=re.I)
        if suffix in {'.html','.svg'}:
            def attribute(match):
                name,quote,value=match.groups();value=unescape(value)
                if name.lower()=='srcset':
                    candidates=[]
                    for item in value.split(','):
                        parts=item.strip().split(maxsplit=1)
                        if parts:candidates.append(rewrite(parts[0],context)+(' '+parts[1] if len(parts)>1 else ''))
                    value=', '.join(candidates)
                else:value=rewrite(value,context)
                return name+'='+quote+escape(value,quote=True)+quote
            source=ATTRIBUTE.sub(attribute,source)
        if suffix in {'.html','.css','.svg'}:
            source=CSS_URL.sub(lambda match:'url('+match[1]+rewrite(unescape(match[2]),context)+match[1]+')',source)
        source=SITE_URL.sub(lambda match:rewrite(unescape(match[0]),context),source)
        if suffix in {'.html','.js'}:
            for name in sorted(pages,key=len,reverse=True):
                # Actual relative page URL literals only; queries/fragments survive.
                pattern=r'([\"\'])'+re.escape(name)+r'(?=[\"\'?#])'
                source=re.sub(pattern,lambda m:m[1]+page_url(name),source)
        return source

    def materialize(name):
        if name in mapping:return
        if name in active:raise ValueError(f'Cyclic asset dependency: {name}')
        active.add(name);path=ROOT/name;suffix=path.suffix.lower()
        content=transform(path.read_text(encoding='utf-8'),name).encode('utf-8') if suffix in {'.html','.css','.js','.svg','.txt','.xml'} else path.read_bytes()
        fingerprint=PurePosixPath(name).parts[0] in {'assets','images','videos'} and suffix!='.txt'
        target=str(PurePosixPath(name).with_name(path.stem+'.'+sha256(content).hexdigest()[:12]+path.suffix)) if fingerprint else name
        mapping[name]=target;output[target]=content;active.remove(name)

    for name in sorted(files):materialize(name)
    output['_headers']=(ROOT/'cloudflare/_headers').read_bytes()
    redirects=['# Legacy URLs and slash aliases redirect to Pages canonical URLs.','/index / 301','/index/ / 301']
    for name in sorted(pages):
        target=page_url(name);redirects.append('/'+name+' '+target+' 301')
        if name!='index.html':redirects.append(target+'/ '+target+' 301')
    output['_redirects']=('\n'.join(redirects)+'\n').encode()
    if any(len(content)>25*1024*1024 for content in output.values()):raise ValueError('A public file exceeds the Cloudflare Pages 25 MiB file limit.')
    ARTIFACTS.mkdir(exist_ok=True)
    manifest={'platform':'cloudflare-pages','output_directory':'dist','origin':ORIGIN,'pages':{name:page_url(name) for name in sorted(pages)},'asset_map':mapping,'files':[]}
    with tempfile.TemporaryDirectory(prefix='cloudflare-stage-',dir=ARTIFACTS) as temp:
        stage=Path(temp).resolve()
        assert stage.is_relative_to(ARTIFACTS.resolve())
        for name,content in output.items():
            target=stage/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(content)
            manifest['files'].append({'path':name,'bytes':len(content),'sha256':sha256(content).hexdigest()})
        if DIST.exists():
            # Only replace this exact, previously generated directory; never a user folder.
            assert DIST.resolve()==ROOT/'dist' and DIST.resolve().is_relative_to(ROOT)
            if not MANIFEST.is_file() or json.loads(MANIFEST.read_text(encoding='utf-8')).get('output_directory')!='dist':raise ValueError('dist exists without a generated build manifest; refusing to replace it.')
            shutil.rmtree(DIST)
        shutil.copytree(stage,DIST)
    manifest['files'].sort(key=lambda item:item['path'])
    MANIFEST.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Cloudflare Pages build: {len(pages)-1} indexable pages, custom 404, {len(output)} public files in dist/.')
    return manifest


if __name__=='__main__':build()
