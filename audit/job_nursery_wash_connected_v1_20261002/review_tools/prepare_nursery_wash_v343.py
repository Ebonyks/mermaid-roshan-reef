from pathlib import Path
import datetime, hashlib, json, subprocess
from PIL import Image
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
F=R/'audit/job_nursery_wash_connected_v1_20261002'
S=R/'assets_src/imagegen/nursery_wash_connected_v1_20261002'
for p in [F,S]:
    assert not p.exists(), p
    p.mkdir(parents=True)
    (p/'.gdignore').write_text('')
(F/'review_tools').mkdir()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
refs=['assets/opera/worlds/actors/roshan_nursery.png','assets/opera/worlds/actors/animation/roshan_nursery_sheet_a.png','assets_src/concepts/opera_nursery_2026-08-01/roshan_nursery_nurse_alpha.png','assets/opera/worlds/widgets/widget_basin_nursery.png','assets/opera/worlds/widgets/widget_basin_nursery_bubbles.png','assets_src/imagegen/day2_wash_foam_v1_20261001/attempt_02_native.png']
refs += [p.relative_to(R).as_posix() for p in (R/'assets/opera/worlds/nursery/refinement_v2').glob('*') if p.is_file() and not p.name.endswith('.import')]
inventory=[]
for p in refs:
    row={'path':p,'sha256':sha(R/p),'bytes':(R/p).stat().st_size}
    if p.endswith('.png'):
        with Image.open(R/p) as im: row.update(dimensions=list(im.size),mode=im.mode)
    row['reuse_decision']='Preserve own Nursery identity or current connected catch source; cannot supply wet/rub/rinse/clean washing poses.'
    if 'widget_basin_nursery.png' in p:row['reuse_decision']='Directly viewed: framed baby clipboard, not a washing basin. Unsuitable as live washing subject.'
    if 'day2_wash_foam' in p:row['reuse_decision']='Directly viewed painted foam; reusable style/material reference, no connected hands, sink or rinse action.'
    inventory.append(row)
rules=['DL-AUTH-05','DL-AUTH-06','DL-AUTH-07','DL-ASSET-01','DL-ASSET-02','DL-ASSET-03','DL-ASSET-04','DL-ASSET-05','DL-ASSET-06','DL-MED-01','DL-VIS-01','DL-VIS-02','DL-VIS-03','DL-VIS-05','DL-VIS-06','DL-VIS-07','DL-VIS-08','DL-LAY-07','DL-INT-01','DL-INT-02','DL-INT-03','DL-INT-04','DL-INT-06','DL-INT-12','DL-MOT-01','DL-MOT-03','DL-MOT-10','DL-MOT-11','DL-MOT-12','DL-MOT-13','DL-SAVE-01','DL-SAVE-02','DL-QA-01','DL-QA-02','DL-QA-03','DL-QA-06']
baseline=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()
scope='Reproduce and reversibly repair Nursery WASH in actual training and authored catalog contexts at 1280x720/1600x720. Current source derives nonempty nursery widget template and returns before the nursery_wash contextual draw, leaving empty work subject despite earned hold progress. Preserve input, progress ownership, rewards, saves, protected originals and sibling phases. Inventory existing Nursery identity/care/sink/foam first; generate only missing own-costume connected wet/rub/rinse/clean work states, preserving every candidate. Evaluate sources, actual mounted subjects and entire meaningful action separately. Nursery and Doctor are absent from ChapterTwoPartyPlan actual birthday route; catalog fixture must never be called ordinary birthday gameplay.'
plan={'status':'IN_PROGRESS','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'baseline':baseline,'scope':scope,'rules':rules,'findings':['MA-VIS-006','MA-PLAY-004','MA-OPERA-012'],'inventory':inventory,'required_evidence':['Fresh unchanged native route/hold/earned completion/next-phase sequences, all eight doctor/nursery context/aspect cases.','Exact source/prompt/reference/native-alpha hashes, every rejected attempt, separate per-item direct visual opinions.','Real production room card entry and touch approach; whole meaningful washing action, release/settle/next phase at both aspects.','Parser/inference/official Godot4.7.2 import/analyzer; unmodified complete CI; document authority/development/2D gates.','Published durable topic-branch review packet with immutable manifest, anonymous exact remote byte verification.'],'acceptance_gaps':'No owner/device/child acceptance. Catalog scope is not a normal birthday route. Static sources alone do not pass contact/motion/whole-action; all <=4.5 remain priority and 4.5 is a provisional floor.'}
(F/'PLAN.json').write_text(json.dumps(plan,indent=2)+'\n',encoding='utf-8')
(S/'PLAN.json').write_text(json.dumps(plan,indent=2)+'\n',encoding='utf-8')
old=R/'audit/day_two_wash_complete_action_v1_20261001/root_route_attempt_03'
fixture=(old/'executed_capture_wash_root_route_v3.gd').read_text(encoding='utf-8').replace('res://tmp/wash_root_route_v3/native_frames/','res://audit/job_nursery_wash_connected_v1_20261002/baseline_capture/native_frames/')
(R/'tmp/capture_nursery_wash_baseline_v343.gd').write_text(fixture,encoding='utf-8')
(F/'review_tools/capture_baseline_v343.gd').write_text(fixture,encoding='utf-8')
runner=(old/'executed_run_wash_root_route_v3.py').read_text(encoding='utf-8').replace("r/'tmp/wash_root_route_v3'","r/'audit/job_nursery_wash_connected_v1_20261002/baseline_capture'").replace('audit/job_review_v2_20261001/full_ci_candidate_retry_v2/SOURCE_BEFORE.json','audit/job_geode_supported_celebration_v1_20261002/full_ci_v3/SOURCE_BEFORE.json').replace('tmp/capture_wash_root_route_v3.gd','tmp/capture_nursery_wash_baseline_v343.gd')
(F/'review_tools/run_baseline_v343.py').write_text(runner,encoding='utf-8')
impact={'id':'job-nursery-wash-connected-20261002','scope':scope,'baseline':baseline,'rules':rules,'findings':['MA-VIS-006','MA-PLAY-004','MA-OPERA-012'],'files':[p.relative_to(R).as_posix() for parent in [F,S] for p in parent.rglob('*') if p.is_file()],'validation':[{'command':'Current source/reuse inventory and fresh baseline capture','result':'PENDING','evidence':F.relative_to(R).as_posix()+'/PLAN.json'}],'acceptance_gaps':plan['acceptance_gaps']}
(R/'design/audit_impacts/job-nursery-wash-connected-20261002.json').write_text(json.dumps(impact,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'baseline':baseline,'review':str(F),'source':str(S),'reuse_files':len(inventory)}))
