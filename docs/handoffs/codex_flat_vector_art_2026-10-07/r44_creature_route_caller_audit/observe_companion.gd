extends "res://scripts/companion.gd"
## R44 observes existing source dispatch only; no new world builders or art.
var audit_phase := "boot"
var audit_calls: Dictionary = {}
var audit_events: Array[Dictionary] = []

func _init(main: ReefMain) -> void:
	super(main)

func _mark(method: String, detail: String="") -> void:
	audit_calls[method]=int(audit_calls.get(method,0))+1
	if method not in ["tick","tick_canvas_care","_tick_follower","_tick_room","_follow_ctx"] and audit_events.size()<512:
		audit_events.append({"method":method,"detail":detail,"audit_phase":audit_phase,"game":m.game,"phase":m.g.get("phase",""),"ticks_msec":Time.get_ticks_msec()})

func tick(delta: float) -> void:
	_mark("tick")
	super.tick(delta)

func tick_canvas_care(delta: float) -> void:
	_mark("tick_canvas_care")
	super.tick_canvas_care(delta)

func _follow_ctx() -> bool:
	_mark("_follow_ctx")
	return super._follow_ctx()

func _tick_follower(delta: float) -> void:
	_mark("_tick_follower")
	super._tick_follower(delta)

func _tick_room(delta: float) -> void:
	_mark("_tick_room")
	super._tick_room(delta)

func _build_room() -> void:
	_mark("_build_room")
	super._build_room()

func make_creature() -> Node3D:
	_mark("make_creature")
	return super.make_creature()

func creature_for(d: Dictionary, c: Array[Color]) -> Node3D:
	_mark("creature_for",String(d.get("id","")))
	return super.creature_for(d,c)

func _stuffie_cutout(d: Dictionary, c: Array[Color], target_height: float) -> Node3D:
	_mark("_stuffie_cutout",String(d.get("id",""))+":"+str(target_height))
	return super._stuffie_cutout(d,c,target_height)

func _add_creature_preview(parent: Control, d: Dictionary, box_pos: Vector2, box_size: Vector2, body: Color, accent: Color) -> void:
	_mark("_add_creature_preview",String(d.get("id","")))
	super._add_creature_preview(parent,d,box_pos,box_size,body,accent)
