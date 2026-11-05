"""Assess full native mixes and select transparent mastering gain/peak protection."""
from pathlib import Path
import json,sys
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import soundfile as sf
from balance_main_arrangements import measure,ROOT,PACKAGE,BUILD

def one(cue):
 raw=BUILD/(cue+'_mix_raw_v2.wav');glue=BUILD/(cue+'_mix_glue_v2.wav')
 a,sr=sf.read(raw,dtype='float32',always_2d=True);b,bsr=sf.read(glue,dtype='float32',always_2d=True)
 assert sr==bsr==48000 and a.shape==b.shape
 assert np.isfinite(b).all() and np.max(np.abs(b))<1
 # RMS windows compare the exact same fixed native performances, not different round robins.
 n=(len(a)//4800)*4800
 x=np.sqrt(np.mean(a[:n].astype('float64').reshape(-1,4800,2)**2,axis=(1,2)))
 y=np.sqrt(np.mean(b[:n].astype('float64').reshape(-1,4800,2)**2,axis=(1,2)))
 valid=x>10**(-50/20)
 gr=20*np.log10(np.maximum(y[valid],1e-12)/x[valid])
 stats={'median_attenuation_db':round(float(-np.median(gr)),3),'p99_attenuation_db':round(float(-np.percentile(gr,1)),3),'maximum_attenuation_db':round(float(-np.min(gr)),3)}
 assert stats['p99_attenuation_db']<2.5,(cue,'Excessive bus compression',stats)
 m=measure(glue);before=measure(raw);gain=round(-18.25-float(m['input_i']),4)
 predicted=float(m['input_tp'])+gain;reduction=max(0,predicted+3.8)
 assert reduction<1.8,(cue,'Fix mix peaks before mastering',reduction)
 return {'id':cue,'raw':before,'glue':m,'compression':stats,'master_gain_db':gain,'predicted_unlimited_true_peak_dbtp':round(predicted,3),'peak_guard_ceiling_db':-3.8,'predicted_peak_guard_reduction_db':round(reduction,3),'peak_guard':'Native ReaLimit with equal threshold/ceiling; verify final loudness and encoded true peaks independently.'}
def main():
 assert (BUILD/'mix_songs_final.result.txt').read_text().strip()=='PASS'
 with ThreadPoolExecutor(max_workers=3)as pool:results=list(pool.map(one,['opera_house','sky_lagoon','castle']))
 (PACKAGE/'mix_assessment.json').write_text(json.dumps({'status':'PASS','album_target_lufs':-18.25,'reason':'A quarter dB of additional album headroom preserves the acoustic guitar attacks while keeping all three masters matched inside the project -18 LUFS +/-0.5 window.','mixes':results},indent=2)+'\n',encoding='utf-8')
 (BUILD/'master_gains.lua').write_text('return {'+','.join(r['id']+'='+str(r['master_gain_db']) for r in results)+'}\n')
 print(json.dumps([{k:r[k] for k in ['id','compression','master_gain_db','predicted_unlimited_true_peak_dbtp','predicted_peak_guard_reduction_db']} for r in results],indent=2))
if __name__=='__main__':main()
