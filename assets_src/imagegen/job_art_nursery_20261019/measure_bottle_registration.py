"""Mask/registration diagnostics only; never paints or modifies source artwork."""
from pathlib import Path
from PIL import Image
import numpy as np,json
root=Path(__file__).resolve().parents[3];src=Path(__file__).resolve().parent
base=Image.open(root/'assets/opera/worlds/widgets/widget_pour_nursery_mover.png').getchannel('A')
target=np.asarray(base)>=16;box=base.point(lambda a:255 if a>=16 else 0).getbbox()
cx=(box[0]+box[2])/2;cy=(box[1]+box[3])/2
records=[]
for name in ['bottle_half','bottle_empty']:
    image=Image.open(src/(name+'_native.png')).getchannel('A')
    bounds=image.point(lambda a:255 if a>=16 else 0).getbbox();cut=image.crop(bounds)
    best={'iou':0}
    for factor in np.linspace(.97,1.02,26):
        scale=(box[3]-box[1])/cut.height*factor
        small=cut.resize((round(cut.width*scale),round(cut.height*scale)),Image.Resampling.LANCZOS)
        for dx in range(-3,4):
            for dy in range(-3,4):
                canvas=Image.new('L',(256,256));xy=(round(cx-small.width/2)+dx,round(cy-small.height/2)+dy)
                canvas.paste(small,xy);mask=np.asarray(canvas)>=16
                iou=float(np.logical_and(mask,target).sum()/np.logical_or(mask,target).sum())
                if iou>best['iou']:best={'iou':iou,'uniform_scale':scale,'native_crop':list(bounds),'placement':xy,'sampling':'Uniform alpha-mask sampling only, no delivered pixels produced'}
    records.append({'state':name,**best})
(src/'bottle_registration_diagnostic.json').write_text(json.dumps({'threshold':.98,'original_alpha16_bbox':box,'records':records},indent=2)+'\n')
print(json.dumps(records,indent=2))
