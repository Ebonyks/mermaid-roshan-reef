#!/usr/bin/env python3
"""Preserve aggregate MIDI event facts and compare bounded tonal sequences.

Inputs are private cached references; this tool neither downloads nor publishes music.
Opening-fit controls and frozen-fit later-section checks are diagnostic.
Runtime, timbre and human musical acceptance are separate.
"""
import sys,json,hashlib,collections,math,datetime
from pathlib import Path
import numpy as np,soundfile as sf
from scipy import signal,ndimage
import argparse
p=argparse.ArgumentParser(description='Offline DKC note/control and bounded audio-chroma diagnostics; not a fidelity score.')
p.add_argument('--study-dir',type=Path,required=True,help='Private acquisition directory containing audio_manifest.json and midi_inputs.json')
p.add_argument('--catalog',type=Path,default=Path(__file__).resolve().parents[2]/'design/music/dkc/soundtrack_catalog.json')
p.add_argument('--mido-path',type=Path,help='Optional existing isolated mido package directory')
args=p.parse_args()
R=args.study_dir.resolve();D=args.catalog.parent
if args.mido_path:sys.path.insert(0,str(args.mido_path))
import mido
DT=.2
def parse(e):
 mf=mido.MidiFile(e['path']);tm=0.;tempo=500000;program=collections.defaultdict(int);active=collections.defaultdict(list);notes=[];channels={};events=collections.Counter();tempos=[]
 for msg in mido.merge_tracks(mf.tracks):
  tm+=mido.tick2second(msg.time,mf.ticks_per_beat,tempo);events[msg.type]+=1
  if msg.type=='set_tempo':tempo=msg.tempo;tempos.append([round(tm,4),round(mido.tempo2bpm(tempo),4)])
  if not hasattr(msg,'channel'):continue
  ch=msg.channel
  if ch not in channels:channels[ch]=dict(channel_one_based=ch+1,programs_zero_based=[],controllers={},pitch_bend_events=0,notes=[])
  c=channels[ch]
  if msg.type=='program_change':program[ch]=msg.program;c['programs_zero_based'].append(msg.program)
  elif msg.type=='control_change':c['controllers'][str(msg.control)]=c['controllers'].get(str(msg.control),0)+1
  elif msg.type=='pitchwheel':c['pitch_bend_events']+=1
  if msg.type=='note_on' and msg.velocity>0:active[ch,msg.note].append((tm,msg.velocity,program[ch]))
  elif msg.type=='note_off' or (msg.type=='note_on' and msg.velocity==0):
   if active[ch,msg.note]:
    start,vel,pr=active[ch,msg.note].pop(0);n=dict(start=start,end=tm,pitch=msg.note,velocity=vel,channel=ch,program=pr);notes.append(n);c['notes'].append(n)
 dangling=sum(map(len,active.values()))
 for c in channels.values():
  ns=c.pop('notes');c['programs_zero_based']=sorted(set(c['programs_zero_based']));c['note_ons_paired']=len(ns)
  c['note_range']=[min(n['pitch'] for n in ns),max(n['pitch'] for n in ns)] if ns else None
  c['velocity_range']=[min(n['velocity'] for n in ns),max(n['velocity'] for n in ns)] if ns else None
  c['first_note_seconds']=round(min(n['start'] for n in ns),4) if ns else None;c['last_release_seconds']=round(max(n['end'] for n in ns),4) if ns else None
  c['median_note_duration']=round(float(np.median([n['end']-n['start'] for n in ns])),4) if ns else None
  c['notes_below_midi_48']=sum(n['pitch']<48 for n in ns);c['nonzero_note_ons']=sum(n['velocity']>0 for n in ns)
 return dict(url=e['url'],name=e['name'],sha256=e['sha256'],duration_seconds=round(tm,4),ticks_per_beat=mf.ticks_per_beat,track_names=[t.name for t in mf.tracks if t.name],tempo_changes=tempos,event_counts=dict(events),unclosed_notes=dangling,channels=list(channels.values()),note_count=len(notes)),notes
def midi_chroma(notes,length):
 M=np.zeros((12,int(length/DT)+2),dtype=np.float32)
 for n in notes:
  if n['channel']==9:continue
  a=max(0,int(n['start']/DT));b=min(M.shape[1],max(a+1,int(n['end']/DT)))
  M[n['pitch']%12,a:b]+=math.sqrt(n['velocity']/127)
 return M
def audio_chroma(path):
 y,sr=sf.read(path);y=y[:int(100*sr)]
 f,t,z=signal.stft(y,fs=sr,nperseg=8192,noverlap=8192-int(sr*DT),boundary='zeros')
 S=np.abs(z);smooth=ndimage.median_filter(S,size=(17,1));S=np.maximum(S-smooth,0)**.6
 C=np.zeros((12,len(t)),np.float32)
 good=(f>=55)&(f<=4000);p=np.rint(69+12*np.log2(np.maximum(f,1)/440)).astype(int)
 for k in range(12):C[k]=S[good & (p%12==k)].sum(axis=0)
 return C
def norm(C):
 c=C-C.mean(axis=0,keepdims=True);return c/(np.linalg.norm(c,axis=0,keepdims=True)+1e-9)
def fit(A,M,scales=None):
 # A bounded opening excerpt, not an unconstrained whole-song DTW.
 a=norm(A);time=np.arange(min(a.shape[1],int(65/DT)))*DT;a=a[:,:len(time)]
 best=(-2,None,None,0)
 for scale in (scales if scales is not None else np.arange(.7,1.51,.025)):
  for offset in np.arange(-4,8.01,.4):
   ix=np.rint((time-offset)/scale/DT).astype(int);valid=(ix>=0)&(ix<M.shape[1])
   if valid.mean()<.85:continue
   m=norm(M[:,np.clip(ix,0,M.shape[1]-1)])
   usable=valid & (np.linalg.norm(m,axis=0)>.5)&(np.linalg.norm(a,axis=0)>.5)
   if usable.sum()<min(10,len(time)*.4):continue
   score=float(np.mean(np.sum(a[:,usable]*m[:,usable],axis=0)))
   if score>best[0]:best=(score,float(scale),float(offset),int(usable.sum()))
 return dict(centered_chroma_similarity=round(best[0],4),midi_seconds_to_audio_scale=best[1],audio_offset_seconds=best[2],compared_frames=best[3])
def main():
 inputs=json.loads((R/'midi_inputs.json').read_text());audio=json.loads((R/'audio_manifest.json').read_text());cat=json.loads((D/'soundtrack_catalog.json').read_text())
 logs=[];cache={}
 for e in inputs:
  if not e.get('parsed'):continue
  try:
   log,notes=parse(e);logs.append(log);cache[e['url']]=(log,midi_chroma(notes,min(210,max(1,log['duration_seconds']))))
  except Exception as ex:logs.append(dict(url=e['url'],error=str(ex)))
 (R/'midi_event_summaries.json').write_text(json.dumps(logs,indent=2))
 features={a['id']:audio_chroma(a['path']) for a in audio if a['status']=='ACQUIRED'}
 rows=[]
 rng=np.random.default_rng(20261102)
 for tr in cat['tracks']:
  id=tr['id'];A=features.get(id);candidates=[]
  for e in tr['midi_files']:
   if e['url'] not in cache or A is None:continue
   log,M=cache[e['url']]
   # Reject declared remixes from structural ranking; retain their logs.
   if any(w in e['name'].lower() for w in ['remix','arranged','orchestrated']):continue
   result=fit(A,M)
   candidates.append(dict(url=e['url'],name=e['name'],sha256=log['sha256'],note_count=log['note_count'],channels=len(log['channels']),**result))
  candidates.sort(key=lambda x:x['centered_chroma_similarity'],reverse=True)
  unique=[];seen=set()
  for c in candidates:
   if c['sha256'] in seen:continue
   seen.add(c['sha256']);log,M=cache[c['url']]
   times=np.arange(A.shape[1])*DT;mask=times>=65;scale=c['midi_seconds_to_audio_scale'];off=c['audio_offset_seconds']
   if scale is not None and mask.sum()>10:
    ix=np.rint((times-off)/scale/DT).astype(int);valid=mask&(ix>=0)&(ix<M.shape[1]);a=norm(A);b=norm(M[:,np.clip(ix,0,M.shape[1]-1)]);valid&=(np.linalg.norm(a,axis=0)>.5)&(np.linalg.norm(b,axis=0)>.5)
    c['held_out_65_to_100s']=dict(similarity=round(float(np.mean(np.sum(a[:,valid]*b[:,valid],axis=0))),4) if valid.sum() else None,frames=int(valid.sum()),offset_and_scale_frozen=True)
   else:c['held_out_65_to_100s']=dict(similarity=None,frames=0,reason='Reference or alignment too short')
   unique.append(c)
  candidates=unique
  row=dict(id=id,title=tr['title'],candidates=candidates)
  if candidates:
   log,M=cache[candidates[0]['url']];shuffle=M[:,rng.permutation(M.shape[1])]
   others=[k for k in features if k!=id and features[k].shape[1]>100]
   wrong=features[others[(int(id[-2:])+3)%len(others)]]
   row['controls']=dict(shuffled_note_order=fit(A,shuffle),wrong_original=fit(wrong,M),transposed_five_semitones=fit(A,np.roll(M,5,axis=0)))
   row['working_selection']=candidates[0]['url'];row['interpretation']='Preferred starting transcription by opening tonal/timing diagnostic; listening and part corrections govern use.'
  else:row['interpretation']='Use original audio and a provisional role/timeline interpretation; missing MIDI does not block arranging decisions.'
  rows.append(row);print('COMPARE',id,len(candidates),candidates[0]['centered_chroma_similarity'] if candidates else '-',flush=True)
 controls=[]
 for scale in [1.0,1.2]:
  M=np.zeros((12,250),np.float32)
  for i in range(25):M[(i*7+i//3)%12,i*10:(i+1)*10]=1
  A=np.stack([np.interp(np.arange(250)/scale,np.arange(250),r) for r in M])
  same=fit(A,M);wrong=fit(A,np.roll(M,5,axis=0))
  controls.append(dict(actual_scale=scale,matched=same,transposed=wrong,pass_test=same['centered_chroma_similarity']>wrong['centered_chroma_similarity']+.2 and abs(same['midi_seconds_to_audio_scale']-scale)<.06))
 assert all(c['pass_test'] for c in controls),controls
 result=dict(schema='dkc-midi-original-stress/1',checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),method='Whitened STFT chroma versus tempo-decoded note-duration chroma; bounded scale .7–1.5 and offset -4–8s; first <=65s; no drum-channel notes. Candidate ranking only, not percentage fidelity.',limits=['No timbre equivalence measurement','MIDI sustain pedal, effects and pitch bends summarized but not synthesized in chroma','Percussion, intros, loops and tuning can reduce discrimination','Controls intentionally permit a wrong original to expose false positives; no pass threshold manufactured'],synthetic_controls=controls,tracks=rows)
 for tr in result['tracks']:
  for c in tr['candidates']:
   if c['centered_chroma_similarity']<-1:c['centered_chroma_similarity']=None;c['measurement_status']='NO_VALID_ALIGNMENT'
  for c in tr.get('controls',{}).values():
   if c['centered_chroma_similarity']<-1:c['centered_chroma_similarity']=None;c['measurement_status']='NO_VALID_ALIGNMENT'
 result['holdout_method']='65–100 seconds, opening offset and scale frozen; candidate mirrors deduplicated by SHA-256.'
 (R/'comparison_results.json').write_text(json.dumps(result,indent=2));print('DONE',len(logs),'MIDI logs',len(rows),'rows',flush=True)
if __name__=='__main__':main()
