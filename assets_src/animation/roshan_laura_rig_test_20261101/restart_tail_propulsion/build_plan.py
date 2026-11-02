"""Source-only diagonal view binding and tail-driven resistive-force trial."""
from pathlib import Path
import json
import math
import numpy as np

HERE = Path(__file__).resolve().parent
JOINTS = np.array([[119, 132], [109, 155], [96, 177], [78, 195], [59, 199], [34, 193]], dtype=float)
NAMES = ['TailA', 'TailB', 'TailC', 'TailD', 'Fin']
DT = 1 / 240
DURATION = 6.0


def smooth(x):
    x = np.clip(x, 0, 1)
    return x*x*x*(x*(x*6-15)+10)


def angles(t, disabled=False):
    if disabled:
        return np.zeros(5)
    env = smooth((t-.35)/.55) * (1-smooth((t-3.65)/.65))
    # A traveling flexion, proximal to distal. The chest never drives this wave.
    phases = np.array([0, .11, .22, .33, .43])
    result = np.deg2rad(np.array([4, 8, 10, 8, 0])) * env * np.sin(2*np.pi*(t-.35-phases)/1.40)
    # The fluke feathers against its local sweep, rather than simply following
    # the last joint as a rigid paddle. Its change of pitch supplies forward drag.
    def peduncle(at):
        e = smooth((at-.35)/.55) * (1-smooth((at-3.65)/.65))
        a = np.deg2rad(np.array([4,8,10,8,0])) * e * np.sin(2*np.pi*(at-.35-phases)/1.40)
        return centerline(a)[4]
    vy = float((peduncle(t+.001)[1]-peduncle(t-.001)[1])/.002)
    pitch = math.radians(22)*math.tanh(vy/80)
    rest = math.atan2(*(JOINTS[5]-JOINTS[4])[::-1])
    result[4] = env*(-math.pi-rest+pitch)-float(result[:4].sum())
    return result


def centerline(a):
    result = [JOINTS[0].copy()]
    theta = 0.0
    for i in range(5):
        theta += a[i]
        c, s = math.cos(theta), math.sin(theta)
        result.append(result[-1] + np.array([[c, -s], [s, c]]) @ (JOINTS[i+1]-JOINTS[i]))
    return np.array(result)


def solve(disabled=False):
    """Move only in response to tail/water force. No prescribed position curve."""
    records = []
    x = speed = 0.0
    previous = centerline(angles(0, disabled)) / 100
    mass, normal_drag, tangent_drag, body_drag = .32, 4.0, .25, 1.3
    for k in range(round(DURATION/DT)+1):
        t = k*DT
        a = angles(t, disabled)
        line = centerline(a) / 100
        mids = (line[1:]+line[:-1])*.5
        old_mids = (previous[1:]+previous[:-1])*.5
        shape_v = (mids-old_mids)/DT
        tangent = line[1:]-line[:-1]
        lengths = np.linalg.norm(tangent, axis=1)
        tangent /= lengths[:, None]
        normal = np.stack([-tangent[:, 1], tangent[:, 0]], axis=1)
        velocity = shape_v + np.array([speed, 0.0])
        vn = np.sum(velocity*normal, axis=1)
        vt = np.sum(velocity*tangent, axis=1)
        forces = -lengths[:, None]*(normal_drag*(vn*abs(vn))[:, None]*normal + tangent_drag*(vt*abs(vt))[:, None]*tangent)
        force = float(forces[:, 0].sum())
        drag = -body_drag*speed*abs(speed)
        acceleration = (force+drag)/mass
        if k % 8 == 0:
            records.append({'t':t, 'angles':dict(zip(NAMES, map(float, a))), 'x':x*100, 'speed':speed*100, 'tail_force':force, 'body_drag':drag})
        speed += acceleration*DT
        x += speed*DT
        previous = line
    return records


def binding():
    bones = [dict(name='Root', parent=None, head=[119,132], tail=[129,132]), dict(name='Torso', parent='Root', head=[119,132], tail=[139,95]), dict(name='Head', parent='Torso', head=[139,95], tail=[142,58])]
    arm = [('LeftUpper','Torso',[113,101],[88,120]),('LeftFore','LeftUpper',[88,120],[62,135]),('LeftHand','LeftFore',[62,135],[58,137]),('RightUpper','Torso',[147,103],[151,120]),('RightFore','RightUpper',[151,120],[164,139]),('RightHand','RightFore',[164,139],[168,144])]
    bones += [dict(name=n,parent=p,head=h,tail=t) for n,p,h,t in arm]
    for i,n in enumerate(NAMES):
        bones.append(dict(name=n,parent='Root' if i==0 else NAMES[i-1],head=JOINTS[i].tolist(),tail=JOINTS[i+1].tolist()))
    # Dense continuous whole-figure mesh. The upper figure remains one rigid plate.
    axis = list(range(0,256,3))+[256]
    points = np.array([[x,y] for y in axis for x in axis],dtype=float)
    n = len(axis)
    triangles=[]
    for y in range(n-1):
        for x in range(n-1):
            k=y*n+x
            triangles.extend([[k,k+1,k+n],[k+1,k+n+1,k+n]])
    weights={n:[0.0]*len(points) for n in ['Torso']+NAMES}
    # Tail region excludes the relaxed arms. Edges outside painted pixels are harmless.
    outline=np.array([[112,123],[138,133],[128,163],[111,184],[92,201],[75,207],[49,216],[6,216],[3,204],[24,194],[12,157],[32,156],[57,175],[69,187],[74,170],[78,149],[94,130]])
    def inside(p):
        x,y=p; odd=False
        for i in range(len(outline)):
            x1,y1=outline[i];x2,y2=outline[(i+1)%len(outline)]
            if (y1>y)!=(y2>y) and x < (x2-x1)*(y-y1)/(y2-y1)+x1: odd=not odd
        return odd
    lengths=np.linalg.norm(JOINTS[1:]-JOINTS[:-1],axis=1)
    cumulative=np.r_[0,np.cumsum(lengths)]
    anchors=np.r_[0,cumulative[:-1]]
    for k,p in enumerate(points):
        best=(float('inf'),0.0)
        for i in range(5):
            d=JOINTS[i+1]-JOINTS[i]
            u=float(np.clip(np.dot(p-JOINTS[i],d)/np.dot(d,d),0,1))
            dist=float(np.linalg.norm(p-(JOINTS[i]+u*d)))
            if dist<best[0]:best=(dist,cumulative[i]+u*lengths[i])
        s=best[1]
        # Smooth spatial influence everywhere. A hard tail outline produced
        # a comb tear in take01; painted connected surfaces cannot use a
        # binary bone assignment at the fin edge or waist.
        f=float(smooth(s/14)*(1-smooth((best[0]-34)/16))*smooth((p[1]-124)/12))
        weights['Torso'][k]=1-f
        i=int(np.clip(np.searchsorted(cumulative,s)-1,0,4))
        u=float(np.clip((s-cumulative[i])/lengths[i],0,1))
        if i==4:weights['Fin'][k]=f
        else:
            weights[NAMES[i]][k]=f*(1-u);weights[NAMES[i+1]][k]=f*u
        fin_gate=float(smooth((80-p[0])/20)*smooth((p[1]-145)/10))
        for name in weights:
            weights[name][k]*=1-fin_gate
        weights['Fin'][k]+=fin_gate
    return dict(bones=bones, meshes=[dict(name='SwimPose',texture='approved_swim_atlas.png',region=[512,512,256,256],z=0,vertices=points.tolist(),triangles=triangles,weights=weights)])


if __name__=='__main__':
    plan=solve()
    quiet=solve(True)
    (HERE/'plan.json').write_text(json.dumps(plan,separators=(',',':'))+'\n')
    (HERE/'view_binding.json').write_text(json.dumps(binding(),separators=(',',':'))+'\n')
    evidence={'method':'qualitative anisotropic planar drag; no prescribed position or root rotation', 'timestep':DT,'output_fps':30,'final_distance_native_px':plan[-1]['x'],'minimum_distance':min(x['x'] for x in plan),'maximum_distance':max(x['x'] for x in plan),'max_speed_native_px_s':max(abs(x['speed']) for x in plan),'tail_disabled_distance':quiet[-1]['x'],'tail_disabled_peak_speed':max(abs(x['speed']) for x in quiet),'scope':'Only causal-motion ablation; does not establish realistic fluid dynamics or visual acceptance.'}
    (HERE/'solver_evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
    print(json.dumps(evidence,indent=2))
