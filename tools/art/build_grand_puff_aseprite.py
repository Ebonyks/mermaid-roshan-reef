"""Reconstruct review-only Grand Puff cels from signed stills, never video pixels.
Run from repository root, then run the emitted Lua with Aseprite --batch --script.
Pillow/scipy are technical isolation and cel-preparation tools; Aseprite owns the
native layers, frames, tags, slices, durations, and flattened round-trip export.
"""
from pathlib import Path
import json, math, hashlib
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage, sparse
from scipy.sparse.linalg import spsolve
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'assets_src/characters/grand_puff_aseprite_2026-09-14'
SRC=ROOT/'assets_src/characters/grand_puff_2026-09-13/grok_signed'
TMP=ROOT/'tmp/puff-aseprite-build'
TMP.mkdir(parents=True,exist_ok=True)
(OUT/'parts').mkdir(exist_ok=True)
(OUT/'previews').mkdir(exist_ok=True)
SIZE=512

def write_json(p,data): p.write_bytes((json.dumps(data,indent=2)+'\n').encode())
def isolate(path):
    im=Image.open(path).convert('RGB'); a=np.array(im).astype(float)
    # Lavender contour is chromatic; fill its enclosed pale eyes/pearls/sparkle.
    ink=(a[:,:,2]-a[:,:,0]>4)&(a[:,:,2]-a[:,:,1]>11)
    labels,n=ndimage.label(ink)
    counts=np.bincount(labels.ravel()); counts[0]=0
    mask=ndimage.binary_fill_holes(labels==counts.argmax())
    # Opaque contour is retained; only exterior cream is removed.
    rgba=np.dstack((a.astype('uint8'),mask.astype('uint8')*255))
    im=Image.fromarray(rgba); box=im.getbbox(); crop=im.crop(box)
    scale=min(420/crop.width,420/crop.height)
    dim=(round(crop.width*scale),round(crop.height*scale))
    crop=crop.resize(dim,Image.Resampling.LANCZOS)
    result=Image.new('RGBA',(512,512)); pos=((512-dim[0])//2,478-dim[1])
    result.alpha_composite(crop,pos)
    return result,{'source_bbox':box,'scale':scale,'offset':[pos[0]-box[0]*scale,pos[1]-box[1]*scale]}

front,tr=isolate(SRC/'grand_puff_signed_identity.jpg')
scale=tr['scale']; ox,oy=tr['offset']
def point(p): return (p[0]*scale+ox,p[1]*scale+oy)
def mask_poly(points):
    m=Image.new('L',(512,512)); ImageDraw.Draw(m).polygon([point(p) for p in points],fill=255); return m

def mask_ellipse(box):
    m=Image.new('L',(512,512)); ImageDraw.Draw(m).ellipse((*point(box[:2]),*point(box[2:])),fill=255); return m

def cut(im,mask):
    result=im.copy(); result.putalpha(Image.fromarray((np.asarray(im.getchannel('A'),dtype=float)*np.asarray(mask)/255).astype('uint8'))); return result

def heal(im,mask):
    # Harmonic painted underlay, used only beneath separated features.
    a=np.asarray(im).copy(); m=np.asarray(mask)>0
    ids=np.full(m.shape,-1,int); ids[m]=np.arange(m.sum()); yy,xx=np.nonzero(m)
    rows=[]; cols=[]; vals=[]; rhs=np.zeros((len(yy),3))
    rows.extend(range(len(yy))); cols.extend(range(len(yy))); vals.extend([4.]*len(yy))
    for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
        y=yy+dy; x=xx+dx; inside=m[y,x]
        r=np.nonzero(inside)[0]; rows.extend(r); cols.extend(ids[y[inside],x[inside]]); vals.extend([-1.]*len(r))
        rhs[~inside]+=a[y[~inside],x[~inside],:3]
    mat=sparse.csr_matrix((vals,(rows,cols)),shape=(len(yy),len(yy)))
    a[yy,xx,:3]=np.clip(spsolve(mat,rhs),0,255).astype('uint8')
    return Image.fromarray(a)

le=mask_poly([(0,0),(590,0),(590,351),(548,431),(512,474),(493,524),(462,581),(427,575),(0,575)])
re=Image.fromarray(np.fliplr(np.array(le)))
lp=mask_ellipse((326,1165,485,1332)); rp=mask_ellipse((890,1164,1052,1334))
eye_l=mask_poly([(474,800),(600,854),(602,931),(561,951),(492,944),(469,914),(465,866)])
eye_r=mask_poly([(802,856),(918,800),(936,857),(933,918),(900,949),(838,945),(808,918)])
mouth=mask_ellipse((640,914,756,977))
features=Image.fromarray(np.maximum.reduce([np.array(x) for x in [eye_l,eye_r,mouth,lp,rp]]))
body=heal(front,features)
# Overlap the ear/body seam by 4 pixels to protect against small ear follow-through.
erase=np.maximum(np.array(le.filter(ImageFilter.MinFilter(9))),np.array(re.filter(ImageFilter.MinFilter(9))))
body.putalpha(Image.fromarray((np.array(body.getchannel('A')).astype(float)*(255-erase)/255).astype('uint8')))
parts={'body_crest':body,'ear_left':cut(front,le),'ear_right':cut(front,re),'paw_left':cut(front,lp),'paw_right':cut(front,rp),
       'eyes_open':cut(front,Image.fromarray(np.maximum(np.array(eye_l),np.array(eye_r)))),'mouth_smile':cut(front,mouth)}
# Expressions are authored as new cels, with the original open eyes/smile retained.
# Draw oversampled smooth ink; these are review candidates, not accepted production art.
INK='#36204e'; LIGHT='#927ba9'; WHITE='#fff6e8'
def face_layer(kind):
    im=Image.new('RGBA',(1536,1536)); d=ImageDraw.Draw(im)
    def p(v): return tuple(z*3 for z in point(v))
    def line(coords,fill=INK,width=12): d.line([p(q) for q in coords],fill=fill,width=max(1,round(width*scale*3)),joint='curve')
    def curve(coords,fill=INK,width=12):
        q=[]
        for t in np.linspace(0,1,32):
            if len(coords)==3: v=(1-t)**2*np.array(coords[0])+2*(1-t)*t*np.array(coords[1])+t*t*np.array(coords[2])
            else: v=(1-t)**3*np.array(coords[0])+3*(1-t)**2*t*np.array(coords[1])+3*(1-t)*t*t*np.array(coords[2])+t**3*np.array(coords[3])
            q.append(v)
        line(q,fill,width)
    if kind in ('closed','wink','dizzy'):
        for side in [0,1]:
            if kind=='wink' and side==1: continue
            if kind=='dizzy' and side==0:
                q=[]
                for t in np.linspace(0,math.pi*4.2,100):
                    r=4+3.3*t; q.append((536+math.cos(t)*r,882+math.sin(t)*r))
                line(q,width=11)
            else:
                x=478 if side==0 else 815
                curve([(x,890),(x+50,832),(x+102,888)],width=14)
                curve([(x+5,899),(x+50,864),(x+97,896)],LIGHT,4)
    elif kind=='laugh':
        box=(*p((637,909)),*p((760,1001))); d.ellipse(box,fill=INK)
        d.ellipse((*p((661,960)),*p((743,992))),fill='#b17caa')
        d.polygon([p(x) for x in [(646,925),(666,929),(657,948)]],fill=WHITE)
        d.polygon([p(x) for x in [(730,929),(751,925),(741,949)]],fill=WHITE)
    elif kind=='surprise':
        d.ellipse((*p((673,930)),*p((729,986))),fill=INK)
        d.ellipse((*p((685,960)),*p((717,978))),fill='#a679a4')
        d.polygon([p(x) for x in [(679,939),(690,939),(686,951)]],fill=WHITE)
        d.polygon([p(x) for x in [(712,939),(723,939),(717,951)]],fill=WHITE)
    return im.resize((512,512),Image.Resampling.LANCZOS)
parts['eyes_closed']=face_layer('closed')
parts['eyes_wink']=face_layer('wink'); parts['eyes_wink'].alpha_composite(cut(front,eye_r))
parts['eyes_dizzy']=face_layer('dizzy')
parts['mouth_laugh']=face_layer('laugh'); parts['mouth_surprise']=face_layer('surprise')
for name,im in parts.items(): im.save(OUT/'parts'/f'{name}.png')
for view in ('profile','back'):
    im,t=isolate(SRC/f'grand_puff_{view}.jpg'); im.save(OUT/'parts'/f'{view}_reference.png')

# Parameters: body width/height, elevation, ear angles, expression, paw lift,
# and whole-body size for intact friendly ending. Frame durations are seconds.
def k(dt=.12,sx=1,sy=1,z=0,ear=0,eyes='open',mouth='smile',step=0,size=1,lean=0):
    return dict(dt=dt,sx=sx,sy=sy,z=z,ear=ear,eyes=eyes,mouth=mouth,step=step,size=size,lean=lean)
clips={
'idle':[k(.32),k(.22,sy=1.006,ear=1),k(.18,sy=1.012,ear=2),k(.10,sy=1.009,eyes='closed'),k(.10,sy=1.006),k(.28)],
'jump':[k(.15),k(.14,sx=1.025,sy=.96,ear=3),k(.20,sx=1.045,sy=.90,ear=5,eyes='closed'),k(.08,sx=.97,sy=1.005,z=6,ear=-3),k(.10,sx=.96,sy=1.015,z=16,ear=-4),k(.12,sx=.98,sy=1,z=22,ear=-2),k(.09,z=12),k(.08,sx=1.045,sy=.91,eyes='closed',ear=5),k(.12,sx=1.015,sy=.97,ear=-2),k(.20)],
'laugh_vulnerable':[k(.16),k(.12,eyes='closed'),k(.18,sx=1.015,sy=.98,eyes='closed',mouth='laugh',ear=2),k(.12,sy=1.01,eyes='closed',mouth='laugh',ear=-2),k(.16,sx=1.015,sy=.98,eyes='closed',mouth='laugh',ear=2),k(.14,sy=1.01,eyes='closed',mouth='laugh',ear=-2),k(.18,eyes='closed',mouth='laugh'),k(.16,eyes='closed'),k(.22)],
'flinch_1':[k(.07),k(.10,sx=.98,sy=1.01,ear=-4,mouth='surprise',lean=-3),k(.14,sx=1.025,sy=.95,eyes='closed',ear=4),k(.16,ear=-2),k(.24)],
'flinch_2':[k(.09),k(.12,sx=1.02,sy=.96,eyes='closed',ear=4),k(.18,eyes='dizzy',lean=-4,ear=3),k(.18,eyes='dizzy',lean=4,ear=-3),k(.18,eyes='dizzy',lean=-2,ear=2),k(.14,eyes='closed'),k(.24)],
'flinch_3':[k(.08),k(.14,sx=1.02,sy=.96,eyes='closed',ear=3),k(.22,eyes='wink',lean=2,ear=-2),k(.20,eyes='wink'),k(.24)],
'angry':[k(.18),k(.15,sx=1.015,sy=.98,ear=2),k(.20,sx=1.035,sy=.99,ear=-3,mouth='surprise'),k(.24,sx=1.04,sy=1.0,ear=-4),k(.16,sx=1.02,sy=.985,eyes='closed'),k(.22)],
'angry_jump_final':[k(.18),k(.18,sx=1.035,sy=.98,ear=-3),k(.16,sx=1.045,sy=.92,ear=4),k(.26,sx=1.05,sy=.89,ear=5,eyes='closed'),k(.08,sx=.96,sy=1.015,z=8,ear=-4),k(.11,sx=.95,sy=1.01,z=20,ear=-5),k(.14,sx=.98,sy=1,z=24,ear=-2),k(.09,z=12),k(.09,sx=1.05,sy=.90,ear=5,eyes='closed'),k(.13,sx=1.02,sy=.95,ear=-3),k(.20),k(.20,eyes='closed')],
'friends':[k(.20),k(.16,eyes='closed',sy=.98),k(.18,eyes='closed',size=.90,ear=3),k(.22,eyes='closed',size=.80,ear=2),k(.26,size=.72,eyes='closed'),k(.20,size=.72,eyes='wink'),k(.50,size=.72,eyes='closed')],
'showing':[k(.20,size=.72,eyes='closed'),k(.18,size=.78,eyes='closed'),k(.18,size=.88,ear=2),k(.20,size=.97,ear=-2),k(.16,sx=1.025,sy=.97,ear=3),k(.30)],
'peek':[k(.20,sy=.92,eyes='closed'),k(.18,sy=.96,eyes='closed',ear=2),k(.26,eyes='wink',lean=-3),k(.20,lean=3),k(.30),k(.18,sy=.96,eyes='closed'),k(.24,sy=.92,eyes='closed')],
'windup':[k(.22),k(.22,sx=1.015,sy=.98,ear=2),k(.22,sx=1.025,sy=.955,ear=3),k(.24,sx=1.04,sy=.93,ear=4),k(.20,sx=1.045,sy=.91,eyes='closed',ear=5),k(.16,sx=1.035,sy=.925,ear=3)],
'prowl':[k(.12),k(.13,sy=.97,step=-3,ear=2,lean=-2),k(.11,z=3,step=3,ear=-2,lean=2),k(.13,sx=1.015,sy=.975,step=3,ear=2,lean=2),k(.11,z=3,step=-3,ear=-2,lean=-2),k(.14)],
'giggle':[k(.16),k(.16,eyes='closed'),k(.13,eyes='closed',mouth='laugh',sy=.985,ear=2,lean=-2),k(.13,eyes='closed',mouth='laugh',sy=1.005,ear=-2,lean=2),k(.16,eyes='closed',mouth='laugh',sy=.99,ear=1),k(.16,eyes='closed'),k(.24)],
'splash':[k(.24),k(.20,ear=3,lean=-2),k(.18,ear=-2,lean=2,eyes='wink'),k(.20,sx=1.02,sy=.98,eyes='closed',ear=2),k(.24),k(.35,eyes='closed')],
}
LAYERS=['ear_left','ear_right','body_crest','paw_left','paw_right','eyes','mouth']
def transform(im,sx,sy,anchor=(256,480),dx=0,dy=0,angle=0,rotation_center=None):
    if angle: im=im.rotate(angle,Image.Resampling.BICUBIC,center=rotation_center)
    ax,ay=anchor
    return im.transform((512,512),Image.Transform.AFFINE,(1/sx,0,ax-ax/sx-dx/sx,0,1/sy,ay-ay/sy-dy/sy),Image.Resampling.BICUBIC)
frames=[]; tags=[]
for name,keys in clips.items():
    start=len(frames)+1
    for j,key in enumerate(keys):
        planes={}
        for layer in LAYERS:
            src=parts['eyes_'+key['eyes']] if layer=='eyes' else parts['mouth_'+key['mouth']] if layer=='mouth' else parts[layer]
            angle=key['ear']*(1 if layer=='ear_left' else -1) if layer.startswith('ear') else 0
            center=point((465,565) if layer=='ear_left' else (942,565))
            dy=-key['z']; dx=key['lean']
            if layer.startswith('paw'):
                sx=key['size']; sy=key['size']
                if key['step'] and ((layer=='paw_left')==(key['step']<0)): dy-=abs(key['step'])
            else: sx=key['sx']*key['size']; sy=key['sy']*key['size']
            im=transform(src,sx,sy,dx=dx,dy=dy,angle=angle,rotation_center=center)
            planes[layer]=im
        composite=Image.new('RGBA',(512,512))
        for im in planes.values(): composite.alpha_composite(im)
        idx=len(frames)+1; folder=TMP/f'{idx:03d}'; folder.mkdir(exist_ok=True)
        layerfiles=[]
        for layer,im in planes.items():
            box=im.getbbox()
            if box:
                file=folder/f'{layer}.png'; im.crop(box).save(file)
                layerfiles.append({'layer':layer,'path':file.as_posix(),'x':box[0],'y':box[1]})
        composite.save(folder/'composite.png')
        frames.append({'index':idx,'clip':name,'key':j,'duration_ms':round(key['dt']*1000),'parameters':key,'bounds':composite.getbbox(),'cels':layerfiles})
    tags.append({'name':name,'from':start,'to':len(frames),'duration_ms':sum(f['duration_ms'] for f in frames[start-1:]),'loop':name in ('idle','prowl','giggle')})
# Native Aseprite source authoring. Cels stay independently editable and named.
lua=['local s=Sprite(512,512,ColorMode.RGB)','s:deleteLayer(s.layers[1])','local layers={}']
for layer in LAYERS: lua+=['do local l=s:newLayer(); l.name='+json.dumps(layer)+'; layers['+json.dumps(layer)+']=l end']
for frame in frames:
    i=frame['index']
    if i>1: lua.append(f's:newEmptyFrame({i})')
    lua.append(f's.frames[{i}].duration={frame["duration_ms"]/1000}')
    for cel in frame['cels']:
        lua.append(f's:newCel(layers[{json.dumps(cel["layer"])}],{i},Image{{fromFile={json.dumps(cel["path"])} }},Point({cel["x"]},{cel["y"]}))')
for tag in tags: lua.append(f'do local t=s:newTag({tag["from"]},{tag["to"]}); t.name={json.dumps(tag["name"])} end')
lua+=['do local sl=s:newSlice(Rectangle(32,32,448,448)); sl.name="authoring_safe_area"; sl.pivot=Point(224,448) end',
       's.data="REVIEW_CANDIDATE; painted part articulation and authored facial cels; no video pixels; stage travel and gameplay events are external"',
       's:saveAs('+json.dumps((OUT/'grand_puff_actions.aseprite').as_posix())+')',
       's:close()']
# Separate native view board; signed references remain flat and clearly labelled.
lua+=['local v=Sprite(512,512,ColorMode.RGB)','v.layers[1].name="signed_view_RGBA"']
front.save(OUT/'parts/front_reference.png')
for i,name in enumerate(['front','profile','back'],1):
    if i>1: lua.append(f'v:newEmptyFrame({i})')
    lua+= [f'v:newCel(v.layers[1],{i},Image{{fromFile={json.dumps((OUT/"parts"/(name+"_reference.png")).as_posix())}}},Point(0,0))',f'do local t=v:newTag({i},{i}); t.name="{name}" end']
lua+=['v:saveAs('+json.dumps((OUT/'grand_puff_signed_views.aseprite').as_posix())+')','v:close()']
(TMP/'build.lua').write_bytes(('\n'.join(lua)+'\n').encode())
contract={'status':'REVIEW_CANDIDATE_NOT_RUNTIME_ACCEPTED','canvas':[512,512],'support_pivot':[256,480],'minimum_pad_px':32,'source_transform':tr,'layers':LAYERS,'tags':tags,'frames':[{k:v for k,v in f.items() if k!='cels'} for f in frames],
'construction':'Signed still paint isolated and partitioned; harmonic underpainting beneath separated features; independently articulated ears, paws, body; new facial cels. No video pixels or image generation. Not full-frame cinematic delivery.',
'limitations':['Three-quarter reconstruction is not included; front/profile/back authority views are retained.','Part articulation is a review candidate, not a claim of complete production movement or a 4.75/5 result.','Peek requires external foreground occlusion; no hatch or dust is baked in.','Jump elevation here is local acting clearance only; runtime owns full trajectory.','Third lock flash and gold counter are external effects, not character pixels.']}
write_json(OUT/'CLIP_CONTRACT.json',contract)
# Review stills + animations. GIF is only review; native RGBA cels retain alpha.
font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',16)
board=Image.new('RGB',(1280,3*300),(27,30,48)); d=ImageDraw.Draw(board)
for n,tag in enumerate(tags):
    fs=frames[tag['from']-1:tag['to']]
    images=[]
    for f in fs:
        im=Image.open(TMP/f'{f["index"]:03d}'/'composite.png')
        bg=Image.new('RGBA',(512,512),(27,30,48,255)); bg.alpha_composite(im)
        images.append(bg.convert('RGB').quantize(colors=128))
    images[0].save(OUT/'previews'/f'{tag["name"]}.gif',save_all=True,append_images=images[1:],duration=[f['duration_ms'] for f in fs],loop=0,disposal=2)
    # Most expressive authored pose, separate label from body silhouette.
    pick=fs[len(fs)//2]; im=Image.open(TMP/f'{pick["index"]:03d}'/'composite.png').resize((248,248),Image.Resampling.LANCZOS)
    x=(n%5)*256; y=(n//5)*300
    board.paste(im,(x+4,y+26),im); d.text((x+10,y+278),tag['name'],font=font,fill='#e8dcef')
board.save(OUT/'previews/action_contact_sheet.jpg',quality=94)
print('Created',len(frames),'prepared frames;',len(tags),'tags; execute',TMP/'build.lua')
