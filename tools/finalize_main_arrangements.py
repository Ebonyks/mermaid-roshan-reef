"""Verify the complete native masters, encode listening copies, and export editable sessions."""
from pathlib import Path
import csv, json, shutil, subprocess, sys, re, base64, zlib
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import soundfile as sf
from balance_main_arrangements import measure, sha, native_state, ROOT, PACKAGE, BUILD
CUES=['opera_house','sky_lagoon','castle']
OWNER=Path(r'C:\Users\Peter\Documents\REAPER Media\Mermaid Roshan Soundtrack 20261031\Full Arrangements 20261101')

def verify_native():
 assert (BUILD/'verify_native_final.result.txt').read_text().strip()=='PASS'
 rows=list(csv.DictReader((BUILD/'native_notes_final.tsv').open(),delimiter='\t'))
 parts=list(csv.DictReader((BUILD/'native_parts_final.tsv').open(),delimiter='\t'))
 balance=json.loads((PACKAGE/'stem_balance.json').read_text())['stems']
 verified=[]
 for cue in CUES:
  s=json.loads((PACKAGE/cue/'score.json').read_text())
  for t in s['tracks']:
   actual=sorted([r for r in rows if r['cue']==cue and r['part']==t['id']],key=lambda x:(float(x['qn']),int(x['pitch'])))
   expected=list(t['notes'])
   if 'keyswitch' in t:expected+=[dict(qn=s['render_start_qn']+.02,duration_qn=.05,pitch=t['keyswitch'],velocity=100)]
   expected.sort(key=lambda x:(x['qn'],x['pitch']));assert len(actual)==len(expected)
   for a,b in zip(actual,expected):
    assert int(a['pitch'])==b['pitch'] and int(a['velocity'])==b['velocity'],(cue,t['id'],a,b)
    assert abs(float(a['qn'])-b['qn'])<.0011 and abs(float(a['duration_qn'])-b['duration_qn'])<.0011
   p=next(r for r in parts if r['cue']==cue and r['part']==t['id']);g=next(r for r in balance if r['cue']==cue and r['part']==t['id'])
   assert abs(float(p['fader'])-g['fader_linear'])<1e-6 and abs(float(p['pan'])-t['pan'])<1e-5
   r=native_state(BUILD/f'{cue}__{t["id"]}_final.chunk.b64');scripts=list(r.iter('ScriptProcessor'))
   if t['id'] in {'congas','maracas','valiha'}:
    want={'congas':'7','maracas':'11','valiha':'3'}[t['id']];assert any(x.get('KeyswitchSelection')==want for x in scripts)
   if t['id']=='sunbird':assert any(x.get('Modes')=='4' for x in scripts)
   verified.append(dict(cue=cue,part=t['id'],notes=len(actual),native_programs=len(list(r.iter('Program'))),native_state_sha256=sha(BUILD/f'{cue}__{t["id"]}_final.chunk.b64')))
 # Independently bind each approved statement to the accepted lead score.
 for cue in CUES:
  s=json.loads((PACKAGE/cue/'score.json').read_text());old=json.loads((PACKAGE/'approved_melodies'/(cue+'.json')).read_text())
  for statement in s['melody_statements']:
   old_start=next(x['start_qn'] for x in old['sections'] if x['theme']==statement['theme'])
   span=8*old['meter'][0]*4/old['meter'][1]
   pickup=.5 if cue=='opera_house' and statement['theme']=='A' else 0
   phrase=[n for n in old['notes'] if old_start-pickup-1e-7<=n['qn']<old_start+span-(.5 if cue=='opera_house' else 0)-1e-7]
   lead=next(t for t in s['tracks'] if t['id']==statement['track'])
   for n in phrase:
    at=statement['start_qn']+n['qn']-old_start
    assert any(abs(x['qn']-at)<1e-5 and x['pitch']==n['pitch'] and x['velocity']==n['velocity'] and x['duration_qn']==n['duration_qn'] for x in lead['notes'])
 return verified

def pcm_checks(path,s):
 a,sr=sf.read(path,dtype='float32',always_2d=True);assert sr==48000 and a.shape[1]==2 and np.isfinite(a).all()
 assert abs(len(a)/sr-s['duration_seconds'])<.035
 peak=float(np.max(np.abs(a)));assert peak<1
 # The written pickup/first note starts after 100 ms; controls must remain silent.
 assert np.max(np.abs(a[:4800]))<.0001,(s['id'],'Unwanted opening control sound')
 end=a[-24000:];tail=20*np.log10(max(float(np.sqrt(np.mean(end.astype('float64')**2))),1e-12))
 assert tail<-65,(s['id'],'Unsettled final tail',tail)
 mono=np.mean(a,axis=1);stereo_rms=np.sqrt(np.mean(a.astype('float64')**2));mono_rms=np.sqrt(np.mean(mono.astype('float64')**2))
 change=20*np.log10(mono_rms/stereo_rms);assert change>-4
 assert np.max(np.abs(np.mean(a,axis=0)))<.001
 return dict(duration_seconds=len(a)/sr,sample_rate=sr,channels=2,frames=len(a),sample_peak_dbfs=round(20*np.log10(peak),3),tail_rms_dbfs=round(tail,3),mono_rms_change_db=round(float(change),3),clipped_samples=int(np.sum(np.abs(a)>=1)),sha256=sha(path))

def one(cue,vorbis_bitrate="128k",native_suffix="_master_native_verified.wav"):
 s=json.loads((PACKAGE/cue/'score.json').read_text());p=BUILD/(cue+native_suffix);data=pcm_checks(p,s);m=measure(p)
 assert -18.5<=float(m['input_i'])<=-17.5,(cue,m)
 assert float(m['input_tp'])<=-3,(cue,m)
 outputs={}
 for ext,codec in [('flac',['-c:a','flac','-sample_fmt','s32','-bits_per_raw_sample','24']),('ogg',['-c:a','libvorbis','-b:a',vorbis_bitrate])]:
  dst=PACKAGE/cue/(cue+('_master' if ext=='flac' else '')+'.'+ext)
  cmd=['ffmpeg','-v','error','-y','-i',str(p),'-map','0:a:0','-ar','48000',*codec,'-metadata','title='+s['title'],'-metadata','artist=Mermaid Roshan Soundtrack','-metadata','album=Reef of Light - Full Theme Review','-metadata','LOOPSTART=0','-metadata','LOOPEND='+str(data['frames']),str(dst)]
  subprocess.run(cmd,check=True);encoded=measure(dst)
  assert -18.5<=float(encoded['input_i'])<=-17.5 and float(encoded['input_tp'])<=-3,(dst,encoded)
  outputs[ext]=dict(path=dst.relative_to(PACKAGE).as_posix(),sha256=sha(dst),bytes=dst.stat().st_size,loudness=encoded)
 return dict(id=cue,title=s['title'],pcm=data,native_loudness=m,outputs=outputs,score_sha256=sha(PACKAGE/cue/'score.json'),composition_sha256=sha(BUILD/(cue+'_composition.rpp')),mix_sha256=sha(BUILD/(cue+'_mix.rpp')))

def export(results):
 OWNER.mkdir(parents=True,exist_ok=True);receipt=[]
 for r in results:
  cue=r['id'];s=json.loads((PACKAGE/cue/'score.json').read_text());d=OWNER/cue;(d/'stems').mkdir(parents=True,exist_ok=True);(d/'renders').mkdir(exist_ok=True)
  for src in [PACKAGE/cue/(cue+'.ogg'),PACKAGE/cue/(cue+'_master.flac'),PACKAGE/cue/'score.json',PACKAGE/cue/(cue+'_arrangement.mid')]:
   shutil.copy2(src,d/src.name);assert sha(src)==sha(d/src.name)
  mapping={}
  for t in s['tracks']:
   src=BUILD/t['stem_file'];dst=d/'stems'/(t['id']+'.wav');shutil.copy2(src,dst);assert sha(src)==sha(dst)
   mapping[src.resolve().as_posix()]=('stems/'+dst.name)
  for kind in ['composition','mix']:
   src=BUILD/(cue+'_'+kind+'.rpp');text=src.read_text(encoding='utf-8')
   for original,relative in mapping.items():text=text.replace(original,relative).replace(original.replace('/','\\'),relative)
   text=re.sub(r'(?m)^(\s*RENDER_FILE) .*$',lambda m:m[1]+' "'+(d/'renders').as_posix()+'"',text)
   dst=d/src.name;dst.write_text(text,encoding='utf-8')
   for media in re.findall(r'(?m)^\s*FILE "([^"]+)"',text):
    ref=d/media;assert ref.is_file(),(dst,media)
   receipt.append(dict(path=dst.relative_to(OWNER).as_posix(),sha256=sha(dst),source_sha256=sha(src),change='Relative printed-stem references and owner render folder; native instruments/effects/MIDI unchanged.'))
  for p in sorted(d.rglob('*')):
   if p.is_file() and p.suffix!='.rpp':receipt.append(dict(path=p.relative_to(OWNER).as_posix(),sha256=sha(p),bytes=p.stat().st_size))
 playlist='#EXTM3U\n'+''.join('#EXTINF:'+str(round(r['pcm']['duration_seconds']))+','+r['title']+'\n'+r['id']+'/'+r['id']+'.ogg\n' for r in results)
 (OWNER/'Main Themes.m3u8').write_text(playlist,encoding='utf-8')
 (OWNER/'Start Here.txt').write_text('MERMAID ROSHAN - FULL THEME ARRANGEMENTS\n\nPlay Main Themes.m3u8 to hear all three complete songs.\nEach song folder contains an OGG listening copy and a 24-bit lossless FLAC master.\nOpen the composition REAPER session to edit notes, UVI instruments, EQ and volume automation. This requires your installed, authorized UVI libraries.\nOpen the mix REAPER session to work with the fixed individual audio performances, balance, room and master chain. The stems include the written volume automation and individual EQ.\nREAPER sessions and stems are together in each song folder; keep the stems folder beside its sessions.\n\nThese are full arrangement review candidates built from your approved melodies. They have not replaced the game audio. Full-song listening, phone/speaker and voice-over checks remain to be accepted.\n\nOnly Opera House uses steel pan, in one part. Sky leads with flute; Castle leads with Sunbird nylon guitar.\n',encoding='utf-8')
 (OWNER/'delivery_receipt.json').write_text(json.dumps(dict(status='LOCAL_EDITABLE_DELIVERY_VERIFIED',files=receipt),indent=2)+'\n',encoding='utf-8')
 return dict(path=str(OWNER),files=len(receipt),receipt_sha256=sha(OWNER/'delivery_receipt.json'))

def main():
 assert (BUILD/'master_songs_verified.result.txt').read_text().strip()=='PASS'
 notes=verify_native()
 with ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(one,CUES))
 delivery=export(results)
 result=dict(status='PASS',stage='FULL_ARRANGEMENT_OWNER_REVIEW',native_host='REAPER / Falcon, owner-local UVI libraries',external_ai_audio_upload=False,master_chain=dict(track_eq='Native ReaEQ with per-role curves in score',room='Quiet filtered shared ReaVerbate return',compressor='ReaComp 1.35:1, attack 30 ms, release 140 ms; measured fixed-performance comparison in mix_assessment.json',album_target_lufs=-18.25,limiter='Native ReaLimit threshold=ceiling=-3.8 dB, release 15 dB/sec; not milliseconds',reaper_normalization=False,codec_normalization=False),melody_preservation='Exact pitches, durations, rhythm and velocities copied from approved A/B phrases; native MIDI verified against complete written score.',native_parts=notes,cues=results,delivery=delivery,acceptance_gaps=['Owner full-song listening and artistic acceptance','Future runtime integration, voice-over/device/child listening; existing game audio unchanged'])
 (PACKAGE/'manifest.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');shutil.copy2(PACKAGE/'manifest.json',OWNER/'manifest.json')
 print(json.dumps([dict(id=r['id'],seconds=r['pcm']['duration_seconds'],lufs=r['native_loudness']['input_i'],true_peak=r['native_loudness']['input_tp'],mono_change=r['pcm']['mono_rms_change_db']) for r in results],indent=2));print('Owner delivery:',OWNER)
if __name__=='__main__':main()
