"""Measure reference-song submixes and verify complete arrangements without uploading audio."""
from pathlib import Path
import json,sys,hashlib,csv,subprocess,shutil,re
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import soundfile as sf
import balance_main_arrangements as core
from compose_main_arrangements import lua
ROOT=Path(__file__).resolve().parents[1];PKG=ROOT/'assets_src/audio/music/warm_ensemble_20261101';BUILD=ROOT/'build/warm_ensemble_20261101';core.BUILD=BUILD
CUES=['opera_house','sky_lagoon','castle'];GROUPS=['foreground','harmony','bass','kit','percussion']
TARGETS={'foreground':(-21.5,-8.5),'harmony':(-27.5,-14),'bass':(-26.5,-13),'kit':(-26.5,-10),'percussion':(-29.5,-12)}
PAN={'foreground':0,'harmony':-.16,'bass':0,'kit':0,'percussion':.16}
ROOM={'foreground':-22,'harmony':-28,'bass':-60,'kit':-34,'percussion':-34}
SCORES=lambda:[json.loads((PKG/c/'score.json').read_text()) for c in CUES]

def pcm(path,duration):
 a,sr=sf.read(path,dtype='float32',always_2d=True);assert sr==48000 and a.shape[1]==2 and np.isfinite(a).all();assert abs(len(a)/sr-duration)<.035
 assert np.max(np.abs(a))<.99999,(path,'Raw clipping: reduce part gain and reprint')
 return a

def group_one(args):
 s,g=args;p=BUILD/(s['id']+'__'+g+'_group.wav');a=pcm(p,s['duration_seconds']);m=core.measure(p);i=float(m['input_i']);tp=float(m['input_tp']);assert i>-60
 target,cap=TARGETS[g];gain=min(target-i,cap-tp)
 return dict(cue=s['id'],group=g,lufs=i,true_peak_dbtp=tp,gain_db=round(gain,4),fader=round(10**(gain/20),8),balanced_lufs=round(i+gain,3),balanced_peak=round(tp+gain,3),pan=PAN[g],room_send_db=ROOM[g],sha256=core.sha(p))

def groups():
 assert (BUILD/'build_warm.result.txt').read_text().strip()=='PASS'
 scores=SCORES()
 # Validate exposed vendor articulation and program mode from the actual rendered native states.
 for s in scores:
  for t in s['tracks']:
   x=core.native_state(BUILD/(s['id']+'__'+t['id']+'_rendered.chunk.b64'));assert len(list(x.iter('Program')))==1
   scripts=list(x.iter('ScriptProcessor'))
   if t.get('articulation_selector'):assert any(p.get('KeyswitchSelection')==str(t['articulation_selector']) for p in scripts),(s['id'],t['id'],'Wrong native instrument articulation')
   if t['id']=='sunbird':assert any(p.get('Modes')=='4' for p in scripts)
 with ThreadPoolExecutor(max_workers=3)as pool:rows=list(pool.map(group_one,[(s,g) for s in scores for g in GROUPS]))
 (PKG/'group_balance.json').write_text(json.dumps(dict(status='PASS',method='Five printed native submixes retain all individually EQed/automated parts. Calibrated foreground, harmony, bass, kit and percussion targets; transient caps preserve a clear melodic hierarchy.',groups=rows),indent=2)+'\n')
 gains={c:{r['group']:r['fader'] for r in rows if r['cue']==c} for c in CUES};(BUILD/'group_gains.lua').write_text('return '+lua(gains)+'\n')
 (BUILD/'groups.lua').write_text('return '+lua([dict(id=g,name=g.title()+' - native ensemble print',mix_group=g,pan=PAN[g],room_send_db=ROOM[g]) for g in GROUPS])+'\n')
 print(json.dumps([dict(cue=r['cue'],group=r['group'],lufs=r['balanced_lufs'],peak=r['balanced_peak']) for r in rows],indent=2))

def assess_one(c):
 version='v3';raw=BUILD/(c+'_mix_raw_'+version+'.wav');glue=BUILD/(c+'_mix_glue_'+version+'.wav');s=next(s for s in SCORES() if s['id']==c)
 a=pcm(raw,s['duration_seconds']);b=pcm(glue,s['duration_seconds']);n=len(a)//4800*4800
 rms=lambda v:np.sqrt(np.mean(v[:n].astype('float64').reshape(-1,4800,2)**2,axis=(1,2)))
 x,y=rms(a),rms(b);active=x>10**(-50/20);gr=-20*np.log10(np.maximum(y[active],1e-12)/x[active]);assert np.percentile(gr,99)<2.5
 m=core.measure(glue);gain=round(-18.25-float(m['input_i']),4);guard=max(0,float(m['input_tp'])+gain+4.8)
 assert guard<5.5,(c,'Mix transient needs correction before mastering',guard) # Final acceptance measures actual fixed-performance limiting, not just this maximum-peak estimate.
 return dict(id=c,loudness=m,master_gain_db=gain,predicted_peak_guard_db=round(guard,3),compression_median_db=round(float(np.median(gr)),3),compression_p99_db=round(float(np.percentile(gr,99)),3),raw_sha256=core.sha(raw),glue_sha256=core.sha(glue))

def assess():
 assert (BUILD/'mix_warm.result.txt').read_text().strip()=='PASS'
 with ThreadPoolExecutor(max_workers=3)as pool:rows=list(pool.map(assess_one,CUES))
 (PKG/'mix_assessment.json').write_text(json.dumps(dict(status='PASS',cues=rows),indent=2)+'\n');(BUILD/'master_gains.lua').write_text('return '+lua({r['id']:r['master_gain_db'] for r in rows})+'\n');print(json.dumps(rows,indent=2))

if __name__=='__main__':{'groups':groups,'assess':assess}[sys.argv[1]]()
