"""Reproducible material diagnostics from actual six-screen Mobile captures."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'whole_scene_revision/color_audit/six_screen'
PATCHES={
'arrival':{'sky':[340,40,440,90],'cloud_sea':[280,355,350,400],'mountain':[560,295,585,315],'rear_hedge':[510,395,560,435],'large_foreground_leaf':[575,615,620,655],'pale_foreground_clump':[50,668,90,705],'lawn':[240,585,315,620],'path':[225,505,275,540],'water':[35,450,90,475],'slide':[877,380,900,410],'bellflower_leaf':[358,650,389,675]},
'meadow':{'sky':[450,40,550,90],'cloud_sea':[205,350,260,375],'mountain':[1000,230,1040,255],'rear_hedge':[830,352,880,390],'large_foreground_leaf':[1100,610,1140,650],'pale_foreground_clump':[655,672,700,704],'lawn':[465,507,520,540],'path':[770,570,830,592],'slide':[441,380,465,410],'swing':[640,329,695,336]},
'castle':{'sky':[530,25,650,75],'mountain':[870,160,910,190],'rear_hedge':[590,300,650,350],'large_foreground_leaf':[640,625,680,660],'pale_foreground_clump':[245,677,285,705],'path':[945,635,975,655],'water':[1035,525,1070,545],'castle_wall':[790,390,810,435],'bridge_deck':[825,499,850,514],'swing':[195,332,260,339]}}
def measure(im,box):
 c=im.crop(box);rgb=np.asarray(c,dtype=float)/255
 lin=np.where(rgb<=.04045,rgb/12.92,((rgb+.055)/1.055)**2.4)
 l=lin@np.array([.2126,.7152,.0722]);hsv=np.asarray(c.convert('HSV'),dtype=float)/255
 return {'luminance_median':round(float(np.median(l)),5),'luminance_p10_p90':np.percentile(l,[10,90]).round(5).tolist(),'HSV_saturation_median':round(float(np.median(hsv[:,:,1])),5)}
board=Image.new('RGB',(1280,1140),'#202830');marked=Image.new('RGB',(1280,2160));bd=ImageDraw.Draw(board)
rows=[];sources=[]
for idx,(stage,patches) in enumerate(PATCHES.items()):
 ims={}
 for col,mode in enumerate(['day','night']):
  f=OUT/f'{stage}_{mode}.png';im=Image.open(f).convert('RGB');assert im.size==(1280,720);ims[mode]=im
  sources.append({'path':f.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'dimensions':list(im.size)})
  board.paste(im.resize((640,360)),(col*640,idx*380));bd.text((col*640+8,idx*380+363),stage+' / '+mode,fill='white')
 annotated=ims['day'].copy();draw=ImageDraw.Draw(annotated)
 for n,(material,box) in enumerate(patches.items(),1):
  day=measure(ims['day'],box);night=measure(ims['night'],box)
  rows.append({'stage':stage,'sample_id':n,'material':material,'rect_xyxy':box,'day':day,'night':night,'night_day_luminance_ratio':round(night['luminance_median']/max(day['luminance_median'],1e-8),4)})
  draw.rectangle(box,outline='#ff4050',width=2);draw.text((box[0],box[1]-12),str(n)+' '+material,fill='#ff4050',stroke_width=1,stroke_fill='white')
 marked.paste(annotated,(0,idx*720))
board.save(OUT/'day-night-board.jpg',quality=94);marked.save(OUT/'sample-map.jpg',quality=94)
findings=[
 {'priority':'P1','material':'Foreground rounded clumps versus hedge','finding':'Repeated pale, broad-leaf foreground clumps read as a different material family from dark detailed hedges across all three views. Brightness, hue and painted texture contribute; saturation alone cannot fix this.','action':'Trial one existing clump with selective highlight compression and hue alignment against neighboring approved foliage; preserve leaf boundaries and purple berries. Expand only after contextual review.'},
 {'priority':'P1','material':'Arrival foliage versus meadow/castle','finding':'Earlier nine-region source audit reports arrival foliage saturation around .93 versus .66-.68 elsewhere. These are selected regions, not whole-stage averages.','action':'Compare same-species foliage on both sides of screen boundaries, then derive bounded color adjustments. Preserve cooler distance colors and front/back value separation.'},
 {'priority':'P1','material':'Grass and new fan','finding':'New seven-blade fan retains connected whole leaves but appears softer than surrounding foreground paint. Four-pose GPU trial passes mechanically; appearance remains rejected for integration. Sparse existing animated grass remains insufficient.','action':'Match contour sharpness, highlight width and base shadow to adjacent grass before palette approval. Audit every cel and root transition.'},
 {'priority':'P2','material':'Castle/bridge/playground night','finding':'Opt-in ambient tint now darkens opaque props. Windows and metallic glints still lack independent emissive treatment.','action':'Separate glow accents from ambient surfaces; retain child-readable bridge and entry contrast. Do not restore day-bright opaque surfaces.'},
 {'priority':'P2','material':'Sky/clouds/mountains','finding':'Depth colors remain readable; cloud family differs in roundness and local contrast. Three-pose candidate passes temporary atlas restoration but has not replaced production cloud.','action':'Audit all clouds against mountain silhouettes and cloud sea through full drift and pose loops. Preserve distant low contrast.'},
 {'priority':'P2','material':'Flowers/berries/rosette/bellflower','finding':'Targeted leaf grades preserve accent colors. Repetitive pale clusters and stationary bellflower leaves remain unresolved.','action':'Compare like materials across every animation cel; keep cream, pink and purple accents varied rather than globally desaturating.'},
 {'priority':'P2','material':'Water/rocks/path','finding':'Path remains distinguishable in day/night views. Water and shore stones share landscape darkening; bright tap ripple needs temporal review.','action':'Check shore masks, ripple peak/fade, bridge contact and left castle approach. Keep these surfaces stable while foliage is corrected.'},
 {'priority':'OPEN','material':'Actor/animals/HUD/touch states','finding':'Actor remains visually bright at night, supporting visibility; acceptability has not been established. Dynamic actors and HUD are excluded from fixed environment patch metrics.','action':'Matched interaction captures and device readability review; preserve protected source colors.'}]
report={'status':'COLOR_AUDIT_FINDINGS_OPEN_NOT_ACCEPTED','scope':'All three environment screens in day and night; 31 mapped material patches. This is coverage of visible material families, not every pixel, every cel, every interaction or a quality score.','method':'Unmasked rectangular samples: sRGB decoded to linear luminance; HSV saturation is a diagnostic only. Painted shade and mixed pixels remain. Sampling locations are visible in sample-map.jpg. Night/day frames share static camera geometry, but dynamic poses are not synchronized; these ratios are not grading targets.','sources':sources,'samples':rows,'findings':findings,'rollback':'Audit only; original artwork untouched. Existing preview corrections remain opt-in.','acceptance_gaps':['Matched per-cel palette stability','All camera seams and drift extremes','Actor, animals and interaction-state color hierarchy','Target-device readability/performance','Owner acceptance; latest owner score remains 3.5/5.']}
(OUT/'AUDIT.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
for stage in PATCHES:
 rr={r['material']:r for r in rows if r['stage']==stage}
 print(stage,'pale/rear day luminance',round(rr['pale_foreground_clump']['day']['luminance_median']/rr['rear_hedge']['day']['luminance_median'],2))
print(len(rows),'samples')
