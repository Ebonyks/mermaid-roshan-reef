"""Refresh revision-four planning artifacts, never openings or acceptance.

JOBS.json, CHARACTER_DIRECTION.json and SCENE_SHOT_DIRECTION.json are authoring
sidecars. The existing DATABASE is the base library; this tool joins their
records, writes V1-shaped draft shot cards and derives reference/text boards.
No board is a generated scene or a bound first frame.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import shutil
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps


def read(p):
    return json.loads(p.read_text(encoding='utf-8'))


def write(p, value):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')


def font(size):
    for p in ('C:/Windows/Fonts/arial.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'):
        if Path(p).exists():return ImageFont.truetype(p,size)
    return ImageFont.load_default(size=size)


def board(root, shot, refs):
    """Reference art + text beats, not fabricated action frames; new v4 paths."""
    canvas=Image.new('RGB',(1600,1000),'#122239');draw=ImageDraw.Draw(canvas)
    draw.text((38,24),shot['id'],font=font(34),fill='#edf6ff')
    draw.text((38,75),'DRAFT BEAT BOARD / REFERENCE + TEXT ONLY / NOT IMAGE_1',font=font(22),fill='#ffd18c')
    images=[]
    for rid in shot['reference_pool_ids']:
        if rid in refs and refs[rid].get('appearance_authority'):
            images.append(refs[rid])
        if len(images)==3:break
    for i,r in enumerate(images):
        x=38+i*514
        with Image.open(root/r['path']) as original:
            im=ImageOps.contain(original.convert('RGBA'),(494,360))
            canvas.paste(im,(x+(494-im.width)//2,122+(360-im.height)//2),im)
        draw.text((x,492),r['id'],font=font(18),fill='#b4d8e5')
    for i,(name,beat) in enumerate(zip(('BEFORE','ACTION / CONTACT','AFTER'),shot['beats'])):
        x=38+i*514;draw.rounded_rectangle((x,540,x+494,906),12,fill='#213951')
        draw.text((x+20,557),name,font=font(24),fill='#b9eee1')
        draw.multiline_text((x+20,606),'\n'.join(textwrap.wrap(beat,35)),font=font(23),fill='white',spacing=8)
    draw.text((38,936),'Exact cast, camera address, frame ranges and blockers: adjacent SHOT_PACKET.json',font=font(22),fill='#d3e2f0')
    relative=f'boards_v4/{shot["id"]}.jpg';target=root/relative
    target.parent.mkdir(parents=True,exist_ok=True)
    canvas.save(target,quality=90,subsampling=0)
    return relative,[r['path'] for r in images]


def bundle_jobs(root, source):
    """Byte-identical runtime art, not scene generation. No originals are edited."""
    db=read(root/'DATABASE.json');jobs=read(root/'JOBS.json');prov=read(root/'PROVENANCE_INPUTS.json')
    refs={r['sha256']:r for r in db['references']}
    source_code=set()
    for job in jobs['jobs']+jobs['chapter2_variants']:
        art=job['runtime_art'];paths=[]
        for field,value in art.items():
            if field.endswith('_paths') and isinstance(value,list):paths.extend(value)
            elif field.endswith('_path') and isinstance(value,str):paths.append(value)
        copied=[];missing=[]
        for path in dict.fromkeys(paths):
            original=(source/path).resolve()
            if not original.is_relative_to(source.resolve()):raise ValueError('Source escapes repository')
            if not original.is_file():missing.append(path);continue
            sha=hashlib.sha256(original.read_bytes()).hexdigest()
            if sha not in refs:
                relative='media_jobs/'+sha[:16]+original.suffix
                target=root/relative;target.parent.mkdir(parents=True,exist_ok=True)
                if not target.exists():
                    try:os.link(original,target)
                    except OSError:shutil.copyfile(original,target)
                dimensions=None
                if original.suffix.lower()=='.png':
                    with Image.open(original) as im:dimensions=list(im.size)
                r=dict(id='REF-'+sha[:16],path=relative,sha256=sha,dimensions=dimensions,
                       role='runtime career source sheet/tile/prop; comparison only, not IMAGE_1',appearance_authority=False,
                       source_paths=[path],license_provenance='Existing project-owned career artwork; source ASSET_LICENSES.md included',
                       modifications='byte-identical copy; no original modified',used_as_delivery_pixels=False)
                refs[sha]=r;db['references'].append(r);prov[relative]=r
            copied.append(refs[sha]['id'])
        job['reference_ids']=list(dict.fromkeys(copied+art.get('exact_existing_builder_reference_ids',[])))
        job['name']=job.get('title',job.get('canon_key',job['id']))
        art['bundled_reference_ids']=job['reference_ids'];art['unavailable_paths']=missing
        art['bundle_status']='SOURCE_ART_BUNDLED_NOT_FIRST_FRAME_APPROVAL'
        source_code.update(job['source_paths'])
    # Preserve the actual script evidence as inert text, never executable imports.
    for path in sorted(source_code|{'ASSET_LICENSES.md','scripts/castle_career_routes.gd'}):
        src=source/path
        if not src.is_file():continue
        relative='evidence/job_sources/'+path.replace('/','__')+'.txt'
        target=root/relative;target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(src,target)
        prov[relative]=dict(source_paths=[path],role='inert source evidence for job/event/asset claims',dimensions=None,
                            license_provenance='Project-authored source / embedded original asset ledger',modifications='byte-identical snapshot')
    # Each proposed phase is legible on its job board, with source artwork above it.
    by_id={r['id']:r for r in db['references']}
    for job in jobs['jobs']+jobs['chapter2_variants']:
        phases=job.get('freeplay_phases',job.get('phases',[]));height=520+len(phases)*140
        canvas=Image.new('RGB',(1600,height),'#122239');draw=ImageDraw.Draw(canvas)
        draw.text((35,22),job['id']+' / '+job['name'],font=font(32),fill='white')
        draw.text((35,70),'SOURCE TILES / COSTUME SHEET + PROPOSED BEATS — NOT AN APPROVED SETUP',font=font(21),fill='#ffd18c')
        raster=[by_id[r] for r in job['reference_ids'] if by_id[r]['path'].endswith('.png')]
        # Show one venue tile, the costume sheet and prop where available; never join tiles incorrectly.
        actor=[r for r in raster if any('sheet_a' in p for p in r['source_paths'])]
        chosen=(raster[:1]+actor[:1]+[r for r in raster if any('/props/' in p for p in r['source_paths'])][:1])
        chosen=list({r['id']:r for r in chosen}.values())
        for i,r in enumerate(chosen):
            with Image.open(root/r['path']) as im:
                thumb=ImageOps.contain(im.convert('RGBA'),(475,340));x=35+i*520
                canvas.paste(thumb,(x+(475-thumb.width)//2,118+(340-thumb.height)//2),thumb)
            draw.text((x,464),r['id'],font=font(18),fill='#b4d8e5')
        for i,phase in enumerate(phases):
            y=520+i*140
            draw.text((35,y),str(i+1)+'. '+phase['label'],font=font(26),fill='#b9eee1')
            text=phase['action']+' End: '+phase['visible_endpoint']
            draw.multiline_text((35,y+39),'\n'.join(textwrap.wrap(text,110)),font=font(23),fill='white',spacing=7)
        relative='boards_jobs/'+job['id']+'.jpg';target=root/relative
        target.parent.mkdir(parents=True,exist_ok=True);canvas.save(target,quality=90,subsampling=0)
        job['board']=relative
        prov[relative]=dict(source_paths=[r['path'] for r in chosen]+['JOBS.json'],dimensions=[1600,height],
                           role='career phase contact sheet; not generated action frames or IMAGE_1',
                           license_provenance='Project-owned source previews and direction',modifications='Reference thumbnails with authored phase text')
    write(root/'DATABASE.json',db);write(root/'JOBS.json',jobs);write(root/'PROVENANCE_INPUTS.json',prov)


def refresh(root):
    db=read(root/'DATABASE.json');direction=read(root/'SCENE_SHOT_DIRECTION.json')
    character=read(root/'CHARACTER_DIRECTION.json');jobs=read(root/'JOBS.json')
    db['jobs']=jobs['jobs'];db['job_variants']=jobs['chapter2_variants'];db['revision']=max(4,db.get('revision',0))
    db['extension_source_baseline']=direction['source_baseline']
    db['authoring_sidecars']=['JOBS.json','CHARACTER_DIRECTION.json','SCENE_SHOT_DIRECTION.json']
    entities={e['id']:e for e in db['entities']};events={e['id']:e for e in db['events']}
    refs={r['id']:r for r in db['references']};prov=read(root/'PROVENANCE_INPUTS.json')
    for c in character['characters']:
        entities[c['entity_id']]['generation_direction']=c
    for s in db['shots']:
        e=events[s['event_id']];historical=s.get('source_card',{})
        s.setdefault('beats',[e['before_state'],e['action'],e['after_state']])
        delta=direction['shot_overrides'].get(s['id'],{})
        s['beats']=[delta.get(k,b) for k,b in zip(('before','action','after'),s['beats'])]
        s['revision']=max(2,s.get('revision',0))
        if 'open_gap' in delta:s['coverage_gap']=delta['open_gap']
        if not s.get('prompt'):
            s['prompt']=(root/'shots'/s['id']/'PROMPT_DRAFT.txt').read_text(encoding='utf-8')
        s.setdefault('depends_on',[])
        s['depends_on']=list(dict.fromkeys(s['depends_on']+direction.get('shot_dependencies',{}).get(s['id'],[])))
        # Empty cast on inherited lawn cards is an unresolved cast, not an empty scene.
        s['cast_status']='EXACT_CAST_PENDING' if not s.get('character_ids') else 'PROPOSED_CAST_REQUIRES_FIRST_FRAME_REVIEW'
        s['scene_cohort_ids']=e['character_ids']
        s['reference_pool_ids']=list(dict.fromkeys(s.get('reference_pool_ids',[])+
            [r for key in [s['location_id']]+(s.get('character_ids') or e['character_ids'])+e.get('prop_ids',[])
             for r in entities[key]['reference_ids']]))
        duration=s['duration_seconds'];n=round(duration*24)
        s['timeline']=[dict(start_frame=0,end_frame_exclusive=24,intent=s['beats'][0]),
                       dict(start_frame=24,end_frame_exclusive=n-24,intent=s['beats'][1]),
                       dict(start_frame=n-24,end_frame_exclusive=n,intent=s['beats'][2])]
        s['timeline_basis']='PROPOSED_24FPS_NOT_MEASURED_RETURN_FOOTAGE'
        s['camera_address']=direction['location_setups'].get(s['location_id'],'Missing approved complete location setup; do not invent one.')
        if s['id'].startswith('SHOT-CRAFT-PICK'):
            s['camera_address']+=' Supply-contact medium insert, keeping the stocked rear table visible as depth anchor.'
        elif s['id'].startswith('SHOT-CRAFT-SCRUB'):
            s['camera_address']+=' Frame the named surface with the adjoining counter/table edge visible; retain screen-side ordering.'
        risk=direction['specific_risks'].get(s['id'],'Do not undo prior saved work, repair unseen geometry, or add a premature success.')
        s['specific_continuity_risk']=risk
        s['generation_ready']=False;s['delivery_accepted']=False;s['opening_reference_id']=None
        if not historical or delta:
            identity=[]
            for key in s.get('character_ids',[]):
                if key in ('CHAR-ROSHAN','CHAR-DADDY','CHAR-RUMI','CHAR-EAGLE'):
                    identity.append(entities[key]['generation_direction']['identity_locks'][0])
            s['prompt']=(f"locked camera on IMAGE_1.\n0-1s: {s['beats'][0]}.\n"
                f"1-{duration-1}s: {s['beats'][1]}.\n{duration-1}-{duration}s: {s['beats'][2]}.\n"
                f"keep the approved room, fixed fixtures and prior completed work unchanged. preserve {'; '.join(identity)}\n"
                f"{direction.get('prompt_constraints',{}).get(s['id'],direction['specific_risks'].get(s['id'],''))}\n"
                f"no HUD, text, extra actors/limbs, tool swapping, new doors or camera drift. end: {s['beats'][2]}.\n"
                "Sound: gentle contact-matched foley and room tone; no speech or synthesized family voices.\n")
        if historical:
            # Preserve the historical card as evidence, not its provisional global scale command.
            s['prompt']='\n'.join(line for line in s['prompt'].splitlines()
                if not line.startswith('keep shared-ground heights locked:'))+'\n'
            scale='preserve the same lawn patch; never compress the whole panorama.'
            if s['id'] in ('SHOT-C2-03','SHOT-C2-04','SHOT-C2-08'):
                scale+=' on the shared ground plane, the Prince is 80% of the King\'s height; preserve IMAGE_1 staging for all other relative scales.'
            if scale not in s['prompt']:
                s['prompt']=s['prompt'].replace('Sound:',scale+'\nSound:',1)
        s['blocking']=list(dict.fromkeys(s.get('blocking',[])+[
            'Exact complete first-frame filename/hash needs owner approval; no board or room-only fallback',
            'Resolve exact cast, 2–4 bindings, contact/scale, incoming/outgoing endpoint review',
            'Independent Imagine readiness gate and full-frame delivery gate remain required']))
        if e.get('open_decision'):s['blocking'].append(e['open_decision'])
        if s['cast_status']=='EXACT_CAST_PENDING':s['blocking'].append('Source scene cohort is not an exact shot cast; resolve before generation')
        s['board'],sources=board(root,s,refs)
        prov[s['board']]=dict(source_paths=sources+['SCENE_SHOT_DIRECTION.json','DATABASE.json'],dimensions=[1600,1000],
            role='reference artwork plus proposed text beat board; narrative only, never IMAGE_1',
            license_provenance='Project-owned reference artwork; original source provenance in DATABASE references',
            modifications='Non-destructive resized source previews beside authored text; no generated action image or delivery pixels')
        card=dict(schema='builder-shot-planning-v1',shot_id=s['id'],event_id=s['event_id'],status='DRAFT',
            template='evidence/IMAGINE_SHOT_CARD_V1.txt',duration_seconds=duration,aspect='16:9',size=[1280,720],
            mode='image_to_video',output_disposition='motion_reference_only',
            bindings=[dict(id='IMAGE_1',path=None,role='approved complete first frame',human_review=None)],
            reference_pool_ids=s['reference_pool_ids'],binding_note='Pool is archival. Choose only 1–3 identity/material refs after complete opening review.',
            beats=s['beats'],timeline=s['timeline'],timeline_basis=s['timeline_basis'],
            camera=historical.get('camera',dict(verb='locked',move_count=0)),camera_address=s['camera_address'],
            cast=s['character_ids'],cast_status=s['cast_status'],scene_cohort_ids=s['scene_cohort_ids'],
            must_move=historical.get('must_move',[s['beats'][1]]),must_not_move=historical.get('must_not_move',['Room landmarks','Unaffected fixtures','Previously completed work']),
            end_state=s['beats'][2],specific_continuity_risk=risk,depends_on=s['depends_on'],depends_on_events=s.get('depends_on_events',[]),
            opening_approval=None,previous_accepted_endpoint=None,blocking_findings=s['blocking'],GENERATION_READY=False,DELIVERY_ACCEPTED=False)
        s['draft_card']=f'shots/{s["id"]}/SHOT_PACKET.json';write(root/s['draft_card'],card)
        (root/'shots'/s['id']/'PROMPT_DRAFT.txt').write_text(s['prompt'],encoding='utf-8')
    # All events appear, including unfilmed careers and real gameplay bridges.
    scene_ids={e['id']:'SCENE-'+e['id'].removeprefix('EV-') for e in db['events']}
    db['scenes']=[]
    for order,e in enumerate(db['events'],1):
        shots=[s for s in db['shots'] if s['event_id']==e['id']]
        db['scenes'].append(dict(id=scene_ids[e['id']],name=e['name'],order=order,event_id=e['id'],
            location_id=e['location_id'],shot_ids=[s['id'] for s in shots],depends_on=[scene_ids[x] for x in e.get('depends_on',[])],
            before_state=e['before_state'],dominant_event=e['action'],after_state=e['after_state'],source=e['source'],
            camera_address=direction['location_setups'].get(e['location_id'],'Detailed approved career setup still required; see JOBS.json'),
            coverage='PARTIAL_DRAFT_SHOTS' if shots else 'NO_DEDICATED_FILM_SHOTS',
            runtime_seam='Enter only after actual prerequisites; exit only to matching saved state. Film never awards or undoes gameplay progress.',
            missing_coverage=[s['coverage_gap'] for s in shots if s.get('coverage_gap')]+([] if shots else ['Needs separate shot breakdown or explicit playable bridge; do not silently omit this event']),
            generation_ready=False,delivery_accepted=False))
    db['reshoot_exchange']='reshoots/README.md'
    write(root/'DATABASE.json',db)
    write(root/'SCENES.json',dict(schema='reef.scene-registry.v1',derived_from='DATABASE.json#scenes',scenes=db['scenes']))
    write(root/'reshoots/QUEUE.json',dict(schema='reef.reshoot-queue.v1',revision=1,
        purpose='All planned shots indexed; not an instruction to regenerate every historical clip',
        rows=[dict(shot_id=s['id'],scene_id=scene_ids[s['event_id']],status='NEEDS_APPROVED_FIRST_FRAME',
                   draft_card=s['draft_card'],board=s['board'],generation_ready=False,delivery_accepted=False) for s in db['shots']]))
    write(root/'PROVENANCE_INPUTS.json',prov)
    automation=root/'automation';automation.mkdir(exist_ok=True)
    shutil.copyfile(Path(__file__).parent/'grok_reshoot_exchange.py',automation/'grok_reshoot_exchange.py')
    print(f"Refreshed {len(db['jobs'])} jobs, {len(db['scenes'])} scenes, {len(db['shots'])} shot cards/boards")


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('packet',type=Path);parser.add_argument('--source-assets',type=Path)
    args=parser.parse_args()
    if args.source_assets:bundle_jobs(args.packet,args.source_assets)
    refresh(args.packet)
