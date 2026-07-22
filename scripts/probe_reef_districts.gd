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
	_check("two ocean kingdoms", ReefDistricts.KINGDOM_BY_REGION.values().has(ReefDistricts.KINGDOM_CARIBBEAN)
		and ReefDistricts.KINGDOM_BY_REGION.values().has(ReefDistricts.KINGDOM_NORWEGIAN))
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
	_check("Caribbean owns warm reef districts",
		ReefDistricts.kingdom_at(Vector2(35, 30)) == ReefDistricts.KINGDOM_CARIBBEAN
		and ReefDistricts.kingdom_at(Vector2(-160, 135)) == ReefDistricts.KINGDOM_CARIBBEAN
		and ReefDistricts.kingdom_at(Vector2(-165, 5)) == ReefDistricts.KINGDOM_CARIBBEAN
		and ReefDistricts.kingdom_at(Vector2(-40, -165)) == ReefDistricts.KINGDOM_CARIBBEAN)
	_check("Norway owns kelp and ice districts",
		ReefDistricts.kingdom_at(Vector2(-35, 165)) == ReefDistricts.KINGDOM_NORWEGIAN
		and ReefDistricts.kingdom_at(Vector2(140, -115)) == ReefDistricts.KINGDOM_NORWEGIAN)
	_check("kelp scatter stays in kelp district",
		ReefDistricts.habitat_point_allowed("kelp", Vector2(-35, 165))
		and not ReefDistricts.habitat_point_allowed("kelp", Vector2(140, -115)))
	_check("cold-water flora stays in ice district",
		ReefDistricts.habitat_point_allowed("ice", Vector2(140, -115))
		and not ReefDistricts.habitat_point_allowed("ice", Vector2(-165, 5)))
	_check("mass warm scatter rejects both Norwegian districts",
		ReefDistricts.habitat_point_allowed("mixed", Vector2(35, 30))
		and not ReefDistricts.habitat_point_allowed("mixed", Vector2(-35, 165))
		and not ReefDistricts.habitat_point_allowed("mixed", Vector2(140, -115)))
	var norwegian_flora_clean := true
	for forbidden_value: Variant in ReefDistricts.FORBIDDEN_NORWEGIAN_FLORA:
		for benthos_value: Variant in ReefDistricts.COLD_WATER_BENTHOS:
			if String(benthos_value).contains(String(forbidden_value)):
				norwegian_flora_clean = false
	_check("Norwegian benthos excludes tropical tokens", norwegian_flora_clean)
	_check("species use compatible districts",
		ReefDistricts.habitat_point_allowed("starfish", Vector2(-40, -165))
		and ReefDistricts.habitat_point_allowed("urchin", Vector2(-160, 135))
		and not ReefDistricts.habitat_point_allowed("anemone", Vector2(-40, -165)))
	_check("friend and portal gateways stay clear",
		not ReefDistricts.habitat_point_allowed("starfish", ReefDistricts.FRIEND_POSITIONS[0] as Vector2)
		and not ReefDistricts.habitat_point_allowed("starfish", Vector2(-5, -95))
		and not ReefDistricts.habitat_point_allowed("mixed",
			ReefDistricts.kingdom_return_gate(ReefDistricts.KINGDOM_CARIBBEAN))
		and not ReefDistricts.habitat_point_allowed("kelp",
			ReefDistricts.kingdom_return_gate(ReefDistricts.KINGDOM_NORWEGIAN)))
	_check("hub flattened", ReefDistricts.shape_terrain(0.0, 0.0, 20.0) < 6.0)
	_check("Faron approach flattened", ReefDistricts.shape_terrain(-72.0, 8.0, 20.0) < 2.0)
	_check("race flat flattened", ReefDistricts.shape_terrain(-40.0, -165.0, 20.0) < 8.0)
	_check("wreck ravine carved", ReefDistricts.shape_terrain(-160.0, 135.0, 0.0) < -8.0)
	_check("moon bowl carved", ReefDistricts.shape_terrain(-165.0, 5.0, 0.0) < -6.0)
	_check("kelp ridge raised", ReefDistricts.shape_terrain(-78.0, 175.0, 0.0) > 7.0)
	_check("seven Blender regional assets", ReefDistricts.REGIONAL_SCENES.size() == 7)
	for key: String in ReefDistricts.REGIONAL_SCENES:
		_check("regional asset %s exists" % key, ResourceLoader.exists(String(ReefDistricts.REGIONAL_SCENES[key])))
	print("REEFDISTRICT|RESULT|", "PASS" if ok else "FAIL")
	quit(0 if ok else 1)
