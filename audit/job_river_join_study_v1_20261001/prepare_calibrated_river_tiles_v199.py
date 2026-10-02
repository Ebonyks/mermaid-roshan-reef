from pathlib import Path
import datetime, json, shutil
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');f=b/'audit/job_river_join_study_v1_20261001';source=b/'assets_src/imagegen/geologist_river_junctions_v1_20261001'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
p=source/'TECHNICAL_DERIVATIVES.json';d=read(p);d['status']='BOTH_COMPLETE_DERIVATIVES_DIRECTLY_REVIEWED4_6_UNBOUND';d['reviewed_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
for x in d['derivatives']:x['direct_review']=True;x['qualification']='Exact complete native1024 derivative directly inspected after uniform whole-canvas conversion; source4.6 only. No sampled network/port/owner approval.'
write(p,d)
gd=r'''extends OperaGeologySurface
## Isolated atlas field study. Actual parent input, grid, flow and saves unchanged.
const PARTS := "res://assets_src/imagegen/geologist_river_components_v1_20261001/"
const JUNCTIONS := "res://assets_src/imagegen/geologist_river_junctions_v1_20261001/"
const NATIVE_TO_RUNTIME := 1024.0 / 1254.0
var source_textures: Dictionary = {}
var dry_circle: Texture2D
var wet_circle: Texture2D

func _source_texture(path: String) -> Texture2D:
	if not source_textures.has(path):
		var image := Image.load_from_file(path)
		assert(image != null and image.get_size() == Vector2i(1024,1024))
		source_textures[path] = ImageTexture.create_from_image(image)
	return source_textures[path] as Texture2D

func _region(path: String, native_rect: Rect2) -> Texture2D:
	var atlas := AtlasTexture.new()
	atlas.atlas = _source_texture(path)
	atlas.region = Rect2(native_rect.position * NATIVE_TO_RUNTIME,
		native_rect.size * NATIVE_TO_RUNTIME)
	assert(Rect2(Vector2.ZERO,Vector2(1024,1024)).encloses(atlas.region))
	return atlas

func _load_textures() -> void:
	super._load_textures()
	dry_circle = _region(PARTS + "attempt_01/whole_canvas_1024.png",Rect2(44,167,560,547))
	wet_circle = _region(PARTS + "attempt_01/whole_canvas_1024.png",Rect2(655,167,560,547))

func _draw_circle_art(center: Vector2, wet: bool, width_now: float) -> void:
	var art := wet_circle if wet else dry_circle
	var size_now := Vector2(width_now,width_now * art.get_height() / float(art.get_width()))
	draw_texture_rect(art,Rect2(center-size_now*0.5,size_now),false)

func _mask(cell: Vector2i) -> int:
	var result := 0
	var steps: Array[Vector2i] = [Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT,Vector2i.UP]
	for bit: int in range(4):
		var next := cell + steps[bit]
		if next.x >= 0 and next.x < RIVER_COLS and next.y >= 0 and next.y < RIVER_ROWS \
				and river_wet[next.y * RIVER_COLS + next.x]:
			result |= 1 << bit
	return result

func _draw_field(center: Vector2, kind: String, angle: float, wet: bool) -> void:
	var source_path := JUNCTIONS + ("wet_attempt_01/" if wet else "dry_attempt_01/") \
		+ "whole_canvas_1024.png"
	var anchor := Vector2(941.0,915.5)
	var pixel_scale := 0.25
	if kind == "elbow":
		anchor = Vector2(889.0,407.0)
	elif kind == "tee":
		anchor = Vector2(317.0,963.0)
	var turned := not is_zero_approx(sin(angle))
	var extent := Vector2(76.0,88.0) if turned else Vector2(88.0,76.0)
	var region_now := Rect2(anchor - extent * 0.5 / pixel_scale,extent / pixel_scale)
	if kind == "endcap":
		anchor = Vector2(345.5555556,345.0)
		pixel_scale = 0.18
		# Keep the complete closed bowl; only its open right stub ends on its port plane.
		region_now = Rect2(53.0,119.0,anchor.x + extent.x * 0.5 / pixel_scale - 53.0,423.0)
	elif kind == "straight":
		source_path = PARTS + "attempt_02/whole_canvas_1024.png"
		var height_now := 302.0 if wet else 300.0
		var source_y := 734.0 if wet else 310.0
		pixel_scale = extent.x / 586.0
		region_now = Rect2(334.5,source_y,586.0,height_now)
		anchor = region_now.get_center()
	var art := _region(source_path,region_now)
	draw_set_transform(center,angle)
	draw_texture_rect(art,Rect2((region_now.position-anchor)*pixel_scale,
		region_now.size*pixel_scale),false)
	draw_set_transform(Vector2.ZERO)

func _draw_river() -> void:
	var flowing := _river_flow_indices()
	for index: int in range(RIVER_COLS * RIVER_ROWS):
		if not river_wet[index]:
			continue
		var cell := Vector2i(index % RIVER_COLS,index / RIVER_COLS)
		var center := river_path_cell_center(cell)
		var mask := _mask(cell)
		var wet := flowing.has(index)
		if mask == 0:
			_draw_circle_art(center,wet,60.0)
		elif mask in [1,2,4,8]:
			var angle := 0.0 if mask == 1 else PI*0.5 if mask == 2 else PI if mask == 4 else -PI*0.5
			_draw_field(center,"endcap",angle,wet)
		elif mask in [5,10]:
			_draw_field(center,"straight",0.0 if mask == 5 else PI*0.5,wet)
		elif mask in [9,3,6,12]:
			var angle := 0.0 if mask == 9 else PI*0.5 if mask == 3 else PI if mask == 6 else -PI*0.5
			_draw_field(center,"elbow",angle,wet)
		elif mask in [13,11,7,14]:
			var angle := 0.0 if mask == 13 else PI*0.5 if mask == 11 else PI if mask == 7 else -PI*0.5
			_draw_field(center,"tee",angle,wet)
		else:
			assert(mask == 15)
			_draw_field(center,"cross",0.0,wet)
	if not river_wet[RIVER_PATH[0].y * RIVER_COLS + RIVER_PATH[0].x]:
		_draw_circle_art(river_path_point(0),true,86.0)
	if not river_wet[RIVER_PATH[-1].y * RIVER_COLS + RIVER_PATH[-1].x]:
		_draw_circle_art(river_path_point(RIVER_PATH.size()-1),false,94.0)
	if held:
		_draw_brush(pointer_pos)
'''
p=f/'join_surface_v3.gd';assert not p.exists();p.write_text(gd,encoding='utf-8',newline='\n')
write(f/'TILE_CALIBRATION_V3.json',{'status':'EXPERIMENTAL_NATIVE_FIELDS_PENDING_SAMPLING_REVIEW','source_native_dimensions':[1254,1254],'complete_runtime_derivative':[1024,1024],'native_to_derivative':1024/1254,'grid_cell':[88,76],'branch_uniform_scale':0.25,'native_anchors':{'elbow':[889,407],'tee':[317,963],'cross':[941,915.5],'endcap':[345.5555556,345]},'endcap_uniform_scale':0.18,'straight_native_region':{'wet':[334.5,734,586,302],'dry':[334.5,310,586,300]},'orientation':'Normal Canvas2D rotation; quarter turns swap88/76 native field extents so final terminal planes still match grid centres. Complete closed endcap bowl retained, only open stubs trimmed.','method':'Read-only AtlasTexture fields of complete preserved derivatives. No rendered image pixels copied/edited, masking, warping or alpha repair. New source sampling/closed boundaries and every actual join still require direct native review.','reference':'Native wet aqua threshold was read-only RGBA/aquacolor geometry measurement; anchors are experimental, not accepted by IoU or source4.6 alone.'})
p=f/'capture_join_study_v3.gd';assert not p.exists();s=(f/'capture_join_study_v2.gd').read_text(encoding='utf-8').replace('/attempt_02/','/attempt_03/').replace('/join_surface.gd','/join_surface_v3.gd')
needle='\tawait _capture("isolated_dry")';assert needle in s;s=s.replace(needle,needle+'\n\tawait _line(Vector2i(4,0),Vector2i(5,0))\n\tawait _capture("isolated_dry_straight")\n\tawait _line(Vector2i(5,0),Vector2i(5,1))\n\tawait _capture("isolated_dry_corner")\n\tawait _line(Vector2i(5,0),Vector2i(6,0))\n\tawait _capture("isolated_dry_t")\n\tawait _line(Vector2i(5,1),Vector2i(6,1))\n\tawait _line(Vector2i(5,1),Vector2i(4,1))\n\tawait _line(Vector2i(5,1),Vector2i(5,2))\n\tawait _capture("isolated_dry_cross")',1);s=s.replace('assert(surface._river_flow_indices().size()==3 and completions==0)','assert(surface._river_flow_indices().size()==3 and completions==0)');p.write_text(s,encoding='utf-8',newline='\n')
p=f/'run_river_join_capture_v199.py';assert not p.exists();s=(f/'run_river_join_capture_v195.py').read_text(encoding='utf-8').replace("out=f/'attempt_02'","out=f/'attempt_03'").replace('capture%dv2','capture%dv3').replace('river_join_%d_v195','river_join_%d_v199').replace('capture_join_study_v2.gd','capture_join_study_v3.gd');p.write_text(s,encoding='utf-8',newline='\n');shutil.copyfile(__file__,f/Path(__file__).name)
for ip,folder in [(b/'design/audit_impacts/job-geology-river-join-study-20261001.json',f),(b/'design/audit_impacts/job-geology-river-junction-source-20261001.json',source)]:
 d=read(ip);d['files']=sorted(set(d['files'])|{p.relative_to(b).as_posix() for p in folder.rglob('*') if p.is_file()});write(ip,d)
print('New atlas sampling candidate prepared; original overlays and20 failed join opinions retained.')
