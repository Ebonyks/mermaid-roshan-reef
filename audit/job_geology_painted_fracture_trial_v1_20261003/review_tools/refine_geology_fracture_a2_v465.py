from pathlib import Path
import datetime, hashlib, json, shutil, subprocess

R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
J=R/'audit/job_geology_painted_fracture_trial_v1_20261003'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
ip=R/'design/audit_impacts/job-geology-painted-fracture-trial-20261003.json'
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()=='ce154e1452c92252b90f5455989a21726d94ff62'
boundary=read(J/'SOURCE_CURRENT_BEFORE_CAPTURE.json')['source_files']
assert len(boundary)==783 and all(sha(R/x['path'])==x['sha256'] for x in boundary)

# Record the complete direct A1 review already performed before any A2 edit.
m=read(J/'QA_BOARD_MANIFEST_A1.json')
assert len(m['boards'])==47 and sum(x['count'] for x in m['boards'])==491
for b in m['boards']:
 assert sha(R/b['path'])==b['sha256']
 b['direct_review']=True
m['status']='ALL_433_CONSECUTIVE_FRAMES_AND_58_SELECTED_CANVASES_DIRECTLY_REVIEWED'
m['reviewed_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
write(J/'QA_BOARD_MANIFEST_A1.json',m)
details=[]
for width,indices in [(1280,[104,105,140,165,190,201]),(1600,[103,104,139,164,189,200])]:
 cap=read(J/'attempt01'/f'CAPTURE_{width}.json')
 chosen=[x for x in cap['views'] if any(x['path'].endswith(f'_phase1_{tag}.webp') for tag in ['brushed','one_piece','two_pieces','earned_completion'])]
 chosen += [cap['motion_frames'][i] for i in indices]
 assert len(chosen)==10
 for x in chosen:
  assert sha(R/x['path'])==x['sha256']
  details.append({'path':x['path'],'sha256':x['sha256'],'direct_review':True,'scope':'Original entire native canvas inspected independently of ordered QA boards.'})
opinions=[]
def opinion(item,score,evaluation,refinement):
 opinions.append({'item':item,'score':score,'priority_inclusive':score<=4.5,'meets_floor_provisional':score>=4.5,'evaluation':evaluation,'refinement':refinement,'scope':'A1 NON_RUNTIME_COUNTERFACTUAL inherited fracture renderer; does not replace current production score or grant owner/device/child acceptance.'})
for name in ['left fragment','middle fragment','right fragment']:
 opinion(name,4.4,'Original painted lavender stone and golden fossil are conserved. Shared irregular boundaries remove straight rectangular strip silhouettes. Exposed cuts lack the clean plum material contour of the authored outer rock and read as unfinished image cuts.','Add restrained source-compatible plum contours only along exposed opaque internal edges; preserve source pixels and the exact complementary partition.')
opinion('reassembled fossil',4.5,'Native assembled spiral remains continuous and recognizable, with conserved proportions and original material. Slight raster edge aliasing keeps the opinion provisional.','Inspect final joins after any contour change; hide internal seam strokes when neighboring pieces are both snapped.')
opinion('intact fossil material',4.5,'The reusable broad painted stone bands and warm spiral already fit the storybook material language. No new generated source is needed for this renderer defect.','Preserve source and attribution; judge exposed edges separately.')
opinion('soil clearing',3.9,'Actual inherited brush grid retains a coarse reveal and vanishes remaining dirt at the completion threshold. Better fragment material does not repair this behavior.','Develop truthful gradual brush/soil removal in a separate reversible action study.')
opinion('brush-to-fragments transition',3.2,'Complete consecutive canvases show remaining soil disappearing and separated pieces appearing at their remote homes abruptly.','Repair visible continuity and staging through the true contact/reveal transition, then recapture every frame.')
opinion('working hand contact',2.7,'Roshan remains away from the working object, with no visible gripping or brushing contact.','Create and audit connected action/contact poses and sequencing at the actual work surface.')
opinion('ghost fossil target',4.2,'The faint intact target supports placement, but exposed pieces crossing it create a layered double-image impression.','Review target opacity and overlap through the full drag/snap sequence without obscuring the pieces.')
opinion('room',2.8,'Flat bands, generic spotlights and empty staging still fail the surrounding painted world.','Use a qualified painted room source with required native coverage, preserving readable interaction staging.')
opinion('earned completion transition',4.0,'Intentional completion and actual return are preserved; generic celebration presentation resets the fossil context rather than celebrating the restored specimen.','Retain the authored restored fossil in a grounded, truthful celebration sequence.')
opinion('whole fossil action',3.6,'Irregular fragments improve material coherence, but unlined cuts, sudden clearing/separation and distant hands keep the complete action below the floor.','Continue isolated fragment refinement, then repair action/contact and recapture the complete ordinary route; do not transfer the material score to the sequence.')
write(J/'DIRECT_REVIEW_ATTEMPT01.json',{'status':'EXPOSED_EDGES_4_4_REJECTED_FOR_FLOOR_JOINED_4_5_PROVISIONAL_WHOLE_ACTION_3_6','reviewed_utc':m['reviewed_utc'],'consecutive_frames':433,'selected_views':58,'ordered_boards':47,'native_details':details,'opinions':opinions,'production_binding':False,'owner_acceptance':None,'qualification':'Actual inherited Library four-phase intentional-input route, earned Library return and elevator developer entry/Back, with an explicit draw-only counterfactual substitution. Complete fossil action only; pan/geode selected views. Main/Castle entry fixture, isolated saves, desktop Mobile and slow readback do not establish ordinary travel, phone, child, owner or all-job acceptance.'})
originals=J/'attempt01/fixture_originals'
for filename in ['capture.gd','painted_fracture_surface.gd']:
 out=originals/(filename+'.original');assert not out.exists();shutil.copyfile(J/filename,out)

plan=read(J/'PLAN.json')
plan['attempt02']={'gap':'A1 exposed internal edges4.4: unfinished cut-image appearance.','change':'Renderer-only 2px plum contour along cached opaque portions of shared internal fractures. Suppress a side when both neighboring pieces are snapped. Same raster, UVs, partition, input, targets, save, progress and completion.','source_alpha':'Read-only original texture alpha bounds line runs; no pixel writes, conversion, raster repair or imagegen upload.','required_evidence':'Fresh parser/inference and official Godot analyzers, actual-input full four-phase earned return at both widths, every consecutive fossil frame and selected native view directly reviewed; exact783 production boundary. No predicted score.','production_binding':False,'owner_acceptance':None}
write(J/'PLAN.json',plan)
d=read(ip);d['scope']+=' A1 all433frames/58selectedviews/47boards/20native details directly reviewed; each exposed cut4.4, joined4.5 provisional, whole3.6. A2 renderer-only read-only alpha-bounded plum internal contours with adjacent-snap suppression; preserve exact A1 fixture before edits and require fresh complete input captures and review.';write(ip,d)

A=[(1/3,0),(.31,.13),(.365,.27),(.315,.40),(.35,.54),(.29,.69),(.355,.84),(1/3,1)]
B=[(2/3,0),(.705,.15),(.64,.28),(.69,.43),(.63,.58),(.70,.73),(.645,.87),(2/3,1)]
polys=[[(0,0)]+A+[(0,1)],A+list(reversed(B)),B+[(1,1),(1,0)]]
areas=[abs(sum(p[i][0]*p[(i+1)%len(p)][1]-p[(i+1)%len(p)][0]*p[i][1] for i in range(len(p)))/2) for p in polys]
assert abs(sum(areas)-1)<1e-10 and all(a>0 for a in areas)
assert all(curve[i+1][1]>curve[i][1] for curve in [A,B] for i in range(7))
assert all(a[0]<b[0] for a,b in zip(A,B))
write(J/'PARTITION_GEOMETRY_PROOF.json',{'source_sha256':sha(R/'assets/opera/worlds/geology/painted_work_v1_20261001/fossil.png'),'piece_areas':areas,'sum_area':sum(areas),'shared_y_monotonic_boundaries':[A,B],'union_entire_original_atlas':True,'no_interior_overlap':'Two separated y-monotonic boundaries; adjacent pieces share identical boundary coordinates.','maximum_internal_excursion':max(abs(x-(1/3 if k==0 else 2/3)) for k,curve in enumerate([A,B]) for x,y in curve),'pick_margin_unchanged_pixels':24,'qualification':'Geometry/UV conservation proof only, never a visual score or acceptance.'})

s=(J/'painted_fracture_surface.gd').read_text(encoding='utf-8-sig')
s=s.replace('const FRACTURE_A :=','var _fracture_edge_runs: Dictionary = {}\n\nconst FRACTURE_A :=',1)
s += '''
\tif index > 0 and not (fossil_snapped[index] and fossil_snapped[index - 1]):
\t\t_draw_exposed_fracture(index - 1, atlas, rect, offset, full_size)
\tif index < 2 and not (fossil_snapped[index] and fossil_snapped[index + 1]):
\t\t_draw_exposed_fracture(index, atlas, rect, offset, full_size)

func _opaque_fracture_runs(edge: int, atlas: AtlasTexture) -> Array:
\tif _fracture_edge_runs.has(edge):
\t\treturn _fracture_edge_runs[edge]
\tvar image: Image = atlas.atlas.get_image()
\tvar curve: Array = FRACTURE_A if edge == 0 else FRACTURE_B
\tvar runs: Array[PackedVector2Array] = []
\tvar run := PackedVector2Array()
\tfor segment: int in range(curve.size() - 1):
\t\tfor step: int in range(49):
\t\t\tif segment > 0 and step == 0:
\t\t\t\tcontinue
\t\t\tvar point: Vector2 = curve[segment].lerp(curve[segment + 1], float(step) / 48.0)
\t\t\tvar pixel := atlas.region.position + point * atlas.region.size
\t\t\tvar x := clampi(floori(pixel.x), 0, image.get_width() - 1)
\t\t\tvar y := clampi(floori(pixel.y), 0, image.get_height() - 1)
\t\t\tif image.get_pixel(x, y).a > 16.0 / 255.0:
\t\t\t\trun.append(point)
\t\t\telse:
\t\t\t\tif run.size() > 1:
\t\t\t\t\truns.append(run)
\t\t\t\trun = PackedVector2Array()
\tif run.size() > 1:
\t\truns.append(run)
\t_fracture_edge_runs[edge] = runs
\treturn runs

func _draw_exposed_fracture(edge: int, atlas: AtlasTexture, rect: Rect2,
\t\toffset: Vector2, full_size: Vector2) -> void:
\tfor run: PackedVector2Array in _opaque_fracture_runs(edge, atlas):
\t\tvar points := PackedVector2Array()
\t\tfor point: Vector2 in run:
\t\t\tpoints.append(rect.position + (point - offset) * full_size)
\t\tdraw_polyline(points, Color("#77516f"), 2.0, true)
'''
(J/'painted_fracture_surface.gd').write_text(s,encoding='utf-8',newline='\n')
c=(J/'capture.gd').read_text(encoding='utf-8-sig').replace('/attempt01/','/attempt02/')
(J/'capture.gd').write_text(c,encoding='utf-8',newline='\n')
(J/'attempt02').mkdir(exist_ok=False)
runner=(J/'review_tools/run_geology_fracture_trial_v462.py').read_text(encoding='utf-8-sig')
runner=runner.replace("G=J/'runtime_gate_a1'","G=J/'runtime_gate_a2'").replace("J/'attempt01'","J/'attempt02'").replace("+'_v462'","+'_v465'")
runner=runner.replace("shutil.copyfile(Path(__file__).with_name('prepare_geology_fracture_trial_v461.py'),J/'review_tools'/'prepare_geology_fracture_trial_v461.py')",'# Initial preparation and A1 runner remain preserved separately.')
(J/'review_tools/run_geology_fracture_trial_v465.py').write_text(runner,encoding='utf-8',newline='\n')
shutil.copyfile(Path(__file__),J/'review_tools'/Path(__file__).name)
d=read(ip);d['files']=sorted(set(d['files'])|{x.relative_to(R).as_posix() for x in J.rglob('*') if x.is_file()});write(ip,d)
assert all(sha(R/x['path'])==x['sha256'] for x in boundary)
print(json.dumps({'A1':'433 frames,58 views,47 boards,20 native details recorded; exposed edges4.4 preserved','A2':'Prepared, no predicted pass; renderer-only original-alpha-bounded2px plum edges','production_files_unchanged':len(boundary),'geometry_areas':areas}))
