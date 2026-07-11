extends SceneTree
# Skin audit: every wardrobe skin binds a live 26-bone skeleton (the V2
# bodies are canonical — the plushie era must stay gone), the fairy carries
# wing bones + wing cards, and the fairy-flight force/restore path returns
# to the skin SHE chose (playtest: some games reverted her to the old look).
func _init() -> void:
	var ps: PackedScene = load("res://scenes/main.tscn")
	root.add_child(ps.instantiate())
	await process_frame
	await process_frame
	var main: Node = root.get_child(root.get_child_count() - 1)
	if main.has_method("_skip_intro"):
		main._skip_intro()
	for i in range(15):
		await process_frame
	var pl: Node = main.player
	for sid in ["classic", "fairy", "huluu", "pearl"]:
		pl.set_skin(sid, "")
		for i in range(5):
			await process_frame
		if pl.skel == null:
			print("FAIL: skin ", sid, " has no live skeleton")
			continue
		if pl.bone_idx.get("tail4", -1) < 0:
			print("FAIL: skin ", sid, " missing tail bones (not a rigged body)")
		if sid == "fairy":
			if pl.skel.find_bone("wingL") < 0:
				print("FAIL: fairy skin has no wing bones (old plushie loaded?)")
			var cards := 0
			for att in pl.skel.get_children():
				if att is BoneAttachment3D:
					cards += 1
			if cards < 2:
				print("FAIL: fairy wing cards missing (", cards, "/2)")
	# the fairy-flight force/restore round trip must come back to HER choice
	main.skin_id = "huluu"
	main._apply_skin()
	for i in range(3):
		await process_frame
	pl.set_skin("fairy", main.FAIRY_SKIN_PATH)
	for i in range(3):
		await process_frame
	main._apply_skin()
	for i in range(3):
		await process_frame
	if String(pl.skin_id) != "huluu":
		print("FAIL: skin reverted after forced-skin game (now: ", pl.skin_id, ")")
	else:
		print("skin round-trip ok (huluu kept through forced fairy)")
	print("skin audit complete")
	quit()
