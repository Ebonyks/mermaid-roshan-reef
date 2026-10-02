from pathlib import Path
import json, shutil
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');f=b/'audit/job_geology_river_runtime_v1_20261002';prefix=f.relative_to(b).as_posix()
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
ip=b/'design/audit_impacts/job-geology-river-painted-runtime-20261002.json';d=read(ip);d['scope']+=' Add unmodified actual-renderer arbitrary network fixtures and a continuous native geode-opening capture, using ordinary four-phase viewport input progression. Geode timing fixture removes capture freezes and the explicit restore test only, does not change production source/input/save or force phases. Every generated capture must be individually reviewed before giving any action opinion.';write(ip,d)
code=(f/'capture_geology_river_runtime.gd').read_text(encoding='utf-8').replace(prefix+'/attempt_01/',prefix+'/timed_attempt_01/')
code=code.replace('var events: Array[Dictionary] = []','var events: Array[Dictionary] = []\nvar motion_world: OperaCareerWorld2D\nvar record_motion := false\nvar motion_frames: Array[Dictionary] = []')
code=code.replace('await process_frame\n','await process_frame\n\t\tif record_motion:\n\t\t\tawait RenderingServer.frame_post_draw\n\t\t\t_motion_frame()\n',1)
start=code.index('func _freeze(');end=code.index('func _open(',start)
code=code[:start]+'''func _motion_frame() -> void:
\tvar index := motion_frames.size()
\tvar path := OUT + "native_views/geode_%d_%04d.webp" % [width_now,index]
\tvar image := root.get_texture().get_image()
\tassert(image.save_webp(path,true) == OK)
\tvar surface := motion_world.surface as OperaGeologySurface
\tmotion_frames.append({"index":index,"path":path.trim_prefix("res://"),"sha256":FileAccess.get_sha256(path),
\t\t"width":width_now,"time_msec":Time.get_ticks_msec(),"pull":surface.geode_pull,
\t\t"surface":surface.progress_snapshot(),"actor_position":[motion_world.player_actor.position.x,motion_world.player_actor.position.y],
\t\t"phase_index":motion_world.phase_index,"direct_review":false,"scores":{},"owner_acceptance":null})

func _capture(world: OperaCareerWorld2D, state_name: String) -> void:
\tvar surface := world.surface as OperaGeologySurface
\trecords.append({"phase_index":world.phase_index,"state":state_name,"motion_frame_index":motion_frames.size(),
\t\t"surface":surface.progress_snapshot(),"qualification":"No capture freeze; timeline marker only."})

'''+code[end:]
needle='\t\t\tawait _capture(world, "five_seams_ready")';assert code.count(needle)==1;code=code.replace(needle,needle+'\n\t\t\tmotion_world = world\n\t\t\trecord_motion = true')
start=code.index('\t\t\tvar saved := surface.progress_snapshot()',code.index('"geology_geode":'));end=code.index('\t\t\tfor target: float',start);code=code[:start]+code[end:]
code=code.replace('\tvar checkpoint: Dictionary = main.save_data.get','\tawait _wait(60)\n\trecord_motion = false\n\tvar checkpoint: Dictionary = main.save_data.get')
code=code.replace('"views":records,"events":events,"final_checkpoint":checkpoint,','"views":records,"events":events,"motion_frames":motion_frames,"final_checkpoint":checkpoint,')
code=code.replace('"Main entry staged in an isolated test save home. Production world/surface/art retained; all phase transitions and work use actual viewport inputs. Not physical device/child/owner or castle/story entry evidence."','"Main entry and scripted touch intervals are a fixture. Actual production renderer and normal four-phase advancement; no capture freezes, source injection, phase forcing or restore interruption. Every rendered geode opening/earned completion frame preserved. Not physical device/child/owner/castle/training/story or human touch pacing evidence."')
(f/'capture_geode_timed_sequence.gd').write_text(code,encoding='utf-8',newline='\n')
code=(f/'review_tools/run_geology_river_gates_v219.py').read_text(encoding='utf-8').replace('run_geology_river_gates_v219.py','run_geology_river_gates_v222.py')
code=code.replace("assert action in commands","commands['parser'] += ['"+prefix+"/capture_geode_timed_sequence.gd']\ncommands['inference'] += ['"+prefix+"/capture_geode_timed_sequence.gd']\ncommands['timedanalyzer']=[godot,'--headless','--path',str(r),'--check-only','--script','"+prefix+"/capture_geode_timed_sequence.gd']\nfor w in [1280,1600]:\n commands['capturetimed'+str(w)]=[godot,'--path',str(r),'-s','"+prefix+"/capture_geode_timed_sequence.gd','--','--width='+str(w),'--touch','--classic-touch-test']\nassert action in commands")
code=code.replace("if arg.startswith(('capture','network1280','network1600')):passed=passed and 'ALL4_INTENTIONAL_PHASES' in logs", "if arg.startswith('capture'):passed=passed and 'ALL4_INTENTIONAL_PHASES' in logs\nif arg.startswith(('network1280','network1600')):passed=passed and 'RIVER_JOIN_CAPTURE|PASS|' in logs")
(f/'review_tools/run_geology_river_gates_v222.py').write_text(code,encoding='utf-8',newline='\n')
shutil.copyfile(__file__,f/'review_tools'/Path(__file__).name)
d=read(ip);d['files']=sorted(set(d['files'])|{p.relative_to(b).as_posix() for p in f.rglob('*') if p.is_file()});write(ip,d)
print('Continuous geode fixture prepared without capture freezes, restore or production changes.')
