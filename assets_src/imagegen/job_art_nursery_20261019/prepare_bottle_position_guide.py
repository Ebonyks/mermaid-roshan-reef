"""Ignored neutral coordinate guide only. No appearance/delivery pixels."""
from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json,subprocess
root=Path(__file__).resolve().parents[3];src=Path(__file__).resolve().parent
out=root/'tmp/p5_position_guides';out.mkdir(parents=True,exist_ok=True);(out/'.gdignore').write_text('')
image=Image.new('RGB',(1254,1254),(240,240,240));draw=ImageDraw.Draw(image)
# Exact measured alpha16bounds of the selected full-size source, no appearance.
draw.rectangle((373,114,905,1163),fill=(204,204,204),outline=(90,90,90),width=3)
draw.line((340,840,940,840),fill=(0,110,190),width=5)
for x,y in [(373,114),(905,114),(373,1163),(905,1163),(373,840),(905,840)]:
    draw.line((x-12,y,x+12,y),fill=(60,60,60),width=2);draw.line((x,y-12,x,y+12),fill=(60,60,60),width=2)
draw.text((355,805),'LIQUID SURFACE y=840 / 1254',fill=(0,70,120))
draw.text((380,90),'BOTTLE BOUNDS ONLY',fill=(60,60,60))
path=out/'bottle_half_position_only.png';image.save(path)
ignored=subprocess.run(['git','check-ignore',str(path)],cwd=root,capture_output=True).returncode==0
assert ignored
record={'path':path.relative_to(root).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
    'role':'position_only','used_as_delivery_pixels':False,'excluded_by_git_ignore':ignored,
    'source_measurement':'bottle_half native alpha16bbox373,114,905,1163; native1254square',
    'meaning':'Horizontal fluid interface at840px=.67canvas height; gray footprint communicates object bounds only. No source scene/background/appearance pixels.',
    'revision_reason':'Two local half-state edits failed to lower the surface enough. Final bottle-family call changes input to an exact neutral position guide; aggregate bottle cap4calls remains unchanged. Stop on nonviability.'}
(src/'bottle_position_guide.json').write_text(json.dumps(record,indent=2)+'\n')
p=src/'prompts.json';d=json.loads(p.read_text())
next(x for x in d if x['id']=='bottle_half_retry')['disposition']='REJECTED_FILL_LEVEL_LOCAL_EDIT_DID_NOT_REACH_HALF; next and final aggregate bottle call uses a measured position-only guide'
next(x for x in d if x['id']=='quilt_half')['disposition']='REJECTED_ROLE_STACKED_FOLDS_INSTEAD_OF_HALF_UNFOLDED_PANEL; revised input starts from a single flat full quilt'
p.write_text(json.dumps(d,indent=2)+'\n')
print(str(path))
