"""Read-only pixel verification and JSON records; never writes or edits an image."""
from pathlib import Path
from PIL import Image
import numpy as np, cv2, hashlib, json, struct, datetime

folder=Path(__file__).resolve().parent
root=next(p for p in folder.parents if (p/'project.godot').is_file())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,data): p.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
plan=json.loads((folder/'source_and_seed_plan.json').read_text(encoding='utf-8'))
rows=[]
for row in plan['sources']:
    n=row['index']; original=root/row['source_path']; source=folder/'sources'/f'{n:04d}.png'
    native=folder/'native_rgba'/f'{n:04d}.png'; final=folder/'frames'/f'{n:04d}.png'
    preservation_native=folder/'upstream_endpoint_matte'/f'{n:04d}.png' if n in [0,40] else native
    a=np.array(Image.open(source).convert('RGBA')); out=np.array(Image.open(preservation_native).convert('RGBA'))
    rgb=a[:,:,:3]; eligible=((rgb.max(2)-rgb.min(2)<=10)&(rgb.min(2)>=205)).astype('uint8')
    _,labels,stats,_=cv2.connectedComponentsWithStats(eligible,connectivity=4)
    outside=set(labels[0])|set(labels[-1])|set(labels[:,0])|set(labels[:,-1]); outside.discard(0)
    seeds=[row['hair_gap_component']['seed']]+[c['seed'] for c in row['left_curl_gap_components']]
    for x,y in seeds:
        assert eligible[y,x], (n,'reviewed seed no longer background')
        outside.add(int(labels[y,x]))
    strict_removed=np.isin(labels,list(outside))&(eligible>0)
    protected=(eligible>0)&~strict_removed
    rgb16=rgb.astype('int16')
    broad_eligible=((rgb16.max(2)-rgb16.min(2)<=22)&(rgb16.min(2)>=170)).astype('uint8')
    _,broad_labels=cv2.connectedComponents(broad_eligible,connectivity=4)
    broad_outside=set(broad_labels[0])|set(broad_labels[-1])|set(broad_labels[:,0])|set(broad_labels[:,-1]); broad_outside.discard(0)
    for x,y in seeds: broad_outside.add(int(broad_labels[y,x]))
    removed=np.isin(broad_labels,list(broad_outside))&(broad_eligible>0)&~protected
    retained=~removed
    depth=cv2.distanceTransform(retained.astype('uint8'),cv2.DIST_C,3)
    deep=retained&(depth>4)
    altered=(out[:,:,:3]!=rgb).any(2)|(out[:,:,3]!=255)
    native_size=list(Image.open(native).size); final_size=list(Image.open(final).size)
    rows.append({'frame_index':n,'source_path':row['source_path'],'source_sha256':sha(original),
        'preserved_source_sha256':sha(source),'source_copy_byte_exact':sha(original)==sha(source)==row['source_sha256'],
        'native_rgba_sha256':sha(native),'preservation_matte_sha256':sha(preservation_native),'native_endpoint_replacement':n in [0,40],'final_rgba_sha256':sha(final),
        'native_dimensions':native_size,'final_dimensions':final_size,
        'reviewed_background_seeds':seeds,'source_matte_seed_pixels_transparent':all(int(out[y,x,3])==0 for x,y in seeds),'background_mask_pixels':int(removed.sum()),
        'deep_retained_pixels':int(deep.sum()),'modified_retained_pixels_beyond4px':int((deep&altered).sum()),
        'classifier_min_rgb':170,'classifier_max_chroma':22,'modification_band_px':4,'classified_field_nonzero_alpha_pixels':int(((out[:,:,3]>0)&removed).sum()),'protected_closed_neutral_pixels':int(protected.sum()),'modified_protected_closed_neutral_pixels':int((protected&altered).sum()),
        'native_foreground_pixels_on_left_edge':int((out[:,0,3]>0).sum()),
        'native_foreground_pixels_on_right_edge':int((out[:,-1,3]>0).sum())})

def master_info(path):
    b=path.read_bytes(); assert struct.unpack_from('<H',b,4)[0]==0xA5E0
    count,width,height=struct.unpack_from('<HHH',b,6); offset=128; durations=[]; layers=0
    for f in range(count):
        size,magic,old,duration,_,new=struct.unpack_from('<IHHH2sI',b,offset);assert magic==0xF1FA
        q=offset+16
        for _ in range(new or old):
            chunk_size,kind=struct.unpack_from('<IH',b,q)
            if f==0 and kind==0x2004: layers+=1
            q+=chunk_size
        durations.append(duration);offset+=size
    return {'file':path.name,'sha256':sha(path),'frame_count':count,'dimensions':[width,height],
        'layers':layers,'durations_ms':durations,'total_duration_ms':sum(durations)}

approved=folder/'approved_K0.png'; k0=np.array(Image.open(approved).convert('RGBA')); endpoints=[]
for n in [0,40]:
    export=folder/'frames'/f'{n:04d}.png'; reopened=folder/'reopen_check'/f'{n:04d}.png'
    r=np.array(Image.open(reopened).convert('RGBA'))
    endpoints.append({'frame_index':n,'approved_k0_sha256':sha(approved),'export_sha256':sha(export),
        'export_exact_png_bytes':export.read_bytes()==approved.read_bytes(),
        'reopened_master_alpha_exact':bool(np.array_equal(r[:,:,3],k0[:,:,3])),
        'reopened_master_visible_rgb_exact':bool(np.array_equal(r[:,:,:3][k0[:,:,3]>0],k0[:,:,:3][k0[:,:,3]>0]))})

native_endpoints=[]
for n in [0,40]:
    native=np.array(Image.open(folder/'native_rgba'/f'{n:04d}.png').convert('RGBA')); reopened=np.array(Image.open(folder/'reopen_check'/f'native_{n:04d}.png').convert('RGBA'))
    native_endpoints.append({'frame_index':n,'approved_k0_sha256':sha(approved),'whole_resized_dimensions':[819,819],'uniform_raster_scale':819/256,'translation':[-48,32],'ideal_inverse_mapping_scale':3.2,'relative_scale_error_pct':100*((819/256)/3.2-1),'master_alpha_exact':bool(np.array_equal(native[:,:,3],reopened[:,:,3])),'master_visible_rgb_exact':bool(np.array_equal(native[:,:,:3][native[:,:,3]>0],reopened[:,:,:3][native[:,:,3]>0]))})

masters=[master_info(folder/'wave.aseprite'),master_info(folder/'native_final_wave.aseprite')]
checks={'classified_field_stays_alpha_zero':all(r['classified_field_nonzero_alpha_pixels']==0 for r in rows),
    'all_source_copies_byte_exact':all(r['source_copy_byte_exact'] for r in rows),
    'all_reviewed_background_seed_pixels_transparent':all(r['source_matte_seed_pixels_transparent'] for r in rows),
    'all_deep_retained_pixels_unchanged':all(r['modified_retained_pixels_beyond4px']==0 for r in rows),
    'all_closed_neutral_highlights_unchanged':all(r['modified_protected_closed_neutral_pixels']==0 for r in rows),
    'all_final_frames_256':all(r['final_dimensions']==[256,256] for r in rows),
    'all_native_frames_match_source_size':all(r['native_dimensions']==plan['sources'][r['frame_index']]['source_size'] for r in rows),
    'masters_have_41_frames_one_layer_1708ms':all(m['frame_count']==41 and m['layers']==1 and m['total_duration_ms']==1708 for m in masters),
    'native_endpoint_master_pixels_exact':all(e['master_alpha_exact'] and e['master_visible_rgb_exact'] for e in native_endpoints),
    'endpoints_exact':all(e['export_exact_png_bytes'] and e['reopened_master_alpha_exact'] and e['reopened_master_visible_rgb_exact'] for e in endpoints)}
record={'schema':'reef.whole-cel-matte-verification.v1','verified_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'status':'UNACCEPTED_MATTE_CANDIDATE_REVIEW_REQUIRED','checks':checks,
    'machine_preservation_checks_pass':all(checks.values()),'frames':rows,'masters':masters,'endpoints':endpoints,'native_endpoint_replacements':native_endpoints,
    'pixel_write_method':'Aseprite Lua only. Python reads and measures pixels, hashes files, and writes JSON records.',
    'model_visual_review':'All 41 seed crops and left-curl/shoulder crops reviewed before application; all 41 output cels reviewed on black and light contacts and native upper-body black contact. Source arm-shadow remnants at1..11 and27..39 remain. Native source contour noise and focus remain; no final acceptance is inferred from preservation checks.',
    'acceptance':{'artifact_free_wave':False,'owner':False,'device':False,'child':False,'runtime':False,'delivery_accepted':False}}
write(folder/'verification.json',record)
print(json.dumps({'checks':checks,'source_left_edge_foreground':[(r['frame_index'],r['native_foreground_pixels_on_left_edge']) for r in rows if r['native_foreground_pixels_on_left_edge']], 'masters':masters,'endpoints':endpoints,'native_endpoint_replacements':native_endpoints}))
