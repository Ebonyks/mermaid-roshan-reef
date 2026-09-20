from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json
W=Path.cwd();B=W/'assets_src/sky_lagoon/animated_rebuild_v1_2026-09-20';out=B/'whole_scene_revision/color_audit';out.mkdir(exist_ok=True)
source=W/'assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_v5_hd_3x1.png';im=Image.open(source).convert('RGB');rgb=np.asarray(im)/255.;hsv=np.asarray(im.convert('HSV'))/255.
patches=[('arrival','rear_shrubs',[1400,1160,1700,1320]),('arrival','foreground_leaves',[1300,1750,1700,1960]),('arrival','lawn',[760,1730,1060,1900]),('meadow','rear_shrubs',[2200,1180,2600,1280]),('meadow','foreground_leaves',[2050,1750,2290,1990]),('meadow','lawn',[2700,1770,3000,1940]),('castle','rear_shrubs',[4300,1050,4550,1230]),('castle','foreground_leaves',[4540,1730,4830,1940]),('meadow','right_approach_foliage',[3930,1480,4050,1560])]
def metrics(a,h):
 linear=np.where(a<=.04045,a/12.92,((a+.055)/1.055)**2.4);lum=linear@np.array([.2126,.7152,.0722]);return {'pixels':len(a),'median_HSV_saturation':round(float(np.median(h[:,1])),4),'median_linear_luminance':round(float(np.median(lum)),4),'luminance_p10_p90':[round(float(x),4) for x in np.percentile(lum,[10,90])],'median_hue_degrees':round(float(np.median(h[:,0])*360),1)}
rows=[];board=im.resize((1536,512));draw=ImageDraw.Draw(board)
for stage,role,box in patches:
 x0,y0,x1,y1=box;a=rgb[y0:y1,x0:x1];h=hsv[y0:y1,x0:x1];m=(h[:,:,0]>.16)&(h[:,:,0]<.52)&(h[:,:,1]>.2)&(h[:,:,2]>.12);stat=metrics(a[m],h[m]);rows.append({'stage':stage,'role':role,'rect':box,'mask':'green/cyan-green foliage range; excludes other hues, not semantic segmentation',**stat});draw.rectangle(tuple(v//4 for v in box),outline='magenta',width=2);draw.text((x0//4,y0//4-11),stage[:1]+':'+role,fill='white')
board.save(out/'sample-map.jpg',quality=94)
manifest=json.loads((W/'assets/sprites/sky_lagoon/whole_scene_v2/manifest.json').read_text());temporal=[]
cards=list(manifest['cards'])
cards.append({'id':'huckleberry_leaf_grade','family':'plant','file':'huckleberry_leaf_grade.png','columns':4,'rows':2,'frames':8})
cards.append({'id':'bellflower_whole_breeze','family':'plant','file':'bellflower_whole_breeze.png','columns':4,'rows':2,'frames':8})
for water in json.loads((B/'whole_scene_revision/water_surface/PACKING.json').read_text(encoding='utf-8'))['cards']:
 cards.append({'id':'water_surface_'+water['id'],'family':'water','file':'water_surface_'+water['id']+'.png','columns':water['columns'],'rows':water['rows'],'frames':water['frames']})
for row in cards:
 atlas=Image.open(W/'assets/sprites/sky_lagoon/whole_scene_v2'/row['file']).convert('RGBA');cw=atlas.width//row['columns'];ch=atlas.height//row['rows'];stats=[]
 for k in range(row['frames']):
  cel=atlas.crop((k%row['columns']*cw,k//row['columns']*ch,(k%row['columns']+1)*cw,(k//row['columns']+1)*ch));a=np.asarray(cel);valid=a[:,:,3]>240
  if valid.any():stats.append(metrics(a[:,:,:3][valid]/255.,np.asarray(cel.convert('HSV'))[valid]/255.))
 temporal.append({'id':row['id'],'family':row['family'],'frames':row['frames'],'saturation_median_range':round(max(x['median_HSV_saturation'] for x in stats)-min(x['median_HSV_saturation'] for x in stats),4),'luminance_median_range':round(max(x['median_linear_luminance'] for x in stats)-min(x['median_linear_luminance'] for x in stats),4)})
report={'status':'ONGOING_COLOR_AUDIT_NOT_ACCEPTANCE','source':str(source.relative_to(W)).replace('\\','/'),'scope':'All three stages: source foliage comparisons and all 26 whole-scene cards. Additional runtime materials/actors, old animated overlays and night rendering require separate review. No global histogram used as quality verdict.','samples':rows,'whole_scene_temporal_cards':temporal,'findings':[{'id':'COLOR-01','finding':'Foreground large leaves and rear shrubbery have different hue/value structure; use material-matched sampling and in-context review before saturation adjustment. Larger darker leaf masses naturally differ from tiny sunlit leaves; do not flatten useful depth.'},{'id':'COLOR-02','finding':'Night backdrop/new bellflower/huckleberry use (0.48,0.56,0.82), while older ambient family multiplies by (0.72,0.78,0.96). These paths can yield inconsistent perceived intensity. Inspect compounded node tint before correction.'},{'id':'COLOR-03','finding':'Cyan extraction fringes falsely increase edge saturation; twelve cleaned cloud candidates address a separate matte issue, not a scene-wide grade.'}],'required_passes':['Day and night rendered comparisons of sky/cloud/mountain/hedge/lawn/foreground/water/castle/playground/actor hierarchy','All old animated overlay frame palettes plus whole-scene card frame palettes','Local correction variants per material with before/after gameplay review','No protected character recoloring or blanket desaturation; preserve depth and warm interaction accents'],'machine_validation':'Three source stages and 26 whole-scene cards measured; color acceptance not established'}
# Preserve authored review/evidence fields while regenerating measured fields.
previous=json.loads((out/'COLOR_AUDIT.json').read_text(encoding='utf-8')) if (out/'COLOR_AUDIT.json').exists() else {}
for key in ('findings','night_correction','overlay_audit','coverage','limitations','foreground_rosette','meadow_berry_fan','bellflower_palette','prop_night_grade','huckleberry_palette','ambient_motion_v3'):
 if key in previous:report[key]=previous[key]
report['scope']='All three stages: nine mapped source foliage regions, 28 whole-scene cards, two water-surface atlases and graded bellflower and huckleberry atlases shared by four plants. Source statistics are diagnostics; runtime material hierarchy and owner/device acceptance remain incomplete.'
report['machine_validation']='Nine source samples and 32 current source entries measured, including 24 water cels and sixteen graded plant cels including rooted bellflower leaf motion; no visual acceptance claim.'
(out/'COLOR_AUDIT.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(rows,indent=2));print('TEMPORAL_MAX',max(temporal,key=lambda x:x['saturation_median_range']))
