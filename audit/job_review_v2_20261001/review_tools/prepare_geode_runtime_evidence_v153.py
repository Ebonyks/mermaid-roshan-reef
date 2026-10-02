from pathlib import Path
import datetime, hashlib, json, shutil, subprocess
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
out=r/'audit/job_geode_runtime_v1_20261001'
impact=r/'design/audit_impacts/job-geode-painted-runtime-20261001.json'
def write(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
d=json.loads(impact.read_text());d['files']=sorted(set(d['files'])|{'tools/capture_geode_runtime_route.gd','tools/capture_geode_runtime_route.gd.uid','audit/job_review_v2_20261001/review_tools/prepare_geode_runtime_evidence_v153.py'})
write(impact,d)
gd='''extends SceneTree
## Actual production surface and all four ordinary career phases. Only entry
## fixture and isolated test save home are supplied; no phase forcing, source
## injection, replacement surface, background overlay or completion callback patch.
const OUT := "res://audit/job_geode_runtime_v1_20261001/"
var main: ReefMain
var width_now := 1280
var records: Array[Dictionary] = []
var events: Array[Dictionary] = []

func _initialize() -> void:
\t_run.call_deferred()

func _wait(count: int) -> void:
\tfor _i: int in range(count):
\t\tawait process_frame

func _touch(at: Vector2, pressed: bool) -> void:
\tvar event := InputEventScreenTouch.new()
\tevent.index = 0
\tevent.position = at
\tevent.pressed = pressed
\tInput.parse_input_event(event)
\tawait _wait(2)

func _surface_touch(surface: Control, at: Vector2, pressed: bool) -> void:
\tawait _touch(surface.get_global_transform_with_canvas() * at, pressed)

func _drag(surface: Control, at: Vector2) -> void:
\tvar event := InputEventScreenDrag.new()
\tevent.index = 0
\tevent.position = surface.get_global_transform_with_canvas() * at
\tInput.parse_input_event(event)
\tawait _wait(2)

func _segment(surface: Control, start: Vector2, end: Vector2) -> void:
\tfor step: int in range(1, 11):
\t\tawait _drag(surface, start.lerp(end, float(step) / 10.0))

func _freeze(node: Node, states: Dictionary) -> void:
\tstates[node] = [node.is_processing(), node.is_physics_processing()]
\tnode.set_process(false)
\tnode.set_physics_process(false)
\tfor child: Node in node.get_children():
\t\t_freeze(child, states)

func _capture(world: OperaCareerWorld2D, state_name: String) -> void:
\tvar states: Dictionary = {}
\t_freeze(world, states)
\tawait _wait(2)
\tvar image := root.get_texture().get_image()
\tvar phase := String((world.phases[mini(world.phase_index, world.phases.size() - 1)] as Dictionary)["name"])
\tvar name := "geologist_%d_%s_%s.webp" % [width_now, phase.to_lower(), state_name]
\tassert(image.save_webp(OUT + "native_views/" + name, true) == OK)
\tvar surface := world.surface as OperaGeologySurface
\trecords.append({"id": name.trim_suffix(".webp"), "path": "native_views/" + name,
\t\t"viewport": [width_now,720], "phase": phase, "phase_index": world.phase_index,
\t\t"state": state_name, "task_open": world.task_open, "phase_progress": world.phase_progress,
\t\t"surface": surface.progress_snapshot(), "right_half_rect": [surface._geode_right_rect().position.x,
\t\t\tsurface._geode_right_rect().position.y, surface._geode_right_rect().size.x, surface._geode_right_rect().size.y],
\t\t"geode_texture": OperaGeologySurface.GEODE_PATH, "surface_script": surface.get_script().resource_path,
\t\t"player_visible": world.player_actor.visible, "player_position": [world.player_actor.position.x,world.player_actor.position.y],
\t\t"qualification": "Native Mobile desktop production render through actual viewport inputs and ordinary phase advancement. Career entry is a supplied fixture; castle/story entrance, physical device and child review not established.",
\t\t"direct_native_review": false, "scores": {}, "owner_acceptance": null})
\tfor raw_node: Variant in states:
\t\tvar node := raw_node as Node
\t\tvar state := states[raw_node] as Array
\t\tnode.set_process(bool(state[0]))
\t\tnode.set_physics_process(bool(state[1]))
\tprint("GEODE_RUNTIME_CAPTURE|", name, "|", surface.progress(), "|", world.phase_advance_pending)

func _open(world: OperaCareerWorld2D) -> void:
\tfor tick: int in range(300):
\t\tvar candidate := world._active_hotspot()
\t\tif candidate != null and candidate.visible:
\t\t\tbreak
\t\tawait _wait(1)
\tvar hot := world._active_hotspot()
\tassert(hot != null and hot.visible and not world.task_open)
\tawait _capture(world, "invitation")
\tvar at := hot.touch_button.get_global_transform_with_canvas() * (hot.touch_button.size * 0.5)
\tawait _touch(at, true)
\tawait _touch(at, false)
\tfor tick: int in range(360):
\t\tif world.task_open:
\t\t\tbreak
\t\tawait _wait(1)
\tassert(world.task_open)
\tawait _wait(8)
\tawait _capture(world, "task_open")
\tevents.append({"event":"viewport_invitation_arrival_open","phase_index":world.phase_index,"task_open":world.task_open})

func _work(world: OperaCareerWorld2D) -> void:
\tvar surface := world.surface as OperaGeologySurface
\tmatch surface.mode:
\t\t"geology_river":
\t\t\tawait _surface_touch(surface, surface.river_path_point(0), true)
\t\t\tfor point: int in range(1, OperaGeologySurface.RIVER_PATH.size()):
\t\t\t\tawait _segment(surface, surface.river_path_point(point - 1), surface.river_path_point(point))
\t\t\tawait _surface_touch(surface, surface.pointer_pos, false)
\t\t"geology_fossil":
\t\t\tvar cell := Vector2(OperaGeologySurface.FOSSIL_RECT.size.x / OperaGeologySurface.FOSSIL_GRID_COLS,
\t\t\t\tOperaGeologySurface.FOSSIL_RECT.size.y / OperaGeologySurface.FOSSIL_GRID_ROWS)
\t\t\tvar at := OperaGeologySurface.FOSSIL_RECT.position + cell * 0.5
\t\t\tawait _surface_touch(surface, at, true)
\t\t\tfor row: int in range(OperaGeologySurface.FOSSIL_GRID_ROWS):
\t\t\t\tvar column := OperaGeologySurface.FOSSIL_GRID_COLS - 1 if row % 2 == 0 else 0
\t\t\t\tvar next := OperaGeologySurface.FOSSIL_RECT.position + (Vector2(column,row) + Vector2(0.5,0.5)) * cell
\t\t\t\tawait _segment(surface, at, next)
\t\t\t\tat = next
\t\t\tawait _surface_touch(surface, at, false)
\t\t\tassert(surface.fossil_stage == 1)
\t\t\tawait _capture(world, "brushed")
\t\t\tfor piece: int in range(3):
\t\t\t\tawait _surface_touch(surface, surface.fossil_piece_home(piece), true)
\t\t\t\tawait _segment(surface, surface.fossil_piece_home(piece), surface.fossil_piece_target(piece))
\t\t\t\tawait _surface_touch(surface, surface.fossil_piece_target(piece), false)
\t\t"geology_pan":
\t\t\tvar center := OperaGeologySurface.PAN_RECT.get_center()
\t\t\tvar at := center
\t\t\tawait _surface_touch(surface, at, true)
\t\t\tfor swing: int in range(OperaGeologySurface.PAN_REQUIRED_REVERSALS + 1):
\t\t\t\tvar direction := 1.0 if swing % 2 == 0 else -1.0
\t\t\t\tvar next := center + Vector2(direction * 150.0, 0.0)
\t\t\t\tawait _segment(surface, at, next)
\t\t\t\tat = next
\t\t\t\tif swing == 3:
\t\t\t\t\tawait _capture(world, "partial_pan")
\t\t\tawait _surface_touch(surface, at, false)
\t\t"geology_geode":
\t\t\tawait _wait(120)
\t\t\tassert(is_zero_approx(surface.progress()) and not world.phase_advance_pending)
\t\t\tevents.append({"event":"passive_open_no_progress","phase_index":world.phase_index})
\t\t\tfor seam: int in range(OperaGeologySurface.GEODE_SEAM_SPOTS.size()):
\t\t\t\tvar at := surface.geode_seam_spot(seam)
\t\t\t\tawait _surface_touch(surface, at, true)
\t\t\t\tawait _surface_touch(surface, at, false)
\t\t\tawait _capture(world, "five_seams_ready")
\t\t\tvar at := surface.geode_half_center()
\t\t\tawait _surface_touch(surface, at, true)
\t\t\tawait _segment(surface, at, at + Vector2(25,0))
\t\t\tawait _surface_touch(surface, at + Vector2(25,0), false)
\t\t\tassert(is_equal_approx(surface.geode_pull,25))
\t\t\tawait _capture(world, "early_crack")
\t\t\tvar saved := surface.progress_snapshot()
\t\t\tsurface.cancel_input()
\t\t\tsurface.configure("geology_geode", Color.WHITE)
\t\t\tsurface.restore_progress(JSON.parse_string(JSON.stringify(saved)) as Dictionary)
\t\t\tsurface.armed_only = false
\t\t\tassert(is_equal_approx(surface.geode_pull,25) and surface.touch_owner == -1)
\t\t\tevents.append({"event":"released_partial_json_restore25","phase_index":world.phase_index})
\t\t\tfor target: float in [65.0,95.0,120.0]:
\t\t\t\tat = surface.geode_half_center()
\t\t\t\tvar amount := target - surface.geode_pull
\t\t\t\tawait _surface_touch(surface, at, true)
\t\t\t\tawait _segment(surface, at, at + Vector2(amount,0))
\t\t\t\tawait _surface_touch(surface, at + Vector2(amount,0), false)
\t\t\t\tassert(is_equal_approx(surface.geode_pull,target))
\t\t\t\tif target < 120.0:
\t\t\t\t\tawait _capture(world, "middle_open" if target == 65.0 else "full_interior_before_award")
\tassert(surface._completion_emitted and world.phase_advance_pending)
\tawait _capture(world, "earned_completion")
\tevents.append({"event":"intentional_completed","phase_index":world.phase_index,"progress":surface.progress()})

func _run() -> void:
\tEngine.max_fps = 30
\tassert(DisplayServer.get_name() != "headless")
\tfor arg: String in OS.get_cmdline_user_args():
\t\tif arg.begins_with("--width="):
\t\t\twidth_now = arg.trim_prefix("--width=").to_int()
\troot.size = Vector2i(width_now,720)
\tDisplayServer.window_set_size(root.size)
\tassert(DirAccess.make_dir_recursive_absolute(OUT + "native_views/") == OK)
\tmain = (load("res://scenes/main.tscn") as PackedScene).instantiate() as ReefMain
\troot.add_child(main)
\tawait _wait(5)
\tmain.day_one_active = false
\tmain._skip_intro()
\tmain._start_menu_ref()._dismiss_menu()
\tmain.game = "level2"
\tmain.g["phase"] = "hall"
\tmain.set_process(false)
\tmain.set_physics_process(false)
\tmain.hud_layer.visible = false
\tmain.player.visible = false
\tmain.save_data["opera_geology_checkpoint"] = {}
\tvar config: Dictionary = {}
\tfor act: Dictionary in OperaHouse.ACTS:
\t\tif String(act.get("costume","")) == "geologist":
\t\t\tconfig = act.duplicate(true)
\tassert(not config.is_empty())
\tvar competition := OperaCompetition.new()
\tcompetition.configure("geologist")
\tvar world := OperaCareerWorld2D.new()
\tmain.add_child(world)
\tworld.setup(main,config,competition,Callable())
\tawait _wait(20)
\tassert(world.phase_index == 0 and world.phases.size() == 4)
\tfor phase: int in range(4):
\t\tassert(world.phase_index == phase)
\t\tawait _open(world)
\t\tawait _work(world)
\t\tif phase < 3:
\t\t\tfor tick: int in range(240):
\t\t\t\tif world.phase_index == phase + 1:
\t\t\t\t\tbreak
\t\t\t\tawait _wait(1)
\t\t\tassert(world.phase_index == phase + 1)
\t\t\tevents.append({"event":"ordinary_advance_after_hold","phase_index":world.phase_index})
\tvar checkpoint: Dictionary = main.save_data.get("opera_geology_checkpoint",{}) as Dictionary
\tvar file := FileAccess.open(OUT + "CAPTURE_%d.json" % width_now,FileAccess.WRITE)
\tfile.store_string(JSON.stringify({"status":"ORDINARY_FOUR_PHASE_NATIVE_ROUTE_CAPTURED_REVIEW_PENDING",
\t\t"views":records,"events":events,"final_checkpoint":checkpoint,
\t\t"qualification":"Main entry staged in an isolated test save home. Production world/surface/art retained; all phase transitions and work use actual viewport inputs. Not physical device/child/owner or castle/story entry evidence."},"\\t"))
\tfile.close()
\tprint("GEODE_RUNTIME_ROUTE|ALL4_INTENTIONAL_PHASES|",width_now,"|",records.size(),"|PASS_CAPTURE_REVIEW_PENDING")
\tquit(0)
'''
(r/'tools/capture_geode_runtime_route.gd').write_text(gd,encoding='utf-8',newline='\n')
# Store previous published review proof durably without changing its original map.
proof=r/'audit/job_review_v2_20261001/opening_motion_remote_verified_v5'
proof.mkdir(exist_ok=False)
for folder in ['opening_motion_publish_v148','opening_motion_remote_v148']:
 for p in (r/'tmp'/folder).iterdir():
  if p.is_file() and p.name not in ['script.py']:
   dest=proof/(folder+'_'+p.name);shutil.copyfile(p,dest)
   d['files'].append(dest.relative_to(r).as_posix())
write(out/'runtime_gate/RECEIPT.json',{'status':'PENDING','qualification':'New production change needs its own exact-byte full suite; G325-source inherited suite no longer sufficient.'})
write(out/'REVIEW.json',{'status':'PENDING_CURRENT_RUNTIME_NATIVE_REVIEW','source_finish':4.6,'runtime_views':[],'complete_action_score':None,'owner_acceptance':None})
(out/'index.html').write_text('''<!doctype html><meta charset="utf-8"><title>Geode production candidate</title><style>body{max-width:1000px;margin:40px auto;padding:20px;background:#edf7f6;color:#302846;font:18px system-ui}img{max-width:100%}</style><h1>Geode production candidate</h1><p>Four directly reviewed painted source states are now bound at separate runtime paths. Crystals are rooted inside each open cavity. Native production review and fresh full-suite verification are pending. Source4.6 does not grant complete action, remote actor contact, device, child or owner approval.</p><p><a href="../job_review_v2_20261001/GEOLOGY_CONTINUATION_REPORT_V5.html">Earlier illustrated source and context report</a></p><img src="../../assets/opera/worlds/geology/painted_geode_v1_20261001/open_embedded.png" alt="Two geode cavities with rooted crystals"><p>Actual production candidate on the work branch; integration and final report remain open.</p>''',encoding='utf-8')
p=r/'audit/MASTER_AUDIT_2026-08-09.md';s=p.read_text(encoding='utf-8');anchor='## 0. Planning entry\n';s=s.replace(anchor,anchor+'\nPainted geode production candidate (2026-10-01): [new runtime review](job_geode_runtime_v1_20261001/index.html) copies four already directly inspected source states to separate runtime paths and binds rooted interior reveal in the production Canvas surface. Shared base and visible right-half selection/pointer use one transform. Fresh ordinary four-phase viewport-input capture and complete suite pending; G325-source inherited suite does not validate this new source change. Old flat siblings, remote actor, room, device/child/owner/final report remain open. [Impact](../design/audit_impacts/job-geode-painted-runtime-20261001.json). No closure/integration/release.\n',1);p.write_text(s,encoding='utf-8',newline='\n')
p=r/'design/05_DOC_LEDGER.md';s=p.read_text(encoding='utf-8');s+='\n<!-- Current geode runtime binding evidence; review claim only. -->\n\n| `audit/job_geode_runtime_v1_20261001/index.html` | 🟣 | `CANDIDATE`; four existing reviewed geode derivatives copied intact to new runtime paths and bound in production Canvas rendering. Ordinary four-phase viewport-input native capture and fresh complete suite pending. Source4.6 does not grant mounted/action, actor-contact, room, device, child, owner, integration or final all-job acceptance. |\n';p.write_text(s,encoding='utf-8',newline='\n')
p=r/'audit/findings/ACTIVE_FINDINGS_2026-08-13.md';s=p.read_text(encoding='utf-8');a=s.index('### MA-PLAY-004') if '### MA-PLAY-004' in s else s.index('## MA-PLAY-004');b=s.find('\n##',a+3);b=len(s) if b<0 else b;part=s[a:b];needle='| history |';i=part.index(needle);j=part.index('\n',i);line=part[i:j];line=line.rstrip().removesuffix('|').rstrip()+' 2026-10-01 painted geode production candidate: four reviewed states now bound at new runtime paths; rooted cavity pixels replace the detached crystal layer. [New source-bound ordinary-route/full-suite evidence](../job_geode_runtime_v1_20261001/index.html) pending. Remote actor and other geology surfaces remain priorities; no lifecycle closure/integration/owner approval. |';part=part[:i]+line+part[j:];s=s[:a]+part+s[b:];p.write_text(s,encoding='utf-8',newline='\n')
shutil.copyfile(Path(__file__),r/'audit/job_review_v2_20261001/review_tools/prepare_geode_runtime_evidence_v153.py')
d['files']=sorted(set(d['files']));write(impact,d)
print('Ordinary-route capture and all pending boundaries prepared; prior368-file remote proof preserved.')
