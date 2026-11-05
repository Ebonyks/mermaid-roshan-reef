"""Reference-led instrumental songs: fixed hooks, explicit vocal-form roles and scored rhythm sections."""
from pathlib import Path
import copy,json,hashlib
from compose_main_arrangements import PALETTE,CH,theme,lua,midi,add,line
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets_src/audio/music/reference_arrangements_20261101'
OLD=ROOT/'assets_src/audio/music/arranged_main_themes_20261101'
REFERENCES={
'opera_house':dict(artist='Harry Belafonte',track='Jump in the Line',recording='1961 RCA, Jump Up Calypso',url='https://www.youtube.com/watch?v=dgWXF32nxLs',form_source='https://lyricsweb.com/song/harry-belafonte/harry-belafonte-jump-in-the-line',application='Retain C1 / verse / C2 cycles, the late instrumental break and final return. One steel pan carries the song; flute responses define C2. Separate full-band refrains from lighter guitar/conga verses.'),
'sky_lagoon':dict(artist='Miriam Makeba',track='Pata Pata',recording='1967 original studio recording, stereo version on Strut reissue',url='https://miriammakeba.bandcamp.com/track/pata-pata-stereo-version',form_source='https://journal.ru.ac.za/index.php/africanmusic/article/view/1831',application='Retain a recurring sung-refrain role, a contrasting melodic section and two speech-over-groove interludes, adapted as fixed valiha dialogues. Flute owns every refrain; the plucked rhythm and percussion change function between sections. Role-based adaptation; no claimed exact reference bar transcription.'),
'castle':dict(artist='Bob Marley & the Wailers',track='Three Little Birds',recording='1977 Exodus studio recording',url='https://shop.bobmarley.com/products/exodus-limited-edition-1lp-and-10',form_source='https://charanga.com/file/download?digilearning_support_file_id=19853#page=1',application='Retain intro / chorus / verse / chorus / verse / chorus / chorus / chorus. Sunbird guitar takes the vocal role; offbeat guitar, bass and one-drop drums anchor the verses; electric-piano voicings and shaker define the choruses.')}
FORMS={
'opera_house':[('Chorus 1 - lantern hook',8,'C1'),('Verse 1 - the invitation',8,'V'),('Chorus 2 - the room answers',8,'C2'),('Chorus 1 - lantern hook',8,'C1'),('Verse 2 - footsteps',8,'V'),('Chorus 2 - the room answers',8,'C2'),('Chorus 1 - lantern hook',8,'C1'),('Verse 3 - a new doorway',8,'V'),('Chorus 2 - the room answers',8,'C2'),('Instrumental break - percussion feature',4,'break'),('Chorus 1 - final lantern hook',8,'C1'),('Verse 4 - everyone arrives',8,'V'),('Chorus 2 - full celebration',8,'C2'),('Outro - final curtain',4,'outro')],
'sky_lagoon':[('Intro - plucked invitation',4,'intro'),('Refrain 1 - cloudwater hook',8,'C1'),('Verse 1 - crossing the water',8,'V'),('Refrain 2 - cloudwater hook',8,'C1'),('Dialogue 1 - valiha takes the voice',8,'dialogue'),('Refrain 3 - cloudwater hook',8,'C1'),('Dialogue 2 - rhythmic reply',8,'dialogue'),('Verse 2 - crossing the water',8,'V'),('Final refrain - twice around the clouds',16,'C1'),('Outro - landing',4,'outro')],
'castle':[('Intro - the house groove',4,'intro'),('Chorus 1 - welcome home',8,'C1'),('Verse 1 - through the rooms',8,'V'),('Chorus 2 - welcome home',8,'C1'),('Verse 2 - familiar faces',8,'V'),('Chorus 3 - everyone together',8,'C1'),('Chorus 4 - stronger response',8,'C1'),('Chorus 5 - home at last',8,'C1'),('Outro - lights in the windows',4,'outro')]}
# Every list is eight 4/4 bars. Returning choruses are literal statements, not generated solos.
HOOKS={
'opera_house':[
'A4:0.5 B4:0.5 D5:1.5 B4:0.5 A4:0.5 R:0.5','F#4:1 A4:1 B4:1 A4:0.5 R:0.5',
'A4:0.5 B4:0.5 D5:1.5 B4:0.5 A4:0.5 R:0.5','G4:1 F#4:0.5 E4:0.5 F#4:1 R:1',
'A4:0.5 B4:0.5 D5:1.5 B4:0.5 A4:0.5 R:0.5','F#4:1 A4:1 B4:1 A4:0.5 R:0.5',
'G4:1 B4:0.5 A4:0.5 E4:1 F#4:0.5 R:0.5','D5:1.5 B4:0.5 A4:0.5 F#4:0.5 D4:0.5 R:0.5'],
'sky_lagoon':[
'G4:0.5 D5:0.5 E5:1.5 D5:0.5 B4:0.5 R:0.5','A4:0.5 B4:0.5 D5:1 G4:1.5 R:0.5',
'G4:0.5 D5:0.5 E5:1.5 D5:0.5 B4:0.5 R:0.5','A4:1 G4:1 E4:1 R:1',
'G4:0.5 D5:0.5 E5:1.5 D5:0.5 B4:0.5 R:0.5','A4:0.5 B4:0.5 D5:1 G4:1.5 R:0.5',
'A4:1 B4:0.5 A4:0.5 D5:1 R:1','B4:0.5 A4:0.5 G4:2.5 R:0.5'],
'castle':[
'Bb3:0.5 F4:0.5 G4:1 D4:1 F4:0.5 R:0.5','Eb4:1 D4:0.5 C4:0.5 Bb3:1.5 R:0.5',
'Bb3:0.5 F4:0.5 G4:1 D4:1 F4:0.5 R:0.5','Eb4:1 F4:0.5 G4:0.5 F4:1 R:1',
'Bb3:0.5 F4:0.5 G4:1 D4:1 F4:0.5 R:0.5','Eb4:1 D4:0.5 C4:0.5 Bb3:1.5 R:0.5',
'Eb4:1 G4:0.5 F4:0.5 D4:1 C4:0.5 R:0.5','D4:0.5 C4:0.5 Bb3:2.5 R:0.5']}
ANSWER=['D5:1 F#5:0.5 E5:0.5 D5:0.75 R:1.25','B4:1 A4:0.5 F#4:0.5 E4:0.75 R:1.25']*3+['G4:1 B4:0.5 A4:0.5 E4:0.75 R:1.25','F#4:1 E4:0.5 C#4:0.5 A4:0.75 R:1.25']
VALIHA=['E5:1 G5:0.5 E5:0.5 D5:1 R:1','B4:1 D5:1 G4:1 R:1','E5:1 G5:0.5 E5:0.5 D5:1 R:1','A4:1 B4:1 D5:1 R:1','E5:1 G5:0.5 E5:0.5 D5:1 R:1','B4:1 D5:1 G4:1 R:1','A4:1 B4:0.5 A4:0.5 D5:1 R:1','B4:0.5 A4:0.5 G4:2 R:1']
HARM={
'opera_house':dict(C1=['D6','D6','G6','D6','D6','G6','Em7','A7'],V=['D6','D6','G6','A7','Bm7','G6','Em7>A7','D6'],C2=['G6','D6','G6','D6','Bm7','G6','E7','A7'],outro=['D6','G6','A7','D6'],**{'break':['Bm7','G6','Em7','A7']}),
'sky_lagoon':dict(C1=['Gadd9','Gadd9','Cmaj7','G/B','Em7','Am7','D','Gadd9'],V=['Em7','Cmaj7','Gadd9','D','Em7','Am7','D/F#','D'],dialogue=['Em7','Cmaj7','Am7','D','G/B','Cmaj7','Am7','D'],intro=['Gadd9','D','Cmaj7','D'],outro=['Gadd9','Cmaj7','D','Gadd9']),
'castle':dict(C1=['Bb6','Bb6','Eb6','Bb6','Gm7','Cm7','F7','Bb6'],V=['Eb6','Abmaj7','Eb/G','Cm7','F7','Bb6','Cm7','F7'],intro=['Bb6','Eb6','F7','Bb6'],outro=['Bb6','Eb6','F7','Bb6'])}

def part(id,base=None,**changes):
 t=copy.deepcopy(PALETTE[base or id]);t.update(id=id,notes=[],sections=[],**changes);t.pop('keyswitch',None);return t

def latin(id,selector,pan):
 return part(id,'congas',state_id='latin_'+id,name=id.title()+' - section rhythm',preset='World Suite 3 Latin Percussions / '+id,articulation_selector=selector,pan=pan,role='percussion',eq=[['hp',120,0,1],['bell',3200,-1,1.4],['shelf',8500,-1,1]],room_send_db=-33)

def build(cue):
 old=json.loads((OLD/'approved_melodies'/(cue+'.json')).read_text());bpm={'opera_house':112,'sky_lagoon':112,'castle':92}[cue]
 lead={'opera_house':'pan','sky_lagoon':'flute','castle':'sunbird'}[cue]
 ts={lead:part(lead), 'guitar_comp':part('guitar_comp'), 'bass':part('bass','jazz_bass' if cue=='castle' else 'cuba_bass'), 'ep':part('ep'), 'kit':part('kit','brushes',name='Drum kit - written groove and fills')}
 if cue=='opera_house':ts.update(flute_response=part('flute_response','flute',role='response',name='Flute - chorus-two responses',pan=.18),congas=part('congas',state_id='latin_congas',articulation_selector=7),maracas=part('maracas',state_id='latin_maracas',articulation_selector=11),cowbell=latin('cowbell',8,.22),timbales=latin('timbales',15,-.15))
 if cue=='sky_lagoon':ts.update(valiha=part('valiha',role='section_lead'),udu=part('udu'),bongos=latin('bongos',3,.18),guiro=latin('guiro',10,-.2))
 if cue=='castle':ts.update(maracas=part('maracas',state_id='latin_maracas',articulation_selector=11))
 s=dict(id=cue,title={'opera_house':'The Curtain Opens - Calypso Revue','sky_lagoon':'Cloudwater Dance','castle':'Welcome Home - Tide Song'}[cue],key=old['key'],bpm=bpm,meter=[4,4],beats_per_bar=4,bars=sum(x[1] for x in FORMS[cue]),tail_seconds=6,tracks=list(ts.values()),sections=[],reference=REFERENCES[cue],composition_start_qn=4,render_start_qn=3.75,hook_statements=[],melody_statements=[],references=[REFERENCES[cue]['url']],prior_melody_sha256=hashlib.sha256((OLD/'approved_melodies'/(cue+'.json')).read_bytes()).hexdigest())
 bar=1;verse=theme(old,'A' if cue=='opera_house' else 'B');scale=4/(old['meter'][0]*4/old['meter'][1])
 # Group membership determines printed submixes; the native session keeps every individual part editable.
 for t in ts.values():
  t['mix_group']='foreground' if t['id']==lead or t['id']=='valiha' else 'bass' if t['id']=='bass' else 'kit' if t['id']=='kit' else 'percussion' if t['role']=='percussion' else 'harmony'
 for si,(name,length,kind) in enumerate(FORMS[cue]):
  start=4+(bar-1)*4;chorus=kind.startswith('C');last=si>=len(FORMS[cue])-4
  foreground='valiha' if kind=='dialogue' else lead if kind not in ['intro','break'] else 'rhythm ensemble'
  sec=dict(name=name,start_bar=bar,bars=length,kind=kind,start_qn=start,foreground=foreground,layer_identity='Full electric-piano / percussion refrain' if chorus else 'Plucked verse rhythm' if kind=='V' else 'Named instrumental handoff')
  s['sections'].append(sec)
  for t in ts.values():
   gain=(.4 if last else 0) if chorus else -1 if kind=='V' else -2
   if t['id']=='valiha':gain=0 if kind=='dialogue' else -12
   if t['id']=='ep':gain=0 if chorus else -7
   t['sections'].append(dict(start_qn=start,gain_db=gain))
  if chorus:
   pattern=ANSWER if kind=='C2' else HOOKS[cue]
   for j in range(length):line(ts[lead],start+j*4,pattern[j%8],4,92 if kind=='C1' else 90)
   for j in range(0,length,8):s['hook_statements'].append(dict(kind=kind,start_qn=start+j*4,track=lead,bars=8))
  elif kind=='V':
   for n in verse:
    q=start+n['qn']*scale
    if q<start:continue
    add(ts[lead],q,n['pitch'],n['duration_qn']*scale,min(94,n['velocity']+3))
   s['melody_statements'].append(dict(theme='prior A' if cue=='opera_house' else 'prior B',start_qn=start,track=lead,scale_qn=scale))
  elif kind=='dialogue':
   for j,pattern in enumerate(VALIHA):line(ts['valiha'],start+j*4,pattern,4,77,.88)
  elif kind=='outro':
   for j in range(2):line(ts[lead],start+j*4,HOOKS[cue][j],4,84)
   tonic={'opera_house':74,'sky_lagoon':67,'castle':58}[cue];add(ts[lead],start+8,tonic,3.3,81)
  for local in range(length):
   at=start+local*4;ch=HARM[cue][kind][local%len(HARM[cue][kind])].split('>')[0];root,voicing=CH[ch];stopping=kind=='outro' and local>=2
   # One bass phrase per two-bar cell, with a directed approach only at section cadences.
   if not stopping:
    rhythm=([0,1.5,2.75,3.5] if chorus else [0,2.5,3.5]) if cue=='opera_house' else ([0,1.75,2.5,3.5] if chorus else [0,2.5]) if cue=='sky_lagoon' else [0,1.5,2.75,3.5]
    if kind=='break':rhythm=[0,2.5]
    for k,pos in enumerate(rhythm):
     note=root if k in [0,2] else root+7 if root+7<=50 else root-5
     if pos==3.5 and local==length-1:note=CH[HARM[cue][FORMS[cue][min(si+1,len(FORMS[cue])-1)][2]][0].split('>')[0]][0]-1
     add(ts['bass'],at+pos+.009,note,.32 if pos>=2.75 else .66,79 if k==0 else 70)
   elif local==2:add(ts['bass'],at,root,3.2,68)
   # Chordal rhythm has a stable, recognizable offbeat role rather than an independent melodic noodle.
   if not stopping:
    positions=[.5,1.5,2.5,3.5] if cue=='castle' else [.75,2,3.5] if cue=='opera_house' else [.5,1.5,2.75]
    if kind=='break':positions=[0,3.5]
    for k,pos in enumerate(positions):
     for p in voicing:add(ts['guitar_comp'],at+pos+(p%3)*.009,p,.23 if cue=='castle' else .37,65 if chorus else 60)
    # Piano belongs to choruses; verses retain only a cadential response.
    if chorus or kind=='intro' or local==length-1:
     for pos in ([0,2.5] if chorus else [2.5]):
      for p in voicing:add(ts['ep'],at+pos+.015,p+12,.7 if chorus else .45,67 if chorus else 54)
   # A complete drum part: kick/snare relationship, small subdivision accents, actual section fills.
   if not stopping:
    kit=ts['kit'];kick=[0,2,3.5] if cue=='opera_house' else [0,2.5] if cue=='sky_lagoon' else [2]
    snare=[1,3] if cue!='castle' else [2]
    if kind=='intro' and local<2:kick=[0];snare=[]
    if kind=='break':kick=[0,2];snare=[1,3]
    for pos in kick:add(kit,at+pos,36,.1,77 if chorus else 68)
    for pos in snare:add(kit,at+pos+.012,38 if chorus else 37,.14,75 if chorus else 64)
    for k in range(8):add(kit,at+k*.5+.006,46 if chorus and k==7 and local%2==1 else 42,.08,53 if k%2 else 39)
    if local==length-1 and si<len(FORMS[cue])-1:
     for k,p in enumerate([38,40,47,45]):add(kit,at+3+k*.25+.004,p,.1,53+k*5)
    if chorus and local%4==0:add(kit,at,51,.2,45)
   elif local==2:add(ts['kit'],at,51,.35,41)
   if cue=='opera_house' and not stopping:
    # Conga open/slap/ghost pattern talks to the bass anticipations across a two-bar cell.
    patt=[(0,48,63),(.75,50,43),(1.5,53,75),(2,48,54),(2.75,55,65),(3.5,53,76)] if local%2==0 else [(0,48,59),(.5,50,46),(1.5,53,70),(2.5,55,72),(3.25,50,45),(3.5,53,79)]
    if kind=='break':patt=[(k*.5,48 if k%2==0 else 53,65+k%3*7) for k in range(8)]
    for pos,p,v in patt:add(ts['congas'],at+pos+.008,p,.13,v)
    if chorus:
     for k in range(8):add(ts['maracas'],at+k*.5+.01,60 if k%2==0 else 62,.12,51 if k%2 else 39)
    if kind=='C1':
     for pos in ([0,1.5,2.5] if local%2==0 else [1,2]):add(ts['cowbell'],at+pos+.005,49,.14,58)
    if kind=='C2' or kind=='break' or local==length-1:
     for pos,p in [(2.75,48),(3.25,50),(3.5,53),(3.75,55)]:add(ts['timbales'],at+pos,p,.11,57 if kind!='break' else 67)
    if kind=='C2':
     for pos,p in [(2.9,74),(3.4,71),(3.7,69)]:add(ts['flute_response'],at+pos,p,.19,76)
   if cue=='sky_lagoon' and not stopping:
    if kind!='dialogue':
     for k,pos in enumerate([0,1.5,2.75]):add(ts['valiha'],at+pos,voicing[(local+k)%3]+12,.39,62)
    for pos,p in [(0,48),(1.5,53),(2.75,48)]:add(ts['udu'],at+pos+.012,p,.17,62 if chorus else 52)
    for pos,p,v in [(0.75,48,59),(1.75,50,69),(2.5,53,61),(3.5,55,72)]:add(ts['bongos'],at+pos+.006,p,.13,v if chorus else v-8)
    if chorus or kind=='dialogue':
     for pos,p,v in [(0.5,60,58),(1,61,48),(2.5,60,58),(3,61,48)]:add(ts['guiro'],at+pos,p,.17,v)
   if cue=='castle' and chorus and not stopping:
    for k in range(8):add(ts['maracas'],at+k*.5+.009,60 if k%2 else 62,.12,41 if k%2 else 32)
   if stopping and local==2:
    for tname in ['guitar_comp','ep']:
     for p in voicing:add(ts[tname],at,p+(12 if tname=='ep' else 0),3,57)
  bar+=length
 s['music_end_qn']=4+s['bars']*4;s['duration_seconds']=(s['music_end_qn']-s['render_start_qn'])*60/bpm+6
 for t in s['tracks']:
  t['notes'].sort(key=lambda n:(n['qn'],n['pitch']))
  # De-overlap rearticulated notes of the same pitch: native note-off pairing must agree with the written score.
  for i,n in enumerate(t['notes']):
   nxt=next((x for x in t['notes'][i+1:] if x['pitch']==n['pitch'] and x['qn']>n['qn']),None)
   if nxt:n['duration_qn']=round(min(n['duration_qn'],max(.025,nxt['qn']-n['qn']-.012)),6)
  t['native_midi_notes']=len(t['notes']);t['stem_file']=cue+'__'+t['id']+'_stem.wav'
  t['pan']=0 # Individual prints are centered; the five ensemble buses provide the documented stereo placement.
  t['ensemble_pan']={'foreground':0,'harmony':-.16,'bass':0,'kit':0,'percussion':.16}[t['mix_group']]
  t['target_lufs']=-22 if t['mix_group']=='foreground' else -28;t['peak_cap_db']=-9 if t['mix_group']=='foreground' else -15
 assert sum(t['state_id']=='steel_pan_main' for t in s['tracks'])==(1 if cue=='opera_house' else 0)
 s['mastering_plan']=dict(target_lufs=-18.25,maximum_true_peak_dbtp=-3,approval='Reference-led review adaptation; no new melody or full mix is owner-accepted.',normalization='Native controlled gain plus light peak protection; final codec files measured independently.')
 s['score_sha256']=hashlib.sha256(json.dumps(s,sort_keys=True).encode()).hexdigest();return s

def main():
 OUT.mkdir(parents=True,exist_ok=True);scores=[build(c) for c in FORMS]
 for s in scores:
  p=OUT/s['id'];p.mkdir(exist_ok=True);(p/'score.json').write_text(json.dumps(s,indent=2)+'\n',encoding='utf-8');(p/(s['id']+'_arrangement.mid')).write_bytes(midi(s))
 (OUT/'performance.lua').write_text('return '+lua(scores)+'\n',encoding='utf-8')
 (OUT/'reference_map.json').write_text(json.dumps(dict(stage='REFERENCE_LED_ARRANGEMENT_REVIEW',owner_corrections=['Opera strongest; preserve its identity.','Specific reference songs, distinct verse/chorus forms and instrument changes required.','Original project melodies lightly reshaped into fixed hooks; do not copy the reference melodies.'],reference_scope='Section identities/order and ensemble functions; our bar counts, keys and melodic content are adaptations, not a verified bar-for-bar transcription.',references=REFERENCES,forms=[{k:s[k] for k in ['id','title','bpm','bars','duration_seconds','sections']} for s in scores],uvi_only=True,external_ai_audio_upload=False,no_runtime_replacement=True),indent=2)+'\n',encoding='utf-8')
 print(json.dumps([dict(cue=s['id'],title=s['title'],bars=s['bars'],seconds=round(s['duration_seconds'],2),parts=len(s['tracks']),notes=sum(len(t['notes']) for t in s['tracks'])) for s in scores],indent=2))
if __name__=='__main__':main()
