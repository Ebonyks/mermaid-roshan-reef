"""Machine checks for the whole-frame packet. Writes verification.json; exits nonzero on any FAIL."""
import sys,os,hashlib; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from render_whole import *
import aseprite_io
checks=[]
def chk(name,ok,detail=''):
    checks.append({'check':name,'result':'PASS' if ok else 'FAIL','detail':detail}); print(('PASS ' if ok else 'FAIL ')+name,detail)
atlas=open(ATLAS,'rb').read(); chk('approved atlas unchanged',hashlib.sha256(atlas).hexdigest()==ATLAS_SHA256,ATLAS_SHA256)
fr=[np.array(Image.open(P('frames','native','%04d.png'%f))) for f in range(N_FRAMES)]
chk('41 native frames, 256x256 RGBA',len(fr)==41 and all(a.shape==(256,256,4) for a in fr))
k0=(np.clip(load_key(0),0,1)*255+0.5).astype(np.uint8)
rest=[f for f in range(N_FRAMES) if at_rest(f)]
chk('rest frames %s are the approved K0 cell verbatim'%rest,all(np.array_equal(fr[f],k0) for f in rest))
edge=max(max(int(a[:,:,3][[0,-1],:].max()),int(a[:,:,3][:,[0,-1]].max())) for a in fr)
chk('no alpha touches the 256 px cell border',edge==0,'max border alpha %d'%edge)
src=json.load(open(P('data','frame_sources.json')))['frames']; sch=schedule()
chk('every frame names exactly one source drawing, matching the schedule',len(src)==41 and all(s['source_key']==sch[s['index']] for s in src))
sw=[f for f in range(1,N_FRAMES) if sch[f]!=sch[f-1]]
chk('one drawing change per beat (4 in total)',len(sw)==4,'switch frames %s'%sw)
gaps=max(s['gap_px_filled'] for s in src)
chk('gap pixels filled per native frame <= 25 (same-frame fill only)',gaps<=25,'max %d px'%gaps)
for f in (5,9,13,20,24,30):
    a,_=frame(f,sch[f],1); u=(np.clip(unpremul(a),0,1)*255+0.5).astype(np.uint8); u[u[:,:,3]==0]=0
    chk('re-render frame %d is pixel-identical'%f,np.array_equal(u,fr[f]))
Qs=[body_targets(float(t)) for t in range(N_FRAMES)]
names=list(json.load(open(P('data','anchors.json')))['0'].keys()); idx={n:i for i,n in enumerate(names)}
wi=idx['waist']; dev=max(float(np.hypot(*(q[wi]-Qs[0][wi]))) for q in Qs)
chk('waist root target within 1 px of rest',dev<=1.0,'max %.3f px'%dev)
Kq=[reg(k,CP[k]) for k in range(4)]
def dist(q,a,b): return float(np.hypot(*(q[idx[a]]-q[idx[b]])))
for a,b in (('eyeL','eyeR'),('crown','waist'),('neck','waist'),('crown','neck')):
    d=[dist(q,a,b) for q in Qs]; kd=[dist(q,a,b) for q in Kq]
    chk("%s-%s target distance inside the approved keys' own range (+/-0.3 px)"%(a,b),min(d)>=min(kd)-0.3 and max(d)<=max(kd)+0.3,
        'targets %.2f-%.2f px; keys %.2f-%.2f px'%(min(d),max(d),min(kd),max(kd)))
m=aseprite_io.read(P('wave_master.aseprite'))
chk('Aseprite master: one layer, 41 whole cels equal to the exported PNGs',len(m['layers'])==1 and len(m['frames'])==41 and all(np.array_equal(m['frames'][f]['roshan_wave'],fr[f]) for f in range(N_FRAMES)))
chk('Aseprite master: 24 fps timing, 1708 ms total',sum(m['durations'])==1708,str(sum(m['durations'])))
json.dump({'checks':checks,'all_pass':all(c['result']=='PASS' for c in checks),
           'scope':'Machine checks only: no human identity/motion review, runtime, device, child or owner acceptance is implied.'},open(P('verification.json'),'w'),indent=1)
sys.exit(0 if all(c['result']=='PASS' for c in checks) else 1)
