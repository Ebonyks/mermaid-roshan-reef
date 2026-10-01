from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote,quote
from urllib.request import Request,urlopen
from concurrent.futures import ThreadPoolExecutor
import datetime,hashlib,json,posixpath,shutil

r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
out=r/'audit/job_review_v2_20261001/resource_checks_v1';assert not out.exists();out.mkdir()
class Links(HTMLParser):
    def __init__(self):super().__init__();self.links=[]
    def handle_starttag(self,tag,attrs):
        for key,value in attrs:
            if key in ['src','href','poster'] and value:self.links.append(value)
pages=['audit/job_review_v2_20261001/index.html','audit/day_two_wash_bubble_reuse_v1_20261001/index.html','audit/job_artwork_refinement_live/index.html','audit/job_artwork_refinement_live/all_items.html','audit/day_one_pool_live_refinement_v2_20261001/index.html','audit/day_two_boxing_live_refinement_v1_20261001/index.html']
paths=set(pages)
for page in pages:
    parser=Links();parser.feed((r/page).read_text(encoding='utf-8'))
    for link in parser.links:
        u=urlsplit(link)
        if u.scheme or not u.path:continue
        p=posixpath.normpath(posixpath.join(posixpath.dirname(page),unquote(u.path)))
        assert not p.startswith('../') and not p.startswith('/')
        paths.add(p)
register=json.loads((r/'audit/job_artwork_refinement_live/ALL_ITEMS.json').read_text())
for row in register['items']:
    for key in ['path','preview_path']:
        p=row.get(key,'')
        if p:paths.add(p)
def head(p):
    try:
        with urlopen(Request('http://127.0.0.1:8880/'+quote(p,safe='/'),method='HEAD'),timeout=20) as response:
            size=(r/p).stat().st_size
            ok=response.status==200 and int(response.headers['Content-Length'])==size
            return {'path':p,'status':response.status,'bytes':size,'pass':ok}
    except Exception as error:return {'path':p,'pass':False,'error':str(error)}
with ThreadPoolExecutor(max_workers=8) as pool:rows=list(pool.map(head,sorted(paths)))
videos=sorted(p for p in json.loads((r/'tmp/v2_preview_allowed.json').read_text()) if p.startswith('audit/day_one_pool_live_refinement_v2_20261001/') and p.endswith('.mp4'))
assert len(videos)==6
ranges=[]
for p in videos:
    size=(r/p).stat().st_size
    for start in [0,size//2,max(0,size-4096)]:
        end=min(start+4095,size-1)
        with (r/p).open('rb') as f:f.seek(start);expected=f.read(end-start+1)
        with urlopen(Request('http://127.0.0.1:8880/'+quote(p,safe='/'),headers={'Range':'bytes=%d-%d'%(start,end)}),timeout=20) as response:
            actual=response.read();header=response.headers.get('Content-Range')
            ranges.append({'path':p,'start':start,'end':end,'status':response.status,'content_range':header,'sha256':hashlib.sha256(actual).hexdigest(),'pass':response.status==206 and header=='bytes %d-%d/%d'%(start,end,size) and actual==expected})
result={'status':'PASS' if all(x['pass'] for x in rows+ranges) else 'FAIL_PRESERVED','checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'server':'http://127.0.0.1:8880','resource_head_count':len(rows),'resource_heads':rows,'native_video_ranges':ranges,'qualification':'Local declared entry/report/source-preview resource reachability and exact-byte range checks only; not remote publication, visual acceptance or exhaustive runtime use. Original sourceA remote receipt stays separately pinned.'}
(out/'RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
shutil.copyfile(Path(__file__),out/'executed_check_distinct_review_resources_v2.py')
p=r/'design/audit_impacts/job-review-separate-v2-20261001.json';d=json.loads(p.read_text());d['files']=sorted(set(d['files']+[x.relative_to(r).as_posix() for x in out.rglob('*') if x.is_file()]));d['validation'].append({'command':'check_distinct_review_resources_v2.py','result':'PASS' if result['status']=='PASS' else 'FAIL','evidence':'audit/job_review_v2_20261001/resource_checks_v1/RECEIPT.json; '+str(len(rows))+' declared resources and 18 exact native video 206 slices. Local reachability only.'});p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':result['status'],'resources':len(rows),'failed':[x for x in rows if not x['pass']],'video_ranges':len(ranges)}))
raise SystemExit(0 if result['status']=='PASS' else 1)
