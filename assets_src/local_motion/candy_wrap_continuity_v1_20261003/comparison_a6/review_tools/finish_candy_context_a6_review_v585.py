from pathlib import Path
import datetime,hashlib,json,shutil,subprocess
B=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');P=B/'assets_src/local_motion/candy_wrap_continuity_v1_20261003';Q=P/'comparison_a6';A=Q/'attempt01';C=B/'assets_src/imagegen/candy_wrap_scene_context_v1_20261003';L=B/'audit/job_artwork_refinement_live'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def put(p,raw):n=p.with_name(p.name+'.v585_next');n.write_bytes(raw);n.replace(p)
def write(p,d,compact=False):put(p,(json.dumps(d,ensure_ascii=False,indent=None if compact else 2,separators=(',',':') if compact else None)+'\n').encode())
idx=read(A/'INDEX.json');assert len(idx['frames'])==41 and len(idx['boards'])==7
observations=[
 (4.5,'The original complete painted scene starts with two connected mittens, one supported sweet and an unfinished gold flap; no action consequence yet.'),
 (4.4,'Both wrists stay attached as a tiny downward grip change begins; the red crescent remains exposed.'),
 (4.4,'The hands begin pressing the raised edge toward the tabletop, preserving the starting contact group.'),
 (4.3,'The flap lowers slightly while both mittens still grip it; a substantial red crescent remains below the edge.'),
 (4.3,'The long edge comes nearer the sweet, but it has not covered the front red crescent.'),
 (4.2,'The gold edge flattens locally between both mittens; full coverage and hand release remain absent.'),
 (4.2,'Roshan leans toward the work and both gloves press the partial flap; the red face remains visible.'),
 (4.2,'A small pressing adjustment continues; paper still ends above the exposed red front.'),
 (4.1,'Both mittens stay in contact with the lowered strip, but the covering edge does not cross the entire sweet.'),
 (4.1,'The strip lies nearer the tabletop while the same uncovered red crescent persists.'),
 (4.1,'The hands and torso lean forward again; the partial fold remains a band across the upper sweet.'),
 (4.1,'The pressing pose continues without a visible completed covering fold.'),
 (4.0,'The gold flap is flatter than in A5, but red remains exposed; this is partial contact, not the declared exit.'),
 (4.0,'Both hands shift around the same lowered flap; the red front remains continuously visible.'),
 (4.0,'The left glove presses a small fold while the right keeps gripping; the sweet remains only partly covered.'),
 (4.0,'A quiet press continues with no new downward covering front across the exposed red crescent.'),
 (4.0,'The hands lower slightly again; the golden strip still leaves a red edge at the front.'),
 (3.9,'The torso leans toward the table and mittens keep holding; neither full coverage nor release occurs.'),
 (3.9,'The partial flap stays pressed between the hands with the red front still exposed.'),
 (3.9,'A repeated pressure pose replaces the requested single completed fold and settle.'),
 (3.9,'Both hands hold the lowered band while the body continues leaning; the wrapper remains unfinished.'),
 (3.9,'The red crescent is still visible under the band, and the gloves do not loosen beside a finished wrapper.'),
 (3.8,'The torso leans farther down while the hands remain clenched; the exposed red area is not covered.'),
 (3.8,'Both mittens keep pressing the incomplete flap; the hand roles have no completed consequence.'),
 (3.6,'Teal cuffs begin gaining irregular extra painted streaks while the same red crescent stays visible.'),
 (3.4,'Native detail confirms smeared/ghosted teal-gold sleeve forms near both wrists; the flap remains incomplete.'),
 (3.3,'The cuff silhouettes lengthen and blur outside their original bounds while the mittens stay on the strip.'),
 (3.2,'Elongated teal-gold cuff shapes spread farther outward; no released hand or completed fold appears.'),
 (3.1,'The right cuff curls away from the wrist and the supported red sweet starts changing outline.'),
 (3.0,'Both cuff forms flare beyond the original simple wrist bands; red visibility increases rather than closes.'),
 (2.9,'The sleeves/cuffs become long curling forms and the paper band retreats above a more fully exposed sweet.'),
 (2.8,'The gold edge draws back toward Roshan’s vest; the red sweet becomes fully exposed in front.'),
 (2.8,'The torso is low over the work, cuffs remain distorted and a purple point begins appearing at the top of the red sweet.'),
 (2.7,'The complete red sweet is exposed again; its upper edge gains an unsupported purple protrusion.'),
 (2.7,'The new purple point and long teal cuff curls persist; the paper does not cover the sweet.'),
 (2.6,'A low torso pose still grips the gold band; altered cuff topology and candy outline prevent acceptance.'),
 (2.6,'The red oval remains fully exposed with the purple point above it; the two original hand shapes continue to change.'),
 (2.6,'The gloves remain pressed near the lifted-back band; no finished fold or relaxed released hands exist.'),
 (2.5,'The mouth/face and glove contours deform further while the band stays behind the exposed sweet.'),
 (2.5,'The near-final image retains the curling cuffs, changed red-sweet shape and absent covering consequence.'),
 (2.4,'Final canvas: fully exposed red sweet with a purple point, elongated teal cuff curls, held band and no release. The declared complete-cover endpoint fails.')
]
assert len(observations)==41
frames=[]
for row,(score,evaluation) in zip(idx['frames'],observations):
    assert sha(B/row['path'])==row['sha256'];frames.append(dict(**row,visual_frame_score=score,evaluation=evaluation,direct_native_review=True,priority=score<=4.5))
components=[
 ('Exactly two owned arms and hand attachment',4.2,'The two original mittens remain Roshan-owned and no outside human arm appears. Late wrist/cuff ghosting prevents a clean topology pass.'),
 ('Mitten and costume continuity',2.5,'After about frame24 the teal cuffs acquire smeared duplicate-looking streaks, then long curling shapes outside the original wrist-band design.'),
 ('Same sweet, support and target continuity',3.4,'One sweet remains on the tabletop, but its red oval changes shape and develops a purple point late in the take. Preserving object count does not pass identity.'),
 ('Attached golden-paper material and bend',3.5,'The partial flap lowers and is pressed locally, then retreats toward the body. The same continuous covering bend across the whole sweet is never completed.'),
 ('Far long-edge direction and complete coverage',1.5,'Small early downward motion does not cover the remaining red crescent. The final red sweet is fully exposed again.'),
 ('Useful hand roles and contact pressure',3.6,'Both mittens visibly press or hold the band in the early/middle span, but no steady brace/one useful completed covering gesture is established.'),
 ('Release and settled completed fold',1.8,'Hands remain in the work grip through the final frame; there is no relaxed release beside a stable covered sweet.'),
 ('Painted character/room style and identity',3.8,'The room and broad painted family remain recognizable, but late cuff, face and sweet distortions prevent continuity acceptance.'),
 ('Attention, timing and one useful consequence',3.2,'Roshan leans toward the work, but repeated pressure/leaning and late distortion replace the required fold, consequence and quiet finish.'),
 ('Whole prompt-only downward far-fold component',2.6,'Rejected: incomplete coverage/release plus late costume and candy deformation. No complete-wrapper or current-game score is raised.')
]
write(A/'DIRECT_REVIEW.json',dict(status='REJECTED_NO_COMPLETE_COVER_OR_RELEASE_LATE_CUFF_AND_SWEET_DISTORTION',reviewed_utc=now(),whole_component_score=2.6,complete_wrapping_score=None,current_production_wrap_score=2.8,direct_every_native_frame_review=True,frame_count=41,board_count=7,native_details_reviewed=[0,12,25,40],individual_frames=frames,component_opinions=[dict(item=i,score=s,evaluation=e,priority=s<=4.5) for i,s,e in components],qualification='Every41 complete native decoded canvases inspected on seven non-resampled original-size boards, plus four exact native details. All41 individual canvas opinions and10 component evaluations written. Exact A5 source/input/seed/settings/workflow, prompt-only change. Reference-only, unbound; source floor cannot accept absent closure, changed cuffs/sweet, runtime/cinematic/device/child/owner/full-wrapper acceptance.'))
write(Q/'REVIEW_STATUS.json',dict(status='LOCAL_REFERENCE_REJECTED_A6_2_6',whole_component_score=2.6,native_frames_reviewed=41,component_opinions=10,source_still_score=4.5,runtime_integration=False,owner_acceptance=None,manifest_preserved_sha256=sha(Q/'MANIFEST.json')))
idx.update(status='ALL41_NATIVE_FRAMES_DIRECTLY_REVIEWED_REFERENCE_REJECTED_2_6',direct_review='DIRECT_REVIEW.json');write(A/'INDEX.json',idx)
write(C/'NEXT_REPAIR_GAP.json',dict(status='SPECIFIC_COMPLETE_COVERING_POSE_GAP_RECORDED',recorded_utc=now(),existing_source='attempt02/native.png',existing_source_sha256=sha(C/'attempt02/native.png'),reuse_decision='Keep the clean4.5 source, established painted character/room and specific gold-paper/red-sweet identity. Do not regenerate them for novelty.',missing_required_state='The far gold edge visibly bends around and completely covers the same supported red sweet while the original two sleeve-attached mittens press the fold; then a small release. A5/A6 fail this endpoint.',next_candidate_scope='One separately preserved targeted complete-covering pose before any more same-source local motion retries. This record is a gap, not a generated candidate, causal diagnosis or accepted frame.',original_full_wrap_still_required=['long-edge cover','neck pinches around same sweet','opposing end twists','release with a stable completed two-ended wrapper'],current_game_wrap_score=2.8,best_contextual_component_score=3.1,runtime_bound=False,owner_acceptance=None))
write(C/'LOCAL_MOTION_REVIEW_SUMMARY.json',dict(status='BOTH_CONTEXTUAL_NATIVE_STUDIES_DIRECTLY_REVIEWED_AND_REJECTED',reviewed_utc=now(),source_attempts=2,source_opinions=16,source_A1_score=4.2,source_A2_starting_score=4.5,background_source_component=4.4,motion_attempts=[dict(attempt='A5',native_frames=41,boards=7,native_details=4,component_opinions=10,whole_component_score=3.1,failure='Lifts flap away and exposes sweet; no cover/release.'),dict(attempt='A6',native_frames=41,boards=7,native_details=4,component_opinions=10,whole_component_score=2.6,failure='No complete cover/release, late cuff/sweet distortion.')],all_A1_A6_native_frames_reviewed=246,all_A1_A6_component_opinions=60,current_production_wrap_score=2.8,runtime_bound=False,owner_acceptance=None,qualification='Exact first four failures preserved. All original required wrapper stages retained. Motion reference only, not runtime/cinematic pixels or owner-approved comprehensive all-job report.'))
builder=P/'review_tools/build_candy_local_review_v582.py';s=builder.read_text(encoding='utf-8');s=s.replace('A6 prompt-only downward covering fold is separately reviewed when its native results are available.','A6 downward-fold2.6 is rejected for absent complete cover/release and late cuff/sweet distortion. Every41 native frame is directly reviewed.');s=s.replace('A5 action3.1 is independently rejected.','A5 action3.1 and A6 action2.6 are independently rejected.');put(builder,s.encode())
reg=read(L/'ALL_ITEMS.json');assert reg['display_revision']=='V49' and len(reg['items'])==2049
write(C/'PRE_A6_CURRENT_TEXT_SNAPSHOT_V585.json',dict(display_revision=reg['display_revision'],prior_scope=reg['scope'],prior_review_resource=reg['review_resources'][-1],qualification='Exact draft current text before A6 completion, preserved as text history without duplicating the full registered source opinions.'))
reg['scope']=reg['scope'].replace('Every205 A1-A5 local motion frame and50 components reviewed','Every246 A1-A6 local motion frame and60 components reviewed').replace('A6 one prompt-only direction comparison remains separately audited.','A6 prompt-only direction comparison2.6 rejected for absent complete cover/release and late cuff/sweet distortion.');reg['updated_utc']=now();reg['review_resources'][-1]['scope']='Two complete context sources/16 source opinions. Clean starting still4.5 provisional; independent A5 action3.1/A6 action2.6 rejected. All246 A1-A6 native frames/60 components illustrated.';write(L/'ALL_ITEMS.json',reg,True)
for name in ['index.html','all_items.html']:
    p=L/name;t=p.read_text(encoding='utf-8').replace('A6 direction comparison is separate.','A6 downward-fold2.6 is also rejected; every246 A1-A6 frame is individually reviewed.');put(p,t.encode())
for path in ['audit/MASTER_AUDIT_2026-08-09.md','audit/findings/ACTIVE_FINDINGS_2026-08-13.md','audit/animation/README.md']:
    p=B/path;t=p.read_text(encoding='utf-8');t=t.replace('Every205 A1-A5 local native frames/35 original-size boards/16 native details/50 component opinions','Every246 A1-A6 local native frames/42 original-size boards/20 native details/60 component opinions').replace('One A6 prompt-only downward covering comparison keeps the exact source/input/seed/settings/developed workflow; its own native/action review remains separate.','A6 prompt-only downward covering comparison keeps the exact source/input/seed/settings/developed workflow; every41 native frames reviewed, whole2.6 rejected for absent complete cover/release and late cuff/sweet distortion.');put(p,t.encode())
ledger=B/'design/05_DOC_LEDGER.md';t=ledger.read_text(encoding='utf-8').replace('A6 independent direction review separate.','A6 every41 native frames/10 components rejected2.6 for absent complete cover/release and late cuff/sweet distortion.');put(ledger,t.encode())
shutil.copyfile(__file__,Q/'review_tools'/Path(__file__).name)
ip=B/'design/audit_impacts/job-candy-painted-context-source-20261003.json';d=read(ip);d['scope']+=' Every41 A6 native frames/10 components now rejected2.6. All246 A1-A6 canvases individually illustrated; exact current production unchanged and the next complete-covering pose gap recorded.'
d['validation'].append(dict(command='Every41 A6 native canvases and10 separate component opinions',result='FAIL',evidence=(A/'DIRECT_REVIEW.json').relative_to(B).as_posix()+'; no complete cover/release, late cuff/sweet distortion, whole2.6 rejected. All original exit criteria retained.'))
d['files']=sorted(set(d['files'])|{p.relative_to(B).as_posix() for base in(C,P) for p in base.rglob('*') if p.is_file()});write(ip,d)
for target in [builder,L/'review_tools/refresh_current_job_review_v49.py']:
    cmd=['C:/Users/Peter/AppData/Local/Python/bin/python.exe','-X','utf8','-B',str(target)];r=subprocess.run(cmd,cwd=B,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW);assert r.returncode==0,r.stderr.decode();print(r.stdout.decode().strip())
allow=B/'tmp/v2_preview_allowed.json';write(allow,sorted(set(read(allow))|{p.relative_to(B).as_posix() for base in(C,P) for p in base.rglob('*') if p.is_file()}))
print(json.dumps(dict(status='ALL246_NATIVE_FRAMES_AND60_COMPONENTS_REVIEWED_A6_REJECTED_2_6',current_game_wrap_score=2.8,registered_items=2049,all783_production_literals_unchanged=read(L/'CURRENT_BOUNDARY_REFRESH.json')['candy_capture_boundary_match'])))
