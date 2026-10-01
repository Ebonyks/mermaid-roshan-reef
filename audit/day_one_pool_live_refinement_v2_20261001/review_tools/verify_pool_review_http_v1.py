from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit, unquote
import datetime, hashlib, json, shutil, urllib.request

root=Path(__file__).resolve().parents[1];family=root/'audit/day_one_pool_live_refinement_v2_20261001'
out=family/'delivery_http_v1';assert not out.exists(),'Preserve earlier HTTP evidence.';out.mkdir()
targets=set()
class Links(HTMLParser):
 def handle_starttag(self,tag,attrs):
  for key,value in attrs:
   if key not in ['href','src'] or not value:continue
   url=urlsplit(urljoin('http://127.0.0.1:8877/'+self.path,value))
   if url.netloc=='127.0.0.1:8877':targets.add(unquote(url.path).lstrip('/'))
parser=Links();parser.path=(family/'index.html').relative_to(root).as_posix();parser.feed((family/'index.html').read_text())
targets.add(parser.path);targets.add((family/'REVIEW.json').relative_to(root).as_posix())
for name in ['native_actions_1280_return_v6','native_actions_1600_fairy_return_v2','native_actions_1600_huluu_return_v2']:
 targets.update(p.relative_to(root).as_posix() for p in (family/name).glob('frame_*.webp'))
targets.update(p.relative_to(root).as_posix() for p in (family/'native_actions_1280_return_v6/inspection_boards').glob('*.webp'))
def verify(path):
 raw=(root/path).read_bytes()
 with urllib.request.urlopen('http://127.0.0.1:8877/'+path,timeout=30) as response:
  received=response.read();status=response.status
 assert status==200 and received==raw,path
 return {'path':path,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'result':'MATCH'}
rows=[]
with ThreadPoolExecutor(max_workers=4) as workers:
 for job in as_completed([workers.submit(verify,p) for p in sorted(targets)]):
  rows.append(job.result())
  if len(rows)%300==0:print(f'POOL_HTTP_PROGRESS|{len(rows)}/{len(targets)}',flush=True)
ranges=[]
for p in sorted((family/'native_actions_1280_return_v6').glob('item_*_native_timestamps.mp4')):
 raw=p.read_bytes();path=p.relative_to(root).as_posix()
 request=urllib.request.Request('http://127.0.0.1:8877/'+path,headers={'Range':'bytes=0-1023'})
 with urllib.request.urlopen(request,timeout=30) as response:
  data=response.read();status=response.status;content_range=response.headers.get('Content-Range')
 assert status==206 and data==raw[:1024] and content_range==f'bytes 0-1023/{len(raw)}',path
 ranges.append({'path':path,'result':'PASS','status':status,'content_range':content_range,'bytes':len(data)})
receipt={'status':'PASS','checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'files_verified':len(rows),'bytes_verified':sum(r['bytes'] for r in rows),'files':sorted(rows,key=lambda r:r['path']),
 'video_byte_ranges':ranges,'qualification':'Local delivery bytes and six media seek ranges only. Browser table/slider/board checks are separate; this establishes no visual, continuous-playback, remote or owner acceptance.'}
(out/'RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
shutil.copyfile(Path(__file__),family/'review_tools'/Path(__file__).name)
impact=root/'design/audit_impacts/day-one-pool-live-refinement-v2-20261001.json';d=json.loads(impact.read_text())
d['files']=sorted(set(d['files'])|{p.relative_to(root).as_posix() for p in family.rglob('*') if p.is_file()})
d['validation'].append({'command':'Current local illustrated entry links/native frames/ordered boards/video byte ranges','result':'PASS','evidence':'audit/day_one_pool_live_refinement_v2_20261001/delivery_http_v1/RECEIPT.json; every verified path has exact-byte comparison.'})
impact.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
print(f'POOL_HTTP|PASS|{len(rows)} exact files|{len(ranges)} media byte ranges|{receipt["bytes_verified"]} bytes',flush=True)
