extends SceneTree
# verifies a saved session restores trophies/stars on boot,
# and that a crafted fish survives a relaunch (it used to vanish: the save
# loads after the reef builds, so build-time spawning missed it)
func _init() -> void:
	var sd: Dictionary = {}
	if FileAccess.file_exists("user://reef_save.json"):
		var f := FileAccess.open("user://reef_save.json", FileAccess.READ)
		if f != null:
			var d: Variant = JSON.parse_string(f.get_as_text())
			if d is Dictionary:
				sd = d
	sd["custom_fish"] = [[0.9, 0.3, 0.3, 1.0, 0.8, 0.2]]   # one crafted fish in the save
	sd["animals"] = {"turtle": true}   # one tank friend already set free
	var w := FileAccess.open("user://reef_save.json", FileAccess.WRITE)
	w.store_string(JSON.stringify(sd))
	w.close()
	var ps: PackedScene = load("res://scenes/main.tscn")
	root.add_child(ps.instantiate())
	await process_frame
	await process_frame
	var main: Node = root.get_child(root.get_child_count() - 1)
	if main.has_method("_skip_intro"):
		main._skip_intro()
	await process_frame
	print("loaded trophies: ", main.trophies, "/5  finale_done: ", main.finale_done)
	var stars := 0
	for f in main.friends:
		if f.has("star"):
			stars += 1
	print("won stars shown: ", stars, "/5")
	var crafted := 0
	for mv in main.aquatic_movers:
		if bool(mv.get("crafted", false)):
			crafted += 1
	if crafted < 1:
		print("FAIL: crafted fish missing after reload (custom_fish in save, none swimming)")
	else:
		print("crafted fish restored: ", crafted)
	# a released tank friend must survive a relaunch (same build-before-load trap)
	var pets := 0
	for mv in main.aquatic_movers:
		if String(mv.get("shop_pet", "")) == "turtle":
			pets += 1
	if pets < 1:
		print("FAIL: shop animal missing after reload (animals.turtle in save, none swimming)")
	else:
		print("shop animals restored: ", pets)
	quit()
