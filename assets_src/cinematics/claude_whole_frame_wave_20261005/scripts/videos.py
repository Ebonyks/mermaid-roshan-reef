"""Viewing copies of the same animation: 768x768 review movie, native 256 px at 3x nearest, and a GIF."""
import sys,os,subprocess; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
BG=(240,239,238); os.makedirs(W('vid','review'),exist_ok=True); os.makedirs(W('vid','native'),exist_ok=True)
for f in range(41):
    m=np.array(Image.open(W('review','%04d.png'%f))).astype(np.float32)/255
    Image.fromarray((on_bg(premul(m),BG)*255+0.5).astype(np.uint8)).save(W('vid','review','%04d.png'%f))
    n=Image.open(P('frames','native','%04d.png'%f)).convert('RGBA'); bg=Image.new('RGBA',n.size,BG+(255,)); bg.alpha_composite(n)
    bg.convert('RGB').resize((768,768),Image.NEAREST).save(W('vid','native','%04d.png'%f))
def ff(*a): subprocess.run(['ffmpeg','-loglevel','error','-y',*a],check=True)
ff('-framerate','24','-i',W('vid','review','%04d.png'),'-c:v','libx264','-crf','15','-pix_fmt','yuv420p','-movflags','+faststart',P('review','wave_review.mp4'))
ff('-framerate','24','-i',W('vid','native','%04d.png'),'-c:v','libx264','-crf','12','-pix_fmt','yuv420p','-movflags','+faststart',P('review','wave_native256_x3_nearest.mp4'))
ff('-framerate','24','-i',W('vid','review','%04d.png'),'-vf','scale=480:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=192[p];[b][p]paletteuse=dither=sierra2_4a','-loop','0',P('review','wave.gif'))
print('videos ok')
