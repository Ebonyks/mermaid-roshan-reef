import sys; sys.path.insert(0,__import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from common import *
from mls import mls_rigid_map, sample
from scipy import ndimage as ndi
C=json.load(open(P('data','correspondences.json')))
CP={k:np.array(C[str(k)]) for k in range(4)}
AO=[np.load(W('armonly_%d.npy'%k)) for k in range(4)]
BODY=[premul(np.array(Image.open(W('body_%d.png'%k))).astype(np.float32)/255) for k in range(4)]
DONORS={0:[2,3],1:[0,2],2:[0,3],3:[0,2]}
for k in range(4):
    hole=ndi.binary_dilation(AO[k]>0.5,iterations=1)
    yy,xx=np.mgrid[-6:7,-6:7]; dk=(xx*xx+yy*yy)<=36
    inside=ndi.binary_closing(BODY[k][:,:,3]>0.5,dk,iterations=1)
    inside=ndi.binary_fill_holes(inside)
    hole=hole&inside
    filled=BODY[k].copy()
    need=hole.copy()
    for d in DONORS[k]:
        mx,my=mls_rigid_map(CP[k],CP[d],256,256)
        don=sample(BODY[d],mx,my)
        dhole=cv2.remap(ndi.binary_dilation(AO[d]>0.5,iterations=2).astype(np.float32),mx,my,cv2.INTER_LINEAR)
        use=need&(dhole<0.01)
        # composite donor under existing body pixels inside the hole (body over donor)
        sel=use[:,:,None]
        comp=filled+don*(1-filled[:,:,3:4])
        filled=np.where(sel,comp,filled)
        need=need&~use
    a=filled[:,:,3]>0.02
    lab,n=ndi.label(a); sz=ndi.sum(np.ones_like(filled[:,:,3]),lab,range(1,n+1))
    small=np.isin(lab,1+np.nonzero(sz<30)[0])
    filled[small]=0
    print(k,'unfilled hole px',int(need.sum()),'fragments removed',int(small.sum()))
    np.save(W('bodyfill_%d.npy'%k),filled)
    save_rgba(filled,P('layers','body_fill_k%d.png'%k))
