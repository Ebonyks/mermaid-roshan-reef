"""Develop owner-approved melodies into the approved original full-song forms.
All supporting figures are written chord/rhythm parts; no generated lead solos.
"""
from pathlib import Path
import json,hashlib,struct
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets_src/audio/music/arranged_main_themes_20261101'
PC={'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}
def pitch(s):return 12*(int(s[-1])+1)+PC[s[0]]+s[1:-1].count('#')-s[1:-1].count('b')
def lua(v):
 if isinstance(v,dict):return '{'+','.join('['+json.dumps(k)+']='+lua(x) for k,x in v.items())+'}'
 if isinstance(v,list):return '{'+','.join(map(lua,v))+'}'
 if isinstance(v,str):return json.dumps(v,ensure_ascii=False)
 if isinstance(v,bool):return str(v).lower()
 if v is None:return 'nil'
 return str(v)
def add(t,qn,p,d,v):
 assert 0<=p<=127 and 1<=v<=127 and d>0
 t['notes'].append(dict(qn=round(qn,6),pitch=p,duration_qn=round(d,6),velocity=int(v)))
def line(t,start,text,beats,vel=80,gate=.91):
 at=0
 for tok in text.split():
  name,d=tok.split(':');d=float(d)
  if name!='R':add(t,start+at,pitch(name),d*gate,vel)
  at+=d
 assert abs(at-beats)<1e-6,(text,at,beats)
def theme(approved,which):
 sec=next(s for s in approved['sections'] if s['theme']==which)
 lo=sec['start_qn'];span=8*(approved['meter'][0]*4/approved['meter'][1]);pickup=.5 if approved['id']=='opera_house' and which=='A' else 0
 return [{**n,'qn':round(n['qn']-lo,6)} for n in approved['notes'] if lo-pickup-1e-7<=n['qn']<lo+span-(.5 if approved['id']=='opera_house' else 0)-1e-7]
def put(t,start,notes):
 for n in notes:add(t,start+n['qn'],n['pitch'],n['duration_qn'],n['velocity'])
# Bass roots and restrained accompaniment voicings, all in concert pitch.
CH={
'D6':(38,[54,57,59]),'G6':(43,[52,55,59]),'Gmaj7':(43,[54,59,62]),'A7':(45,[55,57,61]),'Bm7':(35,[54,57,62]),'Em7':(40,[52,55,59]),'F#m7':(42,[52,57,61]),'E7':(40,[56,59,62]),
'Gadd9':(43,[55,57,62]),'D/F#':(42,[54,57,62]),'Cmaj7':(36,[52,55,59]),'G/B':(35,[50,55,59]),'Am7':(33,[52,55,60]),'Dsus4':(38,[55,57,62]),'D':(38,[54,57,62]),
'Bb6':(34,[50,53,55]),'Eb6':(39,[48,55,58]),'F7':(41,[51,53,57]),'Gm7':(43,[50,53,58]),'Cm7':(36,[48,51,55]),'Abmaj7':(32,[48,55,56]),'Eb/G':(43,[51,55,58]),'Bb/D':(38,[50,53,58])}
HARM={
'opera_house':{'A':['D6','D6','G6','A7','Bm7','G6','Em7>A7','D6'],'B':['F#m7','Bm7','Em7','A7','D6','G6','E7','A7'],'intro':['D6','D6','G6','A7'],'coda':['D6','G6','Em7','A7','Bm7','G6','A7','D6']},
'sky_lagoon':{'A':['Gadd9','D/F#','Em7','Cmaj7','G/B','Am7','Dsus4>D','Gadd9'],'B':['Em7','Cmaj7','Gadd9','D','Em7','Am7','D/F#','D'],'C':['Em7','Cmaj7','Am7','D','G/B','Cmaj7','Am7','D'],'intro':['Gadd9','D','Gadd9','D','Gadd9','D/F#','Em7','D'],'coda':['Gadd9','D/F#','Em7','Cmaj7','G/B','Am7','D','Gadd9']},
'castle':{'A':['Bb6','Bb6','Eb6','F7','Gm7','Cm7','F7','Bb6'],'B':['Eb6','Abmaj7','Eb/G','Cm7','F7','Bb6','Cm7','F7'],'transition':['Gm7','Cm7','Eb6','F7','Bb/D','Cm7','F7','F7'],'intro':['Bb6','Bb6','Eb6','F7','Gm7','Cm7','F7','Bb6'],'coda':['Bb6','Bb6','Eb6','F7','Gm7','Cm7','F7','Bb6']}}
PALETTE={
'pan':dict(state_id='steel_pan_main',name='Steel Pan - principal melody',preset='Steel Pan Main',vendor='UVI',library='World Suite 3',role='lead',pan=0,target_lufs=-22,peak_cap_db=-8,eq=[['hp',85,0,1],['bell',2900,-1.8,1.25],['shelf',8000,-1,1]],room_send_db=-23),
'flute':dict(state_id='djafe_flute_sustain',name='Flute - principal melody',preset='Djafe Flute Sustain',vendor='UVI',library='World Suite 3',role='lead',pan=0,target_lufs=-22,peak_cap_db=-10,eq=[['hp',130,0,1],['bell',3400,-1.2,1.5],['shelf',8500,-.7,1]],room_send_db=-22),
'guitar_comp':dict(state_id='tchad_nylon_guitar',name='Nylon guitar - offbeat harmony',preset='Tchad Nylon Guitar',vendor='UVI',library='World Suite 3',role='harmony',pan=-.22,target_lufs=-31,peak_cap_db=-18,eq=[['hp',145,0,1],['bell',380,-1.4,1.3],['bell',2300,-1.5,1.2],['shelf',6500,-1.2,1]],room_send_db=-25),
'cuba_bass':dict(state_id='cuba_bass',name='Cuba bass - foundation',preset='Cuba Bass',vendor='UVI',library='World Suite 3',role='bass',pan=0,target_lufs=-28.5,peak_cap_db=-15,eq=[['hp',34,0,1],['bell',240,-2,1.2],['shelf',2400,-2.5,1]],room_send_db=-60),
'congas':dict(state_id='congas',name='Congas - hand-written pulse',preset='Congas',vendor='UVI',library='World Suite 3',role='percussion',pan=.18,target_lufs=-32,peak_cap_db=-16,keyswitch=30,eq=[['hp',70,0,1],['bell',450,-1.2,1.3],['shelf',7000,-1,1]],room_send_db=-30),
'maracas':dict(state_id='maracas',name='Maracas - selected lifts',preset='Maracas',vendor='UVI',library='World Suite 3',role='percussion',pan=-.25,target_lufs=-36,peak_cap_db=-22,keyswitch=34,eq=[['hp',420,0,1],['bell',5200,-1.8,1.6],['shelf',8500,-2,1]],room_send_db=-36),
'valiha':dict(state_id='valiha_native',name='Valiha - open plucked accompaniment',preset='Kora 1 / Valiha articulation',vendor='UVI',library='World Suite 3',role='harmony',pan=-.2,target_lufs=-30.5,peak_cap_db=-18,articulation_selector=3,eq=[['hp',170,0,1],['bell',1250,-2.1,1.5],['shelf',7000,-1,1]],room_send_db=-25),
'udu':dict(state_id='udu_large_restored',name='Udu - breathing pulse',preset='Udu Large',vendor='UVI',library='World Suite 3',role='percussion',pan=.13,target_lufs=-34,peak_cap_db=-19,eq=[['hp',48,0,1],['bell',380,-1.1,1.4],['shelf',5200,-1.5,1]],room_send_db=-30),
'sunbird':dict(state_id='sunbird_solo',name='Sunbird guitar - principal melody',preset='Sunbird / Solo mode',vendor='Acousticsamples',library='Sunbird',role='lead',pan=0,target_lufs=-22,peak_cap_db=-8,eq=[['hp',65,0,1],['bell',3200,-1.5,1.35],['shelf',9000,-.8,1]],room_send_db=-25),
'jazz_bass':dict(state_id='jazzistic_double_bass',name='Upright bass - warm foundation',preset='Jazzistic Double Bass',vendor='UVI',library='Jazzistic',role='bass',pan=-.04,target_lufs=-29,peak_cap_db=-16,eq=[['hp',32,0,1],['bell',225,-2,1.1],['shelf',2300,-1.5,1]],room_send_db=-60),
'brushes':dict(state_id='jazz_brushed_kit_1',name='Brushed kit - restrained waltz',preset='Jazz Brushed Kit 1',vendor='UVI',library='Jazzistic',role='percussion',pan=.12,target_lufs=-34,peak_cap_db=-21,eq=[['hp',60,0,1],['bell',430,-1.4,1.2],['shelf',7000,-1.2,1]],room_send_db=-32),
'ep':dict(state_id='lofi_electric_piano_smokey',name='Electric piano - sparse harmonic colour',preset='The Electric Piano Smokey / Delay 0 / Vinyl 0',vendor='UVI',library='LoFi Dreams',role='harmony',pan=.2,target_lufs=-33,peak_cap_db=-20,eq=[['hp',170,0,1],['bell',350,-1.2,1.4],['bell',1700,-1.8,1.5],['shelf',6500,-1.5,1]],room_send_db=-29)}
FORMS={
'opera_house':[('Curtain glimmer',4,'intro',-3),('A - invitation',16,'A',-1),('B - another doorway',16,'B',-1.7),('A - the room opens',16,'A',0),('Bridge - flute statement',8,'bridge',-2),('B - gathering light',16,'B',-.7),('Final A - celebration',16,'A',.6),('Coda - curtain close',8,'coda',-3)],
'sky_lagoon':[('Cloudwater introduction',8,'intro',-3),('A - open water',16,'A',-1),('B - discovering the horizon',16,'B',0),('A - floating homeward',16,'A',-1.5),('Development - reflected sky',16,'C',-2.5),('Final A - broad horizon',16,'A',.6),('Coda - settling light',8,'coda',-3)],
'castle':[('Guitar welcome',8,'intro',-3),('A - a place to belong',24,'A',-1),('B - through the rooms',24,'B',-1.3),('A return - everyone is home',32,'A',.5),('Coda - home at rest',8,'coda',-3.4)]}
EXTRA={
'opera_bridge':['A4:1 D5:1.5 F#5:.5 E5:.5 R:.5','D5:1.5 B4:.5 A4:1 R:1','G4:.5 A4:.5 B4:1 D5:1 R:1','C#5:1 B4:.5 A4:1.5 R:1','F#4:1 A4:.5 B4:.5 D5:1 R:1','E5:1 D5:1 B4:1 R:1','G#4:1 B4:1 E5:1 R:1','C#5:1 B4:.5 A4:1.5 R:1'],
'opera_coda':['B4:.5 D5:1.5 C#5:.5 B4:.5 A4:1','F#4:1.5 E4:.5 F#4:1 D4:1','G4:1 F#4:.5 E4:.5 D4:1 R:1','E4:1 A4:1.5 R:1.5','B4:.5 D5:1.5 B4:1 R:1','G4:1 F#4:1 E4:1 R:1','C#4:1 E4:1 A4:1 R:1','D4:3.5 R:.5'],
'sky_C':['G4:1.5 D5:1 R:.5','E5:2 R:1','R:3','R:3','B4:1 D5:.5 E5:1 R:.5','C5:1 B4:.5 A4:1 R:.5','F#4:1 A4:.5 D5:1 R:.5','E5:.5 D5:.5 B4:1 R:1','G4:1.5 D5:1 R:.5','B4:1.5 A4:1 R:.5','R:3','R:3','E5:1 D5:.5 B4:1 R:.5','C5:1 B4:.5 A4:1 R:.5','A4:.5 B4:.5 D5:1 R:1','B4:.5 A4:.5 G4:1.5 R:.5'],
'sky_coda':['G4:1.5 D5:1 R:.5','E5:1 B4:.5 A4:1 R:.5','B4:.5 A4:.5 G4:1.5 R:.5','D5:2 R:1','E5:.5 D5:.5 B4:1.5 R:.5','C5:1 B4:.5 A4:1 R:.5','B4:.5 A4:.5 G4:1.5 R:.5','G4:2.5 R:.5'],
'castle_extension':['D4:1 C4:.5 Bb3:.5 F4:1','G4:1.5 F4:.5 D4:1','Eb4:1 F4:.5 G4:.5 Bb4:.75 R:.25','A4:.75 G4:.25 F4:1 R:1','G4:1 F4:.5 Eb4:.5 D4:1','C4:1 Eb4:1 G4:.5 R:.5','F4:1 D4:.5 C4:.5 A3:.75 R:.25','Bb3:2 R:1'],
'castle_transition':['G4:1 F4:1 D4:.75 R:.25','Eb4:1 G4:1 R:1','F4:1 Eb4:.5 D4:.5 C4:1','A3:1 C4:.5 F4:1 R:.5','D4:1 F4:.5 G4:1 R:.5','Eb4:1 D4:.5 C4:1 R:.5','C4:.5 Eb4:.5 F4:1 R:1','A3:1 C4:.5 F4:.75 R:.75'],
'castle_coda':['D4:1 C4:.5 Bb3:.5 F4:1','G4:1.5 F4:.5 D4:1','Eb4:1 D4:1 C4:1','F4:1 A3:1 R:1','D4:1 C4:.5 Bb3:1.5','F4:1 D4:1 R:1','F4:.5 A3:.5 C4:1 R:1','Bb3:2.75 R:.25']}
def build(cue):
 approved=json.loads((OUT/'approved_melodies'/f'{cue}.json').read_text());beats=approved['meter'][0]*4/approved['meter'][1]
 names={'opera_house':['pan','guitar_comp','cuba_bass','congas','maracas','flute'],'sky_lagoon':['flute','valiha','cuba_bass','udu'],'castle':['sunbird','jazz_bass','brushes','ep']}[cue]
 tracks={k:{**PALETTE[k],'id':k,'notes':[],'sections':[]} for k in names};lead=tracks[names[0]]
 if cue=='opera_house':tracks['flute']['name']='Flute - bridge only';tracks['flute']['role']='bridge_lead'
 s={'id':cue,'title':approved['title'],'key':approved['key'],'bpm':approved['bpm'],'meter':approved['meter'],'beats_per_bar':beats,'bars':sum(x[1] for x in FORMS[cue]),'tail_seconds':6,'tracks':list(tracks.values()),'sections':[],'approved_melody_sha256':hashlib.sha256((OUT/'approved_melodies'/f'{cue}.json').read_bytes()).hexdigest(),'melody_statements':[]}
 A=theme(approved,'A');B=theme(approved,'B');bar=1
 for si,(name,bars,kind,dyn) in enumerate(FORMS[cue]):
  sec={'name':name,'start_bar':bar,'bars':bars,'kind':kind,'lead_gain_db':dyn};s['sections'].append(sec);start=bar*beats
  for t in tracks.values():t['sections'].append({'start_qn':start,'end_qn':start+bars*beats,'gain_db':dyn if t['role'] in ['lead','bridge_lead'] else dyn*.75})
  def statement(which,at):
   data=A if which=='A' else B;put(lead,at,data)
   s['melody_statements'].append({'theme':which,'start_qn':at,'track':lead['id'],'approved_pitch_rhythm_velocity':True})
  if kind in ['A','B']:
   reps=bars//8
   for r in range(reps):
    at=start+r*8*beats
    if cue=='castle' and ((kind=='A' and bars==24 and r==2) or (kind=='A' and bars==32 and r==3)):
     for j,l in enumerate(EXTRA['castle_extension']):line(lead,at+j*beats,l,beats,79)
    elif cue=='castle' and kind=='B' and r==2:
     for j,l in enumerate(EXTRA['castle_transition']):line(lead,at+j*beats,l,beats,78)
    else:statement(kind,at)
  elif kind=='intro':
   if cue=='opera_house':put(lead,start,[n for n in A if n['qn']<8])
   elif cue=='sky_lagoon':put(lead,start+4*beats,[n for n in A if 0<=n['qn']<4*beats])
   else:statement('A',start)
  elif kind=='bridge':
   for j,l in enumerate(EXTRA['opera_bridge']):line(tracks['flute'],start+j*beats,l,beats,83,.95)
  elif kind=='C':
   for j,l in enumerate(EXTRA['sky_C']):line(lead,start+j*beats,l,beats,81,.95)
  elif kind=='coda':
   key={'opera_house':'opera_coda','sky_lagoon':'sky_coda','castle':'castle_coda'}[cue]
   for j,l in enumerate(EXTRA[key]):line(lead,start+j*beats,l,beats,78,.94 if cue=='sky_lagoon' else .91)
  harmonic_kind='B' if kind=='bridge' else kind
  for local in range(bars):
   at=(bar+local)*beats
   hk=harmonic_kind
   if cue=='castle' and kind=='B' and local>=16:hk='transition'
   chords=HARM[cue][hk];chord=chords[local%len(chords)]
   cells=chord.split('>');cells=[(j*beats/len(cells),beats/len(cells),c) for j,c in enumerate(cells)]
   def chord_at(pos):return next(c for off,d,c in reversed(cells) if pos>=off)
   def root_at(pos):return CH[chord_at(pos)][0]
   if cue=='opera_house':
    g=tracks['guitar_comp'];bass=tracks['cuba_bass'];conga=tracks['congas'];maraca=tracks['maracas']
    if not(kind=='intro' and local<2):
     rhythm=[1.5,3.5] if si==1 and local<8 else [.5,2.5,3.5]
     if kind=='B':rhythm=[0,2.5]
     if kind=='bridge':rhythm=[0,2.5] if local%2==0 else [1.5]
     if si==6:rhythm=[.5,1.5,2.5,3.5]
     if kind=='intro':rhythm=[0] if local==2 else [1.5,3.5]
     if kind=='coda':rhythm=[1.5] if local<5 else ([0] if local==7 else [])
     for k,pos in enumerate(rhythm):
      voicing=CH[chord_at(pos)][1]
      for j,p in enumerate(voicing):add(g,at+pos+j*.018,p,.36 if kind not in ['B','bridge'] else .68,57+[0,-4,-2][j]+(2 if local%4==3 else 0))
    if not(kind=='intro' and local<2):
     root=root_at(0);add(bass,at+.012,root,3.5 if kind=='coda' and local==7 else 1.35,72)
     if kind!='coda' or local<5:
      add(bass,at+2.5,root_at(2.5),.75,65)
      if local%4==3 and kind not in ['bridge','intro','coda']:add(bass,at+3.5,CH[chords[(local+1)%len(chords)].split('>')[0]][0]-1,.36,59)
    pulse=(si==1 and local>=8) or kind=='B' or si in [3,5,6]
    if pulse:
     pattern=[(0,48,54),(1.5,50,48),(2.5,53,60),(3.5,55,56)]
     if si==6:pattern=[(0,48,58),(.75,50,40),(1.5,53,56),(2.5,50,46),(3,55,64),(3.5,53,59)]
     if kind=='B' and local<8:pattern=[(0,48,49),(2.5,53,54)]
     for pos,p,v in pattern:add(conga,at+pos+.008,p,.14,v)
     if local%8==7 and si in [3,5,6]:add(conga,at+3.75,50,.12,45)
    if si in [3,6] or (si==5 and local>=8):
     for k,pos in enumerate([.5,1.5,2.5,3.5]):add(maraca,at+pos+.012,60 if k%2==0 else 62,.12,38 if k%2==0 else 32)
   elif cue=='sky_lagoon':
    val=tracks['valiha'];bass=tracks['cuba_bass'];udu=tracks['udu']
    voicing=CH[chord_at(0)][1]
    solo_answer=kind=='C' and local in [2,3,10,11]
    rhythm=[0,1,2] if (kind=='intro' and local<4) or solo_answer else [.5,2.55]
    if kind=='coda' and local>=6:rhythm=[0] if local==7 else [1.5]
    for j,pos in enumerate(rhythm):add(val,at+pos,voicing[(local+j)%len(voicing)],.75 if pos<2 else .38,58 if solo_answer else 47)
    if solo_answer:
     # A brief written plucked answer while the flute is silent.
     add(val,at+1.5,voicing[2],.25 if local==10 else .35,54) # Short return answer at the repeated plucked pitch.
    if not(kind=='intro' and local<4) and not(kind=='coda' and local>5):add(bass,at+.016,root_at(0),2.2,61)
    if kind not in ['intro','coda'] and not(si==1 and local<8) and not(kind=='C' and local<8):
     add(udu,at+.01,48,.18,48)
     if local%2==1 or si in [2,5]:add(udu,at+1.5,53,.15,39)
   else:
    bass=tracks['jazz_bass'];brush=tracks['brushes'];ep=tracks['ep']
    if kind!='intro' and not(kind=='coda' and local>=2):
     add(bass,at+.018,root_at(0),1.9,65)
     if local%2==1 and kind!='coda':add(bass,at+2.35,root_at(0)+7 if root_at(0)+7<=48 else root_at(0)-5,.48,53)
    if (kind=='A' and bars==24 and local>=16) or kind=='B' or (kind=='A' and bars==32 and local<24):
     add(brush,at+.02,36,.14,33 if local%2==0 else 26)
     add(brush,at+1.5,38 if local%2==0 else 40,.16,36)
     if local%2==1:add(brush,at+2.5,42,.1,28)
    if kind=='B' or (kind=='A' and bars==32 and local<24):
     if local%2==0 or (kind=='A' and 16<=local<24):
      for j,p in enumerate(CH[chord_at(1.5)][1]):add(ep,at+1.5+j*.012,p,1.15,48-j*2)
  bar+=bars
 # Finish note data and enforce written foreground discipline.
 for t in tracks.values():
  t['notes'].sort(key=lambda n:(n['qn'],n['pitch']))
  t['native_midi_notes']=len(t['notes'])+(1 if 'keyswitch' in t else 0)
  t['stem_file']=cue+'__'+t['id']+('_stem_clean.wav' if t['id']=='valiha' else '_stem.wav')
  if t['role'] in ['lead','bridge_lead']:
   for a,b in zip(t['notes'],t['notes'][1:]):assert a['qn']+a['duration_qn']<=b['qn']+1e-6,(cue,t['id'],'overlapping lead')
 assert sum(t['state_id']=='steel_pan_main' for t in tracks.values())==(1 if cue=='opera_house' else 0)
 if cue=='opera_house':
  bridge=next(x for x in s['sections'] if x['kind']=='bridge');a=bridge['start_bar']*beats;b=a+bridge['bars']*beats
  assert not any(a<=n['qn']<b for n in lead['notes'])
 s['composition_start_qn']=beats;s['music_end_qn']=bar*beats;s['render_start_qn']=beats-(.75 if cue=='opera_house' else .25)
 s['duration_seconds']=(s['music_end_qn']-s['render_start_qn'])*60/s['bpm']+s['tail_seconds']
 s['references']={'opera_house':'Andy Narell: lyrical pan phrasing; Ernest Ranglin: economical syncopated harmony','sky_lagoon':'Johnny Pacheco: flute breath and dialogue; Justin Vali: delicate plucked texture','castle':'Ernest Ranglin: melodic guitar economy and light syncopation'}[cue]
 s['mastering_plan']={'target_lufs':-18.25,'maximum_true_peak_dbtp':-3,'stages':['Native instrument-specific ReaEQ','Measured stem gain and peak caps','Written sectional gain automation','Quiet shared room return','Gentle ReaComp bus control assessed against bypass','Constant-gain mastering with measured oversampled peak control only as needed'],'acceptance':'Owner-approved melodies; complete arrangements and exact masters await listening.'}
 s['score_sha256']=hashlib.sha256(json.dumps(s,sort_keys=True).encode()).hexdigest()
 return s

def vlq(n):
 out=[n&127];n>>=7
 while n:out.insert(0,(n&127)|128);n>>=7
 return bytes(out)
def track_bytes(events):
 data=b'';last=0
 for tick,order,msg in sorted(events):data+=vlq(tick-last)+msg;last=tick
 data+=b'\x00\xff\x2f\x00';return b'MTrk'+struct.pack('>I',len(data))+data

def midi(s):
 meta=[(0,0,b'\xff\x51\x03'+round(60000000/s['bpm']).to_bytes(3,'big')),(0,0,bytes([255,88,4,s['meter'][0],2 if s['meter'][1]==4 else 3,36 if s['meter'][1]==8 else 24,8]))]
 for sec in s['sections']:
  name=sec['name'].encode();meta.append((round(sec['start_bar']*s['beats_per_bar']*960),0,b'\xff\x06'+vlq(len(name))+name))
 chunks=[track_bytes(meta)]
 for t in s['tracks']:
  name=t['name'].encode();ev=[(0,0,b'\xff\x03'+vlq(len(name))+name)]
  notes=list(t['notes'])
  if 'keyswitch' in t:notes=[dict(qn=s['render_start_qn']+.02,pitch=t['keyswitch'],duration_qn=.05,velocity=100)]+notes
  for n in notes:ev.extend([(round(n['qn']*960),2,bytes([144,n['pitch'],n['velocity']])),(round((n['qn']+n['duration_qn'])*960),1,bytes([128,n['pitch'],0]))])
  chunks.append(track_bytes(ev))
 return b'MThd'+struct.pack('>IHHH',6,1,len(chunks),960)+b''.join(chunks)
def main():
 scores=[build(cue) for cue in ['opera_house','sky_lagoon','castle']]
 for s in scores:
  folder=OUT/s['id'];folder.mkdir(exist_ok=True)
  (folder/'score.json').write_text(json.dumps(s,indent=2)+'\n',encoding='utf-8')
  (folder/(s['id']+'_arrangement.mid')).write_bytes(midi(s))
 (OUT/'performance.lua').write_text('return '+lua(scores)+'\n',encoding='utf-8')
 commission={'stage':'FULL_ARRANGEMENT_FROM_APPROVED_MELODIES','owner_request':'These melodies sound good. Build the full arrangements from the approved plans, keeping the melodies clear and giving each song room to develop. Be sure to include proper EQ, balancing and mastering.','approval_scope':'The prior three lead recordings and A/B melodies are accepted. New complete arrangements and mixes still require owner listening.','instrument_policy':'UVI soundkits only, including explicitly selected UVI-powered Acousticsamples Sunbird; one pan in Opera, no pan in Sky or Castle.','no_runtime_integration':True,'external_ai_audio_upload':False,'native_programs_private':True,'forms':[{k:s[k] for k in ['id','title','bars','bpm','meter','duration_seconds','sections']} for s in scores]}
 (OUT/'commission.json').write_text(json.dumps(commission,indent=2)+'\n',encoding='utf-8')
 print(json.dumps([{'cue':s['id'],'bars':s['bars'],'seconds':round(s['duration_seconds'],3),'parts':len(s['tracks']),'notes':sum(len(t['notes']) for t in s['tracks']),'unchanged_approved_statements':len(s['melody_statements'])} for s in scores],indent=2))
if __name__=='__main__':main()
