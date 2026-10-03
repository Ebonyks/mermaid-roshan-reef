from pathlib import Path
import json,hashlib,datetime,shutil,subprocess
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');J=R/'audit/job_geology_painted_fracture_trial_v1_20261003';K=R/'audit/job_geology_fossil_reveal_continuity_v1_20261003'
BASE='c5977ebb29bb2011b20fc149ad350290f045045c'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()==BASE
assert not K.exists();K.mkdir();(K/'review_tools').mkdir();(K/'attempt01').mkdir();(K/'.gdignore').write_text('',encoding='utf-8')
prev=read(J/'SOURCE_CURRENT_BEFORE_CAPTURE.json');assert len(prev['source_files'])==783 and all(sha(R/x['path'])==x['sha256'] for x in prev['source_files'])
write(K/'SOURCE_CURRENT_BEFORE_CAPTURE.json',dict(prev,baseline=BASE,created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),qualification='Exact783 literal production boundary before new non-runtime reveal/home placement study; current production unchanged.'))
rules=read(R/'design/audit_impacts/job-geology-painted-fracture-trial-20261003.json')['rules']
piece_width=234*802/674/3;home_spacing=141;hit_width=piece_width+48
assert home_spacing>hit_width
write(K/'PLAN.json',{'baseline':BASE,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'rules':rules,'findings':['MA-VIS-006','MA-PLAY-004','MA-OPERA-012'],'named_gap':'Current whole fossil3.2; fracture A2 whole3.6. Last brush threshold replaces an intact-looking fossil with three pieces at distant homes (transition3.2).','reuse_inventory':[{'path':'assets/opera/worlds/geology/painted_work_v1_20261001/fossil.png','sha256':sha(R/'assets/opera/worlds/geology/painted_work_v1_20261001/fossil.png'),'status':'Existing painted material4.5, unchanged; three complementary A2 pieces4.5 provisional.'},{'path':J.relative_to(R).as_posix()+'/painted_fracture_surface.gd','sha256':sha(J/'painted_fracture_surface.gd'),'status':'Reuse exact reviewed A2 texture partitions and exposed-edge/snap suppression.'},{'path':'scripts/opera_geology_surface.gd','sha256':sha(R/'scripts/opera_geology_surface.gd'),'status':'Inherited one-finger input,40-cell/26-clear threshold, targets, progress, JSON restore, completion; current production byte unchanged.'}],'change':'Non-runtime subclass changes only fossil piece home placement and stage0 underlying drawing. Show already-broken pieces at the same home positions before/after soil clearing, with original painted soil/brush drawing over them. Do not invent a fracture after uncovering or move the pieces automatically. Keep inherited target/snap/input/save/completion behavior; home placement is explicitly changed, not labeled draw-only.','homes':[[639,400],[780,400],[921,400]],'hit_width_including_unchanged_24px_margin':hit_width,'home_center_spacing':home_spacing,'minimum_horizontal_hit_gap':home_spacing-hit_width,'required_evidence':'Fresh parser/inference/officialGodot4.7.2 analyzers and actual Library all4 phases/earned return/elevator replay/Back at both widths. Every input/wait fossil frame and selected native canvas directly reviewed, item opinions, stage-threshold pairs, original783 hashes. Source/material/geometry does not predict a visual/action pass.','known_unrepaired':'Coarse brush-cell edges and remaining dirt threshold disappearance, ghost-target overlap, remote working hands2.7, room2.8, generic completion. No predicted score or whole-action acceptance.','production_binding':False,'owner_acceptance':None})
surface='''extends "res://audit/job_geology_painted_fracture_trial_v1_20261003/painted_fracture_surface.gd"
## NON_RUNTIME_REVEAL_HOME_STUDY: existing painted fracture material unchanged.
## Broken pieces are under the soil at their actual assembly homes throughout.
## Only home placement/underlying stage0 presentation change; inherited input,
## targets, margins, state format, progress and world completion remain intact.

func fossil_piece_home(index: int) -> Vector2:
\treturn Vector2(639.0 + float(clampi(index, 0, 2)) * 141.0, 400.0)

func _draw_fossil() -> void:
\tif fossil_stage != 0:
\t\tsuper._draw_fossil()
\t\treturn
\tfor index: int in range(3):
\t\t_draw_fossil_piece(index,
\t\t\tRect2(fossil_piece_home(index) - FOSSIL_PIECE_SIZE * 0.5, FOSSIL_PIECE_SIZE))
\tvar cell_size := Vector2(FOSSIL_RECT.size.x / float(FOSSIL_GRID_COLS),
\t\tFOSSIL_RECT.size.y / float(FOSSIL_GRID_ROWS))
\tfor row: int in range(FOSSIL_GRID_ROWS):
\t\tfor column: int in range(FOSSIL_GRID_COLS):
\t\t\tvar index: int = row * FOSSIL_GRID_COLS + column
\t\t\tif not fossil_cleared[index] and _fossil_soil_texture != null:
\t\t\t\tvar source_cell := _fossil_soil_texture.get_size() \\
\t\t\t\t\t/ Vector2(FOSSIL_GRID_COLS, FOSSIL_GRID_ROWS)
\t\t\t\tdraw_texture_rect_region(_fossil_soil_texture,
\t\t\t\t\tRect2(FOSSIL_RECT.position + Vector2(column, row) * cell_size,
\t\t\t\t\t\tcell_size), Rect2(Vector2(column, row) * source_cell, source_cell))
\tif held:
\t\t_draw_brush(pointer_pos)
'''
(K/'reveal_surface.gd').write_text(surface,encoding='utf-8',newline='\n')
c=(J/'capture.gd').read_text(encoding='utf-8-sig')
c=c.replace('inherited fossil draw override only','inherited fossil reveal/home placement study').replace('original mechanics and pixels remain','original material/input/save/completion remain; homes intentionally change')
c=c.replace('res://audit/job_geology_painted_fracture_trial_v1_20261003/attempt02/','res://audit/job_geology_fossil_reveal_continuity_v1_20261003/attempt01/')
c=c.replace('res://audit/job_geology_painted_fracture_trial_v1_20261003/painted_fracture_surface.gd','res://audit/job_geology_fossil_reveal_continuity_v1_20261003/reveal_surface.gd')
c=c.replace('NON_RUNTIME_COUNTERFACTUAL_FRACTURE_DRAW_ONLY_SUBSTITUTION','NON_RUNTIME_FOSSIL_REVEAL_HOME_PLACEMENT_SUBSTITUTION').replace('COUNTERFACTUAL_DRAW_ONLY_COMPLETE_FOSSIL_ALL4_EARNED_RETURN_REVIEW_PENDING','NON_RUNTIME_REVEAL_HOME_COMPLETE_FOSSIL_ALL4_EARNED_RETURN_REVIEW_PENDING')
c=c.replace('Explicit non-runtime inherited fossil draw-only surface substitution. Original pixels/mechanics/targets retained.','Explicit non-runtime reveal/home placement substitution. Already-broken painted pieces are under soil at the same homes through reveal. Homes639/780/921 at y400 intentionally changed; original material/input/targets/24px margins/state/completion retained. Coarse cell removal/remaining threshold soil/remote hand contact/room are unrepaired. No predicted quality score.')
(K/'capture.gd').write_text(c,encoding='utf-8',newline='\n')
runner=(J/'review_tools/run_geology_fracture_trial_v465.py').read_text(encoding='utf-8-sig')
runner=runner.replace("J=R/'audit/job_geology_painted_fracture_trial_v1_20261003'","J=R/'audit/job_geology_fossil_reveal_continuity_v1_20261003'").replace("G=J/'runtime_gate_a2'","G=J/'runtime_gate_a1'").replace("J/'attempt02'","J/'attempt01'").replace("+'_v465'","+'_v478'").replace('painted_fracture_surface.gd','reveal_surface.gd').replace('job-geology-painted-fracture-trial-20261003.json','job-geology-fossil-reveal-continuity-20261003.json')
compile(runner,'run_geology_reveal_continuity_v478.py','exec');(K/'review_tools/run_geology_reveal_continuity_v478.py').write_text(runner,encoding='utf-8',newline='\n');shutil.copyfile(K/'review_tools/run_geology_reveal_continuity_v478.py',Path(__file__).with_name('run_geology_reveal_continuity_v478.py'))
shutil.copyfile(Path(__file__),K/'review_tools'/Path(__file__).name)
ip=R/'design/audit_impacts/job-geology-fossil-reveal-continuity-20261003.json'
write(ip,{'id':'job-geology-fossil-reveal-continuity-20261003','baseline':BASE,'scope':'Explicit non-runtime fossil reveal/home placement comparison; reuse exact A2 original painted material and fracture contours. Show already-broken fragments under soil at their unchanged-through-reveal homes639/780/921,y400; retain actual one-finger input/targets/24px margins/state/progress/normal world callbacks. Homes change explicitly, not draw-only. No source bitmap editing/regeneration, forced results, production changes or predicted quality pass. Capture complete action/actual earned route at both aspects; preserve failures and all783 production hashes.','rules':rules,'findings':['MA-VIS-006','MA-PLAY-004','MA-OPERA-012'],'files':sorted(x.relative_to(R).as_posix() for x in K.rglob('*') if x.is_file()),'validation':[{'command':'Fresh parser/inference/officialGodot4.7.2 analyzers and actual input captures at1280/1600','result':'PENDING','evidence':K.relative_to(R).as_posix()+'/PLAN.json'},{'command':'Every native frame/view direct review plus independent individual/transition/action opinions','result':'PENDING','evidence':'No predicted score; full direct review required.'}],'acceptance_gaps':'Current production, coarse dirt clearing/threshold disappearance, ghost target, working hands/room/completion, natural pacing, ordinary story travel, target device/child/owner/all-job/finding closure/integration/release remain open. U published review still undergoing anonymous byte verification; no new K publication/acceptance claim.'})
print(json.dumps({'status':'NAMED_REVEAL_HOME_TRIAL_PREPARED_NO_PREDICTED_SCORE','homes':[[639,400],[780,400],[921,400]],'hit_gap':home_spacing-hit_width,'production_unchanged':783,'baseline':BASE}))
