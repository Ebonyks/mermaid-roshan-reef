from pathlib import Path
import datetime, hashlib, json, shutil, subprocess

R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
J=R/'audit/job_geology_painted_fracture_trial_v1_20261003'
F=R/'audit/job_geology_complete_actions_v1_20261003'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()
assert head=='ce154e1452c92252b90f5455989a21726d94ff62' and not J.exists()
boundary=read(F/'SOURCE_CURRENT_BEFORE_CAPTURE.json')
assert len(boundary['source_files'])==783 and all(sha(R/x['path'])==x['sha256'] for x in boundary['source_files'])
J.mkdir();(J/'review_tools').mkdir();(J/'attempt01').mkdir()
ip=R/'design/audit_impacts/job-geology-painted-fracture-trial-20261003.json'
rules=read(R/'design/audit_impacts/job-geology-painted-invitation-fit-20261003.json')['rules']
write(ip,{'id':ip.stem,'baseline':head,'scope':'Review-only painted fossil fracture trial. Reuse the unchanged approved intact ammonite texture and atlas; replace only its straight-third drawing in an explicitly substituted inherited geology surface with three complementary irregular textured Canvas polygons. Preserve all real input, touch margins, piece homes/targets, restore, progress, completion, world callback and every production byte. Capture actual-input Library four-phase route and complete fossil action at both desktop aspects. No raster editing, source regeneration, production binding, cinematic delivery or transfer of material opinions to whole action. Preserve every failed candidate and native view. Also durably preserve all18803 exact anonymous T verification rows in bounded lossless shards; publication remains independent of acceptance.','rules':rules,'findings':['MA-VIS-006','MA-PLAY-004','MA-OPERA-012'],'files':['audit/job_geology_painted_fracture_trial_v1_20261003/PLAN.json','audit/job_geology_painted_fracture_trial_v1_20261003/.gdignore','audit/job_geology_painted_fracture_trial_v1_20261003/painted_fracture_surface.gd','audit/job_geology_painted_fracture_trial_v1_20261003/capture.gd'],'validation':[{'command':'Direct source, partition, native complete route/action review at1280/1600','result':'PENDING','evidence':'No predicted visual score; complete captures required.'},{'command':'Official Godot4.7.2 parser/inference/analyzer and actual-input captures','result':'PENDING','evidence':'Individual unmodified mechanics and production boundary required.'}],'acceptance_gaps':'Non-runtime counterfactual. Source unchanged; room2.8/contact2.7/clearing3.9/pan3.4 remain priorities. Ordinary story/training/full travel/device/child/owner/all-job/integration/release and finding lifecycles remain open. Pending original Nursery reference-upload and browser persistence approvals remain independent.'})
source=R/'assets/opera/worlds/geology/painted_work_v1_20261001/fossil.png'
license_lines=[x for x in (R/'ASSET_LICENSES.md').read_text(encoding='utf-8-sig').splitlines() if 'painted_work_v1_20261001' in x and 'fossil' in x]
write(J/'PLAN.json',{'baseline':head,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'rules':rules,'findings':['MA-VIS-006','MA-PLAY-004','MA-OPERA-012'],'named_gap':'Current F direct complete action: straight vertical strip pieces3.6 each; fracture3.2; whole fossil3.2. Existing intact painted fossil material4.5 is reusable.','reuse_inventory':[{'path':source.relative_to(R).as_posix(),'sha256':sha(source),'role':'Sole material and identity authority. Same existing atlas115,171,802,674; native pixels preserved; no generation or upload.','license_rows':license_lines},{'path':'scripts/opera_geology_surface.gd','sha256':sha(R/'scripts/opera_geology_surface.gd'),'role':'Inherited actual mechanics; override only _draw_fossil_piece.'},{'path':F.relative_to(R).as_posix()+'/capture.gd','sha256':sha(F/'capture.gd'),'role':'Successful actual-input complete-route fixture; exact original archived.'}],'medium':'2D Canvas renderer geometry carrying original raster pixels; not replacement vector art or authored cinematic delivery.','partition':'Two monotonic irregular boundaries shared verbatim by adjacent pieces. Their union is the entire original rectangular atlas and their interiors do not overlap. Existing source alpha defines outer rock contour. UV mapping preserves original aspect and local material coordinates.','touch':'Each internal fracture excursion <=0.05 full width (<14px mounted), within existing24px generous pick margin. Existing target/home/pick/completion methods inherited unchanged.','review_required':'All selected canvases and every consecutive fossil frame, both widths; direct native join and exposed silhouettes. Geometry proof does not establish art quality.','production_binding':False,'runtime_acceptance':None,'owner_acceptance':None})
(J/'.gdignore').write_text('',encoding='utf-8')
shutil.copyfile(F/'SOURCE_CURRENT_BEFORE_CAPTURE.json',J/'SOURCE_CURRENT_BEFORE_CAPTURE.json')
(J/'attempt01'/'fixture_originals').mkdir()
shutil.copyfile(F/'capture.gd',J/'attempt01'/'fixture_originals'/'current_route_capture.gd.original')
shutil.copyfile(R/'scripts/opera_geology_surface.gd',J/'attempt01'/'fixture_originals'/'production_geology_surface.gd.original')
surface='''extends OperaGeologySurface
## NON_RUNTIME_COUNTERFACTUAL: original fossil pixels, complementary fracture
## partitions only. All inherited mechanics, saves, touch and input unchanged.
const FRACTURE_A := [Vector2(0.333333333333, 0.0), Vector2(0.31, 0.13),
\tVector2(0.365, 0.27), Vector2(0.315, 0.40), Vector2(0.35, 0.54),
\tVector2(0.29, 0.69), Vector2(0.355, 0.84), Vector2(0.333333333333, 1.0)]
const FRACTURE_B := [Vector2(0.666666666667, 0.0), Vector2(0.705, 0.15),
\tVector2(0.64, 0.28), Vector2(0.69, 0.43), Vector2(0.63, 0.58),
\tVector2(0.70, 0.73), Vector2(0.645, 0.87), Vector2(0.666666666667, 1.0)]

func piece_partition(index: int) -> PackedVector2Array:
\tvar polygon := PackedVector2Array()
\tif index == 0:
\t\tpolygon.append(Vector2.ZERO)
\t\tfor point: Vector2 in FRACTURE_A:
\t\t\tpolygon.append(point)
\t\tpolygon.append(Vector2(0.0, 1.0))
\telif index == 1:
\t\tfor point: Vector2 in FRACTURE_A:
\t\t\tpolygon.append(point)
\t\tfor i: int in range(FRACTURE_B.size() - 1, -1, -1):
\t\t\tpolygon.append(FRACTURE_B[i])
\telse:
\t\tfor point: Vector2 in FRACTURE_B:
\t\t\tpolygon.append(point)
\t\tpolygon.append(Vector2.ONE)
\t\tpolygon.append(Vector2(1.0, 0.0))
\treturn polygon

func _draw_fossil_piece(index: int, rect: Rect2) -> void:
\tvar atlas := fossil_texture as AtlasTexture
\tif atlas == null or atlas.atlas == null:
\t\tsuper._draw_fossil_piece(index, rect)
\t\treturn
\tvar points := PackedVector2Array()
\tvar uvs := PackedVector2Array()
\tvar colors := PackedColorArray()
\tvar full_size := Vector2(rect.size.x * 3.0, rect.size.y)
\tvar offset := Vector2(float(index) / 3.0, 0.0)
\tfor point: Vector2 in piece_partition(index):
\t\tpoints.append(rect.position + (point - offset) * full_size)
\t\tuvs.append((atlas.region.position + point * atlas.region.size) / atlas.atlas.get_size())
\t\tcolors.append(Color.WHITE)
\tdraw_polygon(points, colors, uvs, atlas.atlas)
'''
(J/'painted_fracture_surface.gd').write_text(surface,encoding='utf-8',newline='\n')
capture=(F/'capture.gd').read_text(encoding='utf-8-sig')
capture=capture.replace('## Actual production surface and all four ordinary career phases. Only entry\n## fixture and isolated test save home are supplied; no phase forcing, source\n## injection, replacement surface, background overlay or completion callback patch.','## NON_RUNTIME_COUNTERFACTUAL: inherited fossil draw override only. Actual\n## Library entry/earned four phases/return; original mechanics and pixels remain.\n## Explicit surface substitution; no phase forcing or callback/progress repair.')
capture=capture.replace('audit/job_geology_complete_actions_v1_20261003/attempt02/','audit/job_geology_painted_fracture_trial_v1_20261003/attempt01/')
capture=capture.replace('if phase in [1, 2]:','if phase == 1:')
marker='\tassert(not world.using_chapter_two_phases and not world.two_act_enabled)\n'
assert capture.count(marker)==1
sub='''\t# Preserve all script state and actual world signal callables. Only the
\t# derived draw method differs; no re-arming or phase/state injection.
\tvar original := world.surface as OperaGeologySurface
\tvar replacement := (load("res://audit/job_geology_painted_fracture_trial_v1_20261003/painted_fracture_surface.gd") as GDScript).new() as OperaGeologySurface
\tvar before_snapshot := original.progress_snapshot()
\tvar parent := original.get_parent()
\tparent.add_child(replacement)
\tparent.move_child(replacement, original.get_index())
\tfor property: Dictionary in original.get_property_list():
\t\tif int(property.get("usage", 0)) & PROPERTY_USAGE_SCRIPT_VARIABLE:
\t\t\tvar value: Variant = original.get(property["name"])
\t\t\tif value is Array or value is Dictionary:
\t\t\t\tvalue = value.duplicate(true)
\t\t\treplacement.set(property["name"], value)
\treplacement.position = original.position
\treplacement.size = original.size
\treplacement.visible = original.visible
\treplacement.mouse_filter = original.mouse_filter
\treplacement.texture_filter = original.texture_filter
\treplacement.process_mode = original.process_mode
\tfor signal_name: String in ["gesture", "progress_changed"]:
\t\tfor connection: Dictionary in original.get_signal_connection_list(signal_name):
\t\t\treplacement.connect(signal_name, connection["callable"], int(connection["flags"]))
\t\tassert(replacement.get_signal_connection_list(signal_name).size() == original.get_signal_connection_list(signal_name).size())
\tworld.surface = replacement
\tassert(replacement.progress_snapshot() == before_snapshot)
\tassert(replacement.get_global_transform_with_canvas() == original.get_global_transform_with_canvas())
\toriginal.queue_free()
\tawait _wait(4)
\tevents.append({"event":"NON_RUNTIME_COUNTERFACTUAL_FRACTURE_DRAW_ONLY_SUBSTITUTION",
\t\t"production_binding":false,"snapshot_before":before_snapshot,"snapshot_after":replacement.progress_snapshot(),
\t\t"original_pixels":OperaGeologySurface.FOSSIL_PATH,"original_source_sha256":FileAccess.get_sha256(OperaGeologySurface.FOSSIL_PATH)})
'''
capture=capture.replace(marker,sub+marker)
capture=capture.replace('"status":"ACTUAL_COMPLETE_FOSSIL_PAN_CAPTURE_REVIEW_PENDING"','"status":"COUNTERFACTUAL_FRACTURE_COMPLETE_FOSSIL_CAPTURE_REVIEW_PENDING"')
capture=capture.replace('ACTUAL_LIBRARY_COMPLETE_FOSSIL_PAN_ALL4_EARNED_RETURN_AND_DEV_ENTRY_CAPTURED_REVIEW_PENDING','COUNTERFACTUAL_DRAW_ONLY_COMPLETE_FOSSIL_ALL4_EARNED_RETURN_REVIEW_PENDING')
capture=capture.replace('Every input/wait frame of phases 1 and 2 captured','Every input/wait frame of phase1 fossil captured; pan receives selected views only')
capture=capture.replace('"qualification":"','"qualification":"Explicit non-runtime inherited fossil draw-only surface substitution. Original pixels/mechanics/targets retained. ')
capture=capture.replace('no phase forcing','no phase forcing')
(J/'capture.gd').write_text(capture,encoding='utf-8',newline='\n')
shutil.copyfile(Path(__file__),J/'review_tools'/Path(__file__).name)
# Publication evidence: all T rows remain byte-identical and reconstructible.
V=J/'previous_t_remote_verified';V.mkdir()
old=R/'tmp/geology_review_t_remote_v455'
result=read(old/'RESULT.json');assert result['status']=='PASS_ALL_ANONYMOUS_REMOTE_BYTES' and result['files_including_manifest']==18803 and not result['failed_files']
raw=(old/'VERIFICATION_JOURNAL.jsonl').read_bytes();lines=raw.splitlines(keepends=True)
assert len(lines)==18803
parts=[];buf=bytearray()
for line in lines:
 if len(buf)+len(line)>900000 and buf:
  p=V/('JOURNAL_%02d.jsonl'%(len(parts)+1));p.write_bytes(buf);parts.append({'path':p.relative_to(R).as_posix(),'sha256':sha(p),'bytes':len(buf)});buf=bytearray()
 buf.extend(line)
if buf:
 p=V/('JOURNAL_%02d.jsonl'%(len(parts)+1));p.write_bytes(buf);parts.append({'path':p.relative_to(R).as_posix(),'sha256':sha(p),'bytes':len(buf)})
assert b''.join((R/x['path']).read_bytes() for x in parts)==raw
shutil.copyfile(old/'RESULT.json',V/'RESULT.json')
write(V/'JOURNAL_INDEX.json',{'status':'EXACT_LOSSLESS_ALL18803_T_REMOTE_ROWS','original_sha256':hashlib.sha256(raw).hexdigest(),'original_bytes':len(raw),'rows':18803,'ordered_parts':parts,'reconstruction':'Concatenate part bytes in listed order; compare original SHA256.','qualification':'Publication only, no creative or acceptance claim.'})
planned={p.relative_to(R).as_posix() for p in J.rglob('*') if p.is_file()}
d=read(ip);d['files']=sorted(set(d['files'])|planned);write(ip,d)
print(json.dumps({'status':'PREPARED_NON_RUNTIME_DRAW_ONLY_TRIAL_REVIEW_PENDING','baseline':head,'source_sha256':sha(source),'T_remote_rows':18803,'T_journal_shards':len(parts),'files':len(planned)}))
