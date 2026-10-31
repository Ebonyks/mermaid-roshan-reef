"""Strong body anchors on K0 (annotated) matched into K1-K3 by template matching on arm-free body layers."""
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from track import *
B=[body(k) for k in range(4)]
G=[np.pad(gray_on_bg(b),40,constant_values=128) for b in B]
Pd=40
roots={int(k):tuple(v) for k,v in json.load(open(P('data','roots.json'))).items()}
# K0 anchors annotated by eye on the approved cell (256 px coordinates)
anch={'crown':(145,25),'eyeL':(130,63.6),'eyeR':(153,63.6),'mouth':(142,75.7),'waist':(135.5,143),
      'ohand':(180,157),'oelbow':(167,127),'finT':(220,172),'finB':(238,221),'tailjx':(178,226),'tailbot':(150,228),
      'ptail':(200,72),'neck':(141,93)}
res={0:anch}
for k in range(1,4):
    off0=(roots[k][0]-roots[0][0],roots[k][1]-roots[0][1]); res[k]={}
    for n,p in anch.items():
        q,s=match_point(G[0],G[k],(p[0]+Pd,p[1]+Pd),off0,half=9,search=28); res[k][n]=(float(q[0]-Pd),float(q[1]-Pd))
json.dump(res,open(P('data','anchors.json'),'w'),indent=1)
