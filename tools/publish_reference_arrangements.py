"""Publish verified reference-led review recordings and portable owner-local REAPER sessions."""
from pathlib import Path
import csv,json,shutil,re,hashlib
import numpy as np
import soundfile as sf
import finish_reference_arrangements as pipeline
import finalize_main_arrangements as final
from balance_main_arrangements import sha
ROOT=pipeline.ROOT;PKG=pipeline.PKG;BUILD=pipeline.BUILD;CUES=pipeline.CUES
OWNER=Path(r'C:\Users\Peter\Documents\REAPER Media\Mermaid Roshan Soundtrack 20261031\Reference Arrangements 20261101')
final.PACKAGE=PKG;final.BUILD=BUILD

def verify_notes():
 assert (BUILD/'verify_reference.result.txt').read_text().strip()=='PASS'
 rows=list(csv.DictReader((BUILD/'native_notes_final.tsv').open(),delimiter='\t'));report=[]
 for s in pipeline.SCORES():
  for t in s['tracks']:
   a=sorted([r for r in rows if r['cue']==s['id'] and r['part']==t['id']],key=lambda r:(float(r['qn']),int(r['pitch'])))
   e=sorted(t['notes'],key=lambda n:(n['qn'],n['pitch']));assert len(a)==len(e)
   for x,y in zip(a,e):
    assert int(x['pitch'])==y['pitch'] and int(x['velocity'])==y['velocity'] and abs(float(x['qn'])-y['qn'])<.0011,(s['id'],t['id'],x,y)
    if t['mix_group'] not in ['kit','percussion']:assert abs(float(x['duration_qn'])-y['duration_qn'])<.0011,(s['id'],t['id'],'Melodic duration mismatch',x,y)
   report.append(dict(cue=s['id'],part=t['id'],notes=len(e),native_state_sha256=sha(BUILD/(s['id']+'__'+t['id']+'_rendered.chunk.b64'))))
  # All eight-bar instances of each refrain must return the same melody/rhythm/velocity.
  motifs={}
  for h in s['hook_statements']:
   notes=next(t for t in s['tracks'] if t['id']==h['track'])['notes'];at=h['start_qn']
   phrase=[dict(qn=round(n['qn']-at,5),pitch=n['pitch'],duration_qn=n['duration_qn'],velocity=n['velocity']) for n in notes if at-1e-7<=n['qn']<at+32-1e-7]
   if h['kind'] in motifs:assert phrase==motifs[h['kind']],(s['id'],'Unstable returning hook')
   else:motifs[h['kind']]=phrase
 return report

def export(results):
 OWNER.mkdir(parents=True,exist_ok=True);receipt=[]
 for s in pipeline.SCORES():
  c=s['id'];d=OWNER/c;(d/'stems').mkdir(parents=True,exist_ok=True);(d/'renders').mkdir(exist_ok=True)
  for src in [PKG/c/(c+'.ogg'),PKG/c/(c+'_master.flac'),PKG/c/'score.json',PKG/c/(c+'_arrangement.mid')]:
   dst=d/src.name;shutil.copy2(src,dst);assert sha(src)==sha(dst)
  mapping={}
  for g in pipeline.GROUPS:
   src=BUILD/(c+'__'+g+'_group.wav');dst=d/'stems'/(g+'.wav');shutil.copy2(src,dst);assert sha(src)==sha(dst);mapping[src.as_posix()]='stems/'+dst.name
  for kind in ['composition','mix']:
   src=BUILD/(c+'_'+kind+'.rpp');text=src.read_text(encoding='utf-8')
   for original,relative in mapping.items():text=text.replace(original,relative).replace(original.replace('/','\\'),relative)
   text=re.sub(r'(?m)^(\s*RENDER_FILE) .*$',lambda m:m[1]+' "'+(d/'renders').as_posix()+'"',text)
   dst=d/src.name;dst.write_text(text,encoding='utf-8')
   for f in re.findall(r'(?m)^\s*FILE "([^"]+)"',text):assert (d/f).is_file(),(dst,f)
  for f in sorted(d.rglob('*')):
   if f.is_file():receipt.append(dict(path=f.relative_to(OWNER).as_posix(),sha256=sha(f),bytes=f.stat().st_size))
 playlist='#EXTM3U\n'+''.join('#EXTINF:'+str(round(r['pcm']['duration_seconds']))+','+r['title']+'\n'+r['id']+'/'+r['id']+'.ogg\n' for r in results)
 (OWNER/'Reference Themes.m3u8').write_text(playlist,encoding='utf-8')
 for c in CUES:playlist=playlist.replace(c+'/'+c+'.ogg','Reference Arrangements 20261101/'+c+'/'+c+'.ogg')
 (OWNER.parent/'Reference Themes.m3u8').write_text(playlist,encoding='utf-8')
 for n in ['reference_map.json','group_balance.json','mix_assessment.json']:
  shutil.copy2(PKG/n,OWNER/n)
 (OWNER/'Start Here.txt').write_text('REFERENCE-LED MAIN THEMES - FULL ARRANGEMENT REVIEW\n\nPlay Reference Themes.m3u8. Each cue has an OGG listening copy and a lossless 24-bit FLAC.\n\nOpera: Harry Belafonte - Jump in the Line (1961).\nSky: Miriam Makeba - Pata Pata (1967 studio recording).\nCastle: Bob Marley & the Wailers - Three Little Birds (Exodus, 1977).\n\nOur original melodies are reshaped into consistent returning refrains. The reference section roles and form guide the arrangements; exact bar lengths, keys and melodic content are our adaptations. See reference_map.json for the complete section and instrument-role map.\n\nThe composition session retains every individual native UVI part, MIDI, EQ and volume automation, routed through five ensemble buses. It requires your installed UVI libraries and authorized Sunbird. The mix session uses five fixed native submix stems: foreground, harmony, bass, drum kit and percussion. These include individual instrument EQ and written sectional automation. Keep the stems folder beside the mix session.\n\nThese are new review versions. Earlier drafts are preserved. Game audio remains unchanged; full-song artistic, phone and voice-over acceptance is still pending.\n',encoding='utf-8')
 (OWNER/'delivery_receipt.json').write_text(json.dumps(dict(status='OWNER_LOCAL_PORTABLE_DELIVERY_VERIFIED',files=receipt),indent=2)+'\n')
 return dict(path=str(OWNER),files=len(receipt),receipt_sha256=sha(OWNER/'delivery_receipt.json'))

def main():
 assert (BUILD/'master_reference.result.txt').read_text().strip()=='PASS'
 assert (BUILD/'castle_codec_headroom.result.txt').read_text().strip()=='PASS'
 notes=verify_notes();results=[final.one(c,"256k","_master_native_safe.wav" if c=="castle" else "_master_native_verified.wav") for c in CUES]
 # Prove lossless export and preserve the independently measured encoded-master evidence.
 for r in results:
  c=r['id'];a,sr=sf.read(BUILD/(c+('_master_native_safe.wav' if c=='castle' else '_master_native_verified.wav')),dtype='float32',always_2d=True);b,br=sf.read(PKG/c/(c+'_master.flac'),dtype='float32',always_2d=True)
  assert a.shape==b.shape and sr==br==48000 and np.max(np.abs(a-b))<=2**-23
 # Compare the exact fixed performances before/after final peak limiting.
 gains={r['cue']:float(r['album_gain_db']) for r in csv.DictReader((BUILD/'native_mastering.tsv').open(),delimiter='\t') if r['project']=='mix'}
 for r in results:
  c=r['id'];version='v4' if c=='castle' else 'v3';before,_=sf.read(BUILD/(c+'_mix_glue_'+version+'.wav'),dtype='float32',always_2d=True);after,_=sf.read(BUILD/(c+('_master_native_safe.wav' if c=='castle' else '_master_native_verified.wav')),dtype='float32',always_2d=True)
  before=before*10**(gains[c]/20);n=len(before)//4800*4800
  rms=lambda a:np.sqrt(np.mean(a[:n].astype('float64').reshape(-1,4800,2)**2,axis=(1,2)))
  x,y=rms(before),rms(after);active=x>10**(-50/20);gr=-20*np.log10(np.maximum(y[active],1e-12)/x[active])
  stats=dict(median_attenuation_db=round(float(np.median(gr)),3),p99_attenuation_db=round(float(np.percentile(gr,99)),3),maximum_window_attenuation_db=round(float(np.max(gr)),3))
  assert stats['median_attenuation_db']<.5 and stats['p99_attenuation_db']<2.5,(c,'Over-limited full mix',stats)
  r['actual_master_limiting']=stats
 delivery=export(results)
 manifest=dict(status='MACHINE_VERIFIED_OWNER_REVIEW_CANDIDATE',external_ai_audio_upload=False,reference_map_sha256=sha(PKG/'reference_map.json'),native_parts=notes,cues=results,delivery=delivery,mastering=dict(target_lufs=-18.25,peak_limit_dbtp=-3,individual_native_eq=True,individual_sectional_automation=True,ensemble_bus_balance='group_balance.json',bus_compression='mix_assessment.json',peak_guard='Native ReaLimit: Opera/Sky threshold=ceiling -3.8 dB; Castle -4.3 dB for lossy-codec headroom; release 15 dB/sec',normalize_after_native_master=False),acceptance_gaps=['Owner hearing: hook clarity, reference suitability, arrangement/orchestration and section identity','Later voice-over, phone, child and runtime integration; no existing game audio replaced'])
 (PKG/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8');shutil.copy2(PKG/'manifest.json',OWNER/'manifest.json');shutil.copy2(BUILD/'native_mastering.tsv',PKG/'native_mastering.tsv')
 print(json.dumps([dict(cue=r['id'],seconds=round(r['pcm']['duration_seconds'],2),lufs=r['native_loudness']['input_i'],true_peak=r['native_loudness']['input_tp']) for r in results],indent=2));print('Owner review:',OWNER)
if __name__=='__main__':main()
