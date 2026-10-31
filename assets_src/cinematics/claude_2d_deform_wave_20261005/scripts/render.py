"""Roshan wave — whole-figure 2D deformation study (no generative model, no blending).
Every output pixel is ONE spatial resample of ONE approved key drawing (arm, body or sleeve layer)."""
import sys, math, os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
from mls import mls_rigid_map, mls_rigid_points, sample
from scipy import ndimage as ndi
from arm import piecewise_map, chain_dist, extend_root

N_FRAMES=41
KNOT_T=[3,7,17,27,36]            # rest, hand at shoulder, overhead, lowering, rest (Codex timeline)
KNOT_K=[0,1,2,3,0]
BODY_SCHEDULE=[(5,0),(32,2),(99,0)]   # body drawing: K0 until 5, K2 (open smile) until 32, then K0
DRAG=(0.0,1.2,2.0)                 # frames the forearm / hand trail the upper arm
MLS_STEP=3                         # coarse-grid step for large canvases (coordinates only)

C=json.load(open(P('data','correspondences.json'))); CP={k:np.array(C[str(k)]) for k in range(4)}
ROOT={int(k):tuple(v) for k,v in json.load(open(P('data','roots.json'))).items()}
R=np.array(ROOT[0])
def reg(k,pts): return np.asarray(pts,float)-np.array(ROOT[k])+R

# ---------- interpolation (non-uniform Catmull-Rom Hermite, zero tangent at rest knots) ----------
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

# ---------- body geometry ----------
Qk=[reg(k,CP[k]) for k in KNOT_K]          # registered body points per knot
P0=CP[0]
def region_lag(p):
    x,y=p
    if y>165 and x>165: return 4.0, 'fin'
    if y>185: return 2.0, 'tail'
    if x>160 and y<100: return 3.0, 'pony'
    if y<95 and (x<125 or x>156) : return 1.5, 'hair'
    if x>155 and 100<y<170: return 2.0, 'oarm'
    return 0.0, 'core'
LAG=[region_lag(p) for p in P0]
def body_targets(t):
    out=np.zeros_like(Qk[0])
    for i,(lag,kind) in enumerate(LAG):
        g=interp([q[i] for q in Qk],t-lag)
        if kind in ('pony','fin'):   # follow-through: carry a little of the lagged velocity, settled by the last frame
            g=g+0.5*min(1.0,max(0.0,(N_FRAMES-1-t)/3.0))*(g-interp([q[i] for q in Qk],t-lag-2))
        out[i]=g
    # anticipation (frames 0-4): tiny lean toward the waving side, then release
    b=(math.sin(math.pi*t/4.0)**2 if 0<=t<=4 else 0.0)
    neck=R+np.array([5.5,-50])
    up=out[:,1]<R[1]-4
    ang=math.radians(-0.9*b)
    rot=np.array([[math.cos(ang),-math.sin(ang)],[math.sin(ang),math.cos(ang)]])
    out[up]=(out[up]-R)@rot.T+R
    # head tilt toward the raised hand while it is overhead
    tilt=math.radians(-2.2)*max(0,min(1,(t-8)/6))*max(0,min(1,(31-t)/6))
    head=P0[:,1]<90
    rot=np.array([[math.cos(tilt),-math.sin(tilt)],[math.sin(tilt),math.cos(tilt)]])
    hn=out[head]; pivot=np.mean(out[[i for i in range(len(P0)) if abs(P0[i,1]-93)<4 and abs(P0[i,0]-141)<10]],0) if True else neck
    out[head]=(hn-pivot)@rot.T+pivot
    return out

# ---------- arm geometry ----------
def chain(k):
    a=ARM[k]; return [np.array(a[j],float) for j in ('shoulder','elbow','wrist','tip')]
def arm_params(k):
    S,E,W,T=chain(k)
    seg=[(S,E),(E,W),(W,T)]
    ang=[math.degrees(math.atan2(b[1]-a[1],b[0]-a[0]))%360 for a,b in seg]
    L=[float(np.hypot(*(b-a))) for a,b in seg]
    return reg(k,S), ang, L
AP=[arm_params(k) for k in KNOT_K]
def arm_target(t):
    S=interp([p[0] for p in AP],t)
    ang=[float(interp([p[1][j] for p in AP],t-DRAG[j])) for j in range(3)]
    L=[float(interp([p[2][j] for p in AP],t-DRAG[j])) for j in range(3)]
    b=(math.sin(math.pi*t/4.0)**2 if 0<=t<=4 else 0.0)               # anticipation: arm tucks in slightly
    ang[0]-=4*b; ang[1]-=5*b; S=S+np.array([0,0.8*b])
    pts=[S]
    for j in range(3):
        a=math.radians(ang[j]); pts.append(pts[-1]+L[j]*np.array([math.cos(a),math.sin(a)]))
    return pts
def arm_handles(pts):
    """Handles along shoulder->elbow->wrist->tip plus perpendicular width handles."""
    H=[]
    fr=[[0,.25,.5,.75],[0,.25,.5,.75],[0,.33,.66,1.0]]
    wid=[4.0,3.5,5.0]
    for j in range(3):
        a,b=pts[j],pts[j+1]; d=b-a; n=np.array([-d[1],d[0]])/(np.hypot(*d)+1e-9)
        for f in fr[j]: H.append(a+f*d)
        m=a+0.5*d; H.append(m+wid[j]*n); H.append(m-wid[j]*n)
    return np.array(H)
def seg_dist(pts,X,Y):
    D=np.full(X.shape,1e9)
    for j in range(3):
        a,b=pts[j],pts[j+1]; d=b-a; L2=d@d
        u=np.clip(((X-a[0])*d[0]+(Y-a[1])*d[1])/L2,0,1)
        D=np.minimum(D,np.hypot(X-(a[0]+u*d[0]),Y-(a[1]+u*d[1])))
    return D

# ---------- layers ----------
BODY={k:np.load(W('bodyfill_%d.npy'%k)) for k in range(4)}
ARML={k:premul(np.array(Image.open(W('arm_%d.png'%k))).astype(np.float32)/255) for k in range(4)}
# hidden shoulder cap: drawn UNDER the body so it only fills the armpit gap when the arm rotates
ARMCAP={k:extend_root(ARML[k],[np.array(ARM[k][j],float) for j in ('shoulder','elbow','wrist','tip')]) for k in range(4)}
def sleeve_overlay(k,lock=True):
    im=load_key(k); sk=skin_mask(im)
    S=np.array(ARM[k]['shoulder']); ys,xs=np.mgrid[0:256,0:256]
    near=np.hypot(xs-S[0],ys-S[1])<9
    am=np.load(W('armmask_%d.npy'%k))>0.5
    hsv=cv2.cvtColor((im[:,:,:3]*255).astype(np.uint8),cv2.COLOR_RGB2HSV).astype(np.float32)
    sleeve=(hsv[:,:,0]>118)&(hsv[:,:,0]<170)&(hsv[:,:,1]>25)
    outline=(hsv[:,:,2]<140)&ndi.binary_dilation(sleeve,iterations=2)
    near2=np.hypot(xs-S[0],ys-S[1])
    m=(near2<11)&~am&(im[:,:,3]>0.02)&~sk&(sleeve|outline)
    if k==2 and lock:
        m|=(np.hypot(xs-88,ys-86)<6)&~am&(im[:,:,3]>0.02)&~sk
    near=near2<11
    m=ndi.gaussian_filter(m.astype(np.float32),0.6)*(near)
    return BODY[k]*m[:,:,None]
SLEEVE={k:sleeve_overlay(k) for k in range(4)}
SLEEVE_NOLOCK={k:sleeve_overlay(k,lock=False) for k in range(4)}

def source_key(t):
    for sw,k in BODY_SCHEDULE:
        if t<sw: return k
    return 0

def arm_source(t):
    tp=arm_target(t)
    th=[math.degrees(math.atan2(*(tp[j+1]-tp[j])[::-1]))%360 for j in range(3)]
    L1=float(np.hypot(*(tp[1]-tp[0])))
    seg=max(i for i in range(len(KNOT_T)-1) if KNOT_T[i]<=min(max(t,KNOT_T[0]),KNOT_T[-1]-1e-6))
    best=None
    for k in (KNOT_K[seg],KNOT_K[seg+1]):
        S,ang,L=arm_params(k)
        c=sum(abs(((th[j]-ang[j]+180)%360)-180)*wt for j,wt in enumerate((1,1,0.5)))+1.5*abs(L1-L[0])
        if best is None or c<best[0]: best=(c,k)
    return best[1]

def over(top,bot): return top+bot*(1-top[:,:,3:4])

def render_frame(t,scale=1,interp_mode=cv2.INTER_LINEAR,canvas=None,return_layers=False):
    """canvas=None: square 256*scale grid. canvas=(W,H,s,tx,ty): output pixel (xo,yo) shows cell point ((xo-tx)/s,(yo-ty)/s)."""
    k=source_key(t)
    if canvas is None:
        W=H=256*scale
        ys,xs=np.mgrid[0:H,0:W]; X=((xs+0.5)/scale-0.5).astype(np.float32); Y=((ys+0.5)/scale-0.5).astype(np.float32)
    else:
        W,H,s,tx,ty=canvas
        ys,xs=np.mgrid[0:H,0:W]; X=((xs-tx)/s).astype(np.float32); Y=((ys-ty)/s).astype(np.float32)
    # body: target registered points -> this key's own points
    Qt=body_targets(t)
    st=MLS_STEP if (W*H)>300000 else 1
    if st>1:   # deformation field is smooth: solve on a coarse grid, upsample coordinates only
        cx,cy=X[::st,::st],Y[::st,::st]
        bx,by=mls_rigid_map(Qt,CP[k],*cx.shape,XY=(cx,cy))
        bx=cv2.resize(bx,(W,H),interpolation=cv2.INTER_LINEAR); by=cv2.resize(by,(W,H),interpolation=cv2.INTER_LINEAR)
        # resize aligns the sub-grid corners; correct with the exact affine relation of the grid
        gx=cv2.resize(cx,(W,H),interpolation=cv2.INTER_LINEAR); gy=cv2.resize(cy,(W,H),interpolation=cv2.INTER_LINEAR)
        bx=bx+(X-gx); by=by+(Y-gy)
    else:
        bx,by=mls_rigid_map(Qt,CP[k],H,W,XY=(X,Y))
    body=sample(BODY[k],bx,by,scale_src=1.0,interp=interp_mode)
    sleeve=sample(SLEEVE[k],bx,by,scale_src=1.0,interp=interp_mode)
    ka=arm_source(t); tp=arm_target(t); sp=chain(ka)
    ax,ay=piecewise_map(tp,sp,X,Y)
    axf,ayf=ax.astype(np.float32),ay.astype(np.float32)
    arm=sample(ARML[ka],axf,ayf,scale_src=1.0,interp=interp_mode)
    cap=sample(ARMCAP[ka],axf,ayf,scale_src=1.0,interp=interp_mode)
    keep=(chain_dist(tp,X,Y)<15)
    arm=arm*keep[:,:,None]; cap=cap*keep[:,:,None]
    if ka!=2 and k==2:   # K2's front hair lock only belongs over K2's own raised arm root
        sleeve=sample(SLEEVE_NOLOCK[k],bx,by,scale_src=1.0,interp=interp_mode)
    out=over(sleeve,over(arm,over(body,cap)))
    if return_layers:
        return np.clip(out,0,1), (k,ka), {'cap':np.clip(cap,0,1),'body':np.clip(body,0,1),'arm':np.clip(arm,0,1),'sleeve':np.clip(sleeve,0,1)}
    return np.clip(out,0,1), (k,ka)
