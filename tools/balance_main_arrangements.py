"""Measure native EQ stems and choose restrained, reproducible ensemble gains."""
from pathlib import Path
import json,subprocess,re,hashlib,base64,zlib,xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import soundfile as sf
ROOT=Path(__file__).resolve().parents[1];PACKAGE=ROOT/'assets_src/audio/music/arranged_main_themes_20261101';BUILD=ROOT/'build/full_arrangements_20261101'
def measure(path):
 cache=BUILD/(path.stem+'.measure.json')
 fingerprint=hashlib.sha256(path.read_bytes()).hexdigest()
 if cache.exists():
  saved=json.loads(cache.read_text())
  if saved.get('sha256')==fingerprint:return saved['measurement']
 cmd=['ffmpeg','-hide_banner','-nostats','-threads','1','-filter_threads','1','-i',str(path),'-af','loudnorm=I=-18:TP=-3:LRA=11:print_format=json','-f','null','-']
 r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8',errors='replace');assert r.returncode==0,r.stderr[-1000:]
 result=json.loads(re.findall(r'\{[^{}]+\}',r.stderr,re.S)[-1])
 cache.write_text(json.dumps({'sha256':fingerprint,'measurement':result}))
 return result
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def native_state(path):
 b=base64.b64decode(path.read_text())
 for i in range(180,min(450,len(b))):
  try:return ET.fromstring(zlib.decompress(b[i:]))
  except(zlib.error,ET.ParseError):pass
 raise AssertionError('Native state did not decode')
def one(args):
 s,t=args;cue=s['id'];part=t['id'];wav=BUILD/t['stem_file']
 m=measure(wav);a,sr=sf.read(wav,dtype='float32',always_2d=True)
 assert sr==48000 and a.shape[1]==2 and np.isfinite(a).all()
 assert np.max(np.abs(a))<1,(cue,part,'raw clipping')
 assert float(m['input_i'])>-65,(cue,part,'Missing or silent instrument')
 assert abs(len(a)/sr-s['duration_seconds'])<.03
 gain=min(t['target_lufs']-float(m['input_i']),t['peak_cap_db']-float(m['input_tp']))
 native=BUILD/f'{cue}__{part}_rendered.chunk.b64';r=native_state(native)
 progs=list(r.iter('Program'));assert len(progs)==1
 program=progs[0];scripts=list(r.iter('ScriptProcessor'))
 expected={'congas':'7','maracas':'11','valiha':'3'}
 if part in expected:assert any(x.get('KeyswitchSelection')==expected[part] for x in scripts),(part,'Wrong native articulation')
 if part=='sunbird':assert any(x.get('Modes')=='4' for x in scripts),'Sunbird must remain in Solo mode'
 mono=np.mean(a,axis=1);mono_loss=20*np.log10(max(np.sqrt(np.mean(mono.astype('float64')**2)),1e-12)/max(np.sqrt(np.mean(a.astype('float64')**2)),1e-12))
 return {'cue':cue,'part':part,'program':program.get('DisplayName'),'program_path':program.get('ProgramPath'),'raw_lufs':float(m['input_i']),'raw_true_peak_dbtp':float(m['input_tp']),'calibration_gain_db':round(gain,4),'fader_linear':round(10**(gain/20),8),'expected_balanced_lufs':round(float(m['input_i'])+gain,2),'expected_peak_dbtp':round(float(m['input_tp'])+gain,2),'pan':t['pan'],'role':t['role'],'mono_rms_change_db':round(float(mono_loss),3),'wav_sha256':sha(wav),'native_state_sha256':sha(native),'notes':len(t['notes'])}
def main():
 assert (BUILD/'build_stems.result.txt').read_text().strip()=='PASS','Native stems must finish first'
 scores=[json.loads((PACKAGE/cue/'score.json').read_text()) for cue in ['opera_house','sky_lagoon','castle']]
 jobs=[(s,t) for s in scores for t in s['tracks']]
 with ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(one,jobs))
 (PACKAGE/'stem_balance.json').write_text(json.dumps({'status':'PASS','method':'Measured active-gated LUFS plus conservative per-role peak cap; original MIDI dynamics and written sectional gain envelopes retained. These are initial ensemble balances, verified against the full mix next.','stems':results},indent=2)+'\n',encoding='utf-8')
 grouped={}
 for r in results:grouped.setdefault(r['cue'],{})[r['part']]=r['fader_linear']
 text='return {'+','.join(cue+'={'+','.join(k+'='+str(v) for k,v in parts.items())+'}' for cue,parts in grouped.items())+'}\n'
 (BUILD/'mix_gains.lua').write_text(text)
 print(json.dumps([{k:x[k] for k in ['cue','part','raw_lufs','calibration_gain_db','expected_balanced_lufs','expected_peak_dbtp']} for x in results],indent=2))
if __name__=='__main__':main()
