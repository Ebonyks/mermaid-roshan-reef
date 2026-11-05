"""Publish verified reference-led review recordings and portable owner-local REAPER sessions."""
from pathlib import Path
import csv,json,shutil,re,hashlib
import numpy as np
import soundfile as sf
import finish_warm_ensemble as pipeline
import finalize_main_arrangements as final
from balance_main_arrangements import sha,native_state
ROOT=pipeline.ROOT;PKG=pipeline.PKG;BUILD=pipeline.BUILD;CUES=pipeline.CUES
OWNER=Path(r'C:\Users\Peter\Documents\REAPER Media\Mermaid Roshan Soundtrack 20261031\Warm Ensemble 20261101')
final.PACKAGE=PKG;final.BUILD=BUILD

def verify_tone_sources():
 report=[]
 for score in pipeline.SCORES():
  for t in score['tracks']:
   if t['state_id'] not in ['steel_pan_open','tchad_nylon_warm']:continue
   x=native_state(BUILD/(score['id']+'__'+t['id']+'_rendered.chunk.b64'))
   maximizers=list(x.iter('Maximizer'));assert maximizers and all(e.get('Bypass')=='1' for e in maximizers)
   expected=(1.5,0,-1.5) if t['state_id']=='steel_pan_open' else (1,1,-3)
   eqs=list(x.iter('ThreeBandShelves'));assert any(tuple(float(e.get(k)) for k in ['GainLow','GainMid','GainHigh'])==expected for e in eqs)
   if t['state_id']=='steel_pan_open':assert any(float(e.get('Gain'))==.5 for e in x.iter('Layer'))
   report.append(dict(cue=score['id'],part=t['id'],state=t['state_id'],maximizer_bypassed=True,native_eq_db=list(expected),native_state_sha256=sha(BUILD/(score['id']+'__'+t['id']+'_rendered.chunk.b64'))))
 assert len(report)==4
 doc=json.loads((PKG/'source_tone_controls.json').read_text());doc['status']='VERIFIED_IN_ACTUAL_RENDERED_NATIVE_STATES';doc['rendered_parts']=report
 (PKG/'source_tone_controls.json').write_text(json.dumps(doc,indent=2)+'\n')


def verify_notes():
 assert (BUILD/'verify_warm.result.txt').read_text().strip()=='PASS'
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
  for h in s.get('hook_statements',[]):
   notes=next(t for t in s['tracks'] if t['id']==h['track'])['notes'];at=h['start_qn']
   phrase=[dict(qn=round(n['qn']-at,5),pitch=n['pitch'],duration_qn=n['duration_qn'],velocity=n['velocity']) for n in notes if at-1e-7<=n['qn']<at+32-1e-7]
   if h['kind'] in motifs:assert phrase==motifs[h['kind']],(s['id'],'Unstable returning hook')
   else:motifs[h['kind']]=phrase
 # Preserve the original tune through documented handoffs and roll subdivisions.
 for s in pipeline.SCORES():
  old=json.loads((ROOT/'assets_src/audio/music/reference_arrangements_20261101'/s['id']/'score.json').read_text())
  lead={'opera_house':'pan','sky_lagoon':'flute','castle':'sunbird'}[s['id']]
  foreground=[n for t in s['tracks'] if t['mix_group']=='foreground' for n in t['notes']]
  for n in next(t for t in old['tracks'] if t['id']==lead)['notes']:
   assert any(abs(x['qn']-n['qn'])<1e-5 and (x['pitch']==n['pitch'] or (s['id']=='castle' and x['pitch']==n['pitch']+12)) for x in foreground),(s['id'],'Lost melodic backbone',n)
  for roll in s.get('rolls',[]):
   assert roll['strokes']>=5 and 10<=roll['rate_hz']<=18
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
 (OWNER/'Warm Themes.m3u8').write_text(playlist,encoding='utf-8')
 for c in CUES:playlist=playlist.replace(c+'/'+c+'.ogg','Warm Ensemble 20261101/'+c+'/'+c+'.ogg')
 (OWNER.parent/'Warm Themes.m3u8').write_text(playlist,encoding='utf-8')
 for n in ['arrangement_map.json','steelpan_study.json','source_tone_controls.json','source_tone_measurements.json','group_balance.json','mix_assessment.json','arrangement_density.json','Listening Guide.txt']:
  shutil.copy2(PKG/n,OWNER/n)
 (OWNER/'Start Here.txt').write_text('WARM ENSEMBLE - FULL SONG REVIEW\n\nPlay Warm Themes.m3u8. Each cue includes a full OGG listening copy and a lossless 24-bit FLAC.\n\nComposition sessions retain every native UVI part, MIDI, EQ and sectional automation. Mix sessions use five fixed native submixes; keep their stems folder beside the project. Your installed authorized UVI and Sunbird libraries are required for editable instrument playback.\n\n'+(PKG/'Listening Guide.txt').read_text()+'\n\nEarlier drafts are preserved. Tone, roll realism and artistic acceptance await owner hearing; phone, voice-over and game acceptance remain separate.\n',encoding='utf-8')
 receipt=[dict(path=f.relative_to(OWNER).as_posix(),sha256=sha(f),bytes=f.stat().st_size) for f in sorted(OWNER.rglob('*')) if f.is_file() and f.name not in ['delivery_receipt.json','manifest.json']]
 (OWNER/'delivery_receipt.json').write_text(json.dumps(dict(status='OWNER_LOCAL_PORTABLE_DELIVERY_VERIFIED',files=receipt),indent=2)+'\n')
 return dict(path=str(OWNER),files=len(receipt),receipt_sha256=sha(OWNER/'delivery_receipt.json'))

def main():
 assert (BUILD/'master_warm.result.txt').read_text().strip()=='PASS'
 verify_tone_sources();notes=verify_notes();results=[final.one(c,"256k","_master_native_warm.wav") for c in CUES]
 # Prove lossless export and preserve the independently measured encoded-master evidence.
 for r in results:
  c=r['id'];a,sr=sf.read(BUILD/(c+'_master_native_warm.wav'),dtype='float32',always_2d=True);b,br=sf.read(PKG/c/(c+'_master.flac'),dtype='float32',always_2d=True)
  assert a.shape==b.shape and sr==br==48000 and np.max(np.abs(a-b))<=2**-23
 # Compare the exact fixed performances before/after final peak limiting.
 gains={r['cue']:float(r['album_gain_db']) for r in csv.DictReader((BUILD/'native_mastering.tsv').open(),delimiter='\t') if r['project']=='mix'}
 for r in results:
  c=r['id'];version='v3';before,_=sf.read(BUILD/(c+'_mix_glue_'+version+'.wav'),dtype='float32',always_2d=True);after,_=sf.read(BUILD/(c+'_master_native_warm.wav'),dtype='float32',always_2d=True)
  before=before*10**(gains[c]/20);n=len(before)//4800*4800
  rms=lambda a:np.sqrt(np.mean(a[:n].astype('float64').reshape(-1,4800,2)**2,axis=(1,2)))
  x,y=rms(before),rms(after);active=x>10**(-50/20);gr=-20*np.log10(np.maximum(y[active],1e-12)/x[active])
  stats=dict(median_attenuation_db=round(float(np.median(gr)),3),p99_attenuation_db=round(float(np.percentile(gr,99)),3),maximum_window_attenuation_db=round(float(np.max(gr)),3))
  assert stats['median_attenuation_db']<.5 and stats['p99_attenuation_db']<2.5,(c,'Over-limited full mix',stats)
  r['actual_master_limiting']=stats
 delivery=export(results)
 manifest=dict(status='MACHINE_VERIFIED_OWNER_REVIEW_CANDIDATE',external_ai_audio_upload=False,arrangement_map_sha256=sha(PKG/'arrangement_map.json'),native_parts=notes,cues=results,delivery=delivery,mastering=dict(target_lufs=-18.25,peak_limit_dbtp=-3,individual_native_eq=True,individual_sectional_automation=True,ensemble_bus_balance='group_balance.json',bus_compression='mix_assessment.json',peak_guard='Native ReaLimit: threshold=ceiling -4.8 dB for encoded headroom, release 15 dB/sec; pan preset maximizer bypassed upstream',normalize_after_native_master=False),acceptance_gaps=['Owner hearing: guitar warmth, pan-roll realism, melodic hierarchy, sectional variety, Castle improvement and perceived distortion','Later voice-over, phone, child and runtime integration; no existing game audio replaced'])
 (PKG/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8');shutil.copy2(PKG/'manifest.json',OWNER/'manifest.json');shutil.copy2(BUILD/'native_mastering.tsv',PKG/'native_mastering.tsv')
 print(json.dumps([dict(cue=r['id'],seconds=round(r['pcm']['duration_seconds'],2),lufs=r['native_loudness']['input_i'],true_peak=r['native_loudness']['input_tp']) for r in results],indent=2));print('Owner review:',OWNER)
if __name__=='__main__':main()
