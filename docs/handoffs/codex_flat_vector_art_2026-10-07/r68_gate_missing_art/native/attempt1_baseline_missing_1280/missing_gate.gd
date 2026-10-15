extends "res://export/flat_vector_r68/painted_gate.gd"
## Test-only absent-resource provider. No source file is renamed or removed.
func _init(main: ReefMain) -> void:
	super(main)

func _gate_cue_texture() -> Texture2D:
	return null
