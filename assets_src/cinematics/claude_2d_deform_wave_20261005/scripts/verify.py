"""Machine checks for the packet. Writes verification.json; exits nonzero on any FAIL."""
import sys,os,hashlib; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from render import *
import aseprite_io
checks=[]
def chk(name,ok,detail=''):
    checks.append({'check':name,'result':'PASS' if ok else 'FAIL','detail':detail}); print(('PASS ' if ok else 'FAIL ')+name,detail)
atlas=open(ATLAS,'rb').read(); chk('approved atlas unchanged',hashlib.sha256(atlas).hexdigest()==ATLAS_SHA256,ATLAS_SHA256)
fr=[np.array(Image.open(P('frames','native','%04d.png'%f))) for f in range(N_FRAMES)]
chk('41 native frames, 256x256 RGBA',len(fr)==41 and all(a.shape==(256,256,4) for a in fr))
k0=(np.clip(load_key(0),0,1)*255+0.5).astype(np.uint8)
chk('frame 0 is the approved K0 cell verbatim',np.array_equal(fr[0],k0))
chk('frame 40 is the approved K0 cell verbatim (clean return to idle)',np.array_equal(fr[40],k0))
chk('no fully empty frame',all(a[:,:,3].max()>0 for a in fr))
# figure stays inside the cell (no clipping at the border)
edge=max(int(a[:,:,3][[0,-1],:].max()) for a in fr+[]); edge=max(edge,max(int(a[:,:,3][:,[0,-1]].max()) for a in fr))
chk('no alpha touches the 256 px cell border',edge==0,'max border alpha %d'%edge)
# determinism: re-render sample indices and compare pixels
for f in (3,9,17,22,31,37):
    a,_=render_frame(float(f),1,cv2.INTER_LINEAR); u=(np.clip(unpremul(a),0,1)*255+0.5).astype(np.uint8)
    chk('re-render frame %d is pixel-identical'%f,np.array_equal(u,fr[f]))
# root/scale continuity: waist landmark target fixed, inter-anchor distances stable
Qs=[body_targets(float(t)) for t in range(N_FRAMES)]
names=json.load(open(P('data','anchors.json')))['0']; idx={n:i for i,n in enumerate(names)}
wi=idx['waist']; dev=max(float(np.hypot(*(q[wi]-Qs[0][wi]))) for q in Qs)
chk('waist root target within 1 px of rest (Codex wave-study root tolerance)',dev<=1.0,'max %.3f px'%dev)
def dist(q,a,b): return float(np.hypot(*(q[idx[a]]-q[idx[b]])))
Kq=[reg(k,CP[k]) for k in range(4)]
for a,b in (('eyeL','eyeR'),('crown','waist'),('neck','waist'),('crown','neck')):
    d=[dist(q,a,b) for q in Qs]; kd=[dist(q,a,b) for q in Kq]
    ok=min(d)>=min(kd)-0.3 and max(d)<=max(kd)+0.3
    chk('%s-%s target distance stays inside the approved keys\' own range (+/-0.3 px; no scale drift beyond the drawings)'%(a,b),ok,
        'targets %.2f-%.2f px (p-p %.2f%%); keys %.2f-%.2f px'%(min(d),max(d),100*(max(d)-min(d))/d[0],min(kd),max(kd)))
m=aseprite_io.read(P('wave_master.aseprite'))
chk('Aseprite master: 41 frames, 256x256, 5 layers',len(m['frames'])==41 and m['W']==256 and m['H']==256 and len(m['layers'])==5)
chk('Aseprite master: final layer == exported PNG for every frame',all(np.array_equal(m['frames'][f]['final'],fr[f]) for f in range(N_FRAMES)))
chk('Aseprite master: 24 fps timing, 1708 ms total',sum(m['durations'])==1708,str(sum(m['durations'])))
src=json.load(open(P('data','frame_sources.json')))['frames']
chk('every frame records body/arm source drawing',len(src)==41 and all('body_source_key' in s and 'arm_source_key' in s for s in src))
json.dump({'checks':checks,'all_pass':all(c['result']=='PASS' for c in checks),
           'scope':'Machine checks only: no human identity/motion review, runtime, device, child or owner acceptance is implied.'},
          open(P('verification.json'),'w'),indent=1)
sys.exit(0 if all(c['result']=='PASS' for c in checks) else 1)
