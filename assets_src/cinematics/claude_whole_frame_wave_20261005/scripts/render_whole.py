"""Roshan wave, revision 2: whole-frame drawings.
Each output frame is ONE complete approved key drawing (K0..K3 of roshan_gesture_a.png row 0),
deformed as one figure toward the frame's target pose. No pixel from a second drawing, no layer
mixing between keys, no blending, no generated pixels. Every part follows the same timing curve."""
import sys, os, math, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from mls import mls_rigid_map, sample
from arm import piecewise_map, chain_dist, extend_root
from scipy import ndimage as ndi

N_FRAMES=41
KNOT_T=[3,7,17,27,36]          # rest, hand at shoulder, overhead, lowering, rest
KNOT_K=[0,1,2,3,0]
MLS_STEP=3

C=json.load(open(P('data','correspondences.json'))); CP={k:np.array(C[str(k)]) for k in range(4)}
ROOT={int(k):tuple(v) for k,v in json.load(open(P('data','roots.json'))).items()}
R=np.array(ROOT[0])
def reg(k,pts): return np.asarray(pts,float)-np.array(ROOT[k])+R

def hermite_weights(t):
    t=min(max(t,KNOT_T[0]),KNOT_T[-1]); n=len(KNOT_T)
    i=max(j for j in range(n-1) if KNOT_T[j]<=t) if t<KNOT_T[-1] else n-2
    t0,t1=KNOT_T[i],KNOT_T[i+1]; h=t1-t0; s=(t-t0)/h
    h00=2*s**3-3*s**2+1; h10=s**3-2*s**2+s; h01=-2*s**3+3*s**2; h11=s**3-s**2
    def tan(j):
        w=np.zeros(n)
        if 0<j<n-1:
            d=KNOT_T[j+1]-KNOT_T[j-1]; w[j+1]+=1/d; w[j-1]-=1/d
        return w
    w=np.zeros(n); w[i]+=h00; w[i+1]+=h01; w+=h10*h*tan(i)+h11*h*tan(i+1)
    return w
def interp(vals,t):
    w=hermite_weights(t); return sum(wi*np.asarray(v,float) for wi,v in zip(w,vals))

# ---- one pose curve for the whole figure ----
Qk=[reg(k,CP[k]) for k in KNOT_K]
def chain(k):
    a=ARM[k]; return [np.array(a[j],float) for j in ('shoulder','elbow','wrist','tip')]
def arm_params(k):
    S,E,Wr,T=chain(k); seg=[(S,E),(E,Wr),(Wr,T)]
    ang=[math.degrees(math.atan2(b[1]-a[1],b[0]-a[0]))%360 for a,b in seg]
    return reg(k,S), ang, [float(np.hypot(*(b-a))) for a,b in seg]
AP=[arm_params(k) for k in KNOT_K]
def body_targets(t): return interp(Qk,t)
def arm_target(t):
    S=interp([p[0] for p in AP],t)
    ang=[float(interp([p[1][j] for p in AP],t)) for j in range(3)]
    L=[float(interp([p[2][j] for p in AP],t)) for j in range(3)]
    pts=[S]
    for j in range(3):
        a=math.radians(ang[j]); pts.append(pts[-1]+L[j]*np.array([math.cos(a),math.sin(a)]))
    return pts

# ---- per-key regions of the SAME drawing (no donor pixels) ----
def load_png(p): return premul(np.array(Image.open(p)).astype(np.float32)/255)
ARML={k:load_png(W('arm_%d.png'%k)) for k in range(4)}
BODY={k:load_png(W('body_%d.png'%k)) for k in range(4)}      # this key's own pixels minus its arm
def _arm_residue(k):
    """Faint matte pixels of the arm (alpha < 0.5, next to the arm, outside the body silhouette) move with the arm."""
    a=BODY[k][:,:,3]; ao=np.load(W('armonly_%d.npy'%k))>0.5
    yy,xx=np.mgrid[-6:7,-6:7]; dk=(xx*xx+yy*yy)<=36
    inside=ndi.binary_fill_holes(ndi.binary_closing(a>0.5,dk))
    return (ndi.binary_dilation(ao,iterations=3)&(a>0)&~inside).astype(np.float32)[:,:,None]
for _k in range(4):
    _r=_arm_residue(_k); ARML[_k]=ARML[_k]+BODY[_k]*_r*(1-ARML[_k][:,:,3:4]); BODY[_k]=BODY[_k]*(1-_r)
CAP={k:extend_root(ARML[k],chain(k)) for k in range(4)}
def sleeve_overlay(k):
    im=load_key(k); sk=skin_mask(im); S=np.array(ARM[k]['shoulder']); ys,xs=np.mgrid[0:256,0:256]
    am=np.load(W('armmask_%d.npy'%k))>0.5
    hsv=cv2.cvtColor((im[:,:,:3]*255).astype(np.uint8),cv2.COLOR_RGB2HSV).astype(np.float32)
    sleeve=(hsv[:,:,0]>118)&(hsv[:,:,0]<170)&(hsv[:,:,1]>25)
    outline=(hsv[:,:,2]<140)&ndi.binary_dilation(sleeve,iterations=2)
    d=np.hypot(xs-S[0],ys-S[1])
    m=(d<11)&~am&(im[:,:,3]>0.02)&~sk&(sleeve|outline)
    if k==2: m|=(np.hypot(xs-88,ys-86)<6)&~am&(im[:,:,3]>0.02)&~sk
    m=ndi.gaussian_filter(m.astype(np.float32),0.6)*(d<11)
    return BODY[k]*m[:,:,None]
SLEEVE={k:sleeve_overlay(k) for k in range(4)}
def interior_hole(k):
    """Source pixels hidden behind this key's own arm that lie inside its body silhouette."""
    ao=np.load(W('armonly_%d.npy'%k))>0.5
    yy,xx=np.mgrid[-6:7,-6:7]; dk=(xx*xx+yy*yy)<=36
    inside=ndi.binary_fill_holes(ndi.binary_closing(BODY[k][:,:,3]>0.5,dk))
    return (ao&inside).astype(np.float32)
HOLE={k:interior_hole(k) for k in range(4)}

def over(top,bot): return top+bot*(1-top[:,:,3:4])
def grid(scale=1,canvas=None):
    if canvas is None:
        Wd=Hd=256*scale; ys,xs=np.mgrid[0:Hd,0:Wd]
        return Wd,Hd,((xs+0.5)/scale-0.5).astype(np.float32),((ys+0.5)/scale-0.5).astype(np.float32)
    Wd,Hd,s,tx,ty=canvas; ys,xs=np.mgrid[0:Hd,0:Wd]
    return Wd,Hd,((xs-tx)/s).astype(np.float32),((ys-ty)/s).astype(np.float32)

def render(t,k,scale=1,interp_mode=cv2.INTER_LINEAR,canvas=None,want_hole=False):
    Wd,Hd,X,Y=grid(scale,canvas)
    Qt=body_targets(t)
    st=MLS_STEP if Wd*Hd>300000 else 1
    if st>1:
        cx,cy=X[::st,::st],Y[::st,::st]
        bx,by=mls_rigid_map(Qt,CP[k],*cx.shape,XY=(cx,cy))
        bx=cv2.resize(bx,(Wd,Hd)); by=cv2.resize(by,(Wd,Hd))
        bx+=X-cv2.resize(cx,(Wd,Hd)); by+=Y-cv2.resize(cy,(Wd,Hd))
    else:
        bx,by=mls_rigid_map(Qt,CP[k],Hd,Wd,XY=(X,Y))
    body=sample(BODY[k],bx,by,interp=interp_mode); sleeve=sample(SLEEVE[k],bx,by,interp=interp_mode)
    tp=arm_target(t); sp=chain(k)
    ax,ay=piecewise_map(tp,sp,X,Y); ax=ax.astype(np.float32); ay=ay.astype(np.float32)
    keep=(chain_dist(tp,X,Y)<15)[:,:,None]
    arm=sample(ARML[k],ax,ay,interp=interp_mode)*keep; cap=sample(CAP[k],ax,ay,interp=interp_mode)*keep
    out=np.clip(over(sleeve,over(arm,over(body,cap))),0,1)
    if not want_hole: return out
    hole=(cv2.remap(HOLE[k],bx,by,cv2.INTER_LINEAR)>0.5)&(arm[:,:,3]<0.5)&(cap[:,:,3]<0.5)
    return out,hole

def schedule():
    d=json.load(open(P('data','schedule.json')))['source_key']; return {int(k):v for k,v in d.items()}
def at_rest(t): return t<=KNOT_T[0] or t>=KNOT_T[-1]
def fill_gaps(out,hole):
    """Close the few pixels this drawing's own arm hid, from the surrounding pixels of the same frame."""
    if not hole.any(): return out,0
    u=unpremul(out); rgb=(np.clip(u[:,:,:3],0,1)*255+0.5).astype(np.uint8)
    unknown=hole|((u[:,:,3]<0.5)&ndi.binary_dilation(hole,iterations=4))
    f=cv2.inpaint(rgb,unknown.astype(np.uint8)*255,3,cv2.INPAINT_TELEA).astype(np.float32)/255
    o=out.copy(); o[hole,:3]=f[hole]; o[hole,3]=1.0
    return o,int(hole.sum())
def frame(t,k,scale=1):
    """Whole frame t drawn from key k: native (scale 1, bilinear) or review (scale 3, bicubic)."""
    if at_rest(t):
        k0=premul(load_key(0))
        if scale==1: return k0,0
        Wd,Hd,X,Y=grid(scale); return np.clip(sample(k0,X,Y,interp=cv2.INTER_CUBIC),0,1),0
    out,h=render(float(t),k,scale,cv2.INTER_LINEAR if scale==1 else cv2.INTER_CUBIC,want_hole=True)
    return fill_gaps(out,h)

