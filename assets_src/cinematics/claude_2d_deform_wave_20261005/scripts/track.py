import sys; sys.path.insert(0,__import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from common import *
from scipy import ndimage as ndi

def gray_on_bg(img):
    rgb=on_bg(premul(img),(128,128,128))
    return (cv2.cvtColor((rgb*255).astype(np.uint8),cv2.COLOR_RGB2GRAY))

def body(k):
    return np.array(Image.open(W('body_%d.png'%k))).astype(np.float32)/255

def match_point(g0,gk,p,off,half=7,search=26):
    x,y=int(round(p[0])),int(round(p[1]))
    T=g0[y-half:y+half+1,x-half:x+half+1]
    cx,cy=int(round(p[0]+off[0])),int(round(p[1]+off[1]))
    S=gk[cy-half-search:cy+half+search+1,cx-half-search:cx+half+search+1]
    r=cv2.matchTemplate(S,T,cv2.TM_CCOEFF_NORMED)
    _,mx,_,ml=cv2.minMaxLoc(r)
    # subpixel parabola
    dx=dy=0.0
    j,i=ml
    if 0<j<r.shape[1]-1:
        a,b,c=r[i,j-1],r[i,j],r[i,j+1]; den=a-2*b+c; dx=0.5*(a-c)/den if den!=0 else 0
    if 0<i<r.shape[0]-1:
        a,b,c=r[i-1,j],r[i,j],r[i+1,j]; den=a-2*b+c; dy=0.5*(a-c)/den if den!=0 else 0
    return (cx-search+j+dx, cy-search+i+dy), mx

if __name__=='__main__':
    B=[body(k) for k in range(4)]
    G=[gray_on_bg(b) for b in B]
    G=[np.pad(g,40,constant_values=128) for g in G]
    Pd=40
    waist0=(135.5,143.0)
    # coarse offsets from arm-free lower torso/tail patch (bodice V + waist band)
    roots={0:waist0}
    for k in range(1,4):
        best=None
        for guess in [(-14,0),(-44,0),(-48,0),(-30,0)]:
            q,s=match_point(G[0],G[k],(waist0[0]+Pd,waist0[1]+Pd),guess,half=12,search=30)
            if best is None or s>best[1]: best=(q,s)
        roots[k]=(best[0][0]-Pd,best[0][1]-Pd); print('root',k,roots[k],'score %.3f'%best[1])
    roots={k:(round(float(v[0]),2),round(float(v[1]),2)) for k,v in roots.items()}
    json.dump({str(k):v for k,v in roots.items()},open(P('data','roots.json'),'w'),indent=1)
