"""Check actual sampled timing, attachment occupancy and falsifiable motion faults."""
import argparse
import json
from pathlib import Path
import numpy as np
from PIL import Image


def motion_metrics(records):
    times=np.array([r['time'] for r in records])
    dt=np.diff(times)
    velocities=[];accelerations=[]
    for name in records[0]['bones']:
        angles=np.unwrap([np.arctan2(r['bones'][name][1],r['bones'][name][0]) for r in records])
        velocity=np.rad2deg(np.diff(angles)/dt)
        acceleration=np.diff(velocity)/((dt[1:]+dt[:-1])/2)
        velocities.extend(abs(velocity));accelerations.extend(abs(acceleration))
    return {'max_angular_speed_deg_s':float(max(velocities)),'max_angular_acceleration_deg_s2':float(max(accelerations))}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('render');args=parser.parse_args();folder=Path(args.render)
    samples=json.loads((folder/'samples.json').read_text());report={}
    for clip in ['arm_bend','blink','tail_bend']:
        records=[r for r in samples if r['clip']==clip]
        metrics=motion_metrics(records)
        metrics['joint_min_alpha']={name:255 for name in ['LeftUpper','LeftFore','LeftHand']}
        for r in records:
            alpha=np.array(Image.open(folder/clip/f"{r['frame']:04}.png"))[:,:,3]
            for name in metrics['joint_min_alpha']:
                p=np.round(r['bones'][name][4:6]).astype(int)
                value=int(alpha[p[1]-1:p[1]+2,p[0]-1:p[0]+2].min())
                metrics['joint_min_alpha'][name]=min(metrics['joint_min_alpha'][name],value)
        first=records[0]['bones'];last=records[-1]['bones']
        metrics['endpoint_matrix_error']=max(abs(a-b) for name in first for a,b in zip(first[name],last[name]))
        metrics['closed_blink_frames']=sum(r['eyes_closed'] for r in records)
        metrics['half_blink_frames']=sum(r['eyes_half'] for r in records)
        metrics['double_lid_frames']=sum(r['eyes_closed'] and r['eyes_half'] for r in records)
        metrics['pass']=bool(metrics['max_angular_speed_deg_s']<140 and metrics['max_angular_acceleration_deg_s2']<650 and metrics['endpoint_matrix_error']<1e-5 and min(metrics['joint_min_alpha'].values())>192 and metrics['double_lid_frames']==0 and (clip!='blink' or metrics['closed_blink_frames']>=2))
        report[clip]=metrics
    bad=json.loads(json.dumps([r for r in samples if r['clip']=='arm_bend']))
    # An abrupt 90-degree pose jump must fail the same speed/acceleration check.
    m=bad[len(bad)//2]['bones']['LeftFore'];m[0],m[1],m[2],m[3]=-m[1],m[0],-m[3],m[2]
    injected=motion_metrics(bad)
    report['negative_controls']={'90_degree_pose_pop_detected':injected['max_angular_speed_deg_s']>=140,'measured_fault':injected}
    report['thresholds']={'angular_speed_deg_s':140,'angular_acceleration_deg_s2':650,'attachment_alpha_min':192,'endpoint_matrix_error':1e-5}
    report['limits']='Numerical smoothness/contact proxy only. No guarantee of natural acting; owner/device/child review pending.'
    report['pass']=all(report[c]['pass'] for c in ['arm_bend','blink','tail_bend']) and report['negative_controls']['90_degree_pose_pop_detected']
    (folder/'motion_audit.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
    raise SystemExit(0 if report['pass'] else 1)


if __name__=='__main__':main()
