"""Read exact tracked blobs; inspect images without pixel writes. Not a whole-game census."""
from pathlib import Path
import json,hashlib,subprocess,re,datetime
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[3];OLD='d26512b120500492be8e2694ac552a187f0091ca';DEV='831d0bbb155b99d75ef0289cc5cc694e0ef00c1e'
def git(*args):return subprocess.check_output(['git',*args],cwd=R,stderr=subprocess.PIPE)
def sha(b):return hashlib.sha256(b).hexdigest()
def raw(path):return git('show',OLD+':'+path)
def save(name,d):(P/name).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
tracked=git('ls-tree','-r','--name-only',OLD,'assets','assets_src','scripts','scenes','shaders','project.godot').decode().splitlines()
image_paths=[f for f in tracked if Path(f).suffix.lower() in ['.png','.jpg','.jpeg','.webp','.svg'] and re.search(r'geode|geology|geologist|crystal',f,re.I)]
images=[]
for f in image_paths:
 b=raw(f);x={'path':f,'revision':OLD,'bytes':len(b),'sha256':sha(b),'selection':'Relevant filename/path match only; unlabelled artwork elsewhere remains unreviewed'}
 if Path(f).suffix!='.svg':
  import io
  with Image.open(io.BytesIO(b)) as im:
   x.update(dimensions=list(im.size),mode=im.mode,alpha_extrema=list(im.getchannel('A').getextrema()) if 'A' in im.getbands() else None)
 images.append(x)
text_paths=[f for f in tracked if f.startswith(('scripts/','scenes/')) and Path(f).suffix in ['.gd','.tscn','.tres']] + ['project.godot']
terms=['geode_texture','GEODE_PATH','CRYSTALS_PATH','goal_geologist.svg','geode-extraction-attempt01','geode-open-alpha-attempt02','geology_props_candidate.png','geology_props_alpha_retry.png']
refs=[];used=set()
for f in text_paths:
 lines=raw(f).decode('utf-8').splitlines();function=None
 for i,line in enumerate(lines):
  if line.startswith('func '):function=line.split('(')[0].split()[1]
  hits=[t for t in terms if t in line]
  if hits:refs.append({'path':f,'line':i+1,'function':function,'terms':hits,'text':line});used.add(f)
context={'scripts/opera_geology_surface.gd':[(33,54),(247,257),(797,834),(913,940)],'scripts/opera_career_world_2d.gd':[(349,354),(448,464),(1232,1258),(1946,1970),(2578,2595),(4971,4992)],'scripts/opera_hotspot_catalog.gd':[(130,138),(190,197)],'scripts/opera_world_hotspot_2d.gd':[(100,120),(201,225),(234,270),(286,316)],'scripts/chapter_two_career_scene_adapter.gd':[]}
source_files=[];excerpts=[]
for f,spans in context.items():
 b=raw(f);source_files.append({'path':f,'revision':OLD,'sha256':sha(b),'bytes':len(b)});lines=b.decode('utf-8').splitlines()
 for a,z in spans:excerpts.append({'path':f,'revision':OLD,'start_line':a,'end_line':z,'lines':lines[a-1:z]})
geo=raw('scripts/opera_geology_surface.gd').decode();occ=[x for x in refs if 'geode_texture' in x['terms']];assert len(occ)==2;assert [x['function'] for x in occ]==[None,'_load_textures'];draw=geo.split('func _draw_geode()')[1].split('\nfunc ')[0];assert 'geode_texture' not in draw
manifest_paths=['assets_src/geologist_rebuild_2026-09-05/generation_manifest.json','assets_src/minigame_art_quality_2026-09-05/geode-extraction-attempt01/manifest.json','assets_src/minigame_art_quality_2026-09-05/geode-open-alpha-attempt02/manifest.json','assets_src/minigame_art_quality_2026-09-05/geode-open-attempt01/manifest.json']
provenance=[]
for f in manifest_paths:
 b=raw(f);provenance.append({'path':f,'revision':OLD,'bytes':len(b),'sha256':sha(b),'record':json.loads(b)})
rejects=[x for x in images if x['path'].endswith(('geology_props_candidate.png','geology_props_alpha_retry.png'))];assert len(rejects)==2 and all(x['mode']=='RGB' and x['alpha_extrema'] is None for x in rejects)
closed='assets_src/flat_vector_geode_reuse_20261013/geode_closed_1024.png';opened='assets_src/flat_vector_geode_open_reuse_20261013/geode_open_1024.png';cavity='assets_src/flat_vector_geode_layered_20261013/geode_cavity.png'
import io
with Image.open(io.BytesIO(raw(opened))) as im:
 crop=im.crop((260,240,480,800));box=crop.getchannel('A').getbbox();top=list(crop.getchannel('A').crop((0,0,220,1)).getextrema());bottom=list(crop.getchannel('A').crop((0,559,220,560)).getextrema())
 with Image.open(io.BytesIO(raw(cavity))) as ci:assert ci.tobytes()==crop.tobytes()
measure={'source_rect':[260,240,220,560],'decoded_crop_matches_R12':True,'alpha_bbox_in_rect':list(box),'top_row_alpha_extrema':top,'bottom_row_alpha_extrema':bottom,'interpretation':'Rectangle includes hard cut across painted material at top/bottom; positive edge alpha does not reconstruct a painted cap or inner-wall contour. Matte adjustment alone does not supply missing topology/action frames.'}
consumers=[{'role':'Opened geode cavity','path':'scripts/opera_geology_surface.gd','binding_lines':[47,253],'consumer_lines':[805,808],'missing_art_fallback_lines':[809,810,927,940],'condition':'geode_pull>0; crystals_texture nonnull; source-proved potential consumer, prior original state context R8; not newly executed in R13'}, {'role':'Scene goal prop','path':'scripts/opera_career_world_2d.gd','binding_lines':[448,463],'consumer_lines':[1242,1255],'condition':'scene_adapter prop empty -> GOAL_PROPS geologist; exists load; explicit adapter may override. Visibility/route/state closure unreviewed.'},{'role':'GEODE invitation loaded resource binding','path':'scripts/opera_hotspot_catalog.gd','binding_lines':[137,196],'consumer_path':'scripts/opera_career_world_2d.gd','consumer_lines':[1946,1970],'loader_path':'scripts/opera_world_hotspot_2d.gd','loader_lines':[100,109],'presentation':'painted','texture_drawn_in_current_presentation':False,'draw_guard_lines':[220,224],'painted_cue_lines':[234,270],'overlay_texture_lines':[305,307],'overlay_missing_art_fallback_lines':[309,315],'condition':'Current armed station and !task_open and active; catalogue path loaded by configure_object. With current painted presentation _draw calls _draw_painted_landmark and skips _draw_object,so this loaded SVG is not a visible texture consumer. Current procedural cue remains artwork debt; alternate overlay/null-resource variants unreviewed.'}]
data={'schema':'reef.geode_source_closure/1','revision':'FV-AUDIT-20261013-R13','source_revision':OLD,'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':{'relevant_image_filename_matches':len(images),'production_text_files_searched':len(text_paths),'production_text_paths':text_paths,'terms':terms,'search_complete_for_declared_terms_only':True,'all_assets_visual_inventory_complete':False,'runtime_caller_closure_complete':False,'unknown_reason':'Unlabelled sources/dynamic overrides,other routes/states,resource failures and export/runtime save variants remain unreviewed.'},'image_inventory':images,'source_files':source_files,'references':refs,'source_excerpts':excerpts,'provenance':provenance,'rejected_checkerboard_sheets':rejects,'unused_binding':{'path':'scripts/opera_geology_surface.gd','GEODE_PATH':'','geode_texture_occurrences':occ,'draw_consumer_count':0,'setting_only_GEODE_PATH_repairs_shell':False,'reason':'_draw_geode always builds coloured left/right polygons; geode_texture is never read by draw code.'},'crystal_resource_consumers':consumers,'cavity_crop_measurement':measure,'functional_geometry':{'seam_hit_radius':56,'pull_threshold':120,'interaction_rect':[550,165,440,350],'disposition':'Invisible hit geometry remains behavioral contract; visible polygons/markers/board are artwork and not exempted by this source audit.'},'whole_unit_disposition':{'authority':'design/animation/ANIMATION_PRODUCTION_PROTOCOL.md','decision':'ODR-SPRITE-WHOLE-UNIT-20261007','R12':'Nonruntime component study only; not eligible as final whole drawing in one layer. Flattening or baking the same separately moved pieces alone cannot establish the owner-required whole drawing/action/topology.','known_source_states':['Whole closed candidate','Whole static separated-pair candidate; different visible perspective and topology'],'known_source_native_intermediate_states':0,'complete_approved_action_family_found':False,'scope_limit':'Bounded named-source search; absence is not proof no suitable art exists anywhere. No generated intermediate/frame batch or budget is authorized by this audit.','permitted_next_step':'Audit unnamed relevant sources and/or author one complete source-bound whole-frame intermediate candidate with coherent cap/inner-wall/contact at actual drag state under local workflow. Preserve originals and compare complete neighbors; do not reintegrate R12 parts. Method/art/runtime/device/child/owner lanes remain open.'},'new_pixels':0,'new_native_captures':0,'new_generation_calls':0,'accepted_removed':0}
save('SOURCE_AUDIT.json',data)
prod=[f for f in tracked if f.startswith(('scripts/','scenes/','assets/','shaders/')) or f=='project.godot'];tree_rows=git('ls-tree','-r','-l',OLD,'--','assets','scripts','scenes','shaders','project.godot').decode().splitlines();rows=[{'path':line.split('\t',1)[1],'git_blob_id':line.split()[2],'bytes':int(line.split()[3])} for line in tree_rows];difference=git('diff','--name-only',OLD,DEV,'--','scripts','scenes','assets','shaders','project.godot').decode().splitlines();assert not difference
save('ORIGIN_DEV_RECONCILIATION.json',{'source_revision':OLD,'origin_dev':DEV,'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'production_git_blob_census_count':len(rows),'production_git_object_census_sha256':sha(json.dumps(rows,sort_keys=True,separators=(',',':')).encode()),'production_diff_paths':difference,'scope':'All tracked source-revision production Git object IDs and byte lengths in assets/scripts/scenes/shaders/project.godot; exact Git diff against origin/dev. Relevant appearance/code sources separately SHA-256 bound. No merge or integration.'})
print('SOURCE AUDIT',len(images),'images',len(text_paths),'text files',len(refs),'references',len(rows),'production blobs',measure)
