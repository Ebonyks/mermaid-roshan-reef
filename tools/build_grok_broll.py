"""Build the owner-commissioned B-roll planning archive, never approved frames.

The media staging root is private-only. Public output contains no image bytes.
Inputs are pinned V2 plans and previously verified local source copies.
"""
import argparse
import hashlib
import html
import json
import shutil
from pathlib import Path

PACKET = 'assets_src/cinematics/grok_broll_2026-09-19'
PARENT = '0b26557f9500983f7ba2eb670df072dffd352779'
PARENT_REPO = 'Ebonyks/mermaid-roshan-reef'
MEDIA_REPO = 'Ebonyks/mermaid-roshan-grok-videos'
SOURCE_MEDIA = '34ca6928d4c7c3fe107650d3202408d00232c288'

# parent suffix, board, row, yaw proposal, elevation, framing, physical viewpoint,
# cut-in event, cut-out event. Angles are proposals, never measured room geometry.
DIRECTIONS = [
 ('ARRIVAL-TOUCHDOWN','ARRIVAL',1,35,8,'medium-wide','Low front-left quarter of the established landing patch; lake-side mountain remains behind the nose. Nose and travel retain A-roll screen direction.','descent reaches grass-contact phase','plane settles with both passengers still seated'),
 ('BATH-SINK','BATH',1,30,5,'medium-close','From tub-side toward central shell sink, grazing the front rim; mirror and left tub edge stay visible.','bristles first compress on sink grime','one clean patch persists as brush eases off'),
 ('BATH-TUB','BATH',2,35,30,'medium','Elevated front-left three-quarter across horizontal tub rim toward the clean sink edge on right.','brush begins a horizontal contact stroke','clean stripe remains; water still full'),
 ('BATH-DRAIN','BATH',3,25,45,'medium-close','High oblique from the same front hemisphere into tub; include original outlet and clean sink edge.','bare fingers engage original drain','water visibly reaches the drained level; never hide the falling waterline'),
 ('BATH-TOILET','BATH',4,30,8,'medium-close','Low sink-side three-quarter on right pink toilet; clean sink edge and right wall anchor retained.','bristles contact toilet grime','same pink fixture clean and brush withdraws'),
 ('POOL-SKIM','POOL',1,35,4,'medium','Low waterline diagonal along front coping; waterfall left and dry plugged seahorse right remain recognizable.','net crosses beneath litter, not floating toys','litter lifted with flower and star toys still afloat'),
 ('POOL-FALL-1','POOL',2,30,10,'medium','Front-left oblique toward waterfall lane one, shell seat and neighboring dirty lane remain in view.','brush contacts lane one','lane one clear; lanes two and three still dirty'),
 ('POOL-FALL-2','POOL',3,40,25,'medium','Elevated front coping diagonal toward lane two with lane one and seahorse as depth anchors.','brush contacts lane two while lane one remains clear','two lanes clear; lane three still dirty'),
 ('POOL-FALL-3','POOL',4,30,5,'medium-close','Low centre-coping oblique to last waterfall lane; preserve both completed lanes at the edge.','bristles begin final lane contact','three clean lanes; seahorse still plugged and dry'),
 ('POOL-PULL','POOL',5,35,12,'close','Right-front quarter of purple seahorse mouth; coral pedestal and rear towel shelf fix its position.','bare hand grips the lodged pink obstruction','obstruction visibly held clear; nozzle remains dry'),
 ('CRAFT-PICK-1','CRAFT_PICK',1,35,6,'medium-close','Low front-left quarter along LEFT curved counter, with the SMALL stocked rear table behind.','hand closes on the collectible brush bundle','bundle securely lifted; no duplicate loose bundle'),
 ('CRAFT-PICK-2','CRAFT_PICK',2,30,35,'medium-close','Elevated diagonal into LEFT counter; nearest column and rear table maintain depth.','hand grips the same pink bottle','pink bottle held clear; previously collected bundle stays collected'),
 ('CRAFT-PICK-3','CRAFT_PICK',3,35,8,'medium-close','Low front-right quarter along RIGHT curved counter, looking toward rear stocked table.','hand grips blue bottle','blue bottle lifted; first two collectible groups absent'),
 ('CRAFT-PICK-4','CRAFT_PICK',4,40,30,'over-shoulder','Over Roshan shoulder from front-right aisle toward cups on same counter; retain table edge and column.','fingers surround the existing cup group','cups secured as one group; no extra hand or duplicated cups'),
 ('CRAFT-SCRUB-1','CRAFT_CLEAN',1,35,6,'medium','Left-front low diagonal along curved counter; rear table and right counter still dirty.','bristles compress on left-counter grime','left clean; rear/right grime remains'),
 ('CRAFT-SCRUB-2','CRAFT_CLEAN',2,30,25,'medium','Elevated centre-aisle-left quarter into SMALL low STOCKED rear worktable; pinboard fixed behind it.','bristles touch tabletop BETWEEN retained supplies','rear tabletop clean without relocating furniture'),
 ('CRAFT-SCRUB-3','CRAFT_CLEAN',3,35,8,'medium','Right-front counter-height oblique along curved counter, clean rear/left visible in depth.','brush contacts right-counter grime','all three surfaces clean, same stocked table unlocked'),
 ('CRAFT-CUSTOMIZE','CRAFT_CLEAN',4,35,30,'over-shoulder','Over Roshan shoulder at the SMALL rear stocked table looking down at its authored colour choice.','finger touches the authored colour target','one chosen colour visibly selected, not a new symbol or chest'),
 ('EAGLE-FREE','EAGLE',1,30,8,'medium','Low front-left playroom oblique retaining shell couch/cubby and BOTH pinning-bunny positions.','contact clears first pinning dust bunny','second contact clears second bunny, Eagle freed'),
 ('EAGLE-WING','EAGLE',2,35,25,'two-shot','Higher three-quarter from same hemisphere, frame Roshan with original-book Eagle and rear cubby.','Eagle begins its single wingbeat','wings settle; neither restraining bunny returns'),
 ('BUNNY-SOAP','BOSS',1,35,12,'ensemble-wide','Front-left oblique of octagonal rug, with two-window stone attic, left pillar and far chest anchoring depth.','four helpers begin coordinated contact on intact giant','wet suds hide BOTH ears and body, tiny friend still hidden'),
 ('BUNNY-JUMP','BOSS',2,35,5,'ensemble-medium-wide','Lower front-left quarter, SAME action hemisphere, with complete foam mound and all four helpers readable.','foam parts while old casing starts collapsing','small friend airborne, giant casing collapsed into low dust'),
 ('BUNNY-LAND','BOSS',3,35,12,'ensemble-medium','Rug-level eye-line three-quarter from same hemisphere; ground contact area stays completely visible.','small friend continues descending from accepted JUMP endpoint','paws grounded, dust thinned, no intact giant anywhere'),
 ('TEAM-PAPER','TEAM',1,35,5,'ensemble-medium','Floor-height oblique from front-left along red runner, one small arch base and gold pillar in view.','five friends gather same paper cluster','paper collected; web and wall stain remain'),
 ('TEAM-WEB','TEAM',2,35,28,'ensemble-medium','Elevated oblique toward SAME gold pillar and selected web, helpers staggered in depth.','held duster contacts selected web','web gathered; paper absent and wall stain remains'),
 ('TEAM-WALL','TEAM',3,35,12,'ensemble-medium','Eye-level quarter view across lavender wall stain, nearest gold column edge fixes location.','sponge contacts stain with coordinated team support','stain gone; previous paper/web stay cleared'),
 ('TEAM-FINISH','TEAM',4,35,30,'ensemble-wide','High front-left three-quarter along runner; show FOUR small LEFT arches and ONE large draped RIGHT royal arch.','group settles into their earned clean hall','all five calm, one restrained sparkle, same architecture'),
 ('C2-01','LAWN_A',1,35,12,'ensemble-medium','Table front-left quarter on middle lawn patch; mountains and right lake maintain horizon.','friends finish gathering in party hats','four friends settled, six-tier cake and UNLIT candle intact'),
 ('C2-02','LAWN_A',2,35,8,'close','Low tabletop quarter along rocket-to-candle axis; keep rocket contact and wick simultaneously legible.','Roshan taps the finished cream/red rocket','single candle lights; rocket and cake remain still'),
 ('C2-03','LAWN_A',3,35,8,'two-shot','Low side-front quarter of lawn approach, SAME side of party/royals axis as A; King leads Prince.','King crosses established lawn edge','both royals stop facing party; do not repeat entrance'),
 ('C2-04','LAWN_A',4,35,12,'three-shot','Medium three-quarter across encounter axis; Roshan offered hand, King between her and Prince.','Roshan offers hand without touching King','King blocks Prince; no handshake or reconciliation'),
 ('C2-05','LAWN_A',5,35,3,'close','Low oblique of Ember King red scaly foot and grass, cloak hem anchors identity.','foot descends to grass','one soft warm puff settles; no damage or repeated stomp'),
 ('C2-06','LAWN_B',1,35,12,'ensemble-medium','Eye-level table-left oblique under ALREADY completed rainbow shelter, same intact cake nearby.','Roshan turns toward protected friends','four friends safe after three successful gameplay rounds'),
 ('C2-07','LAWN_B',2,35,10,'close','Tight tabletop oblique with EMBER KING red claw and purple cuff, candle holder plus cake rim visible.','red claw grips ONLY the single candle','candle held clear, socket empty, whole cake stays'),
 ('C2-08','LAWN_B',3,35,12,'two-shot','Medium side-front quarter on royal exit axis; King red dragon carries candle, slim Prince trails.','Prince makes the sorry backward glance','both royals exit in same direction, no candle on cake'),
 ('C2-09','LAWN_B',4,35,18,'ensemble-medium','Shoulder-height from Roshan side, empty holder foreground and comforting friends in layered depth.','Roshan notices empty candle holder','four friends together; candle stays absent, cake intact'),
]

def sha(data):
    return hashlib.sha256(data).hexdigest()

def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    data = json.dumps(value, indent=2, ensure_ascii=False) + '\n'
    path.write_bytes(data.encode('utf-8'))

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(value.encode('utf-8'))

def dimensions(path):
    from PIL import Image
    with Image.open(path) as im:
        return list(im.size)

def build(root, source_cache, generations, media_stage):
    public = root / PACKET
    private = media_stage / PACKET
    public.mkdir(parents=True, exist_ok=True)
    v2 = root / 'design/cinematics/v2'
    registry = json.loads((v2/'canon/REFERENCES.json').read_bytes())['references']
    for path in (v2/'canon').glob('*.json'):
        write(public/'source_canon'/path.name, path.read_text(encoding='utf-8'))
    latest = {}
    for rec in generations:
        if rec['version'] > latest.get(rec['id'], {}).get('version', 0):
            latest[rec['id']] = rec
    required_boards = {x[1] for x in DIRECTIONS}
    if set(latest) != required_boards:
        raise ValueError('Missing or unexpected storyboard family')
    # No inferred owner approval; charts/storyboards are never execution bindings.
    pairs = []
    grid = []
    license_rows = []
    for suffix, group, row, yaw, elevation, framing, viewpoint, cut_in, cut_out in DIRECTIONS:
        aid = 'SHOT-' + suffix
        bid = aid + '-B01'
        parent_path = v2/'shots'/aid/'CARD.json'
        parent_bytes = parent_path.read_bytes()
        a = json.loads(parent_bytes)
        write(public/'source_plans'/aid/'CARD.json', parent_bytes.decode('utf-8'))
        prompt = (
            f"{a['action'].rstrip('.').lower()} from the approved alternate opening in IMAGE_1.\n"
            f"locked {framing} camera; {viewpoint.lower()}\n"
            f"0.0-0.75s: begin in the same pre-action state; {cut_in.lower()}.\n"
            f"0.75-3.25s: carry out that single action with visible physical cause; {cut_out.lower()}.\n"
            "3.25-4.0s: settle only where the action is finished; never freeze unfinished motion.\n"
            "keep room geometry, identities, tool orientation, unaffected fixtures and prior completed work fixed. "
            "no mirrored layout, new wall, HUD, text, extra characters, identity drift or repeated payoff. "
            "preserve identity from IMAGE_2 and any named object/grade bindings.\n"
            f"end: {a['end_state'].rstrip('.')}.\n"
            "Sound: synchronized gentle contact foley and matching room tone; no speech, music or protected voice synthesis.\n"
        )
        if suffix == 'BUNNY-JUMP':
            prompt = prompt.replace('3.25-4.0s: settle only where the action is finished; never freeze unfinished motion.',
                '3.25-4.0s: continue the airborne trajectory and falling dust; no settle or freeze before LAND.')
        inherited = ['event_id','location_id','exact_cast','cast_instances','exact_prop_counts','room_state','end_room_state','depends_on','depends_on_events','game_prerequisite','end_state']
        plan = {key: a.get(key) for key in inherited}
        board_path = f"boards/{group}_v{latest[group]['version']}.png"
        plan.update({
            'schema':'reef.grok.broll-plan.v1','shot_id':bid,'parent_shot_id':aid,
            'parent_commit':PARENT,'parent_card_sha256':sha(parent_bytes),
            'parent_url':f'https://github.com/{PARENT_REPO}/blob/{PARENT}/design/cinematics/v2/shots/{aid}/CARD.json',
            'intent':'Alternate coverage of the SAME action, not a new event or second completion.',
            'status':'DRAFT_REQUIRES_EXACT_OWNER_OPENING_APPROVAL','GENERATION_READY':False,'DELIVERY_ACCEPTED':False,
            'inherited_hold':bool(a.get('hold')),'attempt_lineage':{'parent_shot_id':aid,'attempts_used':a.get('attempts_used',0),'attempt_cap':a.get('attempt_cap',3),'reset_allowed':False,'broll_attempts_generated':0},
            'blockers':list(a.get('blocking_findings',[]))+['NEW_CAMERA_LAYOUT_AND_COMPLETE_OPENING_REVIEW','GROK_ACCESS_ACK','PAIRED_ACTION_PHASE_MATCH'],
            'camera':{'verb':'locked','move_count':0,'framing':framing,'viewpoint':viewpoint,'proposed_offset_degrees':yaw,'proposed_elevation_degrees':elevation,'measured':False,'same_action_hemisphere':True,'mirror_allowed':False,'digital_crop_is_new_angle':False,'unseen_reverse_wall_allowed':False},
            'duration_seconds':4,'fps_plan':24,'frame_count_plan':96,'size':[1280,720],'aspect':'16:9','output_disposition':'motion_reference_only',
            'beats':[{'frames_half_open':[0,18],'seconds':[0,0.75],'phase':'start','visible':a['before']}, {'frames_half_open':[18,78],'seconds':[0.75,3.25],'phase':'contact_action','visible':a['action']}, {'frames_half_open':[78,96],'seconds':[3.25,4],'phase':'endpoint','visible':a['after']}],
            'editorial':{'mapping_basis':'PROPOSED_PHASE_MARKERS_NOT_MEASURED_FOOTAGE_TIMECODES','cut_in':cut_in,'cut_out':cut_out,'suggested_b_use_seconds':[0.8,2.6] if suffix not in ('BATH-DRAIN','BUNNY-JUMP','BUNNY-LAND','C2-07') else [0.0,4.0], 'preserve_full_causal_action':suffix in ('BATH-DRAIN','EAGLE-FREE','BUNNY-JUMP','BUNNY-LAND','C2-07'), 'replace_span_not_append_repeat':True,'match_checks':['same motion phase and travel direction','same hand/tool and contact point','same dirt/water/prop state','same cast count and costume','same camera hemisphere and eyelines','no replay of contact or payoff'], 'audio':'Use one continuous room-tone bed; carry foley across cut, never double the impact. Reuse authorized in-game voices only later in edit; generate no voice here.'},
            'preparation_references':[r['reference_id'] for r in a.get('preparation_references',[]) if r.get('reference_id') in registry],
            'suggested_bindings':[{'id':'IMAGE_1','role':'approved_clean_first_frame','path':None,'sha256':None,'owner_approved':False}]+[{'id':r['id'],'role':r['role'],'reference_id':r.get('reference_id'),'sha256':r.get('sha256'),'requires_binding_review':True} for r in a.get('binds',[])[1:]],
            'board':{'path':board_path,'row_one_based':row,'columns':{'1':'start','2':'contact/action','3':'endpoint'},'used_as_generation_pixels':False,'used_as_delivery_pixels':False,'approval':'CANDIDATE_COMPOSITION_ONLY_SEE_BOARD_QC'},
            'prompt_sha256':sha(prompt.encode()),'source_board_path':f'historical_boards/{aid}.jpg',
            'continuous_endpoint_lock':{'required':suffix in ('BUNNY-JUMP','BUNNY-LAND'),'previous_b_shot':{'BUNNY-JUMP':'SHOT-BUNNY-SOAP-B01','BUNNY-LAND':'SHOT-BUNNY-JUMP-B01'}.get(suffix),'accepted_endpoint_sha256':None,'alternate_angle_opening_sha256':None,'note':'Different angles need two separately approved full frames of the SAME world-state/trajectory phase. Do not reuse A pixels or blend endpoints.'}
        })
        dump(public/'shots'/bid/'PLAN.json',plan)
        write(public/'shots'/bid/'PROMPT.txt',prompt)
        brief = f"{bid} — complete alternate first-frame brief\nPaired A shot: {aid}\n\nRedraw the full scene from: {viewpoint}\nFraming: {framing}; proposed yaw offset {yaw} degrees, elevation {elevation} degrees. Angles are planning proposals, not measured geometry.\n\nStart world state: {json.dumps(a['room_state'],ensure_ascii=False)}\nCast instances: {json.dumps(a['cast_instances'],ensure_ascii=False)}\nExact prop counts: {json.dumps(a['exact_prop_counts'],ensure_ascii=False)}\nAction to prepare: {a['action']}\nEnd state must remain: {a['end_state']}\n\nUse actual room, identity and prop sources in REFERENCES.json; current clean source does not authorize a dirty or changed-angle opening. Show recognizable near and far anchors, maintain fixture adjacency, do not invent the unseen rear wall. A close crop/flip is NOT new perspective. Maintain one continuous mermaid tail, child/adult scale and correct handle-to-bristle contact.\n\nDeliver one native complete UI-free candidate and exact filename/hash for owner approval. No storyboard or gameplay pixels may be bound as IMAGE_1. No automatic motion generation or acceptance. Inherit A HOLD and attempt cap; angle naming never bypasses them.\n"
        write(public/'shots'/bid/'FIRST_FRAME_BRIEF.txt',brief)
        slots='\n'.join(f"{s['id']}: {s.get('reference_id') or 'MISSING — complete owner-approved alternate opening required'}\njob: {s['role']}" for s in plan['suggested_bindings'])
        card=f"Imagine shot card v1 — planning copy, NOT executable until canonical packet is compiled and audited\nmovie_id: MERMAID-ROSHAN-BROLL-20260919\nshot_id: {bid}\nstatus: DRAFT\nduration: 4 seconds\naspect: 16:9\nsize: 1280x720\nmode: image-to-video\noutput_disposition: motion_reference_only\n\n{slots}\n\nstart_frame: IMAGE_1\ncamera: locked\nmust_move: {a['action']}\nmust_not_move: {', '.join(a['must_not_move'])}\nend_state: {a['end_state']}\nnegative_constraints: no HUD/text, no extra fixtures/cast, no mirror, no unapproved reverse wall, no repeated story completion\nsound_intent: synchronized contact foley and room tone, no synthesized family voice\n\nARCHIVE_COMPLETE: see immutable publication receipt\nGENERATION_READY: false\nDELIVERY_ACCEPTED: false\n\nPaste-ready draft prompt (only after readiness):\n{prompt}\nArchive: PLAN.json, FIRST_FRAME_BRIEF.txt, ../../REFERENCES.json, ../../BOARD_QC.json\n"
        write(public/'shots'/bid/'SHOT_CARD.txt',card)
        pairs.append({'a':aid,'b':bid,'scene':a['location_id'],'board':board_path,'row':row,'hold':plan['inherited_hold'],'camera':viewpoint,'cut_in':cut_in,'cut_out':cut_out,'plan':f'shots/{bid}/PLAN.json'})
        grid.append(f'<article id="{bid}"><h2>{bid}</h2><p>{html.escape(viewpoint)}</p><p>Board row {row}: start → contact → end. CONCEPT ONLY; see QC.</p><img src="{board_path}" alt="{group} concept board"><p>{html.escape(cut_in)} → {html.escape(cut_out)}</p><a href="shots/{bid}/SHOT_CARD.txt">Shot card</a> · <a href="shots/{bid}/FIRST_FRAME_BRIEF.txt">Opening brief</a></article>')
    dump(public/'PAIRS.json',{'schema':'reef.grok.broll-pairs.v1','parent_commit':PARENT,'count':len(pairs),'pairs':pairs})
    dump(public/'REFERENCES.json',{'schema':'reef.grok.broll-reference-registry.v1','references':{k:{**v,'packet_path':'references/'+v['path']} for k,v in registry.items()}})
    # Freeze the source-only camera caveats; B-roll does not silently overrule them.
    dump(public/'QUEUE.json',{'mode':'PREPARE_THEN_OWNER_REVIEW','auto_generate_motion':False,'first_batch_recommendation':['SHOT-BATH-TUB-B01','SHOT-CRAFT-PICK-1-B01','SHOT-CRAFT-SCRUB-2-B01','SHOT-EAGLE-FREE-B01','SHOT-BUNNY-SOAP-B01','SHOT-TEAM-FINISH-B01'],'all_jobs':[p['b'] for p in pairs],'inherits_parent_holds':True,'first_frame_approval':'Show each full-frame candidate individually; exact filename plus SHA-256, no blanket inferred approval.'})
    dump(public/'RESHOOT_RETURN_TEMPLATE.json',{'shot_id':None,'parent_shot_id':None,'attempt':None,'request_sha256':None,'input_bindings':[],'prompt_sha256':None,'immutable_native_file_url':None,'sha256':None,'duration_seconds':None,'fps':None,'dimensions':None,'camera_setup_id':None,'motion_phase_markers':{'first_contact_frame':None,'irreversible_change_frame':None,'end_state_frame':None},'a_b_match':{'a_clip_sha256':None,'a_cut_frame':None,'b_cut_frame':None,'state_and_direction_review':None},'defects':[{'frame_start':None,'frame_end':None,'observed':None,'required_reconstruction':None}],'owner_opening_approval_receipt':None,'GENERATION_READY':False,'DELIVERY_ACCEPTED':False})
    write(public/'index.html','<!doctype html><meta charset="utf-8"><title>Mermaid Roshan — alternate coverage review</title><style>body{max-width:1200px;margin:auto;padding:24px;background:#171326;color:#f7efff;font:17px system-ui}a{color:#8ee5df}article{margin:30px 0;padding:20px;border:1px solid #746989;border-radius:12px}img{width:100%;height:auto}</style><h1>B-roll: same events, new viewpoints</h1><p>Private visual archive viewer. Every image is a candidate board, never IMAGE_1. Exact state, parent HOLD and owner approval remain binding. Public copy needs PUBLICATION.json media location.</p>'+''.join(grid))
    dump(public/'BOARD_LAYOUT.json',{'columns':3,'rows':{k:max(p['row'] for p in pairs if p['board'].split('/')[1].startswith(k+'_v')) for k in required_boards},'mapping':'Each row corresponds to the paired shot; columns 1/2/3 are start/contact/endpoint. This is an illustrative beat board, not a strip of accepted video frames.'})
    # Copy public planning into private archive, then add exact source bytes.
    for p in public.rglob('*'):
        if p.is_file():
            target=private/p.relative_to(public);target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,target)
    for ref in registry.values():
        src=source_cache/ref['path']; data=src.read_bytes()
        if sha(data)!=ref['sha256']:raise ValueError('Source hash mismatch '+str(src))
        dest=private/'references'/ref['path'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dest)
    for pair in pairs:
        src=source_cache/'boards'/(pair['a']+'.jpg');dest=private/'historical_boards'/src.name
        dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dest)
    provenance=[]
    for rec in generations:
        dst=private/'boards'/f"{rec['id']}_v{rec['version']}.png";dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(rec['path'],dst)
        inputs=[]
        for raw in rec['refs']:
            rp=Path(raw)
            if rp.parent.name=='media': rel='references/media/'+rp.name
            elif rp.name in ('lawn.jpg','daddy.jpg'):
                rel='board_inputs/'+rp.name;target=private/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(rp,target)
            else:
                match=next((g for g in generations if Path(g['path'])==rp),None)
                if match is None:raise ValueError('Unmapped board input '+raw)
                rel=f"boards/{match['id']}_v{match['version']}.png"
            inputs.append({'path':rel,'sha256':sha(rp.read_bytes()),'role':'board_edit_target_only' if rel.startswith('boards/') else 'identity_or_layout_for_board_only'})
        rr={'id':rec['id'],'version':rec['version'],'path':dst.relative_to(private).as_posix(),'sha256':sha(dst.read_bytes()),'dimensions':dimensions(dst),'method':'built_in_image_gen','prompt':rec['prompt'],'prompt_sha256':sha(rec['prompt'].encode()),'inputs':inputs,'selected_concept':latest[rec['id']]['version']==rec['version'],'used_as_generation_pixels':False,'used_as_delivery_pixels':False,'owner_approved':False}
        provenance.append(rr)
        license_rows.append(f"| `{rr['path']}` | OpenAI built-in image generation for this owner-commissioned B-roll storyboard, 2026-09-19 | Project-generated concept; protected originals unchanged | Exact prompt/input hashes in GENERATION_PROVENANCE.json; {'selected candidate' if rr['selected_concept'] else 'superseded/rejected review evidence'}, never accepted first frame |")
    dump(public/'GENERATION_PROVENANCE.json',provenance)
    dump(private/'GENERATION_PROVENANCE.json',provenance)
    licenses='# B-roll packet asset provenance\n\nAll images are private continuity/review material, not delivered frames. No third-party asset licence is invented. Source attribution is inherited verbatim from REFERENCES.json; owner-provided book/family identities remain protected.\n\n| File | Source | Rights/provenance | Modifications and scope |\n|---|---|---|---|\n'+'\n'.join(license_rows)+'\n'
    for key,ref in registry.items():
        licenses+=f"| `references/{ref['path']}` | {ref['remote_url']} | {ref['license_provenance']} | Byte-identical copy; {key}; source reference only |\n"
    for pair in pairs:
        licenses+=f"| `historical_boards/{pair['a']}.jpg` | {SOURCE_MEDIA}:grok_builder_2026-09-14/boards_v4/{pair['a']}.jpg | Inherited project-authored board | Byte-identical historical illustration, not current state authority |\n"
    licenses+='| `board_inputs/daddy.jpg` | `references/media/2eda6f76760b8598.png` | Inherited project-owned character authority | Whole-image diagnostic thumbnail (ffmpeg scale=700:-1), used for board creation only; original preserved |\n| `board_inputs/lawn.jpg` | `references/media/017532ae864e534d.png` | Inherited project-owned panorama authority | Whole-image diagnostic thumbnail (ffmpeg scale=1500:-1), used for board creation only; original preserved |\n'
    write(public/'ASSET_LICENSES.md',licenses);write(private/'ASSET_LICENSES.md',licenses)
    write(public/'.gitattributes','*.json text eol=lf\n*.txt text eol=lf\n*.md text eol=lf\n*.html text eol=lf\n')
    print(json.dumps({'pairs':len(pairs),'boards':len(required_boards),'historical_boards':len(pairs),'actual_references':len(registry),'generation_attempts':len(provenance),'public_packet':str(public),'private_staging':str(private)}))

def main():
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--source-cache',type=Path,required=True);p.add_argument('--generation-records',type=Path,required=True);p.add_argument('--private-stage',type=Path,required=True)
    a=p.parse_args();build(a.root,a.source_cache,json.loads(a.generation_records.read_bytes()),a.private_stage)

if __name__=='__main__':main()
