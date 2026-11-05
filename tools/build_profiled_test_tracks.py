"""Build original private review scores and measured native-Falcon test receipts.

MIDI, effects, routing, printing and mastering run through the guarded REAPER Lua
worker. Vendor soundbanks and captured plug-in states stay in ignored build paths.
"""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import random
import shutil
import subprocess

import numpy as np
import soundfile as sf
import balance_main_arrangements as audio
from prepare_instrument_auditions import lua, note

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / 'build/profiled_test_tracks_20261101'
AUD = ROOT / 'build/expanded_palette_auditions_20261101'
CAP = ROOT / 'build/dkc_instrument_auditions_20261101'
PACKAGE = ROOT / 'assets_src/audio/music/profiled_test_tracks_20261101'
PLAN = ROOT / 'design/music/CUE_PLANS_2026-11-01.json'
NEW = ['percussion_factory_mambo_night_100', 'keysuite_acoustic_tdr_mellow_dark',
       'keysuite_electric_w200_basic_dry', 'atmospherics_warmth', 'ether_fields_castle_texture']
GROUPS = [dict(id=k, name=n, pan=p, room_send_db=r) for k,n,p,r in [
    ('foreground','Written melodies and foreground handoffs',0,-23),
    ('harmony','Warm chords and quiet textures',-.08,-25),
    ('bass','Bass foundation',0,-70),('kit','Lo-fi pulse',0,-34),
    ('percussion','World percussion',.10,-30)]]

def save(path, value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def native(path):
    root=audio.native_state(path);programs=list(root.iter('Program'));assert len(programs)==1,path
    return programs[0]

def prepare_auditions():
    AUD.mkdir(parents=True,exist_ok=True);BUILD.mkdir(parents=True,exist_ok=True)
    tests=[]
    for ident in NEW:
        state=CAP/(ident+'.chunk.b64');p=native(state);notes=[]
        if ident.startswith('percussion'):
            for i,key in enumerate([24,26,28,29,31,33,35,36]):notes.append(note(2+i,key,70,.1))
            for bar in range(2):
                q=10+bar*4
                for beat,key,vel in [(0,24,76),(.75,33,52),(1.5,29,64),(2,35,39),(2.75,31,69),(3.5,33,51)]:notes.append(note(q+beat,key,vel,.1))
        else:
            chords=[[55,62,67,71],[52,59,64,67],[48,55,60,64],[50,57,62,66]]
            for b,ch in enumerate(chords):
                for i,key in enumerate(ch):notes.append(note(2+b*4+i*.015,key,58+i*2,3.55 if 'fields' in ident or 'atmos' in ident else 2.9))
        tests.append(dict(id=ident,state=state.relative_to(ROOT).as_posix(),state_sha256=audio.sha(state),
                          program=p.get('DisplayName'),program_path=p.get('ProgramPath'),bpm=100,
                          notes=notes,end_qn=18,tail_seconds=4.5,
                          eq=[['hp',35 if 'percussion' in ident else 100,0,1],['lp',12500 if 'percussion' in ident else 8500,0,.8]],
                          purpose='Original direct-hit mapping and groove diagnostic; no factory sequence trigger' if 'percussion' in ident else 'Original sustained chord and dynamic-response diagnostic'))
    seq=deepcopy(tests[0]);seq.update(id=NEW[0]+'_sequence',notes=[note(2,72,80,16)],purpose='Factory Mambo Night 100 BPM sequence for host-sync verification; not an original authored rhythm');tests.append(seq)
    save(AUD/'auditions.json',tests);(AUD/'auditions.lua').write_text('return '+lua(tests)+'\n',encoding='utf-8')
    save(BUILD/'source_capture_receipt.json',[dict(id=t['id'],program=t['program'],program_path=t['program_path'],state_sha256=t['state_sha256'])for t in tests])
    print('EXPANDED_AUDITIONS|PREPARED|',len(tests))

def finish_auditions():
    import finish_instrument_auditions as finish
    assert (AUD/'render_status.txt').read_text(encoding='utf-8').startswith('COMPLETE 6')
    finish.BUILD=AUD;finish.audio.BUILD=AUD;(AUD/'review').mkdir(exist_ok=True)
    tests=json.loads((AUD/'auditions.json').read_text(encoding='utf-8'))
    with ThreadPoolExecutor(max_workers=2)as pool:rows=list(pool.map(finish.one,tests))
    for row in rows:
        row.update(active_articulation=None,bpm=100,readiness='NATIVE_RECALLED_RENDERED_AND_MEASURED')
        source=sf.read(AUD/(row['id']+'.wav'),dtype='float32',always_2d=True)[0]
        row['preroll_peak']=float(np.max(np.abs(source[:40000])))
    receipt=dict(status='PASS_NATIVE_AND_MEASUREMENTS',checked_utc=datetime.now(timezone.utc).isoformat(),tests=rows)
    save(AUD/'measurement_receipt.json',receipt)
    path=ROOT/'design/music/INSTRUMENT_AUDITIONS_2026-11-01.json';d=json.loads(path.read_text(encoding='utf-8'));ids={r['id']for r in rows}
    d['tests']=[r for r in d['tests']if r['id']not in ids]+rows;d['expanded_palette']=dict(receipt='build/expanded_palette_auditions_20261101/measurement_receipt.json',native_tests=6,owner_listening='PENDING')
    save(path,d);print('EXPANDED_AUDITIONS|PASS|',len(rows))

# The score generator below preserves the owner's original A/B themes; it does
# not transcribe a reference recording or substitute generic backing loops.

CHORDS = {
 'opera_house': [[50,57,59,66],[50,57,59,66],[55,59,62,64],[57,61,64,67],[47,54,57,62],[55,59,62,64],[52,55,59,62],[50,57,59,66]],
 'sky_lagoon': [[55,57,62,67],[54,57,62,66],[52,55,59,62],[48,55,59,64],[47,55,57,62],[45,52,55,60],[50,57,62,67],[55,57,62,67]],
 'castle': [[46,53,55,62],[46,53,55,62],[51,55,58,60],[53,57,60,63],[43,50,53,58],[48,55,58,62],[53,57,60,63],[46,53,55,62]]}


def prepare_scores():
    assert (AUD/'measurement_receipt.json').is_file(),'Audition the expanded palette before construction'
    auditions=json.loads((ROOT/'design/music/INSTRUMENT_AUDITIONS_2026-11-01.json').read_text(encoding='utf-8'))
    measured={a['id']:a for a in auditions['tests']}
    specs={a['id']:a for a in json.loads((CAP/'auditions.json').read_text(encoding='utf-8'))+json.loads((AUD/'auditions.json').read_text(encoding='utf-8'))}
    plans=json.loads(PLAN.read_text(encoding='utf-8'))
    replacements={'opera_house':{'keys':['keysuite_electric_w200_basic_dry'],'producer':['bba2_ace_t1','percussion_factory_mambo_night_100']},
                  'sky_lagoon':{'producer':['lofi_dreams_foley_kit','atmospherics_warmth']},
                  'castle':{'keys':['keysuite_acoustic_tdr_mellow_dark'],'producer':['lofi_dreams_foley_kit','ether_fields_castle_texture']}}
    for c in plans['cues']:
        for chair in c['performers']:
            if chair['profile_id'] in replacements[c['id']]:
                chair['audition_ids']=replacements[c['id']][chair['profile_id']]
                chair['sources']=[dict(audition_id=k,program=measured[k]['program'],program_path=measured[k]['program_path'],active_articulation=measured[k].get('active_articulation'))for k in chair['audition_ids']]
                extra='Produced layers are declared overdubs; one physical keyboard/guitar never comps and plays its lead simultaneously.'
                chair['physical_model']=chair['physical_model'].replace(extra,'').strip()+' '+extra
        c['hook']['source']='assets_src/audio/music/arranged_main_themes_20261101/approved_melodies/'+c['id']+'.json'
    plans['cues'][2]['hook']['recognition']='Original approved 3/4 theme: D4–C4–Bb3, then F4 into G4; descending home gesture and complete eight-bar answer.'
    plans['cues'][2]['hook']['preserve']='Return to the original owner-approved 3/4 A/B melody; the later 4/4 warm-ensemble study remains historical.'
    save(PLAN,plans)
    subprocess.run(['python','-B','tools/audit_music_performer_plans.py','--for-construction','--test-tracks'],cwd=ROOT,check=True)
    scores=[];part_gains={};capture=[]
    for cue in plans['cues']:
        ident=cue['id'];beats=cue['meter'][0]*4/cue['meter'][1];rng=random.Random(20261101+len(ident));base=beats
        original_path=ROOT/cue['hook']['source'];original=json.loads(original_path.read_text(encoding='utf-8'))
        approved=json.loads((ROOT/'assets_src/audio/music/arranged_main_themes_20261101/approved_melody_receipt.json').read_text(encoding='utf-8'))
        assert audio.sha(original_path)==next(a['score_sha256']for a in approved['accepted_auditions']if a['id']==ident)
        srcbeat=original['beats'];scale=beats/srcbeat
        pickup=min(0,original['notes'][0]['qn']-original['sections'][0]['start_qn'])
        motifs={}
        for theme,secidx in [('A',0),('B',2)]:
            sec=original['sections'][secidx];start=sec['start_qn'];end=start+8*srcbeat
            motifs[theme]=[dict(qn=(n['qn']-start)*scale,pitch=n['pitch'],duration_qn=n['duration_qn']*scale,velocity=n['velocity'])for n in original['notes']if start+pickup-1e-6<=n['qn']<end+pickup-1e-6]
        sections=deepcopy(cue['sections']);tracks=[];part_gains[ident]={}
        def add_track(tid,name,chair,aud,group,kind,eq,pan=0,keyswitch=None):
            spec=specs[aud];state=ROOT/spec['state'];assert audio.sha(state)==spec['state_sha256']
            shutil.copy2(state,BUILD/(aud+'.chunk.b64'))
            t=dict(id=tid,name=name,profile_id=chair,state_id=aud,vendor='Acousticsamples'if aud=='castle_sunbird'else'UVI',
                   library='Sunbird'if aud=='castle_sunbird'else spec['program_path'].split('.ufs')[0].lstrip('$'),preset=spec['program'],
                   program_path=spec['program_path'],active_articulation=measured[aud].get('active_articulation'),mix_group=group,
                   role=kind,ensemble_pan=pan,eq=eq,room_send_db=-27,notes=[],sections=[],keyswitch=keyswitch)
            m=measured[aud];target={'foreground':-27,'harmony':-35,'bass':-32,'kit':-35,'percussion':-35}[group]
            cap={'foreground':-14,'harmony':-21,'bass':-16,'kit':-18,'percussion':-20}[group]
            part_gains[ident][tid]=.10*10**(min(target-m['raw_lufs'],cap-m['raw_true_peak_dbtp'])/20)
            tracks.append(t);return t
        warm_guitar=[['hp',100,0,1],['bell',210,1,1.5],['bell',2700,-3,1.3],['shelf',5200,-2,1],['lp',8200,0,.8]]
        lead_aud={'opera_house':'opera_house_pan','sky_lagoon':'sky_lagoon_flute','castle':'castle_sunbird'}[ident]
        lead_chair={'opera_house':'pitched_percussion','sky_lagoon':'winds','castle':'strings_a'}[ident]
        lead_eq={'opera_house':[['hp',85,0,1],['bell',2800,-2.3,1.4],['lp',11000,0,.8]],'sky_lagoon':[['hp',130,0,1],['bell',3400,-1.2,1.5],['lp',12000,0,.8]],'castle':warm_guitar}[ident]
        lead=add_track('main_melody',{'opera_house':'One steel pan — written principal melody','sky_lagoon':'Flute — complete themes and breathing spaces','castle':'Sunbird steel-string — warm home melody'}[ident],lead_chair,lead_aud,'foreground','main',lead_eq)
        gc=add_track('guitar_chords','Nylon guitar — playable chord answers','strings_b','castle_guitar_comp','harmony','comp',warm_guitar,-.18)
        gl=add_track('guitar_dialogue','Nylon guitar — foreground dialogue; comp rests','strings_b','castle_guitar_comp','foreground','dialogue',warm_guitar,0) if any(sec['foreground']=='strings_b'for sec in sections)else None
        ep_aud={'opera_house':'keysuite_electric_w200_basic_dry','sky_lagoon':'castle_ep','castle':'keysuite_acoustic_tdr_mellow_dark'}[ident]
        eqkeys=[['hp',150,0,1],['bell',2700,-1.4,1.3],['lp',9000,0,.8]]
        kc=add_track('keys_chords','Keys — restrained harmonic support','keys',ep_aud,'harmony','comp',eqkeys,.10)
        kl=add_track('keys_melody','Keys — written pre-chorus and bridge melody','keys',ep_aud,'foreground','dialogue',eqkeys,0)
        bass=add_track('bass','Bass — chord roots, anticipations and phrase cadences','bass','castle_bass'if ident=='castle'else'sky_lagoon_bass','bass','bass',[['hp',32,0,1],['bell',240,-1.5,1.2],['lp',4500,0,.8]])
        if ident=='opera_house':
            add_track('kit','Ace T1 — soft produced backbeat','producer','bba2_ace_t1','kit','kit',[['hp',35,0,1],['lp',10000,0,.8]])
            add_track('congas','Congas — interlocking hand-written pulse','afro_caribbean_percussion','opera_house_congas','percussion','congas',[['hp',90,0,1],['lp',10500,0,.8]],-.14)
            add_track('pf_claves','Percussion Factory — direct claves and shekere','producer','percussion_factory_mambo_night_100','percussion','pf',[['hp',160,0,1],['lp',10000,0,.8]],.16)
            add_track('timbales','Timbales — selected transitions only','aux_percussion','opera_house_timbales','percussion','fills',[['hp',110,0,1],['bell',3300,-1.8,1.3],['lp',10000,0,.8]],.12)
        elif ident=='sky_lagoon':
            add_track('valiha_comp','Valiha D1 — open plucked support','kora','sky_lagoon_valiha','harmony','comp',[['hp',160,0,1],['lp',9500,0,.8]],-.18)
            add_track('valiha_lead','Valiha D1 — written plucked dialogue','kora','sky_lagoon_valiha','foreground','dialogue',[['hp',140,0,1],['lp',10000,0,.8]])
            add_track('tabla','Modern Tabla — original sparse strokes','traditional_percussion','world_modern_tabla','percussion','tabla',[['hp',75,0,1],['lp',11000,0,.8]],.10,38)
            add_track('udu','Udu — contrasting bridge; tabla rests','traditional_percussion','sky_lagoon_udu','percussion','udu',[['hp',45,0,1],['lp',8000,0,.8]],-.12)
            add_track('foley','Foley kit — low-fi connective pulse','producer','lofi_dreams_foley_kit','kit','foley',[['hp',40,0,1],['lp',10000,0,.8]])
            add_track('warmth','Atmospherics Warmth — late-arriving harmonic veil','producer','atmospherics_warmth','harmony','pad',[['hp',320,0,1],['bell',2200,-1.5,1.2],['lp',6500,0,.8]],.10)
        else:
            add_track('kit','LoFi Dreams Jazz Kit — soft three-beat pocket','acoustic_drums','lofi_dreams_jazz_kit','kit','kit',[['hp',35,0,1],['bell',3000,-1.5,1.2],['lp',8000,0,.8]])
            add_track('bodhran','Bodhran — selected low hand-drum support','traditional_percussion','world_bodhran_hits','percussion','bodhran',[['hp',50,0,1],['lp',8500,0,.8]],-.1,36)
            add_track('foley','Foley — occasional quiet wood accent','producer','lofi_dreams_foley_kit','percussion','foley',[['hp',160,0,1],['lp',7500,0,.8]],.12)
            add_track('fm_harp','Ether Fields FM Harp — sparse produced replies','producer','ether_fields_castle_texture','harmony','sparkle',[['hp',330,0,1],['bell',3300,-2,1.2],['lp',8000,0,.8]],.15)
        def emit(t,q,p,v,d=.12,jitter=True):
            if jitter:q+=rng.uniform(-.009,.009)
            if q<base-.75:return
            t['notes'].append(note(q,int(p),int(max(1,min(115,v))),max(.04,d)))
        for si,sec in enumerate(sections):
            nm=sec['name'].lower();q0=base+(sec['start_bar']-1)*beats
            refrain=any(w in nm for w in ['chorus','refrain']);final='final'in nm
            closing=any(w in nm for w in ['close','settle','coda']);opening=si==0;bridge='bridge'in nm
            for t in tracks:
                role=sec['roles'][t['profile_id']];leadmode=t['role']in['main','dialogue']
                active=(role=='lead')if leadmode else(role not in ['rest','lead'] if t['role']=='comp'else role!='rest')
                gain=-90 if not active else (-3 if opening or closing else 0 if final or refrain or bridge else -1.5)
                if t['role']=='pad':gain-=7
                if t['role']=='sparkle':gain-=5
                t['sections'].append(dict(start_qn=q0,gain_db=gain))
                if not active:continue
                if leadmode:
                    theme='B'if'verse'in nm else'A';motif=motifs[theme]
                    for cycle in range(0,sec['bars'],8):
                        length=min(8,sec['bars']-cycle)*beats
                        candidates=[n for n in motif if n['qn']<length-.15]
                        roll=max((n['qn']for n in candidates if n['duration_qn']>=.9 and n['qn']>length-2*beats),default=-999)
                        for n in candidates:
                            pitch=n['pitch']-(12 if t['id']=='valiha_lead' or (t['id']=='guitar_dialogue'and ident=='opera_house')else 0)
                            q=q0+cycle*beats+n['qn'];dur=min(n['duration_qn'],q0+sec['bars']*beats-q-.12)
                            vel=(82 if ident=='sky_lagoon'else 73 if ident=='opera_house'else 69)+(2 if final else -5 if'verse'in nm else 0)+rng.randint(-3,3)
                            if closing and n['qn']>2*beats:continue
                            if t is lead and ident=='opera_house'and refrain and n['qn']==roll:
                                for j in range(int(min(dur,1.8)/.125)):emit(t,q+j*.125,n['pitch'],max(38,int(vel*.70)+(4 if j%2==0 else -2)-j//3),.075)
                            else:emit(t,q,pitch,vel,max(.05,dur))
                    if closing:emit(t,q0+(sec['bars']-2)*beats,{'opera_house':74,'sky_lagoon':67,'castle':58}[ident],61,beats*1.7)
                    continue
                for b in range(sec['bars']):
                    q=q0+b*beats;harmony_index=((b+4)%8)if'verse'in nm else b%8;ch=CHORDS[ident][harmony_index]
                    if t['role']=='comp':
                        if t['id']=='guitar_chords':positions=[.5,2.5]if beats==4 else[.8,1.8]
                        elif t['id']=='valiha_comp':positions=[0,1.5,2.5]if beats==4 else[0,1.5]
                        else:positions=[0,2]if refrain else[0]
                        if opening and b<2 and t['id']!='valiha_comp':continue
                        for k,pos in enumerate(positions):
                            if t['id']=='valiha_comp':emit(t,q+pos,ch[(b+k)%len(ch)]+12,53,.55)
                            else:
                                for j,pitch in enumerate(ch):emit(t,q+pos+j*.025,pitch,51+rng.randint(-4,4),.45 if 'guitar'in t['id']else 1.2)
                    elif t['role']=='bass':
                        root=ch[0]-12
                        positions=[(0,root,1.25),(2.5,root+7,.65),(3.75,root,.17)]if beats==4 else[(0,root,1.65),(2.0,root+7,.65)]
                        if opening or closing:positions=positions[:1]
                        for pos,pitch,dur in positions:emit(t,q+pos,pitch,70+rng.randint(-4,4),dur)
                    elif t['role']=='kit':
                        if opening or bridge or closing or ('verse 1'in nm and b<4):continue
                        if beats==4:
                            for pos,key,vel in [(0,36,69),(1.02,38,48),(2.5,36,61),(3.02,38,52)]:emit(t,q+pos,key,vel)
                            for j in range(8):emit(t,q+j*.5+(.025 if j%2 else 0),42,34 if j%2 else 43,.08)
                        else:
                            for pos,key,vel in [(0,36,58),(1.03,37,33),(2.03,38,42)]:emit(t,q+pos,key,vel)
                            for j in range(3):emit(t,q+j,42,31 if j else 39,.08)
                    elif t['role']=='congas':
                        hits=[(0,48,65),(.75,50,43),(1.5,53,59),(2.75,48,62),(3.5,55,49)]
                        if'verse'in nm and b%2==0:hits=[hits[i]for i in [0,2,4]]
                        for pos,pitch,vel in hits:emit(t,q+pos,pitch,vel)
                    elif t['role']=='pf':
                        if opening or bridge or closing:continue
                        for pos in ([0,1.5,3]if b%2==0 else[1,2]):emit(t,q+pos,33,48,.09)
                        if refrain:
                            for j in range(4):emit(t,q+j+.5,35,35 if j%2 else 43,.08)
                    elif t['role']=='fills':
                        if b==sec['bars']-1 and not closing:
                            keys=sorted({n['pitch']for n in specs['opera_house_timbales']['notes']if n['pitch']>=48})
                            for j in range(4):emit(t,q+beats-1+j*.25,keys[j%len(keys)],43+j*5,.10)
                    elif t['role']=='tabla':
                        if bridge or opening or closing or b==0:continue
                        for pos,key,vel in [(0,48,70),(.75,55,39),(1.5,60,57),(2.75,49,47),(3.5,60,55)]:emit(t,q+pos,key,vel)
                    elif t['role']=='udu':
                        if not bridge:continue
                        keys=sorted({n['pitch']for n in specs['sky_lagoon_udu']['notes']if n['pitch']>=48})
                        for pos,ix,vel in [(0,0,70),(1.5,1,47),(2.75,0,62)]:emit(t,q+pos,keys[ix%len(keys)],vel,.18)
                    elif t['role']=='bodhran':
                        if b==0:continue
                        for pos,key,vel in [(0,48,56),(1.7,49,39),(2.5,50,43)]:emit(t,q+pos,key,vel)
                    elif t['role']=='foley':
                        if opening or closing:continue
                        if ident=='castle':
                            if b%4==3:emit(t,q+1.5,40,31)
                        else:
                            if not bridge:
                                emit(t,q,35,61);emit(t,q+2.75,38,40)
                            for j in range(4):emit(t,q+j+.5,41,31 if j%2 else 40,.08)
                    elif t['role']=='pad':
                        if not(final or'refrain 2'in nm or'refrain 3'in nm)or b%2:continue
                        for pitch in ch[1:]:emit(t,q,pitch+12,51,beats*1.85,False)
                    elif t['role']=='sparkle':
                        if not(bridge or final or closing)or b%4!=2:continue
                        emit(t,q+1,ch[-1]+12,46,.7);emit(t,q+2,ch[-2]+12,41,.7)
        for t in tracks:
            t['notes'].sort(key=lambda n:(n['qn'],n['pitch']));t['native_midi_notes']=len(t['notes'])+bool(t['keyswitch'])
            assert t['notes'],(ident,t['id'],'silent/unwritten part')
        end=base+cue['bars']*beats;renderstart=base-.75
        score=dict(id=ident,title=cue['title']+' — profiled test arrangement',key=cue['key'],bpm=cue['bpm'],meter=cue['meter'],
                   beats_per_bar=beats,bars=cue['bars'],tail_seconds=cue['tail_seconds'],tracks=tracks,sections=sections,
                   composition_start_qn=base,render_start_qn=renderstart,music_end_qn=end,duration_seconds=(end-renderstart)*60/cue['bpm']+cue['tail_seconds'],
                   status='PRIVATE_REVIEW_TEST_NOT_RUNTIME_OR_RELEASE',melody_source=cue['hook']['source'],prior_melody_sha256=audio.sha(original_path),
                   references='DKC1 environmental contrast and motif memory; Bonobo ensemble production; performer-specific principles in the linked cue call sheet.',
                   melody_adaptation='Original A/B pitches preserved; Sky 6/8 quarter-note phrasing expanded 4/3 into 4/4; Castle returns to original approved 3/4; Opera adds bounded cadence rolls.',
                   mastering_plan='Measured part and group gain staging, native ReaEQ, quiet shared room, gentle 1.35:1 glue and measured album gain; native -2 dB peak guard; decoded OGG true-peak/DC/mono checks.')
        score['score_sha256']=hashlib.sha256(json.dumps(score,sort_keys=True,separators=(',',':')).encode()).hexdigest()
        save(PACKAGE/ident/'score.json',score);scores.append(score)
        capture.append(dict(cue=ident,notes=sum(len(t['notes'])for t in tracks),parts=len(tracks),bars=score['bars'],seconds=round(score['duration_seconds'],3),steel_pan_parts=sum('Steel Pan'in t['preset']for t in tracks)))
    (PACKAGE/'performance.lua').write_text('return '+lua(scores)+'\n',encoding='utf-8')
    (BUILD/'part_gains.lua').write_text('return '+lua(part_gains)+'\n',encoding='utf-8')
    (BUILD/'groups.lua').write_text('return '+lua(GROUPS)+'\n',encoding='utf-8')
    save(BUILD/'score_construction_receipt.json',capture)
    print('PROFILED_SCORES|PREPARED|',capture)


def group_gains():
    gains={};rows=[]
    balance={c['id']:c.get('mix_balance_adjustment_db',{})for c in json.loads(PLAN.read_text(encoding='utf-8'))['cues']}
    targets={'foreground':-22.5,'harmony':-31,'bass':-29,'kit':-31.5,'percussion':-31.5}
    caps={'foreground':-8.5,'harmony':-15,'bass':-12,'kit':-12,'percussion':-13}
    for cue in ['opera_house','sky_lagoon','castle']:
        gains[cue]={}
        for g in GROUPS:
            path=BUILD/(cue+'__'+g['id']+'_group.wav');m=audio.measure(path);raw_i=float(m['input_i']);tp=float(m['input_tp'])
            assert raw_i>-65 and tp<-.1,(cue,g,m)
            gain=min(targets[g['id']]-raw_i,caps[g['id']]-tp)+balance[cue].get(g['id'],0);gains[cue][g['id']]=10**(gain/20)
            rows.append(dict(cue=cue,group=g['id'],lufs=raw_i,true_peak_dbtp=tp,gain_db=gain,sha256=audio.sha(path)))
        shutil.copy2(BUILD/(cue+'_source.rpp'),BUILD/(cue+'_source_mix_warm.rpp'))
    (BUILD/'group_gains.lua').write_text('return '+lua(gains)+'\n',encoding='utf-8');save(BUILD/'group_measurements.json',rows)
    print('PROFILED_GROUP_BALANCE|PASS|',len(rows))


def master_gains():
    gains={};rows=[]
    for cue in ['opera_house','sky_lagoon','castle']:
        path=BUILD/(cue+'_mix_glue_v3.wav');m=audio.measure(path);gain=-20-float(m['input_i'])
        gains[cue]=gain;rows.append(dict(cue=cue,input=m,album_gain_db=gain,ceiling_db=-2,sha256=audio.sha(path)))
    (BUILD/'master_gains.lua').write_text('return '+lua(gains)+'\n',encoding='utf-8');save(BUILD/'premaster_measurements.json',rows)
    print('PROFILED_MASTER_GAIN|PREPARED|',gains)


def verify():
    rows=[];(BUILD/'review').mkdir(exist_ok=True)
    for cue in ['opera_house','sky_lagoon','castle']:
        path=BUILD/(cue+'_master_native_warm.wav');pcm,rate=sf.read(path,dtype='float32',always_2d=True)
        score=json.loads((PACKAGE/cue/'score.json').read_text(encoding='utf-8'));assert rate==48000 and pcm.shape[1]==2 and np.isfinite(pcm).all()
        assert abs(len(pcm)/rate-score['duration_seconds'])<.04
        assert np.max(np.abs(pcm))<1
        # Fade only the final 1.5 seconds of the declared post-performance tail.
        n=min(int(1.5*rate),len(pcm));pcm[-n:]*=np.linspace(1,0,n)[:,None]
        out=BUILD/'review'/(cue+'_profiled_test.wav');sf.write(out,pcm,rate,subtype='PCM_24')
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(out),'-c:a','libvorbis','-q:a','6',str(out.with_suffix('.ogg'))],check=True)
        measurements={}
        for file in [out,out.with_suffix('.ogg')]:
            m=audio.measure(file);assert float(m['input_tp'])<=-1.15,(file,m)
            assert -24<float(m['input_i'])<-17,(file,m)
            if file.suffix=='.wav':decoded,rs=sf.read(file,always_2d=True)
            else:
                raw=subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(file),'-f','f32le','-acodec','pcm_f32le','-'],capture_output=True,check=True).stdout
                decoded=np.frombuffer(raw,dtype='<f4').reshape(-1,2);rs=48000
            assert rs==48000 and np.isfinite(decoded).all() and np.max(np.abs(decoded))<1
            dc=float(np.max(np.abs(decoded.mean(axis=0))));assert dc<.003
            mono=decoded.mean(axis=1);delta=20*np.log10(max(np.sqrt(np.mean(mono**2)),1e-12)/max(np.sqrt(np.mean(decoded**2)),1e-12))
            measurements[file.suffix]=dict(lufs=float(m['input_i']),true_peak_dbtp=float(m['input_tp']),dc=dc,mono_rms_change_db=float(delta),sha256=audio.sha(file))
        rows.append(dict(cue=cue,duration_seconds=len(pcm)/rate,score_sha256=score['score_sha256'],measurements=measurements,owner_acceptance='PENDING',runtime_installed=False))
    save(BUILD/'final_verification.json',dict(status='PASS_MACHINE_AUDIO_CHECKS_OWNER_LISTENING_PENDING',tests=rows))
    print('PROFILED_TEST_TRACKS|PASS|',rows)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('stage',choices=['prepare-auditions','finish-auditions','prepare-scores','group-gains','master-gains','verify']);a=parser.parse_args()
    {'prepare-auditions':prepare_auditions,'finish-auditions':finish_auditions,'prepare-scores':prepare_scores,'group-gains':group_gains,'master-gains':master_gains,'verify':verify}[a.stage]()

if __name__=='__main__':main()
