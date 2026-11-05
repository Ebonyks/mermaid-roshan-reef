"""Apply the retained original numerical floors to every native costume frame."""
from pathlib import Path
import concurrent.futures, hashlib, importlib.util, json, os, sys
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT/'tools'/filename)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


def one(row):
    group,theme = row
    original = module('retained_geometry','reference_audit_study.py')
    motion = module('retained_motion','reference_audit_motion.py')
    folder = ROOT/'raw_render'/group/theme
    samples = json.loads((folder/'samples.json').read_text())
    mesh_data = json.loads((folder/'runtime_meshes.json').read_text())
    neutral = np.array(Image.open(folder/'loop/0000.png').convert('RGBA'))
    prepared = []
    for mesh in mesh_data:
        points = np.array(mesh['vertices'],dtype=float)
        triangles = np.array(mesh['triangles'],dtype=int)
        # Polygon2D can also describe an untriangulated contour; these retained rigs use triangles.
        assert triangles.ndim == 2 and triangles.shape[1] == 3,(theme,mesh['name'])
        weights = mesh['weights']
        inverse = np.array([np.linalg.inv(original.affine(samples[0]['bones'][name])) for name in weights])
        centers = points[triangles].mean(axis=1).astype(int)
        alpha = np.array(Image.open(ROOT/f'evidence/material_surfaces/{group}/{theme}'/('surface_'+mesh['name']+'.png')).convert('RGBA'))[:,:,3]
        x = np.clip(centers[:,0],0,1023)
        y = np.clip(centers[:,1],0,1023)
        # Actual isolated shader/material output: other meshes cannot pollute this coverage.
        visible = alpha[y,x]>192
        prepared.append((mesh,points,triangles,weights,inverse,visible))
    reports = {}
    frame_hashes = []
    for clip in ['loop','travel']:
        records = [s for s in samples if s['clip']==clip]
        reference = original.pixel_checks(Image.open(folder/clip/'0000.png').convert('RGBA'))
        report = {'frames':len(records),'outline_failed_frames':[], 'geometry_failed_frames':[], 'joint_failed_frames':[], 'inverted_visible_triangles':0,'min_visible_stretch':1.0,'max_visible_stretch':1.0,'max_bone_scale_error':0.0,'rigid_head_distance_error_px':0.0,'minimum_joint_alpha':255,'max_alpha_components':0,'edge_alpha_pixels':0}
        for record in records:
            frame = int(record['frame'])
            path = folder/clip/f'{frame:04}.png'
            image = Image.open(path).convert('RGBA')
            pixels = np.array(image)
            frame_hashes.append({'clip':clip,'frame':frame,'rgba_sha256':hashlib.sha256(pixels.tobytes()).hexdigest(),'png_sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
            pixel = original.pixel_checks(image)
            report['max_alpha_components'] = max(report['max_alpha_components'],pixel['large_components'])
            report['edge_alpha_pixels'] += pixel['edge_alpha_pixels']
            if not original.seam_pass(pixel,reference):
                report['outline_failed_frames'].append({'frame':frame,'time':record['time'],'pixels':pixel})
            geometric = True
            for mesh,points,triangles,weights,inverse,visible in prepared:
                q,det,sv = original.geometry(points,triangles,weights,inverse,record)
                if not visible.any():
                    continue
                flips = int(np.sum(det[visible]<=0))
                low,high = float(sv[visible].min()),float(sv[visible].max())
                report['inverted_visible_triangles'] = max(report['inverted_visible_triangles'],flips)
                report['min_visible_stretch'] = min(report['min_visible_stretch'],low)
                report['max_visible_stretch'] = max(report['max_visible_stretch'],high)
                geometric &= flips==0 and low>=.8 and high<=1.2
                head = points[:,1]<310
                if head.sum()>1:
                    error = float(abs(np.linalg.norm(points[head][0]-points[head][-1])-np.linalg.norm(q[head][0]-q[head][-1])))
                    report['rigid_head_distance_error_px'] = max(report['rigid_head_distance_error_px'],error)
                    geometric &= error<.01
            for name,values in record['bones'].items():
                error = float(np.max(abs(np.linalg.svd(original.affine(values)[:2,:2],compute_uv=False)-1)))
                report['max_bone_scale_error'] = max(report['max_bone_scale_error'],error)
                geometric &= error<1e-5
            if not geometric:
                report['geometry_failed_frames'].append(frame)
            bad_joints = []
            for name in ['LeftUpper','LeftFore','LeftHand']:
                if name not in record['bones']:
                    continue
                point = np.round(np.array(record['bones'][name][4:6])+np.array(record['root'])).astype(int)
                patch = pixels[point[1]-1:point[1]+2,point[0]-1:point[0]+2,3]
                value = int(patch.min()) if patch.size else 0
                report['minimum_joint_alpha'] = min(report['minimum_joint_alpha'],value)
                if value<=192:
                    bad_joints.append(name)
            if bad_joints:
                report['joint_failed_frames'].append({'frame':frame,'joints':bad_joints})
        report.update(motion.motion_metrics(records))
        report['endpoint_matrix_error'] = max(abs(a-b) for name in records[0]['bones'] for a,b in zip(records[0]['bones'][name],records[-1]['bones'][name]))
        first = np.array(Image.open(folder/clip/'0000.png'))
        last = np.array(Image.open(folder/clip/f"{records[-1]['frame']:04}.png"))
        report['loop_endpoint_changed_pixels'] = int(np.any(first!=last,axis=2).sum()) if clip=='loop' else None
        report['motion_pass'] = report['max_angular_speed_deg_s']<140 and report['max_angular_acceleration_deg_s2']<650 and report['endpoint_matrix_error']<1e-5
        report['geometry_pass'] = not report['geometry_failed_frames']
        report['outline_pass'] = not report['outline_failed_frames']
        report['joint_pass'] = not report['joint_failed_frames']
        report['pass'] = all(report[k] for k in ['motion_pass','geometry_pass','outline_pass','joint_pass']) and (clip!='loop' or report['loop_endpoint_changed_pixels']==0)
        reports[clip] = report
    image = Image.fromarray(neutral)
    reference = original.pixel_checks(image)
    detached = image.copy()
    ImageDraw.Draw(detached).rectangle((20,20,40,40),fill=(255,0,0,255))
    torn = neutral.copy()
    torn[440:460,:,3] = 0
    scaled = original.affine(samples[0]['bones']['Head'])[:2,:2]*1.2
    bad = json.loads(json.dumps([s for s in samples if s['clip']=='loop']))
    matrix = bad[len(bad)//2]['bones']['LeftFore']
    matrix[0],matrix[1],matrix[2],matrix[3] = -matrix[1],matrix[0],-matrix[3],matrix[2]
    pop = motion.motion_metrics(bad)
    controls = {'detached_piece':not original.seam_pass(original.pixel_checks(detached),reference),'torn_figure':not original.seam_pass(original.pixel_checks(Image.fromarray(torn)),reference),'scaled_head':float(np.max(abs(np.linalg.svd(scaled,compute_uv=False)-1)))>1e-5,'pose_pop':pop['max_angular_speed_deg_s']>=140 or pop['max_angular_acceleration_deg_s2']>=650}
    receipt = json.loads((folder/'native_receipt.json').read_text())
    result = {'theme':theme,'group':group,'pass':all(r['pass'] for r in reports.values()) and all(controls.values()) and receipt['pass'],'clips':reports,'negative_controls':controls,'native_state':receipt,'visible_meshes':[x[0]['name'] for x in prepared]}
    out = ROOT/'evidence/costumes_surface'
    out.mkdir(parents=True,exist_ok=True)
    (out/(theme+'.json')).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    (out/(theme+'_frame_hashes.json')).write_text(json.dumps(frame_hashes,indent=2)+'\n',encoding='utf-8',newline='\n')
    print('AUDITED',theme,result['pass'],'outline',sum(len(x['outline_failed_frames']) for x in reports.values()),'geometry',sum(len(x['geometry_failed_frames']) for x in reports.values()),flush=True)
    return result


def main():
    groups = json.loads((ROOT/'sources.json').read_text())['groups']
    rows = [(g['group'],theme) for g in groups for theme in g['themes']]
    results = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=3) as pool:
        for future in concurrent.futures.as_completed([pool.submit(one,row) for row in rows]):
            results.append(future.result())
    signatures = {}
    for group in groups:
        rig = json.loads((ROOT/'raw_render'/group['group']/'runtime_rig.json').read_text())
        signatures[group['group']] = hashlib.sha256(json.dumps(rig['bones'],sort_keys=True,separators=(',',':')).encode()).hexdigest()
    same = len(set(signatures.values())) == 1
    result = {'costumes':sorted(results,key=lambda x:x['theme']),'all_machine_checks_pass':all(r['pass'] for r in results),'same_bone_rest_contract':same,'bone_signatures':signatures,'frames_reviewed':sum(sum(c['frames'] for c in r['clips'].values()) for r in results),'original_thresholds':{'stretch':[.8,1.2],'bone_scale_error':1e-5,'head_distance_px':.01,'alpha_components':1,'hole_raster_allowance_px':8,'joint_patch_alpha_min':192,'speed_deg_s':140,'acceleration_deg_s2':650,'loop_rgba_changed_pixels':0},'visibility':'Actual neutral isolated native material output per mesh, including painted costume alpha. Other meshes do not supply its visibility. Original thresholds and legacy three left-joint probes are unchanged.','additional_right_hand_probe':'Initial audit finds RightHand origin outside skin even in unanimated original frame0. It is not a verified grip/socket; source-contract repair and actual hand contact remain blocking, not a threshold waiver.','acceptance':'Machine diagnostics only. Front-view pilot; existing source defects, human motion, phone, child, owner and runtime adoption remain separate.'}
    (ROOT/'evidence/swim_audit_surface.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    print('SWIM_AUDIT_COMPLETE',result['frames_reviewed'],'same_rest',same,'pass',result['all_machine_checks_pass'],flush=True)


if __name__ == '__main__':
    main()
