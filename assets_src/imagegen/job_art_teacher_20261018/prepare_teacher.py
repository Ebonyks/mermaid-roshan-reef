import hashlib, json, shutil, subprocess
from pathlib import Path
from PIL import Image

root = Path.cwd()
src = root / 'assets_src/imagegen/job_art_teacher_20261018'
art = root / 'assets/opera/worlds/teacher'
art.mkdir(parents=True, exist_ok=True)
records = json.loads((src / 'prompts.json').read_text())
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
for row in records:
    output = src / (row['id'] + '_native.png')
    if not output.exists():
        shutil.copyfile(row['native_source'], output)
    row.update(native_path=output.relative_to(root).as_posix(), native_sha256=sha(output))
(src / 'prompts.json').write_text(json.dumps(records, indent=2)+'\n')
by_id = {r['id']:r for r in records}
def bounds(path):
    image = Image.open(path).convert('RGBA')
    box = image.getchannel('A').point(lambda a: 255 if a >= 16 else 0).getbbox()
    assert box
    return image, (max(0,box[0]-4),max(0,box[1]-4),min(image.width,box[2]+4),min(image.height,box[3]+4))
derived = []
def prepare(asset, native_id, size, family=None, dest=None):
    row=by_id[native_id]; source=root/row['native_path']; image, box=bounds(source)
    assert image.getchannel('A').getextrema()[0] == 0, native_id+' is opaque'
    if family:
        boxes=[bounds(root/by_id[n]['native_path'])[1] for n in family]
        box=(min(b[0] for b in boxes),min(b[1] for b in boxes),max(b[2] for b in boxes),max(b[3] for b in boxes))
    cropped=image.crop(box)
    gutter=12 if asset == "teacher_lesson_board" else 4
    scale=min((size[0]-2*gutter)/cropped.width,(size[1]-2*gutter)/cropped.height)
    assert scale <= 1
    small=cropped.resize((round(cropped.width*scale),round(cropped.height*scale)),Image.Resampling.LANCZOS)
    canvas=Image.new('RGBA',size)
    canvas.alpha_composite(small,((size[0]-small.width)//2,(size[1]-small.height)//2))
    output=dest or art/(asset+'.png'); output.parent.mkdir(parents=True,exist_ok=True);canvas.save(output)
    derived.append(dict(id=asset,native=row['native_path'],native_sha256=row['native_sha256'],output=output.relative_to(root).as_posix(),sha256=sha(output),dimensions=list(size),crop=list(box),uniform_scale=scale,changes='Strong-alpha bbox plus4px margin; uniform lossless PNG downsampling and transparent centering only; family uses common source bbox. No repaint/recolor/warp.'))
for name in ['circle','triangle','square','star','heart']:
    family=['shape_'+name+'_'+s for s in ['rest','lit']]
    for state in ['rest','lit']:
        key='shape_'+name+'_'+state;prepare(key,key,(256,256),family)
prepare('lesson_board','lesson_board_square_alpha',(1024,768))
prepare('teacher_lesson_board','lesson_board_square_alpha',(512,512),dest=root/'assets/opera/worlds/hotspots/teacher_lesson_board.png')
for name in ['shape_slot','join_shell']:
    prepare(name,name,(256,256))
for name in ['tray_aqua','tray_pink']:
    prepare(name,name,(512,384))
for name in ['pearl_uncounted','pearl_counted']:
    prepare(name,name,(128,128),['pearl_uncounted','pearl_counted'])
for name in ['answer_card_rest','answer_card_chosen','answer_card_right']:
    prepare(name,name,(512,512),['answer_card_rest','answer_card_chosen','answer_card_right'])
prepare('guide_hand','guide_hand',(512,512))
prepare('invitation_ring','invitation_ring',(256,128))
prepare('opera_crest_teacher','crest_teacher',(256,256),dest=root/'assets/opera/worlds/ui/crests/opera_crest_teacher.png')
(src/'provenance.json').write_text(json.dumps({'tool':'builtin ImageGen','model_revision':'unexposed; owner approved available tool','source_baseline':'6fb96aeb441952c1053cc5ce18435fc57fc1d1ab','records':derived,'acceptance':'Candidate only. Source and current Mobile context require4.5 per applicable dimension; device/child/owner remain open.'},indent=2)+'\n')
license_file=root/'ASSET_LICENSES.md'
license_text=license_file.read_text(encoding='utf-8')
for row in records:
    path=row['native_path']
    if '| `'+path+'` |' not in license_text:
        license_text+='\n| `'+path+'` | OpenAI built-in ImageGen; model revision unexposed | Owner-requested generated game object; OpenAI output terms | https://openai.com/policies/terms-of-use/ | Native preserved; '+row['status']+'; prompt/hash in assets_src/imagegen/job_art_teacher_20261018/prompts.json. |'
for row in derived:
    path=row['output']
    if '| `'+path+'` |' not in license_text:
        license_text+='\n| `'+path+'` | OpenAI ImageGen derivative | Owner-requested generated game object; OpenAI output terms | https://openai.com/policies/terms-of-use/ | '+row['changes']+' SHA256 '+row['sha256']+'; provenance in assets_src/imagegen/job_art_teacher_20261018/provenance.json. |'
license_file.write_text(license_text+'\n',encoding='utf-8')
print('Prepared',len(derived),'runtime PNGs from',len(records),'native attempts')
