from pathlib import Path
from PIL import Image
import datetime,hashlib,html,json,re,shutil
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');f=r/'audit/job_geode_route_emblem_runtime_v1_20261002'
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
p=f/'index.html';s=p.read_text(encoding='utf-8');shutil.copyfile(p,f/'index_LAYOUT_BEFORE_V289.html')
rows=[]
def fix(m):
 tag=m.group();src=html.unescape(re.search(r'\bsrc="([^"]+)"',tag).group(1));im=(f/src).resolve()
 assert im.is_relative_to(r.resolve()) and im.is_file(),src
 with Image.open(im) as image:w,h=image.size
 rows.append(dict(path=im.relative_to(r).as_posix(),width=w,height=h))
 return tag[:-1]+f' width="{w}" height="{h}">'
s=re.sub(r'<img\b[^>]*>',fix,s);p.write_text(s,encoding='utf-8',newline='\n')
write(f/'LAYOUT_STABILITY_V289.json',dict(status='INTRINSIC_CANVAS_EXTENTS_ADDED_BROWSER_RECHECK_PENDING',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),images=rows,qualification='Read-only image dimensions added to report HTML to reserve lazy image layout. No artwork edits. Initial browser control actions unexpectedly navigated to the last menu image; unreserved image layout is a suspected contributor, not a proven browser root cause. Corrected control must be rechecked.'))
shutil.copyfile(Path(__file__),f/'review_tools'/Path(__file__).name)
ip=r/'design/audit_impacts/job-geode-route-emblem-runtime-20261002.json';d=json.loads(ip.read_text());d['files']=sorted(set(d['files'])|{p.relative_to(r).as_posix() for p in f.rglob('*') if p.is_file()});write(ip,d)
allow=r/'tmp/v2_preview_allowed.json';write(allow,sorted(set(json.loads(allow.read_text()))|set(d['files'])))
print('Reserved exact dimensions for',len(rows),'report images; native pixels unchanged. Browser recheck pending.')
