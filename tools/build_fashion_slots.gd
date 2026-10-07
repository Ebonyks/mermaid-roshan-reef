extends SceneTree
## Offline painted layers; original character cells, faces, hands and contours stay intact.
const OUT := "res://assets/fashion/slots_v1/"
const SOURCE := "res://assets_src/fashion_designer/slots_v1/"
const THEMES: Array[String] = ["strawberry", "chef", "painter", "star", "blossom", "winter"]
const SLOTS: Array[String] = ["head", "body", "tail"]

func _trim(path: String) -> Image:
	var image: Image = Image.load_from_file(path)
	image.convert(Image.FORMAT_RGBA8)
	return image.get_region(image.get_used_rect())

func _component(image: Image, path: String) -> void:
	var art: Image = image.duplicate() as Image
	var ratio: float = minf(420.0/art.get_width(),420.0/art.get_height())
	art.resize(maxi(1,roundi(art.get_width()*ratio)),maxi(1,roundi(art.get_height()*ratio)),Image.INTERPOLATE_LANCZOS)
	var canvas: Image = Image.create(512,512,false,Image.FORMAT_RGBA8)
	canvas.blit_rect(art,Rect2i(Vector2i.ZERO,art.get_size()),(canvas.get_size()-art.get_size())/2)
	canvas.save_png(path)

func _skin(pixel: Color) -> bool:
	return pixel.r > pixel.b + 0.09 and pixel.g > pixel.b + 0.025

func _body(pixel: Color, person: String) -> bool:
	if pixel.a < 0.9999 or _skin(pixel): return false
	if person == "roshan": return pixel.r > 0.48 and pixel.b > 0.43 and pixel.b > pixel.g*1.09
	if person == "rumi":
		if pixel.r > pixel.g*1.7 and pixel.b > pixel.g*1.7: return false
		if pixel.g > pixel.r*1.3 and pixel.b > pixel.r*1.2: return false
	return true

func _tail(pixel: Color, person: String) -> bool:
	if pixel.a < 0.9999 or _skin(pixel): return false
	if person == "roshan": return pixel.b > 0.45 and pixel.b > pixel.r*1.1
	if person == "rumi": return pixel.b > 0.5 and pixel.g > 0.35 and pixel.r < pixel.g*0.9
	return true

func _initialize() -> void:
	DirAccess.make_dir_recursive_absolute(OUT+"items")
	DirAccess.make_dir_recursive_absolute(OUT+"layers")
	var old: Resource = load("res://assets/fashion/skin_engine_v2/catalog.tres")
	var data: Dictionary = old.get("data") as Dictionary
	var fits: Dictionary = {}
	var layers: Dictionary = {}
	var items: Array[Dictionary] = []
	var derivations: Array[Dictionary] = []
	var art: Dictionary = {}
	_component(_trim(SOURCE+"native/original_return.png"),OUT+"items/original_return.png")
	for slot: String in ["head","tail"]:
		items.append({"id":slot+"_original","character":"*","slot":slot,"kind":"original","label":"Original","starter":true,"garment":""})
	for theme: String in THEMES:
		for slot: String in SLOTS:
			var key: String = theme+"_"+slot
			var native: String = SOURCE+"native/"+key+".png"
			var image: Image = _trim(native)
			# Strawberry headband's long side ties are omitted for face clearance.
			if key == "strawberry_head": image = image.get_region(Rect2i(0,0,image.get_width(),roundi(image.get_height()*0.46)))
			art[key] = image
			var icon: String = OUT+"items/"+key+".png"
			_component(image,icon)
			items.append({"id":slot+"_"+theme+"_v1","character":"*","slot":slot,"kind":theme,"label":theme.capitalize(),"starter":theme in ["star","blossom","winter"],"garment":icon,"theme_source":theme})
	for key: String in ["royal_head","pearl_head"]:
		var native: String = "res://assets/flats/castle/logo_studio_v2/castle_banner_motif_crown.png" if key == "royal_head" else "res://assets/fashion/skin_engine_v2/garments/ribbon.png"
		art[key] = _trim(native)
		var icon: String = OUT+"items/"+key+".png"
		_component(art[key] as Image,icon)
		items.append({"id":"head_"+key.trim_suffix("_head")+"_v1","character":"*","slot":"head","kind":key.trim_suffix("_head"),"label":"Crown" if key == "royal_head" else "Bow","starter":true,"garment":icon})
	for family: String in data["families"]:
		var spec: Dictionary = data["families"][family] as Dictionary
		var person: String = String(spec["character"])
		if person not in ["roshan","rumi","daddy_mermaid"]: continue
		var base: String = String((spec["variants"] as Dictionary).get("original","res://"+String(spec["source"])))
		var original: Image = Image.load_from_file(base)
		original.convert(Image.FORMAT_RGBA8)
		var cell: Array = spec["cell"] as Array
		var boxes: Array = spec["boxes"] as Array
		var columns: int = original.get_width()/int(cell[0])
		var body_fits: Array = boxes.duplicate(true)
		var head_fits: Array = []
		var tail_fits: Array = []
		for index: int in range(boxes.size()):
			var b: Array = boxes[index] as Array
			var width: int = int(b[2])-int(b[0])
			var center: int = (int(b[0])+int(b[2]))/2
			var origin := Vector2i(index%columns*int(cell[0]),index/columns*int(cell[1]))
			var top: int = int(b[1])
			for y: int in range(int(b[1])):
				for x: int in range(maxi(0,center-width/2),mini(int(cell[0]),center+width/2)):
					if original.get_pixelv(origin+Vector2i(x,y)).a > 0.5:
						top = mini(top,y)
			var cap_width: int = roundi(width*1.4)
			var cap_height: int = roundi(width*1.0)
			var left: int = clampi(center-cap_width/2,0,int(cell[0])-cap_width)
			var head_bottom: int = mini(int(b[1])-2,top+roundi(width*0.55))
			if person == "daddy_mermaid": head_bottom = 70
			var head_y: int = maxi(0,head_bottom-cap_height)
			head_fits.append([left,head_y,left+cap_width,head_bottom])
			var tail_top: int = int(b[3])+2
			var tail_bottom: int = mini(int(cell[1]),tail_top+roundi((int(b[3])-int(b[1]))*1.2))
			var tail_sum: int = 0
			var tail_count: int = 0
			if person != "daddy_mermaid":
				for y: int in range(tail_top,tail_bottom):
					for x: int in range(int(cell[0])):
						if _tail(original.get_pixelv(origin+Vector2i(x,y)),person):
							tail_sum += x
							tail_count += 1
			var tail_center: int = tail_sum/tail_count if tail_count > 0 else center
			var tail_left: int = maxi(0,tail_center-width)
			var tail_right: int = mini(int(cell[0]),tail_center+width)
			if person == "daddy_mermaid":
				tail_left = 220; tail_right = 446; tail_top = 510; tail_bottom = 712
			tail_fits.append([tail_left,tail_top,tail_right,tail_bottom])
		fits[family] = {"head":head_fits,"body":body_fits,"tail":tail_fits}
		layers[family] = {}
		for item: Dictionary in items:
			var slot: String = String(item["slot"])
			if String(item["kind"]) == "original": continue
			var art_key: String = String(item["kind"])+"_"+slot
			var garment: Image = art[art_key] as Image
			var output: Image = Image.create(original.get_width(),original.get_height(),false,Image.FORMAT_RGBA8)
			var declared: Array = fits[family][slot] as Array
			for index: int in range(declared.size()):
				var b: Array = declared[index] as Array
				var origin := Vector2i(index%columns*int(cell[0]),index/columns*int(cell[1]))
				var box := Rect2i(int(b[0]),int(b[1]),int(b[2])-int(b[0]),int(b[3])-int(b[1]))
				var cloth: Image = garment.duplicate() as Image
				# Sample the broad material panel, not transparency around sleeves/hem.
				if slot == "body" or slot == "tail":
					cloth = cloth.get_region(Rect2i(roundi(cloth.get_width()*0.25),roundi(cloth.get_height()*0.12),maxi(1,roundi(cloth.get_width()*0.5)),maxi(1,roundi(cloth.get_height()*0.65))))
				if slot == "head":
					var ratio: float = minf(float(box.size.x)/cloth.get_width(),float(box.size.y)/cloth.get_height())
					cloth.resize(maxi(1,roundi(cloth.get_width()*ratio)),maxi(1,roundi(cloth.get_height()*ratio)),Image.INTERPOLATE_LANCZOS)
					var cap: Image = Image.create(box.size.x,box.size.y,false,Image.FORMAT_RGBA8)
					cap.blit_rect(cloth,Rect2i(Vector2i.ZERO,cloth.get_size()),Vector2i((box.size.x-cloth.get_width())/2,box.size.y-cloth.get_height()))
					cloth = cap
				else:
					cloth.resize(box.size.x,box.size.y,Image.INTERPOLATE_LANCZOS)
				for y: int in range(box.size.y):
					for x: int in range(box.size.x):
						var at: Vector2i = origin+box.position+Vector2i(x,y)
						var src: Color = original.get_pixelv(at)
						var paint: Color = cloth.get_pixel(x,y)
						if slot == "head":
							if paint.a > 0.01: output.set_pixelv(at,paint)
							continue
						var protected_pixel: bool = false
						for bounds: Array in spec.get("protected_boxes",[]):
							if Rect2i(int(bounds[0]),int(bounds[1]),int(bounds[2])-int(bounds[0]),int(bounds[3])-int(bounds[1])).has_point(at): protected_pixel = true
						if protected_pixel or (not _body(src,person) if slot == "body" else not _tail(src,person)): continue
						if person == "daddy_mermaid" and slot == "body":
							var polygon := PackedVector2Array()
							for vertex: Array in spec["cloth_polygon"]: polygon.append(Vector2(float(vertex[0]),float(vertex[1])))
							if not Geometry2D.is_point_in_polygon(Vector2(at),polygon): continue
						if paint.a < 0.02: continue
						# Fully opaque interior delta preserves source edge alpha and painted detail.
						var blended: Color = src.blend(Color(paint.r,paint.g,paint.b,paint.a*0.88))
						blended.a = 1.0
						output.set_pixelv(at,blended)
			var path: String = OUT+"layers/"+family+"_"+String(item["id"])+".png"
			output.save_png(path)
			layers[family][String(item["id"])] = path
			derivations.append({"path":path,"family":family,"item_id":item["id"],"slot":slot,"source":base,"source_sha256":FileAccess.get_sha256(base),"sha256":FileAccess.get_sha256(path),"fit":declared,"method":"Godot offline cropped/resized painted garment; head limited to cap ROI, body/tail only opaque material interior; protected hand exclusions; no source/frame/animation changes"})
	var board: Image = Image.create(1000,800,false,Image.FORMAT_RGBA8)
	var board_index: int = 0
	for item: Dictionary in items:
		if String(item["garment"]).is_empty(): continue
		var picture: Image = Image.load_from_file(String(item["garment"]))
		picture.resize(180,180,Image.INTERPOLATE_LANCZOS)
		board.blend_rect(picture,Rect2i(Vector2i.ZERO,picture.get_size()),Vector2i(board_index%5*200+10,board_index/5*200+10))
		board_index += 1
	board.save_png(SOURCE+"item_contact_sheet.png")
	var payload: Dictionary = {"schema":3,"items":items,"layers":layers,"fits":fits}
	var catalog: FileAccess = FileAccess.open(OUT+"catalog.tres",FileAccess.WRITE)
	catalog.store_string("[gd_resource type=\"Resource\" script_class=\"FashionSkinCatalog\" load_steps=2 format=3]\n\n[ext_resource type=\"Script\" path=\"res://scripts/fashion_skin_catalog.gd\" id=\"1\"]\n\n[resource]\nscript = ExtResource(\"1\")\ndata = "+JSON.stringify(payload,"\t")+"\n")
	var record: FileAccess = FileAccess.open(SOURCE+"derivations.json",FileAccess.WRITE)
	record.store_string(JSON.stringify({"schema":3,"catalog":payload,"outputs":derivations,"human_pose_fit":"PENDING"},"\t")+"\n")
	print("FASHION_SLOTS_BUILD|ALL OK|",items.size()," items; ",derivations.size()," independent painted layers")
	quit()
