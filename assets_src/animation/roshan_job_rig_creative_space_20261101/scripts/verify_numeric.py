"""Apply the seed's unmodified floors to original clips and new job actions."""
from pathlib import Path
import json,subprocess,sys,hashlib
import numpy as np
from PIL import Image
import audit_study as geometry
from audit_motion import motion_metrics

P=Path(__file__).resolve().parents[1]; RAW=P/'evidence/raw'; OUT=P/'evidence/numeric';OUT.mkdir(exist_ok=True)
rig=json.loads((P/'godot/rig.json').read_text()); summaries={}
for theme in ['original','ballet','magician','painter','astronaut']:
    r=json.loads(json.dumps(rig)); folder=RAW/theme
    r['meshes']=[m for m in r['meshes'] if m['name']!='GarmentExtension' or theme in ['painter','astronaut']]
    for mesh in r['meshes']:
        if mesh['name']=='Body':mesh['texture']=str(folder/'body_alpha.png')
        if mesh['name']=='UpperArm' and theme!='original':mesh['texture']='../art/upper_clean.png'
        if mesh['name']=='Headwear' and theme in ['painter','astronaut']:mesh['texture']='../art/'+theme+'_head.png'
        if mesh['name']=='GarmentExtension':mesh['texture']=str(folder/'extension_alpha.png')
    audit_rig=OUT/(theme+'_rig.json');audit_rig.write_text(json.dumps(r,separators=(',',':')))
    commands=[[sys.executable,str(P/'scripts/audit_study.py'),str(folder),'--rig',str(audit_rig)],
              [sys.executable,str(P/'scripts/audit_motion.py'),str(folder)]]
    codes=[]
    for number,args in enumerate(commands):
        result=subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        (OUT/(theme+'_'+str(number)+'.log')).write_bytes(result.stdout);codes.append(result.returncode)
    for f in folder.glob('*audit*.json'):(OUT/(theme+'_'+f.name)).write_bytes(f.read_bytes())
    summaries[theme]={'commands':commands,'exit_codes':codes,'passed':all(c==0 for c in codes)}
    print('ORIGINAL CLIP FLOORS',theme,summaries[theme]['passed'],flush=True)

jobs={}
for theme,clip in [('painter','paint_banner'),('astronaut','turn_valve')]:
    samples=json.loads((RAW/'jobs_isolated'/theme/'samples.json').read_text())
    original=json.loads((RAW/theme/'samples.json').read_text())[0]
    r=json.loads((OUT/(theme+'_rig.json')).read_text())
    folder=RAW/'jobs_isolated'/theme/clip
    reference=geometry.pixel_checks(Image.open(folder/'0000.png').convert('RGBA'))
    stats={'inverted_visible_triangles':0,'min_visible_stretch':1.0,'max_visible_stretch':1.0,'max_bone_scale_error':0.0,'rigid_head_distance_error_px':0.0,'pixel_seam_pass':True,'joint_min_alpha':{n:255 for n in ['LeftUpper','LeftFore','LeftHand']}}
    for mesh in r['meshes']:
        points=np.array(mesh['vertices']);tri=np.array(mesh['triangles']);weights=mesh['weights']
        rest_inverse=np.array([np.linalg.inv(geometry.affine(original['bones'][name])) for name in weights])
        alpha=np.array(Image.open(P/'godot'/mesh['texture']).convert('RGBA'))[:,:,3]
        centers=points[tri].mean(axis=1).astype(int)
        visible=alpha[np.clip(centers[:,1],0,1023),np.clip(centers[:,0],0,1023)]>192
        if not visible.any():
            stats[mesh['name']+'_opaque_visible_triangles']=0
            continue
        for row in samples:
            q,det,sv=geometry.geometry(points,tri,weights,rest_inverse,row)
            stats['inverted_visible_triangles']=max(stats['inverted_visible_triangles'],int(np.sum(det[visible]<=0)))
            stats['min_visible_stretch']=min(stats['min_visible_stretch'],float(sv[visible].min()))
            stats['max_visible_stretch']=max(stats['max_visible_stretch'],float(sv[visible].max()))
            head=points[:,1]<310
            if head.sum()>1:
                error=abs(np.linalg.norm(points[head][0]-points[head][-1])-np.linalg.norm(q[head][0]-q[head][-1]))
                stats['rigid_head_distance_error_px']=max(stats['rigid_head_distance_error_px'],float(error))
        geometry._GEOMETRY_CACHE.clear()
    for row in samples:
        picture=Image.open(folder/f"{row['frame']:04d}.png").convert('RGBA')
        stats['pixel_seam_pass'] &= geometry.seam_pass(geometry.pixel_checks(picture),reference)
        alpha=np.array(picture)[:,:,3]
        for name in stats['joint_min_alpha']:
            x,y=np.round(row['bones'][name][4:6]).astype(int)
            stats['joint_min_alpha'][name]=min(stats['joint_min_alpha'][name],int(alpha[y-1:y+2,x-1:x+2].min()))
        for name in row['bones']:
            scale_error=float(np.max(np.abs(np.linalg.svd(geometry.affine(row['bones'][name])[:2,:2],compute_uv=False)-1)))
            stats['max_bone_scale_error']=max(stats['max_bone_scale_error'],scale_error)
    stats.update(motion_metrics(samples))
    stats['endpoint_matrix_error']=max(abs(a-b) for name in samples[0]['bones'] for a,b in zip(samples[0]['bones'][name],samples[-1]['bones'][name]))
    stats['endpoint_rgba_exact']=Image.open(folder/'0000.png').tobytes()==Image.open(folder/'0150.png').tobytes()
    stats['passed']=bool(stats['inverted_visible_triangles']==0 and stats['min_visible_stretch']>=.8 and stats['max_visible_stretch']<=1.2 and stats['max_bone_scale_error']<1e-5 and stats['rigid_head_distance_error_px']<.01 and stats['pixel_seam_pass'] and min(stats['joint_min_alpha'].values())>192 and stats['max_angular_speed_deg_s']<140 and stats['max_angular_acceleration_deg_s2']<650 and stats['endpoint_matrix_error']<1e-5 and stats['endpoint_rgba_exact'])
    jobs[clip]=stats
    print('JOB FLOORS',clip,stats['passed'],flush=True)
result={'original_clips':summaries,'job_actions':jobs,'thresholds':'Unchanged seed floors: visible stretch .80–1.20; zero flips; scale <1e-5; rigid head <.01 px; one isolated actor, source holes +8 pixels; joint alpha >192; speed <140 deg/s; acceleration <650 deg/s2; exact endpoints. Fixed fixtures excluded only from the isolated actor seam view, and independently tested in full context.','limits':'Numerical floors do not establish natural acting, source identity acceptance, unsupported surfaces, device, child or owner review.'}
result['passed']=all(x['passed'] for x in summaries.values()) and all(x['passed'] for x in jobs.values())
(OUT/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
print('NUMERIC FLOORS',result['passed'],flush=True)
raise SystemExit(0 if result['passed'] else 1)
