"""Warmer instrumental performances, complementary guitar chords, and scored ensemble handoffs."""
from pathlib import Path
import json,copy,math,hashlib,collections
from compose_main_arrangements import lua,midi,add,line
from compose_reference_arrangements import HARM,HOOKS,part
ROOT=Path(__file__).resolve().parents[1];OLD=ROOT/'assets_src/audio/music/reference_arrangements_20261101';OUT=ROOT/'assets_src/audio/music/warm_ensemble_20261101'
VOICINGS={
'D6':[50,57,59,66],'G6':[43,50,55,59,64],'A7':[45,52,55,61,64],'Bm7':[47,54,57,62,66],'Em7':[40,47,55,59,62],'F#m7':[42,49,57,61,64],'E7':[40,47,56,62,64],
'Gadd9':[43,50,55,57,62],'D/F#':[42,50,57,62,66],'Cmaj7':[48,55,59,64],'G/B':[47,50,55,62],'Am7':[45,52,55,60,64],'Dsus4':[50,57,62,67],'D':[50,57,62,66],
'Bb6':[46,53,58,62,67],'Eb6':[51,58,60,67],'F7':[41,48,57,63,65],'Gm7':[43,50,58,62,65],'Cm7':[48,55,58,63,67],'Abmaj7':[44,51,55,60,67],'Eb/G':[43,51,58,63,67],'Bb/D':[50,53,58,62,65]}
WARM_GUITAR=[['hp',85,0,1],['bell',220,1.1,1.4],['bell',2900,-2.8,1.45],['shelf',4800,-3.5,1],['lp',8500,0,.8]]
WARM_LEAD=[['hp',65,0,1],['bell',210,1,1.5],['bell',2700,-2.6,1.3],['shelf',5200,-3.1,1],['lp',10500,0,.8]]

def in_block(n,lo,hi):return lo-1e-6<=n['qn']<hi-1e-6

def build(cue):
 s=json.loads((OLD/cue/'score.json').read_text());s['prior_score_sha256']=hashlib.sha256((OLD/cue/'score.json').read_bytes()).hexdigest();s['revision']='WARM_GUITAR_ENSEMBLE_PAN_ROLLS';s['rolls']=[];s['phrases']=[]
 tracks={t['id']:t for t in s['tracks']};lead={'opera_house':'pan','sky_lagoon':'flute','castle':'sunbird'}[cue]
 if cue=='castle':
  t=part('flute_colour','flute',name='Flute - contrasting middle chorus',role='section_lead',mix_group='foreground',pan=0,ensemble_pan=0);tracks[t['id']]=t;s['tracks'].append(t)
 if cue=='opera_house':tracks['flute_response']['mix_group']='foreground'
 for t in s['tracks']:
  if t['id']=='guitar_comp':t['state_id']='tchad_nylon_warm';t['eq']=copy.deepcopy(WARM_GUITAR);t['name']='Warm nylon guitar - voiced chords and fingerstyle pulse'
  if t['id']=='sunbird':t['eq']=copy.deepcopy(WARM_LEAD);t['name']='Warm Sunbird nylon guitar - principal melody';t['notes']=[dict(n,velocity=max(50,round(n['velocity']*.86))) for n in t['notes']]
  if t['id']=='pan':t['state_id']='steel_pan_open';t['eq']=[['hp',85,0,1],['bell',2800,-2.3,1.4],['shelf',7200,-1.8,1],['lp',12000,0,.8]]
  if t['id']=='ep':
   for n in t['notes']:n['pitch']-=12
  t['sections']=[]
 tracks['guitar_comp']['notes']=[]
 if cue=='castle':
  # A quiet two-bar guitar greeting before the first full chorus.
  for j in range(2):line(tracks['sunbird'],s['sections'][0]['start_qn']+8+j*4,HOOKS['castle'][j],4,69)
 occurrence=collections.Counter()
 for sec in s['sections']:
  kind=sec['kind'];occurrence[kind]+=1;occ=occurrence[kind];start=sec['start_qn'];length=sec['bars']
  for block in range((length+3)//4):
   lo=start+block*16;hi=min(start+length*4,lo+16);leader=lead;active=set(tracks);light=False
   if cue=='opera_house':
    if kind=='C1':
     if occ==1 and block==0:active-={'congas','maracas','cowbell','timbales','flute_response'};light=True
     if occ==2 and block==1:leader='flute_response'
     if occ==3 and block==0:active-={'ep','cowbell','maracas','flute_response'}
     if occ==4 and block==0:leader='flute_response'
    elif kind=='C2':
     if (occ==1 and block==1) or (occ==2 and block==0) or (occ==3 and block==1):leader='flute_response'
     if occ==3 and block==0:active-={'ep','timbales'};light=True
    elif kind=='V':
     active-={'cowbell','timbales','maracas','flute_response'}
     if occ==1:light=True
     if occ==2 and block==0:active-={'kit','congas','ep'}
     if occ==3 and block==0:leader='flute_response';active.add('flute_response');active-={'kit','ep'}
    elif kind=='break':active={'bass','guitar_comp','ep','congas','timbales'};leader='ep'
   elif cue=='sky_lagoon':
    if kind=='C1':
     if occ==1 and block==0:active-={'kit','bongos','guiro','ep'}
     if occ==2 and block==0:active-={'valiha','guiro'}
     if length==16 and block==2:active-={'ep','kit','bongos','guiro'}
    elif kind=='dialogue':
     leader='valiha'
     if occ==1 and block==0:active={'valiha','udu','guitar_comp'}
     if occ==1 and block==1:active-={'kit','guiro','ep'}
     if occ==2 and block==0:active-={'guitar_comp','ep'}
     if occ==2 and block==1:active-={'kit','guiro'}
    elif kind=='V' and occ==2 and block==1:leader='valiha'
   else:
    if kind=='C1':
     if occ==1 and block==0:active-={'ep','maracas'};light=True
     if occ==2 and block==1:active-={'ep','maracas'}
     if occ==3 and block==0:active-={'kit','maracas'}
     if occ==4:leader='flute_colour';active-={'maracas'}
     if occ==5 and block==0:active-={'ep'}
    if kind=='V':
     active-={'ep','maracas','flute_colour'}
     if occ==1 and block==0:active-={'kit'}
     if occ==2 and block==1:leader='flute_colour';active.add('flute_colour')
   if leader!=lead and leader not in ['ep','valiha']:
    donor=[n for n in tracks[lead]['notes'] if in_block(n,lo,hi)];tracks[lead]['notes']=[n for n in tracks[lead]['notes'] if not in_block(n,lo,hi)]
    dst=tracks[leader];dst['notes']=[n for n in dst['notes'] if not in_block(n,lo,hi)]
    for n in donor:
     m=dict(n);m['velocity']=83
     if cue=='castle':m['pitch']+=12
     dst['notes'].append(m)
    active.add(leader);active.discard(lead)
   elif leader=='valiha' and kind=='V':
    donor=[n for n in tracks[lead]['notes'] if in_block(n,lo,hi)];tracks[lead]['notes']=[n for n in tracks[lead]['notes'] if not in_block(n,lo,hi)];tracks['valiha']['notes']=[n for n in tracks['valiha']['notes'] if not in_block(n,lo,hi)]
    for n in donor:tracks['valiha']['notes'].append(dict(n,velocity=73))
    active.discard(lead)
   for tid,t in tracks.items():
    if tid not in active:t['notes']=[n for n in t['notes'] if not in_block(n,lo,hi)]
    if tid=='kit' and light:t['notes']=[n for n in t['notes'] if not in_block(n,lo,hi) or n['pitch'] in [36,42,44]]
    gain=0 if kind.startswith('C') else -1
    if tid in ['flute_response','flute_colour']:gain=0 if tid==leader else -7
    if tid=='valiha':gain=0 if leader=='valiha' else -12
    if tid=='ep':gain=5 if kind=='break' else -1 if kind.startswith('C') else -6
    if tid=='pan':gain-=1.2
    t['sections'].append(dict(start_qn=lo,gain_db=gain))
   s['phrases'].append(dict(start_qn=lo,bars=(hi-lo)/4,section=sec['name'],leader=leader,active_parts=sorted(active),light_kit=light))
   # Guitar voicings are playable four/five-string shapes with real strum order and breathing rests.
   if 'guitar_comp' in active:
    for local in range(int((hi-lo)/4)):
     at=lo+local*4;bar_index=int((at-start)/4);ch=HARM[cue][kind][bar_index%len(HARM[cue][kind])].split('>')[0];v=VOICINGS[ch]
     if kind=='outro' and bar_index>=2:
      if bar_index==2:
       for k,p in enumerate(v):add(tracks['guitar_comp'],at+k*.022,p,2.8,52+k%2*3)
      continue
     if kind=='V' or (kind=='intro' and cue=='castle'):
      for pos in [0,2]:add(tracks['guitar_comp'],at+pos,v[0],.65,57)
      positions=[1.5,3.5];upper=v[1:]
     else:positions=[.5,2.5] if cue=='castle' else [.75,2.5,3.5];upper=v
     for k,pos in enumerate(positions):
      chord=upper if (bar_index+k)%2==0 else list(reversed(upper))
      for string,p in enumerate(chord):add(tracks['guitar_comp'],at+pos+string*.022,p,.52,57+(2 if k==0 else -2)+string%2*3)
  if cue=='opera_house' and kind=='break':
   tracks['ep']['notes']=[n for n in tracks['ep']['notes'] if not in_block(n,start,start+16)]
   for j in range(2):line(tracks['ep'],start+8+j*4,HOOKS['opera_house'][j],4,77)
 # Sparse rolls preserve the logical tune and use alternating short strikes instead of pitch wobble.
 if cue=='opera_house':
  pan=tracks['pan'];logical=copy.deepcopy(pan['notes']);pan['notes']=[]
  for n in logical:
   q=n['qn'];bar=int((q-4)//4)+1;slot=(q-4)%4;duration=n['duration_qn']
   eligible=duration>=1.2 and (bar%4 in [0,3] or bar>=s['bars']-3)
   if not eligible:pan['notes'].append(dict(n,velocity=round(n['velocity']*.78)));continue
   first=dict(n,duration_qn=.22,velocity=round(n['velocity']*.77));pan['notes'].append(first)
   at=q+.25;strokes=[];i=0
   while at<q+duration-.045:
    v=round(49+8*math.sin(math.pi*(at-q)/duration)+(2 if i%2==0 else -2));dur=min(.085,q+duration-at)
    event=dict(qn=round(at,6),pitch=n['pitch'],duration_qn=round(dur,6),velocity=v);pan['notes'].append(event);strokes.append(event);at+=.125;i+=1
   s['rolls'].append(dict(start_qn=q,pitch=n['pitch'],logical_duration_qn=duration,strokes=len(strokes)+1,roll_interval_qn=.125,rate_hz=round(s['bpm']/60/.125,3),technique='Alternating single-stroke sustained-note roll, soft paired velocities, short release; one pan voice.'))
 for t in s['tracks']:
  t['notes'].sort(key=lambda n:(n['qn'],n['pitch']))
  for i,n in enumerate(t['notes']):
   next_note=next((v for v in t['notes'][i+1:] if v['pitch']==n['pitch'] and v['qn']>n['qn']),None)
   if next_note:n['duration_qn']=round(min(n['duration_qn'],max(.004,next_note['qn']-n['qn']-.003)),6)
  t['native_midi_notes']=len(t['notes']);t['pan']=0;t['stem_file']=cue+'__'+t['id']+'_stem.wav'
 assert sum(t['state_id'].startswith('steel_pan') for t in s['tracks'])==(1 if cue=='opera_house' else 0)
 s['hook_statements_original']=s.pop('hook_statements',[]);s['melody_validation']='Original section order, tune pitches and logical rhythm retained across documented handoffs. Pan roll retriggers subdivide selected sustained notes; Castle flute takes selected phrases one octave higher.'
 s['guitar_voicings']=VOICINGS;s['score_sha256']=hashlib.sha256(json.dumps(s,sort_keys=True).encode()).hexdigest();return s

def main():
 scores=[build(c) for c in ['opera_house','sky_lagoon','castle']]
 for s in scores:
  d=OUT/s['id'];d.mkdir(parents=True,exist_ok=True);(d/'score.json').write_text(json.dumps(s,indent=2)+'\n');(d/(s['id']+'_arrangement.mid')).write_bytes(midi(s))
 (OUT/'performance.lua').write_text('return '+lua(scores)+'\n')
 (OUT/'arrangement_map.json').write_text(json.dumps(dict(stage='WARM_ENSEMBLE_OWNER_REVIEW',owner_direction='Warm guitars and complementary chords; preserve stronger Sky; give Castle more depth; alternating pan rolls/flourishes, less pan dominance and investigate clipping.',reference_form_unchanged=True,original_project_audio_uploaded=False,phrases={s['id']:s['phrases'] for s in scores},pan_rolls=scores[0]['rolls'],guitar_voicings=VOICINGS),indent=2)+'\n')
 print([(s['id'],len(s['tracks']),sum(len(t['notes']) for t in s['tracks']),len(s['rolls'])) for s in scores])
if __name__=='__main__':main()
