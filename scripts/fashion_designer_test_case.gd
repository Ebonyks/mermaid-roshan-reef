class_name FashionDesignerTestCase
extends RefCounted
## Run inside the trusted UI probe, whose user-data directory is isolated.
static func run(main: ReefMain, check: Callable) -> void:
	var voice_manifest: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://assets/audio/fashion/FASHION_VOICE_MANIFEST.json")) as Dictionary
	var voice_entries: Array = voice_manifest.get("entries", []) as Array
	check.call(voice_entries.size() == 11, "Fashion ships all eleven exact provisional instructions")
	for entry: Dictionary in voice_entries:
		var cue: String = String(entry["key"]).trim_prefix("roshan_")
		var path: String = main._audio_ref()._voice_path("roshan", cue, false)
		check.call(not path.is_empty() and FileAccess.get_sha256(path) == String(entry["final_ogg_sha256"]),
			"Fashion exact audio hash and route: " + cue)
	var old_outfits: Dictionary = main.character_outfits.duplicate(true)
	var old_parts: Dictionary = main.character_clothing_parts.duplicate(true)
	var old_unlocked: Dictionary = main.outfits_unlocked.duplicate(true)
	var old_progress: Dictionary = main.fashion_disguise_progress.duplicate(true)
	var old_dressing: Dictionary = main.fashion_dressing_progress.duplicate(true)
	var old_rewards: Dictionary = main.fashion_rewards_claimed.duplicate(true)
	var old_dress: bool = main.chapter2_party_dress_done
	var old_complete: bool = main.chapter2_story_complete
	var old_skin: String = main.skin_id
	main.character_outfits = {}
	main.character_clothing_parts = {}
	main.outfits_unlocked = {}
	main.fashion_disguise_progress = {}
	main.fashion_dressing_progress = {}
	main.fashion_rewards_claimed = {}
	main.chapter2_party_dress_done = false
	var patch: Dictionary = FashionDesigner.normalise_save_patch({
		"character_outfits": {"future_friend": "future_outfit", "roshan": "future_dress"},
		"outfits_unlocked": {"future_unlock": {"future_data": 19}},
		"fashion_disguise_progress": [], "chapter2_party_dress_done": "yes"})
	check.call(patch["character_outfits"]["future_friend"] == "future_outfit"
		and patch["outfits_unlocked"]["future_unlock"]["future_data"] == 19
		and patch["fashion_disguise_progress"].is_empty()
		and not patch["chapter2_party_dress_done"], "Fashion save defaults preserve future IDs and reject malformed containers")
	main.character_outfits = patch["character_outfits"]
	check.call(FashionDesigner.selected(main, "roshan") == "roshan_original"
		and main.character_outfits["roshan"] == "future_dress", "Unknown outfit presents original without erasing future selection")
	check.call(not FashionDesigner.equip(main, "roshan", "roshan_ribbon_v1")
		and not FashionDesigner.equip(main, "roshan", FashionDesigner.PARTY_DRESS, true), "Passive and locked choices cannot equip or advance")
	check.call(FashionDesigner.grant(main, FashionDesigner.PARTY_DRESS)
		and not FashionDesigner.grant(main, FashionDesigner.PARTY_DRESS)
		and main.character_outfits["roshan"] == "future_dress", "Outfit rewards are permanent and idempotent without auto equip")
	main.character_outfits["roshan"] = FashionDesigner.PARTY_DRESS
	main.chapter2_party_dress_done = true
	main.skin_id = "fairy"
	check.call(not FashionDesigner.party_dressed(main),
		"A legacy full-character skin cannot bypass wearing the special party dress")
	main.chapter2_party_dress_done = false
	check.call(FashionDesigner.equip(main, "baby_eagle", "baby_eagle_ribbon_v1", true)
		and FashionDesigner.equip(main, "roshan", "roshan_ribbon_v1", true), "Two recurring characters keep independent intentional choices")
	check.call(main.save_data.get("character_outfits", {}).get("baby_eagle", "") == "baby_eagle_ribbon_v1"
		and main.save_data.get("character_outfits", {}).get("roshan", "") == "roshan_ribbon_v1", "Outfit choices reach the transactional save immediately")
	var previous_companion = main.companion_node
	var previous_companion_id: String = main.companion_id
	main.companion_id = "eagle"
	main.companion_node = main._companion_ref().make_creature()
	FashionDesigner.equip(main, "baby_eagle", "baby_eagle_original", true)
	var live_picture: Node = main.companion_node.get_node("StorybookBob/StorybookSprite")
	var live_texture: Texture2D = live_picture.get("texture") as Texture2D
	check.call(live_texture.resource_path.ends_with("companions/baby_eagle.png"),
		"Already spawned companion receives a changed outfit immediately")
	FashionDesigner.equip(main, "baby_eagle", "baby_eagle_ribbon_v1", true)
	main.companion_node.free()
	main.companion_node = previous_companion
	main.companion_id = previous_companion_id
	var wardrobe := FashionWardrobe.new(main)
	wardrobe.open()
	var layers: CanvasLayer = main.wardrobe_layer
	check.call(layers.find_children("FashionCharacter_*", "Button", true, false).size() == 3,
		"Fashion wardrobe exposes the three mermaids with pictured selectors")
	for node: Node in layers.find_children("Fashion*", "Button", true, false):
		var control := node as Control
		check.call(control.size.x >= 110 and control.size.y >= 110,
			"Fashion picture targets remain thumb sized: " + String(control.name))
	var before: Dictionary = main.character_outfits.duplicate(true)
	main._wardrobe_ref()._close_wardrobe()
	check.call(main.character_outfits == before, "Global Back retains applied outfits")
	main.chapter2_story_complete = true
	FashionDesigner.refresh_unlocks(main)
	FashionDesigner.grant(main, "roshan_garden_v1")
	FashionDesigner.refresh_unlocks(main)
	check.call(not FashionDesigner.complete_disguise_phase(main, 0, "roshan_garden_v1")
		and not FashionDesigner.complete_disguise_phase(main, 0, "roshan_ribbon_v1", true)
		and FashionDesigner.next_disguise_phase(main) == 0, "Disguise play needs a matching intentional choice")
	check.call(FashionDesigner.complete_disguise_phase(main, 0, "roshan_garden_v1", true)
		and FashionDesigner.next_disguise_phase(main) == 1, "Disguise partial progress saves after first pictured role")
	var saved: Dictionary = main.save_data.duplicate(true)
	main.character_outfits = {}
	main.character_clothing_parts = {}
	FashionDesigner.restore(main, saved)
	check.call(FashionDesigner.selected(main, "baby_eagle") == "baby_eagle_ribbon_v1"
		and FashionDesigner.selected(main, "roshan") == "roshan_garden_v1", "Save restore keeps two independent character outfits")
	var resumed: Dictionary = main._save_state._normalise_save(main.save_data)
	main.fashion_disguise_progress = {}
	FashionDesigner.restore(main, resumed)
	check.call(FashionDesigner.next_disguise_phase(main) == 1, "Disguise re-entry restores the next unfinished phase")
	main.fashion_disguise_progress["completed_mask"] = 9.0
	check.call(FashionDesigner.complete_disguise_phase(main, 1, "tail_strawberry_v1", true)
		and int(main.fashion_disguise_progress["completed_mask"]) == 11,
		"JSON numeric progress preserves future high bits while completing a known beat")
	main.fashion_disguise_progress["completed_mask"] = 1
	check.call(FashionDesigner.complete_disguise_phase(main, 1, "tail_strawberry_v1", true)
		and FashionDesigner.complete_disguise_phase(main, 2, "finish_bow", true)
		and not FashionDesigner.complete_disguise_phase(main, 2, "finish_bow", true)
		and main.fashion_rewards_claimed.get("garden_disguise_v1", false), "Disguise reward happens once after three intentional beats")
	check.call(FashionOutfitRenderer.path(main, String(FashionDesigner.character("baby_eagle")["source"]))
		.ends_with("baby_eagle_ribbon.png"), "Recurring Baby Eagle uses its saved wardrobe texture")
	var detached_actor := Sprite2D.new()
	var pose_loop := RoshanSpriteLoop.new()
	pose_loop.wardrobe_owner = main
	detached_actor.add_child(pose_loop)
	pose_loop.setup_sprite_2d(detached_actor)
	check.call(detached_actor.texture.resource_path.begins_with("res://assets/fashion/slots_v1/cache/roshan_directional/") and FashionParts.selected(main,"roshan","head") == "head_pearl_v1" and FashionParts.selected(main,"roshan","tail") == "tail_strawberry_v1",
		"Scene builders carry saved clothes before the actor enters the tree")
	detached_actor.free()
	main.character_outfits = old_outfits
	main.character_clothing_parts = old_parts
	main.outfits_unlocked = old_unlocked
	main.fashion_disguise_progress = old_progress
	main.fashion_dressing_progress = old_dressing
	main.fashion_rewards_claimed = old_rewards
	main.chapter2_party_dress_done = old_dress
	main.chapter2_story_complete = old_complete
	main.skin_id = old_skin
	main._apply_skin()
	main._write_save()
