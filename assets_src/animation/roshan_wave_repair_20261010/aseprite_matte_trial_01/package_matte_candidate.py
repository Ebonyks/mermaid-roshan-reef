"""Hash immutable own candidate evidence after model review; no image writes."""
from pathlib import Path
from PIL import Image
import hashlib,json,datetime,sys
pilot=Path(__file__).resolve().parent;folder=(pilot/sys.argv[1]).resolve()
assert folder.parent==pilot and folder.is_dir()
root=next(p for p in pilot.parents if (p/'project.godot').is_file())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,data): p.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
plan=json.loads((folder/'source_and_seed_plan.json').read_text(encoding='utf-8'))
verification=json.loads((folder/'verification.json').read_text(encoding='utf-8'))
status=verification['status']
assert verification['machine_preservation_checks_pass'], 'Do not package a machine-failed pass as complete'
now=datetime.datetime.now(datetime.timezone.utc);start=datetime.datetime.fromtimestamp(folder.stat().st_ctime,datetime.timezone.utc)
write(folder/'receipt.json',{'schema':'reef.local-whole-cel-matte-receipt.v1','status':status,
    'started_at_utc':start.isoformat(),'completed_at_utc':now.isoformat(),
    'elapsed_local_processing_and_review_minutes':round((now-start).total_seconds()/60,4),
    'timing_limit':'Folder creation to packet completion; engine preparation preceded this folder and concurrent parent/agent work may overlap. Root owns cumulative campaign accounting.',
    'generator_calls':0,'api_calls':0,'gpu_calls':0,'paid_calls':0,'aseprite_version':'1.3.18.4-x64',
    'pixel_writer':'Aseprite Lua','source_packet':plan['source_packet'],'source_frame_count':41,'native_size':[768,896],
    'workflow':['review_seeds.lua','recover_full_edges.lua','black_review.lua','verify_full_matte.py'],
    'whole_cel_uniform_scale':0.3125,'whole_cel_resize':[240,280],'whole_cel_translation':[15,-10],'final_size':[256,256],
    'native_endpoint_replacement':{'source':'approved_K0.png','source_sha256':sha(folder/'approved_K0.png'),
        'whole_resized_dimensions':[819,819],'uniform_raster_scale':819/256,'translation':[-48,32],
        'ideal_inverse_scale':3.2,'relative_scale_error_pct':100*((819/256)/3.2-1),
        'source_RGB_and_upstream_matte_preserved':True,'source_indices':[0,40]},
    'export_endpoint_replacement':'Exact approvedK0 PNG bytes and directly loaded approvedK0 master pixels',
    'geometry':'Root independently measures actual native final and256px output joints/figure/head geometry; source settings or this pixel-preservation PASS do not establish W2/W3/W6.',
    'acceptance':{'artifact_free_wave':False,'owner':False,'device':False,'child':False,'runtime':False,'delivery_accepted':False}})
def package(target,status):
    files=[]
    for p in sorted(target.rglob('*')):
        if not p.is_file() or p==target/'manifest.json':continue
        name=p.relative_to(target).as_posix()
        e={'path':name,'sha256':sha(p),'bytes':p.stat().st_size,'role':'workflow_or_derivation_record','used_as_delivery_pixels':False,
            'provenance':'Project-approved identity and preserved generated source cels, modified only by the declared local Aseprite workflow; source and candidate acceptance scopes remain separate',
            'modification':'Exact recipe, mapping, endpoint replacement and remaining review limitations recorded in candidate README and verification',
            'license_provenance':'Root canonical ASSET_LICENSES.md and source manifests remain authoritative; no external art inputs added'}
        if p.suffix=='.png':
            with Image.open(p) as im:e.update(dimensions=list(im.size),mode=im.mode)
            if '/sources/' in '/'+name:e.update(role='byte_exact_native_source_copy',modification='Byte-exact preservation')
            elif '/upstream_endpoint_matte/' in '/'+name:e.update(role='preserved_upstream_endpoint_matte_diagnostic')
            elif '/native_rgba/' in '/'+name:e.update(role='whole_cel_native_rgba_candidate')
            elif '/frames/' in '/'+name:e.update(role='whole_cel_256_rgba_candidate')
            elif p.name=='approved_K0.png':e.update(role='byte_exact_approved_complete_endpoint_source',modification='Byte-exact approved K0 copy')
            else:e.update(role='review_only_preview_or_baseline')
        if p.suffix=='.aseprite':e.update(role='single_layer_whole_cel_editable_master')
        files.append(e)
    payload=''.join(e['path']+'\t'+e['sha256']+'\n' for e in files).encode('utf-8')
    write(target/'manifest.json',{'schema':'reef.aseprite-matte-packet.v1','status':status,'created_at_utc':now.isoformat(),
        'files':files,'packet_payload_rule':'Sorted relative POSIX path + TAB + SHA256 + LF for every file except this manifest.json; SHA256 of UTF8 payload',
        'packet_payload_sha256':hashlib.sha256(payload).hexdigest(),
        'acceptance':{'artifact_free_wave':False,'owner':False,'device':False,'child':False,'runtime':False,'delivery_accepted':False,'github_publication':'PENDING_ROOT_PROJECT_PACKET'}})
    return {'folder':target.relative_to(root).as_posix(),'payload_files':len(files),'packet_payload_sha256':hashlib.sha256(payload).hexdigest()}
print(json.dumps([package(folder,status),package(pilot,'LOCAL_SOURCE_STUDIES_UNACCEPTED; previous_rejected_diagnostics_preserved; candidate_review_required')]))
