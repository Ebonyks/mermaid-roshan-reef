"""Preserve sources and measure background-hole seeds. No Python pixel writes."""
from pathlib import Path
from PIL import Image
import numpy as np,cv2,sys,shutil,hashlib,json,datetime
pilot=Path(__file__).resolve().parent
root=next(p for p in pilot.parents if (p/'project.godot').is_file())
source=Path(sys.argv[1]).resolve();folder=pilot/sys.argv[2]
assert folder.parent==pilot and not folder.exists(), 'Use a new owned candidate folder'
assert source.is_relative_to(root/'assets_src/animation/roshan_wave_repair_20261010/aseprite_paint_trial_01')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p): return p.relative_to(root).as_posix()
def write(p,data): p.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
folder.mkdir();(folder/'sources').mkdir();rows=[];unusual=[];seed_counts=[]
for n in range(41):
    p=source/f'{n:04d}.png';dest=folder/'sources'/p.name;shutil.copyfile(p,dest)
    a=np.array(Image.open(p).convert('RGB'));h,w=a.shape[:2];pad=w-640
    assert [w,h]==[768,896], 'This candidate expects the reviewed 128px left workspace expansion'
    eligible=((a.max(2)-a.min(2)<=10)&(a.min(2)>=205)).astype('uint8')
    _,labels,stats,_=cv2.connectedComponentsWithStats(eligible,connectivity=4)
    outside=set(labels[0])|set(labels[-1])|set(labels[:,0])|set(labels[:,-1]);outside.discard(0)
    def component(i):
        x,y,cw,ch,area=[int(v) for v in stats[i]]
        mask=(labels==i).astype('uint8');distance=cv2.distanceTransform(mask,cv2.DIST_L2,3)
        yy,xx=np.unravel_index(np.argmax(distance),distance.shape)
        return {'label':int(i),'bbox':[x,y,cw,ch],'area':area,'seed':[int(xx),int(yy)],
            'review_status':'PENDING_ACTUAL_SOURCE_CONTACT_REVIEW'}
    hair=[];left=[]
    for i,(x,y,cw,ch,area) in enumerate(stats):
        if i==0 or i in outside: continue
        if 405+pad<=x<=505+pad and 180<=y<=265 and 20<=area<=600 and cw<=70 and ch<=60:hair.append(component(i))
        elif 165+pad<=x<=195+pad and 200<=y<=270 and 60<=area<=250 and cw<=15 and ch<=45:left.append(component(i))
        elif x<215+pad and y<390 and area>=20:
            unusual.append({'frame':n,'bbox':[int(x),int(y),int(cw),int(ch)],'area':int(area),
                'review_status':'PRESERVE_AMBIGUOUS_CLOSED_PALE_REGION_FOR_PAINT_REVIEW'})
    assert len(hair)==1,(n,'Pink hair-loop background not uniquely identified',hair)
    assert len(left)<=1,(n,'Left-curl hole has ambiguous multiple components',left)
    seed_counts.append(len(left))
    rows.append({'index':n,'source_path':rel(p),'source_sha256':sha(p),
        'preserved_source_path':rel(dest),'preserved_source_sha256':sha(dest),'source_size':[w,h],
        'hair_gap_component':hair[0],'left_curl_gap_components':left})
metadata=[]
for name in ['recipe_profile.json','joint_geometry.json','head_boundary_masks.json','paint_connected.lua','wave_native_rgb.aseprite']:
    p=source/name
    if p.is_file():
        metadata.append({'path':rel(p),'sha256':sha(p),'bytes':p.stat().st_size,'role':'preserved_source_workflow_or_master_reference'})
        if p.suffix=='.json': shutil.copyfile(p,folder/('input_'+name))
shutil.copyfile(pilot/'full_wave_matte_01'/'approved_K0.png',folder/'approved_K0.png')
write(folder/'source_and_seed_plan.json',{'schema':'reef.whole-cel-matte-source-seed-plan.v1',
    'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_packet':rel(source),
    'status':'PENDING_ALL41_SOURCE_BACKGROUND_COMPONENT_REVIEW','sources':rows,
    'source_workflow_references':metadata,'unusual_other_closed_neutral_components':unusual,
    'note':'Only specific model-reviewed true-background hole components may be seeded. Ambiguous shoulder paint stays intact. Coordinates are measured fresh in the padded sources, not copied from a prior drawing.'})
review_seed="""local root=app.params.root;local pc=app.pixelColor
local f=io.open(root..'/source_and_seed_plan.json','r');local plan=json.decode(f:read('*a'));f:close()
local right=Image(1024,672,ColorMode.RGB);local left=Image(1024,1152,ColorMode.RGB)
for _,row in ipairs(plan.sources) do
 local n=row.index;local im=Image{fromFile=root..string.format('/sources/%04d.png',n)}
 local pad=im.width-640;local bx=405+pad;local by=170;local crop=Image(im,Rectangle(bx,by,128,112))
 local sx,sy=row.hair_gap_component.seed[1]-bx,row.hair_gap_component.seed[2]-by
 for d=-4,4 do if d~=0 then crop:drawPixel(sx+d,sy,pc.rgba(255,0,0,255));crop:drawPixel(sx,sy+d,pc.rgba(255,0,0,255)) end end
 right:drawImage(crop,Point((n%8)*128,math.floor(n/8)*112))
 local leftCrop=Image(im,Rectangle(135+pad,200,128,192))
 for _,c in ipairs(row.left_curl_gap_components) do local xx,yy=c.seed[1]-135-pad,c.seed[2]-200;for d=-4,4 do if d~=0 then leftCrop:drawPixel(xx+d,yy,pc.rgba(255,0,0,255));leftCrop:drawPixel(xx,yy+d,pc.rgba(255,0,0,255)) end end end
 left:drawImage(leftCrop,Point((n%8)*128,math.floor(n/8)*192))
end
right:saveAs(root..'/hair_seed_review_board.png');left:saveAs(root..'/left_curl_and_other_islands_review_board.png')
"""
(folder/'review_seeds.lua').write_text(review_seed,encoding='utf-8')
script=(pilot/'full_wave_matte_01'/'recover_full_edges.lua').read_text(encoding='utf-8')
script=script.replace('REJECTED_DIAGNOSTIC_KNOWN_SOURCE_CLIPPING_AND_MASK_ARTIFACTS','UNACCEPTED_MATTE_CANDIDATE_REVIEW_REQUIRED')
script=script.replace("local manualSeeds={seedRows[n].hair_gap_component.seed}","assert(seedRows[n].hair_gap_component.review_status=='MODEL_REVIEWED_TRUE_BACKGROUND','Review every actual background-hole crop before applying');local manualSeeds={seedRows[n].hair_gap_component.seed}")
script=script.replace("'native_rgba','baseline_native_rgba'","'native_rgba','upstream_endpoint_matte','baseline_native_rgba'")
script=script.replace(" cleaned:saveAs(root..string.format('/native_rgba/%04d.png',n))", """ if n==0 or n==40 then
  cleaned:saveAs(root..string.format('/upstream_endpoint_matte/%04d.png',n))
  local endpoint=Image(approvedK0);endpoint:resize{width=819,height=819,method='bilinear'}
  local nativeEndpoint=Image(w,h,ColorMode.RGB);nativeEndpoint:drawImage(endpoint,Point(-48,32));cleaned=nativeEndpoint
  stats.final_native_endpoint_replacement={source='approved_K0.png',source_dimensions={256,256},whole_resized_dimensions={819,819},uniform_raster_scale=819/256,translation={-48,32},ideal_inverse_mapping_scale=3.2,ideal_inverse_mapping_translation={-48,32},upstream_matte_preserved=true}
 end
 cleaned:saveAs(root..string.format('/native_rgba/%04d.png',n))""")
script=script.replace("native_source_matte.aseprite","native_final_wave.aseprite")
(folder/'recover_full_edges.lua').write_text(script,encoding='utf-8')
black=(pilot/'full_wave_matte_01'/'black_review.lua').read_text(encoding='utf-8').replace('Image(3200,3600','Image(3840,3600').replace('Rectangle(0,95,640,400)','Rectangle(0,95,768,400)').replace('(n%5)*640','(n%5)*768')
black=black.replace("if n==14 or n==26 or n==40 then nativeBg:saveAs(root..string.format('/native_on_black/%04d.png',n)) end","nativeBg:saveAs(root..string.format('/native_on_black/%04d.png',n))")
black+= """\nlocal nativeMaster=app.open(root..'/native_final_wave.aseprite')
for _,n in ipairs({0,40}) do local im=Image(nativeMaster.width,nativeMaster.height,ColorMode.RGB);im:drawSprite(nativeMaster,n+1);im:saveAs(root..string.format('/reopen_check/native_%04d.png',n)) end
nativeMaster:close()
"""
(folder/'black_review.lua').write_text(black,encoding='utf-8')
verification=(pilot/'full_wave_matte_01'/'verify_full_matte.py').read_text(encoding='utf-8')
verification=verification.replace('REJECTED_DIAGNOSTIC_KNOWN_SOURCE_CLIPPING_AND_MASK_ARTIFACTS','UNACCEPTED_MATTE_CANDIDATE')
verification=verification.replace('Known source anatomy clipping and paint-mask rectangles remain.','Native source contour focus and neighboring painted transitions require separate complete-motion review; no final acceptance is inferred from preservation checks.')
verification=verification.replace("a=np.array(Image.open(source).convert('RGBA')); out=np.array(Image.open(native).convert('RGBA'))", "preservation_native=folder/'upstream_endpoint_matte'/f'{n:04d}.png' if n in [0,40] else native\n    a=np.array(Image.open(source).convert('RGBA')); out=np.array(Image.open(preservation_native).convert('RGBA'))")
verification=verification.replace("'native_rgba_sha256':sha(native),'final_rgba_sha256':sha(final)","'native_rgba_sha256':sha(native),'preservation_matte_sha256':sha(preservation_native),'native_endpoint_replacement':n in [0,40],'final_rgba_sha256':sha(final)")
verification=verification.replace("native_source_matte.aseprite","native_final_wave.aseprite")
verification=verification.replace("masters=[master_info", "native_endpoints=[]\nfor n in [0,40]:\n    native=np.array(Image.open(folder/'native_rgba'/f'{n:04d}.png').convert('RGBA')); reopened=np.array(Image.open(folder/'reopen_check'/f'native_{n:04d}.png').convert('RGBA'))\n    native_endpoints.append({'frame_index':n,'approved_k0_sha256':sha(approved),'whole_resized_dimensions':[819,819],'uniform_raster_scale':819/256,'translation':[-48,32],'ideal_inverse_mapping_scale':3.2,'relative_scale_error_pct':100*((819/256)/3.2-1),'master_alpha_exact':bool(np.array_equal(native[:,:,3],reopened[:,:,3])),'master_visible_rgb_exact':bool(np.array_equal(native[:,:,:3][native[:,:,3]>0],reopened[:,:,:3][native[:,:,3]>0]))})\n\nmasters=[master_info")
verification=verification.replace("'endpoints_exact':all(e['export_exact_png_bytes']", "'native_endpoint_master_pixels_exact':all(e['master_alpha_exact'] and e['master_visible_rgb_exact'] for e in native_endpoints),\n    'endpoints_exact':all(e['export_exact_png_bytes']")
verification=verification.replace("'endpoints':endpoints", "'endpoints':endpoints,'native_endpoint_replacements':native_endpoints")
(folder/'verify_full_matte.py').write_text(verification,encoding='utf-8')
print(json.dumps({'folder':rel(folder),'frames':len(rows),'source_size':[768,896],
    'hair_seed_ranges':[[min(r['hair_gap_component']['seed'][j] for r in rows),max(r['hair_gap_component']['seed'][j] for r in rows)] for j in range(2)],
    'closed_left_curl_frames':[n for n,c in enumerate(seed_counts) if c],'ambiguous_preserved_components':unusual}))
