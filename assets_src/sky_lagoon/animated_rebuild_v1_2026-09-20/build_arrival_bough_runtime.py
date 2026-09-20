from pathlib import Path
import hashlib,json,runpy,shutil
P=Path(__file__).resolve().parent
W=P.parents[2]
runpy.run_path(str(P/'validate_arrival_boughs.py'))
D=W/'assets/sprites/sky_lagoon/animated_v1'
rows=[]
for source,name in [('tip-atlas.png','arrival_boughs.png'),('arrival-base-with-tips-removed.png','arrival_bough_base.png')]:
 src=P/'arrival_boughs'/source;dst=D/name;shutil.copyfile(src,dst)
 rows.append({'source':src.relative_to(W).as_posix(),'runtime':dst.relative_to(W).as_posix(),'sha256':hashlib.sha256(dst.read_bytes()).hexdigest()})
(P/'arrival_boughs/RUNTIME.json').write_text(json.dumps({'files':rows,'cell_size':[512,256],'grid':[2,2],'used_frames':3,'frame_ms':500,'master_position':[0,448],'additional_rgba_bytes_excluding_mips':6291456,'status':'opt-in runtime candidate; device/owner acceptance pending'},indent=2)+'\n')
print('ARRIVAL_BOUGHS|runtime copies validated and bound|PASS')
