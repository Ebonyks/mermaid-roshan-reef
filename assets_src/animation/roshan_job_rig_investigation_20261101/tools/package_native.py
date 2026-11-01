"""Publish exact native PNG bytes in bounded ZIP chunks and MP4 review copies."""
from pathlib import Path
import hashlib,json,zipfile,subprocess
R=Path(__file__).resolve().parents[1];RAW=R/'evidence/raw_frames_v6'
FF='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/FFmpeg/8.1.2/bin/ffmpeg.exe'
sha=lambda b:hashlib.sha256(b).hexdigest()
(R/'exports').mkdir(exist_ok=True)
groups=[]
for job in ['detective','geologist']:
    for clip in ['work','arm_bend','blink','tail_bend']:
        folder=RAW/job if clip=='work' else RAW/job/clip
        groups.append((job+'_'+clip,sorted(folder.glob('[0-9]*.png'))))
groups.append(('all_slot_mixes',sorted((RAW/'mixes').glob('*.png'))))
groups.append(('legacy_seed_preservation',sorted((R/'evidence/scratch/legacy_reference').glob('*.png'))))
rows=[]
for name,files in groups:
    for first in range(0,len(files),64):
        subset=files[first:first+64];out=R/'exports'/f'{name}_{first:04d}.zip';index=[]
        with zipfile.ZipFile(out,'w',zipfile.ZIP_STORED) as z:
            for p in subset:
                b=p.read_bytes();arc=p.name;z.writestr(arc,b);index.append({'name':arc,'source':str(p.relative_to(R/'evidence')).replace('\\','/'),'sha256':sha(b)})
            z.writestr('frame_index.json',json.dumps({'native':'literal actual Godot PNG bytes','fps':None if name=='legacy_seed_preservation' else 30,'time_mapping':'Legacy samples use clip/time encoded in filename, not a continuous clip' if name=='legacy_seed_preservation' else 'frame i = i/30 seconds','frames':index},indent=2)+'\n')
        with zipfile.ZipFile(out) as z:valid=all(sha(z.read(v['name']))==v['sha256'] for v in index)
        rows.append({'path':str(out.relative_to(R)).replace('\\','/'),'sha256':sha(out.read_bytes()),'bytes':out.stat().st_size,'frames':index,'literal_byte_roundtrip':valid})
        print(out.name,len(subset),valid,flush=True)
for job in ['detective','geologist']:
    out=R/'review'/f'{job}_work.mp4'
    subprocess.run([FF,'-y','-v','error','-framerate','30','-i',str(RAW/job/'%04d.png'),'-f','lavfi','-i','color=c=0x182231:s=1280x720:r=30','-filter_complex','[0:v]scale=720:720:flags=lanczos[fg];[1:v][fg]overlay=280:0:shortest=1,setsar=1[v]','-map','[v]','-an','-c:v','libx264','-crf','17','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],check=True)
(R/'evidence/native_export.json').write_text(json.dumps({'candidate':'v6','pass':all(v['literal_byte_roundtrip'] for v in rows),'archives':rows,'movie_derivation':'Native RGBA uniformly720/1024 scaled and centered on1280x720 dark field;30fps silent source diagnostic. No synthesized acting, retiming or cinematic acceptance.'},indent=2)+'\n')
