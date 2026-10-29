"""Technical whole-picture uniform registration/downsize/padding only; no paint or alpha cleanup."""
from pathlib import Path
import json,hashlib,importlib.util
import numpy as np
from PIL import Image,ImageDraw
r=Path.cwd();s=r/'assets_src/imagegen/job_art_support_careers_20261019';out=r/'assets/opera/worlds/support_quality_20261019';out.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
registration={x['source']:x for x in json.loads((s/'registration02.json').read_text())['records']}
cuffs={x['source']:x for x in json.loads((s/'cuff_registration03.json').read_text())['records']}
spec=importlib.util.spec_from_file_location('measure',r/'docs/handoffs/codex_job_art_imagegen_2026-10-17/tools/measure_job_art.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
records=[]
def save(im,name,src,details):
 p=out/(name+'.png');assert not p.exists(),p
 im.save(p);records.append({'path':p.relative_to(r).as_posix(),'sha256':sha(p),'dimensions':list(im.size),'source':src.relative_to(r).as_posix(),'source_sha256':sha(src),'source_dimensions':list(Image.open(src).size),'technical_derivation':details,'cutout':m.cutout_profile(p.read_bytes()),'acceptance':'CANDIDATE_PENDING_ACTUAL_SOURCE_CONTEXT_4.5_AND_APPLICABLE_MOTION_DEVICE_OWNER'})
def family(mapping,base,side=512,kind='fixed'):
 data={}
 for name,source in mapping:
  im=Image.open(s/(source+'_native.png')).convert('RGBA');assert im.width==im.height
  reg=(cuffs if kind=='hands' else registration).get(source,{}) if source!=base else {}
  scale=reg.get('uniform_scale',1.0);tx,ty=reg.get('translation_at_512',[0,0]);data[source]=(scale,tx,ty)
 x0=min(tx for scale,tx,ty in data.values());y0=min(ty for scale,tx,ty in data.values());x1=max(tx+512*scale for scale,tx,ty in data.values());y1=max(ty+512*scale for scale,tx,ty in data.values());fit=.88*side/max(x1-x0,y1-y0);ox=(side-(x1-x0)*fit)/2-x0*fit;oy=(side-(y1-y0)*fit)/2-y0*fit
 for name,source in mapping:
  src=s/(source+'_native.png');im=Image.open(src).convert('RGBA');scale,tx,ty=data[source];factor=scale*512/im.width*fit;sz=(round(im.width*factor),round(im.height*factor));pos=(round(ox+tx*fit),round(oy+ty*fit));canvas=Image.new('RGBA',(side,side));assert pos[0]>=0 and pos[1]>=0 and pos[0]+sz[0]<=side and pos[1]+sz[1]<=side,(name,pos,sz)
  canvas.alpha_composite(im.resize(sz,Image.Resampling.LANCZOS),pos);save(canvas,name,src,{'method':'Whole native canvas uniformly downsampled and translated on common padded family canvas; original RGB/alpha retained through lossless export, no painting/masking/part warp/cropping.','family_reference':base,'source_uniform_scale':scale,'source_translation_at_512':[tx,ty],'family_uniform_fit':fit,'family_origin':[ox,oy],'output_whole_size':list(sz),'output_origin':list(pos),'registration_record':'cuff_registration03.json' if kind=='hands' else 'registration02.json','limits':'Feature/cuff alignment diagnostic, not acting/contact/identity acceptance.'})
def fit(name,source,canvas=(512,512),padding=.08,project_source=False):
 src=r/source if project_source else s/(source+'_native.png');im=Image.open(src).convert('RGBA');box=im.getchannel('A').getbbox();assert box;crop=im.crop(box);scale=min(canvas[0]*(1-2*padding)/crop.width,canvas[1]*(1-2*padding)/crop.height);assert scale<=1.00001;sz=(round(crop.width*scale),round(crop.height*scale));pos=((canvas[0]-sz[0])//2,(canvas[1]-sz[1])//2);dest=Image.new('RGBA',canvas);dest.alpha_composite(crop.resize(sz,Image.Resampling.LANCZOS),pos);save(dest,name,src,{'method':'Technical transparent-border crop at full alpha>0 bbox, uniform downsample, transparent padding only. No source pixel painted/removed; no nonuniform scale.','crop':list(box),'uniform_scale':scale,'output_size':list(sz),'output_origin':list(pos)})
family([('widget_cast_doctor_0','doctor_patient_base'),('widget_cast_doctor_1','doctor_cast_1_retry'),('widget_cast_doctor_2','doctor_cast_2_retry'),('widget_cast_doctor_3','doctor_cast_3'),('widget_bandage_doctor_0','doctor_patient_base'),('widget_bandage_doctor_1','doctor_bandage_1'),('widget_bandage_doctor_2','doctor_bandage_2'),('widget_bandage_doctor_3','doctor_bandage_3')],'doctor_patient_base')
family([('widget_basin_doctor_'+state,'doctor_basin_'+state) for state in ['off','running','foamy']],'doctor_basin_off')
family([('widget_hands_doctor_'+str(i),source) for i,source in enumerate(['doctor_hands_ready_retry','doctor_hands_wet','doctor_hands_rub_palms','doctor_hands_rub_backs'])],'doctor_hands_ready_retry',kind='hands')
family([('widget_xray_scanner_idle','doctor_scanner_idle'),('widget_xray_scanner_found','doctor_scanner_found_retry')],'doctor_scanner_idle',256)
family([('widget_target_farmer_mover_'+state,'farmer_pig_'+state) for state in ['catch','chew','happy']],'farmer_pig_catch')
family([('widget_barn_gate_'+state,'farmer_barn_gate_'+state) for state in ['closed','open']],'farmer_barn_gate_closed')
family([('widget_portal_magician_ring_'+str(i),'magician_portal_'+state) for i,state in enumerate(['closed','quarter','half','open'])],'magician_portal_closed')
fit('widget_portal_magician_overlay','magician_portal_glint',(512,512),.12)
fit('widget_seed_bed','farmer_seed_bed_retry',(1024,512),.04)
fit('widget_soil_hole','farmer_soil_hole',(128,128),.06)
fit('widget_sprout_seed','assets/opera/worlds/widgets/widget_drag_farmer_mover.png',(128,128),.06,True)
fit('widget_sprout_sprout','farmer_sprout',(128,128),.06)
for i in range(5):fit('widget_sprout_flower_'+str(i),'farmer_flower_'+str(i),(128,128),.06)
for i in range(6):fit('widget_paint_cloud_'+str(i),'painter_cloud_'+str(i),(256,256),.04)
assert len(records)==42
(s/'runtime_provenance01.json').write_text(json.dumps({'model_revision':'unexposed availablebuiltin approved byowner','records':records,'limits':'No actual context/motion/device/owner acceptance from technical derivation.'},indent=2)+'\n')
rejects={'doctor_scanner_found':'Opaque found lens hides patient; retry selected.','doctor_hands_ready':'Adult long-finger anatomy/nails does not match child hand style; retry selected.','farmer_seed_bed':'Soil plane too shallow for fixed five holes; high-camera retry selected.','doctor_cast_1':'Partial cast too broad/too similar to final; retry selected.','doctor_cast_2':'Partial cast too broad/too similar to final; retry selected.'}
p=s/'prompts.json';d=json.loads(p.read_text());used={x['source'] for x in records}
for x in d:x['disposition']='REJECTED: '+rejects[x['id']] if x['id'] in rejects else ('SELECTED_SOURCE_CANDIDATE_PENDING_RUNTIME_CONTEXT_MOTION' if x['native_path'] in used else 'RETAINED_NOT_SELECTED')
p.write_text(json.dumps(d,indent=2)+'\n')
review=s/'review';review.mkdir(exist_ok=True);pages=[]
for page in range((len(records)+7)//8):
 sheet=Image.new('RGB',(1280,860),'#34556d');draw=ImageDraw.Draw(sheet)
 for j,x in enumerate(records[page*8:page*8+8]):
  im=Image.open(r/x['path']).convert('RGBA');im.thumbnail((290,340));cx=(j%4)*320;cy=(j//4)*430;sheet.paste(im,(cx+(320-im.width)//2,cy+40+(340-im.height)//2),im);draw.text((cx+8,cy+8),Path(x['path']).stem,fill='white')
 p=review/f'objects_runtime01_{page}.png';sheet.save(p);pages.append(p.relative_to(r).as_posix())
(s/'technical01.json').write_text(json.dumps({'runtime_pictures':len(records),'decoded_RGBA_bytes':sum(x['dimensions'][0]*x['dimensions'][1]*4 for x in records),'profile_failures':[{'path':x['path'],'cutout':x['cutout']} for x in records if x['cutout']['verdict']!='CUTOUT_OK'],'review_pages':pages,'limits':'Inventory and alpha check only; no actual VRAM/FPS/motion/context acceptance.'},indent=2)+'\n')
p=r/'ASSET_LICENSES.md';t=p.read_text('utf-8')
for x in records:
 assert '| `'+x['path']+'` |' not in t
 t+='\n| `'+x['path']+'` | '+x['source']+'; nativeSHA256 '+x['source_sha256']+' | Project original/reference rights and OpenAI output terms retained | https://openai.com/policies/terms-of-use/ | Uniform technical derivation only, details runtime_provenance01.json; finalSHA256 '+x['sha256']+'. No formal/device/owner acceptance. |'
for n in pages:
 t+='\n| `'+n+'` | Technical labeled contact sheet of hash-bound candidate cutouts | Project/source rights retained | https://openai.com/policies/terms-of-use/ | Diagnostic only, no delivery pixels or acceptance. SHA256 '+sha(r/n)+'. |'
p.write_text(t+'\n',encoding='utf-8')
p=r/'design/audit_impacts/job-art-support-careers-20261019.json';d=json.loads(p.read_text());d['files']=sorted(set(d['files']+['ASSET_LICENSES.md']+[x['path'] for x in records]+[x.relative_to(r).as_posix() for x in s.rglob('*') if x.is_file()]));p.write_text(json.dumps(d,indent=2)+'\n')
print('Prepared42wholePNG technical candidates; profile failures',[(x['path'],x['cutout']['verdict']) for x in records if x['cutout']['verdict']!='CUTOUT_OK'],flush=True)
