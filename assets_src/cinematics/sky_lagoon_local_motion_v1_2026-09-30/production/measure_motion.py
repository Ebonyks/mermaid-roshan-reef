"""Diagnostic silhouette motion, separate from RGB variation; never owner acceptance."""
import argparse,json
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parent
def measure(id):
 folder=ROOT/id
 images=[np.array(Image.open(p).convert('RGBA')) for p in sorted((folder/'isolated').glob('frame_*.png'))]
 masks=[a[:,:,3]>128 for a in images]
 y0=int(np.nonzero(masks[0])[0].min());y1=int(np.nonzero(masks[0])[0].max())
 upper_limit=y0+int((y1-y0)*.45)
 upper=[];bbox=[];brightness=[];disagreements=[]
 for a,m in zip(images,masks):
  ys,xs=np.nonzero(m);bbox.append([int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())])
  top=m.copy();top[upper_limit:]=False
  ty,tx=np.nonzero(top);upper.append([float(tx.mean()),float(ty.mean())])
  common=m&masks[0];brightness.append(float(a[:,:,:3][common].mean()))
  disagreements.append(float(np.count_nonzero(m^masks[0])/max(1,np.count_nonzero(m|masks[0]))))
 span=np.ptp(np.array(upper),axis=0).tolist()
 r={'id':id,'frames_measured':len(images),'cell':[256,256],'alpha_threshold':128,
    'upper_region_centroids':upper,'upper_centroid_span_px':span,'silhouette_bounds':bbox,
    'silhouette_disagreement_vs_first':disagreements,'common_silhouette_rgb_mean':brightness,
    'motion_readability_diagnostic':'INSPECT_MOTION' if max(span)>=4 else 'REJECT_OR_REVIEW_STATIC',
    'limitation':'Centroids and bounds cannot prove acting, topology or stable anchors; per-transition visual review still required. A machine render PASS alone is not motion acceptance.'}
 (folder/'MOTION_MEASUREMENT.json').write_text(json.dumps(r,indent=2),encoding='utf-8')
 print(json.dumps({'id':id,'upper_centroid_span_px':span,'rgb_mean_span':max(brightness)-min(brightness),'diagnostic':r['motion_readability_diagnostic']}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('id');measure(p.parse_args().id)
