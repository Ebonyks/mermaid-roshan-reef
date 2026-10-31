extends SceneTree
## Offline painted-clothing assembly. Never resamples/reorders character cells.
const OUT := "res://assets/fashion/skin_engine_v2/"
const SOURCE := "res://assets_src/fashion_designer/skin_engine_v2/"
const FIT := "res://assets_src/fashion_designer/party_garment_v1/pose_fit.json"
const OTHER := {
	"rumi_eight_pose_runtime": {"source": "assets/characters/rumi/rumi_eight_pose_runtime.png", "character": "rumi", "cell": [256,384], "boxes": [[133,106,191,175],[102,105,159,177],[94,110,153,181],[91,111,150,183],[161,105,217,179],[147,107,204,178],[153,99,210,171],[154,103,211,174]]},
	"rumi_pool_idle_swim_atlas": {"source": "assets/characters/rumi/rumi_pool_idle_swim_atlas.png", "character": "rumi", "cell": [256,256], "boxes": [[111,61,149,111],[111,61,149,111],[112,61,150,111],[112,61,150,111],[157,64,196,112],[164,64,203,112],[163,63,202,111],[165,65,204,113]]},
	"daddy": {"source": "assets/characters/friends/daddy.webp", "character": "daddy_mermaid", "cell": [727,1024], "boxes": [[295,212,481,458]], "protected_boxes": [[275,413,345,510]], "cloth_polygon": [[340,212],[419,212],[458,257],[480,405],[422,458],[301,441],[295,280]]},
	"baby_eagle": {"source": "assets/characters/companions/baby_eagle.png", "character": "baby_eagle", "cell": [290,512], "boxes": [[130,207,180,244]]},
	"rainbow_friend": {"source": "assets/sprites/dust_bunnies/rainbow_friend.png", "character": "rainbow_dust_bunny", "cell": [512,512], "boxes": [[214,370,290,425]]},
}
const GARMENTS := {
	"party": "res://assets_src/fashion_designer/party_garment_v1/native.png",
	"garden": SOURCE + "native/roshan_garden.png",
	"rumi_party": SOURCE + "native/rumi_festival.png",
	"daddy_party": SOURCE + "native/daddy_festival.png",
	"daddy_garden": SOURCE + "native/daddy_garden.png",
	"ribbon": SOURCE + "native/pearl_bow.png",
}

func _trim(path: String) -> Image:
	var image: Image = Image.load_from_file(path)
	image.convert(Image.FORMAT_RGBA8)
	return image.get_region(image.get_used_rect())

func _export_component(image: Image, path: String, limit: int = 512, padded: bool = true) -> void:
	var scaled: Image = image.duplicate() as Image
	var ratio: float = minf(float(limit) / scaled.get_width(), float(limit) / scaled.get_height())
	scaled.resize(maxi(1, roundi(scaled.get_width() * ratio)), maxi(1, roundi(scaled.get_height() * ratio)), Image.INTERPOLATE_LANCZOS)
	if not padded:
		scaled.save_png(path)
		return
	var canvas: Image = Image.create(limit, limit, false, Image.FORMAT_RGBA8)
	canvas.blit_rect(scaled, Rect2i(Vector2i.ZERO, scaled.get_size()), (canvas.get_size() - scaled.get_size()) / 2)
	canvas.save_png(path)

func _cloth_pixel(pixel: Color, character: String) -> bool:
	if pixel.a < 0.02:
		return false
	if character == "daddy_mermaid":
		return true # Explicit hand ROI and coat polygon protect his original anatomy.
	# Preserve original skin/hand highlights; no face is in any clothing ROI.
	if pixel.r > pixel.b + 0.09 and pixel.g > pixel.b + 0.025:
		return false
	if character == "roshan":
		return pixel.r > 0.48 and pixel.b > 0.43 and pixel.b > pixel.g * 1.09
	if character == "rumi":
		# Bright braid and turquoise/pink tail colors crossing a torso ROI stay intact.
		if pixel.r > pixel.g * 1.7 and pixel.b > pixel.g * 1.7:
			return false
		if pixel.g > pixel.r * 1.3 and pixel.b > pixel.r * 1.2:
			return false
	return true

func _clean_daddy() -> Image:
	# Preserve the approved PNG master's pose/RGB; repair its white matte only.
	# The protected runtime WEBP has visible encoded strips and colored blocks.
	var image: Image = Image.load_from_file("res://assets_src/daddy_master.png")
	image.convert(Image.FORMAT_RGBA8)
	image.resize(727,1024,Image.INTERPOLATE_LANCZOS)
	for y: int in range(image.get_height()):
		for x: int in range(image.get_width()):
			var pixel: Color = image.get_pixel(x,y)
			var low: float = minf(pixel.r,minf(pixel.g,pixel.b))
			var high: float = maxf(pixel.r,maxf(pixel.g,pixel.b))
			if low > 0.88 and high-low < 0.045:
				pixel.a *= clampf((0.96-low)/0.08,0.0,1.0)
				image.set_pixel(x,y,pixel)
	image.save_png(OUT+"atlases/daddy_original.png")
	return image

func _initialize() -> void:
	var raw: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(FIT)) as Dictionary
	var families: Dictionary = OTHER.duplicate(true)
	for family: String in raw["sources"]:
		var fit: Dictionary = raw["sources"][family]
		families[family] = {"source": fit["source"], "character": "roshan", "cell": [256,256], "boxes": fit["cells"]}
	var garments: Dictionary = {}
	for key: String in GARMENTS:
		garments[key] = _trim(String(GARMENTS[key]))
		_export_component(garments[key], OUT + "garments/" + key + ".png")
	for key: String in ["wardrobe_panel", "wardrobe_card"]:
		_export_component(_trim(SOURCE + "native/" + key + ".png"), OUT + "ui/" + key + ".png", 256 if key == "wardrobe_card" else 1024, false)
	var clean_daddy: Image = _clean_daddy()
	var derivations: Array[Dictionary] = []
	for family: String in families:
		var spec: Dictionary = families[family]
		var original: Image = Image.load_from_file("res://" + String(spec["source"]))
		original.convert(Image.FORMAT_RGBA8)
		if family == "daddy":
			original = clean_daddy.duplicate() as Image
			spec["pixel_source"] = OUT+"atlases/daddy_original.png"
			spec["master_source"] = "assets_src/daddy_master.png"
		var cell: Array = spec["cell"]
		var boxes: Array = spec["boxes"]
		var polygon := PackedVector2Array()
		for vertex: Array in spec.get("cloth_polygon",[]):
			polygon.append(Vector2(float(vertex[0]),float(vertex[1])))
		var columns: int = original.get_width() / int(cell[0])
		spec["dimensions"] = [original.get_width(), original.get_height()]
		spec["source_sha256"] = FileAccess.get_sha256("res://" + String(spec["source"]))
		spec["variants"] = {}
		if family == "daddy": spec["variants"]["original"] = OUT+"atlases/daddy_original.png"
		var kinds: Array[String] = ["ribbon", "party", "garden"]
		if spec["character"] == "roshan":
			kinds.append("disguise")
		for kind: String in kinds:
			var result: Image = original.duplicate() as Image
			var character: String = String(spec["character"])
			var garment_key: String = "garden" if kind == "disguise" else kind
			if character == "rumi" and kind == "party":
				garment_key = "rumi_party"
			if character == "daddy_mermaid" and kind in ["party", "garden"]:
				garment_key = "daddy_" + kind
			var garment: Image = garments[garment_key]
			if character in ["roshan","rumi"] and kind in ["party","garden","disguise"] and garment_key != "rumi_party":
				garment = garment.get_region(Rect2i(roundi(garment.get_width()*0.16),0,roundi(garment.get_width()*0.68),roundi(garment.get_height()*0.74)))
			if character == "daddy_mermaid" and kind in ["party","garden"]:
				garment = garment.get_region(Rect2i(0,roundi(garment.get_height()*0.15),garment.get_width(),roundi(garment.get_height()*0.85)))
			for index: int in range(boxes.size()):
				var b: Array = boxes[index]
				var origin := Vector2i(index % columns * int(cell[0]), index / columns * int(cell[1]))
				var box := Rect2i(int(b[0]), int(b[1]), int(b[2])-int(b[0]), int(b[3])-int(b[1]))
				var cloth: Image = garment.duplicate() as Image
				var cloth_size: Vector2i = box.size
				var placement: Vector2i = origin + box.position
				if kind == "ribbon" or character in ["baby_eagle", "rainbow_dust_bunny"]:
					cloth_size.y = mini(box.size.y, roundi(cloth_size.x * 0.75))
				cloth.resize(cloth_size.x, cloth_size.y, Image.INTERPOLATE_LANCZOS)
				for y: int in range(cloth_size.y):
					for x: int in range(cloth_size.x):
						var at: Vector2i = placement + Vector2i(x,y)
						if not polygon.is_empty():
							if not Geometry2D.is_point_in_polygon(Vector2(at),polygon):
								continue
						var protected_pixel: bool = false
						for bounds: Array in spec.get("protected_boxes",[]):
							if Rect2i(int(bounds[0]),int(bounds[1]),int(bounds[2])-int(bounds[0]),int(bounds[3])-int(bounds[1])).has_point(at):
								protected_pixel = true
						if protected_pixel:
							continue
						var source_pixel: Color = original.get_pixelv(at)
						if not _cloth_pixel(source_pixel, character):
							continue
						var paint: Color = cloth.get_pixel(x,y)
						var blended: Color = source_pixel.blend(paint)
						blended.a = source_pixel.a
						result.set_pixelv(at, blended)
				if kind == "disguise":
					var accessory: Image = (garments["ribbon"] as Image).duplicate() as Image
					accessory.resize(maxi(8, box.size.x / 2), maxi(8, box.size.y / 4), Image.INTERPOLATE_LANCZOS)
					var point: Vector2i = origin + box.position + Vector2i(box.size.x / 4, box.size.y / 2)
					for y: int in range(accessory.get_height()):
						for x: int in range(accessory.get_width()):
							var at: Vector2i = point + Vector2i(x,y)
							var pixel: Color = result.get_pixelv(at)
							if _cloth_pixel(original.get_pixelv(at), character):
								var painted: Color = pixel.blend(accessory.get_pixel(x,y))
								painted.a = pixel.a
								result.set_pixelv(at, painted)
			var destination: String = OUT + "atlases/" + family + "_" + kind + ".png"
			result.save_png(destination)
			spec["variants"][kind] = destination
			derivations.append({"path": destination, "source": spec["source"], "garment": GARMENTS[garment_key], "sha256": FileAccess.get_sha256(destination), "method": "Painted RGBA garment sampled only within declared clothing ROI; original alpha and protected color pixels preserved; no frame/layout/animation change"})
	var ids: Array[String] = ["roshan", "rumi", "baby_eagle", "daddy_mermaid", "rainbow_dust_bunny"]
	var outfits: Array[Dictionary] = []
	for person: String in ids:
		for kind: String in ["original", "ribbon", "party", "garden"]:
			var id: String = person + "_original" if kind == "original" else person + "_" + kind + "_v1"
			if person == "roshan" and kind == "party":
				id = "roshan_party_dress_v1"
			outfits.append({"id": id, "character": person, "kind": kind, "label": kind.capitalize(), "garment": "" if kind == "original" else OUT + "garments/" + ("daddy_" + kind if person == "daddy_mermaid" and kind in ["party","garden"] else ("rumi_party" if person == "rumi" and kind == "party" else kind)) + ".png"})
		if person == "roshan":
			outfits.append({"id":"roshan_garden_disguise_v1","character":person,"kind":"disguise","label":"Garden disguise","garment":OUT+"garments/garden.png"})
	var data: Dictionary = {"schema":2,"families":families,"outfits":outfits,"dressing_characters":["roshan","rumi","daddy_mermaid"],"identity_contract":"Source dimensions/cell regions/alpha/animation timing and pixels outside declared clothing ROIs remain unchanged"}
	var catalog: FileAccess = FileAccess.open(OUT+"catalog.tres",FileAccess.WRITE)
	catalog.store_string("[gd_resource type=\"Resource\" script_class=\"FashionSkinCatalog\" load_steps=2 format=3]\n\n[ext_resource type=\"Script\" path=\"res://scripts/fashion_skin_catalog.gd\" id=\"1\"]\n\n[resource]\nscript = ExtResource(\"1\")\ndata = "+JSON.stringify(data,"\t")+"\n")
	var record: FileAccess = FileAccess.open(SOURCE+"derivations.json",FileAccess.WRITE)
	record.store_string(JSON.stringify({"schema":2,"families":families,"outputs":derivations,"human_pose_fit":"PENDING; requires full-frame/cell review"},"\t")+"\n")
	print("FASHION_SKIN_BUILD|ALL OK|",derivations.size()," painted atlases; original frame geometry preserved")
	quit()
