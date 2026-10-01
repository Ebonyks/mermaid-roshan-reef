from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote,urlsplit
import json,re
ROOT=Path(__file__).resolve().parents[1]
ALLOW_PATH=ROOT/'tmp/v2_preview_allowed.json'
ALLOW=set()
ALLOW_MTIME=None
def refresh_allow():
    global ALLOW,ALLOW_MTIME
    stamp=ALLOW_PATH.stat().st_mtime_ns
    if stamp!=ALLOW_MTIME:
        ALLOW=set(json.loads(ALLOW_PATH.read_text()))
        ALLOW_MTIME=stamp
class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*a,**kw):super().__init__(*a,directory=str(ROOT),**kw)
    def list_directory(self,path):self.send_error(404);return None
    def permitted(self):
        refresh_allow()
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
            match=re.fullmatch(r'bytes=(\d*)-(\d*)',requested.strip())
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
