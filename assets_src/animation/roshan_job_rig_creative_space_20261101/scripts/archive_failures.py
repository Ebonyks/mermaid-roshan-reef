"""Preserve exact rejected native captures without altering pixels or test floors."""
from pathlib import Path
import hashlib,json,shutil
from PIL import Image
import audit_study as audit

P=Path(__file__).resolve().parents[1]
RAW=P/'evidence/raw';OUT=P/'review/failures';OUT.mkdir(exist_ok=True)
rows=[]
for theme,clip,isolated in [('painter','tail_bend',False),('astronaut','tail_bend',False),('painter','paint_banner',True),('astronaut','turn_valve',True)]:
    folder=(RAW/'jobs_isolated'/theme/clip) if isolated else RAW/theme/clip
    paths=sorted(folder.glob('*.png'))
    reference=audit.pixel_checks(Image.open(paths[0]).convert('RGBA'))
    measured=[(f,audit.pixel_checks(Image.open(f).convert('RGBA'))) for f in paths]
    failures=[(f,m) for f,m in measured if not audit.seam_pass(m,reference)]
    selected={paths[0],paths[-1],paths[min(33,len(paths)-1)]}
    if failures:
        selected|={failures[0][0],failures[-1][0],max(failures,key=lambda x:(x[1]['large_components'],x[1]['interior_hole_pixels']))[0]}
    exact=[]
    for f in sorted(selected):
        target=OUT/(theme+'_'+clip+'_'+f.name);shutil.copy2(f,target)
        exact.append(dict(path=target.relative_to(P).as_posix(),source_build_path=f.relative_to(P).as_posix(),sha256=hashlib.sha256(target.read_bytes()).hexdigest(),frame=int(f.stem),time_s=int(f.stem)/30,pixel_metrics=dict(measured)[f]))
    rows.append(dict(theme=theme,clip=clip,isolated_actor=isolated,frames=len(paths),failing_seam_frames=len(failures),failure_indices=[int(f.stem) for f,m in failures],reference=reference,selected_exact_captures=exact))
(OUT/'index.json').write_text(json.dumps(dict(rows=rows,method='Unchanged audit_study pixel_checks/seam_pass; native PNG copies, no resizing, repair or recompression',limits='Selected diagnostic frames and complete failure-index lists; no full-speed or acceptance claim.'),indent=2)+'\n',encoding='utf8')
print('ARCHIVED REJECTED NATIVE CASES',sum(len(x['selected_exact_captures']) for x in rows))
