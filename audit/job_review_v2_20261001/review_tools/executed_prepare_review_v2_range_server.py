from pathlib import Path
import json, shutil

r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
m=json.loads((r/'audit/job_review_v2_20261001/MANIFEST_V2.json').read_text())
allowed=set(json.loads((r/'tmp/v2_preview_allowed.json').read_text()))
for family in ['audit/job_review_v2_20261001','audit/day_two_wash_bubble_reuse_v1_20261001','assets_src/imagegen/day2_wash_foam_v1_20261001']:
    allowed.update(p.relative_to(r).as_posix() for p in (r/family).rglob('*') if p.is_file())
register=json.loads((r/'audit/job_artwork_refinement_live/ALL_ITEMS.json').read_text())
for row in register['items']:
    for key in ['path','preview_path']:
        p=row.get(key,'')
        if p and (r/p).is_file():allowed.add(p)
for p in allowed:
    assert p and not p.startswith('/') and '..' not in p.split('/')
    assert not any(x.lower() in {'.git','.secrets','.codex','.claude','.aws','keystore'} for x in p.split('/'))
(r/'tmp/v2_preview_allowed.json').write_text(json.dumps(sorted(allowed),indent=2)+'\n',encoding='utf-8')
code='''from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote,urlsplit
import json,re
ROOT=Path(__file__).resolve().parents[1]
ALLOW=set(json.loads((ROOT/'tmp/v2_preview_allowed.json').read_text()))
class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*a,**kw):super().__init__(*a,directory=str(ROOT),**kw)
    def list_directory(self,path):self.send_error(404);return None
    def permitted(self):
        raw=unquote(urlsplit(self.path).path).lstrip('/')
        return raw in ALLOW and '..' not in raw.split('/') and (ROOT/raw).resolve().is_relative_to(ROOT.resolve())
    def do_GET(self):
        if not self.permitted():self.send_error(404);return
        super().do_GET()
    def do_HEAD(self):
        if not self.permitted():self.send_error(404);return
        super().do_HEAD()
    def send_head(self):
        self.byte_range=None
        path=Path(self.translate_path(self.path))
        if not path.is_file():self.send_error(404);return None
        try:f=path.open('rb')
        except OSError:self.send_error(404);return None
        size=path.stat().st_size
        requested=self.headers.get('Range')
        start,end=0,size-1
        if requested:
            match=re.fullmatch(r'bytes=(\\d*)-(\\d*)',requested.strip())
            if not match or not any(match.groups()):
                f.close();self.send_error(416);return None
            a,b=match.groups()
            if a:start=int(a);end=min(int(b),size-1) if b else size-1
            else:start=max(0,size-int(b));end=size-1
            if start<0 or start>=size or end<start:
                f.close();self.send_response(416);self.send_header('Content-Range','bytes */%d'%size);self.end_headers();return None
            self.byte_range=(start,end)
        self.send_response(206 if requested else 200)
        self.send_header('Content-Type',self.guess_type(str(path)))
        self.send_header('Accept-Ranges','bytes')
        self.send_header('Content-Length',str(end-start+1))
        if requested:self.send_header('Content-Range','bytes %d-%d/%d'%(start,end,size))
        self.send_header('Last-Modified',self.date_time_string(path.stat().st_mtime))
        self.end_headers()
        if start:f.seek(start)
        return f
    def copyfile(self,source,outputfile):
        if self.byte_range is None:return super().copyfile(source,outputfile)
        left=self.byte_range[1]-self.byte_range[0]+1
        while left:
            chunk=source.read(min(65536,left))
            if not chunk:break
            outputfile.write(chunk);left-=len(chunk)
ThreadingHTTPServer(('127.0.0.1',8880),Handler).serve_forever()
'''
(r/'tmp/serve_distinct_review_v2.py').write_text(code,encoding='utf-8')
dest=r/'audit/job_review_v2_20261001/review_tools/executed_prepare_review_v2_range_server.py'
shutil.copyfile(Path(__file__),dest)
for src,name in [('tmp/serve_distinct_review_v2.py','serve_distinct_review_v2.py'),('tmp/v2_preview_allowed.json','V2_PREVIEW_ALLOWED.json')]:
    shutil.copyfile(r/src,r/'audit/job_review_v2_20261001/review_tools'/name)
impact_path=r/'design/audit_impacts/job-review-separate-v2-20261001.json'
impact=json.loads(impact_path.read_text())
impact['files']=sorted(set(impact['files']+[dest.relative_to(r).as_posix(),'audit/job_review_v2_20261001/review_tools/serve_distinct_review_v2.py','audit/job_review_v2_20261001/review_tools/V2_PREVIEW_ALLOWED.json']))
impact['validation'].append({'command':'Exact-allowlist localhost resource and native-video byte-range checks','result':'PENDING','evidence':'Separate V2 preview binds only 127.0.0.1:8880 and explicit known review/source paths. No directory listing or project-wide disclosure. Native video seeking requires exact-byte 206 verification.'})
impact_path.write_text(json.dumps(impact,indent=2)+'\n',encoding='utf-8')
print('Prepared exact-allowlist V2 range server',len(allowed),'paths; owned server restart and verification pending.')
