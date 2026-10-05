import numpy as np, cv2
def mls_rigid_map(p, q, H, W, scale=1.0, alpha=1.0, chunk=40000, eps=1e-8, XY=None):
    """Backward map for an output grid of HxW (in output pixel units = scale * canvas units).
    p: (N,2) control points in OUTPUT canvas coords (canvas units); q: (N,2) matching SOURCE coords.
    Returns map_x, map_y (source coords, canvas units) for each output pixel centre."""
    p=np.asarray(p,np.float64); q=np.asarray(q,np.float64)
    if XY is None:
        ys,xs=np.mgrid[0:H,0:W]
        v=np.stack([(xs.ravel()+0.5)/scale-0.5,(ys.ravel()+0.5)/scale-0.5],1)
    else:
        v=np.stack([XY[0].ravel(),XY[1].ravel()],1).astype(np.float64)
    out=np.empty_like(v)
    for s in range(0,len(v),chunk):
        vv=v[s:s+chunk]
        d=vv[:,None,:]-p[None,:,:]
        w=1.0/(np.sum(d*d,2)**alpha+eps)
        ws=w.sum(1,keepdims=True)
        ps=(w@p)/ws; qs=(w@q)/ws
        ph=p[None]-ps[:,None]; qh=q[None]-qs[:,None]
        vp=vv-ps
        # rigid: fr = sum w_i * [ (ph·vp) qh + (ph⊥·vp) qh⊥ ]  (equivalent closed form)
        a=np.sum(ph*vp[:,None,:],2)               # ph . vp
        b=ph[:,:,0]*vp[:,None,1]-ph[:,:,1]*vp[:,None,0]  # ph x vp
        fr0=np.sum(w*(a*qh[:,:,0]-b*qh[:,:,1]),1)
        fr1=np.sum(w*(a*qh[:,:,1]+b*qh[:,:,0]),1)
        n=np.sqrt(fr0**2+fr1**2)+eps
        L=np.linalg.norm(vp,axis=1)
        out[s:s+chunk,0]=L*fr0/n+qs[:,0]
        out[s:s+chunk,1]=L*fr1/n+qs[:,1]
    return out[:,0].reshape(H,W).astype(np.float32), out[:,1].reshape(H,W).astype(np.float32)

def mls_rigid_points(p,q,pts,alpha=1.0,eps=1e-8):
    """Forward-evaluate the MLS rigid deformation p->q at arbitrary points (canvas units)."""
    p=np.asarray(p,np.float64); q=np.asarray(q,np.float64); vv=np.asarray(pts,np.float64).reshape(-1,2)
    d=vv[:,None,:]-p[None]; w=1.0/(np.sum(d*d,2)**alpha+eps); ws=w.sum(1,keepdims=True)
    ps=(w@p)/ws; qs=(w@q)/ws; ph=p[None]-ps[:,None]; qh=q[None]-qs[:,None]; vp=vv-ps
    a=np.sum(ph*vp[:,None,:],2); b=ph[:,:,0]*vp[:,None,1]-ph[:,:,1]*vp[:,None,0]
    fr0=np.sum(w*(a*qh[:,:,0]-b*qh[:,:,1]),1); fr1=np.sum(w*(a*qh[:,:,1]+b*qh[:,:,0]),1)
    n=np.sqrt(fr0**2+fr1**2)+eps; L=np.linalg.norm(vp,axis=1)
    return np.stack([L*fr0/n+qs[:,0],L*fr1/n+qs[:,1]],1)

def sample(img_premul, mx, my, scale_src=1.0, interp=cv2.INTER_LINEAR):
    """Sample a premultiplied RGBA float image at source canvas coords (one spatial resample)."""
    return cv2.remap(img_premul, mx*scale_src, my*scale_src, interp, borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0,0))
