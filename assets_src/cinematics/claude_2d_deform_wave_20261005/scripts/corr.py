import sys; sys.path.insert(0,__import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from track import *
from mls import mls_rigid_points
from scipy import ndimage as ndi
B=[body(k) for k in range(4)]
G=[np.pad(gray_on_bg(b),40,constant_values=128) for b in B]
Pd=40
AO=[np.load(W('armonly_%d.npy'%k)) for k in range(4)]
anch=json.load(open(P('data','anchors.json')))
names=list(anch['0'].keys())
A0=np.array([anch['0'][n] for n in names])
a0=B[0][:,:,3]
# candidate points in K0
g0=gray_on_bg(B[0])
mask=(ndi.binary_dilation(a0>0.3,iterations=2)).astype(np.uint8)*255
feat=cv2.goodFeaturesToTrack(g0,400,0.01,5,mask=mask).reshape(-1,2)
cont,_=cv2.findContours(((a0>0.5)*255).astype(np.uint8),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
c=max(cont,key=len).reshape(-1,2)[::7].astype(np.float32)
cand=np.concatenate([A0,feat,c],0)
# drop candidates near K0 arm hole
holedist=ndi.distance_transform_edt(AO[0]<0.5)
keep=[i for i,(x,y) in enumerate(cand) if i<len(A0) or holedist[int(y),int(x)]>6]
cand=cand[keep]
print('candidates',len(cand))
tracks={0:cand.copy()}; valid=np.ones(len(cand),bool)
for k in range(1,4):
    Ak=np.array([anch[str(k)][n] for n in names])
    pred=mls_rigid_points(A0,Ak,cand)
    hd=ndi.distance_transform_edt(AO[k]<0.5)
    out=np.zeros_like(pred)
    for i,(p,pr) in enumerate(zip(cand,pred)):
        if i<len(A0): out[i]=Ak[i]; continue
        q,s=match_point(G[0],G[k],(p[0]+Pd,p[1]+Pd),(pr[0]-p[0],pr[1]-p[1]),half=6,search=5)
        q=(q[0]-Pd,q[1]-Pd); out[i]=q
        bad=(s<0.72) or np.hypot(q[0]-pr[0],q[1]-pr[1])>4.5 or not(0<q[0]<255 and 0<q[1]<255) or hd[int(q[1]),int(q[0])]<6
        if bad: valid[i]=False
    tracks[k]=out
print('valid in all',valid.sum())
# local consistency filter: displacement vs neighbours (K0->Kk), in every key
for it in range(2):
    idx=np.nonzero(valid)[0]
    for k in range(1,4):
        D=tracks[k][idx]-cand[idx]
        for j,i in enumerate(idx):
            dd=np.hypot(*(cand[idx]-cand[i]).T); nb=(dd<18)&(dd>0)
            if nb.sum()>=3:
                med=np.median(D[nb],0)
                if np.hypot(*(D[j]-med))>3.0 and i>=len(A0): valid[i]=False
print('after filter',valid.sum())
out={str(k):tracks[k][valid].tolist() for k in range(4)}
out['is_anchor']=[bool(i<len(A0)) for i in np.nonzero(valid)[0]]
json.dump(out,open(P('data','correspondences.json'),'w'))
