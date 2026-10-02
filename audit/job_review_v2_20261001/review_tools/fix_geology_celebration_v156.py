from pathlib import Path
import hashlib,json,shutil
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
out=r/'audit/job_geode_runtime_v1_20261001'
impact=r/'design/audit_impacts/job-geode-painted-runtime-20261001.json'
write=lambda p,d:p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
d=json.loads(impact.read_text())
d['scope']+=' The first actual18-view ordinary career run exposes an existing completion teleport: actor rest remains the wander point under the work panel. Preserve that raw18-view failure. Capture the staged geologist task actor rest at the same position so the existing celebration tween returns visibly, without modifying input, rewards, saves, actor art or other careers. Re-run actual four-phase inputs at both widths under the new boundary.'
d['files']=sorted(set(d['files'])|{'scripts/opera_career_world_2d.gd','audit/job_review_v2_20261001/review_tools/fix_geology_celebration_v156.py','audit/job_review_v2_20261001/review_tools/run_geode_runtime_gates_v156.py','audit/job_geode_runtime_v1_20261001/ATTEMPT_01_BASELINE_REVIEW.json'})
d['rules']=sorted(set(d['rules'])|{'DL-READ-05','DL-MOT-02'})
write(impact,d)
write(out/'ATTEMPT_01_BASELINE_REVIEW.json',{'status':'PARTIAL6_OF18_DIRECT_NATIVE_REVIEW_BEFORE_CELEBRATION_FIX','views_directly_inspected':['geologist_1280_geode_'+s+'.webp' for s in ['task_open','early_crack','middle_open','full_interior_before_award','earned_completion','invitation']],
 'source_boundary':{'scripts/opera_career_world_2d.gd':hashlib.sha256((r/'scripts/opera_career_world_2d.gd').read_bytes()).hexdigest(),'scripts/opera_geology_surface.gd':hashlib.sha256((r/'scripts/opera_geology_surface.gd').read_bytes()).hexdigest()},
 'evaluation':'Actual production geode artwork is painted and crystals remain rooted4.6. Narrow/oblique/rooted full snapshots read in order4.5 provisional. Old ochre work panel4.0/procedural room2.8 remain belowfloor; distant floor-crawling work pose contact2.7. Completion actor visibly absent1.0 even though visible=true: player_position616.49,264.08 lies under opaque work panel. Invitation points at generic flat crystal mural, not the new object3.4; no source score transferred to that state.',
 'scores':{'geode_finish':4.6,'rooted_crystal_semantics':4.6,'selected_static_progression':4.5,'work_panel':4.0,'room':2.8,'work_actor_contact':2.7,'completion_actor_visibility':1.0,'invitation':3.4,'complete_action':None},'owner_acceptance':None,'qualification':'Six of18 raw native views inspected here; remaining12 not claimed. Raw originals/receipt preserved at root; new attempt02 must not overwrite them.'})
p=r/'scripts/opera_career_world_2d.gd';s=p.read_text(encoding='utf-8');needle='\tif career_id == "geologist" and task_open:\n\t\tplayer_actor.position = Vector2(30, 422)\n\t\tplayer_actor.scale = Vector2.ONE\n'
assert s.count(needle)==1
s=s.replace(needle,needle+'\t\t# Completion must celebrate at the visible task rest, not the old\n\t\t# wander position behind the opaque full-canvas work surface.\n\t\t_capture_actor_rest("player", player_actor)\n',1);p.write_text(s,encoding='utf-8',newline='\n')
p=r/'tools/capture_geode_runtime_route.gd';s=p.read_text(encoding='utf-8');s=s.replace('const OUT := "res://audit/job_geode_runtime_v1_20261001/"','const OUT := "res://audit/job_geode_runtime_v1_20261001/attempt_02/"');s=s.replace('\tassert(surface._completion_emitted and world.phase_advance_pending)','\tassert(surface._completion_emitted and world.phase_advance_pending)\n\tassert(world.player_actor.position.x < 310.0,\n\t\t"Celebration actor must remain outside the opaque work panel")');p.write_text(s,encoding='utf-8',newline='\n')
source=Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/run_geode_runtime_gates_v154.py').read_text(encoding='utf-8')
source=source.replace("arg=sys.argv[1]","arg=sys.argv[1]\naction=arg.removesuffix('v2')")
source=source.replace("'scripts/opera_geology_surface.gd','tools/capture_geode_runtime_route.gd'","'scripts/opera_geology_surface.gd','scripts/opera_career_world_2d.gd','tools/capture_geode_runtime_route.gd'")
source=source.replace('assert arg in commands','assert action in commands').replace('run_geode_runtime_gates_v154.py','run_geode_runtime_gates_v156.py').replace('commands[arg]','commands[action]')
source=source.replace("(out/'native_views').glob('*')","out.rglob('*') if p.is_file()")
source=source.replace("|{(out/('CAPTURE_'+arg[7:]+'.json')).relative_to(r).as_posix()}","")
Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/run_geode_runtime_gates_v156.py').write_text(source,encoding='utf-8',newline='\n')
shutil.copyfile(Path(__file__),r/'audit/job_review_v2_20261001/review_tools/fix_geology_celebration_v156.py')
print('Preserved first actual18 native captures; actor rest corrected, attempt02 isolated, source code must be revalidated.')
