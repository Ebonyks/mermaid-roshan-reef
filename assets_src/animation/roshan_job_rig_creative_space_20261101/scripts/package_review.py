"""Publishable diagnostic movies, frame boards and exact native-frame hashes."""
from pathlib import Path
import hashlib,json,subprocess,shutil
from PIL import Image,ImageDraw
import numpy as np

P=Path(__file__).resolve().parents[1];RAW=P/'evidence/raw';OUT=P/'review';OUT.mkdir(exist_ok=True)
KEYS=OUT/'native_keyframes';KEYS.mkdir(exist_ok=True)
FFMPEG=shutil.which('ffmpeg')
hashes=[];movies=[]
for theme in ['original','ballet','magician','painter','astronaut']:
    for clipdir in sorted((RAW/theme).iterdir()):
        if not clipdir.is_dir():continue
        paths=sorted(clipdir.glob('*.png'))
        if not paths:continue
        for index,f in enumerate(paths):
            im=Image.open(f).convert('RGBA')
            hashes.append(dict(theme=theme,clip=clipdir.name,frame=index,png_sha256=hashlib.sha256(f.read_bytes()).hexdigest(),rgba_sha256=hashlib.sha256(im.tobytes()).hexdigest(),dimensions=list(im.size)))
        if theme not in ['painter','astronaut']:continue
        indices=list(np.linspace(0,len(paths)-1,12).round().astype(int))
        if clipdir.name=='blink':indices=[0,15,28,30,31,32,33,34,36,45,60,72]
        board=Image.new('RGB',(1280,1050),'#172033');draw=ImageDraw.Draw(board)
        for j,k in enumerate(indices):
            picture=Image.open(paths[k]).convert('RGBA');bg=Image.new('RGBA',picture.size,['#f2f2ed','#10131e','#64748b'][j%3]);bg.alpha_composite(picture);bg.thumbnail((320,320));x=j%4*320;y=j//4*350;board.paste(bg.convert('RGB'),(x,y));draw.text((x+8,y+325),f'{theme} {clipdir.name} {k}/30s',fill='white')
        board.save(OUT/(theme+'_'+clipdir.name+'_board.jpg'),quality=94)
        for k in sorted({0,len(paths)//2,len(paths)-1, min(45,len(paths)-1)}):shutil.copy2(paths[k],KEYS/f'{theme}_{clipdir.name}_{k:04d}.png')
        manifest=OUT/(theme+'_'+clipdir.name+'.ffconcat')
        manifest.write_text('ffconcat version 1.0\n'+''.join("file '"+f.resolve().as_posix()+"'\noption framerate 30\nduration 0.033333333333\n" for f in paths),encoding='utf-8')
        output=OUT/(theme+'_'+clipdir.name+'.mp4')
        filters='color=c=0x172033:s=1280x720:r=30[bg];[0:v]scale=720:720:flags=lanczos[fg];[bg][fg]overlay=280:0:shortest=1,format=yuv420p[out]'
        command=[FFMPEG,'-y','-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',str(manifest),'-filter_complex_threads','1','-filter_complex',filters,'-map','[out]','-frames:v',str(len(paths)),'-r','30','-an','-c:v','libx264','-threads','2','-preset','fast','-crf','18','-movflags','+faststart',str(output)]
        result=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        (OUT/(theme+'_'+clipdir.name+'_encode.log')).write_bytes(result.stdout)
        movies.append(dict(file=output.name,exit=result.returncode,source_frames=len(paths),sha256=hashlib.sha256(output.read_bytes()).hexdigest() if output.exists() else None,mapping='Native source indices 0..N inclusive at 30fps; uniform 1024-square to 720-square mapping, landscape padding. H264 diagnostic only; no cinematic delivery or runtime art claim.'))
        print('REVIEW',theme,clipdir.name,len(paths),'frames',flush=True)
    if theme in ['painter','astronaut']:
        job='paint_banner' if theme=='painter' else 'turn_valve';im=Image.open(RAW/theme/job/'0045.png').convert('RGBA');detail=Image.new('RGB',(1280,600),'#172033');d=ImageDraw.Draw(detail)
        windows=[('shoulders / neckline',(420,315,660,425)),('waist / apron',(445,425,665,635)),('tail / fin join',(350,740,590,925)),('hand / object',(285,350,465,485)),('headwear',(405,85,685,360))]
        for index,(name,rect) in enumerate(windows):
            crop=im.crop(rect);bg=Image.new('RGBA',crop.size,'#cbd5e1');bg.alpha_composite(crop);bg.thumbnail((250,550));x=index*256;detail.paste(bg.convert('RGB'),(x,35));d.text((x+5,8),name,fill='white')
        detail.save(OUT/(theme+'_contact_details.png'))
(OUT/'native_frame_hashes.json').write_text(json.dumps(dict(frames=len(hashes),rows=hashes,raw_reconstruction='Run godot/capture_all.gd against frozen source; PNG and RGBA hashes are recorded independently.'),indent=2)+'\n',encoding='utf-8')
(OUT/'movies.json').write_text(json.dumps(dict(movies=movies,all_encodes_ok=all(x['exit']==0 for x in movies),role='DIAGNOSTIC_REVIEW_ONLY',normal_speed_human_review='PENDING',frame_step_human_review='PENDING',device_child_owner='PENDING'),indent=2)+'\n',encoding='utf-8')
print('REVIEW PACKAGE',len(hashes),'native frames',len(movies),'movies',flush=True)
