extends SceneTree
# Import/runtime contract for the Fairy Pond 2D art and readability pass.

const BACKGROUNDS: Array[String] = [
	"res://assets/fairy/pond_panorama.png",
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
	"res://assets/fairy/sprites/ornament_lily_cluster.png",
	"res://assets/fairy/sprites/ornament_lavender_reeds.png",
]

func _audit_texture(path: String, require_alpha: bool, expected_size: Vector2i) -> bool:
	if not FileAccess.file_exists(path):
		print("FAIRY_ART|FAIL|missing_texture=", path)
		return false
	var image := Image.new()
	var error: int = image.load(ProjectSettings.globalize_path(path))
	if error != OK or image.is_empty():
		print("FAIRY_ART|FAIL|load_texture=", path, " error=", error)
		return false
	if image.get_size() != expected_size:
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
	print("FAIRY_ART|texture=", path.get_file(), " size=", image.get_size(), " alpha=", require_alpha)
	return true

func _run() -> void:
	var failed := false
	for path in BACKGROUNDS:
		if not _audit_texture(path, false, Vector2i(4096, 1024)):
			failed = true
	for path in SPRITES:
		if not _audit_texture(path, true, Vector2i(1024, 1024)):
			failed = true
	var source: String = FileAccess.get_file_as_string("res://scripts/games/fairy.gd")
	var source_contracts: Array[String] = [
		"const FS_PACE := 0.70",
		"FS_HELPFUL_CUE_ART",
		"FS_DANGER_CUE_ART",
		"FS_ORNAMENT_ART",
		"Sprite3D.new()",
		"panel.rotation = Vector3(-PI / 2.0, 0.0, -PI / 2.0)",
	]
	for contract in source_contracts:
		if not source.contains(contract):
			print("FAIRY_ART|FAIL|missing_source_contract=", contract)
			failed = true
	print("FAIRY_ART|RESULT=", "FAIL" if failed else "OK", " sprites=", SPRITES.size())
	quit(1 if failed else 0)

func _init() -> void:
	call_deferred("_run")
