"""Read-only raster verification, actual Aseprite roundtrip and coordinate checks."""
import json,subprocess,sys,tempfile
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parent))
from prepare import P,ROOT,OLD,digest,fit,measure
ASE=r'C:\Program Files\Aseprite\Aseprite.exe'

def main():
    plan=json.loads((P/'registration_plan.json').read_text());checks=[];rows=[]
    target=plan['frames'][0]['target_landmarks'];r=np.array(target['bodice_waist_tip'])
    source={n:((np.array(v)-r)/1.0073+r+[12,-9]).tolist() for n,v in target.items()}
    f=fit(source,target);assert abs(f['uniform_scale']-1.0073)<1e-12
    assert abs(f['uniform_scale']*64-round(f['uniform_scale']*64))>.1
    checks.append('Known continuous scale/translation recovered without 1/64 quantization')
    stretch={n:list(v) for n,v in target.items()};stretch['neck_base'][1]-=30
    assert not fit(stretch,target)['anatomy_geometry_pass']
    checks.append('Internal torso deformation fails separately from global registration')
    assert [x['index'] for x in plan['frames']]==list(range(41))
    assert plan['new_model_takes']==plan['new_imagegen_calls']==0
    rng=np.random.default_rng(20261004)
    for row in plan['frames']:
        i=row['index'];src=ROOT/row['source'];out=P/f'frames/{i:04d}.png'
        assert digest(src)==row['source_sha256'] and row['apply_registration'] and row['no_new_clipping']
        a=np.array(Image.open(src).convert('RGBA'));b=np.array(Image.open(out).convert('RGBA'))
        assert a.shape==b.shape==(832,576,4)
        s=row['uniform_scale'];tx,ty=row['translation']
        # Independent exact-value spot checks, including anatomy-failed frames.
        for x,y in zip(rng.integers(0,576,256),rng.integers(0,832,256)):
            sx,sy=(x-tx)/s,(y-ty)/s;ix,iy=int(np.floor(sx)),int(np.floor(sy));fx,fy=sx-ix,sy-iy
            def sample(xx,yy):return a[yy,xx].astype(float) if 0<=xx<576 and 0<=yy<832 else np.array([238,238,238,255.])
            expected=np.floor((sample(ix,iy)*(1-fx)+sample(ix+1,iy)*fx)*(1-fy)+(sample(ix,iy+1)*(1-fx)+sample(ix+1,iy+1)*fx)*fy+.5).astype(np.uint8)
            assert np.array_equal(expected,b[y,x]),('Affine pixels differ',i,int(x),int(y))
        roi=None
        if row['manual_eye_roi_xyxy']:
            x0,y0,x1,y1=row['manual_eye_roi_xyxy']
            roi=[int(np.floor(x0*s+tx)),int(np.floor(y0*s+ty)),int(np.ceil(x1*s+tx)),int(np.ceil(y1*s+ty))]
        try:
            observed=measure(out,roi);after=fit(observed,row['target_landmarks'])
            root_error=float(np.linalg.norm(np.array(observed['bodice_waist_tip'])-plan['fixed_root']))
            global_error=abs(after['uniform_scale']-1)
            rows.append({'index':i,'sha256':digest(out),'observed_landmarks':observed,'root_error_px':root_error,
                         'remaining_global_scale':after['uniform_scale'],'registration_pass':root_error<=1 and global_error<=.003,
                         'anatomy_geometry_pass':after['anatomy_geometry_pass'],'max_anchor_residual_px':after['max_anchor_residual_px'],
                         'pair_scale_ratios':after['pair_scale_ratios'],'manual_export_eye_roi_xyxy':roi})
        except (ValueError,AssertionError) as exc:
            rows.append({'index':i,'sha256':digest(out),'registration_pass':False,'anatomy_geometry_pass':False,'measurement_error':str(exc)})
    checks.append('All41 frames, including anatomy failures, match 256 independent affine pixel samples each')
    with tempfile.TemporaryDirectory(prefix='roshan-scale-v2-roundtrip-') as tmp:
        subprocess.run([ASE,'-b','--script-param','master='+str(P/'registered_review.aseprite'),'--script-param','output='+tmp,
                        '--script-param','report='+str(P/'master_metadata.json'),'--script',str(P/'scripts/verify_master.lua')],check=True,timeout=120)
        for i in range(41):
            assert np.array_equal(np.array(Image.open(P/f'frames/{i:04d}.png').convert('RGBA')),np.array(Image.open(Path(tmp)/f'{i:04d}.png').convert('RGBA'))),('Roundtrip',i)
    checks.append('All41 reopened master frames pixel-exact, 205 anchors and41 timeline tags present')
    meta=json.loads((P/'master_metadata.json').read_text());assert sum(r['duration_ms'] for r in meta['rows'])==1708
    for i,row in enumerate(meta['rows']):assert row['duration_ms']==round((i+1)*1000/24)-round(i*1000/24)
    checks.append('Original41-frame24fps timeline retained; Aseprite millisecond durations sum1708ms')
    report={'status':'REGISTRATION_PASS' if all(r['registration_pass'] for r in rows) else 'REGISTRATION_NEEDS_CORRECTION',
            'checks':checks,'registered_indices':[r['index'] for r in rows if r['registration_pass']],
            'registration_failures':[r['index'] for r in rows if not r['registration_pass']],
            'anatomy_geometry_failures':[r['index'] for r in rows if not r['anatomy_geometry_pass']],
            'accepted':False,'frames':rows,'new_model_takes':0,'new_imagegen_calls':0,
            'remaining_acceptance':'Native identity, internal proportions, fingers, blur, cropped source hand, performance and loop seam remain human quality gates.'}
    (P/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(report['status'],'registration failures',report['registration_failures'],'anatomy geometry failures',report['anatomy_geometry_failures'])
    print('ROOT_MAX',max(r.get('root_error_px',0) for r in rows),'SCALE_MAX',max(abs(r.get('remaining_global_scale',1)-1) for r in rows))
    return 0 if report['status']=='REGISTRATION_PASS' else 1

if __name__=='__main__':raise SystemExit(main())
