from pathlib import Path
from PIL import Image
import numpy as np,sys,importlib.util,hashlib
root=Path.cwd();sys.path.insert(0,str(root/'tools'));import ltx_wave_experiment as runner
folder=root/'assets_src/animation/roshan_wave_repair_20261010/aseprite_matte_trial_01';preferred=folder/'variant_04'
spec=importlib.util.spec_from_file_location('measure_wave',root/'docs/handoffs/codex_roshan_wave_whole_sprites_2026-10-07/tools/measure_wave.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
rows=[]
for n in [14,26,40]:
 original=folder/'sources'/f'{n:04d}.png';source=root/'assets_src/animation/roshan_wave_repair_20261010/native640_01/take_01/native_frames'/f'{n:04d}.png';p=preferred/'native_rgba'/f'{n:04d}.png';base=preferred/'baseline_native_rgba'/f'{n:04d}.png'
 a=np.array(Image.open(original).convert('RGB'));b=np.array(Image.open(base).convert('RGBA'));o=np.array(Image.open(p).convert('RGBA'))
 removed=b[:,:,3]==0;near=np.zeros(removed.shape,dtype=bool)
 for dy in range(-2,3):
  for dx in range(-2,3):
   ya,yb=max(0,-dy),min(a.shape[0],a.shape[0]-dy);xa,xb=max(0,-dx),min(a.shape[1],a.shape[1]-dx)
   near[ya:yb,xa:xb]|=removed[ya+dy:yb+dy,xa+dx:xb+dx]
 retained=b[:,:,3]>0;deep=retained&~near
 altered=(o[:,:,:3]!=a).any(2)|(o[:,:,3]!=255)
 eligible=(a.max(2)-a.min(2)<=10)&(a.min(2)>=205);protected=retained&eligible
 rows.append({'frame_index':n,'source_path':runner.relative(root,source),'source_sha256':runner.sha(source),'preserved_source_copy_sha256':runner.sha(original),'source_copy_byte_exact':runner.sha(source)==runner.sha(original),'native_rgba_path':runner.relative(root,p),'native_rgba_sha256':runner.sha(p),'sprite_rgba_path':runner.relative(root,preferred/'sprite_rgba'/f'{n:04d}.png'),'sprite_rgba_sha256':runner.sha(preferred/'sprite_rgba'/f'{n:04d}.png'),'native_dimensions':list(Image.open(p).size),'sprite_dimensions':list(Image.open(preferred/'sprite_rgba'/f'{n:04d}.png').size),'unmodified_deep_figure_pixels':int(deep.sum()),'modified_pixels_beyond2px_boundary':int((deep&altered).sum()),'protected_closed_neutral_pixels':int(protected.sum()),'modified_protected_closed_neutral_pixels':int((protected&altered).sum()),'model_observation':'Matte improved and source26 arm/hand remains defective' if n==26 else 'Matte improved; native source line noise/focus still requires separate whole-frame review'})
masters=[{'path':runner.relative(root,p),'sha256':runner.sha(p),'layers':m.aseprite_layers(str(p))} for p in [preferred/'matte_trial.aseprite',preferred/'native_matte_trial.aseprite']]
runner.write_json(folder/'review.json',{'schema':'reef.aseprite-boundary-alpha-model-review.v1','reviewer_kind':'model_observation','reviewer':'Codex whole_frame_interpolation subagent','reviewed_at_utc':runner.utc(),'preferred_variant':'variant_04','status':'PREFERRED_MATTE_CANDIDATE_NOT_FINAL_ARTWORK','scope':'Three source-only whole-cel RGBA isolation/unmatting samples, reviewed native and256px over true black/light/dark fields','generator_calls':0,'paid_calls':0,'cleanup_minutes':'Not continuously metered; bounded local trial performed within renewed180-minute campaign cleanup cap; root must account aggregate session time','pixel_edits':'AsepriteLua only; direct same-frame boundary color/alpha fitting with declared foreground seeds. No Python image writes.','samples':rows,'master_layer_counts':masters,'manual_background_seeds':{'14':[459,226],'26':[454,218],'40':[457,219]},'remaining_blocks':['Native source26 hand/forearm is visibly smeared/incompletely drawn','Native generated contour noise/focus variation remain source limitations','Complete41-frame transitions,seam,W2/W3 geometry not established by a matte trial','Human/owner/device/child/runtime/delivery acceptance absent'],'acceptance':{'artifact_free_wave':False,'owner':False,'device':False,'child':False,'runtime':False,'delivery_accepted':False}})
files=[]
for p in sorted(folder.rglob('*')):
 if not p.is_file() or p.name=='manifest.json':continue
 e={'path':p.relative_to(folder).as_posix(),'sha256':runner.sha(p),'bytes':p.stat().st_size,'role':'workflow_or_derivation_record','used_as_delivery_pixels':False,'provenance':'Local derivative of native640_01/take_01 candidate generated from approved identity source; sources remain unaccepted','modification':'AsepriteRGBA boundary cleanup variant; details in README/script/review'}
 if p.suffix=='.png':
  with Image.open(p) as im:e.update(dimensions=list(im.size),mode=im.mode)
  if '/sources/' in '/'+e['path']:e.update(role='native_source_copy',modification='Byte-exact preserved nativeRGB copy')
  elif '/native_rgba/' in '/'+e['path']:e.update(role='native_rgba_matte_candidate')
  elif '/sprite_rgba/' in '/'+e['path']:e.update(role='whole_frame_uniformly_reduced_rgba_matte_candidate')
  else:e.update(role='review_only_preview_or_baseline')
 if p.suffix=='.aseprite':e.update(role='single_layer_whole_cel_editable_master')
 files.append(e)
payload=''.join(e['path']+'\t'+e['sha256']+'\n' for e in files).encode('utf-8')
runner.write_json(folder/'manifest.json',{'schema':'reef.aseprite-matte-pilot-packet.v1','status':'LOCAL_SOURCE_STUDY_UNACCEPTED','created_at_utc':runner.utc(),'files':files,'packet_payload_rule':'Sorted relative POSIX path + TAB + sha256 + LF for every file except manifest.json; SHA256 of UTF8 payload','packet_payload_sha256':hashlib.sha256(payload).hexdigest(),'acceptance':{'artifact_free_wave':False,'owner':False,'device':False,'child':False,'runtime':False,'delivery_accepted':False,'github_publication':'PENDING_ROOT_PROJECT_PACKET'}})
print({'samples':rows,'masters':masters,'file_count':len(files),'payload_sha256':hashlib.sha256(payload).hexdigest()})
