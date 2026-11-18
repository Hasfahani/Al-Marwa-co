"""Check built Pages files and, with --base-url, Wrangler or production HTTP."""
from __future__ import annotations
import argparse
from hashlib import sha256
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET
from urllib.error import HTTPError
from urllib.parse import urlsplit, parse_qs
from urllib.request import Request, build_opener, HTTPRedirectHandler

ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/'dist'
ORIGIN='https://al-marwaco.com'

class Page(HTMLParser):
    def __init__(self):super().__init__();self.tags=[]
    def handle_starttag(self,tag,attrs):self.tags.append((tag,dict(attrs)))
    def canonical(self):return next(a['href'] for tag,a in self.tags if tag=='link' and a.get('rel')=='canonical')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--base-url');parser.add_argument('--check-hosts',action='store_true');parser.add_argument('--pages-url');args=parser.parse_args()
    manifest=json.loads((ROOT/'artifacts/cloudflare-build-manifest.json').read_text(encoding='utf-8'))
    pages=manifest['pages'];routes={route:name for name,route in pages.items()};assets={item['path'] for item in manifest['files']}
    assert set(pages)=={p.name for p in ROOT.glob('*.html')}
    assert not {'CNAME','.nojekyll'} & assets
    assert not any(path.startswith(('scripts/','.git/','.github/','artifacts/')) for path in assets)
    assert not any(path.startswith('videos/') and path.endswith('.pdf') for path in assets)
    for record in manifest['files']:assert sha256((DIST/record['path']).read_bytes()).hexdigest()==record['sha256'],record['path']
    for name,route in pages.items():
        source=(DIST/name).read_text(encoding='utf-8');document=Page();document.feed(source)
        assert document.canonical()==ORIGIN+route,name
        for tag,attrs in document.tags:
            for attr in ('href','src','poster'):
                target=attrs.get(attr)
                if not target:continue
                parts=urlsplit(target)
                if parts.netloc and parts.hostname!='al-marwaco.com':continue
                if parts.scheme and parts.scheme not in {'http','https'}:continue
                if not parts.path:continue
                assert parts.path.startswith('/'),(name,target)
                assert parts.path in routes or parts.path.lstrip('/') in assets,(name,target)
                assert not parts.path.endswith('.html'),(name,target)
        for match in re.finditer(r'<script type="application/ld\+json">(.*?)</script>',source,re.S):json.loads(match[1])
        if name=='404.html':assert 'noindex' in source
        else:assert not any(tag=='meta' and attrs.get('name')=='robots' and 'noindex' in attrs.get('content','') for tag,attrs in document.tags)
    tree=ET.parse(DIST/'sitemap.xml');ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9','x':'http://www.w3.org/1999/xhtml'}
    expected={ORIGIN+route for name,route in pages.items() if name!='404.html'}
    assert {n.text for n in tree.findall('s:url/s:loc',ns)}==expected
    for link in tree.findall('s:url/x:link',ns):assert link.get('href') in expected
    for path in assets:
        if path.startswith(('assets/','images/','videos/')) and not path.endswith('.txt'):assert re.search(r'\.[0-9a-f]{12}\.[^/]+$',path),path
        if path.endswith('.js'):assert 'contact.html' not in (DIST/path).read_text(encoding='utf-8'),path
        if path.endswith('.css'):
            for match in re.finditer(r'url\(\s*[\"\']?([^\"\')\s]+)',(DIST/path).read_text(encoding='utf-8')):
                ref=urlsplit(match[1])
                if ref.scheme or ref.netloc or not ref.path:continue
                target=((DIST/path).parent/ref.path).resolve() if not ref.path.startswith('/') else (DIST/ref.path.lstrip('/')).resolve()
                assert target.is_relative_to(DIST) and target.is_file(),(path,match[1])
    redirects={}
    for line in (DIST/'_redirects').read_text().splitlines():
        if not line or line.startswith('#'):continue
        start,target,status=line.split();assert status=='301' and start!=target
        redirects[start]=target
    assert not any(target in redirects for target in redirects.values()),'Redirect chain or loop'
    assert not any(line.startswith('/* ') for line in (DIST/'_redirects').read_text().splitlines()),'SPA catch-all hides real 404s'
    print(f'Cloudflare artifact checks passed: {len(expected)} canonical pages, referenced assets, clean links, sitemap and redirect targets.')
    if not args.base_url:return

    class NoRedirect(HTTPRedirectHandler):
        def redirect_request(self,*args,**kwargs):return None
    opener=build_opener(NoRedirect())
    def get(path,host=None,head=False):
        headers={'User-Agent':'AL-Marwa-Deployment-Check/1.0'}
        if host:headers['Host']=host
        try:response=opener.open(Request(args.base_url.rstrip('/')+path,headers=headers,method='HEAD' if head else 'GET'),timeout=15)
        except HTTPError as error:response=error
        with response:return response.status,response.headers,response.read().decode('utf-8','replace')
    for name,route in pages.items():
        if name=='404.html':continue
        status,headers,source=get(route);assert status==200,(route,status)
        doc=Page();doc.feed(source);assert doc.canonical()==ORIGIN+route,route
        assert 'noindex' not in headers.get('X-Robots-Tag',''),route
        status,headers,_=get('/'+name);assert status in {301,308},(name,status)
        assert urlsplit(headers['Location']).path==route,(name,headers['Location'])
    status,headers,_=get('/contact.html?shipment_type=LCL&origin=China&destination=Lebanon')
    assert status in {301,308} and parse_qs(urlsplit(headers['Location']).query)=={'shipment_type':['LCL'],'origin':['China'],'destination':['Lebanon']},headers.get('Location')
    status,headers,source=get('/__deployment_test__/missing/deep-page')
    assert status==404 and 'noindex' in source,(status,source[:100])
    doc=Page();doc.feed(source)
    stylesheet=next(attrs['href'] for tag,attrs in doc.tags if tag=='link' and attrs.get('rel')=='stylesheet')
    assert get(stylesheet,head=True)[0]==200,'Custom 404 stylesheet is broken'
    for path in assets:
        if path.startswith(('assets/','images/','videos/')) and not path.endswith('.txt'):
            status,headers,_=get('/'+path,head=True)
            assert status==200 and 'immutable' in headers.get('Cache-Control',''),(path,status,headers.get('Cache-Control'))
    status,headers,_=get('/')
    assert headers.get('X-Content-Type-Options')=='nosniff'
    assert 'https://formsubmit.co' in headers.get('Content-Security-Policy','')
    assert 'immutable' not in headers.get('Cache-Control',''),'HTML must remain fresh'
    if urlsplit(args.base_url).hostname in {'127.0.0.1','localhost'}:
        for host in ['sample.pages.dev','preview.sample.pages.dev']:
            status,headers,_=get('/',host=host);assert 'noindex' in headers.get('X-Robots-Tag',''),(host,status,dict(headers))
    elif args.pages_url:
        assert urlsplit(args.pages_url).hostname.endswith('.pages.dev')
        with opener.open(args.pages_url,timeout=15) as response:assert 'noindex' in response.headers.get('X-Robots-Tag','')
    if args.check_hosts:
        assert args.base_url.rstrip('/')==ORIGIN,'Host checks are for the production domain only'
        for url in ['http://al-marwaco.com/contact?test=1','https://www.al-marwaco.com/contact?test=1']:
            try:response=opener.open(url,timeout=15)
            except HTTPError as error:response=error
            with response:
                assert response.status in {301,308}
                assert response.headers['Location']=='https://al-marwaco.com/contact?test=1',response.headers['Location']
    print('Cloudflare HTTP checks passed: canonical pages, legacy redirects, query preservation, real 404s and cache/security headers. Preview noindex is checked locally or with --pages-url.')

if __name__=='__main__':main()
