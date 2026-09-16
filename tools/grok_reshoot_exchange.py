"""Append-only Grok request/return/QC exchange. Never invokes a model or approves art.

Run from repository root, or copy this tool beside an extracted builder packet.
Untrusted return metadata is data only. Local media must already be in inbox/.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlparse

SCHEMA = 'reef.grok-reshoot.v1'
ID = re.compile(r'[A-Z0-9][A-Z0-9_-]{0,100}\Z')
HASH = re.compile(r'[a-f0-9]{64}\Z')

def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def blob_hash(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda:stream.read(1048576),b''):h.update(block)
    return h.hexdigest()

def fingerprint(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()

def require(condition,message):
    if not condition:raise ValueError(message)

def safe(root,relative):
    require(isinstance(relative,str) and relative and not Path(relative).is_absolute(),'Relative path required')
    require('\\' not in relative and ':' not in relative,'Portable relative path required')
    p=(root/relative).resolve()
    require(p.is_relative_to(root.resolve()),'Path escapes exchange root')
    return p

def immutable(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    payload=json.dumps(value,indent=2,ensure_ascii=False)+'\n'
    # Exclusive creation prevents collisions/overwriting attempts, including concurrent writers.
    with path.open('x',encoding='utf-8',newline='\n') as out:out.write(payload)

def contract(packet,shot_id):
    require(bool(ID.fullmatch(shot_id)),'Invalid shot ID')
    db=load(packet/'DATABASE.json')
    shots={s['id']:s for s in db['shots']}
    require(shot_id in shots,'Unknown shot ID')
    shot=shots[shot_id]
    events={e['id']:e for e in db['events']}
    event=events[shot['event_id']]
    # Dependency shot edits must stale successor requests, not merely reference-library changes.
    pending=list(shot.get('depends_on',[])); ancestor_ids=set()
    while pending:
        dep=pending.pop()
        require(dep in shots,'Unresolved ancestor shot')
        if dep not in ancestor_ids:
            ancestor_ids.add(dep);pending.extend(shots[dep].get('depends_on',[]))
    dependencies=[shots[s] for s in sorted(ancestor_ids)]
    relevant_shots=[shot]+dependencies
    event_ids={s['event_id'] for s in relevant_shots}
    pending=[x for s in relevant_shots for x in s.get('depends_on_events',[])]+list(event_ids)
    traversed=set()
    while pending:
        key=pending.pop();require(key in events,'Unresolved ancestor event')
        if key not in traversed:
            traversed.add(key);pending.extend(events[key].get('depends_on',[]))
    dependency_events=[events[k] for k in sorted(traversed) if k!=shot['event_id']]
    entity_ids=set()
    ref_ids=set()
    for s in relevant_shots:
        entity_ids.update(s.get('character_ids',[])+s.get('scene_cohort_ids',[])+[s['location_id']])
        ref_ids.update(s.get('reference_pool_ids',[]))
    for e in [event]+dependency_events:
        entity_ids.update(e.get('character_ids',[])+e.get('prop_ids',[]))
        if e.get('location_id'):entity_ids.add(e['location_id'])
    entities=[e for e in db['entities'] if e['id'] in entity_ids]
    require(entity_ids=={e['id'] for e in entities},'Unresolved dependency entity')
    for e in entities:ref_ids.update(e.get('reference_ids',[]))
    refs=[r for r in db['references'] if r['id'] in ref_ids]
    require(ref_ids=={r['id'] for r in refs},'Unresolved dependency reference')
    direction=load(packet/'CHARACTER_DIRECTION.json') if (packet/'CHARACTER_DIRECTION.json').exists() else None
    job_source=load(packet/'JOBS.json') if (packet/'JOBS.json').exists() else {}
    variants=[v for v in job_source.get('chapter2_variants',db.get('job_variants',[])) if v.get('event_id') in traversed]
    job_ids={v['base_job_id'] for v in variants}
    job_ids.update(s['job_id'] for s in relevant_shots if s.get('job_id'))
    jobs=[j for j in job_source.get('jobs',db.get('jobs',[])) if j['id'] in job_ids]
    # Hash actual references too: edited pixels cannot hide behind stale metadata.
    for ref in refs:
        if ref.get('path'):
            source=safe(packet,ref['path'])
            require(source.is_file() and blob_hash(source)==ref['sha256'],'Reference media missing or hash changed')
    result=dict(shot=shot,event=event,entities=entities,references=refs,dependencies=dependencies,dependency_events=dependency_events,
                character_direction=direction,owner_conflicts=load(packet/'CONFLICT_RESOLUTIONS.json'))
    if jobs or variants:result.update(career_jobs=jobs,career_variants=variants)
    return result

def attempt_path(packet,shot_id,attempt):
    require(bool(ID.fullmatch(shot_id)),'Invalid shot ID')
    require(type(attempt) is int and 1<=attempt<=999,'Attempt out of range')
    return safe(packet,f'reshoots/attempts/{shot_id}/A{attempt:03d}')

def export_request(packet,shot_id):
    snapshot=contract(packet,shot_id)
    folder=safe(packet,f'reshoots/attempts/{shot_id}')
    attempts=sorted(folder.glob('A[0-9][0-9][0-9]')) if folder.exists() else []
    number=len(attempts)+1
    require(number<=3,'Three-attempt cap reached: owner/operator must review the approach; no blind retry loop')
    previous=None;review=None;superseded=False
    if attempts:
        previous=attempts[-1]
        review=load(previous/'REVIEW.json') if (previous/'REVIEW.json').exists() else None
        superseded=(previous/'SUPERSEDED.json').exists()
        if superseded:
            marker=load(previous/'SUPERSEDED.json');old=load(previous/'REQUEST.json')
            require(marker.get('reason')=='SOURCE_CONTRACT_CHANGED' and
                    marker.get('request_sha256')==blob_hash(previous/'REQUEST.json') and
                    marker.get('old_contract_sha256')==old['contract_sha256'] and
                    marker.get('new_contract_sha256')==fingerprint(snapshot) and
                    marker['old_contract_sha256']!=marker['new_contract_sha256'] and
                    marker.get('generation_ready') is False and marker.get('delivery_accepted') is False,
                    'Invalid or stale SUPERSEDED marker')
        elif review:
            check_current(packet,load(previous/'REQUEST.json'))
            verify_history(packet,previous)
        require(superseded or (review and review['decision']=='REGENERATE'),'Only reviewed regeneration or explicitly superseded stale requests permit a next attempt')
        require(int(previous.name[1:])==number-1,'Noncontiguous attempt history')
    shot=snapshot['shot']
    prompt=shot['prompt']
    if previous and review and not superseded:
        # Refinements are quoted task data; no executable code or external instructions are run.
        corrections=[i['reconstruction'] for i in review['issues']]
        prompt=prompt.rstrip()+'\n\nRevision requirements (same shot, fixed identity/layout):\n'+'\n'.join('- '+x for x in corrections)
        sound=[line for line in shot['prompt'].splitlines() if line.startswith('Sound:')]
        prompt+='\n'+(sound[-1] if sound else 'Sound: gentle scene foley; no synthesized family voices.')+'\n'
    request=dict(schema=SCHEMA,shot_id=shot_id,attempt=number,kind='PLANNING_REQUEST',
                 contract_sha256=fingerprint(snapshot),snapshot=snapshot,prompt=prompt,
                 prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest(),
                 parent_review_sha256=blob_hash(previous/'REVIEW.json') if previous and review and not superseded else None,
                 supersedes_request_sha256=blob_hash(previous/'REQUEST.json') if previous and (previous/'SUPERSEDED.json').exists() else None,
                 generation_ready=False,delivery_accepted=False,
                 blocking=['Owner must approve the exact first-frame file and hash',
                           'Resolve and independently verify 2–4 approved IMAGE bindings',
                           'Run Imagine readiness gate; this tool never authorizes or runs generation'])
    target=attempt_path(packet,shot_id,number)/'REQUEST.json'
    immutable(target,request)
    return target

def check_current(packet,request):
    require(request.get('schema')==SCHEMA,'Wrong request schema')
    require(fingerprint(request['snapshot'])==request['contract_sha256'],'Frozen request snapshot changed')
    require(hashlib.sha256(request['prompt'].encode()).hexdigest()==request['prompt_sha256'],'Frozen request prompt changed')
    require(request.get('generation_ready') is False and request.get('delivery_accepted') is False,'Request cannot grant approval')
    require(fingerprint(contract(packet,request['shot_id']))==request['contract_sha256'],'STALE: shot, entity, event, dependency or authority changed; resolve before reusing')

def verify_history(packet,folder):
    """Recheck frozen links and bytes on every reuse, not just initial ingestion."""
    returned=load(folder/'RETURN.json')
    require(returned.get('request_sha256')==blob_hash(folder/'REQUEST.json'),'Return request link changed')
    require(returned.get('delivery_accepted') is False and returned.get('generation_ready') is False,'Return cannot grant approval')
    for artifact in returned['artifacts']:
        media=safe(packet,artifact['path'])
        require(media.is_relative_to((packet/'reshoots/inbox').resolve()),'Returned media escapes inbox')
        require(media.is_file() and blob_hash(media)==artifact['sha256'],'Returned media changed after ingest')
        require(media.stat().st_size==artifact['bytes'],'Returned byte size changed')
    if (folder/'REVIEW.json').exists():
        review=load(folder/'REVIEW.json')
        require(review.get('return_sha256')==blob_hash(folder/'RETURN.json'),'Review return link changed')
        require(review.get('delivery_accepted') is False,'Review cannot grant approval')
        require(review.get('decision') in ('REGENERATE','HOLD','ROUGH_REFERENCE_CANDIDATE'),'Invalid recorded QC decision')
    return returned

def ingest_return(packet,path):
    returned=load(path)
    folder=attempt_path(packet,returned['shot_id'],returned['attempt'])
    request=load(folder/'REQUEST.json');check_current(packet,request)
    require(returned.get('request_sha256')==blob_hash(folder/'REQUEST.json'),'Return does not match this exact request')
    require(returned.get('delivery_accepted') is False and returned.get('generation_ready') is False,'Generator cannot grant approval')
    require(isinstance(returned.get('generator'),str) and returned['generator'].strip(),'Generator/model name required')
    media=returned.get('artifacts')
    require(isinstance(media,list) and 1<=len(media)<=8,'One to eight returned artifacts required')
    seen=set()
    for item in media:
        require(item.get('role') in ('clip','first_frame_candidate','end_frame','contact_sheet'),'Unknown artifact role')
        require(bool(HASH.fullmatch(str(item.get('sha256','')))),'Artifact SHA256 required')
        p=safe(packet,item['path'])
        require(p.is_relative_to((packet/'reshoots/inbox').resolve()),'Returned media must already be inside reshoots/inbox')
        require(p not in seen,'Duplicate artifact path');seen.add(p)
        require(p.is_file() and blob_hash(p)==item['sha256'],'Missing or hash-mismatched returned artifact')
        require(type(item.get('bytes')) is int and p.stat().st_size==item['bytes'],'Artifact byte size mismatch')
        if item.get('source_url'):
            u=urlparse(item['source_url'])
            require(u.scheme=='https' and u.hostname and not u.username and not u.password,'Only credential-free HTTPS source URLs allowed')
            require(not u.query and not u.fragment,'Use a durable query-free source URL, never a signed download/token URL or fragment')
        if item['role']=='clip':
            require(item.get('fps')==24 and type(item.get('frames')) is int and item['frames']>0,'Clip frame count and 24fps required; metadata still needs ffprobe verification')
    returned['status']='GENERATED_PENDING_QC'
    returned['metadata_verification_only']=True
    target=folder/'RETURN.json';immutable(target,returned)
    return target

def record_review(packet,path):
    review=load(path);folder=attempt_path(packet,review['shot_id'],review['attempt'])
    request=load(folder/'REQUEST.json');check_current(packet,request)
    returned=verify_history(packet,folder)
    require(review.get('return_sha256')==blob_hash(folder/'RETURN.json'),'QC does not match returned artifacts')
    require(review.get('decision') in ('REGENERATE','HOLD','ROUGH_REFERENCE_CANDIDATE'),'Unknown decision; no automatic acceptance')
    require(isinstance(review.get('reviewer'),str) and bool(review['reviewer'].strip()),'Named reviewer required')
    require(review.get('delivery_accepted') is False,'Delivery acceptance cannot be set here')
    require(isinstance(review.get('issues'),list),'Issues must be a list')
    require(review['decision']!='REGENERATE' or bool(review['issues']),'Regeneration requires concrete findings')
    for issue in review['issues']:
        require(issue.get('category') in ('identity','layout','event','contact','motion','camera','sound','technical'),'Unknown issue category')
        artifact=next((a for a in returned['artifacts'] if a['sha256']==issue.get('artifact_sha256')),None)
        require(artifact is not None,'Finding must bind an actual returned artifact')
        a,b=issue.get('start_frame'),issue.get('end_frame_exclusive')
        require(type(a) is int and type(b) is int and 0<=a<b<=artifact.get('frames',1),'Invalid exact finding span')
        for field in ('observation','expected','reconstruction'):
            require(isinstance(issue.get(field),str) and bool(issue[field].strip()),'Observed defect, expected state and reconstruction text required')
    review['status']='QC_RECORDED_NOT_OWNER_ACCEPTANCE'
    target=folder/'REVIEW.json';immutable(target,review)
    return target

def supersede(packet,shot_id,attempt):
    folder=attempt_path(packet,shot_id,attempt)
    request=load(folder/'REQUEST.json')
    current=fingerprint(contract(packet,shot_id))
    require(current!=request['contract_sha256'],'Only stale requests can be superseded')
    target=folder/'SUPERSEDED.json'
    immutable(target,dict(reason='SOURCE_CONTRACT_CHANGED',request_sha256=blob_hash(folder/'REQUEST.json'),
                          old_contract_sha256=request['contract_sha256'],new_contract_sha256=current,
                          generation_ready=False,delivery_accepted=False))
    return target

def status(packet):
    db=load(packet/'DATABASE.json');rows=[]
    for shot in db['shots']:
        folder=safe(packet,f'reshoots/attempts/{shot["id"]}')
        attempts=sorted(folder.glob('A[0-9][0-9][0-9]')) if folder.exists() else []
        state='NEEDS_APPROVED_FIRST_FRAME'
        if attempts:
            latest=attempts[-1]
            try:
                check_current(packet,load(latest/'REQUEST.json'))
                state='AWAITING_RETURN'
                if (latest/'RETURN.json').exists():
                    verify_history(packet,latest);state='AWAITING_QC'
                if (latest/'REVIEW.json').exists():state=load(latest/'REVIEW.json')['decision']
            except (ValueError,KeyError,OSError,json.JSONDecodeError):state='STALE'
        rows.append(dict(shot_id=shot['id'],attempts=len(attempts),state=state,
                         generation_ready=False,delivery_accepted=False))
    return rows

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('packet',type=Path);sub=p.add_subparsers(dest='command',required=True)
    ex=sub.add_parser('export');ex.add_argument('shot_id')
    ret=sub.add_parser('ingest');ret.add_argument('return_json',type=Path)
    qc=sub.add_parser('review');qc.add_argument('review_json',type=Path)
    stale=sub.add_parser('supersede');stale.add_argument('shot_id');stale.add_argument('attempt',type=int)
    sub.add_parser('status')
    args=p.parse_args();packet=args.packet.resolve()
    try:
        if args.command=='export':result=str(export_request(packet,args.shot_id))
        elif args.command=='ingest':result=str(ingest_return(packet,args.return_json))
        elif args.command=='review':result=str(record_review(packet,args.review_json))
        elif args.command=='supersede':result=str(supersede(packet,args.shot_id,args.attempt))
        else:result=status(packet)
        print(json.dumps(result,indent=2));return 0
    except (ValueError,KeyError,OSError,json.JSONDecodeError) as exc:
        print(json.dumps({'error':str(exc),'state':'BLOCKED_NO_AUTOMATIC_APPROVAL'}));return 1

if __name__=='__main__':raise SystemExit(main())
