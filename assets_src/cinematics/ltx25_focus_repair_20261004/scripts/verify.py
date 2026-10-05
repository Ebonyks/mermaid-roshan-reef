"""Verify source identity, complete native-frame Aseprite roundtrips and comparison mapping."""
import hashlib,json,subprocess
from pathlib import Path
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parents[1];ROOT=P.parents[2]
OLD=ROOT/'assets_src/cinematics/ltx25_8gb_wave_20261004'
OUT=ROOT/'export/ltx25_focus_repair_20261004';OUT.mkdir(parents=True,exist_ok=True)
ROUND=OUT/'roundtrip';ROUND.mkdir(exist_ok=True)
ASE=r'C:\Program Files\Aseprite\Aseprite.exe'
PROBE=r'C:\Users\Peter\AppData\Local\Programs\MermaidReefTools\FFmpeg\8.1.2\bin\ffprobe.exe'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pixels(p):
    with Image.open(p) as im:return np.array(im.convert('RGBA'))
receipt=json.loads((P/'receipt.json').read_text())
assert sha(ROOT/receipt['source_latent'])==receipt['source_latent_sha256']
assert sha(P/'workflow.api.json')==receipt['workflow_sha256']
assert receipt['baseline_pixel_identical_frames']==41 and all(receipt['baseline_per_frame_exact'])
assert receipt['new_transformer_jobs']==0 and receipt['new_imagegen_calls']==0 and receipt['new_decoder_ablation_jobs']==1
for n in [1,2]:
    proof=json.loads((P/f'decoder_{n}_proof.json').read_text())
    assert proof['steps']==n and proof['same_video_latent_unchanged'] is True,proof
subprocess.run([ASE,'--batch','--script-param','master='+str(P/'decoder_2_review.aseprite'),
    '--script-param','output='+str(ROUND),'--script',str(P/'scripts/roundtrip.lua')],check=True,timeout=120)
rows=[]
for i in range(41):
    native=P/f'decoder_2_frames/{i:04d}.png';a=pixels(native)
    assert a.shape==(832,576,4) and np.isfinite(a).all()
    assert np.array_equal(a,pixels(ROUND/f'{i:04d}.png')),'Aseprite roundtrip '+str(i)
    pair=pixels(OUT/f'comparison_frames/{i:04d}.png')
    assert pair.shape==(832,1152,4)
    baseline=OLD/f'results/scale_registered/refined_frames/{i:04d}.png'
    assert np.array_equal(pair[:,:576,:],pixels(baseline)),'Baseline column '+str(i)
    assert np.array_equal(pair[:,576:,:],a),'Experimental column '+str(i)
    rows.append({'index':i,'native_sha256':sha(native),'aseprite_pixel_exact':True,'left_default_right_experimental_pixel_exact':True})
videos=[]
for name,width in [('decoder_2_review.mp4',576),('decoder_1_vs_2.mp4',1152)]:
    result=subprocess.run([PROBE,'-v','error','-select_streams','v:0','-count_frames',
        '-show_entries','stream=width,height,r_frame_rate,nb_read_frames','-of','json',str(P/name)],check=True,capture_output=True,text=True)
    v=json.loads(result.stdout)['streams'][0]
    assert (v['width'],v['height'],v['r_frame_rate'],v['nb_read_frames'])==(width,832,'24/1','41'),v
    videos.append({'path':name,**v})
review=json.loads((P/'native_review.json').read_text());assert review['decoder2_verdict']=='REJECT'
report={'status':'MACHINE_VERIFICATION_PASS','native_frames':41,'default_pixel_parity_frames':41,
    'aseprite_roundtrip_frames':41,'aseprite_timeline_ms':1708,'exact_comparison_columns':82,
    'rows':rows,'videos':videos,'native_visual_status':review['status'],
    'geometry_focus_or_device_acceptance':False,'new_transformer_jobs':0,'new_imagegen_calls':0}
(P/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('MACHINE_PASS41 native/default/roundtrip frames;82 exact comparison columns;2 correct videos; VISUAL_REJECT')
