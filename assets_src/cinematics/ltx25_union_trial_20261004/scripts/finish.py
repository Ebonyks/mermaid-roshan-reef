"""Aseprite export and source-accurate comparison; Python reads pixels for verification only."""
from pathlib import Path
import subprocess,json,hashlib,argparse
from PIL import Image
import numpy as np
P=Path(__file__).resolve().parents[1];ROOT=P.parents[2]
ASE=r'C:\Program Files\Aseprite\Aseprite.exe'
FF=r'C:\Users\Peter\AppData\Local\Programs\MermaidReefTools\FFmpeg\8.1.2\bin\ffmpeg.exe'
PROBE=FF.replace('ffmpeg.exe','ffprobe.exe')
def pixels(p):
 with Image.open(p) as im:return np.array(im.convert('RGBA'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main(take):
 folder=P/take;receipt=json.loads((folder/'receipt.json').read_text());assert receipt['status']=='EXECUTION_PASS'
 out=ROOT/'export/ltx25_union_trial_20261004'/take;out.mkdir(parents=True,exist_ok=True)
 comp=out/'comparison_frames';comp.mkdir(exist_ok=True);rounds=out/'roundtrip';rounds.mkdir(exist_ok=True)
 subprocess.run([ASE,'--batch','--script-param','packet='+str(P),'--script-param','root='+str(ROOT),'--script-param','take='+take,'--script-param','output='+str(comp),'--script',str(P/'scripts/review.lua')],check=True,timeout=120)
 for source,dest in [(folder/'refined_frames',folder/'native_review.mp4'),(comp,folder/'comparison.mp4')]:
  subprocess.run([FF,'-hide_banner','-loglevel','error','-y','-framerate','24','-start_number','0','-i',str(source/'%04d.png'),'-frames:v','41','-c:v','libx264','-crf','15','-pix_fmt','yuv420p','-movflags','+faststart',str(dest)],check=True,timeout=120)
 subprocess.run([ASE,'--batch','--script-param','master='+str(folder/'native_review.aseprite'),'--script-param','output='+str(rounds),'--script',str(P/'scripts/export_roundtrip.lua')],check=True,timeout=120)
 proof=[]
 for i in range(41):
  f=folder/f'refined_frames/{i:04d}.png';a=pixels(f);assert a.shape==(896,640,4)
  assert np.array_equal(a,pixels(rounds/f'{i:04d}.png'))
  pair=pixels(comp/f'{i:04d}.png');assert pair.shape==(896,1920,4)
  prior=ROOT/f'assets_src/cinematics/ltx25_scale_filter_v2_20261004/frames/{i:04d}.png'
  assert np.array_equal(pair[32:864,8:584],pixels(prior))
  assert np.array_equal(pair[:,640:1280],pixels(P/f'guide_full/{i:04d}.png'))
  assert np.array_equal(pair[:,1280:],a)
  stage=pixels(folder/f'stage1_frames/{i:04d}.png');assert stage.shape==(448,320,4)
  proof.append({'index':i,'native_sha256':sha(f),'aseprite_pixel_exact':True,'comparison_source_columns_exact':True})
 videos=[]
 for name,width in [('native_review.mp4',640),('comparison.mp4',1920)]:
  d=json.loads(subprocess.run([PROBE,'-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=width,height,r_frame_rate,nb_read_frames','-of','json',str(folder/name)],check=True,capture_output=True,text=True).stdout)['streams'][0]
  assert (d['width'],d['height'],d['r_frame_rate'],d['nb_read_frames'])==(width,896,'24/1','41');videos.append({'name':name,**d})
 for lane,dims in [('full',(896,640,4)),('half',(448,320,4)),('quarter',(224,160,4))]:
  for i in range(41):assert pixels(P/f'guide_{lane}/{i:04d}.png').shape==dims
 result={'status':'MACHINE_EXPORT_PASS','native_frames':41,'stage1_frames':41,'guide_frames':123,'aseprite_roundtrip_frames':41,'aseprite_timeline_ms':1708,'exact_comparison_columns':123,'rows':proof,'videos':videos,'comparison_mapping':'Prior registered v2 left with8px left/32px top pad (removes prior constant24px layout offset); authored whole-figure outline middle; Union native right. No scaling or temporal replacement.','creative_or_device_acceptance':False}
 (folder/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print('EXPORT_PASS',take,'41 native roundtrips,123 exact comparison columns,2 correct videos')
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('take');main(a.parse_args().take)
