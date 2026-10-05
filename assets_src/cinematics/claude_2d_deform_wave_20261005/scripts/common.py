import numpy as np, cv2, json, os
from PIL import Image
from paths import *
import hashlib

# Waving-arm joint chain per approved key (256px atlas cell coords).
ARM={
 0: dict(shoulder=(120,103), elbow=(115,127), wrist=(104,150), palm=(101,156), tip=(98,165)),
 1: dict(shoulder=(114,104), elbow=(101,112), wrist=(94,91),  palm=(92.4,82.8), tip=(91,71)),
 2: dict(shoulder=(92,90),   elbow=(82.6,65), wrist=(74,42),  palm=(70.6,34.4), tip=(67.5,22)),
 3: dict(shoulder=(79,103),  elbow=(57,104),  wrist=(55,81),  palm=(53.75,75), tip=(51.25,62.5)),
}

_ATLAS=None
def load_key(k):
    """Approved wave key k = row 0, column k of roshan_gesture_a.png (256 px cells), straight alpha float."""
    global _ATLAS
    if _ATLAS is None:
        b=open(ATLAS,'rb').read()
        assert hashlib.sha256(b).hexdigest()==ATLAS_SHA256, 'approved atlas changed; refusing to build'
        _ATLAS=np.array(Image.open(ATLAS).convert('RGBA'))
    return _ATLAS[0:256,k*256:(k+1)*256].astype(np.float32)/255.0

def skin_mask(im):
    rgb=(im[:,:,:3]*255).astype(np.uint8); a=im[:,:,3]
    hsv=cv2.cvtColor(rgb,cv2.COLOR_RGB2HSV).astype(np.float32)
    h,s,v=hsv[:,:,0],hsv[:,:,1],hsv[:,:,2]
    return (h>=3)&(h<=22)&(s>=25)&(s<=120)&(v>=170)&(a>0.5)

def premul(im):
    o=im.copy(); o[:,:,:3]*=o[:,:,3:4]; return o
def unpremul(im):
    o=im.copy(); a=np.clip(o[:,:,3:4],1e-6,1); o[:,:,:3]=np.where(o[:,:,3:4]>1e-6,o[:,:,:3]/a,0); return o
def save_rgba(im,path,unp=True):
    o=unpremul(im) if unp else im
    Image.fromarray((np.clip(o,0,1)*255+0.5).astype(np.uint8),'RGBA').save(path)
def on_bg(im,color=(200,220,235)):
    o=unpremul(im); bg=np.ones_like(o[:,:,:3])*np.array(color)/255.0
    return o[:,:,:3]*o[:,:,3:4]+bg*(1-o[:,:,3:4])
