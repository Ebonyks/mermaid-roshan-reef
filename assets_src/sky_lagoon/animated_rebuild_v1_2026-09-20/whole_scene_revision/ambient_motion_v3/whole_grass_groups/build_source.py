from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,subprocess,json,hashlib,zipfile,xml.etree.ElementTree as ET
p=Path(__file__).resolve().parent;r=subprocess.run(['C:/Program Files/Aseprite/Aseprite.exe','-b','--script-param','out='+str(p),'--script',str(p/'author_individual.lua')],capture_output=True,text=True,creationflags=subprocess.CREATE_NO_WINDOW,timeout=120);assert r.returncode==0,r.stderr;(p/'individual-author.log').write_text(r.stdout+r.stderr);info=json.loads((p/'TUFTS.json').read_text());report=[]
for row in info['tufts']:
 j=row['tuft'];rootx,rooty=row['root'];box=(round(rootx)-128,rooty-220,round(rootx)+128,rooty+36);frames=[Image.open(p/f'tuft-{j}-cel-{k}.png').convert('RGBA') for k in range(4)];rest=np.asarray(Image.open(p/f'tuft-{j}-rest.png').convert('RGBA'));stop=rooty-8
 assert np.array_equal(np.asarray(frames[0])[rest[:,:,3]>0],rest[rest[:,:,3]>0])
 atlas=Image.new('RGBA',(512,512))
 for k,f in enumerate(frames):
  assert np.array_equal(np.asarray(f)[stop:],np.asarray(frames[0])[stop:]);cell=f.crop(box);assert cell.getchannel('A').getbbox() is not None;atlas.paste(cell,(k%2*256,k//2*256));cell.save(p/f'tuft-{j}-cell-{k}.png')
 atlas.save(p/f'tuft-{j}-atlas.png');report.append({'tuft':j,'crop_box':box,'runtime_root':[128,220],'fixed_rows_from':stop,'unique_frames':len({hashlib.sha256(f.tobytes()).hexdigest() for f in frames})})
for k in range(4):assert np.array_equal(np.asarray(Image.open(p/f'group-cel-{k}.png')),np.asarray(Image.open(p/f'group-reopen-{k}.png')))
root=ET.Element('image',w='512',h='256',name='Three grass tufts: four pose alternatives');stack=ET.SubElement(root,'stack')
with zipfile.ZipFile(p/'three-grass-tufts-four-poses.ora','w',zipfile.ZIP_DEFLATED) as z:
 z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
 for k in range(4):
  group=ET.SubElement(stack,'stack',name=f'Pose {k+1}',visibility='visible' if k==0 else 'hidden',opacity='1.0')
  for j in reversed(range(3)):
   for label,name in [('fixed root',f'tuft-{j}-base.png'),('whole crown',f'tuft-{j}-upper-{k}.png')]:
    path=f'data/{k}-{name}';z.write(p/name,path);ET.SubElement(group,'layer',name=f'Tuft {j+1} {label}',src=path,x='0',y='0',opacity='1.0',visibility='visible',**{'composite-op':'svg:src-over'})
 z.writestr('stack.xml',ET.tostring(root));z.write(p/'group-cel-0.png','mergedimage.png')
(p/'INDIVIDUAL_MOTION_REVIEW.json').write_text(json.dumps({'status':'SOURCE_TRIAL_NOT_RUNTIME_ACCEPTED','frames':4,'native_layers':6,'cycle_seconds':1.4,'frame_duration_seconds':.35,'ora_pose_layers':24,'native_reopen_exact':True,'individual_tufts':report,'source_split':'Naturally disconnected plants; exact rest reconstruction before motion. No blade cut or invented hidden pixels.','motion':'Each complete grass crown bends independently with slightly delayed phase; roots fixed. Direct Aseprite deformation, not independent redraws.','three_atlases_raw_rgba_mib':3,'limits':['Need actual Mobile placement/color/motion review','Not native Krita animation timelines','No claim of broad lawn coverage or owner acceptance']},indent=2)+'\n');print(r.stdout)
