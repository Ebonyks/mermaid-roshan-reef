"""Pick the single source drawing for every frame: one switch per beat, minimising how far the drawing
must bend plus the hidden-pixel gap it would open (both computed, not hand-picked)."""
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from render_whole import *
HOLE_WEIGHT=2.0     # one native pixel of gap costs as much as 2 degrees of extra bending
def bend(t,k):
    tp=arm_target(t); S,ang,L=arm_params(k)
    th=[math.degrees(math.atan2(*(tp[j+1]-tp[j])[::-1]))%360 for j in range(3)]
    return sum(abs(((th[j]-ang[j]+180)%360)-180)*w for j,w in enumerate((1,1,0.5)))
table={}; sched={}
for i in range(len(KNOT_T)-1):
    a,b=KNOT_K[i],KNOT_K[i+1]; ts=list(range(KNOT_T[i],KNOT_T[i+1]+1))
    for t in ts:
        for k in (a,b):
            _,h=render(float(t),k,want_hole=True); table[(t,k)]=(bend(t,k),int(h.sum()))
    cost=lambda t,k: table[(t,k)][0]+HOLE_WEIGHT*table[(t,k)][1]
    s=min(range(ts[0]+1,ts[-1]+1),key=lambda s: sum(cost(t,a) for t in ts if t<s)+sum(cost(t,b) for t in ts if t>=s))
    for t in ts: sched[t]=a if t<s else b
for t in range(N_FRAMES):
    if t<KNOT_T[0] or t>KNOT_T[-1]: sched[t]=0
json.dump({'rule':'one switch per beat; cost = bend degrees (upper arm, forearm, 0.5 x hand) + %.1f x gap pixels'%HOLE_WEIGHT,
           'source_key':{str(t):sched[t] for t in range(N_FRAMES)},
           'candidates':[{'frame':t,'key':k,'bend_deg':round(v[0],2),'gap_px':v[1]} for (t,k),v in sorted(table.items())]},
          open(P('data','schedule.json'),'w'),indent=1)
print('sources',[sched[t] for t in range(N_FRAMES)])
