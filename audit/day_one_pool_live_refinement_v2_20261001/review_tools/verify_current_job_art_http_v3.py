from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit, unquote, quote
import datetime, hashlib, json, shutil, urllib.request

r=Path(__file__).resolve().parents[1]
families=['audit/day_one_pool_live_refinement_v2_20261001','assets_src/imagegen/day1_playroom_sign_v2_20261001','audit/day_two_boxing_puff_reuse_v1_20261001']
pool=r/families[0];out=pool/'delivery_http_v3'
assert not out.exists(),'Preserve earlier delivery receipts'
out.mkdir()
targets=set()
class Links(HTMLParser):
    def handle_starttag(self,tag,attrs):
        for key,value in attrs:
            if key not in ['href','src'] or not value:continue
            u=urlsplit(urljoin('http://127.0.0.1:8877/'+self.path,value))
            if u.netloc=='127.0.0.1:8877':
                p=unquote(u.path).lstrip('/')
                if (r/p).is_file():targets.add(p)
for family in families:
    for p in (r/family).rglob('*'):
        if not p.is_file() or any(x.startswith('delivery_http_') for x in p.relative_to(r/family).parts):continue
        targets.add(p.relative_to(r).as_posix())
        if p.suffix=='.html':
            parser=Links();parser.path=p.relative_to(r).as_posix();parser.feed(p.read_text(encoding='utf-8'))
targets.add('audit/job_artwork_refinement_live/index.html')
targets.add('audit/job_artwork_refinement_live/STATUS.json')
def verify(path):
    raw=(r/path).read_bytes()
    with urllib.request.urlopen('http://127.0.0.1:8877/'+quote(path),timeout=45) as response:
        received=response.read();status=response.status
    assert status==200 and received==raw,path
    return dict(path=path,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),result='MATCH')
rows=[];failures=[]
with ThreadPoolExecutor(max_workers=4) as workers:
    jobs={workers.submit(verify,p):p for p in sorted(targets)}
    for job in as_completed(jobs):
        try:rows.append(job.result())
        except Exception as e:failures.append(dict(path=jobs[job],error=str(e)))
        if (len(rows)+len(failures))%500==0:print('CURRENT_HTTP_PROGRESS',len(rows),len(failures),len(targets),flush=True)
ranges=[]
for p in sorted((pool/'native_actions_1280_return_v6').glob('item_*_native_timestamps.mp4')):
    raw=p.read_bytes();path=p.relative_to(r).as_posix()
    for header,expected,begin,end in [('bytes=0-1023',raw[:1024],0,1023),('bytes=1024-2047',raw[1024:2048],1024,2047),('bytes=-1024',raw[-1024:],len(raw)-1024,len(raw)-1)]:
        request=urllib.request.Request('http://127.0.0.1:8877/'+quote(path),headers={'Range':header})
        with urllib.request.urlopen(request,timeout=30) as response:
            status=response.status;data=response.read();cr=response.headers.get('Content-Range')
        assert status==206 and data==expected and cr==f'bytes {begin}-{end}/{len(raw)}',path
        ranges.append(dict(path=path,range=header,status=status,content_range=cr,result='PASS'))
receipt=dict(status='PASS' if not failures else 'FAIL_PRESERVED',checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),files_verified=len(rows),bytes_verified=sum(x['bytes'] for x in rows),failures=failures,files=sorted(rows,key=lambda x:x['path']),video_byte_ranges=ranges,qualification='Exact local delivery bytes for all three current review families, direct HTML dependencies and root entry/status, plus six videos × three seek ranges. Excludes previous/fresh delivery receipts to avoid self-reference. Visual, playback, phone, remote and owner acceptance remain separate.')
(out/'RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8',newline='\n')
shutil.copyfile(Path(__file__),pool/'review_tools'/Path(__file__).name)
print(json.dumps({k:receipt[k] for k in ['status','files_verified','bytes_verified','failures']}),flush=True)
raise SystemExit(0 if not failures else 1)
