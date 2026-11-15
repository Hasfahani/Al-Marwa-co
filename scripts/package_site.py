"""Create a deployment ZIP containing only public website files."""
from hashlib import sha256
import json
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'artifacts'
STATIC_EXTENSIONS={'.html','.css','.js','.jpg','.jpeg','.png','.svg','.gif','.webp','.avif','.ico','.woff','.woff2','.ttf','.eot','.mp4','.webm','.pdf','.txt'}


def main():
    files=list(ROOT.glob('*.html'))+[ROOT/name for name in ['robots.txt','sitemap.xml','llms.txt','CNAME','.nojekyll','LICENSE.txt','README.txt']]
    for directory in ['assets','images','videos','downloads']:
        files.extend(path for path in (ROOT/directory).rglob('*') if path.is_file() and path.suffix.lower() in STATIC_EXTENSIONS and not any(part.startswith('.') for part in path.relative_to(ROOT).parts))
    files=sorted(set(files))
    assert all(path.is_file() and path.resolve().is_relative_to(ROOT) for path in files)
    OUT.mkdir(exist_ok=True)
    archive=OUT/'al-marwa-site.zip';temporary=OUT/'al-marwa-site.zip.tmp'
    records=[]
    with ZipFile(temporary,'w',compression=ZIP_DEFLATED,compresslevel=6) as bundle:
        for path in files:
            name=path.relative_to(ROOT).as_posix();content=path.read_bytes()
            bundle.write(path,name)
            records.append({'path':name,'bytes':len(content),'sha256':sha256(content).hexdigest()})
    temporary.replace(archive)
    # Verify the finished archive against the exact source bytes being released.
    with ZipFile(archive) as bundle:
        assert bundle.testzip() is None
        assert {'index.html','robots.txt','sitemap.xml','llms.txt','CNAME','.nojekyll'}.issubset(bundle.namelist())
        assert not any(name.startswith(('.git/','.github/','scripts/','artifacts/')) for name in bundle.namelist())
        for record in records:assert sha256(bundle.read(record['path'])).hexdigest()==record['sha256']
    manifest={'archive':archive.name,'sha256':sha256(archive.read_bytes()).hexdigest(),'file_count':len(records),'files':records}
    (OUT/'release-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print(f'Verified deployment archive: {archive.name}; {len(records)} public files; {archive.stat().st_size:,} bytes.')


if __name__=='__main__':main()
