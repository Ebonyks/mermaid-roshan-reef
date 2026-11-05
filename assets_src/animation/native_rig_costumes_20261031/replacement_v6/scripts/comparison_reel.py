"""Portable side-by-side review of the two final costumes in all three actions."""
from pathlib import Path
import subprocess
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1];FF='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/FFmpeg/8.1.2/bin/ffmpeg.exe'
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',28)
for clip,title in [('arm_bend','Shoulder and arm bend'),('blink','Blink'),('tail_bend','Tail bend and settle')]:
 bg=Image.new('RGB',(1280,720),(225,233,243));d=ImageDraw.Draw(bg);d.text((34,22),'Coral ballet',font=font,fill=(50,35,48));d.text((674,22),'Violet magician',font=font,fill=(50,35,48));d.text((38,673),title+' / shared native Godot rig / source prototype',font=font,fill=(40,50,70));board=ROOT/'review'/f'compare_{clip}_background.png';bg.save(board)
 inputs=['-loop','1','-i',str(board)]
 for theme in ['ballet','magician']:inputs+=['-framerate','30','-i',str(ROOT/f'evidence/render_{theme}_v8'/clip/'%04d.png')]
 graph='[1:v]scale=640:640:flags=lanczos[a];[2:v]scale=640:640:flags=lanczos[b];[0:v][a]overlay=0:45:shortest=1[t];[t][b]overlay=640:45:shortest=1,format=yuv420p,setsar=1[out]'
 subprocess.run([FF,'-y','-v','error',*inputs,'-filter_complex',graph,'-map','[out]','-r','30','-an','-c:v','libx264','-crf','16','-preset','fast','-movflags','+faststart',str(ROOT/'review'/f'compare_{clip}.mp4')],check=True)
files=ROOT/'review/comparison_concat.txt';files.write_text(''.join(f"file 'compare_{c}.mp4'\n" for _ in range(2) for c in ['arm_bend','blink','tail_bend']),encoding='utf-8')
subprocess.run([FF,'-y','-v','error','-f','concat','-safe','0','-i',str(files),'-c','copy','-movflags','+faststart',str(ROOT/'review/costume_comparison.mp4')],check=True)
print('COMPARISON_REEL_OK')
