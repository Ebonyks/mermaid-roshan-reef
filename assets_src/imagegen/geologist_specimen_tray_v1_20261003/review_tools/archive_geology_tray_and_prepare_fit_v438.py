from pathlib import Path
import datetime,hashlib,json,shutil,subprocess
from PIL import Image
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
F=R/'assets_src/imagegen/geologist_specimen_tray_v1_20261003'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
origin=Path('C:/Users/Peter/.codex/generated_images/01a0f309-110a-7602-af22-f30d657bd017/exec-d79df1c6-b2e6-47e5-8204-e50c0da8ee3d.png')
a=F/'attempt01';a.mkdir(exist_ok=False);shutil.copyfile(origin,a/'native.png')
with Image.open(a/'native.png') as im:
 assert im.mode=='RGBA';dims=list(im.size);alpha=im.getchannel('A');bounds=alpha.getbbox();extrema=alpha.getextrema()
 assert extrema==(0,255) and bounds and all(alpha.getpixel(p)==0 for p in [(0,0),(im.width-1,0),(0,im.height-1),(im.width-1,im.height-1)])
write(a/'GENERATION.json',{'method':'OpenAI built-in ImageGen','intent':'Fresh text-only empty painted specimen tray','generated_utc':'2026-10-03T01:43:00Z','generation_time_qualification':'Approximate wall-clock call time; source preservation time below is exact.','preserved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'default_source_path':str(origin),'original_sha256':sha(origin),'native_path':(a/'native.png').relative_to(R).as_posix(),'native_sha256':sha(a/'native.png'),'native_dimensions':dims,'mode':'RGBA','alpha_extrema':extrema,'alpha_used_rect':bounds,'prompt_path':(F/'PROMPT.txt').relative_to(R).as_posix(),'prompt_sha256':sha(F/'PROMPT.txt'),'references':[],'references_uploaded':False,'native_modifications':'None, exact copy.','runtime_binding':False,'owner_acceptance':None})
opinions=[
 {'id':'TRAY-S01','item':'Complete empty tray source','score':4.6,'evaluation':'One coherent shallow hollow tray with continuous rounded cream/plum rim, visible aqua floor, lavender front face and modest grounded shadow. Broad painted grain and value bands match the existing geology mineral/fossil material family. Native silhouette is complete and isolated; a source opinion, not a room or action pass.'},
 {'id':'TRAY-S02','item':'Hollow interior and continuous rim','score':4.6,'evaluation':'Back wall, inside floor, rounded corner joins and low front wall form one readable container. No false second tray, handles, specimens, lid or floating ornament.'},
 {'id':'TRAY-S03','item':'Painted material and style','score':4.6,'evaluation':'Aqua/lavender/cream planes show soft hand-painted texture and restrained light; plum outer contour is broad enough for the playset. No glossy photoreal or mesh lighting.'},
 {'id':'TRAY-S04','item':'Full silhouette and alpha','score':4.5,'evaluation':'Native RGBA contains real transparent margins and a soft contact shadow. Fine blue/purple edge pixels remain visible at the far contour at native size; small mounted scale still requires direct review. The inclusive4.5 priority rule is retained.'},
 {'id':'TRAY-S05','item':'Resting perspective and proportions','score':4.6,'evaluation':'Slightly elevated three-quarter view clearly exposes the floor; about twice-wide body and low front rim read as a shallow specimen container. Complete base/shadow communicates support without a painted tabletop.'},
 {'id':'TRAY-S06','item':'110pixel mounted readability','score':None,'evaluation':'Await direct native in-context rendering; a native source score cannot establish small-scale cavity/rim clarity or room clearance.'}]
write(a/'DIRECT_SOURCE_REVIEW.json',{'status':'NATIVE_DIRECTLY_REVIEWED_PROVISIONAL_SOURCE4_6_MOUNT_PENDING','reviewed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'native_sha256':sha(a/'native.png'),'review_method':'Direct complete native generated image inspection, with read-only alpha/dimension measurements; no source resizing, painting, recolouring or synthesis.','opinions':opinions,'runtime_binding':False,'current_trays_score':2.9,'owner_acceptance':None})
# A separate ignored-by-Godot counterfactual layout study only. No production source injection claim.
P=R/'audit/job_geology_painted_invitation_fit_v1_20261003';assert not P.exists()
prior=read(R/'design/audit_impacts/job-geode-current-recheck-20261002.json')
ip=R/'design/audit_impacts/job-geology-painted-invitation-fit-20261003.json'
write(ip,{'id':'job-geology-painted-invitation-fit-20261003','baseline':prior['baseline'] if False else '1652a9bb33af0d11a594b5996df66d2266c02d39','scope':'Non-runtime counterfactual fit study only: replace the existing flat fossil rectangle, three tray drawings and polygon crystal/ring in an isolated actual Library/elevator fixture backdrop with intact reused painted fossil/mineral/slab and one new text-only painted tray. Preserve source art, correct individual alpha-region aspect ratios, sole pixel ownership and working panel hide/stage rules. Explicitly mark backdrop substitution; no current-production score transfer. Review every selected native image at both aspects for props, duplicates and actor overlap before any production change. Preserve current room2.8/contact2.7 and all acceptance gaps.','rules':prior['rules'],'findings':prior['findings'],'files':[(P/x).relative_to(R).as_posix() for x in ['.gdignore','PLAN.json','painted_prop_backdrop.gd','capture.gd','SOURCE_CURRENT_BEFORE_CAPTURE.json','review_tools/'+Path(__file__).name]],'validation':[{'command':'Counterfactual painted invitation native fit at both aspects','result':'PENDING','evidence':(P/'PLAN.json').relative_to(R).as_posix()}],'acceptance_gaps':'Counterfactual fixture substitutes a non-runtime backdrop subclass. It cannot prove current artwork, complete actor contact, background native coverage, runtime action or owner/device/child acceptance. No new production binding.'})
(P/'review_tools').mkdir(parents=True);(P/'.gdignore').write_text('',encoding='utf-8')
boundary=read(R/'audit/job_geode_current_recheck_v1_20261002/SOURCE_CURRENT_BEFORE_CAPTURE.json');assert len(boundary['source_files'])==783 and all(sha(R/x['path'])==x['sha256'] for x in boundary['source_files'])
write(P/'SOURCE_CURRENT_BEFORE_CAPTURE.json',boundary)
# Atlas addresses pixels only; do not transform the native generated source.
x0,y0,x1,y1=bounds
backdrop='''extends OperaWorldBackdrop2D
## NON-RUNTIME COUNTERFACTUAL PROP FIT. Source and production owners unchanged.

func _load_geology_props() -> void:
\tsuper._load_geology_props()
\tfor entry: Array in [["fossil", "fossil.png", Rect2(115,171,802,674)],
\t\t["mineral", "mineral.png", Rect2(231,130,569,767)]]:
\t\tvar atlas := AtlasTexture.new()
\t\tatlas.atlas = load(GEOLOGY_WORK_ART + String(entry[1])) as Texture2D
\t\tatlas.region = entry[2] as Rect2
\t\tatlas.filter_clip = true
\t\tgeology_props[String(entry[0])] = atlas
\tvar tray := AtlasTexture.new()
\ttray.atlas = ImageTexture.create_from_image(Image.load_from_file("res://assets_src/imagegen/geologist_specimen_tray_v1_20261003/attempt01/native.png"))
\ttray.region = Rect2(TRAYRECT)
\ttray.filter_clip = true
\tgeology_props["tray"] = tray

func _draw_geologist(mid: Color, _accent: Color) -> void:
\t# Existing wall bands retained verbatim: this study does not pass the room.
\tfor band in range(5):
\t\tvar y := 150.0 + float(band) * 74.0
\t\tvar color := mid.lightened(0.18 - float(band) * 0.055)
\t\tdraw_polyline(PackedVector2Array([Vector2(0,y+24),Vector2(220,y-12),
\t\t\tVector2(470,y+18),Vector2(760,y-18),Vector2(1040,y+12),Vector2(1280,y-10)]),color,34.0)
\tif stage_mode:
\t\t_draw_geology_prop("slab", GEOLOGY_CELEBRATION_SLAB)
\t\treturn
\tif bool(get_meta("geology_work_open", false)):
\t\treturn
\t_draw_geology_prop("slab",Rect2(355,485,180,180.0*369.0/889.0))
\t_draw_geology_prop("fossil",Rect2(383,425,105,105.0*674.0/802.0))
\t_draw_geology_prop("slab",Rect2(530,445,430,430.0*369.0/889.0))
\tvar tray: Texture2D = geology_props["tray"] as Texture2D
\tvar tray_height := 110.0*tray.get_height()/float(tray.get_width())
\tfor index in range(3):
\t\t_draw_geology_prop("tray",Rect2(550.0+float(index)*145.0,520.0-tray_height,110,tray_height))
\t_draw_geology_prop("mineral",Rect2(1090,435,130.0*569.0/767.0,130))
'''.replace('TRAYRECT',f'{x0},{y0},{x1-x0},{y1-y0}')
(P/'painted_prop_backdrop.gd').write_text(backdrop,encoding='utf-8',newline='\n')
old=R/'audit/job_geode_current_recheck_v1_20261002/capture.gd'
s=old.read_text(encoding='utf-8').replace('res://audit/job_geode_current_recheck_v1_20261002/attempt01/','res://audit/job_geology_painted_invitation_fit_v1_20261003/attempt01/')
s=s.replace('\t\t\tmotion_world = world\n\t\t\trecord_motion = true\n','')
needle='\tassert(world != null and world.phase_index == 0 and world.phases.size() == 4)\n'
assert s.count(needle)==1
s=s.replace(needle,needle+'''\tvar original_backdrop := world.backdrop_node
\tvar replacement := (load("res://audit/job_geology_painted_invitation_fit_v1_20261003/painted_prop_backdrop.gd") as GDScript).new() as OperaWorldBackdrop2D
\tvar parent := original_backdrop.get_parent()
\tparent.add_child(replacement)
\tparent.move_child(replacement, original_backdrop.get_index())
\treplacement.position = original_backdrop.position
\treplacement.size = original_backdrop.size
\treplacement.setup("geologist")
\tworld.backdrop_node = replacement
\toriginal_backdrop.queue_free()
\tawait _wait(4)
\tevents.append({"event":"NON_RUNTIME_COUNTERFACTUAL_BACKDROP_SUBSTITUTION","production_binding":false})
''')
s=s.replace('ACTUAL_LIBRARY_ALL4_PHASES_EARNED_RETURN_AND_DEV_ENTRY_CAPTURED_REVIEW_PENDING','COUNTERFACTUAL_PAINTED_PROPS_SELECTED_VIEWS_REVIEW_PENDING')
s=s.replace('Native capture readback slows wall clock.','Non-runtime backdrop substituted for static prop fit only. No production source changed, no full action or current room acceptance.')
(P/'capture.gd').write_text(s,encoding='utf-8',newline='\n')
write(P/'PLAN.json',{'status':'PREPARED_BEFORE_COUNTERFACTUAL_CAPTURE','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'baseline':'1652a9bb33af0d11a594b5996df66d2266c02d39','fixture':old.relative_to(R).as_posix(),'fixture_sha256':sha(old),'native_views':[1280,1600],'scope':'Selected normal Library four-phase/elevator views with an explicit non-runtime backdrop substitution; native motion capture disabled. Complete current actions remain the independent unchanged-source capture packet.','sole_pixel_ownership':'Override only named geology props, remove each original flat drawing/ring rather than adding a sticker on top. Existing wall bands/lights remain weak. Preserve work-open hide and unchanged earned-stage slab.','source_art':'Exact painted fossil/mineral/slab plus unchanged generated native tray using alpha region addresses only; no image editing.','planned_clearance':'Fossil slab x355..535 clear of Roshan left-side card; specimen trays on shared x530..960 slab; crystal x1090..1187 beside rather than beneath the rival. All relationships require native review.','source_boundary_count':783,'current_production_unchanged':True,'owner_acceptance':None,'integration':False,'release':False})
shutil.copyfile(Path(__file__),F/'review_tools'/Path(__file__).name)
shutil.copyfile(Path(__file__),P/'review_tools'/Path(__file__).name)
licenses=R/'ASSET_LICENSES.md'
with licenses.open('a',encoding='utf-8',newline='\n') as out:
 out.write('\n| `assets_src/imagegen/geologist_specimen_tray_v1_20261003/attempt01/native.png` | OpenAI built-in ImageGen, fresh text-only single empty painted specimen tray | Original project-generated art; OpenAI terms | https://openai.com/policies/terms-of-use/ | Exact native RGBA preserved; prompt/native SHA and six component opinions. Source4.6 provisional, native contour4.5 priority, mounted/current/action/owner acceptance separate; no existing reference upload. |\n')
 out.write('| `audit/job_geology_complete_actions_v1_20261003/**`, `audit/job_geology_painted_invitation_fit_v1_20261003/**` | Authorized native Godot4.7.2 game/fixture capture and read-only diagnostic display evidence | Original project review evidence; original source provenance retained | Exact PLAN, capture/source hashes and raw machine receipts | Actual unchanged-source full actions and counterfactual static backdrop fit are explicitly separate. Failed attempts preserved; no device/child/owner or cinematic delivery acceptance. |\n')
for packet,impact in [(F,R/'design/audit_impacts/job-geology-specimen-tray-20261003.json'),(P,ip)]:
 d=read(impact);d['files']=sorted(set(d['files'])|{p.relative_to(R).as_posix() for p in packet.rglob('*') if p.is_file()}|{'ASSET_LICENSES.md'});write(impact,d)
print(json.dumps({'native_dimensions':dims,'alpha_used_rect':bounds,'native_sha256':sha(a/'native.png'),'source_score':4.6,'fit':'PREPARED_COUNTERFACTUAL_ONLY'}))
