"""Validate the proposed data-only costume exchange format; never accept a performance."""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path, PurePosixPath
from PIL import Image


class InvalidSkin(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise InvalidSkin(message)


def fields(value: dict, required: set[str], optional: set[str], label: str) -> None:
    require(isinstance(value, dict), label + ': expected object')
    require(required <= value.keys(), label + ': missing ' + str(sorted(required-value.keys())))
    require(not value.keys()-required-optional, label + ': unknown fields ' + str(sorted(value.keys()-required-optional)))


def number(value) -> bool:
    return type(value) in (int, float) and math.isfinite(value)


def point(value, label: str) -> None:
    require(isinstance(value, list) and len(value)==2 and all(number(v) for v in value), label+': expected finite x,y')


def asset(root: Path, reference: dict, suffixes: set[str]) -> Path:
    fields(reference, {'path','sha256'}, set(), 'asset reference')
    name=reference['path']
    require(isinstance(name,str) and name and '\\' not in name and ':' not in name, 'asset path must be repository-relative POSIX')
    relative=PurePosixPath(name)
    require(not relative.is_absolute() and '..' not in relative.parts, 'asset path escapes repository')
    require(not any(p.lower() in {'.git','.secrets','.aws','.codex','.claude'} for p in relative.parts), 'private/operational asset path forbidden')
    target=(root/name).resolve()
    require(target.is_relative_to(root.resolve()) and target.is_file(), 'missing or escaping asset: '+name)
    require(target.suffix.lower() in suffixes, 'unsupported asset type: '+name)
    digest=hashlib.sha256(target.read_bytes()).hexdigest()
    require(reference['sha256']==digest, 'asset hash mismatch: '+name)
    return target


def validate_rig(rig: dict, root: Path) -> None:
    fields(rig, {'format','rig_id','version','status','skeleton','bones','views','sockets','identity_assets','templates'}, {'interfaces'}, 'rig')
    require(rig['format']=='roshan.rig-binding/1', 'unsupported rig format')
    require(rig['status'] in ['prototype','approved'], 'unknown rig status')
    require(all(isinstance(rig[k],str) and rig[k] for k in ['rig_id','version']), 'empty rig identity/version')
    bones=rig['bones']
    require(isinstance(bones,list) and bones and all(isinstance(n,str) and n for n in bones) and len(set(bones))==len(bones), 'invalid/duplicate bones')
    skeleton=json.loads(asset(root,rig['skeleton'],{'.json'}).read_text(encoding='utf-8'))
    require(isinstance(skeleton,dict) and isinstance(skeleton.get('bones'),list) and all(isinstance(b,dict) for b in skeleton['bones']) and [b.get('name') for b in skeleton['bones']]==bones, 'canonical skeleton bone list mismatch')
    require(isinstance(rig['views'],dict) and rig['views'], 'rig needs views')
    for view,definition in rig['views'].items():
        fields(definition, {'canvas','slots'}, set(), 'view '+view)
        require(isinstance(definition['canvas'],list) and len(definition['canvas'])==2 and all(type(v)==int and v>0 for v in definition['canvas']), 'invalid view canvas')
        require(isinstance(definition['slots'],dict) and definition['slots'], 'view needs slots')
        for slot,spec in definition['slots'].items():
            fields(spec, {'required','modes','layer'}, set(), 'slot '+slot)
            require(type(spec['required']) is bool and type(spec['layer']) is int, 'invalid slot requirement/layer')
            require(isinstance(spec['modes'],list) and spec['modes'] and set(spec['modes'])<={'rigid','weighted'}, 'invalid slot modes')
    require(isinstance(rig['sockets'],dict), 'invalid sockets')
    for name,socket in rig['sockets'].items():
        fields(socket, {'bone','offset'}, set(), 'socket '+name)
        require(socket['bone'] in bones, 'unknown socket bone')
        point(socket['offset'],'socket offset')
    require(isinstance(rig['identity_assets'],list) and rig['identity_assets'], 'rig must pin immutable anatomy/identity assets')
    for reference in rig['identity_assets']:
        asset(root,reference,{'.png','.json'})
    require(isinstance(rig['templates'],dict), 'invalid templates')
    for reference in rig['templates'].values():
        asset(root,reference,{'.json'})


def validate_mesh(mesh: dict, bones: list[str]) -> None:
    fields(mesh, {'format','space','vertices','uv','triangles','weights'}, {'seams'}, 'garment mesh')
    require(mesh['format']=='roshan.attachment-mesh/1' and mesh['space']=='canonical_canvas_px', 'unknown mesh format/space')
    vertices=mesh['vertices'];uv=mesh['uv']
    require(isinstance(vertices,list) and len(vertices)>=3 and isinstance(uv,list) and len(uv)==len(vertices), 'mesh vertex/UV count mismatch')
    for value in vertices+uv:
        point(value,'mesh point')
    require(isinstance(mesh['triangles'],list) and mesh['triangles'], 'mesh requires triangles')
    for triangle in mesh['triangles']:
        require(isinstance(triangle,list) and len(triangle)==3 and all(type(i)==int and 0<=i<len(vertices) for i in triangle), 'invalid triangle index')
        a,b,c=[vertices[i] for i in triangle]
        require(abs((b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]))>1e-8, 'degenerate triangle')
    weights=mesh['weights']
    require(isinstance(weights,dict) and weights and set(weights)<=set(bones), 'unknown/missing weight bones')
    for values in weights.values():
        require(isinstance(values,list) and len(values)==len(vertices) and all(number(x) and 0<=x<=1 for x in values), 'invalid weight array')
    for index in range(len(vertices)):
        require(abs(sum(values[index] for values in weights.values())-1.0)<=1e-6, 'weights must sum to1 per vertex')
    if 'seams' in mesh:
        require(isinstance(mesh['seams'],dict), 'invalid seam map')
        for indices in mesh['seams'].values():
            require(isinstance(indices,list) and indices and all(type(i)==int and 0<=i<len(vertices) for i in indices), 'invalid seam vertex index')


def validate_skin(skin_path: Path, rig_path: Path, root: Path) -> dict:
    rig=json.loads(rig_path.read_text(encoding='utf-8'))
    validate_rig(rig,root)
    skin=json.loads(skin_path.read_text(encoding='utf-8'))
    fields(skin, {'format','skin_id','rig','views','attachments','coverage','provenance'}, set(), 'skin')
    require(skin['format']=='roshan.skin/1', 'unsupported skin format')
    require(isinstance(skin['skin_id'],str) and skin['skin_id'] and all(c in 'abcdefghijklmnopqrstuvwxyz0123456789_-' for c in skin['skin_id']), 'invalid skin ID')
    fields(skin['rig'], {'id','version','contract_sha256'}, set(), 'skin rig pin')
    require(skin['rig']=={'id':rig['rig_id'],'version':rig['version'],'contract_sha256':hashlib.sha256(rig_path.read_bytes()).hexdigest()}, 'incompatible rig pin')
    views=skin['views']
    require(isinstance(views,list) and views and len(set(views))==len(views) and set(views)<=rig['views'].keys(), 'missing/unknown/duplicate views')
    require(isinstance(skin['attachments'],list), 'attachments must be a list')
    attachments={}
    for item in skin['attachments']:
        fields(item, {'id','view','slot','mode','texture'}, {'binding','geometry','template_id'}, 'attachment')
        require(isinstance(item['id'],str) and item['id'] and item['id'] not in attachments, 'empty/duplicate attachment ID')
        view=item['view'];slot=item['slot']
        require(view in views and slot in rig['views'][view]['slots'], 'unknown attachment view/slot')
        require(item['mode'] in rig['views'][view]['slots'][slot]['modes'], 'attachment mode not allowed by slot')
        texture=asset(root,item['texture'],{'.png'})
        with Image.open(texture) as image:
            width,height=image.size
            require(image.mode=='RGBA', 'garment texture must be RGBA')
            require(max(width,height)<=1024 or all(n>0 and n&(n-1)==0 for n in [width,height]), 'texture exceeds size/POT rule')
        if item['mode']=='rigid':
            require('binding' in item and 'geometry' not in item and 'template_id' not in item, 'rigid attachment must use a socket binding only')
            binding=item['binding']
            fields(binding, {'socket','pivot','offset','rotation_deg','scale'}, set(), 'rigid binding')
            require(binding['socket'] in rig['sockets'], 'unknown socket')
            point(binding['pivot'],'texture pivot');point(binding['offset'],'socket-local offset')
            require(number(binding['rotation_deg']) and number(binding['scale']) and binding['scale']>0, 'invalid rigid transform')
        else:
            require('geometry' in item and 'binding' not in item, 'weighted attachment must use geometry only')
            path=asset(root,item['geometry'],{'.json'})
            mesh=json.loads(path.read_text(encoding='utf-8'))
            validate_mesh(mesh,rig['bones'])
            require(all(0<=uv[0]<=width and 0<=uv[1]<=height for uv in mesh['uv']), 'UV outside garment texture')
            require(set(mesh.get('seams',{})) <= set(rig.get('interfaces',{})), 'unknown canonical seam interface')
            if 'template_id' in item:
                require(item['template_id'] in rig['templates'] and item['geometry']==rig['templates'][item['template_id']], 'template reference changed or unknown')
        attachments[item['id']]=item
    require(isinstance(skin['coverage'],dict) and set(skin['coverage'])==set(views), 'coverage must declare every supported view')
    used=[]
    for view in views:
        coverage=skin['coverage'][view];slots=rig['views'][view]['slots']
        require(isinstance(coverage,dict) and set(coverage)==set(slots), 'every slot must be assigned or explicitly null')
        for slot,identity in coverage.items():
            if identity is None:
                require(not slots[slot]['required'], 'required slot is empty: '+slot)
                continue
            require(identity in attachments, 'coverage references missing attachment')
            item=attachments[identity]
            require(item['view']==view and item['slot']==slot, 'coverage/view/slot mismatch')
            used.append(identity)
    require(len(used)==len(set(used)) and set(used)==set(attachments), 'orphaned/duplicate active attachments')
    provenance=skin['provenance']
    fields(provenance, {'sources','edits','generator_calls'}, set(), 'provenance')
    require(isinstance(provenance['sources'],list) and provenance['sources'], 'missing garment provenance')
    for source in provenance['sources']:
        fields(source, {'asset','license','role','acceptance_scope'}, set(), 'provenance source')
        require(source['role'] in ['garment_source','registration_reference','style_reference'] and isinstance(source['license'],str) and source['license'], 'missing source role/license')
        require(isinstance(source['acceptance_scope'],str) and source['acceptance_scope'], 'source acceptance/rejection scope must be retained')
        asset(root,source['asset'],{'.png','.json','.aseprite'})
    require(isinstance(provenance['edits'],list) and all(isinstance(x,str) and x for x in provenance['edits']), 'invalid edit log')
    require(type(provenance['generator_calls']) is int and provenance['generator_calls']>=0, 'invalid generator call count')
    return {'format_and_bindings_pass':True,'skin_id':skin['skin_id'],'rig_id':rig['rig_id'],'rig_status':rig['status'],'views':views,'attachments':len(attachments),'live_actor_verified':False,'garment_only_pixels_reviewed':False,'seams_and_motion_accepted':False,'device_verified':False,'owner_accepted':False,'production_accepted':False,'limits':'Structural/reference/weight checks only. Actual garment-only pixels, registration, seam compatibility, strain, contacts and live-actor invariants require separate measured evidence.'}


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skin',type=Path,required=True)
    parser.add_argument('--rig',type=Path,required=True)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument('--report',type=Path)
    args=parser.parse_args()
    try:
        result=validate_skin(args.skin,args.rig,args.root.resolve())
    except (InvalidSkin,ValueError,OSError,TypeError,KeyError) as error:
        result={'format_and_bindings_pass':False,'error':str(error),'production_accepted':False}
    if args.report:
        args.report.parent.mkdir(parents=True,exist_ok=True)
        args.report.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(result,indent=2))
    return 0 if result['format_and_bindings_pass'] else 1


if __name__=='__main__':
    raise SystemExit(main())
