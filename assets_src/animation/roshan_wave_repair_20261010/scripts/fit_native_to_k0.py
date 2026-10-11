"""Correspondence diagnosis only; does not edit images or accept pixels."""
from pathlib import Path
import cv2,numpy as np,json
ROOT=Path.cwd();P=ROOT/'assets_src/animation/roshan_wave_repair_20261010'
ref=cv2.imread(str(ROOT/'assets_src/animation/whole_sprite_pipeline_20261007/references/approved_K0.png'),cv2.IMREAD_UNCHANGED)
refgray=cv2.cvtColor(ref[:,:,:3],cv2.COLOR_BGR2GRAY);refgray[ref[:,:,3]<128]=236
sift=cv2.SIFT_create();a,da=sift.detectAndCompute(refgray,None);rows=[]
for frame in [0,4,34,40]:
 im=cv2.imread(str(P/f'native640_01/take_01/native_frames/{frame:04}.png'));g=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY);b,db=sift.detectAndCompute(g,None)
 pairs=cv2.BFMatcher().knnMatch(da,db,k=2);good=[m for m,n in pairs if m.distance<.7*n.distance]
 A=np.float32([a[m.queryIdx].pt for m in good]);B=np.float32([b[m.trainIdx].pt for m in good]);M,mask=cv2.estimateAffinePartial2D(A,B,method=cv2.RANSAC,ransacReprojThreshold=3)
 rows.append({'frame':frame,'matches':len(good),'inliers':int(mask.sum()),'matrix_k0_to_native':M.tolist(),'uniform_scale':float(np.hypot(M[0,0],M[1,0])),'mean_residual':float(np.mean(np.linalg.norm((A@M[:,:2].T+M[:,2])-B,axis=1)[mask[:,0]>0]))})
print(json.dumps(rows,indent=2));(P/'provenance/native_k0_registration_diagnostic.json').write_text(json.dumps(rows,indent=2)+'\n')
