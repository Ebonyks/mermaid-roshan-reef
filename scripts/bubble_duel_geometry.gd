class_name BubbleDuelGeometry
extends RefCounted
## Non-destructive adapter: contacts follow the existing painted frame.
const SCALE: float = 2.1
const MAGNIFY: float = 0.58
var appearance: BubbleDuelCast
var cache: Dictionary = {}


func _init(cast_art: BubbleDuelCast) -> void:
	appearance = cast_art


func apply(fighter: BubbleDuelFighter, tick: int) -> void:
	var person: String = String(fighter.profile.get("character", "roshan"))
	fighter.pose_duration = 16.0 / 15.0 if person == "roshan" else (0.8 if person == "marlo" else 4.0 / 6.0)
	fighter.moving_pose = fighter.pose_time < fighter.pose_duration
	fighter.draw_clock = fighter.pose_time if fighter.moving_pose else float(tick) / 30.0
	var spec: Dictionary = appearance.frame(fighter.profile, fighter.moving_pose, fighter.draw_clock)
	var key: String = person + ":" + String(spec["source"]) + ":" + str(spec["index"])
	if not cache.has(key):
		var ratio: float = MAGNIFY / SCALE
		var rest: Vector2 = appearance.contact(fighter.profile, false, 0.0) * ratio
		var shift: Vector2 = Vector2(0, 12.5) - rest
		var fin: Vector2 = appearance.contact(fighter.profile, fighter.moving_pose, fighter.draw_clock) * ratio + shift
		var body: Rect2 = spec["body"]
		var factor: float = float(spec["factor"]) * ratio
		body = Rect2((body.position - (spec["anchor"] as Vector2)) * factor + shift, body.size * factor)
		cache[key] = {"shift": shift, "fin": fin, "body": body}
	var entry: Dictionary = cache[key]
	fighter.draw_offset = entry["shift"]
	fighter.fin_center = entry["fin"]
	fighter.fin_half = Vector2(6.0, 3.5)
	var body: Rect2 = entry["body"]
	if fighter.facing < 0.0:
		body.position.x = -body.end.x
	fighter.body_box = body
	fighter.shot_tip = appearance.tool_tip(fighter.profile, Vector2.ZERO, 1.0,
		fighter.moving_pose, fighter.draw_clock) * MAGNIFY / SCALE + fighter.draw_offset
