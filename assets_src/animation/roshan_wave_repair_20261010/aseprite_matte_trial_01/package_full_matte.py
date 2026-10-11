"""Hash own matte packets and write provenance receipts; never edits images."""
from pathlib import Path
from PIL import Image
import hashlib,json,datetime
pilot=Path(__file__).resolve().parent
folder=pilot/'full_wave_matte_01'
root=next(p for p in pilot.parents if (p/'project.godot').is_file())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,data): p.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
now=datetime.datetime.now(datetime.timezone.utc)
created=datetime.datetime.fromtimestamp(folder.stat().st_ctime,datetime.timezone.utc)
write(folder/'receipt.json',{'schema':'reef.local-whole-cel-matte-receipt.v1',
    'status':'REJECTED_DIAGNOSTIC_KNOWN_SOURCE_CLIPPING_AND_MASK_ARTIFACTS',
    'started_at_utc':created.isoformat(),'completed_at_utc':now.isoformat(),
    'elapsed_local_processing_and_review_minutes':round((now-created).total_seconds()/60,4),
    'timing_limit':'Folder creation to verification completion; concurrent parent/agent work can overlap, so root must account campaign aggregate time.',
    'generator_calls':0,'api_calls':0,'gpu_calls':0,'paid_calls':0,
    'aseprite_version':'1.3.18.4-x64','pixel_writer':'Aseprite Lua',
    'workflow':'recover_full_edges.lua; black_review.lua; verify_full_matte.py',
    'source_frame_count':41,'native_size':[640,896],'uniform_scale':0.3125,'final_size':[256,256],
    'whole_cel_translation':[55,-10], 'manual_component_review':'All 41 hair-loop seed crops; all left-curl/ambiguous shoulder crops; black/light complete-cel contacts and native upper-body black contact.',
    'known_rejections':['Source frame28 fingertip clipping at native x=0','Visible source paint-mask rectangles and old-arm remnants','Source native focus/line noise'],
    'all_originals_preserved':True,'exact_endpoint_export_png_sha256':sha(folder/'approved_K0.png'),
    'acceptance':{'artifact_free_wave':False,'owner':False,'device':False,'child':False,'runtime':False,'delivery_accepted':False}})

def package(target,status):
    files=[]
    for p in sorted(target.rglob('*')):
        if not p.is_file() or p==target/'manifest.json':continue
        name=p.relative_to(target).as_posix()
        e={'path':name,'sha256':sha(p),'bytes':p.stat().st_size,'role':'workflow_or_derivation_record',
            'used_as_delivery_pixels':False,'modification':'Preserved sources or declared Aseprite whole-cel RGBA cleanup; exact recipe/status in local README and verification records',
            'license_provenance':'Project source art and local authorized derivation; no new external art inputs. Root canonical asset-license rows remain authoritative.'}
        if p.suffix=='.png':
            with Image.open(p) as im:e.update(dimensions=list(im.size),mode=im.mode)
            if '/sources/' in '/'+name:e.update(role='byte_exact_native_source_copy',modification='Byte-exact source preservation')
            elif '/native_rgba/' in '/'+name:e.update(role='native_whole_cel_rgba_matte_diagnostic')
            elif '/frames/' in '/'+name:e.update(role='uniformly_mapped_whole_cel_rgba_matte_diagnostic')
            elif p.name=='approved_K0.png':e.update(role='byte_exact_approved_endpoint_source',modification='Byte-exact approvedK0 copy')
            else:e.update(role='review_only_preview_or_baseline')
        if p.suffix=='.aseprite':e.update(role='single_layer_whole_cel_editable_master')
        files.append(e)
    payload=''.join(e['path']+'\t'+e['sha256']+'\n' for e in files).encode('utf-8')
    write(target/'manifest.json',{'schema':'reef.aseprite-matte-packet.v1','status':status,
        'created_at_utc':now.isoformat(),'files':files,
        'packet_payload_rule':'Sorted relative POSIX path + TAB + SHA256 + LF for every file except this manifest.json; SHA256 of UTF8 payload',
        'packet_payload_sha256':hashlib.sha256(payload).hexdigest(),
        'acceptance':{'artifact_free_wave':False,'owner':False,'device':False,'child':False,'runtime':False,'delivery_accepted':False,'github_publication':'PENDING_ROOT_PROJECT_PACKET'}})
    return {'folder':target.relative_to(root).as_posix(),'payload_files':len(files),'packet_payload_sha256':hashlib.sha256(payload).hexdigest()}

print(json.dumps([package(folder,'REJECTED_DIAGNOSTIC_KNOWN_SOURCE_CLIPPING_AND_MASK_ARTIFACTS'),package(pilot,'LOCAL_SOURCE_STUDIES_UNACCEPTED; full_wave_matte_01_REJECTED_DIAGNOSTIC')]))
