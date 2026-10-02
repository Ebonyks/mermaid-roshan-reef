from pathlib import Path
import json,shutil
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
f=r/'audit/job_geology_painted_work_v1_20261001'
assert (f/'runtime_gate/capture1600.receipt.json').is_file()
assert json.loads((f/'runtime_gate/capture1600.receipt.json').read_text())['status']=='PASS'
p=r/'design/audit_impacts/job-geology-painted-work-20261001.json';d=json.loads(p.read_text());d['scope']+=' First mounted36-view run exposes a clipped1100px fossil slab and actor-overlapped invitations. Preserve all36 native first-attempt bytes. Uniform900px slab stays within canvas; fossil homes450 and brush extent215 retain height/indices and conserved aspect while sitting on the work surface. Local invitation offsets separate props from the unchanged actor/approach; ordinary routes must still pass. New attempt02 adds actual held-brush, one/two-piece and alternating-pan still states.';p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
surface=r/'scripts/opera_geology_surface.gd';s=surface.read_text();s=s.replace('Rect2(500.0, 165.0, 560.0, 300.0)','Rect2(500.0, 215.0, 560.0, 300.0)').replace('* 245.0, 560.0)','* 245.0, 450.0)').replace('var slab_width := 1100.0 if mode == "geology_fossil" else 860.0','var slab_width := 900.0 if mode == "geology_fossil" else 860.0').replace('var slab_center := Vector2(760.0, 450.0) if mode == "geology_fossil" \\\n\t\t\telse Vector2(760.0, 400.0)','var slab_center := Vector2(760.0, 400.0)');surface.write_text(s,encoding='utf-8')
catalog=r/'scripts/opera_hotspot_catalog.gd';s=catalog.read_text();lines=s.splitlines()
for i,line in enumerate(lines):
 if '"FOSSIL":' in line and 'painted_work_v1' in line:lines[i]=line.replace('"presentation": "overlay"','"offset": Vector2(80, -90), "presentation": "overlay"')
 if '"PAN":' in line and 'painted_work_v1' in line:lines[i]=line.replace('"presentation": "overlay"','"offset": Vector2(70, -90), "presentation": "overlay"')
catalog.write_text('\n'.join(lines)+'\n',encoding='utf-8')
capture=f/'capture_geology_painted_work.gd';s=capture.read_text().replace('/attempt_01/','/attempt_02/')
s=s.replace('\t\t\t\tat = next\n\t\t\tawait _surface_touch(surface, at, false)', '\t\t\t\tat = next\n\t\t\t\tif row == 0:\n\t\t\t\t\tawait _capture(world, "partial_brush")\n\t\t\tawait _surface_touch(surface, at, false)',1)
s=s.replace('\t\t\t\tawait _surface_touch(surface, surface.fossil_piece_target(piece), false)','\t\t\t\tawait _surface_touch(surface, surface.fossil_piece_target(piece), false)\n\t\t\t\tif piece < 2:\n\t\t\t\t\tawait _capture(world, "one_piece" if piece == 0 else "two_pieces")')
s=s.replace('\t\t\t\tif swing == 3:', '\t\t\t\tif swing < 2:\n\t\t\t\t\tawait _capture(world, "pan_right" if swing == 0 else "pan_left")\n\t\t\t\tif swing == 3:')
capture.write_text(s,encoding='utf-8');(f/'attempt_02').mkdir();shutil.copyfile(__file__,f/'review_tools'/Path(__file__).name)
d=json.loads(p.read_text());d['files']=sorted(set(d['files'])|{x.relative_to(r).as_posix() for x in f.rglob('*') if x.is_file()});p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
print('Preserved first attempt; refined actual fossil support/invitation positions and expanded current capture.')
