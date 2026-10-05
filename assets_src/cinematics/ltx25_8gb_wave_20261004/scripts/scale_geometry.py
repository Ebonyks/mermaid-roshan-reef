"""Root-constrained multi-anchor fit; never edits image pixels."""
import numpy as np
def fit(src,tgt):
 names=list(tgt)
 X=np.array([src[n] for n in names]);Y=np.array([tgt[n] for n in names]);root_index=names.index('bodice_waist_tip');xc=X-X[root_index];yc=Y-Y[root_index];s=float(np.sum(xc*yc)/np.sum(xc*xc));t=Y[root_index]-s*X[root_index];err=np.linalg.norm(s*X+t-Y,axis=1);pairs={}
 for a,b in [('image_left_eye','image_right_eye'),('crown_gem','image_left_eye'),('crown_gem','image_right_eye'),('crown_gem','bodice_waist_tip'),('neck_base','bodice_waist_tip')]:pairs[a+'__'+b]=float(s*np.linalg.norm(X[names.index(a)]-X[names.index(b)])/np.linalg.norm(Y[names.index(a)]-Y[names.index(b)]))
 grid=round(64*s);actual=grid/64;placement=np.round(Y[root_index]-actual*X[root_index]).astype(int)
 return {'uniform_scale':s,'translation':t.tolist(),'fit_constraint':'Waist fixed at root; remaining four landmarks jointly estimate a single scale. No rotation or limb warp.','max_anchor_residual_px':float(err.max()),'anchor_residuals_px':dict(zip(names,err.tolist())),'pair_scale_ratios':pairs,'pass':bool(err.max()<=6 and all(abs(v-1)<=.03 for v in pairs.values())),'scaled_canvas':[9*grid,13*grid],'raster_uniform_scale':actual,'placement':placement.tolist()}
