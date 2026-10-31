extends SceneTree
## Additive static clothing bake: authored character cells/animation never change.
const OUT := "res://assets/fashion/beta_20261025/"
const SOURCE := "res://assets_src/fashion_designer/beta_20261025/"
const THEMES: Array[String] = ["ballet", "magician", "candy", "astronaut"]
const SLOTS: Array[String] = ["head", "body", "tail"]

func _trim(path: String) -> Image:
	var image: Image = Image.load_from_file(path)
	assert(image != null, "Missing native garment: " + path)
	image.convert(Image.FORMAT_RGBA8)
	return image.get_region(image.get_used_rect())

func _material(p: Color, person: String, slot: String) -> bool:
	if p.a < 0.9999 or (p.r > p.b + 0.09 and p.g > p.b + 0.025): return false
	if slot == "body":
		if person == "roshan": return p.r > 0.48 and p.b > 0.43 and p.b > p.g * 1.09
		if person == "rumi":
			if p.r > p.g * 1.7 and p.b > p.g * 1.7: return false
			if p.g > p.r * 1.3 and p.b > p.r * 1.2: return false
	else:
		if person == "roshan": return p.b > 0.45 and p.b > p.r * 1.1
		if person == "rumi": return p.b > 0.5 and p.g > 0.35 and p.r < p.g * 0.9
	return true

func _initialize() -> void:
	DirAccess.make_dir_recursive_absolute(OUT + "items")
	DirAccess.make_dir_recursive_absolute(OUT + "layers")
	var original_catalog: Resource = load("res://assets/fashion/slots_v1/catalog.tres")
	var data: Dictionary = (original_catalog.get("data") as Dictionary).duplicate(true)
	var source_catalog: Resource = load("res://assets/fashion/skin_engine_v2/catalog.tres")
	var families: Dictionary = (source_catalog.get("data") as Dictionary)["families"] as Dictionary
	var rows: Array[Dictionary] = []
	for theme: String in THEMES:
		for slot: String in SLOTS:
			var key: String = theme + "_" + slot
			var native: String = SOURCE + "native/" + key + ".png"
			var garment: Image = _trim(native)
			var icon: Image = garment.duplicate() as Image
			var ratio: float = minf(420.0 / icon.get_width(), 420.0 / icon.get_height())
			icon.resize(maxi(1, roundi(icon.get_width() * ratio)), maxi(1, roundi(icon.get_height() * ratio)), Image.INTERPOLATE_LANCZOS)
			var card: Image = Image.create(512, 512, false, Image.FORMAT_RGBA8)
			card.blit_rect(icon, Rect2i(Vector2i.ZERO, icon.get_size()), (card.get_size() - icon.get_size()) / 2)
			var icon_path: String = OUT + "items/" + key + ".png"
			assert(card.save_png(icon_path) == OK)
			var id: String = slot + "_" + theme + "_v1"
			(data["items"] as Array).append({"id":id, "character":"*", "slot":slot, "kind":theme, "label":theme.capitalize(), "starter":theme in ["ballet", "magician"], "garment":icon_path})
			for family: String in data["fits"]:
				var spec: Dictionary = families[family] as Dictionary
				var person: String = String(spec["character"])
				var base: String = String((spec["variants"] as Dictionary).get("original", "res://" + String(spec["source"])))
				var source: Image = Image.load_from_file(base)
				source.convert(Image.FORMAT_RGBA8)
				var output: Image = Image.create(source.get_width(), source.get_height(), false, Image.FORMAT_RGBA8)
				var cell: Array = spec["cell"] as Array
				var columns: int = source.get_width() / int(cell[0])
				var fits: Array = data["fits"][family][slot] as Array
				var polygon := PackedVector2Array()
				for vertex: Array in spec.get("cloth_polygon", []): polygon.append(Vector2(float(vertex[0]), float(vertex[1])))
				for index: int in range(fits.size()):
					var b: Array = fits[index] as Array
					var box := Rect2i(int(b[0]), int(b[1]), int(b[2]) - int(b[0]), int(b[3]) - int(b[1]))
					var origin := Vector2i(index % columns * int(cell[0]), index / columns * int(cell[1]))
					var cloth: Image = garment.duplicate() as Image
					if slot == "head":
						var scale: float = minf(float(box.size.x) / cloth.get_width(), float(box.size.y) / cloth.get_height())
						cloth.resize(maxi(1, roundi(cloth.get_width() * scale)), maxi(1, roundi(cloth.get_height() * scale)), Image.INTERPOLATE_LANCZOS)
						var cap: Image = Image.create(box.size.x, box.size.y, false, Image.FORMAT_RGBA8)
						cap.blit_rect(cloth, Rect2i(Vector2i.ZERO, cloth.get_size()), Vector2i((box.size.x - cloth.get_width()) / 2, box.size.y - cloth.get_height()))
						cloth = cap
					else:
						# Use the complete painted garment, with no central-panel crop.
						# Registration still preserves the existing silhouette and foreground.
						cloth.resize(box.size.x, box.size.y, Image.INTERPOLATE_LANCZOS)
					for y: int in range(box.size.y):
						for x: int in range(box.size.x):
							var at: Vector2i = origin + box.position + Vector2i(x, y)
							var paint: Color = cloth.get_pixel(x, y)
							if slot == "head":
								if paint.a > 0.01: output.set_pixelv(at, paint)
								continue
							var old: Color = source.get_pixelv(at)
							if paint.a < 0.02 or not _material(old, person, slot): continue
							var protected_pixel: bool = false
							for bounds: Array in spec.get("protected_boxes", []):
								if Rect2i(int(bounds[0]), int(bounds[1]), int(bounds[2]) - int(bounds[0]), int(bounds[3]) - int(bounds[1])).has_point(at): protected_pixel = true
							if protected_pixel: continue
							if person == "daddy_mermaid" and slot == "body" and not Geometry2D.is_point_in_polygon(Vector2(at), polygon): continue
							var blended: Color = old.blend(paint)
							blended.a = 1.0
							output.set_pixelv(at, blended)
				var path: String = OUT + "layers/" + family + "_" + id + ".png"
				assert(output.save_png(path) == OK)
				data["layers"][family][id] = path
				rows.append({"path":path, "sha256":FileAccess.get_sha256(path), "family":family, "item_id":id, "slot":slot, "source":base, "source_sha256":FileAccess.get_sha256(base), "garment":native, "garment_sha256":FileAccess.get_sha256(native), "fit":fits, "full_source_rect":true, "fixed_opacity_reduction":false, "method":"Godot complete-source rectangle resize into unchanged slot masks; skin/hand/source contour and animation preserved. Human garment-fit review separate."})
	data["schema"] = 4
	var catalog: FileAccess = FileAccess.open(OUT + "catalog.tres", FileAccess.WRITE)
	catalog.store_string("[gd_resource type=\"Resource\" script_class=\"FashionSkinCatalog\" load_steps=2 format=3]\n\n[ext_resource type=\"Script\" path=\"res://scripts/fashion_skin_catalog.gd\" id=\"1\"]\n\n[resource]\nscript = ExtResource(\"1\")\ndata = " + JSON.stringify(data, "\t") + "\n")
	var record: FileAccess = FileAccess.open(SOURCE + "derivations.json", FileAccess.WRITE)
	record.store_string(JSON.stringify({"builder_sha256":FileAccess.get_file_as_string("res://tools/build_fashion_beta.gd").replace("\r\n", "\n").sha256_text(), "schema":1, "new_items":12, "outputs":rows, "old_catalog_sha256":FileAccess.get_file_as_string("res://assets/fashion/slots_v1/catalog.tres").replace("\r\n", "\n").sha256_text(), "source_text_hashing":"UTF-8 LF", "human_fit":"PENDING"}, "\t") + "\n")
	print("FASHION_BETA_BUILD|ALL OK|12 new pieces; ", rows.size(), " new layers")
	quit()
