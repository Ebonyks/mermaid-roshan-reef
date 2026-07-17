extends SceneTree

var ok := true

func _check(label: String, condition: bool) -> void:
	print("REEFDISTRICT|", label, "|", "OK" if condition else "FAIL")
	if not condition:
		ok = false

func _init() -> void:
	_check("six district centers", ReefDistricts.REGION_CENTERS.size() == 6)
	_check("authored grove count", ReefDistricts.GROVES.size() == 14)
	_check("district centers have neutral buffers", ReefDistricts.minimum_center_separation() >= 125.0)
	_check("Faron is within a short swim", ReefDistricts.friend_position(2).length() <= 75.0)
	for i in range(ReefDistricts.FRIEND_POSITIONS.size()):
		_check("friend %d is reachable" % i, (ReefDistricts.FRIEND_POSITIONS[i] as Vector2).length() <= 95.0)
	_check("six regional object signatures", ReefDistricts.REGION_SIGNATURES.size() == 6)
	for key: String in ReefDistricts.REGION_SIGNATURES:
		_check("%s has three object families" % key, (ReefDistricts.REGION_SIGNATURES[key] as Array).size() >= 3)
	var kinds := {}
	for value: Dictionary in ReefDistricts.GROVES:
		kinds[String(value["kind"])] = true
	_check("all grove identities", kinds.size() == 6)
	_check("pearl region", ReefDistricts.region_at(Vector2(5, 8)) == "pearl")
	_check("kelp region", ReefDistricts.region_at(Vector2(-35, 165)) == "kelp")
	_check("wreck region", ReefDistricts.region_at(Vector2(-160, 135)) == "wreck")
	_check("moon region", ReefDistricts.region_at(Vector2(-165, 5)) == "moon")
	_check("rainbow region", ReefDistricts.region_at(Vector2(-40, -165)) == "rainbow")
	_check("ice region", ReefDistricts.region_at(Vector2(140, -115)) == "ice")
	_check("hub flattened", ReefDistricts.shape_terrain(0.0, 0.0, 20.0) < 6.0)
	_check("Faron approach flattened", ReefDistricts.shape_terrain(-72.0, 8.0, 20.0) < 2.0)
	_check("race flat flattened", ReefDistricts.shape_terrain(-40.0, -165.0, 20.0) < 8.0)
	_check("wreck ravine carved", ReefDistricts.shape_terrain(-160.0, 135.0, 0.0) < -8.0)
	_check("moon bowl carved", ReefDistricts.shape_terrain(-165.0, 5.0, 0.0) < -6.0)
	_check("kelp ridge raised", ReefDistricts.shape_terrain(-78.0, 175.0, 0.0) > 7.0)
	for key: String in ReefDistricts.STRUCTURE_SCENES:
		_check("structure %s exists" % key, ResourceLoader.exists(String(ReefDistricts.STRUCTURE_SCENES[key])))
	_check("six Blender regional assets", ReefDistricts.REGIONAL_SCENES.size() == 6)
	for key: String in ReefDistricts.REGIONAL_SCENES:
		_check("regional asset %s exists" % key, ResourceLoader.exists(String(ReefDistricts.REGIONAL_SCENES[key])))
	print("REEFDISTRICT|RESULT|", "PASS" if ok else "FAIL")
	quit(0 if ok else 1)
