from pathlib import Path
import json
r=Path.cwd();s=r/'assets_src/imagegen/job_art_nursery_20261019'
p=r/'scripts/nursery_painted_art.gd';t=p.read_text('utf-8-sig');start=t.index('\tvar label :=');end=t.index('\nfunc draw_bedtime()',start)
t=t[:start]+'''\t# Four disjoint windows preserve the original shell label without a hole
	# polygon accidentally being filled by Canvas drawing.
	var clear_regions := [Rect2(0, 112, 256, 29), Rect2(0, 141, 107, 64),
		Rect2(173, 141, 83, 64), Rect2(0, 205, 256, 20)]
	for region: Rect2 in clear_regions:
		var clipped_region := region.intersection(Rect2(0, 112, 256, bottom - 112.0))
		if not clipped_region.has_area():
			continue
		window = PackedVector2Array([clipped_region.position,
			Vector2(clipped_region.end.x, clipped_region.position.y), clipped_region.end,
			Vector2(clipped_region.position.x, clipped_region.end.y)])
		for glass_only: PackedVector2Array in Geometry2D.intersect_polygons(
				PackedVector2Array(GLASS), window):
			var vertices := PackedVector2Array()
			var uvs := PackedVector2Array()
			for point: Vector2 in glass_only:
				vertices.append(destination.position + point / 256.0 * destination.size)
				uvs.append(point / 256.0)
			surface.draw_polygon(vertices, PackedColorArray([Color.WHITE]), uvs,
				art("bottle_empty"))
''' +t[end:];p.write_text(t,encoding='utf-8')
p=r/'scripts/opera_gesture_surface.gd';t=p.read_text('utf-8');anchor='var nursery_bottle_texture: Texture2D = null';assert anchor in t;t=t.replace(anchor,'var nursery_painted_art: NurseryPaintedArt = null\n'+anchor,1)
def replace_func(text,name,body):
 start=text.index('func '+name+'(');end=text.find('\nfunc ',start+5);assert end>=0,name
 return text[:start]+body.rstrip()+'\n\n'+text[end:]
t=replace_func(t,'_draw_nursery_feed_scene','''func _draw_nursery_feed_scene(_center: Vector2) -> void:
	_nursery_art().draw_feed()''')
t=replace_func(t,'_draw_nursery_bedtime_scene','''func _draw_nursery_bedtime_scene(_center: Vector2) -> void:
	_nursery_art().draw_bedtime()''')
t=replace_func(t,'_draw_nursery_burp_scene','''func _draw_nursery_burp_scene(_center: Vector2) -> void:
	_nursery_art().draw_burp()''')
t=replace_func(t,'_draw_nursery_context','''func _draw_nursery_context(_center: Vector2) -> void:
	if visual_context == "nursery_wash":
		_nursery_art().draw_wash()


func _nursery_art() -> NurseryPaintedArt:
	if nursery_painted_art == null:
		nursery_painted_art = NurseryPaintedArt.new()
		nursery_painted_art.bind(self)
	return nursery_painted_art''')
# The pose now names the nipple point. State/progress/approach remain identical;
# the conservative whole-sprite bound follows that registered drawing.
t=replace_func(t,'_nursery_feed_bottle_rect','''func _nursery_feed_bottle_rect(active: bool) -> Rect2:
	var pose := _nursery_feed_bottle_pose(active)
	var tip: Vector2 = pose["position"]
	var side := minf(size.x, size.y) * 0.34
	var center := tip + ((Vector2.ONE * 0.5 - NurseryPaintedArt.BOTTLE_NIPPLE_UV)
		* side).rotated(float(pose["rotation"]))
	return Rect2(center - Vector2.ONE * side * 0.5, Vector2.ONE * side)''')
old='var baby := _nursery_baby_center(1) - Vector2(0.0, size.y * 0.07)';new='var baby := _nursery_baby_center(1) + Vector2(0.0, size.y * 0.10)';assert old in t;t=t.replace(old,new,1)
anchor='\tvar pressing := bool(pose.get("pressing", false))\n';assert anchor in t
t=t.replace(anchor,anchor+'''	if visual_context.begins_with("nursery_") or visual_context in ["pour_nursery", "push_nursery"]:
		_nursery_art().draw_guide(at, pressing)
		return
''',1)
anchor='\t\t"hold":\n\t\t\tif _is_nursery_feed_context():';assert anchor in t
# The hand indicates the actual source basin, without pretending a demo earns wash progress.
t=t.replace(anchor,'''\t\t"hold":
			if visual_context == "nursery_wash":
				var wash := _nursery_art().wash_rect()
				at = wash.position + wash.size * Vector2(0.73, 0.58)
				pressing = true
			elif _is_nursery_feed_context():''',1)
p.write_text(t,encoding='utf-8')
# Explicit older-care whole poses: animator owns texture only and restores the
# normal atlas automatically on its next play/show_pose call.
p=r/'scripts/opera_roshan_actor.gd';t=p.read_text('utf-8');anchor='func stop() -> void:';assert anchor in t
t=t.replace(anchor,'''func show_authored_nursery_pose(texture: Texture2D, frame: int) -> void:
	if _career_key != "nursery" or not _has_target() or texture == null:
		return
	current_animation = "work"
	current_frame = clampi(frame, 0, 7)
	_frame_elapsed = 0.0
	_playing = false
	_one_shot = false
	set_process(false)
	_target.texture = texture


'''+anchor,1);p.write_text(t,encoding='utf-8')
p=r/'scripts/opera_career_world_2d.gd';t=p.read_text('utf-8');anchor='func _play_roshan_task_pose(phase: Dictionary) -> void:\n';assert anchor in t
t=t.replace(anchor,anchor+'''	if career_id == "nursery" and String(phase.get("name", "")) in ["FEED", "BURP"]:
		_update_nursery_care_pose(phase)
		return
''',1)
anchor='func _widget_template(phase: Dictionary) -> String:';assert anchor in t
t=t.replace(anchor,'''func _update_nursery_care_pose(phase: Dictionary) -> void:
	if not is_instance_valid(player_animator) or surface == null:
		return
	var amount := phase_progress / maxf(0.1, float(phase.get("goal", 1.0)))
	var frame := clampi(floori(amount * 8.0), 0, 7)
	var texture := surface._nursery_art().art("care_%02d" % frame)
	player_animator.show_authored_nursery_pose(texture, frame)


'''+anchor,1)
old='if career_id == "boxer" and player_actor != null:\n\t\tplayer_actor.visible = true';assert old in t;t=t.replace(old,'if career_id in ["boxer", "nursery"] and player_actor != null:\n\t\tplayer_actor.visible = true',1)
anchor='\tif phase_index >= _finale_start() or competition.is_cooperative():\n\t\t_stage_room_finale_partner()';assert anchor in t
t=t.replace(anchor,'''	if career_id == "nursery" and String(phase.get("visual_context", "")) == "nursery_wash" \
			and player_actor != null:
		# The approved connected wash picture already includes Roshan and basin.
		# Draw her exactly once, restoring the stage actor when the next phase arms.
		player_actor.visible = false
'''+anchor,1)
anchor='\t_performance_tick(delta)\n';assert anchor in t;t=t.replace(anchor,anchor+'''	if career_id == "nursery" and task_open and phase_index < phases.size():
		var nursery_phase := phases[phase_index] as Dictionary
		if String(nursery_phase.get("name", "")) in ["FEED", "BURP"]:
			_update_nursery_care_pose(nursery_phase)
''',1)
p.write_text(t,encoding='utf-8')
# Catch: all catching/mercy/live-input logic stays exact. Replace only drawing
# and source paths; support anchors follow the authored baby bottom and palms.
p=r/'scripts/opera_nursery_catch.gd';t=p.read_text('utf-8');t=t.replace('var pillows_texture: Texture2D = null','var pillows_texture: Texture2D = null\nvar painted_art: NurseryPaintedArt = null',1)
t=t.replace('res://assets/opera/worlds/widgets/widget_catch_nursery_cradle.png','res://assets/opera/worlds/nursery_quality_20261019/cradle.png').replace('res://assets/opera/worlds/widgets/widget_catch_nursery_pillows.png','res://assets/opera/worlds/nursery_quality_20261019/pillows.png')
anchor='\tfor path: String in BABY_PATHS:';assert anchor in t;t=t.replace(anchor,'\tpainted_art = NurseryPaintedArt.new()\n\tpainted_art.bind(self)\n'+anchor,1)
start=t.index('func _draw() -> void:')
t=t[:start]+'''func _draw() -> void:
	# One complete painted mobile, not code rods/dots or a separate card.
	if painted_art != null:
		var mobile_side := minf(size.x * 0.28, size.y * 0.44)
		painted_art.picture("mobile", Rect2(
			Vector2(size.x * 0.5 - mobile_side * 0.5, 0), Vector2.ONE * mobile_side))
	if pillows_texture != null:
		var ratio := float(pillows_texture.get_height()) / float(pillows_texture.get_width())
		var height := size.x * ratio
		draw_texture_rect(pillows_texture,
			Rect2(0, size.y * PILLOW_Y - height * 0.5, size.x, height), false)
	for landing: Dictionary in safe_landings:
		var extent := minf(76.0, size.x * 0.21)
		var fade := clampf(float(landing.get("time", 0.0)) / 0.35, 0.0, 1.0)
		_draw_baby(int(landing.get("texture", 0)),
			Vector2(float(landing.get("x", 0.5)) * size.x,
				size.y * PILLOW_Y - extent * 0.43), extent, fade)
	var catch_point := Vector2(catcher_x * size.x, size.y * 0.80)
	var catch_radius := minf(58.0, size.x * 0.15)
	if cradle_texture != null:
		draw_texture_rect(cradle_texture,
			Rect2(catch_point - Vector2(catch_radius, catch_radius * 1.55),
				Vector2.ONE * catch_radius * 2.0), false)
	if input_live_t <= 0.0 and painted_art != null:
		painted_art.draw_guide(catch_point, false)
	for entry: Dictionary in fallers:
		var extent := minf(86.0, size.x * 0.23)
		_draw_baby(int(entry.get("texture", 0)),
			Vector2(float(entry.get("x", 0.5)) * size.x,
				float(entry.get("y", 0.0)) * size.y - extent * 0.27), extent)
	var shown := mini(settled.size(), 5)
	for index in range(shown):
		var spread := float(index) - float(shown - 1) * 0.5
		_draw_baby(settled[index], catch_point + Vector2(spread * 20.0, -42.0 * 0.43), 42.0)
''';p.write_text(t,encoding='utf-8')
# Record exact implemented behavior/source boundaries, no acceptance inferred.
p=s/'job_cards.json';d=json.loads(p.read_text());d['actual_call_accounting']={'total':11,'crib':1,'quilt_all_keys_including_reject':4,'bottle_all_states_including_rejects_and_guide':4,'pat_hand_including_reject':2,'model_seed_cost':'unexposed; no paid API/CLI','cleanup_minutes':'Not instrumented; no invented actual time.'};d['method_change']='Three half-bottle generations retained rejected for fill-height, one empty retained selected. Stop at4aggregate bottle calls. Original full bottle exterior/label and registered ImageGen empty glass are rendered with disjoint textured cavity windows. No generated half accepted, no procedural replacement art.';d['reviews']='PENDING actual-source/current Mobile/frame/contact review, full exact-engine and device/child/owner gates; no4.5score yet.';p.write_text(json.dumps(d,indent=2)+'\n')
print('Nursery painted rendering wired; input/reward/save/catch physics unchanged; current context and engine checks pending')
