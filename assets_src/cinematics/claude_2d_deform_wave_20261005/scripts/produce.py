"""Render the 41 native 256 px frames (committed) and the 640x896 review frames (work dir, for videos)."""
import sys,time,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from render import *
fit=json.load(open(P('data','codex_canvas_fit.json')))
CV=(640,896,fit['scale'],fit['tx_640'],fit['ty_640'])
os.makedirs(W('review'),exist_ok=True)
log=[]; t0=time.time()
for f in range(N_FRAMES):
    if f in (0,N_FRAMES-1):
        # rest endpoints: the approved K0 cell itself (recomposition differs from it in 15 seam pixels)
        Image.fromarray((load_key(0)*255+0.5).astype(np.uint8),'RGBA').save(P('frames','native','%04d.png'%f))  # atlas bytes verbatim
        k0=premul(load_key(0))
        Wd,Hd,sc,tx,ty=CV; ys,xs=np.mgrid[0:Hd,0:Wd]
        b=sample(k0,((xs-tx)/sc).astype(np.float32),((ys-ty)/sc).astype(np.float32),interp=cv2.INTER_CUBIC)
        save_rgba(np.clip(b,0,1),W('review','%04d.png'%f))
        log.append({'index':f,'body_source_key':0,'arm_source_key':0,'method':'approved K0 cell verbatim (native); whole-canvas scale only (review)'})
        continue
    a,src=render_frame(float(f),1,cv2.INTER_LINEAR); save_rgba(a,P('frames','native','%04d.png'%f))
    b,_=render_frame(float(f),interp_mode=cv2.INTER_CUBIC,canvas=CV); save_rgba(b,W('review','%04d.png'%f))
    log.append({'index':f,'body_source_key':int(src[0]),'arm_source_key':int(src[1]),'method':'layered whole-figure 2D deformation'})
json.dump({'frames':log,'note':'K0..K3 = roshan_gesture_a.png row 0 columns 0..3'},open(P('data','frame_sources.json'),'w'),indent=1)
print('rendered %d frames in %.1fs'%(N_FRAMES,time.time()-t0))
