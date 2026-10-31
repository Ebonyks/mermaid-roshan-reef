"""Offline deterministic Aseprite correction; never submits generation jobs."""
import json,subprocess,sys,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from prepare import P,ROOT,OLD
ASE=r'C:\Program Files\Aseprite\Aseprite.exe'
FF=r'C:\Users\Peter\AppData\Local\Programs\MermaidReefTools\FFmpeg\8.1.2\bin\ffmpeg.exe'
def child(name):
    return subprocess.run([sys.executable,'-X','utf8','-s','-B',str(P/'scripts'/name)],check=True)
def ase(script,params):
    args=[ASE,'-b']
    for key,value in params.items():args+=['--script-param',key+'='+str(value)]
    args+=['--script',str(P/'scripts'/script)]
    return subprocess.run(args,check=True,timeout=300)
def encode():
    out=ROOT/'export/ltx25_scale_filter_v2_20261004/comparison_frames';out.mkdir(parents=True,exist_ok=True)
    ase('compare.lua',{'root':ROOT,'packet':P,'output':out})
    for src,dst in [(P/'frames',P/'registered_review.mp4'),(out,P/'raw_v1_v2_comparison.mp4')]:
        subprocess.run([FF,'-hide_banner','-loglevel','error','-y','-framerate','24','-i',str(src/'%04d.png'),
                        '-c:v','libx264','-crf','15','-preset','medium','-pix_fmt','yuv420p','-movflags','+faststart',str(dst)],check=True,timeout=120)
    return out
def check_comparison(out):
    import numpy as np
    from PIL import Image
    for i in range(41):
        a=np.array(Image.open(out/f'{i:04d}.png').convert('RGBA'))
        for j,folder in enumerate([OLD/'results/scale_registered/refined_frames',OLD/'scale_continuity/decoded_filtered',P/'frames']):
            assert np.array_equal(a[:,j*576:(j+1)*576],np.array(Image.open(folder/f'{i:04d}.png').convert('RGBA'))),('Column mismatch',i,j)
    report={'status':'PASS','compared_native_columns':123,'frames':41,'dimensions':[1728,832],
            'columns':['raw fifth take','faulty v1 filter','continuous v2 filter'],'timeline':'i -> i at24fps; no substituted frames',
            'encoding':{'codec':'libx264','crf':15,'pixel_format':'yuv420p','fps':24},'video_acceptance':False}
    probe=Path(FF).with_name('ffprobe.exe')
    for name in ['registered_review.mp4','raw_v1_v2_comparison.mp4']:
        info=json.loads(subprocess.run([str(probe),'-v','error','-show_streams','-of','json',str(P/name)],capture_output=True,text=True,check=True).stdout)
        video=next(s for s in info['streams'] if s['codec_type']=='video')
        assert int(video['nb_frames'])==41 and video['avg_frame_rate']=='24/1'
    (P/'comparison_verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('COMPARISON123_NATIVE_COLUMNS_PASS')
if __name__=='__main__':
    start=time.monotonic();child('prepare.py');ase('register.lua',{'packet':P,'root':ROOT})
    result=subprocess.run([sys.executable,'-X','utf8','-s','-B',str(P/'scripts/verify.py')])
    if result.returncode:
        child('feedback.py');ase('register.lua',{'packet':P,'root':ROOT,'feedback_only':'true'});child('verify.py')
    check_comparison(encode())
    (P/'execution.json').write_text(json.dumps({'new_model_takes':0,'new_imagegen_calls':0,'offline':True,'wall_seconds':time.monotonic()-start},indent=2)+'\n',encoding='utf-8')
