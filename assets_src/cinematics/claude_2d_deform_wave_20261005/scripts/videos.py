import sys, subprocess, os; sys.path.insert(0,__import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from render import arm_target
from common import *
from PIL import ImageDraw, ImageFont
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18); F2=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15)
BG=(240,239,238); V=W('vid')
for d in ('review','cmp','native'): os.makedirs(f'{V}/{d}',exist_ok=True)
for f in range(41):
    m=np.array(Image.open(W('review','%04d.png'%f))).astype(np.float32)/255
    mine=(on_bg(premul(m),BG)*255+0.5).astype(np.uint8); Image.fromarray(mine).save(f'{V}/review/%04d.png'%f)
    cod=np.array(Image.open(W('codex','%04d.png'%f)).convert('RGB'))
    t=Image.fromarray(np.concatenate([cod,np.full((896,6,3),60,np.uint8),mine],1)); d=ImageDraw.Draw(t)
    d.text((10,10),'Codex: LTX-2.5 Union take 1 (native)',fill=(20,20,20),font=F)
    d.text((656,10),'Claude: 2D whole-figure deformation',fill=(20,20,20),font=F)
    d.text((10,866),'frame %02d / 40   24 fps'%f,fill=(20,20,20),font=F); t.save(f'{V}/cmp/%04d.png'%f)
    n=Image.open(P('frames','native','%04d.png'%f)).convert('RGBA'); bg=Image.new('RGBA',n.size,BG+(255,)); bg.alpha_composite(n)
    bg.convert('RGB').resize((768,768),Image.NEAREST).save(f'{V}/native/%04d.png'%f)
fit=json.load(open(P('data','codex_canvas_fit.json'))); s,tx,ty=fit['scale'],fit['tx_640'],fit['ty_640']
cols=[]
for f in [6,10,17,20,22,24,26,30]:
    tp=arm_target(float(f)); c=(tp[2]+tp[3])/2; cx,cy=c[0]*s+tx,c[1]*s+ty
    x0=int(np.clip(cx-110,0,420)); y0=int(np.clip(cy-110,0,676))
    cod=np.array(Image.open(f'{V}/cmp/%04d.png'%f))[:,:640][y0:y0+220,x0:x0+220]
    mine=np.array(Image.open(f'{V}/review/%04d.png'%f))[y0:y0+220,x0:x0+220]
    t=Image.fromarray(np.concatenate([cod,np.full((4,220,3),60,np.uint8),mine],0)); d=ImageDraw.Draw(t)
    d.text((4,2),'f%02d Codex'%f,fill=(0,0,0),font=F2); d.text((4,226),'f%02d Claude'%f,fill=(0,0,0),font=F2)
    cols+= [np.array(t),np.full((444,4,3),60,np.uint8)]
Image.fromarray(np.concatenate(cols[:-1],1)).save(P('comparison','hand_closeups.png'))
tiles=[]
for f in range(0,41,2):
    T=Image.open(f'{V}/review/%04d.png'%f).resize((214,299),Image.LANCZOS); ImageDraw.Draw(T).text((4,4),str(f),fill=(0,0,0),font=F2); tiles.append(np.array(T))
Image.fromarray(np.concatenate([np.concatenate(tiles[i:i+7],1) for i in range(0,21,7)],0)).save(P('review','contact_sheet.png'))
def ff(*a): subprocess.run(['ffmpeg','-loglevel','error','-y',*a],check=True)
ff('-framerate','24','-i',f'{V}/review/%04d.png','-c:v','libx264','-crf','15','-pix_fmt','yuv420p','-movflags','+faststart',P('review','wave_review.mp4'))
ff('-framerate','24','-i',f'{V}/cmp/%04d.png','-c:v','libx264','-crf','15','-pix_fmt','yuv420p','-movflags','+faststart',P('comparison','comparison_codex_vs_claude.mp4'))
ff('-framerate','6','-i',f'{V}/cmp/%04d.png','-c:v','libx264','-crf','15','-pix_fmt','yuv420p','-movflags','+faststart',P('comparison','comparison_frame_step_6fps.mp4'))
ff('-framerate','24','-i',f'{V}/native/%04d.png','-c:v','libx264','-crf','12','-pix_fmt','yuv420p','-movflags','+faststart',P('review','wave_native256_x3_nearest.mp4'))
ff('-framerate','24','-i',f'{V}/cmp/%04d.png','-vf','scale=643:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=192[p];[b][p]paletteuse=dither=sierra2_4a','-loop','0',P('comparison','comparison.gif'))
print('ok')
