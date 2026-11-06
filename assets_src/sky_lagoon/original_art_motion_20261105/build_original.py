"""Original-v5-only rooted breeze. Complete context replacement, not added cutouts.
No generation, new object, broad colour-only material guess or camera movement.
"""
from pathlib import Path
import hashlib, json, math, time
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy.ndimage import map_coordinates, binary_dilation

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
SOURCE=ROOT/'assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_v5_hd_3x1.png'
EXPECTED='017532ae864e534d9b356472e2e29150855ede6583a7f63f02f0401d28c7be41'
N=60
DURATIONS=[30,30,40]*20
CONFIGS=[
 dict(id='lake_foxtails', label='Original lakeside purple flower spikes', xy=[5632,1344], amplitude=2.25, root=1782, top=1405,
      heads=[('purple',[(5830,1404),(5861,1450),(5876,1510),(5897,1580),(5900,1666),(5865,1713),(5798,1705),(5783,1640),(5800,1530),(5818,1460)]),
             ('purple',[(5740,1468),(5775,1515),(5792,1590),(5796,1695),(5754,1730),(5710,1703),(5699,1635),(5714,1550)])],
      stems=[([(5836,1630),(5824,1782)],11), ([(5754,1660),(5737,1764)],9)]),
 dict(id='meadow_spikes',label='Original meadow-border pink and yellow spikes',xy=[2400,900],amplitude=1.5,root=1305,top=978,
      heads=[('yellow',[(2558,980),(2583,1000),(2601,1070),(2600,1134),(2545,1146),(2535,1060)]),
             ('pink',[(2628,1020),(2651,1045),(2670,1110),(2662,1190),(2610,1197),(2600,1120)]),
             ('pink',[(2675,1085),(2697,1110),(2703,1185),(2694,1238),(2646,1234),(2640,1180)]),
             ('purple',[(2750,969),(2776,1000),(2791,1060),(2805,1135),(2780,1180),(2730,1180),(2716,1135),(2730,1050)])],
      stems=[([(2566,1100),(2560,1290)],7), ([(2633,1160),(2625,1305)],8), ([(2680,1200),(2657,1305)],7), ([(2756,1130),(2741,1255)],8)]),
 dict(id='arrival_bells',label='Original cream and pink arrival flowers',xy=[1520,1000],amplitude=2.0,root=1470,top=1135,
      heads=[('cream',[(1672,1143),(1693,1165),(1708,1220),(1714,1280),(1700,1335),(1660,1335),(1643,1293),(1646,1225)]),
             ('cream',[(1754,1128),(1775,1150),(1794,1210),(1807,1270),(1807,1348),(1775,1364),(1735,1344),(1721,1280),(1733,1210)]),
             ('pink',[(1883,1250),(1903,1272),(1925,1320),(1938,1404),(1914,1430),(1870,1420),(1850,1374),(1861,1310)])],
      stems=[([(1676,1280),(1665,1460)],9), ([(1769,1300),(1765,1470)],10), ([(1894,1370),(1884,1465)],8)])
]

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write_json(p,obj): Path(p).write_text(json.dumps(obj,indent=2)+'\n',encoding='utf-8')
def palette_gif(images,path):
    # One fixed palette prevents moving quantization noise in static scenery.
    sample=images[0].resize((512,512))
    palette=sample.quantize(colors=256,method=Image.Quantize.MEDIANCUT)
    frames=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in images]
    frames[0].save(path,save_all=True,append_images=frames[1:],duration=DURATIONS,loop=0,optimize=False,disposal=1)

def field_for(config,source):
    x,y=config['xy']; a=np.asarray(source,dtype=np.float32)
    r,g,b=a[:,:,0],a[:,:,1],a[:,:,2]
    channels={'purple':(b>g*1.13)&(r>g*.90),
              'pink':(r>g*1.18)&(r>b*1.04),
              'yellow':(r>g*.97)&(g>b*1.28)&(g>80),
              'cream':(r>g*.98)&(g>b*1.13)&(g>105)}
    selected=np.zeros((512,512),bool)
    for color,poly in config['heads']:
        mask=Image.new('L',(512,512)); ImageDraw.Draw(mask).polygon([(px-x,py-y) for px,py in poly],fill=255)
        selected|=(np.asarray(mask)>0)&channels[color]
    stem=Image.new('L',(512,512)); d=ImageDraw.Draw(stem)
    for line,width in config['stems']:
        d.line([(px-x,py-y) for px,py in line],fill=255,width=width)
    selected|=np.asarray(stem)>0
    # A bounded surrounding collar transports the existing contour continuously.
    # This is NOT a foreground alpha matte or a physically separated depth layer.
    collar=binary_dilation(selected,iterations=4)
    influence=np.asarray(Image.fromarray((collar*255).astype('uint8')).filter(ImageFilter.GaussianBlur(2.2)),dtype=np.float32)/255
    yy,xx=np.indices((512,512),dtype=np.float32)
    ramp=np.clip((config['root']-(yy+y))/(config['root']-config['top']),0,1)**1.65
    border=np.minimum.reduce([xx,yy,511-xx,511-yy])
    influence*=ramp*np.clip(border/12,0,1)
    influence[influence<1/255]=0
    # Quantize before both CPU render and shader sampling: same authored field.
    return np.rint(influence*255).astype('uint8'), selected

def frame(source,field,config,index):
    phase=index*2*math.pi/N
    dx=config['amplitude']*(math.sin(phase)+.16*math.sin(2*phase))/1.16
    a=np.asarray(source,dtype=np.float32)
    yy,xx=np.indices(a.shape[:2],dtype=np.float32)
    sx=xx-dx*field.astype(np.float32)/255
    out=np.stack([map_coordinates(a[:,:,c],[yy,sx],order=1,mode='nearest',prefilter=False) for c in range(3)],axis=-1)
    return Image.fromarray(np.rint(out).astype('uint8'))

def build():
    started=time.monotonic()
    assert sha(SOURCE)==EXPECTED,'Original source changed'
    original=Image.open(SOURCE).convert('RGB'); base=original.convert('RGBA')
    configs=[]; all_frames={}; survey=original.resize((1800,600))
    ds=ImageDraw.Draw(survey)
    for folder in ['sources','fields','jobs','evidence','demo_project/background','demo_project/patches','frames']:
        (HERE/folder).mkdir(parents=True,exist_ok=True)
    metrics=[]
    for config in CONFIGS:
        name=config['id']; x,y=config['xy']; box=(x,y,x+512,y+512)
        source=original.crop(box)
        source.save(HERE/f'sources/{name}.png')
        source.save(HERE/f'demo_project/patches/{name}.png')
        field,selected=field_for(config,source)
        Image.fromarray(field).save(HERE/f'fields/{name}.png')
        Image.fromarray(field).save(HERE/f'demo_project/patches/{name}_field.png')
        Image.fromarray((selected*255).astype('uint8')).save(HERE/f'evidence/{name}_selection.png')
        overlay=np.asarray(source).copy(); t=field.astype(float)/255*.7
        overlay[:,:,0]=np.rint(overlay[:,:,0]*(1-t)+255*t).astype('uint8')
        overlay[:,:,1]=np.rint(overlay[:,:,1]*(1-t)).astype('uint8')
        overlay[:,:,2]=np.rint(overlay[:,:,2]*(1-t)).astype('uint8')
        Image.fromarray(overlay).save(HERE/f'evidence/{name}_field_review.png')
        images=[frame(source,field,config,i) for i in range(N)]
        all_frames[name]=images
        framepath=HERE/f'frames/{name}'; framepath.mkdir(exist_ok=True)
        for i,im in enumerate(images): im.save(framepath/f'{i:03d}.png')
        palette_gif(images,HERE/f'{name}.gif')
        base.paste((0,0,0,0),(x+1,y+1,x+511,y+511)) #1px sampling underlap, contains no moving feature
        ds.rectangle((x*1800/6144,y*600/2048,(x+512)*1800/6144,(y+512)*600/2048),outline='#ffdf85',width=2)
        ds.text((x*1800/6144,y*600/2048-13),name,fill='#fff2b0')
        raw=np.asarray(source)
        maximum=0; changed=0
        for im in images:
            delta=np.any(np.asarray(im)!=raw,axis=2)
            assert not delta[field==0].any(),'Fixed scenery changed'
            root_y=max(0,min(512,config['root']-y))
            assert not delta[root_y:].any(),'Root band moved'
            maximum=max(maximum,int(np.abs(np.asarray(im).astype(int)-raw.astype(int)).max()))
            changed=max(changed,int(delta.sum()))
        assert np.array_equal(np.asarray(images[0]),raw)
        assert np.array_equal(np.asarray(frame(source,field,config,N)),raw),'Loop endpoint mismatch'
        with Image.open(HERE/f'{name}.gif') as gif:
            durations=[]
            for i in range(gif.n_frames): gif.seek(i); durations.append(gif.info.get('duration'))
            assert gif.n_frames==N and sum(durations)==2000,(name,gif.n_frames,durations)
        actual_max=max(abs(config['amplitude']*(math.sin(i*2*math.pi/N)+.16*math.sin(2*i*2*math.pi/N))/1.16) for i in range(N))*field.max()/255
        metrics.append(dict(id=name,source_box=list(box),frames=N,duration_ms=sum(durations),encoded_delays_ms=sorted(set(durations)),average_fps=30,
          unique_decoded_source_frames=len({hashlib.sha256(np.asarray(im).tobytes()).hexdigest() for im in images}),
          max_horizontal_native_px=float(actual_max),vertical_px=0,rotation_degrees=0,scale_change=0,field_nonzero_pixels=int((field>0).sum()),
          fixed_pixels_per_patch=int((field==0).sum()),max_changed_pixels=changed,max_rgb_change=maximum,rest_exact=True,root_band_exact=True,loop_endpoint_exact=True))
        configs.append({k:v for k,v in config.items() if k not in ['heads','stems']})
        job=dict(identity=name,revision=1,author='Codex',date='2026-11-05',source_commit='6dfd04aef441f30e0374e9ae9049cff845ce4ebd',
          output_lane='REFERENCE_ONLY / standalone Canvas study',intention='Existing painted flower spikes respond quietly to a passing breeze.',
          required_action='Small horizontal bend above rooted support; no vertical translation, rigid rotation, scale pulse or relighting.',
          fixed='Camera, all scenery outside the bounded contour collar, lower stem/root support and non-target flowers.',
          entry_exit='Source pose at phase0 and analytic phase2pi;60 samples exclude duplicated endpoint.',
          source=dict(path=SOURCE.relative_to(ROOT).as_posix(),sha256=EXPECTED,size=list(original.size),acceptance_scope='Existing approved v5 identity/composition only; animation unaccepted'),
          reuse_gap='No missing appearance art. Complete original context replacement window; no new decorative asset.',
          method='Hand-bounded per-flower hue selections plus authored stem paths; rooted grayscale displacement field; original-image bilinear resampling. Nearby contour collar participates. Not a true depth split or isolated foreground alpha matte.',
          settings=config,frames=N,fps=30,duration_seconds=2,limits=dict(local_attempts=2,wall_hours=8,cleanup_minutes=120,paid_budget_usd=0,generated_calls=0),
          provenance=dict(source_crop=f'sources/{name}.png',field=f'fields/{name}.png',aseprite=f'{name}.aseprite',frame_mapping='frame i = analytic phase2pi*i/60, no retiming or repeated padding',
             background_edit='Erase the window interior from a derivative base, leaving a1px sampling underlap at its boundary; replace once at original integer position. Original source untouched.'),
          review=dict(machine='See evidence/machine-verification.json and Mobile evidence',human='PENDING normal-speed and frame-step',device='PENDING',child_owner='PENDING'),
          status=dict(archive_complete='PENDING_REMOTE_VERIFICATION',generation_ready='NOT_APPLICABLE_LOCAL',delivery_accepted=False,runtime_integrated=False))
        write_json(HERE/f'jobs/{name}.json',job)
    # Every delivered pixel has one visible owner; a1px window-border underlap supports filtering.
    reconstructed=base.copy()
    for config in CONFIGS: reconstructed.paste(original.crop((*config['xy'],config['xy'][0]+512,config['xy'][1]+512)),tuple(config['xy']))
    assert np.array_equal(np.asarray(reconstructed),np.asarray(original.convert('RGBA')))
    for row in range(2):
        for col in range(6):
            base.crop((col*1024,row*1024,(col+1)*1024,(row+1)*1024)).save(HERE/f'demo_project/background/{row}_{col}.png')
    reconstructed.resize((1800,600)).save(HERE/'original-rest.png')
    survey.save(HERE/'original-target-map.png')
    write_json(HERE/'demo_project/targets.json',configs)
    # Fixed overview and full-resolution contextual close-up, no zoom/pan.
    overview=[]; board=[]
    for i in range(N):
        scene=base.copy()
        for config in CONFIGS: scene.paste(all_frames[config['id']][i],tuple(config['xy']))
        overview.append(scene.convert('RGB').resize((1800,600),Image.Resampling.LANCZOS))
        panel=Image.new('RGB',(1536,550),'#152c31'); draw=ImageDraw.Draw(panel)
        for j,config in enumerate(CONFIGS):
            panel.paste(all_frames[config['id']][i],(j*512,38))
            draw.text((j*512+12,12),config['label'],fill='#f1e6cb')
        board.append(panel)
    # Full-board palette sampled from all panels, rather than first-panel crop.
    palette=board[0].quantize(colors=256,method=Image.Quantize.MEDIANCUT)
    quant=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in board]
    quant[0].save(HERE/'original-flowers-closeup.gif',save_all=True,append_images=quant[1:],duration=DURATIONS,loop=0,disposal=1,optimize=False)
    palette_gif(overview,HERE/'original-lagoon-fixed.gif')
    sheet=Image.new('RGB',(1536,1536))
    for row,index in enumerate([0,15,45]):
        for col,config in enumerate(CONFIGS): sheet.paste(all_frames[config['id']][index],(col*512,row*512))
    sheet.save(HERE/'evidence/frame-step.png')
    write_json(HERE/'evidence/machine-verification.json',dict(source_sha256=sha(SOURCE),source_unchanged=True,rest_reconstruction_exact=True,
      no_new_items=True,source_inputs=[SOURCE.relative_to(ROOT).as_posix()],pixels_have_unique_visible_owner=True,window_edge_underlap_px=1,targets=metrics,
      texture_bytes_without_mipmaps=12*1024*1024*4+3*512*512*4+3*512*512,
      background_native_size=[6144,2048],runtime_texture_sizes=[[1024,1024],[512,512]],new_3d_nodes=0,generated_calls=0,
      build_seconds=round(time.monotonic()-started,3),limits='Contiguous contour collar is resampled; exact foreground isolation/depth separation is not claimed. Machine checks do not establish human/device acceptance.'))
    print(json.dumps(metrics,indent=2))

if __name__=='__main__': build()
