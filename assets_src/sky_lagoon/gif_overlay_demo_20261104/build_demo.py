"""Build the owner-commissioned Sky Lagoon overlay study from existing v5 pixels."""
from pathlib import Path
from hashlib import sha256
import json
import math
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[3]
PACKET = Path(__file__).resolve().parent
PROJECT = PACKET / 'demo_project'
SOURCE = ROOT / 'assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_v5_hd_3x1.png'
EXPECTED_SOURCE = '017532ae864e534d9b356472e2e29150855ede6583a7f63f02f0401d28c7be41'
FRAME_COUNT = 32
FPS = 8
# Coordinates stay in the original 6144x2048 master. Polygons are locally
# reviewed motion regions, with a 16px unchanged border and fixed root band.
SPECS = [
    dict(id='fir_crown', box=[0,0,384,512], amplitude=8, phase=0.0,
         polygon=[(112,16),(152,16),(187,100),(215,214),(285,292),(326,370),(368,430),(16,430),(16,220),(65,110)], kind='foliage'),
    dict(id='meadow_flowers', box=[1550,1580,1934,1964], amplitude=10, phase=0.25, protected_top=96,
         polygon=[(95,20),(256,20),(305,94),(361,171),(326,249),(44,252),(18,174),(20,80)], kind='foliage'),
    dict(id='lakeside_lupines', box=[5550,1420,5934,1804], amplitude=9, phase=0.5,
         polygon=[(70,20),(361,20),(363,246),(295,284),(70,281),(26,200),(35,122)], kind='foliage'),
    dict(id='lake_ripples', box=[4992,1088,5376,1472], amplitude=5, phase=0.75,
         polygon=[(16,16),(368,16),(368,368),(16,368)], kind='water'),
]

def digest(path):
    return sha256(path.read_bytes()).hexdigest()

def weight_for(spec, size):
    width,height=size
    mask=Image.new('L',size)
    ImageDraw.Draw(mask).polygon(spec['polygon'],fill=255)
    mask=mask.filter(ImageFilter.GaussianBlur(5))
    y,x=np.mgrid[:height,:width]
    edge=np.minimum.reduce([x,y,width-1-x,height-1-y])
    border=np.clip((edge-16)/24,0,1)
    weight=np.asarray(mask,dtype=np.float64)/255 * border
    if 'protected_top' in spec:
        weight*=np.clip((y-spec['protected_top'])/32,0,1)
    if spec['kind']=='foliage':
        # This base is an absolute fixed drawing band, not a translated card.
        root=0.76*height
        weight*=np.clip((root-y)/(0.6*height),0,1)
    return weight

def sample_frame(source, spec, weight, index):
    if index % FRAME_COUNT == 0:
        return source.copy()
    data=np.asarray(source)
    height,width=data.shape[:2]
    y,x=np.mgrid[:height,:width]
    phase=math.tau*index/FRAME_COUNT
    motion=math.sin(phase)
    if spec['kind']=='water':
        motion=math.sin(phase)*np.sin(y/15) + .25*math.sin(2*phase)*np.sin(y/8)
    displacement=spec['amplitude']*weight*motion
    source_x=np.clip(x-displacement,0,width-1)
    left=np.floor(source_x).astype(int)
    right=np.minimum(left+1,width-1)
    mix=(source_x-left)[...,None]
    pixels=np.rint(data[y,left]*(1-mix)+data[y,right]*mix).astype('uint8')
    return Image.fromarray(pixels)

def gif(path, images):
    # GIF has a centisecond clock. Alternating 120/130ms keeps 8fps exact.
    palette_board=Image.new('RGB',(images[0].width,images[0].height*len(images)))
    for index,image in enumerate(images):
        palette_board.paste(image.convert('RGB'),(0,index*image.height))
    palette=palette_board.quantize(colors=256,method=Image.Quantize.MEDIANCUT)
    indexed=[im.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE) for im in images]
    durations=[120 if i%2==0 else 130 for i in range(len(images))]
    indexed[0].save(path,save_all=True,append_images=indexed[1:],duration=durations,loop=0,optimize=True)
    with Image.open(path) as decoded:
        total=0
        for index in range(decoded.n_frames):
            decoded.seek(index)
            decoded.load()
            total+=decoded.info['duration']
        assert total==4000 and decoded.info['loop']==0
        return dict(frames=decoded.n_frames,duration_ms=total,bytes=path.stat().st_size,sha256=digest(path))

def main():
    assert digest(SOURCE)==EXPECTED_SOURCE
    master=Image.open(SOURCE).convert('RGB')
    PROJECT.mkdir(exist_ok=True)
    (PROJECT/'background').mkdir(exist_ok=True)
    source_files={str(SOURCE.relative_to(ROOT)).replace('\\','/'):EXPECTED_SOURCE}
    for row in range(2):
        for column in range(6):
            relative=f'assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v5_tile_r{row}_c{column}.png'
            path=ROOT/relative
            image=Image.open(path).convert('RGB')
            assert image.tobytes()==master.crop((column*1024,row*1024,(column+1)*1024,(row+1)*1024)).tobytes()
            # Native 1024 cards, no new palette or JPEG recompression.
            image.save(PROJECT/'background'/f'{row}_{column}.png')
            source_files[relative]=digest(path)
    manifest=dict(schema='reef.sky-lagoon-overlay-study.v1',status='REVIEW_CANDIDATE',
        source_files=source_files,frames=FRAME_COUNT,fps=FPS,period_seconds=4,
        method='Existing whole-patch raster deformation, explicitly ambient motion. Original crops remain the appearance authority. No generated art, no rejected object frames, no character animation, no crossfades.',
        palette='GIF previews use a single 256-color palette per loop. Godot uses lossless RGB PNG cells to preserve the exact source border and baseline.',
        job_budget=dict(generated_takes=0,paid_calls=0,wall_cap_minutes=40,cleanup_cap_minutes=15,attempts_per_object=2),
        items=[],tests={},acceptance_gaps=['Human full-speed visual/motion review','Target Lenovo M11/older Android timing and overdraw','Child and owner acceptance','Production integration'])
    poster=Image.new('RGB',(1536,550),'#173b49')
    for item_index,spec in enumerate(SPECS):
        folder=PROJECT/spec['id'];folder.mkdir(exist_ok=True)
        source=master.crop(spec['box'])
        source.save(PACKET/f"{spec['id']}_source.png")
        weight=weight_for(spec,source.size)
        Image.fromarray(np.rint(weight*255).astype('uint8')).save(PACKET/f"{spec['id']}_motion_weight.png")
        frames=[sample_frame(source,spec,weight,i) for i in range(FRAME_COUNT)]
        height,width=np.asarray(source).shape[:2]
        y,x=np.mgrid[:height,:width]
        edge=np.minimum.reduce([x,y,width-1-x,height-1-y])
        alpha=Image.fromarray(np.rint(np.clip((edge-2)/12,0,1)*255).astype('uint8'))
        frames=[im.convert('RGBA') for im in frames]
        for frame in frames:
            frame.putalpha(alpha)
        assert frames[0].convert('RGB').tobytes()==source.tobytes()
        assert sample_frame(source,spec,weight,FRAME_COUNT).tobytes()==source.tobytes()
        locked=weight==0
        original=np.asarray(source)
        for index,frame in enumerate(frames):
            assert np.array_equal(np.asarray(frame.convert('RGB'))[locked],original[locked])
            frame.save(folder/f'{index:02}.png')
        assert len({im.tobytes() for im in frames})>=16
        decoded_gif=gif(PACKET/f"{spec['id']}.gif",frames)
        entry=dict(spec,frame_size=source.size,gif=decoded_gif,source_crop_sha256=digest(PACKET/f"{spec['id']}_source.png"),
            frames_sha256=[digest(folder/f'{i:02}.png') for i in range(FRAME_COUNT)],
            locked_pixels=int(locked.sum()),all_locked_pixels_exact=True,base_rgba_mib=source.width*source.height*4*FRAME_COUNT/1048576)
        manifest['items'].append(entry)
        thumb=frames[8].copy();thumb.thumbnail((384,512));poster.paste(thumb,(item_index*384,0))
        ImageDraw.Draw(poster).text((item_index*384+8,520),spec['id'],fill='white')
    poster.save(PACKET/'objects_review.png')
    manifest['edge_treatment']='Transparent 14px guard within the unchanged 16px border. Every moving pixel remains fully opaque; fixed RGB paint is preserved under the guard.'
    manifest['tests'].update(source_master_hash='PASS',native_tiles_match_master='PASS',
        all_rest_frames_exact='PASS',locked_borders_and_bases='PASS',periodic_seams='PASS',gif_decode_and_clock='PASS')
    manifest['base_rgba_mib_without_sharing']=48+sum(item['base_rgba_mib'] for item in manifest['items'])
    manifest['base_rgba_mib']=48+sum(item['base_rgba_mib']*len(set(item['frames_sha256']))/FRAME_COUNT for item in manifest['items'])
    manifest['license']='Project-owned art from canonical ASSET_LICENSES.md. New derivatives retain source licensing and candidate status.'
    (PROJECT/'loops.json').write_text(json.dumps(manifest['items'],indent=2)+'\n',encoding='utf-8')
    (PACKET/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    # Aseprite is the editable bridge for the exact generated complete cels.
    lua=['local root = app.params["packet"]']
    for spec in SPECS:
        width=spec['box'][2]-spec['box'][0];height=spec['box'][3]-spec['box'][1]
        lua.extend([f'do local s=Sprite({width}, {height}, ColorMode.RGB)',
                    'local layer=s.layers[1]',f'layer.name="{spec["id"]}"',
                    'for i=0,31 do', 'if i>0 then s:newEmptyFrame() end',
                    f'local image=Image{{fromFile=root.."/demo_project/{spec["id"]}/"..string.format("%02d.png",i)}}',
                    's:newCel(layer,i+1,image,Point(0,0))', 's.frames[i+1].duration=0.125', 'end',
                    f's:saveAs(root.."/{spec["id"]}.aseprite")', 's:close() end'])
    (PACKET/'build_masters.lua').write_text('\n'.join(lua)+'\n',encoding='utf-8')
    print('OVERLAY_BUILD PASS',len(SPECS),'objects',FRAME_COUNT,'frames each;',manifest['base_rgba_mib'],'MiB base RGBA')

if __name__=='__main__':
    main()
