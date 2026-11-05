"""Measure native captures, keep fit failures, and build inspectable boards.

No artwork repair or score promotion is performed by this analysis.
"""
from pathlib import Path
import json, hashlib, sys, shutil
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
from seed_geometry import pixel_checks, seam_pass, affine
from seed_motion import motion_metrics

R=Path(__file__).resolve().parents[1]
RAW=R/'evidence/raw_frames_v6'
E=R/'evidence'; REVIEW=R/'review'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
load=lambda p:json.loads(p.read_text())


def pixels(path):
    return np.array(Image.open(path).convert('RGBA'))


def changed(a,b):
    return int(np.any(pixels(a)!=pixels(b),axis=2).sum())


def board(paths,out,labels=None):
    size=256; cols=4; rows=(len(paths)+3)//4
    canvas=Image.new('RGB',(cols*size,rows*(size+24)),(28,34,47))
    draw=ImageDraw.Draw(canvas)
    for n,p in enumerate(paths):
        tile=Image.new('RGBA',(1024,1024),(235,239,242,255))
        tile.alpha_composite(Image.open(p).convert('RGBA'))
        tile=tile.convert('RGB').resize((size,size),Image.Resampling.LANCZOS)
        x=n%cols*size;y=n//cols*(size+24);canvas.paste(tile,(x,y))
        draw.text((x+6,y+size+4),(labels[n] if labels else p.stem)[:42],fill='white')
    canvas.save(out,quality=94)


def main():
    results={}; frame_index={}
    for job in ['detective','geologist']:
        folder=RAW/job
        
        if not (folder/'work_samples.json').exists():shutil.copy2(folder/'samples.json',folder/'work_samples.json')
        work=load(folder/'work_samples.json')
        metrics=motion_metrics(work)
        records=load(folder/'samples_regression.json')
        (folder/'samples.json').write_text(json.dumps(records)+'\n')
        (folder/'stress_samples.json').write_text(json.dumps(records)+'\n')
        max_scale=max(float(np.abs(np.linalg.svd(affine(row['bones'][name])[:2,:2],compute_uv=False)-1).max()) for row in work for name in row['bones'])
        contacts=[r for r in work if r['contact_active']]
        faults={}
        for name in ['grip_slip','fixture_drift','identity_scale','original_underlay']:
            p=folder/f'fault_{name}.json';d=load(p)
            (E/'controls').mkdir(exist_ok=True)
            shutil.copy2(p,E/'controls'/f'{job}_{p.name}')
            shutil.copy2(folder/f'fault_{name}.png',E/'controls'/f'{job}_fault_{name}.png')
            if name=='grip_slip':detected=d['grip_error_px']>3
            elif name=='fixture_drift':detected=d['fixture_drift_px']>2
            elif name=='identity_scale':detected=max(abs(np.linalg.svd(affine(d['bones']['Head'])[:2,:2],compute_uv=False)-1))>.1
            else:detected=changed(folder/'0069.png',folder/f'fault_{name}.png')>1000
            faults[name]={'detected':bool(detected),'changed_pixels':changed(folder/'0069.png',folder/f'fault_{name}.png')}
        samples=[]
        for clip in ['arm_bend','blink','tail_bend']:
            pp=sorted((folder/clip).glob('[0-9]*.png'))
            samples.extend(pp)
        samples+=sorted(folder.glob('[0-9]*.png'))
        frame_index[job]=[{'path':str(p.relative_to(RAW)).replace('\\','/'),'png_sha256':sha(p),'rgba_sha256':hashlib.sha256(pixels(p).tobytes()).hexdigest()} for p in samples]
        durations={'contact_begin_s':min(r['time'] for r in contacts),'contact_end_s':max(r['time'] for r in contacts),'contact_frames':len(contacts)}
        source=E/'source_controls_v4'
        poison=changed(source/f'{job}_normal.png',source/f'{job}_poison_old_source.png')
        reinsert=changed(source/f'{job}_normal.png',source/f'{job}_reinsert_old_underlay.png')
        results[job]={'work_frames':len(work),'motion':metrics,'max_bone_scale_error':max_scale,'max_grip_error_native_px':max(r['grip_error_px'] for r in work),'max_fixture_drift_native_px':max(r['fixture_drift_px'] for r in work),'contact':durations,'layer_ownership_correct':all(r['tool_z']<r['fingers_z'] for r in work),'faults':faults,'source_poison_changed_pixels':poison,'old_underlay_reinsertion_changed_pixels':reinsert,'machine_contact_pass':bool(max(r['grip_error_px'] for r in work)<=3 and max(r['fixture_drift_px'] for r in work)<=2 and len(contacts)>=60 and max_scale<1e-5 and metrics['max_angular_speed_deg_s']<140 and metrics['max_angular_acceleration_deg_s2']<650 and all(v['detected'] for v in faults.values()) and poison==0 and reinsert>100),'limits':'Contact is independently rendered but uses authored sockets. Natural gripping fingers, brush support and acting require exact human review. Front view only; no facing change acceptance.'}
        board([folder/f'{i:04d}.png' for i in [0,20,39,48,60,69,90,105,120,135,171,192]],REVIEW/f'{job}_work_board.jpg',[f'{job} {i}/30s' for i in [0,20,39,48,60,69,90,105,120,135,171,192]])
        (E/job).mkdir(exist_ok=True)
        for p in [folder/'work_samples.json',folder/'samples_regression.json']:
            shutil.copy2(p,E/job/p.name)
        for i in [0,39,69,105,135,171,192]:
            shutil.copy2(folder/f'{i:04d}.png',E/job/f'{i:04d}.png')
    mixes=[]
    for row in load(RAW/'mixed_samples.json'):
        p=RAW/'mixes'/row['file'];pix=pixel_checks(Image.open(p))
        t=row['parts'];rest=RAW/'mixes'/f"{t['head']}_{t['body']}_{t['tail']}_rest.png"
        ref=pixel_checks(Image.open(rest));a=pixels(p)[:,:,3]
        waist=int(a[472:479,520:550].min())
        eq=changed(p,RAW/'fresh'/row['file'])
        passed=seam_pass(pix,ref) and waist>192
        mixes.append({'file':row['file'],'parts':t,'time':row['time'],'pixel_checks':pix,'rest_reference':ref,'same_continuity_floor_pass':bool(passed),'waist_min_alpha':waist,'fresh_live_changed_pixels':eq})
    new=[x for x in mixes if any(v in ['detective','geologist'] for v in x['parts'].values())]
    mix_report={'snapshots':len(mixes),'fresh_live_mismatch_snapshots':sum(x['fresh_live_changed_pixels']>0 for x in mixes),'fit_failing_snapshots':sum(not x['same_continuity_floor_pass'] for x in mixes),'new_job_fit_failing_snapshots':sum(not x['same_continuity_floor_pass'] for x in new),'rows':mixes,'status':'Compatibility cannot be signed off without shared waist contract; failures are retained. Deterministic state equality never proves fit.'}
    for n in range(0,len(mixes),24):
        rows=mixes[n:n+24];board([RAW/'mixes'/x['file'] for x in rows],REVIEW/f'mixes_{n//24+1:02d}.jpg',[x['file'] for x in rows])
    swaps=load(RAW/'live_swaps.json');swaps['original_restoration_changed_pixels']=changed(RAW/'original_before_swaps.png',RAW/'original_after_swaps.png')
    shutil.copy2(RAW/'capture_environment.json',E/'capture_environment.json')
    (E/'frame_index.json').write_text(json.dumps(frame_index,indent=2)+'\n')
    (E/'action_contact.json').write_text(json.dumps(results,indent=2)+'\n')
    (E/'mixed_outline.json').write_text(json.dumps(mix_report,indent=2)+'\n')
    (E/'live_swaps.json').write_text(json.dumps(swaps,indent=2)+'\n')
    for name in ['original_before_swaps.png','original_after_swaps.png']:shutil.copy2(RAW/name,E/name)
    print(json.dumps({'jobs':results,'mixes':{k:v for k,v in mix_report.items() if k!='rows'},'swaps':swaps},indent=2))


if __name__=='__main__':main()
