import sys; sys.path.insert(0,__import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from common import *
from scipy import ndimage as ndi

def disk(r):
    y,x=np.mgrid[-r:r+1,-r:r+1]; return (x*x+y*y)<=r*r+0.5

def build_layers(k):
    im=load_key(k); a=im[:,:,3]
    rgb=im[:,:,:3]
    hsv=cv2.cvtColor((rgb*255).astype(np.uint8),cv2.COLOR_RGB2HSV).astype(np.float32)
    H,Sat,V=hsv[:,:,0],hsv[:,:,1],hsv[:,:,2]
    sk=skin_mask(im)
    lab,n=ndi.label(sk)
    px,py=ARM[k]['palm']
    A=lab==lab[int(round(py)),int(round(px))]
    A=ndi.binary_closing(A,disk(1))
    A=ndi.binary_fill_holes(A)
    # finger gaps/inner lines: fill concavities between fingers
    A2=ndi.binary_fill_holes(ndi.binary_closing(A,disk(2)))
    # only accept the closing additions if they are darkish line/skin-shade pixels (not background)
    add=A2&~A&(a>0.3)
    A=A|add
    dark=(V<150)|(a<0.98)
    body_color=(a>0.9)&~dark&~ndi.binary_dilation(A,disk(1))
    bgnear=ndi.binary_dilation(a<0.05,disk(2))
    ring=(ndi.binary_dilation(A,disk(1))|(ndi.binary_dilation(A,disk(3))&bgnear))&~A&(a>0.02)&~body_color
    hair=(H>=5)&(H<=30)&(Sat>95)
    # outline shared with the body only where it borders bodice/sleeve colours, never hair
    near_body=ndi.binary_dilation(body_color&~hair,disk(2))
    shared=ring&near_body&dark
    armmask=A|ring
    arm_only=armmask&~shared
    # drop body fragments isolated by the arm removal
    rest=(a*(1-arm_only))>0.02
    lab,n=ndi.label(rest)
    sizes=ndi.sum(np.ones_like(a),lab,range(1,n+1))
    keep=np.zeros(n+1,bool); keep[1:]=sizes>=500
    frag=rest&~keep[lab]
    arm_only=arm_only|frag
    armmask=armmask|frag
    return im,armmask.astype(np.float32),arm_only.astype(np.float32),shared

if __name__=='__main__':
    rows=[]
    for k in range(4):
        im,am,ao,sh=build_layers(k)
        np.save(W('armmask_%d.npy'%k),am); np.save(W('armonly_%d.npy'%k),ao)
        Pm=premul(im)
        arm=Pm*am[:,:,None]; body=Pm*(1-ao)[:,:,None]
        save_rgba(arm,W('arm_%d.png'%k)); save_rgba(body,W('body_%d.png'%k))
        save_rgba(arm,P('layers','arm_k%d.png'%k))
