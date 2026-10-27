"""Full-width Sky Lagoon source geography; never condense/crop the native panorama."""
from pathlib import Path
import hashlib,json,shutil
from PIL import Image
V=Path(__file__).resolve().parent;R=V.parents[4];A=V/'art';I=V/'inputs';A.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
existing_record=V/'world_composition_provenance.json'
selected=json.loads(existing_record.read_text('utf8')).get('selection') if existing_record.exists() else None
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf8',newline='\n')
bg=R/'assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_v5_hd_3x1.png'
world=Image.open(bg).convert('RGBA');layers=[dict(role='entire original panorama',source=bg.relative_to(R).as_posix(),sha256=sha(bg),native_size=list(world.size),crop=None,operation='Complete6144x2048 landscape; no crop, warp, condensed spacing or missing water/path')]
S=R/'assets/sprites/sky_lagoon';shadow=S/'sky_lagoon_contact_shadow.png'
def place(p,box,role,opacity=1,method='Uniform source scale with integer rounding, native alpha and source-over'):
 im=Image.open(p).convert('RGBA');x,y,w,h=box;layer=im.resize((w,h),Image.Resampling.LANCZOS)
 if opacity!=1:layer.putalpha(layer.getchannel('A').point(lambda a:round(a*opacity)))
 world.alpha_composite(layer,(x,y));layers.append(dict(role=role,source=p.relative_to(R).as_posix(),sha256=sha(p),native_size=list(im.size),target_box=box,opacity=opacity,operation=method))
def contact(box,role,opacity=.5):place(shadow,box,role,opacity,'Nonuniform fitting of existing oval contact shadow; opacity only')
layout=R/'scripts/arena/sky_lagoon_layout.json';contract=json.loads(layout.read_text('utf8'))['cards']['castle'];s=contract['height_master']/contract['texture_size'][1]
cx,cy=contract['anchor_master'];ax,ay=contract['anchor_pixel'];cw=round(contract['texture_size'][0]*s);ch=round(contract['height_master']);ox=round(cx-ax*s);oy=round(cy-ay*s)
place(R/contract['path'].removeprefix('res://'),[ox,oy,cw,ch],'current four-tower Pearl Castle at authored bridge-bearing anchor')
for source,cx,base,height,role in [('sky_lagoon_slide_v3_compact.png',2550,1400,620,'slide'),('sky_lagoon_seesaw_v5_fitted.png',3826,1500,265,'seesaw')]:
 p=S/source;w,h=Image.open(p).size;ww=round(w/h*height);contact([round(cx-ww*.45),base-18,round(ww*.9),36],role+' contact',.4);place(p,[round(cx-ww/2),base-height,ww,height],'playground '+role+' at original runtime rest anchor')
sf=R/'assets/props/story/play_swing_frame.png';ss=R/'assets/props/story/play_swing_seat.png';fw,fh=Image.open(sf).size;w=round(fw/fh*480)
contact([2910,1375,580,42],'swing contact',.4);place(sf,[round(3200-w/2),910,w,480],'playground swing frame at runtime rest anchor3200,1390')
place(ss,[3100,945,200,370],'one existing swing seat and its two ropes; fixed to authored beam')
plane=V.parent/'v40_wide_arrival/art/landed_plane_source_cutout.png'
contact([675,1520,810,45],'plane soft body contact',.3);contact([996,1562,78,16],'plane main wheel contact',.7);contact([1329,1557,60,14],'plane nose wheel contact',.7)
place(plane,[620,1050,960,523],'native demo plane and wheels on full original stone landing path')
out=A/'sky_lagoon_full_world.png';world.convert('RGB').save(out)
# Appearance edit target. Transparent extension windows add page height while
# keeping the entire original world and its native geographic relationships.
page=Image.new('RGBA',(2048,1463));preview=world.resize((2048,683),Image.Resampling.LANCZOS);page.alpha_composite(preview,(0,467));target=I/'arrival_extension_target.png'
if not target.exists():page.save(target)
save(V/'world_composition_provenance.json',dict(owner_scope='Full Sky Lagoon: water, playground, landing area and route to Pearl Castle; no otter. Direct owner answer overrides rejected V40 condensed layout and stale handoff approved-V40 wording.',world_size=[6144,2048],full_panorama_preserved=True,horizontal_crop=None,geography='Original full panorama and complete left water/rope-post approach, central playground/lawn/path, mountain path and right lagoon shore; castle uses exact current runtime anchor. No condensed world.',source_contract=dict(path=layout.relative_to(R).as_posix(),sha256=sha(layout)),playground_source=dict(path='scripts/arena/sky_lagoon_promenade.gd',sha256=sha(R/'scripts/arena/sky_lagoon_promenade.gd'),role='Static source placement reference only; no game change'),layers=layers,world_output=out.relative_to(R).as_posix(),world_sha256=sha(out),extension_target=dict(path=target.relative_to(R).as_posix(),sha256=sha(target),size=[2048,1463],world_band=[0,467,2048,1150],operation='Existing composed source world resampled only for edit-target binding; transparent top/bottom windows. Not delivery art or position-only guide.',delivery_world_band=[0,1401,6144,3449],delivery_canvas=[6144,4389]),native_resolution='Native6144x2048 source world, existing card sizes and plane video resolution retained; no print upscaling or PPI acceptance. New generated extensions will have their actual native dimensions recorded separately.'))
if selected:
 record=json.loads(existing_record.read_text('utf8'));record['selection']=selected;save(existing_record,record)
print(out)
