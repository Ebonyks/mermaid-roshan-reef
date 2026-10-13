from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import subprocess

B = Path(__file__).resolve().parent
R = Path(r'C:\Users\Peter\.codex\worktrees\flat-vector-art-audit-20261007\mermaid-roshan-reef')
O = B / 'root_picture_actions_review_20261012'
E = r'C:\Users\Peter\AppData\Local\Programs\MermaidReefTools\Godot\4.7.2\godot_console.exe'
REV = '6cde8aeae04aaedcc0b1ff22a05ef93ab9bf666f'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def write(p, x):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(x, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')

def copy(p, q):
    q.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(p, q)
    assert sha(p) == sha(q)

runs = [
 ('partial_buttons','root_picture_actions_20261013T011656','FAIL: Snowman mouse circles did not progress. Trampoline three taps and Xmas six taps progressed, with guarded native states retained. This is not a green combined run.'),
 ('rejected_mouse','root_snow_actions_v2_20261013T011951','FAIL: viewport local mouse remains outside rolling region; missing direct-entry picture tick also applies. Diagnostic only, not game defect.'),
 ('rejected_axes_no_tick','root_snow_axes_v3_20261013T012225','FAIL: raw-axis route entered, but direct-entry fixture did not schedule the production picture tick. Diagnostic only.'),
 ('bounded_snow','root_snow_bridge_v4_20261013T012443','PASS: raw axis circles plus three face taps through chase entry, using declared synthetic unmapped-controller mode and standalone production-tick bridge. No natural route or phone-touch acceptance.'),
 ('rejected_hold_right','root_snow_followthrough_v5_20261013T012850','FAIL: held-right test caught one bite, then failed to follow direction changes within cap. Diagnostic input-policy limit, not production defect.'),
 ('rejected_frame_expectation','root_snow_followthrough_v6_20261013T013324','FAIL: all bites/carrot completed; third-bite capture evaluated its own medal expectation before frame_post_draw advanced into payoff. Timing-expectation error preserved.'),
 ('completed_snow_fixture','root_snow_followthrough_v7_20261013T013624','PASS: all growth, stack, face, chase, three bites and carrot payoff through guided raw input, synthetic unmapped-controller mode and production-tick bridge. Zero progress-counter assignment; no device/child/owner/natural-route acceptance.')
]
captures = []
for role, run, limit in runs:
    receipt = json.loads((B/(run+'_receipt.json')).read_text(encoding='utf-8'))
    assert receipt['changed_runtime_sources'] == [] and receipt['runtime_source_file_count'] == 6452
    for suffix in ['_receipt.json','_source_before.json','_capture.log']:
        copy(B/(run+suffix),O/'receipts'/(run+suffix))
    for aspect in ['1280x720','1600x720']:
        p = B/run/aspect/'capture_manifest.json'
        m = json.loads(p.read_text(encoding='utf-8'))
        assert m['source_revision'] == REV and m['normal_save_before'] == m['normal_save_after']
        copy(p,O/'captures'/role/aspect/p.name)
        if role in ['bounded_snow','completed_snow_fixture']:
            assert m['errors'] == [] and receipt['returncode'] == 0
        for state in m['states']:
            p = B/run/aspect/state['image']['file']
            assert sha(p) == state['image']['sha256']
            q = O/'captures'/role/aspect/p.name
            copy(p,q)
            captures.append({'path':q.relative_to(O).as_posix(),'run_role':role,'state_id':state['id'],'aspect':aspect,'sha256':sha(p),'run_returncode':receipt['returncode'],'phase':state.get('phase'),'balls':state.get('balls'),'face':state.get('face'),'bites':state.get('bites'),'won':state.get('won'),'presentation':state.get('presentation'),'input':state['input'],'scope_limit':limit})

harnesses = ['root_capture_picture_actions_20261012.gd','root_capture_snow_actions_v2_20261012.gd','root_capture_snow_axes_v3_20261012.gd','root_capture_snow_bridge_v4_20261012.gd','root_capture_snow_followthrough_v5_20261012.gd','root_capture_snow_followthrough_v6_20261012.gd','root_capture_snow_followthrough_v7_20261012.gd']
gates = []
for name in harnesses:
    p = B/name
    copy(p,O/'harnesses'/name)
    for command in [['python','-m','gdtoolkit.parser',str(p)],['python','-B',str(R/'tools/lint_inference.py'),str(p)],[E,'--headless','--path',str(R),'--check-only','-s',str(p)]]:
        result = subprocess.run(command,cwd=R,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=90,creationflags=subprocess.CREATE_NO_WINDOW)
        gates.append({'command':command,'returncode':result.returncode,'stdout':result.stdout,'stderr':result.stderr,'scope':'Harness compilation/type checks only; failed diagnostic execution receipts remain failed.'})
        assert result.returncode == 0,gates[-1]
for name in ['root_picture_capture_launch.py','build_root_picture_actions_harness.py',Path(__file__).name]:
    copy(B/name,O/'harnesses'/name)
copy(B/'root_picture_scope_dispositions_20261012.json',O/'source_scope_dispositions.json')

viewed = [
 'captures/partial_buttons/1280x720/trampoline_bounce1_apex.png',
 'captures/partial_buttons/1280x720/trampoline_bounce2_apex.png',
 'captures/partial_buttons/1280x720/trampoline_bounce3_apex.png',
 'captures/partial_buttons/1280x720/xmas_ornament5_placed.png',
 'captures/partial_buttons/1280x720/xmas_flower_payoff.png',
 'captures/bounded_snow/1280x720/snow_ball3_stacked.png',
 'captures/bounded_snow/1280x720/snow_chase_entry.png',
 'captures/bounded_snow/1600x720/snow_ball1_growing.png',
 *['captures/completed_snow_fixture/1280x720/'+name+'.png' for name in ['snow_bite1','snow_bite2','snow_bite3','snow_carrot_collected_payoff']]
]
assert len(viewed) == len(set(viewed)) == 12
for p in viewed:
    assert (O/p).exists()

def obs(i,title,ids,classification,weakness,comparison,proposal,proof,limits):
    return {'id':i,'title':title,'existing_piece_ids':ids,'classification':classification,'observation':weakness,'same_scene_comparison':comparison,'proposed_update':proposal,'source_or_native_evidence':proof,'limits':limits,'status':'OPEN_CONTEXT_REVIEW','accepted_removals':0}

observations = [
 obs('ROOTACT-01','Snow field and ball material across action',['FV-55B5EF60A12C','FV-C99F706798D3'],'Confirmed visible procedural art','Rolling and stacked balls remain flat white rounded panels with generic rims/shadows over a large grey panel ground.','The approved painted carrot, coal, Roshan and source-book snow surfaces carry authored contours, material and light. Coal is intentionally angular/dark; snow should remain soft/cool.','Reuse a suitable clean painted snowball and calm snowy ground if found. Otherwise name only those gaps, drawing one coherent ball family for rolling, three stack sizes and eating states. Retain child construction and separate face placement.',['captures/bounded_snow/1600x720/snow_ball1_growing.png','captures/bounded_snow/1280x720/snow_ball3_stacked.png','assets/book/hall/p_snowman.jpg'],'Reference page protected and unchanged; context fixture does not establish natural route, phone touch or full-speed motion acceptance.'),
 obs('ROOTACT-02','Snowman stacked support/contact',['FV-C99F706798D3'],'Source and visual contact candidate','The top sphere reads as separated from the middle by a narrow gap/dark seam.','Current source centers210/385 with radii72/98 yield a5px separation between head bottom282 and middle top287 before rims/shadows; the lower pair overlap. Painted snowbook volumes join as one supported stack.','Review painted contact footprints and stable stacking anchors together. Repair support readability rather than placing an unrelated new sticker over each generic disc. Keep three independently constructed balls and face anchors coherent.',['scripts/games/picture_games.gd:_mg_snow_new_ball/_mg_snow_ball_done','captures/bounded_snow/1280x720/snow_ball3_stacked.png'],'5px is source geometry, not a measured pixel gap or child verdict. All scaling, stack transition and chase occlusions require review.'),
 obs('ROOTACT-03','Coal eye reuse',['FV-0FCB49F07274'],'Existing painted raster; no automatic vector defect','The live coal is the later painted Pass35 card, not the historical orthographic render.','Dark irregular facets, indigo contour and subtle surface marks fit the painted carrot family while distinguishing hard coal from soft snow. Repeated eyes use the same whole card.','Prefer retaining current approved coal and review its size/contact inside the new snow-head material. Audit card-frame presentation separately; no novelty redraw commissioned.',['ASSET_LICENSES.md historical row161 and superseding row224','assets/mg/coal.png','captures/bounded_snow/1280x720/snow_chase_entry.png'],'42x42 face rects and110px tap cards have different readability needs. Device/child/owner acceptance remains open.'),
 obs('ROOTACT-04','Snowman bite acting/contact',['FV-C99F706798D3'],'Existing presentation gap; requires animation/contact context','Balls disappear using scale(1.3,0.2) over0.18s. Third/head eating occurs high above Roshan’s fixed chase height, and the last head can remain briefly as a thin white oval during the payoff.','The detailed Roshan card remains at chase center y470 while the head begins at y210. Better snow texture alone does not establish a readable eating/contact action.','Audit the entire bite transition and authored contact/settle cues before accepting a new ball family. Any needed character action uses approved identity states and a bounded2D animation job card, preserving the existing chase/catch objective and source provenance.',['scripts/games/picture_games.gd:_mg_snow_chase_phase/_mg_tick_snow_chase','captures/completed_snow_fixture/1280x720/snow_bite2.png','captures/completed_snow_fixture/1280x720/snow_bite3.png','captures/completed_snow_fixture/1280x720/snow_carrot_collected_payoff.png'],'Stills and source establish a presentation concern, not a reviewed full-motion verdict. No character pixels or gameplay mechanics changed.'),
 obs('ROOTACT-05','Xmas completed topper obscured by reward',['FV-E9E82E0C6703'],'Source and native confirmed reward-placement defect','The medal card covers nearly the entire newly placed friendship-flower topper.','The detailed tree and five ornaments are readable before completion. The meaningful new sixth object is covered at the exact payoff.','Preserve tree, ornaments and protected flower. Give the one-owner medal a per-caller placement or sequencing that lets the child see the complete decorated tree/topper; replacing only its material at the same bounds is insufficient.',['captures/partial_buttons/1280x720/xmas_ornament5_placed.png','captures/partial_buttons/1280x720/xmas_flower_payoff.png','Source flower rect570,135/140x130; medal rect490,140/300x230; medal2.2s and picture close1.6s'],'No source image edit or new tree commissioned. Full lifetime, reentry and phone safe-area checks still required.'),
 obs('ROOTACT-06','Trampoline objective/header placement',['FV-C6F64FAA2F32','FV-E9E82E0C6703'],'Native confirmed target/header overlap','The large painted objective star sits over the instruction panel through all three bounce apex captures. The detached mat highlight remains below the pad.','Roshan, star and proposed trampoline need a clear shared play space; the header should not compete with the object she reaches.','Use the protected trampoline page as source appearance/context direction for a blue padded frame and dark mesh. Inventory a complete reusable mat, otherwise derive or draw only the clean isolated pad gap. Test header/target spacing and mat contact at every bounce, preserving one-finger input and the existing three-bounce objective.',['captures/partial_buttons/1280x720/trampoline_bounce1_apex.png','captures/partial_buttons/1280x720/trampoline_bounce2_apex.png','captures/partial_buttons/1280x720/trampoline_bounce3_apex.png','assets/book/hall/p_trampoline.jpg'],'Book people and overlapping mats cannot be copied blindly into the current playable object. Original remains protected. Full-speed jump/landing review is pending.'),
 obs('ROOTACT-07','Xmas flower enabled-state appearance',['FV-E1D26D3057A3'],'Protected-source presentation candidate','The enabled flower uses modulate(1.3,1.3,1.0), which makes it paler/brighter than its source card and neighboring ornaments.','The disabled flower starts at0.5 grey; five placed ornaments retain their authored jewel/material appearance.','Preserve the protected flower pixels and audit a separate compatible selection/ready cue around it instead of relying on a source-color wash. Keep locked/enabled distinction and exact unlock behavior.',['captures/partial_buttons/1280x720/xmas_ornament5_placed.png','scripts/games/picture_games.gd:_mg_build_xmas/_mg_xmas_tap'],'Presentation proposal only; no permission inferred to restyle the protected flower.'),
 obs('ROOTACT-08','Sticker reward icons and reward overlap',[],'Visible progress/decorative glyph art plus ordinary text','Snowman sticker and carrot sticker toasts use emoji artwork. The carrot toast crosses the top of the medal card during payoff.','Painted coal/carrot gameplay objects have stable project identity; emoji appearance depends on the platform/font rather than the authored scene family.','Inventory authored sticker-icon reuse. Treat the decorative/progress icon separately from ordinary label text, and audit the two simultaneous reward surfaces for hierarchy/overlap while preserving every save key and award trigger.',['scripts/main.gd:STICKER_DEFS/award_sticker/_sticker_toast','captures/bounded_snow/1280x720/snow_chase_entry.png','captures/completed_snow_fixture/1280x720/snow_carrot_collected_payoff.png'],'Bind exact glyph and caller roles to the existing glyph inventory before adding counts. Device font/render evidence remains pending.')
]

reuse = []
for path,limit in [
 ('assets/book/hall/p_snowman.jpg','Protected source appearance reference. No exact source-to-compound-cutout derivation proved here; existing snow scene includes people/face/buttons and differs from rolling/empty-ball phases.'),
 ('assets/book/hall/p_trampoline.jpg','Protected source appearance reference. Blue padded frames/dark mesh are relevant; foreground people and occluded mats prevent blind direct reuse.'),
 ('assets/mg/snowman.png','Inspected compound cutout includes Roshan fragment, damaged head, face/buttons; not a ready clean rolling/stack ball. Generic license row93 does not by itself establish exact derivation.'),
 ('assets/art35/cards/mg/snowman_snowman.png','Inspected smaller variant of the same compound motif, not a cleaner independent state; bytes differ.'),
 ('assets/mg/coal.png','Inspected painted Pass35 whole coal card. Preserve unless exact scene/phone review identifies a named gap; historical orthographic row is superseded for these current pixels.')]:
    p = R/path
    from PIL import Image
    im = Image.open(p)
    reuse.append({'path':path,'sha256':sha(p),'dimensions':list(im.size),'inspected':True,'modifications':'NONE','fit_limit':limit})

review = {
 'schema':'reef.root_picture_action_review/1','recorded_at_utc':datetime.now(timezone.utc).isoformat(),'source_revision':REV,
 'reviewer':'Root Codex independent inspection; not owner/child/device acceptance',
 'rules':['DL-AUTH-05','DL-AUTH-06','DL-AUTH-07','DL-VIS-01','DL-VIS-02','DL-VIS-03','DL-VIS-04','DL-VIS-05','DL-VIS-06','DL-VIS-07','DL-VIS-08','DL-ASSET-01','DL-ASSET-02','DL-ASSET-03','DL-ASSET-04','DL-ASSET-05','DL-ASSET-06','DL-MOT-14','DL-MOT-15','DL-MOT-16'],
 'related_findings':['MA-VIS-006','MA-VIS-007','MA-VIS-008','MA-DOC-008'],
 'capture_count':len(captures),'independently_viewed_unique_native_count':len(viewed),'reviewed_capture_paths':viewed,
 'captures':captures,'observations':observations,'observation_count':len(observations),'reuse_inventory':reuse,
 'evidence_lanes':{'implementation':'UNCHANGED','machine':'Harness syntax/type/engine compilation passes separately. Execution histories preserve failed runs; bounded snow and completed snow fixture pass. All6452 runtime sources and normal-save suffix fingerprints unchanged. Not full production CI.','visual':'Eight bounded context observations and12 unique independently viewed native frames.','device':'PENDING','child':'PENDING','owner':'PENDING','full_game_inventory':'PENDING','accepted_removals':0},
 'scope_limits':['All entries direct production API fixtures, not natural castle/Lagoon child route.','Snowman explicitly sets synthetic unmapped-controller environment and schedules unchanged _tick_mg2d once per actual Node process frame; no progress-counter assignment.','Guided chase inputs track live run_x and do not establish preschool control usability.','No exact human motion/contact review, phone performance, pause/save/resume/fallback closure or art acceptance.','Original failed attempts remain failed; successful revised capture does not rewrite history.','No creative image edits, new generation or runtime change.','Local staging only until published with complete hashes and exact remote access verification.']
}
write(O/'review.json',review)
write(O/'harness_validation.json',{'schema':1,'gates':gates,'all_compile_pass':all(x['returncode']==0 for x in gates),'execution_pass_limit':'Only bounded_snow and completed_snow_fixture execution receipts are PASS; the original other runs retain failures.'})
files = [{'path':p.relative_to(O).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size,'role':'native diagnostic capture' if p.suffix=='.png' else 'diagnostic source/evidence'} for p in sorted(O.rglob('*')) if p.is_file() and p.name!='manifest.json']
payload = ''.join(f"{x['path']}\t{x['sha256']}\t{x['bytes']}\n" for x in files).encode('utf-8')
write(O/'manifest.json',{'schema':'reef.root_picture_action_packet/1','source_revision':REV,'files':files,'payload_hash_definition':'UTF-8 sorted path TAB SHA256 TAB bytes LF, excluding manifest','packet_payload_sha256':hashlib.sha256(payload).hexdigest(),'delivery':'LOCAL_STAGING_NOT_DELIVERED','acceptance':'ZERO_ACCEPTED_REMOVALS'})
print(json.dumps({'output':str(O),'payload_files':len(files),'native_captures':len(captures),'native_viewed':len(viewed),'observations':len(observations),'review_sha256':sha(O/'review.json'),'manifest_sha256':sha(O/'manifest.json'),'payload_sha256':hashlib.sha256(payload).hexdigest(),'maximum_file_bytes':max(x['bytes'] for x in files)}))
