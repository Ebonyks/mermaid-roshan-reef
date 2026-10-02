from pathlib import Path
from PIL import Image
import datetime,hashlib,json,re,shutil
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');F=R/'audit/job_nursery_wash_connected_v1_20261002';O=F/'doctor_dated_full_review_v1'
ip=R/'design/audit_impacts/job-nursery-wash-connected-20261002.json'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
target=F/'review_tools'/Path(__file__).name;receipt=O/'IMAGE_LAYOUT_V380.json'
imp=read(ip);imp['files']=sorted(set(imp['files'])|{target.relative_to(R).as_posix(),receipt.relative_to(R).as_posix()});write(ip,imp);shutil.copyfile(Path(__file__),target)
p=O/'index.html';s=p.read_text(encoding='utf-8');rows=[]
def fix(m):
 tag=m.group(0);src=re.search(r'src="([^"]+)"',tag).group(1);path=(O/src).resolve();assert path.is_relative_to(R.resolve()) and path.is_file()
 with Image.open(path) as image:w,h=image.size
 rows.append({'path':path.relative_to(R).as_posix(),'width':w,'height':h,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
 assert ' width=' not in tag;return tag[:-1]+f' width="{w}" height="{h}">'
s=re.sub(r'<img\b[^>]*>',fix,s);assert len(rows)==36;p.write_text(s,encoding='utf-8',newline='\n')
write(receipt,{'status':'INTRINSIC_EVIDENCE_DIMENSIONS_DECLARED','recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'first_browser_navigation':'The click locator matched the first lazy native image but it had a zero-size layout before load. The initial click timed out without navigation.','repair':'Declare each evidence image actual intrinsic width and height, reserving its true aspect ratio before lazy loading. Native image bytes remain unchanged.','images':rows,'browser_verification':'PENDING'})
print('DOCTOR_EVIDENCE_LAYOUT|36 intrinsic image dimensions declared|all native pixels unchanged')
