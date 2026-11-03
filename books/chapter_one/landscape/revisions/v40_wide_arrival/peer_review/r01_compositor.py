"""Source-only wide arrival layout; no generated or painted scene pixels."""
from pathlib import Path
import json, hashlib
from PIL import Image, ImageDraw, ImageChops
V=Path(__file__).resolve().parent;R=V.parents[4]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf8',newline='\n')
A=V/'art';A.mkdir(exist_ok=True)
S=R/'assets/sprites/sky_lagoon'
bg=R/'assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_v5_hd_3x1.png'
demo=V.parent/'v39_owner_corrections/inputs/demo_landing_frame_396.png'
crop=[1250,0,4117,2048]
canvas=Image.open(bg).convert('RGBA').crop(crop)
layers=[dict(role='background',source=bg.relative_to(R).as_posix(),sha256=sha(bg),native_size=list(Image.open(bg).size),crop=crop)]
def place(p,box,role,opacity=1,im=None,operation='Uniform resampling and RGBA source-over; no relighting/repainting'):
 original=Image.open(p).convert('RGBA') if im is None else im
 x,y,w,h=box;layer=original.resize((w,h),Image.Resampling.LANCZOS)
 if opacity!=1:layer.putalpha(layer.getchannel('A').point(lambda a:round(a*opacity)))
 canvas.alpha_composite(layer,(x,y))
 layers.append(dict(role=role,source=p.relative_to(R).as_posix(),sha256=sha(p),native_size=list(Image.open(p).size),target_box=box,opacity=opacity,operation=operation))
shadow=S/'sky_lagoon_contact_shadow.png'
for box,role,opacity in [([780,1384,440,46],'slide contact',.45),([1240,1380,490,50],'swing contact',.4),([1840,1535,900,70],'castle contact',.34),([160,1627,905,53],'plane contact',.7)]:place(shadow,box,role,opacity)
place(S/'sky_lagoon_castle_stained_glass_v1.png',[1815,630,1000,977],'Pearl Castle with original Roshan glass')
place(S/'sky_lagoon_slide_v3_compact.png',[780,1000,425,412],'playground slide')
sf=R/'assets/props/story/play_swing_frame.png';ss=R/'assets/props/story/play_swing_seat.png'
place(sf,[1205,982,570,400],'existing playground swing frame')
place(ss,[1410,1020,160,296],'one existing swing seat and its two ropes')
# Irregular isolation of existing video plane, including actual landing wheels.
# All visible plane colors remain source pixels; the polygon changes alpha only.
poly=[[400,324],[408,322],[426,321],[445,323],[463,325],[471,329],[473,334],[469,338],[463,339],[475,359],[488,379],[504,401],[552,401],[582,400],[615,400],[649,400],[674,400],[687,399],[701,401],[713,405],[725,410],[736,423],[744,437],[746,440],[752,433],[759,433],[772,436],[789,437],[796,440],[795,447],[788,451],[773,456],[765,459],[775,472],[781,486],[781,495],[776,504],[766,512],[749,517],[730,521],[706,524],[707,537],[710,540],[710,548],[706,553],[700,554],[696,552],[695,547],[696,541],[700,538],[698,526],[664,527],[641,524],[613,521],[588,517],[576,514],[571,516],[565,521],[562,530],[563,538],[562,546],[558,554],[552,557],[545,557],[540,553],[537,546],[537,539],[540,532],[544,528],[545,520],[528,519],[500,523],[473,526],[444,528],[419,527],[399,523],[381,519],[368,514],[363,509],[363,505],[367,504],[378,507],[397,512],[413,513],[437,506],[464,499],[496,491],[526,484],[514,479],[502,473],[485,465],[468,457],[452,449],[436,440],[424,433],[416,429],[401,430],[390,430],[377,429],[369,426],[365,424],[366,421],[375,419],[389,418],[403,417],[402,414],[401,410],[406,407],[419,404],[440,401],[437,384],[434,367],[432,349],[430,336],[405,336],[397,334],[394,331],[395,328]]
im=Image.open(demo).convert('RGBA');mask=Image.new('L',(im.width*4,im.height*4));ImageDraw.Draw(mask).polygon([(round(x*4),round(y*4)) for x,y in poly],fill=255);mask=mask.resize(im.size,Image.Resampling.LANCZOS)
im.putalpha(mask);bounds=[358,318,802,560];im=im.crop(bounds);isolated=A/'landed_plane_source_cutout.png';im.save(isolated)
layers.append(dict(role='plane isolation',source=demo.relative_to(R).as_posix(),sha256=sha(demo),frame_index_zero_based=396,time_seconds=16.5,native_size=[1280,720],polygon=poly,crop=bounds,operation='4x polygon alpha coverage downsampled LANCZOS; RGB unchanged inside mask; source-only isolation',output=isolated.relative_to(R).as_posix(),output_sha256=sha(isolated)))
place(isolated,[120,1175,940,512],'plane on landing wheels',operation='Uniform 940/444 scale, rounding height to nearest pixel; source video pixels, no invented gear')
out=A/'sky_lagoon_wide_arrival.png';canvas.convert('RGB').save(out)
save(V/'composition_provenance.json',dict(method='Source-only non-destructive crop/cutout/compositing; no full-scene redraw, generation, RGB retouch or relighting',canvas_size=list(canvas.size),layers=layers,output=out.relative_to(R).as_posix(),output_sha256=sha(out),owner_request='PDF3/story2: no otter, wider playground plus castle in one blended location',native_resolution_limit='6144x2048 original background cropped2867x2048; castle and fixture native sizes recorded; plane is native444x242 video cutout scaled940x512, not newly generated detail. Review master, final-print PPI remains open.',source_authority=['assets_src/sky_lagoon/reductive_rebuild_2026-07-28/README.md','books/chapter_one/landscape/revisions/v39_owner_corrections/demo_source_reference.json'],generation_calls=0))
print(out)
