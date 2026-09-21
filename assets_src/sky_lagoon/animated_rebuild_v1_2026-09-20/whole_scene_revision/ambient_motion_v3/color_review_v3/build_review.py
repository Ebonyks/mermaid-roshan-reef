from pathlib import Path
import json, hashlib, html
import numpy as np
from PIL import Image, ImageDraw
OUT=Path(__file__).resolve().parent
ROOT=next(p for p in OUT.parents if (p/'project.godot').exists())
PREVIOUS=json.loads((OUT.parent/'color_review_v2/AUDIT.json').read_text())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def stats(im):
 a=np.asarray(im.convert('RGBA')); mask=a[:,:,3]>=250
 if not mask.any():mask=a[:,:,3]>=32
 if not mask.any():return None
 rgb=a[:,:,:3][mask].astype(float)/255
 lin=np.where(rgb<=.04045,rgb/12.92,((rgb+.055)/1.055)**2.4)
 lum=lin@np.array([.2126,.7152,.0722]); mx=rgb.max(1);mn=rgb.min(1)
 sat=np.divide(mx-mn,mx,out=np.zeros_like(mx),where=mx>0)
 return {'sample_pixels':int(mask.sum()),'alpha_coverage':float(a[:,:,3].sum()/255), 'linear_luminance_p10_p50_p90':np.percentile(lum,[10,50,90]).round(6).tolist(),'saturation_median':round(float(np.median(sat)),6),'rgb_median':np.median(rgb,axis=0).round(5).tolist()}
images={};sources=[];board=Image.new('RGB',(1280,1140),'#1b303a')
for i,stage in enumerate(['arrival','meadow','castle']):
 for j,mode in enumerate(['day','night']):
  p=OUT/f'{stage}_{mode}.png'; im=Image.open(p).convert('RGB');assert im.size==(1280,720)
  images[stage,mode]=im;sources.append({'path':p.relative_to(ROOT).as_posix(),'sha256':digest(p),'dimensions':list(im.size),'role':'unaltered current-scene baseline; temporary study cards hidden'})
  board.paste(im.resize((640,360)),(j*640,i*380));ImageDraw.Draw(board).text((j*640+8,i*380+363),stage+' / '+mode+' / 07dde8dd source',fill='white')
board.save(OUT/'day-night-board.jpg',quality=94)
samples=[]
for row in PREVIOUS['samples']:
 samples.append({k:row[k] for k in ['stage','material','sample_id','rect_xyxy']}|{m:stats(images[row['stage'],m].crop(row['rect_xyxy'])) for m in ['day','night']})
# Same capture locations as the prior mapped review; statistics do not imply same-species correspondence.
selected=['rear_hedge','large_foreground_leaf','pale_foreground_clump','lawn','bellflower_leaf','tree_canopy','water','castle_wall','roof','window']
crops=[r for r in samples if r['material'] in selected]
cb=Image.new('RGB',(1000,len(crops)*108),'#1b303a');dr=ImageDraw.Draw(cb)
for i,r in enumerate(crops):
 y=i*108;dr.text((8,y+5),r['stage']+' / '+r['material'],fill='white')
 for j,m in enumerate(['day','night']):
  crop=images[r['stage'],m].crop(r['rect_xyxy']);crop.thumbnail((150,72));cb.paste(crop.resize((150,72)),(300+j*340,y+5))
  st=r[m];dr.text((460+j*340,y+10),f"{m}\nL {st['linear_luminance_p10_p50_p90'][1]:.3f}\nS {st['saturation_median']:.3f}",fill='white')
cb.save(OUT/'material-comparison.jpg',quality=95)
base=ROOT/'assets/sprites/sky_lagoon/whole_scene_v2'
man=json.loads((base/'manifest.json').read_text());specs=[]
for r in man['cards']:specs.append((r['id'],base/r['file'],r['columns'],r['rows'],r['frames'],r['family']))
def add(name,rel,c,r,n,f):specs.append((name,ROOT/rel,c,r,n,f))
for n in ['arrival','castle']:add('water_surface_'+n,f'assets/sprites/sky_lagoon/whole_scene_v2/water_surface_{n}.png',4,4,12,'water')
for name,file,c,r,n,fam in [('huckleberry','huckleberry_restyled_breeze.png',4,2,8,'plant'),('bellflower','bellflower_whole_breeze.png',4,2,8,'plant')]:add(name,'assets/sprites/sky_lagoon/whole_scene_v2/'+file,c,r,n,fam)
for name,c,r,n,fam in [('conifer_breeze',3,2,6,'tree'),('bridge_contact',4,3,12,'bridge'),('bridge_chains',4,3,12,'bridge')]:add(name,'assets/sprites/sky_lagoon/animated_v1/'+name+'.png',c,r,n,fam)
add('water_tap_ripple','assets/sprites/fx_water/fx_water_ripple_ring_atlas.png',4,2,8,'effect')
for animal in ['otter','frog','hare','squirrel','raccoon']:
 for action in ['idle','startle']:add(animal+'_'+action,f'assets/sprites/sky_lagoon/animals/{animal}_{action}_atlas.png',2,2,4,'animal')
results=[];cells_by_id={}
for ident,p,c,r,n,fam in specs:
 im=Image.open(p).convert('RGBA');assert im.width%c==0 and im.height%r==0
 cw,ch=im.width//c,im.height//r;cells=[];ss=[]
 for k in range(n):
  cell=im.crop(((k%c)*cw,(k//c)*ch,(k%c+1)*cw,(k//c+1)*ch));cells.append(cell);ss.append({'frame':k,'stats':stats(cell),'visible_sha256':hashlib.sha256(np.where(np.asarray(cell)[:,:,3:4]>0,np.asarray(cell),0).tobytes()).hexdigest()})
 good=[s for s in ss if s['stats']]
 l=[s['stats']['linear_luminance_p10_p50_p90'][1] for s in good];sat=[s['stats']['saturation_median'] for s in good];cov=[s['stats']['alpha_coverage'] for s in good]
 # Ranking is diagnostic only; pose silhouette/alpha changes can explain a large range.
 results.append({'id':ident,'family':fam,'path':p.relative_to(ROOT).as_posix(),'sha256':digest(p),'grid':[c,r],'played_frames':n,'unique_visible_cells':len(set(s['visible_sha256'] for s in ss)),'luminance_median_range':round(max(l)-min(l),6),'saturation_median_range':round(max(sat)-min(sat),6),'alpha_coverage_relative_range':round((max(cov)-min(cov))/max(cov),6),'minimum_luminance_frame':good[int(np.argmin(l))]['frame'],'maximum_luminance_frame':good[int(np.argmax(l))]['frame'],'frames':ss})
 cells_by_id[ident]=cells
ranked=sorted(results,key=lambda r:r['luminance_median_range'],reverse=True)
tb=Image.new('RGB',(1200,12*182),'#203640');td=ImageDraw.Draw(tb)
for i,r in enumerate(ranked[:12]):
 y=i*182;td.text((8,y+5),f"{r['id']} / {r['played_frames']} played / L range {r['luminance_median_range']:.4f} / S range {r['saturation_median_range']:.4f}",fill='white')
 for j,k in enumerate([r['minimum_luminance_frame'],r['maximum_luminance_frame']]):
  cel=cells_by_id[r['id']][k].copy();bbox=cel.getbbox()
  if bbox:cel=cel.crop(bbox)
  cel.thumbnail((530,140));tile=Image.new('RGBA',(550,140),'#667c84');tile.alpha_composite(cel,((550-cel.width)//2,(140-cel.height)//2));tb.paste(tile.convert('RGB'),(j*590+8,y+26));td.text((j*590+8,y+165),f'cell {k} (independently fitted for inspection)',fill='white')
tb.save(OUT/'temporal-extremes.jpg',quality=94)
findings=PREVIOUS['findings']
findings[0]['decision']='The 07dde8dd preview replaces two pale berry owners with eight-cel pointed/dappled plants. Other foliage families remain separate review targets; this does not establish foreground/background acceptance.'
findings[7]['action']='Retain original cyan glass identity; test independent night material brightness without changing walls, warm trim or the protected portrait.'
findings[7]['decision']='A separate ten-window alpha-mask trial has pixel-exact rollback in two GPU views. Selected for opt-in integration, not integrated at this checkpoint.'
report={'status':'COLOR_AUDIT_OPEN_NOT_ACCEPTED','checkpoint':'07dde8dd521ec566c2346bcf7259fe694ae0cde0','owner_score':3.5,'new_score':None,'scope':{'scene_material_locations':len(samples),'rendered_views':6,'source_atlases':len(results),'played_cell_slots':sum(r['played_frames'] for r in results)},'method':'Current baseline Mobile renders; unmasked scene rectangles, source cels with alpha>=250 (fallback >=32 for translucent effects), linear Rec709 luminance and HSV saturation. Source-cell distributions are not tracked material correspondences or runtime flicker verdicts. Different foliage species, shadow coverage, night tint and poses preclude equal-intensity targets. No universal pass threshold or automatic recoloring.','sources':sources,'samples':samples,'temporal_atlases':results,'diagnostic_priority_order':[r['id'] for r in ranked],'findings':findings,'next_corrections':['Unify offending leaf highlight width, shadow hue and paint texture by plant family, preserving darker foreground depth.','Recheck night leaf detail against nearby hedge; do not brighten every environmental layer.','Integrate selected whole-tuft grass trial only after matching adjoining lawn, stable roots and clear routes.','Test cyan castle glass independently from opaque wall tint; preserve portrait and gold identity.','Review high-cloud generated poses for shadow/palette variation in context before recoloring or redrawing.','Keep rejected low-cloud seam trial out of runtime; clouds must pass complete-scene compositing as well as atlas checks.'],'visual_review_notes':['Agent inspected the six-view day/night board and twelve temporal-extreme pairs. This is not owner acceptance.','Tap ripple changes from a compact blue ring to a broad fading pale ring; its large source-color range is consistent with the authored effect, not sufficient evidence of color flicker.','Frog, squirrel, hare and raccoon poses expose different proportions of pale underside and darker fur/skin. Do not normalize their whole-cel average colors.','Frog startle cell 2 shows a detached-looking toe fragment; record as a separate contour/anatomy review need, not a palette correction.','Grass extreme pairs confirm that several existing regions are bright detached marks rather than connected tufts; color consistency alone cannot repair this motion-design weakness.'], 'limits':['No runtime color or asset changed by this review.','Six frozen views do not cover full camera pan, every animal/event, cloud drift or device presentation.','Temporal source metrics cannot establish night composite or motion acceptance.','Animation shape, stiffness, sparse lawn coverage and missing low-cloud-sea movement remain separate open defects.','Protected actor/portrait colors are not environmental grading targets.']}
(OUT/'AUDIT.json').write_text(json.dumps(report,indent=2)+'\n')
esc=html.escape
cards=''.join('<article><b>'+esc(f['priority']+' / '+f['family'])+'</b><p>'+esc(f['finding'])+'</p><p>'+esc(f['action'])+'</p><small>'+esc(f['decision'])+'</small></article>' for f in findings)
trs=''.join(f"<tr><td>{esc(r['id'])}</td><td>{r['played_frames']}</td><td>{r['unique_visible_cells']}</td><td>{r['luminance_median_range']:.4f}</td><td>{r['saturation_median_range']:.4f}</td></tr>" for r in ranked)
(OUT/'index.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Sky Lagoon color audit</title><style>body{max-width:1280px;margin:24px auto;padding:0 18px;background:#172b35;color:#e9f2f5;font:16px/1.55 system-ui}img{max-width:100%}article{padding:16px;background:#24414d;margin:12px 0}small{color:#c0d1d8}a{color:#95dbed}table{width:100%;border-collapse:collapse}td,th{text-align:left;padding:7px;border-bottom:1px solid #48616b}</style><h1>Sky Lagoon: color remains an open finding</h1><p>Source checkpoint 07dde8dd. Latest owner rating: 3.5/5. No new rating or visual acceptance claimed.</p><p>Six current Mobile views, 48 material locations, '''+str(len(results))+''' source atlases and '''+str(sum(r['played_frames'] for r in results))+''' played cell slots. Scene crops include mixed materials; temporal metrics rank inspection needs, not defects.</p><img src="day-night-board.jpg" alt="All three stages in daylight and at night"><h2>Material decisions</h2>'''+cards+'''<details><summary>View matched-location day/night material crops</summary><img src="material-comparison.jpg" alt="Material crops with luminance and saturation diagnostics"></details><h2>Animation color variation</h2><p>Different poses expose different paint and transparent coverage. Large ranges require visual review; small ranges do not prove good animation. Cells below are independently fitted to make their paint inspectable.</p><img src="temporal-extremes.jpg" alt="Lowest and highest median-luminance cels for the twelve largest diagnostic ranges"><table><tr><th>Atlas</th><th>Played slots</th><th>Unique visible</th><th>L range</th><th>S range</th></tr>'''+trs+'''</table><p><a href="AUDIT.json">Source hashes, every cel measurement, findings and remaining evidence</a></p><p>No runtime recoloring in this audit. Device, full-pan, contact-state and owner acceptance remain open.</p></html>''',encoding='utf-8')
print(json.dumps({'scope':report['scope'],'largest_diagnostic_ranges':[{k:r[k] for k in ['id','luminance_median_range','saturation_median_range']} for r in ranked[:8]]},indent=2))
