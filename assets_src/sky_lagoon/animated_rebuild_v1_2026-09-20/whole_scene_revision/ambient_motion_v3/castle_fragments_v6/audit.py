from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
p=Path('tmp/sky-lagoon-whole-scene-v2/castle-layer-ownership-audit');base=Path('assets/sprites/sky_lagoon/whole_scene_v2');manifest=json.loads((base/'manifest.json').read_text());cards={r['id']:r for r in manifest['cards']}
master=Image.open('assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_v5_hd_3x1.png').convert('RGB')
def masks(file,cols,rows,count,position,scale,box):
 im=Image.open(base/file).convert('RGBA');cw,ch=im.width//cols,im.height//rows;result=[]
 for k in range(count):
  a=im.crop((k%cols*cw,k//cols*ch,(k%cols+1)*cw,(k//cols+1)*ch)).getchannel('A');a=a.resize((round(cw*scale),round(ch*scale)),Image.Resampling.BILINEAR);can=Image.new('L',(box[2]-box[0],box[3]-box[1]));can.paste(a,(round(position[0]-box[0]),round(position[1]-box[1])));result.append(np.asarray(can))
 return result
records=[];board=Image.new('RGB',(1248,620),'#20343e');draw=ImageDraw.Draw(board)
for side,legacy,owner,box in [('left','castle_left_verge','castle_foreground_rosette',(4500,1640,5050,2048)),('right','castle_right_verge','bellflower',(5520,1520,6144,2048))]:
 r=cards[legacy];old=masks(r['file'],r['columns'],r['rows'],r['frames'],r['position'],r['scale'],box)
 if owner=='bellflower':file='bellflower_whole_breeze.png';fore=masks(file,4,2,8,(5820-308*.95,1980-468*.95),.95,box)
 else:
  f=cards[owner];file=f['file'];fore=masks(file,f['columns'],f['rows'],f['frames'],f['position'],f['scale'],box)
 union=np.logical_or.reduce([a>8 for a in old]);overlaps=[int((union & (a>=250)).sum()) for a in fore];foreunion=np.logical_or.reduce([a>8 for a in fore]);rec={'side':side,'legacy_grass_id':legacy,'legacy_frames':len(old),'legacy_alpha_union_pixels':int(union.sum()),'nearby_whole_plant':owner,'whole_plant_frames':len(fore),'geometric_overlap_with_opaque_plant_min_max': [min(overlaps),max(overlaps)],'legacy_union_outside_all_plant_poses':int((union & ~foreunion).sum()),'source_box':box,'legacy_sha256':hashlib.sha256((base/r['file']).read_bytes()).hexdigest(),'plant_sha256':hashlib.sha256((base/file).read_bytes()).hexdigest()};records.append(rec)
 crop=master.crop(box).convert('RGBA');overlay=np.zeros((crop.height,crop.width,4),dtype='uint8');overlay[foreunion]=[0,210,255,85];overlay[union]=[255,50,160,190];crop.alpha_composite(Image.fromarray(overlay));x=0 if side=='left' else 624;board.paste(crop.convert('RGB'),(x,55));draw.text((x+8,8),f'{side}: magenta legacy grass / cyan whole plant',fill='white');draw.text((x+8,29),'Source-space alpha overlap; not a runtime occlusion verdict',fill='white')
board.save(p/'ownership.jpg',quality=95);report={'status':'SOURCE_SPACE_OWNERSHIP_DIAGNOSTIC','method':'Every played atlas alpha, mapped at declared master position and scale with rounded pixel placement. No Godot draw-order or occlusion inference.','regions':records,'finding':'Both grass-labeled source regions include non-grass painted objects. Nearby complete plant owners do not by themselves prove those legacy strokes are hidden or belong to that same plant.','next':'Capture each legacy patch alone and with complete plant owners in the actual scene, then freeze/remove incorrect partial-object motion with source restoration if necessary.','limits':['Original master used only as a spatial reference; it is not the current runtime composite.','Alpha overlap is not identity, source ownership, visibility, or animation acceptance.']};(p/'REVIEW.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(records,indent=2))
