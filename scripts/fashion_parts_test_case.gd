class_name FashionPartsTestCase
extends RefCounted
## Trusted UI probe extension: real GUI slot actions plus actual transactional reload.
static func run(main: ReefMain, check: Callable) -> void:
	var old_outfits: Dictionary = main.character_outfits.duplicate(true)
	var old_parts: Dictionary = main.character_clothing_parts.duplicate(true)
	var old_dressing: Dictionary = main.fashion_dressing_progress.duplicate(true)
	var old_skin: String = main.skin_id
	var old_complete: bool = main.chapter2_story_complete
	var old_progress: Dictionary = main.fashion_disguise_progress.duplicate(true)
	var old_rewards: Dictionary = main.fashion_rewards_claimed.duplicate(true)
	var old_unlocked: Dictionary = main.outfits_unlocked.duplicate(true)
	main.character_outfits = {}
	main.character_clothing_parts = {"future_person":{"future_slot":"future_piece"}}
	main.fashion_dressing_progress = {}
	main.skin_id = "classic"
	var wardrobe := FashionWardrobe.new(main)
	wardrobe.open()
	await main.get_tree().process_frame
	check.call(main.wardrobe_layer.find_child("FashionHelp",true,false) == null and main.wardrobe_layer.find_children("FashionSlot_*","Button",true,false).size() == 3,
		"Wardrobe has exactly three pictured slots and no ambiguous question mark")
	for person: String in FashionParts.PEOPLE:
		await FashionSkinEngineTestCase._tap(main,main.wardrobe_layer.find_child("FashionCharacter_"+person,true,false) as Control)
		var before: Dictionary = FashionParts.selections(main,person)
		await FashionSkinEngineTestCase._tap(main,main.wardrobe_layer.find_child("FashionSlot_head",true,false) as Control)
		check.call(FashionParts.selections(main,person) == before,"Selecting a slot never equips: "+person)
		await FashionSkinEngineTestCase._tap(main,main.wardrobe_layer.find_child("FashionOutfit_head_royal_v1",true,false) as Control)
		await FashionSkinEngineTestCase._tap(main,main.wardrobe_layer.find_child("FashionSlot_body",true,false) as Control)
		await FashionSkinEngineTestCase._tap(main,main.wardrobe_layer.find_child("FashionOutfit_"+person+"_ribbon_v1",true,false) as Control)
		await FashionSkinEngineTestCase._tap(main,main.wardrobe_layer.find_child("FashionSlot_tail",true,false) as Control)
		await FashionSkinEngineTestCase._tap(main,main.wardrobe_layer.find_child("FashionOutfit_tail_star_v1",true,false) as Control)
		var parts: Dictionary = FashionParts.selections(main,person)
		check.call(parts["head"] == "head_royal_v1" and parts["body"] == person+"_ribbon_v1" and parts["tail"] == "tail_star_v1",
			"Real GUI head/body/tail choices stay independent: "+person)
		var selector: Button = main.wardrobe_layer.find_child("FashionCharacter_"+person,true,false) as Button
		check.call(selector.modulate == Color.WHITE and main.wardrobe_layer.find_children("FashionCurrentLook","TextureRect",true,false).size() == 1,
			"One clean preview and untinted character selector: "+person)
		var texture: Texture2D = FashionOutfitRenderer.portrait(main,person)
		check.call(texture != null and (texture is AtlasTexture or texture is ImageTexture),"Shared Godot composite reaches the portrait: "+person)
	# A private live animation keeps all its real playback state during every slot swap.
	var atlas := AtlasTexture.new()
	atlas.atlas = load("res://assets/characters/roshan_25d/roshan_directional.png") as Texture2D
	atlas.region = Rect2(256,0,256,256)
	atlas.margin = Rect2(3,4,5,6)
	atlas.filter_clip = true
	var original := SpriteFrames.new()
	original.set_animation_speed("default",7.5)
	original.set_animation_loop("default",false)
	original.add_frame("default",atlas,0.75)
	original.add_frame("default",atlas,1.25)
	var actor := AnimatedSprite2D.new()
	actor.sprite_frames = FashionSkinEngine.animation_frames(main,original)
	main.add_child(actor)
	for state: Dictionary in [{"paused":false,"speed":1.3,"custom":-0.75},{"paused":true,"speed":0.8,"custom":2.0},{"paused":false,"speed":0.0,"custom":0.6}]:
		for id: String in ["head_pearl_v1","body_star_v1","tail_blossom_v1"]:
			actor.speed_scale = float(state["speed"])
			actor.play("default",float(state["custom"]))
			if bool(state["paused"]): actor.pause()
			actor.set_frame_and_progress(1,0.37)
			var playing: bool = actor.is_playing()
			var speed: float = actor.get_playing_speed()
			var bound: SpriteFrames = actor.sprite_frames
			FashionDesigner.equip(main,"roshan",id,true)
			var frame: AtlasTexture = actor.sprite_frames.get_frame_texture("default",1) as AtlasTexture
			check.call(actor.sprite_frames == bound and actor.frame == 1 and is_equal_approx(actor.frame_progress,0.37) and actor.is_playing() == playing and is_equal_approx(actor.get_playing_speed(),speed) and frame.region == atlas.region and frame.margin == atlas.margin and frame.filter_clip == atlas.filter_clip and bound.get_frame_duration("default",1) == 1.25,
				"Independent slot preserves real animation state: "+id+str(state))
	check.call(original.get_frame_texture("default",1) == atlas and atlas.atlas.resource_path.ends_with("roshan_directional.png"),"Mixed slots never mutate original animation resources")
	var first: Texture2D = FashionSkinEngine.texture(main,atlas.atlas)
	var path_before_goal: String = first.resource_path
	FashionParts.goal(main,"roshan",FashionParts.selections(main,"roshan"))
	check.call(first.resource_path == path_before_goal and not path_before_goal.is_empty() and ResourceLoader.exists(path_before_goal),"Identical goal preview never steals the live mixed texture path")
	var again: Texture2D = FashionSkinEngine.texture(main,atlas.atlas)
	check.call(first == again,"Repeated sampling reuses one composed texture")
	for index: int in range(6):
		FashionDesigner.equip(main,"roshan","tail_star_v1" if index%2 == 0 else "tail_blossom_v1",true)
	check.call(main.fashion_composed_textures.size() <= 26,"Mix cache is bounded by source families, never outfit combinations")
	actor.queue_free()
	main._wardrobe_ref()._close_wardrobe()
	(main.character_clothing_parts["rumi"] as Dictionary)["future_slot"] = {"future_data":17}
	(main.character_clothing_parts["daddy_mermaid"] as Dictionary)["head"] = "future_hat"
	main._write_save()
	var saved: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(ReefMain.SAVE_PATH)) as Dictionary
	var expected: Dictionary = JSON.parse_string(JSON.stringify(main.character_clothing_parts)) as Dictionary # JSON numbers restore as floats.
	main.character_clothing_parts = {}
	FashionDesigner.restore(main,saved)
	check.call(main.character_clothing_parts == expected and FashionParts.selected(main,"daddy_mermaid","head") == "head_original" and main.character_clothing_parts["daddy_mermaid"]["head"] == "future_hat",
		"Disk reload preserves independent pieces, future IDs, fields and characters")
	wardrobe.open()
	await main.get_tree().process_frame
	check.call(FashionParts.selected(main,"roshan","head") == "head_pearl_v1" and FashionParts.selected(main,"roshan","body") == "body_star_v1" and FashionParts.selected(main,"roshan","tail") == "tail_blossom_v1",
		"Leaving, reloading and reopening retains a mixed outfit")
	main._wardrobe_ref()._close_wardrobe()
	main.chapter2_story_complete = true # Explicit availability fixture, not earned route evidence.
	main.fashion_disguise_progress = {}
	FashionDesigner.grant(main,"roshan_garden_v1")
	FashionDesigner.refresh_unlocks(main)
	wardrobe.open()
	await main.get_tree().process_frame
	await FashionSkinEngineTestCase._tap(main,main.wardrobe_layer.find_child("FashionDisguisePlay",true,false) as Control)
	var goal_piece: TextureRect = main.wardrobe_layer.find_child("FashionGoalPiece",true,false) as TextureRect
	check.call(goal_piece.size == Vector2(160,184),"Practice goal respects its layout bounds after texture assignment")
	await FashionSkinEngineTestCase._tap(main,main.wardrobe_layer.find_child("FashionOutfit_roshan_ribbon_v1",true,false) as Control)
	check.call(FashionDesigner.next_disguise_phase(main) == 0,"Wrong disguise body is kind and awards no phase")
	await FashionSkinEngineTestCase._tap(main,main.wardrobe_layer.find_child("FashionOutfit_roshan_garden_v1",true,false) as Control)
	check.call(FashionDesigner.next_disguise_phase(main) == 1,"Real GUI practice fits its pictured body")
	await FashionSkinEngineTestCase._tap(main,main.wardrobe_layer.find_child("FashionOutfit_tail_star_v1",true,false) as Control)
	check.call(FashionDesigner.next_disguise_phase(main) == 1,"Wrong disguise tail preserves the unfinished phase")
	await FashionSkinEngineTestCase._tap(main,main.wardrobe_layer.find_child("FashionOutfit_tail_strawberry_v1",true,false) as Control)
	await FashionSkinEngineTestCase._tap(main,main.wardrobe_layer.find_child("FashionOutfit_finish_bow",true,false) as Control)
	check.call(FashionDesigner.next_disguise_phase(main) == 3 and FashionParts.selected(main,"roshan","body") == "roshan_garden_v1" and FashionParts.selected(main,"roshan","tail") == "tail_strawberry_v1" and FashionParts.selected(main,"roshan","head") == "head_pearl_v1" and bool(main.fashion_rewards_claimed.get("garden_disguise_v1",false)),
		"Real GUI disguise practice completes body/tail/head with a persistent mixed outfit")
	main._wardrobe_ref()._close_wardrobe()
	main.chapter2_story_complete = old_complete
	main.fashion_disguise_progress = old_progress
	main.fashion_rewards_claimed = old_rewards
	main.outfits_unlocked = old_unlocked
	main.character_outfits = old_outfits
	main.character_clothing_parts = old_parts
	main.fashion_dressing_progress = old_dressing
	main.skin_id = old_skin
	FashionSkinEngine.refresh(main)
	main._write_save()
