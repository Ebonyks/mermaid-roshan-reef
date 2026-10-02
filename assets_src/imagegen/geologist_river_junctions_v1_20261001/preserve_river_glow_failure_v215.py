from pathlib import Path
import datetime, hashlib, json, shutil
from PIL import Image
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');s=b/'assets_src/imagegen/geologist_river_junctions_v1_20261001';a=s/'dry_attempt_05'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();now=datetime.datetime.now(datetime.timezone.utc).isoformat()
src=Path('C:/Users/Peter/.codex/generated_images/01a0f309-110a-7602-af22-f30d657bd017/exec-f12c0a02-9f76-4a57-ad59-73a8c5bb27f8.png');dst=a/'native_generated.png';assert not dst.exists();shutil.copyfile(src,dst);assert sha(src)==sha(dst);im=Image.open(dst)
p=read(a/'GENERATION_PENDING.json');p.update(status='GENERATED_EXTERIOR_CLEANUP_FAILED_DIRECT_SOURCE3_8',generator_original_path=str(src),native_path=dst.relative_to(b).as_posix(),native_sha256=sha(dst),native_dimensions=list(im.size),native_mode=im.mode,pixel_modifications='None; exact generated complete original.');write(a/'PROVENANCE.json',p)
d=read(s/'dry_attempt_04/REVIEW.json');d.update(native_path=dst.relative_to(b).as_posix(),sha256=sha(dst),source_dimensions=list(im.size),reviewed_utc=now,qualification='A5 lightens bank painting but retains large brown/lavender exterior glow; complete source3.8 rejected. No normalization or runtime binding.')
for x in d['components']:
 x.update(id=x['id'].replace('A04','A05'),path=dst.relative_to(b).as_posix(),sha256=sha(dst),source_dimensions=list(im.size),reviewed_utc=now,evaluation='The raised banks now have brighter cream/gold value bands, material4.5 provisional. However, broad brown/lavender glow still surrounds the solid object; complete component3.8 is rejected. Actual repeat-fit remains unreviewed. No manual pixel cleanup or runtime binding.')
write(a/'REVIEW.json',d);shutil.copyfile(__file__,s/Path(__file__).name)
ip=b/'design/audit_impacts/job-geology-river-junction-source-20261001.json';d=read(ip);d['files']=sorted(set(d['files'])|{x.relative_to(b).as_posix() for x in s.rglob('*') if x.is_file()});write(ip,d)
print('Preserved failed cleanup',sha(dst),im.size)
