class_name DustBossPatterns
extends EncounterPatterns2D

## Compatibility name for existing probes. All attack rules are shared;
## Grand Puff contributes only the content profile.
func _init() -> void:
	super(EncounterProfile2D.grand_puff())
