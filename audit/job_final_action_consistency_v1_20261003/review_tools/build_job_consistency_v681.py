from pathlib import Path
import datetime, hashlib, html, json, re, shutil, subprocess
from PIL import Image
B=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
BASE='6c5c1bd4a0951964a08043e72ae6472d2d402a9e'
REL='audit/job_final_action_consistency_v1_20261003'; P=B/REL
L=B/'audit/job_artwork_refinement_live'; D='design/animation/JOB_FINAL_ACTION_PRESENTATION_V1.json'
IP=B/'design/audit_impacts/job-final-action-consistency-20261003.json'
ROOT=Path('C:/Users/Peter/Documents/mermaid-roshan-reef')
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
sha=lambda data:hashlib.sha256(data).hexdigest()
def put(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((json.dumps(d,indent=2,ensure_ascii=False)+'\n').encode())
def copy(src,dst):dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(src.read_bytes())
def rel(p):return p.relative_to(B).as_posix()
def git(*args):return subprocess.run(['git',*args],cwd=B,capture_output=True,check=True).stdout
assert git('rev-parse','HEAD').decode().strip()==BASE
assert (P/'AUTHORITY_START.json').is_file() and IP.is_file()
assert not (P/'index.html').exists()
start=json.loads((P/'AUTHORITY_START.json').read_text())

# Literal-only GDScript dictionary reader. No eval, execution or engine mutation.
def const(source,name):
 m=re.search(r'^const\s+'+re.escape(name)+r'[^=\n]*=\s*',source,re.M);assert m,name
 s=source[m.end():]; pat=re.compile(r'\s+|\#[^\n]*|"(?:\\.|[^"\\])*"|-?\d+(?:\.\d+)?|[A-Za-z_][A-Za-z0-9_]*|[{}\[\]:,]')
 tokens=[];at=0;depth=0
 while at<len(s):
  mt=pat.match(s,at);assert mt,(name,s[at:at+40]);v=mt.group();at=mt.end()
  if v.isspace() or v.startswith('#'):continue
  tokens.append(v)
  if v in ('{','['):depth+=1
  elif v in ('}',']'):
   depth-=1
   if depth==0:break
 cursor=0
 def value():
  nonlocal cursor
  t=tokens[cursor];cursor+=1
  if t.startswith('"'):return json.loads(t)
  if t in ('true','false'):return t=='true'
  if t=='null':return None
  if re.fullmatch(r'-?\d+(?:\.\d+)?',t):return float(t) if '.' in t else int(t)
  if t=='[':
   a=[]
   while tokens[cursor]!=']':
    a.append(value())
    if tokens[cursor]==',':cursor+=1
    else:assert tokens[cursor]==']'
   cursor+=1;return a
  if t=='{':
   d={}
   while tokens[cursor]!='}':
    k=value();assert tokens[cursor]==':';cursor+=1;assert k not in d;d[k]=value()
    if tokens[cursor]==',':cursor+=1
    else:assert tokens[cursor]=='}'
   cursor+=1;return d
  raise AssertionError((name,t))
 v=value();assert cursor==len(tokens)
 return v,source[:m.start()].count('\n')+1
def source(name):
 p=B/name;data=p.read_bytes();return dict(path=name,sha256=sha(data),normalized_lf_sha256=sha(data.replace(b'\r\n',b'\n')),bytes=len(data)),data.decode('utf-8-sig')
world_path='scripts/opera_career_world_2d.gd'; world_record,world=source(world_path)
adapter_record,adapter=source('scripts/chapter_two_career_scene_adapter.gd')
performance_record,performance=source('scripts/opera_performance_plan.gd')
phases,phase_line=const(world,'PHASES');legacy,legacy_line=const(world,'LEGACY_PHASES');birthday,birthday_line=const(adapter,'PHASE_SETS')
enabled,enabled_line=const(performance,'ENABLED');practice,_=const(performance,'PRACTICE_COUNTS')
assert len(phases)==15 and set(birthday).issubset(phases)
rows=[]
for career,steps in phases.items():
 for index,step in enumerate(steps):
  rows.append(dict(id=f'OPERA-{career}-{index:02}',lane='Current base Opera phase declaration',career=career,index=index,name=step['name'],mode=step['mode'],voice=step.get('voice'),source=world_path,constant='PHASES',constant_line=phase_line,required_final_work='Roshan visibly finishes the verb shown in this phase and its voice prompt at the same target, then releases or settles into a safe pose.',runtime_final_action_acceptance=None,presentation_migration='PENDING',actual_route_capture='REQUIRED; declaration is not route evidence'))
 for part,count in [('practice',min(practice.get(career,len(steps)),len(steps))),('stage',len(steps))]:
  if career not in enabled:continue
  for index in range(count):
   step=steps[index]
   rows.append(dict(id=f'TWOACT-{career}-{part}-{index:02}',lane='Enabled practice/stage plan expansion',career=career,index=index,name=step['name'],mode=step['mode'],performance_part=part,source='scripts/opera_performance_plan.gd',source_phase=f'OPERA-{career}-{index:02}',required_final_work='Same meaningful finish as the referenced phase. Retain held ballet poses and specialist input; no generic looping replacement.',runtime_final_action_acceptance=None,presentation_migration='PENDING',actual_route_capture='REQUIRED; expanded source plan is not fresh gameplay evidence'))
for career,definition in birthday.items():
 for index,step in enumerate(definition['phases']):
  rows.append(dict(id=f'BIRTHDAY-CATALOG-{career}-{index:02}',lane='Birthday adapter catalog declaration; route activation separate',career=career,index=index,name=step['name'],mode=step['mode'],milestone=step.get('milestone'),voice=step.get('voice'),scene_id=definition.get('scene_id'),source=adapter_record['path'],constant='PHASE_SETS',constant_line=birthday_line,required_final_work='Roshan finishes this exact physical submilestone; preserve cake dependencies, five-berry ownership and the parked/unlaunched rocket state wherever specified.',runtime_final_action_acceptance=None,presentation_migration='PENDING',actual_route_capture='REQUIRED; catalog includes candidates that are not current story unlocks'))
put(P/'PHASE_COVERAGE.json',dict(baseline=BASE,qualification='Source-derived planning coverage only. Includes all current base declarations, actual enabled plan expansions and nonempty adapter catalog entries. Not an exhaustive all-days task discovery, count of distinct games or newly accepted runtime actions.',source_records=[world_record,adapter_record,performance_record],counts=dict(base_phases=sum(len(v) for v in phases.values()),base_careers=len(phases),enabled_two_act_careers=enabled,enabled_plan_instances=sum(min(practice[k],len(phases[k]))+len(phases[k]) for k in enabled),birthday_catalog_phases=sum(len(v['phases']) for v in birthday.values()),planned_rows=len(rows)),rows=rows,legacy_declarations=dict(constant='LEGACY_PHASES',line=legacy_line,careers=len(legacy),phase_count=sum(len(v) for v in legacy.values()),qualification='Kept as historical/dependency inventory, not asserted active. Resolve caller selection before counting actual use.'),empty_birthday_catalog_careers=[k for k,v in birthday.items() if not v['phases']],absent_birthday_catalog_careers=sorted(set(phases)-set(birthday)),remaining_discovery=['Day One dynamic Main/fixture tasks and their every-item substeps','Ordinary activated eight-career ChapterTwo route variants and caller overrides','Optional family-supper, movie, bedtime and other castle/freeplay interactions','Dynamic Teacher lesson question/substep variants','All object/pose/interruption/save/device/child/owner evidence']))

clips=[]
for name,start_line,end_line,why in [('Common task pose',2367,2383,'Most ordinary work falls back to the shared work row; a work loop does not prove the task-specific final contact.'),('Activity layout',2817,2920,'Mixed full-stage, specialist-focus and 392x232 card layouts are literal current source facts.'),('Progress completion',3592,3666,'Progress threshold accepts completion, cheers and holds before advancing. This is not proof of a visible final physical verb.')]:
 lines=world.splitlines();body='\n'.join(lines[start_line-1:end_line])
 clips.append(dict(name=name,path=world_path,source_sha256=world_record['sha256'],start_line=start_line,end_line=end_line,text=body,interpretation=why,qualification='Static caller trace; no new runtime acceptance'))
for name in ['project.godot','scripts/opera_world_backdrop_2d.gd','scripts/opera_gesture_surface.gd','scripts/opera_roshan_actor.gd','scripts/comfy_games.gd']:
 record,text=source(name);matches=[]
 patterns={'project.godot':['window/size/','window/stretch/'],'scripts/opera_world_backdrop_2d.gd':['1672','941','2048','world_%s','source_y'], 'scripts/opera_gesture_surface.gd':['candy_wrap','candymaker','wrap_contact'], 'scripts/opera_roshan_actor.gd':['work','1024','256'], 'scripts/comfy_games.gd':['_stir_dinner','pot_stirred','completed','room_kitchen_item_soup_pot']}
 for i,line in enumerate(text.splitlines()):
  if any(x in line for x in patterns[name]):matches.append(dict(line=i+1,text=line))
 clips.append(dict(name=name,path=name,source_sha256=record['sha256'],matches=matches,qualification='Source fact only; selected texture/current route must be captured'))
put(P/'CURRENT_LAYOUT_AND_COMPLETION_TRACE.json',dict(baseline=BASE,observations=clips,window_distinction='project.godot mode=2 is separate from the audit fixture forcing a fixed-size window; the 392x232 activity card is a separate in-game layout choice. A browser page also constrains displayed screenshots.',card_inner_pixels=[392,232],outer_card_pixels=[416,292],observed_wrapping_drawing_pixels=[222.72,222.72],card_share_of_1280x720=392*232/(1280*720),runtime_changed=False))

# Exact reusable source inspection. Dimensions alone never grant native provenance.
names=['assets/opera/worlds/widgets/widget_crank_candymaker_mover.png','assets/opera/worlds/actors/animation/roshan_candymaker_sheet_a.png','assets_src/imagegen/candy_wrap_twist_release_pose_v1_20261003/twist_attempt05/native.png']
# Find the existing endpoint directory through its filename, without inventing a copy.
names=names[:2]
for parent,child in [('candy_wrap_scene_context_v1_20261003','attempt02'),('candy_twist_release_pose_v1_20261003','twist_attempt05'),('candy_wrap_transition_keys_v1_20261003','release_attempt04')]:
 candidate=B/'assets_src/imagegen'/parent/child/'native.png'
 if not candidate.is_file():
  candidates=list((B/'assets_src/imagegen'/parent).rglob('native.png'))
  candidates=[p for p in candidates if child in p.parts]
  assert len(candidates)==1,(parent,child,candidates)
  candidate=candidates[0]
 names.append(rel(candidate))
names.extend(rel(p) for p in sorted((B/'assets/opera/worlds/backdrops').glob('world_candymaker*.png')))
resolution=[]
for name in names:
 p=B/name;data=p.read_bytes()
 with Image.open(p) as im:dim=list(im.size)
 resolution.append(dict(path=name,sha256=sha(data),bytes=len(data),dimensions=dim,role='source review key' if name.startswith('assets_src') else 'existing runtime resource',native_2048_square_background_coverage=('NOT_APPLICABLE_CHARACTER_OR_PROP_RESOURCE' if '/widgets/' in name or '/actors/' in name else 'NOT_PROVEN_BY_CONTAINER_DIMENSIONS'),reuse_decision='Preserve. Verify native source provenance and intended draw scale before binding; do not enlarge and relabel as a high-resolution replacement.'))
put(P/'RESOLUTION_REUSE_INVENTORY.json',dict(baseline=BASE,inspected_sources=resolution,observed_new_complete_source_dimensions=[1672,941],qualification='1672x941 review keys improve source detail but do not meet the required minimum native 2048x2048 background coverage. POT runtime tile dimensions do not establish native source resolution. No pixel editing or upscaling performed.',named_gaps=['Legible stage-size finishing action with stable Roshan identity and local hand/prop contact','Native 2048x2048 coverage per playable background screen with recorded original dimensions/provenance','The opposite wrist midpoint still has no source reaching 4.5','Current actual wrapper/whisk binding does not use the proposed golden wrapper source family']))

contract=dict(schema='reef.job-final-action-presentation.v1',status='OWNER_SELECTED_DIRECTION_RUNTIME_ROLLOUT_PENDING',baseline=BASE,owner_direction=dict(date='2026-10-03',exact_choice='Use the same final-action sequence everywhere, with Roshan visibly finishing each task (recommended).',scope='All Roshan-owned job tasks and substeps across actual job days and Opera training/freeplay',qualification='Direction accepted; existing artwork, motion, runtime, device and comprehensive report acceptance are not implied.'),intent='The child directs the work. Roshan herself visibly performs the last meaningful action on the same object, releases or settles safely, and leaves a readable result before celebration or the next task.',sequence=[dict(beat='request',requirement='A valid touch gives prompt visible response and preserves the child’s selected answer/plan.'),dict(beat='arrive',requirement='Roshan reaches the actual target through current navigation. No remote progress.'),dict(beat='work',requirement='The child’s existing gesture drives the relevant operation; hand/tool makes local visible contact.'),dict(beat='finish',requirement='Roshan visibly finishes the exact task verb. Do not replace work with a cheer or auto-solve a choice.'),dict(beat='settle',requirement='Same hands, cuffs, prop, support, costume and room persist; release into a clear stable state.'),dict(beat='show_result',requirement='The actual earned object/state stays visible and consistent with the saved consequence.'),dict(beat='celebrate_or_next',requirement='Celebrate only after the real finish is legible; retain existing specialist/voice/return ownership.')],presentation=dict(direction='Shared stage-size work presentation; migrate the legacy small activity-card format',qualifier='This is the scoped layout plan. Runtime layout is not yet changed.',camera='Keep the room and actor scale/identity continuous within each job. Any closer work framing uses the same transition grammar in training and story, not a nested unrelated mini-scene.',composition='Full 1280x720 base Canvas stage with supported expanded aspects; give hands and target enough screen area for phone readability. Keep Back/voice cues reachable and result visible.',actor_ownership='Only one live Roshan presentation at a time. Transfer between route actor and work presentation coherently; no duplicate tail, disappearance or costume substitution.',reuse='Use approved source families and the same career-specific props/costume/room. Candy gold-paper study is a pilot family, not a different art medium for every job.'),resolution=dict(background_native_minimum_per_playable_screen=[2048,2048],multi_screen_rule='Native coverage is measured per playable screen; preserve panorama composition and use non-overlapping 1024 cards after source acceptance.',runtime_texture_rule='At most 1024 longest side or power of two; POT only for VRAM compression. Preserve original masters.',character_prop_rule='Choose native pose/prop density for actual largest draw size; no unreviewed enlargement to conceal missing detail. Individual cutout sources need not meet a background dimension requirement.',review_key_gap='Current 1672x941 full scene keys do not satisfy native 2048x2048 background coverage.',required_receipt='Original dimensions, exact source hash, master provenance, output/tile hashes and measured display scale; padded/upscaled tile dimensions are insufficient.'),specialist_constraints=['Ballerina held poses/one-shot curtain call remain under DL-MOT-09; common format does not create a looping work animation.','Teacher: child chooses/counts/combines; Roshan visibly confirms or places the chosen result without solving for the child.','Geode: Roshan opens a supported geode with crystals remaining embedded inside both halves; no loot drop.','Nursery: preserve Faron’s role, baby conservation, continuous support and safe resting states.','ChapterTwo cake: keep Farmer→Chef→Candy Maker dependencies and correct fruit counts/tiers; park the rocket unlaunched where specified.','Boxer/Racer and other specialists retain their current input and action owners; stage-wide presentation alone is not final-contact acceptance.','Existing Day One owner-selected story clips retain their separate scoped authority; no new movie inserted to replace the child’s action.'],lifecycle=dict(owner='Existing gameplay state owner',progress='Validate current intentional request, actual target/contact and required work; a timer, final pose or clip end alone cannot award progress.',interrupt_before_commit='Cancel unfinished work on retarget, exit, pause/focus policy and teardown; clear touch/callback ownership.',interrupt_after_commit='Keep earned progress, place the prop safely and suppress duplicate rewards on restore.',save='Add compatible defaults only; never remove save keys or infer completion from animation timestamps.'),quality=dict(source_floor=4.5,inclusive_priority_threshold=4.5,hard_gaps=['Identity/topology/contact or object-conservation failure','Wrong final verb or missing final action','Unproven native background resolution','Unreadable hand/target scale or cropped anatomy','Interrupted action earning progress','Missing ordinary runtime route or device/child/owner evidence'],score_lanes=['native source','mounted image','object sequence','complete meaningful action','runtime route','device','child','owner'],acceptance='Score each relevant item/lane separately. Source 4.5 does not transfer to motion or runtime; priorities at exactly 4.5 remain included.'),implementation=dict(runtime_changed=False,selected_motion=None,common_timing=None,geometry=None,qualification='No measured runtime timing/sockets are fabricated. Coverage rows are planning entries, not accepted action bindings.'),references=dict(phase_coverage=REL+'/PHASE_COVERAGE.json',current_layout_trace=REL+'/CURRENT_LAYOUT_AND_COMPLETION_TRACE.json',resolution_inventory=REL+'/RESOLUTION_REUSE_INVENTORY.json',production_protocol='design/animation/ANIMATION_PRODUCTION_PROTOCOL.md',impact=rel(IP)))
put(B/D,contract)
put(P/'OWNER_DIRECTION.json',contract['owner_direction'])
put(P/'PRESENTATION_CONTRACT.json',contract)

# Preserve prior register and boundary bytes; this change does not rescore a single item.
preserved=[]
for name in ['ALL_ITEMS.json','ATLAS_STATE_ITEMS_V51.json','CURRENT_STAMP.json']:
 p=L/name
 if p.is_file():preserved.append(dict(path=rel(p),sha256=sha(p.read_bytes()),bytes=p.stat().st_size))
put(P/'REGISTER_BOUNDARY_BEFORE.json',dict(files=preserved,scores_changed=False,known_items=2160,inclusive_priorities=1063,pending_primary_opinions=294))
copy(L/'index.html',P/'previous_library_index.html')
boundary=B/'assets_src/local_motion/candy_wrap_continuity_v1_20261003/PRODUCTION_BOUNDARY.json'
copy(boundary,P/'PRODUCTION_BOUNDARY.json')

# Archive every already completed AE remote row losslessly, with bounded files.
remote=B/'tmp/transition_remote_v674'; result=json.loads((remote/'RESULT.json').read_text());assert result['revision']==BASE and result['files_including_manifest']==24975 and result['status']=='PASS_ALL_ANONYMOUS_REMOTE_BYTES'
old=P/'previous_AE_remote_verified'; old.mkdir()
for src,dst in [(remote/'RESULT.json',old/'RESULT.json'),(B/'tmp/transition_publish_v674/RECEIPT.json',old/'INITIAL_PUBLICATION_RECEIPT.json')]:copy(src,dst)
journals=[p for p in remote.iterdir() if p.suffix=='.jsonl'];assert len(journals)==1,journals
raw=journals[0].read_bytes();lines=raw.splitlines(keepends=True);assert len(lines)==24975
parts=[];part=b''
for line in lines:
 if len(part)+len(line)>850000 and part:
  name='JOURNAL_%03d.jsonl'%len(parts);(old/name).write_bytes(part);parts.append(dict(path=rel(old/name),bytes=len(part),sha256=sha(part),records=len(part.splitlines())));part=b''
 part+=line
if part:
 name='JOURNAL_%03d.jsonl'%len(parts);(old/name).write_bytes(part);parts.append(dict(path=rel(old/name),bytes=len(part),sha256=sha(part),records=len(part.splitlines())))
assert b''.join((B/p['path']).read_bytes() for p in parts)==raw
put(old/'JOURNAL_SHARDS.json',dict(revision=BASE,source_sha256=sha(raw),source_bytes=len(raw),records=24975,lossless_reconstruction=True,parts=parts))
ci_cmd=['C:/Program Files/GitHub CLI/gh.exe','run','view','37127165966','--repo','Ebonyks/mermaid-roshan-reef','--json','databaseId,headSha,status,conclusion,url,jobs']
ci_run=subprocess.run(ci_cmd,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW,check=True);(old/'HOSTED_RUN.json').write_bytes(ci_run.stdout);(old/'HOSTED_RUN.stderr.log').write_bytes(ci_run.stderr);ci=json.loads(ci_run.stdout);assert ci['headSha']==BASE
put(old/'HOSTED_STATUS_OBSERVED.json',dict(checked_utc=now(),revision=BASE,status=ci['status'],conclusion=ci['conclusion'],run_url=ci['url'],qualification='Actual dated observation, not a prediction of a new candidate CI result.'))

# Existing complete source images are review references, never invented runtime pixels.
reference_sources=[resolution[2]['path'],resolution[3]['path'],resolution[4]['path']]
capture='audit/job_candy_wrap_contact_runtime_v1_20261003/attempt05/native_frames/training_1280_0081.webp'
art_refs=[]
for name in [capture]+reference_sources:
 p=B/name
 with Image.open(p) as im:dim=list(im.size)
 art_refs.append(dict(path=name,sha256=sha(p.read_bytes()),dimensions=dim,role='DATED_UNBOUND_RUNTIME_STUDY' if name==capture else 'EXISTING_NATIVE_SOURCE_ONLY',modifications='None; report displays complete image',new_opinion=None,runtime_acceptance=None))
put(P/'ILLUSTRATION_REFERENCES.json',dict(baseline=BASE,images=art_refs,qualification='Existing images reused unchanged. Owner likes twisting images but has not approved the complete action or runtime integration. Source vs mounted/action scores remain in their original reports.'))
def href(name):return '../../'+name
def image_ref(i,title,note):
 r=art_refs[i];return '<figure><a href="'+html.escape(href(r['path']))+'"><img src="'+html.escape(href(r['path']))+'" alt="'+html.escape(title)+'"></a><figcaption><strong>'+html.escape(title)+'</strong><br>'+html.escape(note)+'<br>'+str(r['dimensions'][0])+'×'+str(r['dimensions'][1])+' · unchanged source</figcaption></figure>'
families=[]
for career,steps in phases.items():
 matches=[r for r in rows if r['career']==career]
 families.append('<tr><th>'+html.escape(career.title())+'</th><td>'+html.escape(' → '.join(s['name'] for s in steps))+'</td><td>'+str(len(matches))+'</td><td>Pending individual final-contact and full-stage review</td></tr>')
row_html=[]
for r in rows:
 row_html.append('<tr data-career="'+r['career']+'"><td>'+html.escape(r['id'])+'</td><td>'+html.escape(r['name'])+'</td><td>'+html.escape(r['lane'])+'</td><td>'+html.escape(r.get('voice') or r['required_final_work'])+'</td><td>Pending</td></tr>')
counts=json.loads((P/'PHASE_COVERAGE.json').read_text())['counts']
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Roshan finishes the work · shared job format</title><style>
:root{font-family:system-ui,sans-serif;color:#292047;background:#f4f7fc;line-height:1.55}body{margin:0}main{max-width:1120px;margin:auto;padding:30px 22px 80px}h1{font-size:clamp(28px,4vw,44px);line-height:1.1}h2{font-size:25px;margin-top:38px}p{max-width:82ch}.note{background:#fff0d5;border-left:5px solid #be7120;padding:16px 20px;border-radius:12px}.direction{background:#e1f3ed;border-left:5px solid #25876a;padding:16px 20px;border-radius:12px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:20px}.beats{display:flex;flex-wrap:wrap;gap:10px}.beat{background:white;border:1px solid #c8c0df;border-radius:12px;padding:12px;flex:1 1 135px}.beat b{display:block}figure{margin:18px 0;background:white;padding:12px;border-radius:14px}img{display:block;width:100%;height:auto;max-width:100%;border-radius:9px}figcaption{padding:10px 3px;font-size:14px}.table{overflow:auto}table{border-collapse:collapse;width:100%;background:white;font-size:14px}th,td{text-align:left;padding:12px;border-bottom:1px solid #dad7e6;vertical-align:top}input{font:inherit;padding:9px;border:1px solid #74638d;border-radius:8px;width:min(92%,450px)}summary{cursor:pointer;font-weight:600}a{color:#384393}code{overflow-wrap:anywhere}.facts{color:#65547a;font-size:14px}</style><main>
<h1>Roshan finishes the work</h1><p>One shared presentation across job days and Opera training. The child directs the action; Roshan visibly performs the last meaningful step on the actual object.</p>
<div class="direction"><b>Owner selected · 3 October 2026</b><p>“Use the same final-action sequence everywhere, with Roshan visibly finishing each task.” This direction now applies throughout the job audit.</p></div>
<div class="note"><b>Rollout is still pending.</b><p>This is an illustrated production brief and source-derived coverage plan. It has not changed the game, enlarged a runtime image, accepted the wrapping motion, or rescored the library.</p></div>
<p><a href="../../audit/job_artwork_refinement_live/index.html">Current illustrated library</a> · <a href="PRESENTATION_CONTRACT.json">Exact presentation contract</a> · <a href="PHASE_COVERAGE.json">Every planned phase row</a> · <a href="RESOLUTION_REUSE_INVENTORY.json">Native-resolution inventory</a></p>
<h2>The common sequence</h2><div class="beats">'''
for step in contract['sequence']:page+='<div class="beat"><b>'+html.escape(step['beat'].replace('_',' ').title())+'</b>'+html.escape(step['requirement'])+'</div>'
page+='''</div><p>The final action must be the work itself: the last wrapper twist, the bandage being smoothed onto the arm, the berry placed where it belongs, or the geode opened with its crystals still inside. A cheer cannot stand in for that contact. The child keeps control of choices and gestures.</p>
<h2>Why the wrapping currently looks windowed</h2><p>The inherited activity surface is <b>392×232 pixels</b> inside a 416×292 card. The reviewed wrapping artwork occupies about <b>223×223 pixels</b>. That uses only a small part of the 1280×720 game canvas. Teacher, Geologist, Boxer and Racer already have larger or full-stage paths, so the layout is inconsistent.</p><p>The fixed-size desktop audit window is a separate capture setting. Enlarging the browser screenshot or changing desktop window mode would not fix the small in-game working area.</p>'''
page+=image_ref(0,'Existing wrapping contact study · small working area','Whole dated 1280×720 canvas. The connected study is unbound and its complete action remains rejected at 4.1; current production WRAP remains 2.8.')
page+='''<h2>Working view and native resolution</h2><p>The rollout direction is a shared stage-size composition with Roshan and the object readable on the phone. Each career keeps its own room, costume and props. When a closer working view is needed, the same framing and entry/exit grammar applies in story and training.</p><p>Backgrounds require <b>at least 2048×2048 native coverage per playable screen</b>. Current complete wrapping review keys are 1672×941. They are useful source studies, but do not meet that background coverage requirement. Padding or upscaling into 2048 tiles does not supply missing native detail. Character and prop cutouts must instead carry enough detail for their measured display size and obey the texture import limits.</p><div class="note">A larger working view and higher native-resolution masters are separate requirements. Both need to pass before the replacement is considered ready.</div>
<h2>Existing artwork to preserve and reuse</h2><p>These complete images stay as source references. They show the intended connected Roshan/paper family. They are not a playable storyboard, accepted motion, or proof that the current game uses this wrapper.</p><div class="grid">'''
page+=image_ref(1,'Partial-fold source','Same-sheet start. Source opinion 4.5 provisional; inherited room 4.4. Fold trajectory remains incomplete.')
page+=image_ref(2,'Finished-twist source','Roshan visibly holds the narrow paper necks. Source opinion 4.5 provisional; opposite-motion midpoint is still missing.')
page+=image_ref(3,'Early-release source','Clean attached thumbs/cuffs and supported candy. Source 4.5 provisional; release trajectory and runtime remain unaccepted.')
page+='''</div><h2>Coverage by career</h2><p>'''+str(counts['base_phases'])+' base phase declarations across 15 careers, '+str(counts['enabled_plan_instances'])+' instances from the three enabled practice/stage plans, and '+str(counts['birthday_catalog_phases'])+' nonempty birthday adapter declarations produce '+str(len(rows))+''' planned rows. These are source declarations and plan expansions; they are not a count of distinct games or proof of activated story routes. Day One dynamic tasks, optional castle games, lesson variants and every-object substeps still need their separate census.</p><div class="table"><table><thead><tr><th>Career</th><th>Base phase sequence</th><th>Planned rows</th><th>Shared-format status</th></tr></thead><tbody>'''+''.join(families)+'''</tbody></table></div>
<h2>Rollout order</h2><ol><li>Measure and prototype the stage-size Candy working view against the ordinary training and story caller paths. Preserve the original game as a reversible baseline.</li><li>Resolve native source resolution, the missing opposed wrist midpoint, hand/paper anchors and the supported release. Review the complete action independently from the stills.</li><li>Apply the same finish/result/return grammar to Chef, Doctor, Farmer and Nursery, retaining their exact props, counts and physical workflows.</li><li>Check every remaining job, Day One task, optional castle activity and individual substep. Preserve specialist input, story dependencies and saved outcomes.</li><li>Validate ordinary routes, repeated/zero input, cancellation, pause/exit/restore, both canvas aspects and Mobile performance; then obtain device, child and owner review.</li></ol>
<p>All library opinions remain unchanged: 2160 known entries, 1063 inclusive priorities and 294 primary opinions pending. The all-job goal remains active; this owner direction does not close any finding or approve the comprehensive report.</p>
<details><summary>Every source-derived planned phase</summary><p><label for="filter">Filter by career, phase or route declaration</label><br><input id="filter" type="search" placeholder="e.g. candymaker or bandage"></p><p id="visibleCount">'''+str(len(rows))+''' planned rows</p><div class="table"><table><thead><tr><th>Stable planning ID</th><th>Phase</th><th>Declaration lane</th><th>Intended verb / prompt</th><th>Acceptance</th></tr></thead><tbody id="rows">'''+''.join(row_html)+'''</tbody></table></div></details>
<h2>Evidence and independent checks</h2><p><a href="CURRENT_LAYOUT_AND_COMPLETION_TRACE.json">Current source trace</a> · <a href="ILLUSTRATION_REFERENCES.json">Exact unchanged image hashes</a> · <a href="AUTHORITY_START.json">Rules/findings reviewed at scope change</a> · <a href="previous_AE_remote_verified/RESULT.json">Earlier complete review publication receipt</a></p><p class="facts">This planning revision changes no production source, artwork pixels, save schema, numerical opinion, finding lifecycle, integration or release status. MA-VIS-006 remains CONFIRMED_OPEN; MA-PLAY-004 remains IN_PROGRESS. Common runtime timing and sockets are unmeasured and unassigned.</p>
<script>const filter=document.getElementById('filter');filter.addEventListener('input',()=>{const q=filter.value.trim().toLowerCase();let n=0;for(const r of document.querySelectorAll('#rows tr')){r.hidden=!r.textContent.toLowerCase().includes(q);if(!r.hidden)n++}document.getElementById('visibleCount').textContent=n+' planned rows'});</script></main></html>'''
(P/'index.html').write_text(page,encoding='utf-8',newline='\n')

# Update authority navigation without altering old evidence or canonical lifecycle.
master=B/'audit/MASTER_AUDIT_2026-08-09.md';text=master.read_text(encoding='utf-8-sig');anchor='## 0. Planning entry\n';assert anchor in text
notice='\nOwner-selected job presentation direction (2026-10-03): [shared Roshan final-action brief, source-derived phase coverage and resolution/layout inventory](job_final_action_consistency_v1_20261003/index.html). Every Roshan-owned task/substep across actual job days and Opera training must visibly end with her meaningful work on the same object, safe settling and a readable result before celebration/next. Legacy392×232 activity cards and about223×223 wrapping display are identified as layout gaps; shared stage-size presentation and genuine native2048×2048 background coverage per playable screen are the rollout targets. Current1672×941 source keys do not prove that coverage. Runtime/art/scores unchanged; all source/motion/actual-route/device/child/owner/comprehensive acceptance gaps and MA-VIS-006 CONFIRMED_OPEN/MA-PLAY-004 IN_PROGRESS remain. The choice accepts direction only. [Versioned contract](../'+D+').\n'
text=text.replace(anchor,anchor+notice,1)
index_anchor='## Development task index'
if index_anchor not in text:
 index_anchor=next(line for line in text.splitlines() if line.startswith('#') and 'development task index' in line.lower())
text=text.replace(index_anchor,index_anchor+'\n\nJob final-action consistency and native-resolution rollout: [owner-selected contract](../'+D+') · [illustrated scoped coverage](job_final_action_consistency_v1_20261003/index.html). Runtime completion remains pending; do not transfer source/plan scores to action acceptance.\n',1)
master.write_text(text,encoding='utf-8',newline='\n')
design=B/'design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md';text=design.read_text(encoding='utf-8-sig');marker='`DL-INT-03`';pos=text.index(marker)
paragraph='Owner-selected job presentation direction (2026-10-03): Roshan herself visibly performs the last meaningful task action in the shared work sequence, then settles and leaves the earned result readable before celebration or the next step. Apply the same grammar across actual job days and Opera training without taking the child’s choices/gestures away or awarding progress from a clip ending. Use the [versioned final-action contract](animation/JOB_FINAL_ACTION_PRESENTATION_V1.json) for stage-size framing, native-resolution requirements and specialist/lifecycle boundaries. The direction does not accept any current asset, motion or runtime repair.\n\n'
text=text[:pos]+paragraph+text[pos:];design.write_text(text,encoding='utf-8',newline='\n')
ledger=B/'design/05_DOC_LEDGER.md';text=ledger.read_text(encoding='utf-8-sig');line=next(l for l in text.splitlines() if '`design/animation/ANIMATION_PRODUCTION_PROTOCOL.md`' in l)
newrow='| `'+D+'` | 🟢 | `BINDING_OPERATIONAL` for the owner-selected shared Roshan final-action presentation across all jobs/training, stage-size layout direction and native-resolution receipts. Source-derived coverage remains a plan; specialist, input/contact/save, cinematic, device/child/owner and release authorities remain unchanged. Runtime rollout and artwork acceptance are pending. |'
text=text.replace(line,line+'\n'+newrow,1);ledger.write_text(text,encoding='utf-8',newline='\n')
animation=B/'audit/animation/README.md';text=animation.read_text(encoding='utf-8-sig');at=text.find('\n')+1;text=text[:at]+'\nOwner-selected 2026-10-03: [all-job shared final-action and native-resolution brief](../job_final_action_consistency_v1_20261003/index.html) · [versioned contract](../../'+D+'). Roshan performs each task’s last meaningful action; current small-card layouts and genuine native background resolution are rollout gaps. Runtime and all acceptance lanes remain pending.\n'+text[at:];animation.write_text(text,encoding='utf-8',newline='\n')
library=L/'index.html';text=library.read_text(encoding='utf-8-sig');pos=text.index('</h1>')+len('</h1>');banner='<div class="notice"><p><strong>Owner-selected shared job format · 3 October 2026.</strong> Roshan visibly finishes every task; stage-size working views and genuine native-resolution masters are the rollout targets. <a href="../job_final_action_consistency_v1_20261003/index.html">Illustrated format and coverage brief</a>. Runtime rollout and acceptance remain pending; individual scores are unchanged.</p></div>'
text=text[:pos]+banner+text[pos:];library.write_text(text,encoding='utf-8',newline='\n')
copy(ROOT/'tmp/job_consistency_scope_v680.py',P/'review_tools/job_consistency_scope_v680.py');copy(Path(__file__),P/'review_tools/build_job_consistency_v681.py')
put(P/'BUILD_RECEIPT.json',dict(status='SHARED_DIRECTION_AND_COVERAGE_RECORDED_NOT_IMPLEMENTED',baseline=BASE,checked_utc=now(),counts=counts,new_pixels=0,runtime_changed=False,scores_changed=False,owner_product_acceptance=None,goal_status='active',previous_publication_all24975_bytes_verified=True))
files=[rel(p) for p in P.rglob('*') if p.is_file()]+[D,'audit/MASTER_AUDIT_2026-08-09.md','design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md','design/05_DOC_LEDGER.md','audit/animation/README.md','audit/job_artwork_refinement_live/index.html']
impact=json.loads(IP.read_text());impact['files']=sorted(files);impact['validation'].append(dict(command='Literal phase reader and previous complete publication journal archive',result='PASS',evidence=REL+'/BUILD_RECEIPT.json'));put(IP,impact)
for r in preserved:assert sha((B/r['path']).read_bytes())==r['sha256']
put(P/'REGISTER_BOUNDARY_AFTER.json',dict(files=preserved,all_literal_hashes_match=True,scores_changed=False))
impact['files'].append(REL+'/REGISTER_BOUNDARY_AFTER.json');impact['files'].sort();put(IP,impact)
print(json.dumps(dict(status='BUILT',counts=counts,files=len(impact['files']),prior_remote_rows_archived=24975,prior_ci_status=ci['status'],prior_ci_conclusion=ci['conclusion'],scores_unchanged=True,runtime_unchanged=True)))
