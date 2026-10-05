import sys, math; sys.path.insert(0,'.')
from common import *
from scipy import ndimage as ndi

def seg_frames(pts):
    out=[]
    for j in range(3):
        a,b=np.asarray(pts[j],float),np.asarray(pts[j+1],float); d=b-a; L=float(np.hypot(*d)); dh=d/L
        out.append((a,dh,np.array([-dh[1],dh[0]]),L))
    return out

def piecewise_map(tp, sp, X, Y, power=3.0, lead=(0.0,0.0,0.0)):
    """Backward map: output coords (X,Y) near target chain tp -> source coords near source chain sp.
    Each segment maps rigidly (with along-axis length ratio); maps are blended by inverse distance."""
    T=seg_frames(tp); S=seg_frames(sp)
    num_x=np.zeros_like(X); num_y=np.zeros_like(X); den=np.zeros_like(X)
    for j in range(3):
        a,dh,nh,L=T[j]; sa,sdh,snh,sL=S[j]
        rx=X-a[0]; ry=Y-a[1]
        u=(rx*dh[0]+ry*dh[1])/L; v=rx*nh[0]+ry*nh[1]
        mx=sa[0]+u*sL*sdh[0]+v*snh[0]; my=sa[1]+u*sL*sdh[1]+v*snh[1]
        uc=np.clip(u,0,1); dist=np.hypot(rx-uc*L*dh[0],ry-uc*L*dh[1])
        # distance along axis beyond the segment ends counts more, so joints blend smoothly
        w=1.0/(dist**2+1.0)**power
        num_x+=w*mx; num_y+=w*my; den+=w
    return num_x/den, num_y/den

def chain_dist(pts,X,Y):
    D=np.full(X.shape,1e9)
    for a,dh,nh,L in seg_frames(pts):
        rx=X-a[0]; ry=Y-a[1]; u=np.clip((rx*dh[0]+ry*dh[1]),0,L)
        D=np.minimum(D,np.hypot(rx-u*dh[0],ry-u*dh[1]))
    return D

def extend_root(arm, pts, back=0.45, u0=0.12):
    """Hidden underlay: replicate the upper-arm cross-section a little way back into the sleeve."""
    a,dh,nh,L=seg_frames(pts)[0]
    H,W=arm.shape[:2]; ys,xs=np.mgrid[0:H,0:W].astype(np.float32)
    rx=xs-a[0]; ry=ys-a[1]; u=(rx*dh[0]+ry*dh[1])/L; v=rx*nh[0]+ry*nh[1]
    # half-width at u0 from the arm alpha profile
    vs=np.arange(-12,12.5,0.5); px=a[0]+u0*L*dh[0]+vs*nh[0]; py=a[1]+u0*L*dh[1]+vs*nh[1]
    al=ndi.map_coordinates(arm[:,:,3],[py,px],order=1)
    inside=vs[al>0.5]; vlo,vhi=(inside.min(),inside.max()) if len(inside) else (-4,4)
    region=(u<u0)&(u>-back)&(v>vlo-0.5)&(v<vhi+0.5)
    sx=(a[0]+u0*L*dh[0]+v*nh[0]).astype(np.float32); sy=(a[1]+u0*L*dh[1]+v*nh[1]).astype(np.float32)
    src=np.stack([cv2.remap(arm[:,:,c],sx,sy,cv2.INTER_LINEAR) for c in range(4)],2)
    cap=np.zeros_like(arm); m=region&(arm[:,:,3]<0.95)
    cap[m]=src[m]
    return cap
