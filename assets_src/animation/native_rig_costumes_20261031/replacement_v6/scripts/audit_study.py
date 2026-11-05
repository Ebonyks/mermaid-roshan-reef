"""Independent geometry/pixel diagnostics of actual Godot captures and Bone2D telemetry.

PASS covers named numerical checks, never a guarantee of natural acting or acceptance.
"""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

ROOT=Path(__file__).resolve().parents[1]
_GEOMETRY_CACHE={}


def affine(values):
    a,b,c,d,x,y=values
    return np.array([[a,c,x],[b,d,y],[0,0,1.]])


def pixel_checks(image):
    a=np.array(image)[:,:,3]
    mask=a>96
    labels,n=ndimage.label(mask)
    counts=np.bincount(labels.ravel());counts[0]=0
    big=sorted(counts[counts>12].tolist(),reverse=True)
    filled=ndimage.binary_fill_holes(mask)
    holes=filled & ~mask
    hl,hn=ndimage.label(holes)
    hc=np.bincount(hl.ravel());hc[0]=0
    return {'large_components':len(big),'secondary_component_pixels':big[1:] if len(big)>1 else [],'max_interior_hole_pixels':int(hc.max(initial=0)),'interior_hole_pixels':int(holes.sum()),'interior_hole_components':int(np.sum(hc>12)),'edge_alpha_pixels':int(np.sum(a[0]>0)+np.sum(a[-1]>0)+np.sum(a[:,0]>0)+np.sum(a[:,-1]>0))}


def seam_pass(pixels, reference):
    # Preserve intentional source gaps; allow only eight pixels of raster jitter.
    return (pixels['large_components']==1 and pixels['edge_alpha_pixels']==0
            and pixels['max_interior_hole_pixels']<=reference['max_interior_hole_pixels']+8
            and pixels['interior_hole_pixels']<=reference['interior_hole_pixels']+8
            and pixels['interior_hole_components']<=reference['interior_hole_components'])


def geometry(points, triangles, weights, rest_inverse, record):
    transforms=np.array([affine(record['bones'][name])@rest_inverse[i] for i,name in enumerate(weights)])
    key=id(points)
    if key not in _GEOMETRY_CACHE:
        w=np.array(list(weights.values()))
        ph=np.c_[points,np.ones(len(points))]
        p=points[triangles]
        reference=np.stack([p[:,1]-p[:,0],p[:,2]-p[:,0]],axis=2)
        det0=reference[:,0,0]*reference[:,1,1]-reference[:,0,1]*reference[:,1,0]
        inv=np.stack([reference[:,1,1],-reference[:,0,1],-reference[:,1,0],reference[:,0,0]],axis=1).reshape(-1,2,2)/det0[:,None,None]
        _GEOMETRY_CACHE[key]=(w[:,:,None]*ph[None,:,:],inv)
    weighted,inverse=_GEOMETRY_CACHE[key]
    deformed=np.einsum('bij,bnj->ni',transforms,weighted,optimize=True)[:,:2]
    q=deformed[triangles]
    moved=np.stack([q[:,1]-q[:,0],q[:,2]-q[:,0]],axis=2)
    jac=moved@inverse
    det=jac[:,0,0]*jac[:,1,1]-jac[:,0,1]*jac[:,1,0]
    trace=np.sum(jac*jac,axis=(1,2))
    delta=np.sqrt(np.maximum(trace*trace-4*det*det,0))
    sv=np.sqrt(np.maximum(np.c_[(trace+delta)/2,(trace-delta)/2],0))
    return deformed,det,sv


def main():
    parser=argparse.ArgumentParser();parser.add_argument('render');parser.add_argument('--rig',default=str(ROOT/'godot/rig.json'));parser.add_argument('--mesh');args=parser.parse_args()
    folder=Path(args.render)
    rig=json.loads(Path(args.rig).read_text())
    if rig.get('meshes') and not args.mesh:
        reports={}
        for mesh in rig['meshes']:
            result=subprocess.run([sys.executable,__file__,str(folder),'--rig',args.rig,'--mesh',mesh['name']],capture_output=True,text=True)
            (folder/f"audit_{mesh['name']}_stdout.log").write_text(result.stdout+'\n'+result.stderr)
            reports[mesh['name']]=json.loads((folder/f"geometry_audit_{mesh['name']}.json").read_text())
        report={'meshes':reports,'machine_geometry_pass':all(r['machine_geometry_pass'] for r in reports.values()),'scope':'All separate native meshes, same fixed tolerances; naturalness, device, child and owner acceptance separate.'}
        (folder/'geometry_audit.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps({k:{'pass':r['machine_geometry_pass'],'clips':r['clips']} for k,r in reports.items()},indent=2))
        raise SystemExit(0 if report['machine_geometry_pass'] else 1)
    mesh=next((m for m in rig.get('meshes',[]) if m['name']==args.mesh),rig)
    samples=json.loads((folder/'samples.json').read_text())
    stress=json.loads((folder/'stress_samples.json').read_text())
    points=np.array(mesh['vertices']);tri=np.array(mesh['triangles']);weights=mesh['weights']
    first=samples[0]
    rest_inverse=np.array([np.linalg.inv(affine(first['bones'][name])) for name in weights])
    texture=ROOT/'godot'/mesh.get('texture','../art/neutral.png')
    alpha=np.array(Image.open(texture))[:,:,3]
    centers=points[tri].mean(axis=1).astype(int)
    visible=alpha[np.clip(centers[:,1],0,1023),np.clip(centers[:,0],0,1023)]>192
    # Small threshold regions isolate face and distal fingers from intentional joint bending.
    head=points[:,1]<310
    hand_left=(points[:,0]<400)&(points[:,1]>525)&(points[:,1]<590)
    stats={}
    reference_pixels=pixel_checks(Image.open(folder/'arm_bend/0000.png').convert('RGBA'))
    for clip in ['arm_bend','blink','tail_bend']:
        records=[s for s in samples if s['clip']==clip]
        clip_stress=[s for s in stress if s['clip']==clip]
        out={'frames':len(records),'visible_triangle_count':int(visible.sum()),'inverted_visible_triangles':0,'min_visible_area_ratio':1.,'max_visible_area_ratio':1.,'max_visible_stretch':1.,'min_visible_stretch':1.,'max_bone_scale_error':0.,'rigid_head_distance_error_px':0.,'max_alpha_components':0,'max_interior_hole_pixels':0,'edge_alpha_pixels':0,'worst_frame':None,'pixel_seam_pass':True,'max_total_interior_hole_pixels':0,'max_interior_hole_components':0}
        worst=0
        seen=set()
        for s in records+clip_stress:
            stamp=round(s['time'],6)
            if stamp in seen:continue
            seen.add(stamp)
            q,det,sv=geometry(points,tri,weights,rest_inverse,s)
            out['inverted_visible_triangles']=max(out['inverted_visible_triangles'],int(np.sum(det[visible]<=0)))
            out['min_visible_area_ratio']=min(out['min_visible_area_ratio'],float(det[visible].min()))
            out['max_visible_area_ratio']=max(out['max_visible_area_ratio'],float(det[visible].max()))
            out['max_visible_stretch']=max(out['max_visible_stretch'],float(sv[visible].max()))
            out['min_visible_stretch']=min(out['min_visible_stretch'],float(sv[visible].min()))
            for name in weights:
                m=affine(s['bones'][name])[:2,:2]
                out['max_bone_scale_error']=max(out['max_bone_scale_error'],float(np.max(np.abs(np.linalg.svd(m,compute_uv=False)-1))))
            h0=points[head];h1=q[head]
            if len(h0)>1:
                out['rigid_head_distance_error_px']=max(out['rigid_head_distance_error_px'],float(abs(np.linalg.norm(h0[0]-h0[-1])-np.linalg.norm(h1[0]-h1[-1]))))
            bad=float(np.maximum(sv[visible]-1,1-sv[visible]).max())
            if bad>worst:
                worst=bad
                out['worst_frame']={k:s[k] for k in ['frame','time'] if k in s}
                worst_tri=np.where(visible)[0][np.argmax(np.max(np.maximum(sv[visible]-1,1-sv[visible]),axis=1))]
                out['worst_triangle_source_center']=centers[worst_tri].tolist()
        for s in records:
            im=Image.open(folder/clip/f"{s['frame']:04}.png").convert('RGBA')
            pix=pixel_checks(im)
            out['pixel_seam_pass']=out['pixel_seam_pass'] and seam_pass(pix,reference_pixels)
            out['max_total_interior_hole_pixels']=max(out['max_total_interior_hole_pixels'],pix['interior_hole_pixels'])
            out['max_interior_hole_components']=max(out['max_interior_hole_components'],pix['interior_hole_components'])
            out['max_alpha_components']=max(out['max_alpha_components'],pix['large_components'])
            out['max_interior_hole_pixels']=max(out['max_interior_hole_pixels'],pix['max_interior_hole_pixels'])
            out['edge_alpha_pixels']+=pix['edge_alpha_pixels']
        a=Image.open(folder/clip/'0000.png')
        z=Image.open(folder/clip/f"{records[-1]['frame']:04}.png")
        out['loop_endpoint_changed_pixels']=int(np.any(np.array(a)!=np.array(z),axis=2).sum())
        out['geometry_pass']=bool(out['pixel_seam_pass'] and out['inverted_visible_triangles']==0 and out['min_visible_stretch']>=.80 and out['max_visible_stretch']<=1.20 and out['max_bone_scale_error']<1e-5 and out['rigid_head_distance_error_px']<.01 and out['edge_alpha_pixels']==0 and out['max_alpha_components']==1 and out['loop_endpoint_changed_pixels']==0)
        stats[clip]=out
    # Fault injection proves that a slit and a detached piece are recognized by pixel diagnostics.
    im=Image.open(folder/'arm_bend/0000.png').convert('RGBA')
    normal=pixel_checks(im)
    broken=np.array(im);broken[405:425,520:535,3]=0
    hole=pixel_checks(Image.fromarray(broken))
    detached=im.copy();ImageDraw.Draw(detached).rectangle((20,20,40,40),fill=(255,0,0,255))
    extra=pixel_checks(detached)
    s=dict(first);s['bones']=dict(first['bones']);scaled=list(s['bones']['Head']);scaled[0]*=1.2;scaled[1]*=1.2;s['bones']['Head']=scaled
    scaled_error=float(np.max(np.abs(np.linalg.svd(affine(s['bones']['Head'])[:2,:2],compute_uv=False)-1)))
    negative={'interior_slit_detected':not seam_pass(hole,normal),'detached_piece_detected':not seam_pass(extra,normal),'scaled_head_detected':scaled_error>.1}
    report={'render_folder':str(folder),'thresholds':{'visible_stretch':[.8,1.2],'bone_scale_error':1e-5,'rigid_head_distance_error_px':.01,'inverted_visible_triangles':0},'clips':stats,'negative_controls':negative,'seam_reference':reference_pixels,'seam_raster_allowance_pixels':8,'machine_geometry_pass':all(s['geometry_pass'] for s in stats.values()) and all(negative.values()),'visual_naturalness':'Requires exact normal-speed and frame-step review; metrics do not establish naturalness','owner_device_child_acceptance':'PENDING'}
    report_name=f'geometry_audit_{args.mesh}.json' if args.mesh else 'geometry_audit.json'
    (folder/report_name).write_text(json.dumps(report,indent=2)+'\n')
    # Inspectable chronological boards on three backgrounds, including closeups of the actual render.
    for clip in stats:
        paths=sorted((folder/clip).glob('*.png'))
        indices=np.linspace(0,len(paths)-1,12).round().astype(int)
        board=Image.new('RGB',(1536,1152),(24,30,41));draw=ImageDraw.Draw(board)
        for j,k in enumerate(indices):
            tile=Image.new('RGBA',(1024,1024),[(245,245,245,255),(8,12,20,255),(80,90,100,255)][j%3])
            tile.alpha_composite(Image.open(paths[k]).convert('RGBA'))
            tile=tile.convert('RGB').resize((384,350),Image.Resampling.LANCZOS)
            x=(j%4)*384;y=(j//4)*384
            board.paste(tile,(x,y));draw.text((x+10,y+355),f'{clip} frame {k} / {k/30:.3f}s',fill='white')
        board.save(folder/f'{clip}_board.jpg',quality=95)
    print(json.dumps({'geometry_pass':report['machine_geometry_pass'],'clips':stats,'negative_controls':negative},indent=2))


if __name__=='__main__':main()
