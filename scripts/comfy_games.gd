class_name ComfyGames
extends RefCounted

## Optional, chapter-gated castle play that never owns story progression.
## Persistent state stays on ReefMain; this satellite owns policy and the
## lightweight, non-modal castle presentation.

const DAY_TWO_HIDE_AND_SEEK := "day2_castle_hide_and_seek"
const DAY_TWO_FAMILY_EVENING := "day2_family_comfy_evening"
const SUPER_SEEKER_STICKER := "super_seeker"
const FUTURE_REWARD_ID := "comfy_evening_mystery_reward"
const STATE_VERSION := 2
const MOVIE_SCENE_COUNT := 3

const CHAPTER_GAMES: Dictionary = {
	2: [DAY_TWO_HIDE_AND_SEEK, DAY_TWO_FAMILY_EVENING],
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

const DINNER_INGREDIENTS: Array[Dictionary] = [
	{
		"id": "apple",
		"name": "Apple",
		"texture": "res://assets/props/story/fruit_apple.png",
		"rect": Rect2(120.0, 350.0, 190.0, 190.0),
		"line": "Plop! A crunchy apple goes into our supper!",
	},
	{
		"id": "carrot",
		"name": "Carrot",
		"texture": "res://assets/mg/carrot.png",
		"rect": Rect2(540.0, 360.0, 190.0, 190.0),
		"line": "Plop! A bright carrot goes into our supper!",
	},
	{
		"id": "strawberry",
		"name": "Strawberry",
		"texture": "res://assets/chapter2/birthday/sky_lagoon_strawberry_single.png",
		"rect": Rect2(950.0, 350.0, 190.0, 190.0),
		"line": "Plop! A sweet strawberry makes it extra special!",
	},
]

const BEDTIME_FAMILY: Array[Dictionary] = [
	{
		"id": "rumi",
		"name": "Rumi",
		"texture": "res://assets/characters/rumi/rumi_eight_pose_runtime.png",
		"atlas_region": Rect2(512.0, 0.0, 256.0, 384.0),
		"rect": Rect2(75.0, 285.0, 210.0, 315.0),
		"line": "Goodnight, Rumi. Snuggle in!",
	},
	{
		"id": "baby_eagle",
		"name": "Baby Eagle",
		"texture": "res://assets/book/baby_eagle.png",
		"rect": Rect2(355.0, 330.0, 210.0, 270.0),
		"line": "Goodnight, Baby Eagle. Tuck your wings in!",
	},
	{
		"id": "daddy_mermaid",
		"name": "Daddy Mermaid",
		"texture": "res://assets/characters/friends/daddy.webp",
		"rect": Rect2(655.0, 270.0, 210.0, 330.0),
		"line": "Goodnight, Daddy Mermaid. Sweet dreams!",
	},
	{
		"id": "roshan",
		"name": "Mermaid Roshan",
		"texture": "res://assets/characters/roshan_25d/roshan_base.png",
		"rect": Rect2(955.0, 270.0, 210.0, 330.0),
		"line": "Goodnight, Mermaid Roshan. What a cosy day!",
	},
]

var m: ReefMain
var castle_root: Control = null
var observed_room_id := ""
var observed_stage_instance_id := 0
var observed_day_two_available := false
var announced_objective := ""


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
	var hunt_accepted_value: Variant = hunt_raw.get("accepted", false)
	var hunt_completed_value: Variant = hunt_raw.get("completed", false)
	var hunt_accepted: bool = bool(hunt_accepted_value) \
		if typeof(hunt_accepted_value) == TYPE_BOOL else false
	var hunt_completed: bool = complete_from_finds or (bool(hunt_completed_value) \
		if typeof(hunt_completed_value) == TYPE_BOOL else false)

	var quest_value: Variant = raw.get(DAY_TWO_FAMILY_EVENING, {})
	var quest_raw: Dictionary = quest_value as Dictionary \
		if quest_value is Dictionary else {}
	var dinner_value: Variant = quest_raw.get("dinner", {})
	var dinner_raw: Dictionary = dinner_value as Dictionary \
		if dinner_value is Dictionary else {}
	var ingredients_value: Variant = dinner_raw.get("ingredients", {})
	var ingredients_raw: Dictionary = ingredients_value as Dictionary \
		if ingredients_value is Dictionary else {}
	var ingredients: Dictionary = {}
	var all_ingredients_added := true
	for ingredient: Dictionary in DINNER_INGREDIENTS:
		var ingredient_id := String(ingredient["id"])
		var ingredient_value: Variant = ingredients_raw.get(ingredient_id, false)
		var ingredient_added: bool = bool(ingredient_value) \
			if typeof(ingredient_value) == TYPE_BOOL else false
		ingredients[ingredient_id] = ingredient_added
		all_ingredients_added = all_ingredients_added and ingredient_added
	var pot_value: Variant = dinner_raw.get("pot_stirred", false)
	var pot_stirred: bool = bool(pot_value) \
		if typeof(pot_value) == TYPE_BOOL else false
	var dinner_completed_value: Variant = dinner_raw.get("completed", false)
	var dinner_completed: bool = (all_ingredients_added and pot_stirred) \
		or (bool(dinner_completed_value) \
		if typeof(dinner_completed_value) == TYPE_BOOL else false)

	var movie_value: Variant = quest_raw.get("movie", {})
	var movie_raw: Dictionary = movie_value as Dictionary \
		if movie_value is Dictionary else {}
	var scenes_value: Variant = movie_raw.get("scenes_watched", 0)
	var scenes_watched: int = clampi(int(scenes_value), 0, MOVIE_SCENE_COUNT) \
		if typeof(scenes_value) in [TYPE_INT, TYPE_FLOAT] else 0
	var movie_completed_value: Variant = movie_raw.get("completed", false)
	var movie_completed: bool = scenes_watched >= MOVIE_SCENE_COUNT \
		or (bool(movie_completed_value) \
		if typeof(movie_completed_value) == TYPE_BOOL else false)

	var bedtime_value: Variant = quest_raw.get("bedtime", {})
	var bedtime_raw: Dictionary = bedtime_value as Dictionary \
		if bedtime_value is Dictionary else {}
	var tucked_value: Variant = bedtime_raw.get("tucked_in", {})
	var tucked_raw: Dictionary = tucked_value as Dictionary \
		if tucked_value is Dictionary else {}
	var tucked_in: Dictionary = {}
	var all_tucked_in := true
	for family_member: Dictionary in BEDTIME_FAMILY:
		var family_id := String(family_member["id"])
		var family_value: Variant = tucked_raw.get(family_id, false)
		var is_tucked: bool = bool(family_value) \
			if typeof(family_value) == TYPE_BOOL else false
		tucked_in[family_id] = is_tucked
		all_tucked_in = all_tucked_in and is_tucked
	var bedtime_completed_value: Variant = bedtime_raw.get("completed", false)
	var bedtime_completed: bool = all_tucked_in \
		or (bool(bedtime_completed_value) \
		if typeof(bedtime_completed_value) == TYPE_BOOL else false)

	var quest_accepted_value: Variant = quest_raw.get("accepted", false)
	var quest_completed_value: Variant = quest_raw.get("completed", false)
	var quest_accepted: bool = hunt_accepted or hunt_completed \
		or (bool(quest_accepted_value) \
		if typeof(quest_accepted_value) == TYPE_BOOL else false)
	var quest_completed: bool = bedtime_completed \
		or (bool(quest_completed_value) \
		if typeof(quest_completed_value) == TYPE_BOOL else false)
	var reward_value: Variant = quest_raw.get("reward", {})
	var reward_raw: Dictionary = reward_value as Dictionary \
		if reward_value is Dictionary else {}
	var reward_unlocked_value: Variant = reward_raw.get("unlocked", false)
	var reward_unlocked: bool = quest_completed \
		or (bool(reward_unlocked_value) \
		if typeof(reward_unlocked_value) == TYPE_BOOL else false)
	return {
		"version": STATE_VERSION,
		DAY_TWO_HIDE_AND_SEEK: {
			"accepted": hunt_accepted,
			"found": found,
			"completed": hunt_completed,
		},
		DAY_TWO_FAMILY_EVENING: {
			"accepted": quest_accepted,
			"dinner": {
				"ingredients": ingredients,
				"pot_stirred": pot_stirred,
				"completed": dinner_completed,
			},
			"movie": {
				"scenes_watched": scenes_watched,
				"completed": movie_completed,
			},
			"bedtime": {
				"tucked_in": tucked_in,
				"completed": bedtime_completed,
			},
			"completed": quest_completed,
			"reward": {
				"id": FUTURE_REWARD_ID,
				"unlocked": reward_unlocked,
				"verified": false,
				"introduced": false,
			},
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
	if not bool(hunt.get("completed", false)):
		_build_hide_and_seek_room()
		return
	var quest := _quest_state()
	if bool(quest.get("completed", false)):
		_build_friend_visit_for_current_room()
		return
	var dinner: Dictionary = quest.get("dinner", {}) as Dictionary
	if not bool(dinner.get("completed", false)):
		if m.castle_room_id == "kitchen":
			_build_cooking_game(dinner)
		else:
			_build_friend_visit_for_current_room()
		return
	var movie: Dictionary = quest.get("movie", {}) as Dictionary
	if not bool(movie.get("completed", false)):
		if m.castle_room_id == "movie_lounge":
			_build_movie_game(movie)
		else:
			_build_friend_visit_for_current_room()
		return
	var bedtime: Dictionary = quest.get("bedtime", {}) as Dictionary
	if not bool(bedtime.get("completed", false)):
		if m.castle_room_id == "sleepover_bedroom":
			_build_bedtime_game(bedtime)
		else:
			_build_friend_visit_for_current_room()


func clear_castle_room() -> void:
	if castle_root != null and is_instance_valid(castle_root):
		if castle_root.get_parent() != null:
			castle_root.get_parent().remove_child(castle_root)
		castle_root.queue_free()
	castle_root = null


func _build_hide_and_seek_room() -> void:
	for friend: Dictionary in FRIENDS:
		if String(friend["room"]) != m.castle_room_id:
			continue
		if _is_found(String(friend["id"])):
			_build_friend_visit(friend)
		else:
			_build_hidden_friend(friend)
		break


func _build_friend_visit_for_current_room() -> void:
	for friend: Dictionary in FRIENDS:
		if String(friend["room"]) == m.castle_room_id:
			_build_friend_visit(friend)
			return


func _build_cooking_game(dinner: Dictionary) -> void:
	_announce_once("dinner", "Roshan",
		"Dinner time! Tap the apple, carrot, and strawberry for our cosy supper.",
		"talk")
	var ingredients: Dictionary = dinner.get("ingredients", {}) as Dictionary
	var ingredients_ready := true
	for ingredient: Dictionary in DINNER_INGREDIENTS:
		var ingredient_id := String(ingredient["id"])
		if bool(ingredients.get(ingredient_id, false)):
			continue
		ingredients_ready = false
		var button := _make_picture_button(
			"ComfyDinnerIngredient_%s" % ingredient_id,
			ingredient["rect"] as Rect2, _definition_texture(ingredient),
			"Add %s" % String(ingredient["name"]))
		button.set_meta("comfy_dinner_ingredient", ingredient_id)
		button.pressed.connect(_add_dinner_ingredient.bind(ingredient_id))
		castle_root.add_child(button)
		_pulse(button, 1.06)
	if not ingredients_ready:
		return
	var pot := _make_picture_button("ComfyDinnerSoupPot",
		Rect2(500.0, 285.0, 280.0, 260.0),
		load("res://assets/flats/castle/rooms/room_kitchen_item_soup_pot.png") \
			as Texture2D, "Stir dinner")
	pot.set_meta("comfy_dinner_finish", true)
	pot.pressed.connect(_stir_dinner)
	castle_root.add_child(pot)
	_pulse(pot, 1.07)
	_announce_once("stir_dinner", "Roshan",
		"Everything is in! Tap the soup pot and stir, stir, stir!", "talk")


func _build_movie_game(movie: Dictionary) -> void:
	var scenes_watched := int(movie.get("scenes_watched", 0))
	var screen := _make_picture_button("ComfyFamilyMovieScreen",
		Rect2(445.0, 175.0, 390.0, 300.0),
		load("res://assets/flats/castle/dream_house/movie_screen_frame.png") \
			as Texture2D, "Watch the family movie")
	screen.set_meta("comfy_movie_scene", scenes_watched + 1)
	screen.pressed.connect(_watch_movie_scene)
	castle_root.add_child(screen)
	_pulse(screen, 1.035)
	_announce_once("movie", "Everyone",
		"Movie time! Tap the big screen to watch our three favourite moments.",
		"talk")


func _build_bedtime_game(bedtime: Dictionary) -> void:
	_announce_once("bedtime", "Daddy Mermaid",
		"What a lovely evening! Tap each sleepy friend to tuck everyone into bed.",
		"talk")
	var tucked_in: Dictionary = bedtime.get("tucked_in", {}) as Dictionary
	for family_member: Dictionary in BEDTIME_FAMILY:
		var family_id := String(family_member["id"])
		if bool(tucked_in.get(family_id, false)):
			continue
		var button := _make_picture_button(
			"ComfyBedtime_%s" % family_id,
			family_member["rect"] as Rect2,
			_definition_texture(family_member),
			"Tuck in %s" % String(family_member["name"]))
		button.set_meta("comfy_bedtime_family", family_id)
		button.pressed.connect(_tuck_in_family_member.bind(family_id))
		castle_root.add_child(button)
		_pulse(button, 1.045)


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
	button.set_meta("direct_world_character", true)
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
	return _definition_texture(friend)


func _definition_texture(definition: Dictionary) -> Texture2D:
	var source := load(String(definition["texture"])) as Texture2D
	if not definition.has("atlas_region"):
		return source
	var atlas := AtlasTexture.new()
	atlas.atlas = source
	atlas.region = definition["atlas_region"] as Rect2
	return atlas


func _make_picture_button(button_name: String, rect: Rect2,
		texture: Texture2D, accessible_name: String) -> TextureButton:
	var button := TextureButton.new()
	button.name = button_name
	button.position = rect.position
	button.size = rect.size
	button.ignore_texture_size = true
	button.stretch_mode = TextureButton.STRETCH_KEEP_ASPECT_CENTERED
	button.texture_normal = texture
	button.tooltip_text = accessible_name
	button.set_meta("visual_pointer", true)
	button.set_meta("direct_world_art_hotspot", true)
	button.set_meta("optional_side_game", true)
	return button


func _find_friend(friend_id: String) -> void:
	if _is_found(friend_id):
		return
	var hunt := _hunt_state()
	var found: Dictionary = hunt.get("found", {}) as Dictionary
	hunt["accepted"] = true
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
			"You found everyone! Super Seeker Roshan wins! Now let's cook dinner in the Royal Kitchen.",
			"win")
	else:
		m._write_save()
		m.show_msg(String(friend.get("name", "Friend")),
			String(friend.get("line", "You found me!")), "hide_seek_found")
	refresh_castle_room()


func _add_dinner_ingredient(ingredient_id: String) -> void:
	var quest := _quest_state()
	var dinner: Dictionary = quest.get("dinner", {}) as Dictionary
	var ingredients: Dictionary = dinner.get("ingredients", {}) as Dictionary
	if bool(ingredients.get(ingredient_id, false)):
		return
	ingredients[ingredient_id] = true
	dinner["ingredients"] = ingredients
	quest["accepted"] = true
	quest["dinner"] = dinner
	_set_quest_state(quest)
	m._write_save()
	var ingredient := _ingredient_def(ingredient_id)
	m.show_msg("Roshan", String(ingredient.get("line", "Plop! Into dinner it goes!")),
		"talk")
	refresh_castle_room()


func _stir_dinner() -> void:
	var quest := _quest_state()
	var dinner: Dictionary = quest.get("dinner", {}) as Dictionary
	var ingredients: Dictionary = dinner.get("ingredients", {}) as Dictionary
	if bool(dinner.get("completed", false)) or not _all_dinner_ingredients(ingredients):
		return
	dinner["pot_stirred"] = true
	dinner["completed"] = true
	quest["accepted"] = true
	quest["dinner"] = dinner
	_set_quest_state(quest)
	m._write_save()
	m.show_msg("Everyone",
		"Dinner is ready! Yum! When you're ready, let's watch a movie in the Cloud Movie Lounge.",
		"win")
	refresh_castle_room()


func _watch_movie_scene() -> void:
	var quest := _quest_state()
	var dinner: Dictionary = quest.get("dinner", {}) as Dictionary
	var movie: Dictionary = quest.get("movie", {}) as Dictionary
	if not bool(dinner.get("completed", false)) or bool(movie.get("completed", false)):
		return
	var scenes_watched := clampi(int(movie.get("scenes_watched", 0)) + 1,
		0, MOVIE_SCENE_COUNT)
	movie["scenes_watched"] = scenes_watched
	movie["completed"] = scenes_watched >= MOVIE_SCENE_COUNT
	quest["accepted"] = true
	quest["movie"] = movie
	_set_quest_state(quest)
	m._write_save()
	var scene_lines: Array[String] = [
		"Look! A silly crab is dancing in the movie!",
		"Now everyone is flying through sparkly clouds!",
		"The movie ends with the biggest family hug. Time for the Sleepover Bedroom!",
	]
	m.show_msg("Everyone", scene_lines[scenes_watched - 1],
		"win" if scenes_watched >= MOVIE_SCENE_COUNT else "talk")
	refresh_castle_room()


func _tuck_in_family_member(family_id: String) -> void:
	var quest := _quest_state()
	var movie: Dictionary = quest.get("movie", {}) as Dictionary
	var bedtime: Dictionary = quest.get("bedtime", {}) as Dictionary
	var tucked_in: Dictionary = bedtime.get("tucked_in", {}) as Dictionary
	if not bool(movie.get("completed", false)) or bool(tucked_in.get(family_id, false)):
		return
	tucked_in[family_id] = true
	bedtime["tucked_in"] = tucked_in
	var complete := _all_tucked_in(tucked_in)
	bedtime["completed"] = complete
	quest["accepted"] = true
	quest["bedtime"] = bedtime
	if complete:
		quest["completed"] = true
		quest["reward"] = {
			"id": FUTURE_REWARD_ID,
			"unlocked": true,
			"verified": false,
			"introduced": false,
		}
	_set_quest_state(quest)
	m._write_save()
	var family_member := _bedtime_def(family_id)
	if complete:
		m.show_msg("Everyone",
			"Goodnight! The whole family is cosy. A mystery reward is unlocked and waiting for a future adventure!",
			"win")
	else:
		m.show_msg(String(family_member.get("name", "Friend")),
			String(family_member.get("line", "Goodnight!")), "talk")
	refresh_castle_room()


func _visit_friend(friend_id: String) -> void:
	var friend := _friend_def(friend_id)
	if friend.is_empty():
		return
	m.show_msg(String(friend["name"]),
		"Let's play together in the castle!", "hide_seek_visit")


func _hunt_state() -> Dictionary:
	var state := normalise_save_patch({"comfy_games": m.comfy_games_state})
	m.comfy_games_state = state
	return (state[DAY_TWO_HIDE_AND_SEEK] as Dictionary).duplicate(true)


func _set_hunt_state(hunt: Dictionary) -> void:
	var state := normalise_save_patch({"comfy_games": m.comfy_games_state})
	state[DAY_TWO_HIDE_AND_SEEK] = hunt.duplicate(true)
	m.comfy_games_state = normalise_save_patch({"comfy_games": state})


func _quest_state() -> Dictionary:
	var state := normalise_save_patch({"comfy_games": m.comfy_games_state})
	m.comfy_games_state = state
	return (state[DAY_TWO_FAMILY_EVENING] as Dictionary).duplicate(true)


func _set_quest_state(quest: Dictionary) -> void:
	var state := normalise_save_patch({"comfy_games": m.comfy_games_state})
	state[DAY_TWO_FAMILY_EVENING] = quest.duplicate(true)
	m.comfy_games_state = normalise_save_patch({"comfy_games": state})


func _is_found(friend_id: String) -> bool:
	var found: Dictionary = _hunt_state().get("found", {}) as Dictionary
	return bool(found.get(friend_id, false))


func _all_found(found: Dictionary) -> bool:
	for friend: Dictionary in FRIENDS:
		if not bool(found.get(String(friend["id"]), false)):
			return false
	return true


func _all_dinner_ingredients(ingredients: Dictionary) -> bool:
	for ingredient: Dictionary in DINNER_INGREDIENTS:
		if not bool(ingredients.get(String(ingredient["id"]), false)):
			return false
	return true


func _all_tucked_in(tucked_in: Dictionary) -> bool:
	for family_member: Dictionary in BEDTIME_FAMILY:
		if not bool(tucked_in.get(String(family_member["id"]), false)):
			return false
	return true


func _friend_def(friend_id: String) -> Dictionary:
	for friend: Dictionary in FRIENDS:
		if String(friend["id"]) == friend_id:
			return friend
	return {}


func _ingredient_def(ingredient_id: String) -> Dictionary:
	for ingredient: Dictionary in DINNER_INGREDIENTS:
		if String(ingredient["id"]) == ingredient_id:
			return ingredient
	return {}


func _bedtime_def(family_id: String) -> Dictionary:
	for family_member: Dictionary in BEDTIME_FAMILY:
		if String(family_member["id"]) == family_id:
			return family_member
	return {}


func _announce_once(objective_id: String, speaker: String, line: String,
		voice_event: String) -> void:
	if announced_objective == objective_id:
		return
	announced_objective = objective_id
	m.show_msg(speaker, line, voice_event)


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
