"""Uniform scale + translation from the 256 px cell to Codex's 640x896 review canvas (grayscale NCC vs their K0 guide)."""
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
g=np.array(Image.open(W('codex','guide_0000.png')).convert('RGB')).astype(np.float32)/255
gray=cv2.cvtColor((g*255).astype(np.uint8),cv2.COLOR_RGB2GRAY).astype(np.float32)
rgb=on_bg(premul(load_key(0)),(238,238,238))
def score(s,tx,ty):
    M=np.float32([[s,0,tx],[0,s,ty]])
    w=cv2.warpAffine((rgb*255).astype(np.float32),M,(576,832),flags=cv2.INTER_LINEAR,borderValue=(238,238,238))
    wg=cv2.cvtColor(w.astype(np.uint8),cv2.COLOR_RGB2GRAY).astype(np.float32)
    a=wg-wg.mean(); b=gray-gray.mean(); return float((a*b).sum()/np.sqrt((a*a).sum()*(b*b).sum()))
best=None
for s in np.arange(3.15,3.32,0.01):
    for dy in range(-12,13,2):
        for dx in range(-6,7,2):
            tx=53-s*95+dx; ty=47-s*15+dy; v=score(s,tx,ty)
            if best is None or v>best[0]: best=(v,s,tx,ty)
sc,s,tx,ty=best; b2=best
for s2 in np.arange(s-0.01,s+0.0101,0.0025):
    for dx in np.arange(-1.5,1.6,0.5):
        for dy in np.arange(-1.5,1.6,0.5):
            v=score(s2,tx+dx,ty+dy)
            if v>b2[0]: b2=(v,s2,tx+dx,ty+dy)
sc,s,tx,ty=b2
json.dump({'scale':float(s),'tx_576':float(tx),'ty_576':float(ty),'tx_640':float(tx+32),'ty_640':float(ty+32),'ncc':float(sc),
           'meaning':'review pixel (X,Y) = (scale*x + tx, scale*y + ty) for 256 px cell point (x,y); Codex canvas = 576x832 guide + 32 px padding'},
          open(P('data','codex_canvas_fit.json'),'w'),indent=1)
