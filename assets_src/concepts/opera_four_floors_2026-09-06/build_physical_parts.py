from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,shutil
src=Path('assets_src/concepts/opera_four_floors_2026-09-06');out=Path('assets/flats/castle/opera_house_four_floors');fg=out/'foreground';dst=out/'physical';dst.mkdir(exist_ok=True)
generated=Path('C:/Users/Peter/.codex/generated_images/01a074c8-3302-7b80-a549-9432a9186031')
for source,name in [('exec-85b92669-dd34-494d-8fe3-b594b1ec3541.png','physical_repair_master.png'),('exec-c4563414-22c2-4276-96b2-fe53b8152dc9.png','cart_empty_repair.png')]:
 if not (src/name).exists():shutil.copy2(generated/source,src/name)
master=Image.open(src/'venue_native_v7.png').convert('RGBA');repair=Image.open(src/'physical_repair_master.png').convert('RGBA')
cart=Image.open(src/'cart_empty_repair.png').convert('RGBA').resize((130,108),Image.Resampling.LANCZOS)
repair.paste(cart,(1490,625))
# Every resting scene pixel has one owner. Remove overlapping prior kiosk masks.
old=json.loads((src/'foreground_masks.json').read_text())['objects'];masks={};owned=np.zeros((941,1672),bool)
order=['snack_stand','flower_stand','left_couch','planter','right_couch','drinks_cart']
for name in order:
 m=Image.new('L',master.size);ImageDraw.Draw(m).polygon(old[name]['polygon'],fill=255);a=np.asarray(m)>0;a &= ~owned;owned |= a;masks[name]=a
parts={
'flower':{'body':'flower_stand','bit':1,'polygon':[(152,654),(158,657),(162,662),(160,667),(155,669),(149,665),(149,659)]},
'cupcake':{'body':'snack_stand','bit':1,'polygon':[(57,716),(63,717),(67,721),(70,727),(70,733),(68,738),(61,740),(53,739),(51,735),(50,729),(51,724),(54,719)]},
'cup':{'body':'drinks_cart','bit':1,'polygon':[(1550,696),(1557,695),(1562,698),(1565,701),(1565,708),(1561,711),(1552,711),(1547,708),(1546,703),(1547,699)]},
'pitcher':{'body':'drinks_cart','bit':2,'polygon':[(1559,652),(1567,650),(1587,652),(1584,656),(1591,656),(1599,657),(1602,661),(1600,668),(1596,672),(1591,672),(1590,681),(1593,690),(1590,697),(1586,702),(1579,705),(1578,709),(1576,711),(1575,721),(1579,723),(1579,726),(1568,726),(1566,723),(1570,720),(1571,710),(1569,707),(1562,705),(1559,701),(1556,696),(1555,690),(1555,682),(1557,677),(1558,669),(1556,665),(1554,662),(1556,658)]}
}
# Assign source pieces to their actual parent even at the old overlapping boundary.
part_masks={}
for name,spec in parts.items():
 m=Image.new('L',master.size);ImageDraw.Draw(m).polygon(spec['polygon'],fill=255)
 if name=='pitcher': ImageDraw.Draw(m).polygon([(1592,660),(1598,660),(1598,665),(1594,669),(1592,668)],fill=0)
 a=np.asarray(m)>0
 if name=="pitcher":
  a &= ~part_masks["cup"];m=Image.fromarray((a*255).astype("uint8"))
 for body in masks:masks[body][a]=body==spec['body']
 part_masks[name]=a;box=m.getbbox();spec['native_bounds']=list(box);spec['source_rect']=[box[0]*1280/1672,box[1]*720/941,(box[2]-box[0])*1280/1672,(box[3]-box[1])*720/941]
 rgba=master.copy();rgba.putalpha(m);card=rgba.crop(box);card.save(dst/(name+'.png'))
 spec['sha256']=hashlib.sha256((dst/(name+'.png')).read_bytes()).hexdigest()
 if name=='cupcake':
  for bite,ellipse in [(1,(8,-4,27,16)),(2,(-5,-4,28,24))]:
   bitten=card.copy();alpha=bitten.getchannel('A');ImageDraw.Draw(alpha).ellipse(ellipse,fill=0);bitten.putalpha(alpha);bitten.save(dst/f'cupcake_bite_{bite}.png')
 if name=='flower':
  a=np.asarray(card.getchannel('A'));yy,xx=np.indices(a.shape);cx=(a.shape[1]-1)/2;cy=(a.shape[0]-1)/2
  outer=((xx-cx)**2+(yy-cy)**2)>12;angles=np.mod(np.arctan2(yy-cy,xx-cx)+np.pi,2*np.pi);sectors=np.floor(angles/(2*np.pi/6)).astype(int)
  core=card.copy();core.putalpha(Image.fromarray(np.where(outer,0,a).astype('uint8')));core.save(dst/'flower_core.png')
  for i in range(6):
   petal=card.copy();petal.putalpha(Image.fromarray(np.where(outer & (sectors==i),a,0).astype('uint8')));petal.save(dst/f'flower_petal_{i}.png')
# Matching replacement bodies, never an icon/patch drawn on top of the old prop.
for body,a in masks.items():
 box=old[body]['native_bounds'];alpha=Image.fromarray((a*255).astype('uint8'));members=[(n,s) for n,s in parts.items() if s['body']==body]
 count=4 if body=='drinks_cart' else (2 if members else 1)
 for state in range(count):
  card=master.copy()
  for name,spec in members:
   if state & spec['bit']:card.paste(repair,(0,0),Image.fromarray((part_masks[name]*255).astype('uint8')))
  card.putalpha(alpha);card.crop(box).save(dst/f'{body}_{state}.png')
# Background contains zero original foreground pixels; the exact original body
# cards complete it at rest without a differently painted floor around their edges.
occupied=np.zeros((941,1672),np.uint16)
for a in masks.values():occupied+=a.astype(np.uint16)
assert occupied.max()==1
background=master.copy();background.putalpha(Image.fromarray(np.where(occupied,0,255).astype('uint8')))
for i in range(2):background.crop((i*836,0,(i+1)*836,941)).save(out/f'venue_{i}.png')
composite=background.copy()
for body in order:
 card=Image.open(dst/f'{body}_0.png');box=old[body]['native_bounds'];composite.alpha_composite(card,(box[0],box[1]))
assert np.array_equal(np.asarray(composite),np.asarray(master)),'Idle composite changed'
composite.save('tmp/opera-physical-idle.png')
manifest={'source':'venue_native_v7.png','source_sha256':hashlib.sha256((src/'venue_native_v7.png').read_bytes()).hexdigest(),'parts':parts,'rest_composite_byte_identical':True,'rest_pixel_owner_count_min':1,'rest_pixel_owner_count_max':1,'portable_identity':'Exact source pixels at exact native-to-canvas scale, no independent icons','petal_partition':'6 disjoint outer masks plus centre equal original bloom alpha','cake_states':'Alpha removal from original cupcake, no redrawn replacement','body_variants':'Original source body, with only the removed piece footprint replaced by generated empty-surface repair pixels','repair_scope':'Whole-frame and cart crop repair sources; only picked part alpha footprints used'}
manifest['body_bounds']={k:v['native_bounds'] for k,v in old.items()}
manifest['files']=[{'path':x.as_posix(),'sha256':hashlib.sha256(x.read_bytes()).hexdigest()} for x in sorted(dst.glob('*.png'))]
manifest['repairs']=[{'path':(src/n).as_posix(),'sha256':hashlib.sha256((src/n).read_bytes()).hexdigest()} for n in ['physical_repair_master.png','cart_empty_repair.png','prompt_physical_repair.txt','prompt_cart_repair.txt']]
(src/'physical_parts_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');(dst/'parts.json').write_text(json.dumps(parts,indent=2)+'\n')
print('Rest composite byte-identical; one owner per native pixel. Four physical parts extracted.')
