extends SceneTree
# Import/runtime contract for the Fairy Pond 2D art and readability pass.

const BACKGROUNDS: Array[String] = [
	"res://assets/fairy/pond_dawn.png",
	"res://assets/fairy/pond_twilight.png",
	"res://assets/fairy/pond_boss_clearing.png",
]

const SPRITES: Array[String] = [
	"res://assets/fairy/sprites/bug_jewel.png",
	"res://assets/fairy/sprites/bug_moth.png",
	"res://assets/fairy/sprites/bug_firefly.png",
	"res://assets/fairy/sprites/boss_leaf.png",
	"res://assets/fairy/sprites/boss_seed.png",
	"res://assets/fairy/sprites/boss_sprout.png",
	"res://assets/fairy/sprites/boss_bud.png",
	"res://assets/fairy/sprites/boss_opening.png",
	"res://assets/fairy/sprites/boss_bloom.png",
	"res://assets/fairy/sprites/helpful_flower_gate.png",
	"res://assets/fairy/sprites/danger_thorn_halo.png",
]

const RETIRED_MODELS: Array[String] = [
	"res://assets/fairy/models/bug_jewel.glb",
	"res://assets/fairy/models/bug_moth.glb",
	"res://assets/fairy/models/bug_firefly.glb",
	"res://assets/fairy/models/boss_leaf.glb",
	"res://assets/fairy/models/boss_seed.glb",
	"res://assets/fairy/models/boss_sprout.glb",
	"res://assets/fairy/models/boss_bud.glb",
	"res://assets/fairy/models/boss_opening.glb",
	"res://assets/fairy/models/boss_bloom.glb",
	"res://assets/art35/arena/fairy_bank_0.glb",
	"res://assets/art35/arena/fairy_bank_1.glb",
	"res://assets/art35/arena/fairy_flower_gate.glb",
	"res://assets/art35/arena/fairy_lily_cluster.glb",
	"res://assets/art35/arena/fairy_shadow_beetle.glb",
	"res://assets/art35/arena/fairy_shadow_eel.glb",
	"res://assets/art35/arena/fairy_shadow_jellyfish.glb",
]

func _audit_texture(path: String, require_alpha: bool) -> bool:
	if not FileAccess.file_exists(path):
		print("FAIRY_ART|FAIL|missing_texture=", path)
		return false
	var image := Image.new()
	var error: int = image.load(ProjectSettings.globalize_path(path))
	if error != OK or image.is_empty():
		print("FAIRY_ART|FAIL|load_texture=", path, " error=", error)
		return false
	if image.get_width() != 1024 or image.get_height() != 1024:
		print("FAIRY_ART|FAIL|texture_size=", image.get_size(), " path=", path)
		return false
	if require_alpha:
		var corners: Array[float] = [
			image.get_pixel(0, 0).a,
			image.get_pixel(image.get_width() - 1, 0).a,
			image.get_pixel(0, image.get_height() - 1).a,
			image.get_pixel(image.get_width() - 1, image.get_height() - 1).a,
		]
		for alpha_value in corners:
			if alpha_value > 0.01:
				print("FAIRY_ART|FAIL|opaque_corner=", corners, " path=", path)
				return false
	print("FAIRY_ART|texture=", path.get_file(), " size=1024x1024 alpha=", require_alpha)
	return true

func _run() -> void:
	var failed := false
	for path in BACKGROUNDS:
		if not _audit_texture(path, false):
			failed = true
	for path in SPRITES:
		if not _audit_texture(path, true):
			failed = true
	for path in RETIRED_MODELS:
		if FileAccess.file_exists(path):
			print("FAIRY_ART|FAIL|retired_3d_model=", path)
			failed = true
	var source: String = FileAccess.get_file_as_string("res://scripts/games/fairy.gd")
	var source_contracts: Array[String] = [
		"const FS_PACE := 0.70",
		"FS_HELPFUL_CUE_ART",
		"FS_DANGER_CUE_ART",
		"Sprite3D.new()",
		"panel.rotation.x = -PI / 2.0",
		"panel.flip_v = true",
	]
	for contract in source_contracts:
		if not source.contains(contract):
			print("FAIRY_ART|FAIL|missing_source_contract=", contract)
			failed = true
	if source.contains("assets/fairy/models/") or source.contains(".glb"):
		print("FAIRY_ART|FAIL|fairy_runtime_still_references_3d")
		failed = true
	print("FAIRY_ART|RESULT=", "FAIL" if failed else "OK", " sprites=", SPRITES.size())
	quit(1 if failed else 0)

func _init() -> void:
	call_deferred("_run")
