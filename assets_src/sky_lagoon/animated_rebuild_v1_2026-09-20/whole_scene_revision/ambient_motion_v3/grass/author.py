from pathlib import Path
import subprocess,re
w=Path.cwd();p=w/'tmp/sky-lagoon-whole-scene-v2/grass-pointed-trial/blade-layers';t=(w/'assets_src/sky_lagoon/animated_rebuild_v1_2026-09-20/whole_scene_revision/meadow_berry_fan/author_cels.lua').read_text(encoding='utf-8')
t=t.replace('local W,H=640,490','local W,H=640,426').replace('local px,py=688*640/1433,635*640/1433','local px,py=798*640/1537,917*640/1537')
t=re.sub(r"local names=.*?local s=Sprite", "local names={'right_outer','left_outer','center','right_upper','left_upper','right_mid','left_mid','roots_fixed'}\nlocal angles={{0,-1.2,.8,.3},{0,-1.1,.7,.2},{0,-1.8,1.3,.3},{0,-1.6,1.1,.2},{0,-1.4,1.0,.4},{0,-1.0,.7,.2},{0,-.9,.6,.3},{0,0,0,0}}\nlocal s=Sprite",t,flags=re.S)
t=t.replace('for k=1,8 do','for k=1,4 do').replace('s.frames[k].duration=.3','s.frames[k].duration=.65').replace('local angle=-angles[j][k]*2*math.pi/180*lock','lock=lock*math.max(0,math.min(1,(375-y)/45))\n    local angle=-angles[j][k]*2*math.pi/180*lock').replace('s:newTag(1,8)','s:newTag(1,4)').replace('meadow_berry_fan_breeze_study','grass_fan_breeze_study').replace('meadow-berry-fan-eight-cels','grass-fan-four-cels')
t=t.replace('im:drawPixel(x,y,sample(source,sx,sy))','if angle==0 then im:drawPixel(x,y,source:getPixel(x,y)) else im:drawPixel(x,y,sample(source,sx,sy)) end')
(p/'author_cels.lua').write_text(t,encoding='utf-8')
r=subprocess.run(['C:/Program Files/Aseprite/Aseprite.exe','-b','--script-param','base='+str(p),'--script',str(p/'author_cels.lua')],capture_output=True,text=True,creationflags=subprocess.CREATE_NO_WINDOW,timeout=240)
(p/'author-log.txt').write_text(r.stdout+r.stderr,encoding='utf-8');print('GRASS_ASEPRITE',r.returncode,r.stdout,r.stderr,flush=True)
