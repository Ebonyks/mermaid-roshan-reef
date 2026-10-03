from pathlib import Path
import datetime, hashlib, json, shutil, subprocess

R = Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
F = R / 'audit/job_geology_complete_actions_v1_20261003'
assert not F.exists()
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
def write(p, d):
    p.write_text(json.dumps(d, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')

baseline = subprocess.run(['git','rev-parse','HEAD'],cwd=R,capture_output=True,check=True).stdout.decode().strip()
assert baseline == '1652a9bb33af0d11a594b5996df66d2266c02d39'
old = R / 'audit/job_geode_current_recheck_v1_20261002/capture.gd'
boundary = read(R / 'audit/job_nursery_wash_connected_v1_20261002/SOURCE_CURRENT_MACHINE_V3.json')
assert len(boundary['source_files']) == 783
assert all(sha(R/x['path']) == x['sha256'] for x in boundary['source_files'])
prior = read(R/'design/audit_impacts/job-geode-current-recheck-20261002.json')
ip = R/'design/audit_impacts/job-geology-complete-actions-20261003.json'
write(ip, {'id':'job-geology-complete-actions-20261003','baseline':baseline,
    'scope':'Fill the explicit current timed fossil-brushing/assembly and pan-rocking coverage gaps by instrumenting only the established non-runtime actual Library card, all-four-phase earned route and Opera elevator replay fixture. Preserve every production byte, touch path, gameplay/save/completion owner and earlier score/history. Capture every rendered input/wait frame through invitation, work, completion hold and next-phase arrival at both native widths; record current actor, material and pointer state without manipulating them. Directly review every native full canvas, individual action/contact/material/transition opinions, and display all evidence before assigning current action scores. No new artwork, runtime or protected-original modifications, cinematic delivery, owner/device/child acceptance or finding closure.',
    'rules':prior['rules'],'findings':prior['findings'],
    'files':[(F/x).relative_to(R).as_posix() for x in ['.gdignore','PLAN.json','capture.gd','SOURCE_CURRENT_BEFORE_CAPTURE.json','review_tools/'+Path(__file__).name]],
    'validation':[{'command':'Complete actual Geologist fossil and pan action capture and direct review at 1280x720 and 1600x720','result':'PENDING','evidence':(F/'PLAN.json').relative_to(R).as_posix()}],
    'acceptance_gaps':'Current full actions require direct visual review. Native capture readback slows wall clock. Desktop fixtures are not physical device/child/owner acceptance. Room and embodied hand contact remain known priorities; global strict 2D and all-job closure remain unfinished.'})
(F/'review_tools').mkdir(parents=True)
(F/'.gdignore').write_text('',encoding='utf-8')
s = old.read_text(encoding='utf-8')
needle = 'res://audit/job_geode_current_recheck_v1_20261002/attempt01/'
assert s.count(needle)==1
s=s.replace(needle,'res://audit/job_geology_complete_actions_v1_20261003/attempt01/')
s=s.replace('native_frames/geode_%d_%04d.webp','native_frames/work_%d_%04d.webp')
# Geode timing evidence already exists. Record only complete fossil/pan sequences.
needle='\t\t\tmotion_world = world\n\t\t\trecord_motion = true\n'
assert s.count(needle)==1
s=s.replace(needle,'')
needle='\t\tassert(world.phase_index == phase)\n\t\tawait _open(world)'
assert s.count(needle)==1
s=s.replace(needle,'\t\tassert(world.phase_index == phase)\n\t\tif phase in [1, 2]:\n\t\t\tmotion_world = world\n\t\t\trecord_motion = true\n\t\tawait _open(world)')
needle='\t\t\tassert(world.phase_index == phase + 1)\n'
assert s.count(needle)==1
s=s.replace(needle,needle+'\t\tif phase in [1, 2]:\n\t\t\trecord_motion = false\n\t\t\tevents.append({"event":"complete_work_sequence_recorded","from_phase":phase,"frame_count":motion_frames.size()})\n')
needle='\t\t"phase_index":phase,"game":main.game'
assert s.count(needle)==1
s=s.replace(needle,'\t\t"mode":(motion_world.surface as OperaGeologySurface).mode if is_instance_valid(motion_world.surface) else "",\n\t\t"actor_position":motion_world.player_actor.position,\n\t\t"actor_size":motion_world.player_actor.size,\n\t\t"actor_texture":motion_world.player_actor.texture.resource_path,\n\t\t"pointer_position":(motion_world.surface as OperaGeologySurface).pointer_pos,\n\t\t"pointer_held":(motion_world.surface as OperaGeologySurface).held,\n\t\t"pan_visual_x":(motion_world.surface as OperaGeologySurface).pan_visual_x,\n\t\t"fossil_drag_piece":(motion_world.surface as OperaGeologySurface).fossil_drag_piece,\n\t\t"fossil_drag_position":(motion_world.surface as OperaGeologySurface).fossil_drag_position,\n'+needle)
s=s.replace('ACTUAL_LIBRARY_ALL4_PHASES_EARNED_RETURN_AND_DEV_ENTRY_CAPTURED_REVIEW_PENDING','ACTUAL_LIBRARY_COMPLETE_FOSSIL_PAN_ALL4_EARNED_RETURN_AND_DEV_ENTRY_CAPTURED_REVIEW_PENDING')
s=s.replace('Native capture readback slows wall clock.','Every input/wait frame of phases 1 and 2 captured; native readback slows wall clock. No per-frame production timing claim.')
(F/'capture.gd').write_text(s,encoding='utf-8',newline='\n')
write(F/'SOURCE_CURRENT_BEFORE_CAPTURE.json',boundary)
write(F/'PLAN.json',{'status':'PREPARED_BEFORE_CAPTURE','baseline':baseline,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'named_gap':'Current Library all-four-phase selected still evidence leaves complete fossil-brushing/assembly and pan action scores unassigned. Detached actor contact and room drawings remain weak.',
    'reuse':'Exact current production drawings and source assets; exact existing Library/elevator fixture inputs, outcomes and checkpoints. No new generation or gameplay modification.',
    'fixture_source':old.relative_to(R).as_posix(),'fixture_source_sha256':sha(old),'fixture_sha256':sha(F/'capture.gd'),
    'changes':['New output directory and frame basename only','Record consecutive frames for phase 1 fossil and phase 2 pan from invitation through next-phase arrival; omit already-reviewed geode motion recording','Add read-only actor/pointer/material state annotations'],
    'native_widths':[1280,1600],'native_height':720,'engine_baseline':'Godot 4.7.2-stable','render_fps_ceiling':30,
    'source_boundary_count':783,'required_visual_review':'Every native frame in order, full room/actor/contact, fossil concealment, brush contact and gridded clearing, same fossil piece ownership/assembly, pan rim/support/grains/water/mineral persistence, alternating tilts, complete completion hold and invitation transitions. Report material, individual objects, semantic actions, body contact and transitions separately. No frame may inherit approval from a good source still.',
    'owner_acceptance':None,'runtime_changes':False,'integration':False,'release':False})
shutil.copyfile(Path(__file__),F/'review_tools'/Path(__file__).name)
print('GEOLOGY_COMPLETE_ACTIONS_PREPARED|783 unchanged|no production edits')
