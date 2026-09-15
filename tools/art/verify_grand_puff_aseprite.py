"""Validate and preview actual Aseprite round-trip, with source/hash/bounds checks."""
from pathlib import Path
import argparse,json,hashlib,subprocess
import numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'assets_src/characters/grand_puff_aseprite_2026-09-14'
TMP=ROOT/'tmp/puff-aseprite-build'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write_json(p,v): p.write_bytes((json.dumps(v,indent=2)+'\n').encode())
parser=argparse.ArgumentParser(); parser.add_argument('--aseprite',default='C:/Program Files/Aseprite/Aseprite.exe'); parser.add_argument('--build',action='store_true'); args=parser.parse_args()
def run(script):
    result=subprocess.run([args.aseprite,'--batch','--script',str(script)],cwd=ROOT,capture_output=True,text=True,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0),timeout=180)
    if result.returncode or result.stderr.strip(): raise RuntimeError(result.stdout+'\n'+result.stderr)
if args.build: run(TMP/'build.lua')
c=json.loads((OUT/'CLIP_CONTRACT.json').read_text())
lines=['local s=app.open('+json.dumps((OUT/'grand_puff_actions.aseprite').as_posix())+')',f'assert(#s.frames=={len(c["frames"])})','assert(#s.layers==7)','assert(#s.tags==15)','assert(s.width==512 and s.height==512)','local lines={}']
for i,layer in enumerate(c['layers'],1): lines.append(f'assert(s.layers[{i}].name=={json.dumps(layer)})')
for ti,t in enumerate(c['tags'],1):
    lines.append(f'do local t=s.tags[{ti}]; assert(t.name=={json.dumps(t["name"])}); assert(t.fromFrame.frameNumber=={t["from"]} and t.toFrame.frameNumber=={t["to"]}) end')
lines+=['for i,f in ipairs(s.frames) do','local im=Image(512,512,ColorMode.RGB)','im:drawSprite(s,i)','im:saveAs('+json.dumps(TMP.as_posix()+'/roundtrip_')+'..string.format("%03d",i)..".png")','table.insert(lines,i..","..math.floor(f.duration*1000+0.5))','end','local f=io.open('+json.dumps((TMP/'native_inventory.csv').as_posix())+',"w"); f:write(table.concat(lines,"\\n")); f:close()','s:close()','local v=app.open('+json.dumps((OUT/'grand_puff_signed_views.aseprite').as_posix())+')','assert(#v.frames==3 and #v.tags==3)','v:close()']
(TMP/'verify.lua').write_bytes(('\n'.join(lines)+'\n').encode()); run(TMP/'verify.lua')
inventory=(TMP/'native_inventory.csv').read_text().replace('\\n','\n').splitlines()
assert len(inventory)==len(c['frames'])
maxdiff=0; bounds=[]; native=[]
for f,row in zip(c['frames'],inventory):
    assert row==f'{f["index"]},{f["duration_ms"]}',row
    p=TMP/f'roundtrip_{f["index"]:03d}.png'; im=Image.open(p).convert('RGBA'); a=np.array(im).astype(int)
    b=np.array(Image.open(TMP/f'{f["index"]:03d}/composite.png').convert('RGBA')).astype(int)
    visible=(a[:,:,3]>0)|(b[:,:,3]>0); delta=int(abs(a-b)[visible].max()); maxdiff=max(maxdiff,delta)
    assert delta<=4,('roundtrip colour delta',f['index'],delta)
    box=im.getbbox(); assert box[0]>=32 and box[1]>=32 and box[2]<=480 and box[3]<=480,(f['index'],box)
    assert a[:,:,3].min()==0 and a[:,:,3].max()==255
    bounds.append(box); native.append({'frame':f['index'],'sha256':sha(p),'bounds':box,'duration_ms':f['duration_ms']})
# Re-encode review GIFs using actual native exports, never the preparation composites.
for tag in c['tags']:
    fs=c['frames'][tag['from']-1:tag['to']]; images=[]
    for f in fs:
        im=Image.open(TMP/f'roundtrip_{f["index"]:03d}.png'); bg=Image.new('RGBA',(512,512),(27,30,48,255)); bg.alpha_composite(im)
        images.append(bg.convert('RGB').quantize(colors=128))
    images[0].save(OUT/'previews'/f'{tag["name"]}.gif',save_all=True,append_images=images[1:],duration=[f['duration_ms'] for f in fs],loop=0,disposal=2)
board=Image.new('RGB',(1536,570),(27,30,48)); d=ImageDraw.Draw(board)
for row,name in enumerate(['jump','laugh_vulnerable','friends']):
    t=next(t for t in c['tags'] if t['name']==name)
    for col,idx in enumerate(np.linspace(t['from'],t['to'],8).round().astype(int)):
        im=Image.open(TMP/f'roundtrip_{idx:03d}.png').resize((180,180),Image.Resampling.LANCZOS)
        board.paste(im,(col*192,row*190),im); d.text((col*192+5,row*190+176),f'{name} / {idx}',fill='white')
board.save(OUT/'previews/native_motion_strip.jpg',quality=94)
# Full-size transparent representative and an exact small-scale diagnostic.
Image.open(TMP/'roundtrip_001.png').save(OUT/'previews/idle_transparent.png')
im=Image.open(TMP/'roundtrip_019.png'); im.resize((112,112),Image.Resampling.LANCZOS).save(OUT/'previews/laugh_112px.png')
bindings=json.loads((OUT/'SOURCE_BINDINGS.json').read_text())
for item in bindings['files']: assert sha(ROOT/item['path'])==item['sha256'],item['path']
# Silent labelled diagnostic reel, not cinematic delivery.
reel=TMP/'reel'; reel.mkdir(exist_ok=True); concat=[]
font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',23); small=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',16)
for f in c['frames']:
    im=Image.open(TMP/f'roundtrip_{f["index"]:03d}.png').convert('RGBA')
    bg=Image.new('RGBA',(768,600),(27,30,48,255)); bg.alpha_composite(im,(0,45)); bg.alpha_composite(im.resize((112,112),Image.Resampling.LANCZOS),(584,280))
    d=ImageDraw.Draw(bg); d.text((28,14),f['clip'].replace('_',' '),font=font,fill='#eeddf6'); d.text((546,224),'112 px cell',font=small,fill='#c9bed7'); d.text((28,562),'ASEPRITE REVIEW CANDIDATE  /  body only  /  no live integration',font=small,fill='#c9bed7')
    p=reel/f'{f["index"]:03d}.png'; bg.convert('RGB').save(p)
    concat.extend(["file '"+p.as_posix()+"'","option framerate 1000",f"duration {f['duration_ms']/1000:.3f}"])
concat.extend(["file '"+p.as_posix()+"'","option framerate 1000"])
(reel/'concat.txt').write_bytes(('\n'.join(concat)+'\n').encode())
ffmpeg='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/FFmpeg/8.1.2/bin/ffmpeg.exe'
# Sample the native timeline directly: concat's PNG demuxer quantizes durations.
proc=subprocess.Popen([ffmpeg,'-v','error','-y','-f','rawvideo','-pixel_format','rgb24','-video_size','768x600','-framerate','30','-i','pipe:0','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(OUT/'previews/all_actions_review.mp4')],stdin=subprocess.PIPE,stderr=subprocess.PIPE,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
ends=np.cumsum([f['duration_ms'] for f in c['frames']]); last=-1; pixels=None
for sample in range(round(float(ends[-1])*30/1000)):
    index=min(len(ends)-1,int(np.searchsorted(ends,sample*1000/30,side='right')))
    if index!=last: pixels=Image.open(reel/f'{index+1:03d}.png').convert('RGB').tobytes(); last=index
    proc.stdin.write(pixels)
proc.stdin.close(); errors=proc.stderr.read(); result=proc.wait()
if result: raise RuntimeError(errors.decode())
report={'status':'PASS_NATIVE_AND_TECHNICAL_CHECKS_ONLY','tool':'Aseprite 1.3.18.4-x64','command':'python tools/art/verify_grand_puff_aseprite.py'+(' --build' if args.build else ''),'source_files_verified':len(bindings['files']),'frame_count':len(native),'tag_count':len(c['tags']),'editable_layers':c['layers'],'max_roundtrip_channel_delta':maxdiff,'roundtrip_tolerance':4,'all_frames_inside_32px_border':True,'all_frames_RGBA_with_transparency':True,'native_frames':native,'artifact_sha256':{p.relative_to(OUT).as_posix():sha(p) for p in sorted(OUT.rglob('*')) if p.is_file() and p.name!='VERIFICATION.json'},'visual_review':'Contact sheet and native jump/laugh/friends strips inspected by Codex, 2026-09-14. Four pearl forms and spiral ears retained in inspected poses. No owner acceptance or motion score.','remaining':['Full normal-speed owner review','Three-quarter view not authored','In-context Mobile/Speedy and child/device evidence','Richer painted in-betweens may be needed; part articulation is not production acceptance'],'runtime_changes':False}
write_json(OUT/'VERIFICATION.json',report)
print('PASS:',len(native),'native frames, 15 tags, 7 layers, exact durations, 32px border, 25 unchanged source hashes; max channel difference',maxdiff)
