class_name ComfyGames
extends RefCounted

## Optional, chapter-gated castle play that never owns story progression.
## Persistent state stays on ReefMain; this satellite owns policy and the
## lightweight, non-modal castle presentation.

const DAY_TWO_HIDE_AND_SEEK := "day2_castle_hide_and_seek"
const SUPER_SEEKER_STICKER := "super_seeker"
const STATE_VERSION := 1

const CHAPTER_GAMES: Dictionary = {
	2: [DAY_TWO_HIDE_AND_SEEK],
}

const FRIENDS: Array[Dictionary] = [
	{
		"id": "rumi",
		"name": "Rumi",
		"room": "mermaid_pool",
		"room_name": "Mermaid Pool",
		"texture": "res://assets/characters/rumi/rumi_eight_pose_runtime.png",
		"atlas_region": Rect2(512.0, 0.0, 256.0, 384.0),
		"rect": Rect2(930.0, 300.0, 220.0, 330.0),
		"line": "You found me by the sparkly pool!",
	},
	{
		"id": "baby_eagle",
		"name": "Baby Eagle",
		"room": "playroom",
		"room_name": "Playroom",
		"texture": "res://assets/book/baby_eagle.png",
		"rect": Rect2(830.0, 335.0, 235.0, 300.0),
		"line": "Chirp chirp! You found my hiding place!",
	},
	{
		"id": "daddy_mermaid",
		"name": "Daddy Mermaid",
		"room": "library",
		"room_name": "Library",
		"texture": "res://assets/characters/friends/daddy.webp",
		"rect": Rect2(95.0, 285.0, 230.0, 350.0),
		"line": "You found Daddy behind the storybooks!",
	},
]

var m: ReefMain
var castle_root: Control = null
var observed_room_id := ""
var observed_stage_instance_id := 0
var observed_day_two_available := false


func _init(main: ReefMain) -> void:
	m = main


static func normalise_save_patch(source: Dictionary) -> Dictionary:
	var raw_value: Variant = source.get("comfy_games", {})
	var raw: Dictionary = raw_value as Dictionary if raw_value is Dictionary else {}
	var hunt_value: Variant = raw.get(DAY_TWO_HIDE_AND_SEEK, {})
	var hunt_raw: Dictionary = hunt_value as Dictionary \
		if hunt_value is Dictionary else {}
	var found_value: Variant = hunt_raw.get("found", {})
	var found_raw: Dictionary = found_value as Dictionary \
		if found_value is Dictionary else {}
	var found: Dictionary = {}
	for friend: Dictionary in FRIENDS:
		var friend_id := String(friend["id"])
		found[friend_id] = bool(found_raw.get(friend_id, false)) \
			if typeof(found_raw.get(friend_id, false)) == TYPE_BOOL else false
	var complete_from_finds := true
	for friend_id_value: Variant in found:
		if not bool(found[friend_id_value]):
			complete_from_finds = false
			break
	var accepted_value: Variant = hunt_raw.get("accepted", false)
	var completed_value: Variant = hunt_raw.get("completed", false)
	return {
		"version": STATE_VERSION,
		DAY_TWO_HIDE_AND_SEEK: {
			"accepted": bool(accepted_value) \
				if typeof(accepted_value) == TYPE_BOOL else false,
			"found": found,
			"completed": complete_from_finds or (bool(completed_value) \
				if typeof(completed_value) == TYPE_BOOL else false),
		},
	}


func restore_state(source: Dictionary) -> void:
	m.comfy_games_state = normalise_save_patch(source)


func serialize_state() -> Dictionary:
	return {"comfy_games": normalise_save_patch({
		"comfy_games": m.comfy_games_state,
	})}


func unlocked_game_ids(chapter: int) -> Array[String]:
	var result: Array[String] = []
	for chapter_value: Variant in CHAPTER_GAMES:
		if int(chapter_value) > chapter:
			continue
		for game_id_value: Variant in CHAPTER_GAMES[chapter_value]:
			result.append(String(game_id_value))
	return result


func is_day_two_available() -> bool:
	return not m.day_one_is_active()


func tick_castle_room() -> void:
	var stage_instance_id := 0
	if m.castle_room_stage != null and is_instance_valid(m.castle_room_stage):
		stage_instance_id = m.castle_room_stage.get_instance_id()
	var available := is_day_two_available()
	if observed_room_id == m.castle_room_id \
			and observed_stage_instance_id == stage_instance_id \
			and observed_day_two_available == available:
		return
	refresh_castle_room()


func refresh_castle_room() -> void:
	clear_castle_room()
	observed_room_id = m.castle_room_id
	observed_stage_instance_id = m.castle_room_stage.get_instance_id() \
		if m.castle_room_stage != null \
		and is_instance_valid(m.castle_room_stage) else 0
	observed_day_two_available = is_day_two_available()
	if not is_day_two_available() or m.castle_room_stage == null \
			or not is_instance_valid(m.castle_room_stage):
		return
	castle_root = Control.new()
	castle_root.name = "ComfyGamesCastleLayer"
	castle_root.mouse_filter = Control.MOUSE_FILTER_IGNORE
	castle_root.z_index = 28
	castle_root.set_meta("optional_side_game", true)
	castle_root.set_meta("story_progression_owner", false)
	castle_root.set_meta("no_fail", true)
	castle_root.set_meta("main_story_blocking", false)
	m.castle_room_stage.add_child(castle_root)
	castle_root.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)

	var hunt := _hunt_state()
	if not bool(hunt.get("accepted", false)):
		if m.castle_room_id == "main_hall":
			_build_invitation()
		return
	if bool(hunt.get("completed", false)):
		if m.castle_room_id == "main_hall":
			_build_completed_badge()
	else:
		_build_progress_badge()
	for friend: Dictionary in FRIENDS:
		if String(friend["room"]) != m.castle_room_id:
			continue
		if _is_found(String(friend["id"])):
			_build_friend_visit(friend)
		else:
			_build_hidden_friend(friend)
		break


func clear_castle_room() -> void:
	if castle_root != null and is_instance_valid(castle_root):
		if castle_root.get_parent() != null:
			castle_root.get_parent().remove_child(castle_root)
		castle_root.queue_free()
	castle_root = null


func _build_invitation() -> void:
	var button := Button.new()
	button.name = "DayTwoComfyInvitation"
	button.position = Vector2(1040.0, 72.0)
	StorybookUI.style_icon_button(button, "♡", "gold", Vector2(150.0, 150.0),
		"Play hide-and-seek with Rumi, Baby Eagle, and Daddy Mermaid")
	button.set_meta("visual_pointer", true)
	button.set_meta("optional_quest_accept", DAY_TWO_HIDE_AND_SEEK)
	button.pressed.connect(_accept_hide_and_seek)
	castle_root.add_child(button)
	_pulse(button)


func _build_progress_badge() -> void:
	var button := Button.new()
	button.name = "ComfyHideAndSeekProgress"
	button.position = Vector2(1050.0, 64.0)
	var found_count := _found_count()
	var pips := "●".repeat(found_count) + "○".repeat(FRIENDS.size() - found_count)
	StorybookUI.style_icon_button(button, pips, "gold", Vector2(158.0, 96.0),
		"Hide-and-seek: %d of %d friends found" % [found_count, FRIENDS.size()])
	button.set_meta("visual_pointer", true)
	button.set_meta("comfy_progress", found_count)
	button.pressed.connect(_give_next_hint)
	castle_root.add_child(button)
	_pulse(button, 1.025)


func _build_completed_badge() -> void:
	var button := Button.new()
	button.name = "ComfyHideAndSeekComplete"
	button.position = Vector2(1050.0, 64.0)
	StorybookUI.style_icon_button(button, "♡★", "gold", Vector2(158.0, 96.0),
		"Super Seeker hide-and-seek complete")
	button.pressed.connect(func() -> void:
		m.show_msg("Everyone", "Super Seeker Roshan found every friend!", "win")
		m._say("everyone", "", 0.8))
	castle_root.add_child(button)


func _build_hidden_friend(friend: Dictionary) -> void:
	var button := TextureButton.new()
	button.name = "ComfyHidden_%s" % String(friend["id"])
	button.position = (friend["rect"] as Rect2).position
	button.size = (friend["rect"] as Rect2).size
	button.ignore_texture_size = true
	button.stretch_mode = TextureButton.STRETCH_KEEP_ASPECT_CENTERED
	button.texture_normal = _friend_texture(friend)
	button.tooltip_text = "Found %s" % String(friend["name"])
	button.set_meta("visual_pointer", true)
	button.set_meta("comfy_hidden_friend", String(friend["id"]))
	button.pressed.connect(_find_friend.bind(String(friend["id"])))
	castle_root.add_child(button)
	_pulse(button, 1.045)


func _build_friend_visit(friend: Dictionary) -> void:
	var button := TextureButton.new()
	button.name = "ComfyFriendVisit_%s" % String(friend["id"])
	button.position = (friend["rect"] as Rect2).position
	button.size = (friend["rect"] as Rect2).size
	button.ignore_texture_size = true
	button.stretch_mode = TextureButton.STRETCH_KEEP_ASPECT_CENTERED
	button.texture_normal = _friend_texture(friend)
	button.tooltip_text = "Play with %s" % String(friend["name"])
	button.set_meta("comfy_castle_friend", String(friend["id"]))
	button.pressed.connect(_visit_friend.bind(String(friend["id"])))
	castle_root.add_child(button)


func _friend_texture(friend: Dictionary) -> Texture2D:
	var source := load(String(friend["texture"])) as Texture2D
	if not friend.has("atlas_region"):
		return source
	var atlas := AtlasTexture.new()
	atlas.atlas = source
	atlas.region = friend["atlas_region"] as Rect2
	return atlas


func _accept_hide_and_seek() -> void:
	var hunt := _hunt_state()
	if bool(hunt.get("accepted", false)):
		return
	hunt["accepted"] = true
	_set_hunt_state(hunt)
	m._write_save()
	m.show_msg("Daddy Mermaid",
		"Rumi, Baby Eagle, and Daddy are hiding around the castle! Explore anywhere, and tap us when you find us!",
		"talk")
	m._say("daddy", "talk", 0.8)
	refresh_castle_room()


func _find_friend(friend_id: String) -> void:
	if _is_found(friend_id):
		return
	var hunt := _hunt_state()
	var found: Dictionary = hunt.get("found", {}) as Dictionary
	found[friend_id] = true
	hunt["found"] = found
	var friend := _friend_def(friend_id)
	var complete := _all_found(found)
	hunt["completed"] = complete
	_set_hunt_state(hunt)
	if complete:
		# If the bonus sticker is new, award_sticker commits both rewards in one
		# snapshot. If an imported save already owns it, commit the hunt directly.
		if bool(m.stickers.get(SUPER_SEEKER_STICKER, false)):
			m._write_save()
		else:
			m.award_sticker(SUPER_SEEKER_STICKER)
		m.show_msg("Everyone",
			"You found Rumi, Baby Eagle, and Daddy! Super Seeker Roshan wins!",
			"win")
		m._say("everyone", "", 0.8)
	else:
		m._write_save()
		m.show_msg(String(friend.get("name", "Friend")),
			String(friend.get("line", "You found me!")), "win")
		m._say(_voice_id(friend_id), "talk", 0.8)
	refresh_castle_room()


func _visit_friend(friend_id: String) -> void:
	var friend := _friend_def(friend_id)
	if friend.is_empty():
		return
	m.show_msg(String(friend["name"]),
		"Let's play together in the castle!", "talk")
	m._say(_voice_id(friend_id), "talk", 0.8)


func _give_next_hint() -> void:
	for friend: Dictionary in FRIENDS:
		if _is_found(String(friend["id"])):
			continue
		m.show_msg("Roshan", "I hear a friend near the %s!" \
			% String(friend["room_name"]), "hint")
		m._say("roshan", "hide_seek_hint", 0.8)
		return


func _hunt_state() -> Dictionary:
	var state := normalise_save_patch({"comfy_games": m.comfy_games_state})
	m.comfy_games_state = state
	return (state[DAY_TWO_HIDE_AND_SEEK] as Dictionary).duplicate(true)


func _set_hunt_state(hunt: Dictionary) -> void:
	var state := normalise_save_patch({"comfy_games": m.comfy_games_state})
	state[DAY_TWO_HIDE_AND_SEEK] = hunt.duplicate(true)
	m.comfy_games_state = normalise_save_patch({"comfy_games": state})


func _is_found(friend_id: String) -> bool:
	var found: Dictionary = _hunt_state().get("found", {}) as Dictionary
	return bool(found.get(friend_id, false))


func _found_count() -> int:
	var count := 0
	var found: Dictionary = _hunt_state().get("found", {}) as Dictionary
	for friend: Dictionary in FRIENDS:
		if bool(found.get(String(friend["id"]), false)):
			count += 1
	return count


func _all_found(found: Dictionary) -> bool:
	for friend: Dictionary in FRIENDS:
		if not bool(found.get(String(friend["id"]), false)):
			return false
	return true


func _friend_def(friend_id: String) -> Dictionary:
	for friend: Dictionary in FRIENDS:
		if String(friend["id"]) == friend_id:
			return friend
	return {}


func _voice_id(friend_id: String) -> String:
	match friend_id:
		"daddy_mermaid":
			return "daddy"
		"baby_eagle":
			return "sparkle"
		"rumi":
			return "rumi"
		_:
			return "roshan"


func _pulse(control: Control, amount: float = 1.06) -> void:
	control.pivot_offset = control.size * 0.5
	var tween := control.create_tween().set_loops()
	tween.tween_property(control, "scale", Vector2.ONE * amount, 0.72) \
		.set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	tween.tween_property(control, "scale", Vector2.ONE, 0.72) \
		.set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
