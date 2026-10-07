extends SceneTree
## Deterministic game clothing assembly; originals and native garment stay intact.
## This static gameplay atlas builder never produces cinematic frames.
const OUT := "res://assets/fashion/outfits/"
const FIT := "res://assets_src/fashion_designer/party_garment_v1/pose_fit.json"
const GARMENT := "res://assets_src/fashion_designer/party_garment_v1/native.png"
const OTHER := {
	"rumi_eight_pose_runtime": ["res://assets/characters/rumi/rumi_eight_pose_runtime.png", 256, 384,
		[[158, 123], [121, 121], [121, 128], [118, 130], [189, 126], [173, 127], [178, 117], [183, 123]]],
	"rumi_pool_idle_swim_atlas": ["res://assets/characters/rumi/rumi_pool_idle_swim_atlas.png", 256, 256,
		[[130, 79], [130, 79], [131, 79], [131, 79], [177, 84], [183, 83], [183, 82], [184, 84]]],
	"baby_eagle": ["res://assets/characters/companions/baby_eagle.png", 290, 512, [[155, 225]]],
	"daddy": ["res://assets/characters/friends/daddy.webp", 725, 1024, [[392, 255]]],
	"rainbow_friend": ["res://assets/sprites/dust_bunnies/rainbow_friend.png", 512, 512, [[251, 398]]],
}

func _initialize() -> void:
	# Optional `-- --fit=<pose_fit.json> --out=<dir/>` bakes the same four outfits onto other
	# 256 px cell atlases (animation clips) without touching the game outputs below.
	var fit_path: String = FIT
	var out_dir: String = OUT
	for arg: String in OS.get_cmdline_user_args():
		if arg.begins_with("--fit="):
			fit_path = arg.trim_prefix("--fit=")
		elif arg.begins_with("--out="):
			out_dir = arg.trim_prefix("--out=")
	var game_outputs: bool = fit_path == FIT and out_dir == OUT
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(out_dir))
	var fit: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(fit_path)) as Dictionary
	var garment: Image = Image.load_from_file(GARMENT)
	garment.convert(Image.FORMAT_RGBA8)
	garment = garment.get_region(garment.get_used_rect())
	if game_outputs:
		var export := garment.duplicate() as Image
		export.resize(384, 448, Image.INTERPOLATE_LANCZOS)
		var padded := Image.create(512, 512, false, Image.FORMAT_RGBA8)
		padded.blit_rect(export, Rect2i(0, 0, 384, 448), Vector2i(64, 32))
		padded.save_png("res://assets/fashion/party_dress_garment.png")
	for base: String in fit["sources"]:
		var spec: Dictionary = fit["sources"][base]
		var source: Image = Image.load_from_file("res://" + String(spec["source"]))
		source.convert(Image.FORMAT_RGBA8)
		for kind: String in ["ribbon", "party", "garden", "disguise"]:
			var output := source.duplicate() as Image
			var cells: Array = spec["cells"] as Array
			for index: int in range(cells.size()):
				var bounds: Array = cells[index] as Array
				var origin := Vector2i(index % (source.get_width() / 256), index / (source.get_width() / 256)) * 256
				var box := Rect2i(int(bounds[0]), int(bounds[1]), int(bounds[2]) - int(bounds[0]), int(bounds[3]) - int(bounds[1]))
				if kind == "party":
					# Garment's waist is 55% down the cutout. Align neckline and waist;
					# short petal peplum covers only the upper tail, never the fin.
					var width: int = maxi(28, roundi(box.size.x * 1.7))
					var height: int = maxi(48, roundi(box.size.y * 1.42))
					var placement := Vector2i(box.get_center().x - width / 2, box.position.y - 2) + origin
					var cloth := garment.duplicate() as Image
					cloth.resize(width, height, Image.INTERPOLATE_LANCZOS)
					output.blend_rect(cloth, Rect2i(0, 0, width, height), placement)
					# Original hands/skin cross in front of the clothing. Keep their pixels.
					for y: int in range(maxi(0, placement.y), mini(source.get_height(), placement.y + height)):
						for x: int in range(maxi(0, placement.x), mini(source.get_width(), placement.x + width)):
							var pixel: Color = source.get_pixel(x, y)
							if pixel.a > 0.02 and pixel.r > pixel.b + 0.09 and pixel.g > pixel.b + 0.025:
								output.set_pixel(x, y, pixel)
				else:
					if kind in ["garden", "disguise"]:
						# Recolour clothing pixels only; source contours and shading remain.
						for y: int in range(box.position.y, box.end.y):
							for x: int in range(box.position.x, box.end.x):
								var pixel: Color = source.get_pixelv(origin + Vector2i(x, y))
								if pixel.a > 0.1 and pixel.r > 0.54 and pixel.b > 0.49 and pixel.b > pixel.g * 1.11 and pixel.r > pixel.b * 0.99:
									output.set_pixelv(origin + Vector2i(x, y), Color(pixel.g * 0.72, pixel.r * 0.94, pixel.b * 0.74, pixel.a))
					var bow := _bow(kind)
					bow.resize(26 if kind != "disguise" else 38, 16 if kind != "disguise" else 23, Image.INTERPOLATE_LANCZOS)
					output.blend_rect(bow, Rect2i(Vector2i.ZERO, bow.get_size()), origin + Vector2i(box.get_center().x - bow.get_width() / 2, box.position.y + 3))
			output.save_png(out_dir + base + "_" + kind + ".png")
	if not game_outputs:
		print("FASHION_ASSETS|OK|%d clip sources x 4 outfits -> %s" % [fit["sources"].size(), out_dir])
		quit()
		return
	for base: String in OTHER:
		var spec: Array = OTHER[base]
		var source: Image = Image.load_from_file(String(spec[0]))
		source.convert(Image.FORMAT_RGBA8)
		for kind: String in ["ribbon", "party", "garden"]:
			var output := source.duplicate() as Image
			var cells: Array = spec[3] as Array
			var columns: int = source.get_width() / int(spec[1])
			for index: int in range(cells.size()):
				var center: Array = cells[index] as Array
				var origin := Vector2i(index % columns * int(spec[1]), index / columns * int(spec[2]))
				var width: int = (34 if base.begins_with("rumi") else 44) if int(spec[1]) <= 290 else 92
				var bow := _bow(kind)
				bow.resize(width, roundi(width * 0.6), Image.INTERPOLATE_LANCZOS)
				output.blend_rect(bow, Rect2i(Vector2i.ZERO, bow.get_size()), origin + Vector2i(int(center[0]) - width / 2, int(center[1]) - bow.get_height() / 2))
			output.save_png(OUT + base + "_" + kind + ".png")
	print("FASHION_ASSETS|OK|55 clothing atlases; original sources preserved")
	quit()

func _bow(kind: String) -> Image:
	var image := Image.create(120, 72, false, Image.FORMAT_RGBA8)
	var ink := Color("413653")
	var fill := Color("bda1ef") if kind == "ribbon" else (Color("efaaa1") if kind == "party" else Color("a2d7aa"))
	var left := PackedVector2Array([Vector2(6, 5), Vector2(60, 30), Vector2(7, 62)])
	var right := PackedVector2Array([Vector2(114, 5), Vector2(60, 30), Vector2(113, 62)])
	for y: int in range(72):
		for x: int in range(120):
			var point := Vector2(x, y)
			var in_wing: bool = Geometry2D.is_point_in_polygon(point, left) or Geometry2D.is_point_in_polygon(point, right)
			var inner := (point - Vector2(60, 33)) * 1.18 + Vector2(60, 33)
			var in_inner: bool = Geometry2D.is_point_in_polygon(inner, left) or Geometry2D.is_point_in_polygon(inner, right)
			if in_wing:
				image.set_pixel(x, y, fill.lightened(0.15 * (1.0 - y / 72.0)) if in_inner else ink)
			var knot: float = pow((x - 60.0) / 13.0, 2) + pow((y - 33.0) / 18.0, 2)
			if knot <= 1.0:
				image.set_pixel(x, y, Color("fff0ac") if knot < 0.6 else ink)
	return image
