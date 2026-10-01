from pathlib import Path
import hashlib, json, re, shutil

r = Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
old = Path(__file__).resolve().parent
impact_path = r/'design/audit_impacts/job-review-separate-v2-20261001.json'
impact = json.loads(impact_path.read_text(encoding='utf-8'))
impact['scope'] += ' Extend the unchanged-source diagnostic to complete local-input washing actions in both actual training and Chapter Two phase catalogs at both widths. Preserve the register browser overflow observation and repair only the separately named V2 builder/layout; complete direct sequence and refreshed browser evaluation remain pending.'
browser = r/'audit/job_review_v2_20261001/browser_review_v1'
browser.mkdir(exist_ok=True)
rows=[]
for name in ['wash_review_v2_browser_summary.png','wash_review_v2_browser_foam.png','wash_register_v2_browser.png']:
    src=old/name; dst=browser/name
    assert src.is_file() and not dst.exists()
    shutil.copyfile(src,dst)
    rows.append({'path':dst.relative_to(r).as_posix(),'sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),'source':str(src),'modifications':'Exact screenshot bytes; no crop or pixel modification.','review':'DIRECT','qualification':'Local desktop browser review, not game/device/child/owner acceptance.'})
(browser/'REVIEW.json').write_text(json.dumps({'status':'PRESERVED_PRE_CORRECTION_OBSERVATIONS','screenshots':rows,'register_failure':'Long foam source identifier extends the third card and introduces horizontal page scrolling at the observed browser width. The earlier control receipt does not establish V2 layout acceptance.','foam_review':'Source image loads and explicit source-only score is displayed; long page needs scrolling to inspect its full image.','corrected_browser_review':'PENDING'},indent=2)+'\n',encoding='utf-8')
script=r/'tmp/capture_complete_wash_v1.gd'
s=script.read_text(encoding='utf-8')
old_line='\t\t\t\t\tworld.player_animator._process(STEP)\n'
assert s.count(old_line)==1
s=s.replace(old_line,old_line+'\t\t\t\t\t# Phase/pose changes can re-enable these; keep this diagnostic at one manual tick.\n\t\t\t\t\tworld.surface.set_process(false)\n\t\t\t\t\tworld.player_animator.set_process(false)\n')
script.write_text(s,encoding='utf-8')
p=r/'tmp/run_complete_wash_v1.py';s=p.read_text(encoding='utf-8')
s=s.replace("'PASS_UNBOUND_NATIVE_CAPTURE'", "'PASS_ORIGINAL_LOCAL_INPUT_NATIVE_CAPTURE'")
s=s.replace('Local unbound fixture/process checks only.', 'Original unchanged artwork in a local-input/manual-tick fixture; process checks only.')
s=s.replace('Fresh source draft4.6 remains unbound; no runtime source change, native score or complete action, ordinary played route or owner approval.', 'Original currently bound artwork captured without replacement. Complete native sequences require direct evaluation; no ordinary root route, phone, child or owner approval.')
s=s.replace("'reuse_candidates':['assets/castle/dirty_cleanup_2d/effects/fx_soap_bubbles.png','assets_src/imagegen/day2_wash_foam_v1_20261001/attempt_02_native.png','assets_src/imagegen/day2_wash_foam_v1_20261001/attempt_02_whole_canvas_1024x608.png','assets/opera/worlds/widgets/widget_basin_shared_shine.png']", "'original_bound_artwork':['assets/opera/worlds/widgets/widget_basin_doctor_bubbles.png','assets/opera/worlds/widgets/widget_basin_nursery_bubbles.png','assets/opera/worlds/actors/animation/roshan_doctor_sheet_a.png','assets/opera/worlds/actors/animation/roshan_nursery_sheet_a.png']")
p.write_text(s,encoding='utf-8')
builder=r/'audit/job_review_v2_20261001/review_tools/build_current_job_item_register_v2.py'
s=builder.read_text(encoding='utf-8')
# Append to the current HTML template style, keeping regeneration deterministic.
assert s.count('</style>')==1
s=s.replace('</style>','.cards>*,.grid>*{min-width:0}article,.card{min-width:0}h2,h3,code,a{overflow-wrap:anywhere}img{max-width:100%}</style>')
builder.write_text(s,encoding='utf-8')
report=r/'audit/day_two_wash_bubble_reuse_v1_20261001/index.html'
s=report.read_text(encoding='utf-8')
replacements={'all28':'all 28','all20':'all 20','at1280':'at 1280','/1600':'/1600','source4.6':'source 4.6','display4.6':'display 4.6','doctor3.0':'doctor 3.0','nursery3.2':'nursery 3.2','context3.0':'context 3.0','context3.2':'context 3.2','subject2.9':'subject 2.9','subject2.2':'subject 2.2','foam1':'foam 1','foam2':'foam 2','attempt1':'attempt 1','attempt2':'attempt 2','cells0/2':'cells 0/2','firstcell':'first cell','below4.5':'below 4.5'}
for a,b in replacements.items():s=s.replace(a,b)
report.write_text(s,encoding='utf-8')
licenses=r/'ASSET_LICENSES.md';s=licenses.read_text(encoding='utf-8')
for row in rows:
    if row['path'] not in s:
        s+='\n| `'+row['path']+'` | Mermaid Roshan local browser review screenshot | Project review evidence; underlying artwork rights unchanged | Local V2 review at http://127.0.0.1:8880/; SHA-256 `'+row['sha256']+'` | Exact screenshot; no pixel changes; preserved pre-correction layout evidence; not runtime art |\n'
licenses.write_text(s,encoding='utf-8')
executed=r/'audit/job_review_v2_20261001/review_tools/executed_prepare_wash_and_browser_review_v3.py'
shutil.copyfile(Path(__file__),executed)
impact['files']=sorted(set(impact['files']+[x.relative_to(r).as_posix() for x in browser.rglob('*') if x.is_file()]+[builder.relative_to(r).as_posix(),executed.relative_to(r).as_posix()]))
impact['validation'].append({'command':'Direct browser screenshot review and V2 register overflow repair','result':'PENDING','evidence':'audit/job_review_v2_20261001/browser_review_v1/REVIEW.json preserves observed overflow; corrected layout and complete local-input washing captures pending.'})
impact_path.write_text(json.dumps(impact,indent=2)+'\n',encoding='utf-8')
print('Prepared manual single-tick wash diagnostic; preserved three directly reviewed browser observations; separate V2 layout fix pending browser verification.')
