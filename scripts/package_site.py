"""Build and verify a Cloudflare Pages ZIP containing only referenced site files."""
from hashlib import sha256
import json
import shutil
import sys
from zipfile import ZipFile, ZIP_DEFLATED

sys.dont_write_bytecode=True
from build_cloudflare import build, DIST, ARTIFACTS


def main():
    manifest=build()
    archive=ARTIFACTS/'al-marwa-cloudflare.zip';temporary=archive.with_suffix('.zip.tmp')
    with ZipFile(temporary,'w',compression=ZIP_DEFLATED,compresslevel=6) as bundle:
        for record in manifest['files']:
            content=(DIST/record['path']).read_bytes()
            assert sha256(content).hexdigest()==record['sha256']
            bundle.write(DIST/record['path'],record['path'])
    temporary.replace(archive)
    with ZipFile(archive) as bundle:
        assert bundle.testzip() is None
        assert {'index.html','404.html','robots.txt','sitemap.xml','llms.txt','_headers','_redirects'}.issubset(bundle.namelist())
        assert not any(name.startswith(('.git/','.github/','scripts/','artifacts/')) for name in bundle.namelist())
        assert 'CNAME' not in bundle.namelist() and '.nojekyll' not in bundle.namelist()
        assert not any(name.startswith('videos/') and name.endswith('.pdf') for name in bundle.namelist())
        for record in manifest['files']:assert sha256(bundle.read(record['path'])).hexdigest()==record['sha256']
    release={'archive':archive.name,'platform':'cloudflare-pages','sha256':sha256(archive.read_bytes()).hexdigest(),'file_count':len(manifest['files']),'files':manifest['files']}
    (ARTIFACTS/'release-manifest.json').write_text(json.dumps(release,indent=2)+'\n',encoding='utf-8')
    shutil.copyfile(archive,ARTIFACTS/'al-marwa-site.zip')
    print(f'Verified Cloudflare ZIP: {archive.name}; {release["file_count"]} public files; {archive.stat().st_size:,} bytes.')


if __name__=='__main__':main()
