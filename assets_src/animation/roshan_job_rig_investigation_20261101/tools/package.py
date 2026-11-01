"""Lossless native-frame publication and silent landscape review movies."""
from pathlib import Path
import subprocess,json,hashlib,shutil,sys
import numpy as np
from PIL import Image,ImageSequence
R=Path(__file__).resolve().parents[1]; RAW=R/'evidence/raw_frames_v4'
FF='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/FFmpeg/8.1.2/bin/ffmpeg.exe'


def main():
    (R/'exports').mkdir(exist_ok=True);rows=[]
    for job in ['detective','geologist']:
        for clip in ['work','arm_bend','blink','tail_bend']:
            folder=RAW/job if clip=='work' else RAW/job/clip
            frames=sorted(folder.glob('[0-9]*.png'))
            out=R/'exports'/f'{job}_{clip}.apng'
            args=[FF,'-y','-v','error','-framerate','30','-i',str(folder/'%04d.png'),'-frames:v',str(len(frames)),'-c:v','apng','-plays','0',str(out)]
            subprocess.run(args,check=True)
            decoded=Image.open(out);bad=[];count=0
            for count,im in enumerate(ImageSequence.Iterator(decoded),1):
                source=np.array(Image.open(frames[count-1]).convert('RGBA'))
                actual=np.array(im.convert('RGBA'))
                if not np.array_equal(actual,source):bad.append(count-1)
            report={'job':job,'clip':clip,'frames':len(frames),'decoded_frames':count,'rgba_mismatch_indices':bad,'args':args,'lossless_pass':count==len(frames) and not bad,'native_dimensions':[1024,1024],'time_mapping':'frame i = i/30s; endpoint included; each displayed for1/30s; no retiming or fabricated in-between pixels','sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'bytes':out.stat().st_size}
            rows.append(report);print(job,clip,report['lossless_pass'],out.stat().st_size,flush=True)
            if clip=='work':
                movie=R/'review'/f'{job}_work.mp4'
                subprocess.run([FF,'-y','-v','error','-i',str(out),'-f','lavfi','-i','color=c=0x182231:s=1280x720:r=30','-filter_complex','[0:v]scale=720:720:flags=lanczos[fg];[1:v][fg]overlay=280:0:shortest=1,setsar=1[v]','-map','[v]','-an','-c:v','libx264','-crf','17','-pix_fmt','yuv420p','-movflags','+faststart',str(movie)],check=True)
                report['review_movie']={'path':str(movie.relative_to(R)),'sha256':hashlib.sha256(movie.read_bytes()).hexdigest(),'derivation':'actual native engine RGBA uniformly720/1024 scaled, centered on1280x720 dark field; silent diagnostic; no cinematic delivery acceptance'}
    (R/'evidence/lossless_export.json').write_text(json.dumps({'ffmpeg':FF,'clips':rows,'pass':all(x['lossless_pass'] for x in rows)},indent=2)+'\n')
    # Preserve exact geometry/motion reports and their inspectable boards.
    for job in ['detective','geologist']:
        for p in (RAW/job).glob('*audit*.json'):shutil.copy2(p,R/'evidence'/job/p.name)
        for p in (RAW/job).glob('*board.jpg'):shutil.copy2(p,R/'review'/f'{job}_{p.name}')
    if not all(x['lossless_pass'] for x in rows):raise SystemExit(1)


if __name__=='__main__':main()
