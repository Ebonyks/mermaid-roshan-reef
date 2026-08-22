extends Node2D

const KING_SEQUENCE: Array[StringName] = [&"idle", &"heavy_walk", &"cape_fan"]
const PRINCE_SEQUENCE: Array[StringName] = [&"idle_glance", &"sleek_walk", &"cinderstep"]

@onready var king: AnimatedSprite2D = $EmberKing
@onready var prince: AnimatedSprite2D = $EmberPrince

var _sequence_index: int = 0
var _elapsed: float = 0.0


func _ready() -> void:
	_play_current_pair()


func _process(delta: float) -> void:
	_elapsed += delta
	if _elapsed < 4.0:
		return
	_elapsed = 0.0
	_sequence_index = (_sequence_index + 1) % KING_SEQUENCE.size()
	_play_current_pair()


func _play_current_pair() -> void:
	king.play(KING_SEQUENCE[_sequence_index])
	prince.play(PRINCE_SEQUENCE[_sequence_index])
