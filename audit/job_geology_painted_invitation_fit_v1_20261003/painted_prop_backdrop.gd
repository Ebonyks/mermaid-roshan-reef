extends OperaWorldBackdrop2D
## NON-RUNTIME COUNTERFACTUAL PROP FIT. Source and production owners unchanged.

func _load_geology_props() -> void:
	super._load_geology_props()
	for entry: Array in [["fossil", "fossil.png", Rect2(115,171,802,674)],
		["mineral", "mineral.png", Rect2(231,130,569,767)]]:
		var atlas := AtlasTexture.new()
		atlas.atlas = load(GEOLOGY_WORK_ART + String(entry[1])) as Texture2D
		atlas.region = entry[2] as Rect2
		atlas.filter_clip = true
		geology_props[String(entry[0])] = atlas
	var tray := AtlasTexture.new()
	tray.atlas = ImageTexture.create_from_image(Image.load_from_file("res://assets_src/imagegen/geologist_specimen_tray_v1_20261003/attempt01/native.png"))
	tray.region = Rect2(8,378,1239,555)
	tray.filter_clip = true
	geology_props["tray"] = tray

func _draw_geologist(mid: Color, _accent: Color) -> void:
	# Existing wall bands retained verbatim: this study does not pass the room.
	for band in range(5):
		var y := 150.0 + float(band) * 74.0
		var color := mid.lightened(0.18 - float(band) * 0.055)
		draw_polyline(PackedVector2Array([Vector2(0,y+24),Vector2(220,y-12),
			Vector2(470,y+18),Vector2(760,y-18),Vector2(1040,y+12),Vector2(1280,y-10)]),color,34.0)
	if stage_mode:
		_draw_geology_prop("slab", GEOLOGY_CELEBRATION_SLAB)
		return
	if bool(get_meta("geology_work_open", false)):
		return
	_draw_geology_prop("slab",Rect2(355,580,180,180.0*369.0/889.0))
	_draw_geology_prop("fossil",Rect2(383,543,105,105.0*674.0/802.0))
	var tray: Texture2D = geology_props["tray"] as Texture2D
	var tray_height := 110.0*tray.get_height()/float(tray.get_width())
	for index in range(3):
		_draw_geology_prop("slab",Rect2(535.0+float(index)*145.0,603,140,140.0*369.0/889.0))
		_draw_geology_prop("tray",Rect2(550.0+float(index)*145.0,625.0-tray_height,110,tray_height))
	_draw_geology_prop("mineral",Rect2(1090,545,130.0*569.0/767.0,130))
