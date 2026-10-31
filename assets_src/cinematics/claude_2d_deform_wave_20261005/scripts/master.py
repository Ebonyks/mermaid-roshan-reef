"""Layered Aseprite master (256x256, 41 frames, 24 fps timing, beat tags) + reader round-trip check."""
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from render import *
import aseprite_io
def u8(premul_img):
    o=unpremul(premul_img); return (np.clip(o,0,1)*255+0.5).astype(np.uint8)
LAYERS=[('cap_under_body (hidden joint fill)',False),('body',False),('arm',False),('sleeve_over_arm',False),('final',True)]
frames=[]; mism=0
for f in range(N_FRAMES):
    png=np.array(Image.open(P('frames','native','%04d.png'%f)).convert('RGBA'))
    if f in (0,N_FRAMES-1):
        fr={'final':png}
    else:
        out,src,L=render_frame(float(f),1,cv2.INTER_LINEAR,return_layers=True)
        fin=u8(out)
        if not np.array_equal(fin,png): mism+=1
        fr={'final':fin,'body':u8(L['body']),'arm':u8(L['arm']),'cap_under_body (hidden joint fill)':u8(L['cap']),'sleeve_over_arm':u8(L['sleeve'])}
    frames.append(fr)
DUR=[round((i+1)*1000/24)-round(i*1000/24) for i in range(N_FRAMES)]
TAGS=[(0,3,'rest_anticipation'),(3,7,'rise_to_shoulder'),(7,17,'rise_overhead'),(17,27,'wave_lowering'),(27,36,'lower_to_rest'),(36,40,'settle')]
aseprite_io.write(P('wave_master.aseprite'),256,256,LAYERS,frames,DUR,TAGS)
m=aseprite_io.read(P('wave_master.aseprite'))
ok=all(np.array_equal(m['frames'][f]['final'],np.array(Image.open(P('frames','native','%04d.png'%f)).convert('RGBA'))) for f in range(N_FRAMES))
assert mism==0 and ok, (mism,ok)
print('master ok; total %d ms; tags %s'%(sum(m['durations']),[t[2] for t in m['tags']]))
