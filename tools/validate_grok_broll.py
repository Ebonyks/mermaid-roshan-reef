"""Fail-closed validation of the paired B-roll PLANNING package.

This does not replace audit_imagine_handoff or establish visual acceptance.
"""
import argparse
import hashlib
import json
from pathlib import Path

DEFAULT = Path(__file__).resolve().parents[1]/'assets_src/cinematics/grok_broll_2026-09-19'
INHERITED = ('event_id','location_id','exact_cast','cast_instances','exact_prop_counts','room_state','end_room_state','depends_on','depends_on_events','game_prerequisite','end_state')

def read(path):return json.loads(path.read_bytes())
def sha(data):return hashlib.sha256(data).hexdigest()

def validate_plan(plan, parent, prompt):
    errors=[]
    def check(ok, message):
        if not ok:errors.append(message)
    check(plan.get('schema')=='reef.grok.broll-plan.v1','planning schema')
    check(plan.get('shot_id')==parent['shot_id']+'-B01','exact A/B pairing')
    check(plan.get('parent_shot_id')==parent['shot_id'],'parent shot')
    for key in INHERITED:check(plan.get(key)==parent.get(key),'inherited '+key)
    check(plan.get('GENERATION_READY') is False and plan.get('DELIVERY_ACCEPTED') is False,'no inferred acceptance')
    check(plan.get('inherited_hold') is bool(parent.get('hold')),'parent HOLD preserved')
    lineage=plan.get('attempt_lineage',{})
    check(lineage.get('reset_allowed') is False,'no attempt reset')
    check(lineage.get('attempts_used')==parent.get('attempts_used',0),'attempts consumed')
    check(lineage.get('attempt_cap')==parent.get('attempt_cap',3),'attempt cap')
    check(lineage.get('broll_attempts_generated')==0,'no invented B output')
    check(set(parent.get('blocking_findings',[])) <= set(plan.get('blockers',[])),'parent blockers preserved')
    camera=plan.get('camera',{})
    check(camera.get('verb')=='locked' and camera.get('move_count')==0,'one locked camera')
    check(camera.get('mirror_allowed') is False,'mirror forbidden')
    check(camera.get('digital_crop_is_new_angle') is False,'crop not angle')
    check(camera.get('unseen_reverse_wall_allowed') is False,'no invented reverse wall')
    check(camera.get('same_action_hemisphere') is True,'same action hemisphere')
    check(camera.get('measured') is False,'proposed camera not measured')
    check(25 <= camera.get('proposed_offset_degrees',0) <= 50,'meaningful proposed offset')
    check(plan.get('duration_seconds')==4 and plan.get('fps_plan')==24 and plan.get('frame_count_plan')==96,'duration/fps/frame plan')
    check(plan.get('size')==[1280,720] and plan.get('aspect')=='16:9','landscape target')
    check([b.get('frames_half_open') for b in plan.get('beats',[])]==[[0,18],[18,78],[78,96]],'complete nonoverlapping frame spans')
    binds=plan.get('suggested_bindings',[])
    check(2<=len(binds)<=4,'two to four bindings')
    check([b.get('id') for b in binds]==[f'IMAGE_{i+1}' for i in range(len(binds))],'sequential unique bindings')
    if binds:
        check(binds[0].get('path') is None and binds[0].get('sha256') is None and binds[0].get('owner_approved') is False,'no approved IMAGE_1 invented')
    board=plan.get('board',{})
    check(board.get('used_as_generation_pixels') is False and board.get('used_as_delivery_pixels') is False,'board not pixels')
    editorial=plan.get('editorial',{})
    check(editorial.get('replace_span_not_append_repeat') is True,'no repeated event')
    check(editorial.get('mapping_basis')=='PROPOSED_PHASE_MARKERS_NOT_MEASURED_FOOTAGE_TIMECODES','no fake measured timecodes')
    check(len(editorial.get('match_checks',[]))>=6,'splice match checklist')
    check(plan.get('prompt_sha256')==sha(prompt),'prompt fingerprint')
    text=prompt.decode('utf-8')
    check(text.rstrip().splitlines()[-1].startswith('Sound:'),'final Sound line')
    check('end: '+parent['end_state'].rstrip('.')+'.' in text,'exact endpoint prompt')
    check('IMAGE_1' in text and 'IMAGE_2' in text,'input roles in prompt')
    check('locked' in text and 'no mirrored layout' in text,'prompt camera/negative controls')
    if parent['shot_id'] in ('SHOT-BUNNY-JUMP','SHOT-BUNNY-LAND'):
        lock=plan.get('continuous_endpoint_lock',{})
        check(lock.get('required') is True and lock.get('accepted_endpoint_sha256') is None,'continuous endpoint remains gated')
    return errors

def validate(packet, require_ready=False):
    errors=[];pairs=read(packet/'PAIRS.json')['pairs'];registry=read(packet/'REFERENCES.json')['references']
    check=lambda ok,msg:errors.append(msg) if not ok else None
    check(len(pairs)==36,'36 pairs required')
    check(len({p['a'] for p in pairs})==36 and len({p['b'] for p in pairs})==36,'one-to-one pairing')
    check(len(registry)==41,'41 supplied references')
    qc=read(packet/'BOARD_QC.json');provenance=read(packet/'GENERATION_PROVENANCE.json')
    selected={p['id']:p for p in provenance if p['selected_concept']}
    check({k:v['version'] for k,v in selected.items()}==qc['selected_versions'],'selected board QC/provenance versions')
    check(len(selected)==10,'10 selected boards')
    check(len({(p['board'],p['row']) for p in pairs})==36,'one board row per shot')
    for p in pairs:
        folder=packet/'shots'/p['b'];plan=read(folder/'PLAN.json')
        parent_file=packet/'source_plans'/p['a']/'CARD.json';parent=read(parent_file)
        check(plan['parent_card_sha256']==sha(parent_file.read_bytes()),p['b']+' parent hash')
        errors.extend(p['b']+': '+e for e in validate_plan(plan,parent,(folder/'PROMPT.txt').read_bytes()))
        check(set(plan['preparation_references']) <= set(registry),p['b']+' unresolved source')
        check(plan['board']['path']==p['board'] and plan['board']['row_one_based']==p['row'],p['b']+' board mapping')
        for name in ('SHOT_CARD.txt','FIRST_FRAME_BRIEF.txt'):check((folder/name).is_file(),p['b']+' missing '+name)
    if require_ready:errors.append('All 36 are planning candidates: complete owner-approved IMAGE_1, access and canonical execution gates remain required.')
    return {'pairs':len(pairs),'boards':len(selected),'illustrated_beats':len(pairs)*3,'ready':0,'errors':errors,'result':'FAIL' if errors else 'PASS_PLANNING_ONLY'}

def main():
    p=argparse.ArgumentParser();p.add_argument('packet',nargs='?',type=Path,default=DEFAULT);p.add_argument('--require-ready',action='store_true');a=p.parse_args()
    result=validate(a.packet,a.require_ready);print(json.dumps(result,indent=2));raise SystemExit(bool(result['errors']))

if __name__=='__main__':main()
