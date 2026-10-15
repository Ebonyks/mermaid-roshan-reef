extends SceneTree

var owner: ReefMain
var director: LivingWorldDirector
var queries: Array[Dictionary] = []
var checks: Array[Dictionary] = []
var layers: Array[CanvasLayer] = []
var catalogue: Dictionary = {}

func check(id: String, ok: bool) -> void:
	checks.append({"id": id, "pass": ok})

func reset() -> void:
	owner.game = ""
	owner.g = {}
	owner.intro_active = false
	owner.mg_kind = ""
	owner.living_probe_stage_override = ""
	owner.companion_care_layer = null
	owner.companion_layer = null
	owner.collection_layer = null
	owner.stickers_layer = null
	owner.wardrobe_layer = null
	owner.craft_layer = null
	owner.opera_active_act_index = -1
	owner.castle_room_id = "main_hall"
	owner.kart_ground = "terrain"

func query(id: String, expected: String, inputs: Dictionary) -> void:
	var actual: String = director.resolve_stage_id()
	queries.append({"id": id, "inputs": inputs, "actual": actual, "expected": expected, "registry_member": catalogue.has(actual), "pass": actual == expected})

func _initialize() -> void:
	call_deferred("run")

func run() -> void:
	owner = load("res://scripts/main.gd").new() as ReefMain
	director = LivingWorldDirector.new(owner)
	catalogue = LivingWorldCatalog.build()
	check("bare_main_outside_tree_no_player", not owner.is_inside_tree() and owner.player == null)
	check("catalogue_100", catalogue.size() == 100)
	reset()
	query("bare_empty_reef_no_player", "", {"game": "", "player": "null"})
	var simple: Dictionary = {"fetch": "minigame.fetch", "dolls": "minigame.dolls", "brawl": "minigame.brawl", "seek": "minigame.seek", "race": "minigame.race_sunset", "shop": "minigame.shop", "treasure": "minigame.treasure", "melody": "minigame.melody", "slide": "minigame.slide_ice", "fairyshoot": "minigame.fairy_flight", "kart": "kart.ocean_circuit", "galaxy": "galaxy.butterfly_garden", "ember": "ember.fortress_planet", "combat": "combat.ice_berry", "stuffie": "stuffie.sparring_den", "dungeon": "dungeon.ice.00", "emberdun": "dungeon.ember.00", "north": "north.mountain_pass", "level2": "sky.courtyard"}
	for key: String in simple:
		reset()
		owner.game = key
		query("simple_" + key, String(simple[key]), {"game": key, "other_components": "null", "player": "null"})
	for x: float in [-1.0, 0.0, 2047.99, 2048.0, 4095.99, 4096.0, 6144.0, 7000.0]:
		reset()
		owner.game = "level2"
		owner.g = {"phase": "promenade", "lagoon_master_x": x}
		var expected: String = "sky.promenade_runway" if x < 2048.0 else ("sky.promenade_playground" if x < 4096.0 else "sky.promenade_castle")
		query("promenade_" + str(x), expected, {"game": owner.game, "g": owner.g})
	for room: Dictionary in CastleRooms25D.ROOMS:
		reset()
		owner.game = "level2"
		owner.g = {"phase": "hall"}
		owner.castle_room_id = String(room["id"])
		query("castle_" + owner.castle_room_id, "castle.room." + owner.castle_room_id, {"game": owner.game, "g": owner.g, "castle_room_id": owner.castle_room_id})
	reset()
	owner.game = "level2"
	owner.g = {"phase": "hall"}
	owner.castle_room_id = "__unregistered_fixture__"
	query("castle_invalid_fallback", "castle.room.main_hall", {"castle_room_id": owner.castle_room_id, "g": owner.g})
	var overlay_fields: Dictionary = {"companion_care_layer": "overlay.companion_care", "companion_layer": "overlay.companion_picker", "collection_layer": "overlay.critter_book", "stickers_layer": "overlay.sticker_book", "wardrobe_layer": "overlay.wardrobe", "craft_layer": "overlay.craft_studio"}
	for field: String in overlay_fields:
		reset()
		owner.game = "level2"
		var layer: CanvasLayer = CanvasLayer.new()
		layer.visible = false
		layers.append(layer)
		owner.set(field, layer)
		query("overlay_" + field, String(overlay_fields[field]), {"game": owner.game, "synthetic_layer": field, "layer_visible": false, "layer_inside_tree": layer.is_inside_tree()})
		owner.intro_active = true
		query("intro_priority_" + field, "intro.storybook", {"intro_active": true, "synthetic_layer": field})
	reset()
	owner.companion_care_layer = layers[0]
	owner.craft_layer = layers[5]
	query("overlay_priority_care_before_craft", "overlay.companion_care", {"both_fields_present": true})
	for kind: String in ["snowman", "garden", "trampoline", "xmas", "__unmapped__"]:
		reset()
		owner.game = "level2"
		owner.mg_kind = kind
		query("picture_" + kind, "picture." + kind if kind != "__unmapped__" else "", {"game": owner.game, "mg_kind": kind})
	reset()
	owner.game = "slide"
	owner.g = {"fr": {"theme": "rainbow"}}
	query("slide_rainbow", "minigame.slide_rainbow", {"game": owner.game, "g": owner.g})
	reset()
	owner.game = "fairyshoot"
	owner.g = {"phase": "boss"}
	query("fairy_boss", "minigame.fairy_boss", {"game": owner.game, "g": owner.g})
	reset()
	owner.game = "kart"
	owner.kart_ground = "float"
	query("kart_float", "kart.rainbow_road", {"game": owner.game, "kart_ground": owner.kart_ground})
	for act: int in range(-1, 19):
		reset()
		owner.game = "opera"
		owner.opera_active_act_index = act
		query("opera_" + str(act), "opera.act.%02d" % act if OperaHouse.is_live_act_index(act) else "", {"game": owner.game, "act": act, "actual_live_predicate": OperaHouse.is_live_act_index(act)})
	var aliases: Array = JSON.parse_string(FileAccess.get_file_as_string(OS.get_environment("R57_ALIASES")))
	for alias: String in aliases:
		reset()
		owner.game = alias.trim_prefix("game.")
		var result: String = director.resolve_stage_id()
		queries.append({"id": "alias_suffix_" + alias, "inputs": {"game": owner.game, "other_inputs": "empty/null diagnostic defaults"}, "actual": result, "registry_member": catalogue.has(result), "assertion": "observation_only_not_normal_route"})
	reset()
	owner.living_probe_stage_override = "__not_a_catalogue_entry__"
	query("headless_override_bypasses_registry", "__not_a_catalogue_entry__", {"override": owner.living_probe_stage_override})
	check("never_setup_or_ready", not owner.is_inside_tree() and owner.player == null and owner.living_layer == null and owner.living_canvas == null and owner.get_child_count() == 0)
	var failed: int = 0
	for row: Dictionary in checks + queries:
		if row.has("pass") and not bool(row["pass"]):
			failed += 1
	var result: Dictionary = {"engine": Engine.get_version_info(), "display": DisplayServer.get_name(), "configured_renderer": ProjectSettings.get_setting("rendering/renderer/rendering_method"), "catalogue": catalogue, "queries": queries, "checks": checks, "failed": failed, "scope": "Unchanged pure catalogue/selector component on bare existing Main outside SceneTree. Synthetic diagnostic inputs; no ready/tick/setup/render/game constructors or player; zero normal-route/art acceptance."}
	var file: FileAccess = FileAccess.open(OS.get_environment("R57_OUT"), FileAccess.WRITE)
	file.store_string(JSON.stringify(result, "\t") + "\n")
	file.close()
	reset()
	for layer: CanvasLayer in layers:
		layer.free()
	director = null
	owner.free()
	print("R57_COMPONENT ", queries.size(), " queries ", checks.size(), " invariants failed=", failed)
	quit(0 if failed == 0 else 1)
