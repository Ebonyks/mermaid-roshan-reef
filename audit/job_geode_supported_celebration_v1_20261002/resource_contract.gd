extends SceneTree

func _initialize() -> void:
	var backdrop := OperaWorldBackdrop2D.new()
	backdrop.setup("geologist")
	assert(backdrop.geology_props.size() == 1)
	var goal := load("res://assets/opera/worlds/geology/coherent_geode_v1_20261002/open_geode.tres") as AtlasTexture
	var destination := OperaWorldBackdrop2D.geology_celebration_goal_rect(goal)
	var height := destination.size.x * goal.get_height() / float(goal.get_width())
	var bottom := destination.position.y + (destination.size.y + height) * 0.5
	assert(is_equal_approx(bottom, OperaWorldBackdrop2D.GEOLOGY_CELEBRATION_CONTACT.y))
	for key: String in backdrop.geology_props:
		var texture: AtlasTexture = backdrop.geology_props[key] as AtlasTexture
		assert(texture.filter_clip)
		assert(texture.atlas == load(texture.atlas.resource_path))
	backdrop.free()
	print("SUPPORTED_GEODE_RESOURCE_CONTRACT|PASS|ONE_SHARED_PAINTED_SLAB_AND_GEODE_BASE_CONTACT")
	quit(0)
