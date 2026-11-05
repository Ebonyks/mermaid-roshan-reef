"""New garment meshes on the pinned bones; no seed vertex/weight is edited."""
from pathlib import Path
import json,math
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[1];rig=json.loads((R/'demo/rig.json').read_text())
bones=[b['name'] for b in rig['bones']]
chain=np.array([[534.8,475.46],[560.54,590.3],[564.5,708.44],[508.4,790.28],[434.48,793.58],[328.22,755.3]])
lengths=np.linalg.norm(np.diff(chain,axis=0),axis=1);cum=np.r_[0,np.cumsum(lengths)];centers=(cum[:-1]+cum[1:])/2


def weights(p,kind):
    w=dict.fromkeys(bones,0.)
    if kind in ['Torso','Head']:
        w[kind]=1.;return w
    x=np.array(p);best=1e30;s=0
    for i,(a,b) in enumerate(zip(chain,chain[1:])):
        t=float(np.clip(np.dot(x-a,b-a)/np.dot(b-a,b-a),0,1));q=a+t*(b-a);dist=np.dot(x-q,x-q)
        if dist<best:best=dist;s=float(cum[i]+t*lengths[i])
    g=np.exp(-.5*((s-centers)/90.)**2);g/=g.sum()
    torso=.80*math.exp(-(s/95.)**2)
    w['Torso']=torso
    for name,value in zip(['TailA','TailB','TailC','TailD','Fin'],g):w[name]=float(value*(1-torso))
    return w


def mesh(name,texture,kind,z=0):
    a=np.array(Image.open(R/'demo'/texture))[:,:,3];ys,xs=np.where(a>24)
    x0=max(0,int(xs.min())//8*8-8);x1=min(1024,(int(xs.max())//8+2)*8)
    y0=max(0,int(ys.min())//8*8-8);y1=min(1024,(int(ys.max())//8+2)*8)
    xx=list(range(x0,x1+1,8));yy=list(range(y0,y1+1,8));points=[[x,y] for y in yy for x in xx];tri=[];nx=len(xx)
    for j in range(len(yy)-1):
        for i in range(nx-1):k=j*nx+i;tri.extend([[k,k+1,k+nx],[k+1,k+nx+1,k+nx]])
    ww=[weights(p,kind) for p in points]
    return {'name':name,'texture':texture,'vertices':points,'triangles':tri,'weights':{b:[row[b] for row in ww] for b in bones},'z':z}


new=[]
for job in ['detective','geologist']:
    new.extend([mesh(job+'_body','art/'+job+'_body.png','Torso'),mesh(job+'_tail','art/'+job+'_tail.png','tail',-1)])
    audit=json.loads(json.dumps(rig));audit['meshes']=[m for m in audit['meshes'] if m['name']!='Headwear']
    audit['meshes'][0]['texture']='art/investigation_anatomy.png'
    audit['meshes']+=new[-2:]+[mesh(job+'_headwear','art/'+job+'_head.png','Head',1)]
    (R/'demo'/('audit_rig_'+job+'.json')).write_text(json.dumps(audit,separators=(',',':'))+'\n')
(R/'demo/garment_meshes.json').write_text(json.dumps({'contract':'roshan.canvas.shared@1.0.0','bones_unchanged':True,'method':'New garment vertices only. Torso/head rigid, tail smooth longitudinal Gaussian90px across the pinned authored tail chain, with a95px source waist blend. Original seed common vertices/weights untouched.','meshes':new},separators=(',',':'))+'\n')
print('NEW_GARMENT_BINDINGS',[(m['name'],len(m['vertices'])) for m in new])
