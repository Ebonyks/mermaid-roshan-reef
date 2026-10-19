"""One-time rendering integration; fail if the expected baseline is absent."""
from pathlib import Path
import re
root=Path(__file__).resolve().parents[3]
p=root/'scripts/opera_gesture_surface.gd'
t=p.read_text('utf-8')
def function(text,name,body):
    pattern=r'^func '+re.escape(name)+r'\([^\n]*\).*?(?=^func |\Z)'
    value,count=re.subn(pattern,body.rstrip()+'\n\n\n',text,count=1,flags=re.S|re.M)
    assert count==1,name
    return value
assert 'const ChefArt' not in t
t=t.replace('const DRAWS_CARD_BACKING := false','const ChefArt := preload("res://scripts/chef_painted_art.gd")\nvar chef_painted_art: ChefPaintedArt\n\nconst DRAWS_CARD_BACKING := false',1)
t+='''\n\nfunc _chef_art_ref() -> ChefPaintedArt:
\tif chef_painted_art == null:
\t\tchef_painted_art = ChefArt.new()
\t\tchef_painted_art.bind(self)
\treturn chef_painted_art
'''
t=t.replace('''"target_chef": [Vector2(0.31, 0.40), Vector2(0.50, 0.34), Vector2(0.69, 0.40),
\t\tVector2(0.36, 0.58), Vector2(0.50, 0.54), Vector2(0.64, 0.58), Vector2(0.50, 0.70)]''','''"target_chef": [Vector2(0.47, 0.22), Vector2(0.53, 0.22), Vector2(0.42, 0.38),
\t\tVector2(0.58, 0.38), Vector2(0.38, 0.56), Vector2(0.62, 0.56), Vector2(0.50, 0.75)]''',1)
t=t.replace('''\t\t"trace_chef":
\t\t\tvar angle := -PI * 0.75 + amount * TAU
\t\t\treturn Vector2(size.x * 0.50, size.y * 0.54) \\
\t\t\t\t+ Vector2(cos(angle) * size.x * 0.30, sin(angle) * size.y * 0.27)''','''\t\t"trace_chef":
\t\t\treturn Vector2(size.x * 0.50 + sin(amount * TAU * 1.5 - PI * 0.5)
\t\t\t\t* lerpf(12.0, 40.0, amount), lerpf(size.y * 0.18, size.y * 0.82, amount))''',1)
start=t.index('\tif visual_context == "trace_chef":',t.index('func _trace_progress_for_point'))
end=t.index('\tmatch visual_context:',start)
t=t[:start]+'''\tif visual_context == "trace_chef":
\t\treturn clampf(inverse_lerp(size.y * 0.18, size.y * 0.82, point.y), 0.0, 1.0)
'''+t[end:]
old='''\t\t"trace_chef":
\t\t\tvar normalized := (point - Vector2(size.x * 0.50, size.y * 0.54)) \\
\t\t\t\t/ Vector2(size.x * 0.30, size.y * 0.27)
\t\t\treturn absf(normalized.length() - 1.0) <= 0.38'''
new='''\t\t"trace_chef":
\t\t\tvar amount := _trace_progress_for_point(point)
\t\t\treturn point.y >= size.y * 0.15 and point.y <= size.y * 0.85 \\
\t\t\t\tand absf(point.x - _trace_demo_point(amount).x) <= maxf(28.0, size.x * 0.08)'''
assert old in t
t=t.replace(old,new,1)
t=t.replace('func _draw_authored_trace_corridor() -> void:\n','''func _draw_authored_trace_corridor() -> void:
\tif visual_context == "trace_chef":
\t\t_chef_art_ref().draw_frost()
\t\tlast_trace_subject_route = visual_context
\t\treturn
''',1)
t=function(t,'_draw_chef_crank','''func _draw_chef_crank(_progress: float) -> void:
\t_chef_art_ref().draw_stir()''')
t=function(t,'_draw_oven','''func _draw_oven(_center: Vector2) -> void:
\t_chef_art_ref().draw_oven()''')
t=function(t,'_oven_meter_rect','''func _oven_meter_rect() -> Rect2:
\tvar height := size.y * 0.64
\treturn Rect2(size.x * 0.84 - 5.0, size.y * 0.12, height * 0.25, height)''')
t=t.replace('func _draw_anchored_targets() -> void:\n','''func _draw_anchored_targets() -> void:
\tif visual_context == "target_chef":
\t\t_chef_art_ref().draw_targets()
\t\tlast_target_subject_route = visual_context
\t\treturn
''',1)
t=t.replace('func _target_piece_rect(index: int) -> Rect2:\n','''func _target_piece_rect(index: int) -> Rect2:
\tif visual_context == "target_chef":
\t\treturn Rect2(_target_anchor_point(index) - Vector2.ONE * 20.0, Vector2.ONE * 40.0)
''',1)
t=t.replace('func _pour_pitcher_rect() -> Rect2:\n','''func _pour_pitcher_rect() -> Rect2:
\tif visual_context == "pour_chef":
\t\treturn Rect2(pour_x - 70.0, size.y * 0.10 - 10.0, 140.0, 140.0)
''',1)
t=t.replace('func _draw_pour_scene(_center: Vector2) -> void:\n','''func _draw_pour_scene(_center: Vector2) -> void:
\tif visual_context == "pour_chef":
\t\t_chef_art_ref().draw_pour()
\t\tlast_specialist_subject_route = "chef_mixing_bowl"
\t\treturn
''',1)
t=t.replace('\tvar pressing := bool(pose.get("pressing", false))\n\tif _is_candymaker_pour()', '''\tvar pressing := bool(pose.get("pressing", false))
\tif visual_context.ends_with("_chef"):
\t\t_chef_art_ref().draw_hand(at)
\t\treturn
\tif _is_candymaker_pour()''',1)
p.write_text(t,encoding='utf-8')
p=root/'scripts/opera_chef_surface.gd'
t=p.read_text('utf-8')
start=t.index('\t\t\tvar pitcher := _pour_pitcher_rect()')
end=t.index('\t\t\tlast_specialist_subject_route',start)
t=t[:start]+'''\t\t\t_chef_art_ref().draw_pour_stream()
\t\t\t_chef_art_ref().draw_pitcher()
'''+t[end:]
start=t.index('\t\t\tvar guide := _trace_path_points(1.0)')
end=t.index('\t\t\tlast_trace_subject_route',start)
t=t[:start]+'\t\t\t_chef_art_ref().draw_frost_path()\n'+t[end:]
start=t.index('\tif placed > 0:')
end=t.index('\n\nfunc _draw_baked_rows()',start)
t=t[:start]+'''\tif placed > 0:
\t\tvar texture := _art(Cake.STACKED_UNFROSTED_TEXTURE) if placed >= 3 else \\
\t\t\t_chef_art_ref().art("stack_two" if placed == 1 else "stack_four")
\t\tif texture != null:
\t\t\tdraw_texture_rect(texture, _stage_rect(1013.0, CAKE_SCALE), false)
\n'''+t[end:]
t=function(t,'_draw_stack_cap','')
t=t.replace('return Rect2(pour_x - 60.0, 180.0, 120.0, 110.0)', 'return Rect2(pour_x - 60.0, 175.0, 120.0, 120.0)',1)
t=function(t,'_oven_meter_rect','''func _oven_meter_rect() -> Rect2:
\treturn Rect2(709, 263, 30, 120)''')
t=function(t,'_draw_oven','''func _draw_oven(_center: Vector2) -> void:
\t# Keep this room's authored hearth as its sole oven.
\t_chef_art_ref().draw_meter(clampf(oven_t, 0.0, 1.0))
\tlast_specialist_subject_route = "chef_room_hearth"''')
t=t.replace('sin(amount * TAU * 1.5 - PI * 0.5) * 45.0', 'sin(amount * TAU * 1.5 - PI * 0.5) * lerpf(18.0, 45.0, amount)',1)
p.write_text(t,encoding='utf-8')
print('Wired Chef painted rendering and source-aligned trace/target anchors; game state remains on existing surface')
