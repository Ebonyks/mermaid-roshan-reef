from pathlib import Path
import hashlib,json
r=Path.cwd();s=r/'assets_src/imagegen/job_art_boxer_20261019';p=r/'scripts/opera_boxing_surface.gd';t=p.read_text('utf-8');before=t
def repl(name,body):
 global t
 a=t.index('func '+name+'(');b=t.find('\nfunc ',a+5)
 if b<0:b=len(t)
 t=t[:a]+body.rstrip()+'\n\n'+t[b:]
# These loaded flat markers are replaced entirely; no dormant texture is
# misreported as visible painted art.
for text in ['const TARGET_PATH := \\\n\t"res://assets/opera/worlds/widgets/widget_target_boxer_mark.png"\n','const TELEGRAPH_PATH := \\\n\t"res://assets/opera/worlds/props/fx_telegraph_ring.png"\n','var _target_texture: Texture2D = null\n','var _telegraph_texture: Texture2D = null\n','\t\t_target_texture = _load_texture(TARGET_PATH)\n','\t\t_telegraph_texture = _load_texture(TELEGRAPH_PATH)\n']:
 assert text in t,text;t=t.replace(text,'',1)
a='var _mitts_texture: Texture2D = null';assert a in t;t=t.replace(a,'var _painted_gloves: Array[Texture2D] = []\nvar _feedback_pictures: PaintedFeedbackArt = null\n'+a,1)
a='func _load_resources() -> void:\n';assert a in t;t=t.replace(a,a+'''	if _painted_gloves.is_empty():
		_painted_gloves.append(_load_texture("res://assets/opera/worlds/boxer_quality_20261019/glove_left.png"))
		_painted_gloves.append(_load_texture("res://assets/opera/worlds/boxer_quality_20261019/glove_right.png"))
''',1)
repl('_draw','''func _draw() -> void:
	# Authored pictures retain their own light. Invitation pixels sit behind
	# the actual mitt, opponent or buckle, never as ink over their faces.
	_draw_progress_lights()
	match mode:
		"boxing_guide":
			for hand in range(2):
				_draw_target(guide_target_position(hand), _guide_done[hand])
			_draw_mitts()
		"boxing_jab":
			_draw_target(active_target_position(), false)
			_draw_mitts()
		"boxing_guard":
			_draw_counter()
		"boxing_imp":
			if imp_is_open() or _imp_state == "windup":
				_draw_target(active_target_position(), false)
			_draw_boxer_imp()
		"boxing_belt":
			_draw_belt()
	for hand in range(2):
		_draw_glove(hand)
	if _impact_t > 0.0:
		_draw_impact()
	if hit_feedback_t > 0.0:
		_draw_friendly_hit()
	if demo_active and not completion_accepted:
		_draw_demo()''')
repl('_draw_progress_lights','''func _pictures() -> PaintedFeedbackArt:
	if _feedback_pictures == null:
		_feedback_pictures = PaintedFeedbackArt.new()
	return _feedback_pictures


func _draw_progress_lights() -> void:
	var count := _mode_goal()
	var step := 34.0
	var start_x := (size.x - step * float(count - 1)) * 0.5
	var working := not touch_owners.is_empty() \
		and maxf(_glove_depth(0), _glove_depth(1)) > 0.1
	for index in range(count):
		var at := Vector2(start_x + float(index) * step, 28.0)
		var state := "full" if index < _round_index else (
			"filling" if index == _round_index and working else "empty")
		_pictures().pearl(self, at, state, 30.0)''')
# Retire the now-unreferenced vector lane renderer; the painted hand shows the
# actual same start-to-target route without adding code objects.
repl('_draw_punch_lanes','')
repl('_draw_target','''func _draw_target(at: Vector2, completed: bool) -> void:
	var key := int(floor(_elapsed / 0.22)) % 4
	_pictures().invitation(self, at, _target_radius() * 2.2, key, completed)''')
repl('_draw_counter','''func _draw_counter() -> void:
	var target := guard_target_position(_guard_side)
	_draw_target(target, false)
	var origin := Vector2(size.x * 0.5, size.y * 0.18)
	var amount := clampf(1.0 - _counter_t / COUNTER_SECONDS, 0.0, 1.0)
	var eased := amount * amount * (3.0 - 2.0 * amount)
	var counter := origin.lerp(target, eased)
	_paint_glove(1, counter, 160.0 * (0.78 + amount * 0.25), 0.0)''')
repl('_draw_boxer_imp','''func _draw_boxer_imp() -> void:
	var texture := _imp_textures.get(_imp_state) as Texture2D
	if texture == null:
		texture = _imp_textures.get("idle") as Texture2D
	var side := minf(380.0, size.y * 0.57)
	var bob := sin(_elapsed * 3.4) * 5.0 if _imp_state in ["idle", "taunt"] else 0.0
	var center := Vector2(size.x * 0.5, size.y * 0.36 + bob)
	if texture != null:
		draw_texture_rect(texture,
			Rect2(center - Vector2.ONE * side * 0.5, Vector2.ONE * side), false)''')
repl('_draw_belt','''func _draw_belt() -> void:
	_draw_target(active_target_position(), finished)
	var rect := _belt_rect()
	if _belt_texture != null:
		draw_texture_rect(_belt_texture, rect, false)''')
repl('_draw_glove','''func _paint_glove(hand: int, at: Vector2, side: float, angle: float) -> void:
	if hand < 0 or hand >= _painted_gloves.size() or _painted_gloves[hand] == null:
		return
	draw_set_transform(at, angle)
	draw_texture_rect(_painted_gloves[hand],
		Rect2(-Vector2(0.49, 0.43) * side, Vector2.ONE * side), false)
	draw_set_transform(Vector2.ZERO)


func _draw_glove(hand: int) -> void:
	var position := glove_positions[hand]
	var depth := _glove_depth(hand)
	var scale_value := 0.92 + depth * 0.38
	if _impact_t > 0.0 and position.distance_to(_impact_position) < 130.0:
		scale_value += sin((_impact_t / 0.52) * PI) * 0.10
	var angle := (-0.08 if hand == 0 else 0.08) \
		+ clampf((pointer_pos.x - position.x) / maxf(1.0, size.x), -0.08, 0.08)
	# Separate original left/right art: no mirror or independently deformed cuff.
	_paint_glove(hand, position, 168.0 * scale_value, angle)''')
repl('_draw_impact','''func _draw_impact() -> void:
	var amount := 1.0 - clampf(_impact_t / 0.52, 0.0, 1.0)
	if _puff_texture != null:
		var side := 130.0 + amount * 90.0
		draw_texture_rect(_puff_texture,
			Rect2(_impact_position - Vector2.ONE * side * 0.5, Vector2.ONE * side),
			false, Color(1.0, 1.0, 1.0, 1.0 - amount * 0.55))''')
repl('_draw_friendly_hit','''func _draw_friendly_hit() -> void:
	var amount := clampf(hit_feedback_t / 0.78, 0.0, 1.0)
	var center := Vector2(size.x * 0.5, size.y * 0.64)
	if _puff_texture != null:
		var side := 170.0 + (1.0 - amount) * 60.0
		draw_texture_rect(_puff_texture,
			Rect2(center - Vector2.ONE * side * 0.5, Vector2.ONE * side),
			false, Color(1.0, 1.0, 1.0, amount))''')
repl('_draw_demo','''func _draw_demo() -> void:
	var cycle := fmod(demo_t, 2.4) / 2.4
	var hand := int(floor(fmod(demo_t, 4.8) / 2.4))
	var start := glove_rest_position(hand)
	var target := active_target_position()
	if mode == "boxing_guide":
		target = guide_target_position(hand)
	elif mode == "boxing_guard":
		hand = _guard_side
		start = glove_rest_position(hand)
		target = guard_target_position(hand)
	var travel := clampf(cycle / 0.72, 0.0, 1.0)
	travel = travel * travel * (3.0 - 2.0 * travel)
	var at := start.lerp(target, travel)
	var texture := _pictures().art("res://assets/opera/worlds/teacher/guide_hand.png")
	if texture != null:
		var side := 58.0
		draw_set_transform(at, PI)
		draw_texture_rect(texture, Rect2(-Vector2(0.436523, 0.986328) * side,
			Vector2.ONE * side), false)
		draw_set_transform(Vector2.ZERO)''')
repl('_draw_star','')
# Remove only color constants whose last rendering consumer was retired.
for name in ['GLOVE_CORAL','GLOVE_LIGHT','GLOVE_SHADOW','CUFF_TEAL','CUFF_CORAL','PEARL_GOLD','INK','BUBBLE']:
 lines=t.splitlines();hits=[i for i,line in enumerate(lines) if name in line]
 if len(hits)==1 and lines[hits[0]].startswith('const '+name+' := '):lines.pop(hits[0]);t='\n'.join(lines)+'\n'
p.write_text(t,encoding='utf-8')
# Non-rendering functions must be byte-identical to the integrated specialist.
def funcs(text):
 import re
 matches=list(re.finditer(r'^func (\w+)\(',text,re.M));return {m.group(1):text[m.start():matches[i+1].start() if i+1<len(matches) else len(text)].strip() for i,m in enumerate(matches)}
a=funcs(before);b=funcs(t);allowed={'_load_resources','_draw','_draw_progress_lights','_draw_punch_lanes','_draw_target','_draw_counter','_draw_boxer_imp','_draw_belt','_draw_glove','_draw_impact','_draw_friendly_hit','_draw_demo','_draw_star'}
changed=[name for name in a if a[name]!=b.get(name)]
assert set(changed)<=allowed,changed
assert all(b[name]==body for name,body in a.items() if name not in allowed)
(s/'render_scope.json').write_text(json.dumps({'changed_existing_functions':changed,'unchanged_behavior':'Every original non-render/resource function compared byte-identical before/after, including touch ownership, forward thresholds, timers, state machine, no-loss/misses, progress signals, close/cancel.','new_functions':['render-only _pictures','render-only _paint_glove'],'glove_registration':{'native_canvas':[1024,1024],'runtime_canvas':[512,512],'knuckle_control_uv':[0.49,0.43],'base_draw_side':168,'transform':'Original rigid angle and uniform depth/impact scale; separate left/right native pictures, no mirror/warp.'},'shared_effects':'2ring/open+5pearlImageGen calls; initialempty/filling role rejects preserved. No remaining plain primitives in specialist drawing.','native_context_review':'PENDING actual Mobile source/neighbor/contact/two-aspect review; no4.5score inferred from wiring.'},indent=2)+'\n')
p=r/'design/audit_impacts/job-art-nursery-20261019.json';d=json.loads(p.read_text());d['files']=sorted(set(d['files']+[f.relative_to(r).as_posix() for f in s.rglob('*') if f.is_file()]));p.write_text(json.dumps(d,indent=2)+'\n')
print('Boxer painted rendering wired; all non-render/resource functions byte-identical, current art/runtime checks pending')
