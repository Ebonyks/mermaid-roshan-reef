extends SceneTree

var ok := true

func _check(label: String, condition: bool) -> void:
	print("REEFDISTRICT|", label, "|", "OK" if condition else "FAIL")
	if not condition:
		ok = false

func _init() -> void:
	_check("six district centers", ReefDistricts.REGION_CENTERS.size() == 6)
	_check("authored grove count", ReefDistricts.GROVES.size() == 18)
	_check("six regional object signatures", ReefDistricts.REGION_SIGNATURES.size() == 6)
	for key: String in ReefDistricts.REGION_SIGNATURES:
		_check("%s has three object families" % key, (ReefDistricts.REGION_SIGNATURES[key] as Array).size() >= 3)
	var kinds := {}
	for value: Dictionary in ReefDistricts.GROVES:
		kinds[String(value["kind"])] = true
	_check("all grove identities", kinds.size() == 6)
	_check("pearl region", ReefDistricts.region_at(Vector2(5, 8)) == "pearl")
	_check("kelp region", ReefDistricts.region_at(Vector2(-22, 116)) == "kelp")
	_check("wreck region", ReefDistricts.region_at(Vector2(-122, 100)) == "wreck")
	_check("moon region", ReefDistricts.region_at(Vector2(-124, 4)) == "moon")
	_check("rainbow region", ReefDistricts.region_at(Vector2(-12, -105)) == "rainbow")
	_check("ice region", ReefDistricts.region_at(Vector2(82, -60)) == "ice")
	_check("hub flattened", ReefDistricts.shape_terrain(0.0, 0.0, 20.0) < 6.0)
	_check("race flat flattened", ReefDistricts.shape_terrain(-12.0, -105.0, 20.0) < 7.0)
	_check("wreck ravine carved", ReefDistricts.shape_terrain(-122.0, 104.0, 0.0) < -8.0)
	_check("moon bowl carved", ReefDistricts.shape_terrain(-124.0, 4.0, 0.0) < -6.0)
	_check("kelp ridge raised", ReefDistricts.shape_terrain(-55.0, 132.0, 0.0) > 7.0)
	for key: String in ReefDistricts.STRUCTURE_SCENES:
		_check("structure %s exists" % key, ResourceLoader.exists(String(ReefDistricts.STRUCTURE_SCENES[key])))
	_check("six Blender regional assets", ReefDistricts.REGIONAL_SCENES.size() == 6)
	for key: String in ReefDistricts.REGIONAL_SCENES:
		_check("regional asset %s exists" % key, ResourceLoader.exists(String(ReefDistricts.REGIONAL_SCENES[key])))
	print("REEFDISTRICT|RESULT|", "PASS" if ok else "FAIL")
	quit(0 if ok else 1)
