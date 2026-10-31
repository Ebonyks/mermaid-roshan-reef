"""Render the 41 native whole frames (committed) and 3x review frames (work dir)."""
import sys,os,time; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from render_whole import *
SCHED=schedule(); os.makedirs(W('review'),exist_ok=True); log=[]; t0=time.time()
for f in range(N_FRAMES):
    k=SCHED[f]
    if at_rest(f):
        Image.fromarray((load_key(0)*255+0.5).astype(np.uint8),'RGBA').save(P('frames','native','%04d.png'%f))  # atlas bytes verbatim
        b,_=frame(f,0,3); save_rgba(b,W('review','%04d.png'%f))
        log.append({'index':f,'source_key':0,'method':'approved K0 cell verbatim (rest)','gap_px_filled':0}); continue
    a,n=frame(f,k,1); save_rgba(a,P('frames','native','%04d.png'%f))
    b,_=frame(f,k,3); save_rgba(b,W('review','%04d.png'%f))
    log.append({'index':f,'source_key':k,'method':'one complete key drawing deformed as one figure','gap_px_filled':n})
json.dump({'frames':log,'note':'K0..K3 = roshan_gesture_a.png row 0 columns 0..3; every frame uses exactly one of them'},open(P('data','frame_sources.json'),'w'),indent=1)
print('rendered %d frames in %.0fs'%(N_FRAMES,time.time()-t0))
