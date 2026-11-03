"""Prepare a reproducible source-only Canvas rig; never alter source masters.

Image operations are registration, alpha cleanup, patch extraction and resampling.
All new painted pixels come from the retained ImageGen sources.
"""
from pathlib import Path
import hashlib
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops
from scipy import ndimage

ROOT = Path(__file__).resolve().parents[1]
SIZE = 1024
SCALE = 0.66
OFFSET = np.array([86., 92.])


def save_json(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')


def xy(x, y):
    return np.array([x, y]) * SCALE + OFFSET


def smooth(x):
    x = np.clip(x, 0., 1.)
    return x * x * (3. - 2. * x)


def clean_source(path):
    im = Image.open(path).convert('RGBA')
    a = np.array(im)
    labels, n = ndimage.label(a[:, :, 3] > 48)
    counts = np.bincount(labels.ravel())
    counts[0] = 0
    main = labels == np.argmax(counts)
    support = ndimage.binary_dilation(main, iterations=3)
    a[:, :, 3] *= support
    return Image.fromarray(a), {'source_size': im.size, 'removed_alpha_pixels': int(np.sum((np.array(im)[:, :, 3] > 0) & ~support))}


def canvas_image(im):
    canvas = Image.new('RGBA', (SIZE, SIZE))
    canvas.alpha_composite(im.resize((round(im.width*SCALE), round(im.height*SCALE)), Image.Resampling.LANCZOS), tuple(OFFSET.astype(int)))
    return canvas


def bone_specs():
    # Coordinates measured on the retained native neutral source, not guessed from a generated pose.
    return [
        ('Root', None, (680, 581), (700, 581)),
        ('Torso', 'Root', (680, 581), (681, 390)),
        ('Head', 'Torso', (681, 390), (681, 155)),
        ('LeftUpper', 'Torso', (589, 436), (550, 549)),
        ('LeftFore', 'LeftUpper', (550, 549), (492, 630)),
        ('LeftHand', 'LeftFore', (492, 630), (445, 696)),
        ('RightUpper', 'Torso', (790, 423), (833, 548)),
        ('RightFore', 'RightUpper', (833, 548), (891, 642)),
        ('RightHand', 'RightFore', (891, 642), (925, 705)),
        ('TailA', 'Root', (680, 581), (719, 755)),
        ('TailB', 'TailA', (719, 755), (725, 934)),
        ('TailC', 'TailB', (725, 934), (640, 1058)),
        ('TailD', 'TailC', (640, 1058), (528, 1063)),
        ('Fin', 'TailD', (528, 1063), (367, 1005)),
    ]


def weights(points, specs):
    native = (points - OFFSET) / SCALE
    x, y = native.T
    weights = np.zeros((len(specs), len(points)))
    idx = {b[0]: i for i, b in enumerate(specs)}
    def put(name, w):
        weights[idx[name]] += w
    # Semantic arm regions include transparent separation, so the elbow cannot drag the bodice.
    rows=[400,450,470,490,510,530,550,570,590,610,630,650,670,690,710,740]
    left_boundary = np.interp(y,rows,[615,616,617,615,613,611,599,587,581,570,558,551,548,542,527,520])
    right_boundary = np.interp(y,rows,[770,771,774,777,781,786,807,816,823,838,854,864,870,877,895,900])
    boundary_width=np.interp(y,[400,470,490],[40,12,4])
    left = smooth((left_boundary-x)/boundary_width) * smooth((y-400)/45) * (y < 745)
    right = smooth((x-right_boundary)/boundary_width) * smooth((y-400)/45) * (y < 745)
    left *= 0
    right *= 0
    static_right_arm=smooth((x-right_boundary)/4)*smooth((y-470)/45)*(y<745)
    arms = np.clip(left+right+static_right_arm, 0, 1)
    put('Torso',static_right_arm)
    for prefix, aw in [('Left', left), ('Right', right)]:
        fore = smooth((y-505)/80)
        hand = smooth((y-617)/45)
        put(prefix+'Upper', aw*(1-fore))
        put(prefix+'Fore', aw*fore*(1-hand))
        put(prefix+'Hand', aw*fore*hand)
    body = 1-arms
    head = 1-smooth((y-345)/65)
    head = np.maximum(head,smooth((x-804)/25)*(y<470))
    head = np.maximum(head,(1-smooth((x-550)/35))*(y<450))
    tail = smooth((y-540)/150)
    put('Head', body*head)
    put('Torso', body*(1-head)*(1-tail))
    # Piecewise smooth weights follow the curved tail, rather than straight vertical bands.
    centers = np.array([xy(*b[2]) for b in specs[9:]] + [xy(*specs[-1][3])])
    seg = centers[1:]-centers[:-1]
    v = points[:, None, :]-centers[None, :-1, :]
    proj = np.clip(np.sum(v*seg[None,:,:],axis=2)/np.sum(seg*seg,axis=1),0,1)
    closest = centers[None,:-1,:]+proj[:,:,None]*seg[None,:,:]
    d2 = np.sum((points[:,None,:]-closest)**2,axis=2)
    near = np.argmin(d2,axis=1)
    arclength = np.r_[0,np.cumsum(np.linalg.norm(seg,axis=1))]
    s = arclength[near]+proj[np.arange(len(points)),near]*np.linalg.norm(seg,axis=1)[near]
    # One chain cross-section blend per joint; flukes are rigid as one authored shape.
    tw = np.zeros((5,len(points)))
    for i in range(5):
        start = arclength[i]
        before = np.ones(len(points)) if i == 0 else smooth((s-start+60)/120)
        after = np.ones(len(points)) if i == 4 else 1-smooth((s-arclength[i+1]+60)/120)
        tw[i] = before*after
    tw /= np.maximum(tw.sum(axis=0),1e-10)
    for i,name in enumerate(['TailA','TailB','TailC','TailD','Fin']):
        put(name,body*(1-head)*tail*tw[i])
    weights /= np.maximum(weights.sum(axis=0),1e-10)
    return weights


def make_mesh(image, specs, arm=False, rigid=None):
    step=6
    axis=np.r_[np.arange(0,SIZE,step),SIZE].astype(float)
    gx,gy=np.meshgrid(axis,axis)
    points=np.c_[gx.ravel(),gy.ravel()]
    n=len(axis);tri=[]
    for row in range(n-1):
        for col in range(n-1):
            a=row*n+col;b=a+1;c=a+n;d=c+1
            tri.extend([(a,b,d),(a,d,c)])
    support=ndimage.maximum_filter(np.array(image)[:,:,3],size=27)>0
    visible=[]
    for t in tri:
        q=points[list(t)]
        samples=np.vstack([q,q.mean(axis=0),(.5*q+.5*np.roll(q,1,axis=0))])
        samples=np.clip(samples.astype(int),0,SIZE-1)
        if support[samples[:,1],samples[:,0]].any():visible.append(t)
    used=np.unique(np.array(visible).ravel());remap=np.full(len(points),-1);remap[used]=np.arange(len(used))
    tri=remap[np.array(visible)];points=points[used]
    if rigid:
        w=np.zeros((len(specs),len(points)))
        w[[b[0] for b in specs].index(rigid)]=1
    elif arm:
        y=((points-OFFSET)/SCALE)[:,1]
        fore=smooth((y-465)/180);hand=smooth((y-617)/45)
        w=np.zeros((len(specs),len(points)))
        for name,val in [('LeftUpper',1-fore),('LeftFore',fore*(1-hand)),('LeftHand',fore*hand)]:
            w[[b[0] for b in specs].index(name)]=val
    else:w=weights(points,specs)
    return {'vertices':points.tolist(),'triangles':tri.tolist(),'weights':{s[0]:w[i].round(9).tolist() for i,s in enumerate(specs)}}


def main():
    art = ROOT/'art'
    art.mkdir(exist_ok=True)
    neutral, cleanup = clean_source(ROOT/'native/neutral.png')
    base = canvas_image(neutral)
    base.save(art/'neutral.png')
    # Preserve the original arm below the sleeve. Only the formerly hidden shoulder
    # cap comes from the isolated ImageGen repair; it is uniformly registered.
    arm_source,_=clean_source(ROOT/'native/shoulder_arm.png')
    # Input shoulder (735,390), wrist (490,910) -> original shoulder/wrist.
    factor=194/520
    cap=Image.new('RGBA',neutral.size)
    resized=arm_source.resize((round(arm_source.width*factor),round(arm_source.height*factor)),Image.Resampling.LANCZOS)
    cap.alpha_composite(resized,(round(589-735*factor),round(436-390*factor)))
    yy,xx=np.mgrid[:neutral.height,:neutral.width]
    boundary=np.interp(yy,[400,450,470,490,510,530,550,570,590,610,630,650,670,690,710,740],[615,616,617,615,613,611,599,587,581,570,558,551,548,542,527,520])
    region=(xx<boundary)&(yy>430)&(yy<740)
    native_array=np.array(neutral)
    violet=(native_array[:,:,2]>native_array[:,:,0]*.95)&(native_array[:,:,2]>native_array[:,:,1]*1.08)&(yy<459)&(yy>400)&(xx>530)&(xx<620)
    sleeve=ndimage.binary_dilation(violet,iterations=2)
    removal=region & ~sleeve
    body_array=native_array.copy();body_array[:,:,3][removal]=0
    body_art=canvas_image(Image.fromarray(body_array));body_art.save(art/'body.png')
    original_arm=native_array.copy();original_arm[:,:,3]*=removal
    cap_array=np.array(cap)
    transition=smooth((yy-440)/20)
    arm_array=cap_array.astype(float)*(1-transition[:,:,None])+original_arm.astype(float)*transition[:,:,None]
    arm_array[:,:,3]*=(xx<boundary+10)&(yy>386)&(yy<740)
    arm_art=canvas_image(Image.fromarray(np.uint8(np.clip(arm_array,0,255))))
    arm_art.save(art/'arm.png')
    # Rigid upper/forearm artwork shares a rounded 25-native-pixel elbow overlap.
    # This preserves painted limb widths; broad soft skinning visibly compressed them.
    py,px=np.mgrid[:SIZE,:SIZE]
    elbow=xy(550,549)
    tangent=xy(492,630)-elbow;tangent/=np.linalg.norm(tangent)
    direction=(px-elbow[0])*tangent[0]+(py-elbow[1])*tangent[1]
    joint=((px-elbow[0])**2+(py-elbow[1])**2)<(25*SCALE)**2
    parts=[]
    for name,selection in [('upper_arm',(direction<=0)|joint),('forearm',(direction>=0)|joint)]:
        a=np.array(arm_art);a[:,:,3]*=selection
        part=Image.fromarray(a);part.save(art/f'{name}.png');parts.append(part)
    composite=arm_art.copy();composite.alpha_composite(body_art);composite.save(art/'neutral_composite.png')
    # Use only small feathered eye patches. Generated changes elsewhere never enter the rig.
    patch_report = {}
    for state in ['half','closed']:
        source,_ = clean_source(ROOT/'native'/f'blink_{state}.png')
        patch = Image.new('RGBA', neutral.size)
        mask = Image.new('L', neutral.size)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((581,188,676,279),fill=255)
        draw.ellipse((688,188,790,279),fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(6))
        # Skin/lash differences only. The mask is safely inside the rigid head region.
        patch = source.copy()
        patch.putalpha(ImageChops.multiply(source.getchannel('A'), mask))
        result=canvas_image(patch)
        result.save(art/f'eyes_{state}.png')
        patch_report[state]={'native_patch_bounds':[[581,188,676,279],[688,188,790,279]],'method':'two isolated eye ellipses, exact source coordinates, 6px feather, no face replacement'}
    specs=bone_specs()
    bones=[{'name':name,'parent':parent,'head':xy(*head).tolist(),'tail':xy(*tail).tolist()} for name,parent,head,tail in specs]
    body_mesh=make_mesh(body_art,specs)
    rig={'version':2,'size':SIZE,'bones':bones}
    upper_mesh=make_mesh(parts[0],specs,rigid='LeftUpper')
    fore_mesh=make_mesh(parts[1],specs,rigid='LeftFore')
    rig['meshes']=[dict(body_mesh,name='Body',texture='../art/body.png',z=0),dict(upper_mesh,name='UpperArm',texture='../art/upper_arm.png',z=-2),dict(fore_mesh,name='Forearm',texture='../art/forearm.png',z=-1)]
    save_json(ROOT/'godot/rig.json',rig)
    mesh_stats={m['name']:{'vertices':len(m['vertices']),'triangles':len(m['triangles'])} for m in rig['meshes']}
    save_json(ROOT/'evidence/art_preparation.json',{'scale':SCALE,'offset':OFFSET.tolist(),'cleanup':cleanup,'eye_patches':patch_report,'meshes':mesh_stats,'shoulder_cap':{'native_source':'native/shoulder_arm.png','uniform_scale':factor,'source_shoulder':[735,390],'target_shoulder':[589,436],'original_arm_kept_below_y':460,'static_transition':[440,460],'runtime_animated_crossfade':False},'source_hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'native').glob('*.png')}})
    preview=Image.new('RGBA',(SIZE*3,SIZE),(224,232,239,255))
    for i,state in enumerate(['open','half','closed']):
        im=composite.copy()
        if state!='open':im.alpha_composite(Image.open(art/f'eyes_{state}.png'))
        preview.alpha_composite(im,(i*SIZE,0))
    preview.convert('RGB').resize((1536,512),Image.Resampling.LANCZOS).save(ROOT/'evidence/art_board.jpg',quality=95)
    print(json.dumps({'meshes':mesh_stats,'source_alpha_bounds':base.getchannel('A').getbbox()}))


if __name__=='__main__':
    main()
