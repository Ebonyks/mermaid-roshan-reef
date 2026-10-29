from pathlib import Path
import json,re,hashlib,subprocess
r=Path.cwd();s=r/'assets_src/imagegen/job_art_support_careers_20261019';p=r/'scripts/opera_gesture_surface.gd';t=p.read_text();original=t
assert 'func _support_art_ref' not in t
def replace_function(name,body):
 global t
 pattern=r'^func '+name+r'\(.*?(?=^func |\Z)';m=re.search(pattern,t,re.M|re.S);assert m,name;t=t[:m.start()]+body+'\n\n'+t[m.end():]
anchor='const ChefArt := preload("res://scripts/chef_painted_art.gd")';assert anchor in t;t=t.replace(anchor,'const SupportArt := preload("res://scripts/support_career_painted_art.gd")\nvar support_painted_art: SupportCareerPaintedArt\n\n'+anchor)
t+='\n\nfunc _support_art_ref() -> SupportCareerPaintedArt:\n\tif support_painted_art == null:\n\t\tsupport_painted_art = SupportArt.new()\n\t\tsupport_painted_art.bind(self)\n\treturn support_painted_art\n'
for name,signature,call in [('_draw_doctor_crank','progress: float','patient(false, progress)'),('_draw_doctor_basin_subject','','basin()'),('_draw_trace_doctor_subject','','patient(true, trace_journey)'),('_draw_trace_magician_subject','','rope()'),('_draw_magician_portal','','portal()'),('_draw_garden_plant','','garden()'),('_draw_paint_reveal','','paint()')]:replace_function(name,'func '+name+'('+signature+') -> void:\n\t_support_art_ref().'+call+'\n')
replace_function('_paint_canvas_rect','func _paint_canvas_rect() -> Rect2:\n\treturn _support_art_ref().paint_window()\n')
replace_function('_draw_farm_lob','func _draw_farm_lob() -> void:\n\t_support_art_ref().picnic()\n\t_draw_farm_vegetable()\n')
replace_function('_draw_farm_munch_reaction','func _draw_farm_munch_reaction() -> void:\n\t# Authored whole-group catch/chew/happy keys are selected by picnic().\n\tpass\n')
replace_function('_draw_xray_scan','''func _draw_xray_scan() -> void:
\t_draw_target_subject()
\tlast_specialist_subject_route = "xray_device"
\tvar scan_at := xray_scanner_pos
\tif demo_active and not xray_complete:
\t\tscan_at = _demo_finger_pose().get("at", scan_at) as Vector2
\tvar feedback := _support_art_ref().feedback
\tfor index in range(XRAY_SPOTS.size()):
\t\tvar target := _xray_target_center(index)
\t\tif xray_found[index]:
\t\t\tfeedback.pearl(self, target, "full", 28.0)
\t\telif index == xray_found_count:
\t\t\tfeedback.invitation(self, target, 54.0, int(demo_t * 4.0) % 4)
\t_support_art_ref().scanner(scan_at, _xray_scanner_radius(), xray_glow > 0.0)
\t_support_art_ref().pearls(XRAY_SPOTS.size(), xray_found_count)
''')
anchor='\tif visual_context == "trace_chef":\n\t\t_chef_art_ref().draw_frost()';assert anchor in t;t=t.replace(anchor,'''\tif visual_context in ["trace_doctor", "trace_magician"]:
\t\t_draw_authored_trace_subject()
\t\tlast_trace_subject_route = visual_context
\t\treturn
'''+anchor)
anchor='\tif visual_context == "chapter2_basket_delivery":\n\t\t_draw_chapter2_basket_delivery()';assert anchor in t;t=t.replace(anchor,'''\tif visual_context == "push_farmer":
\t\t_support_art_ref().herd()
\t\treturn
'''+anchor)
anchor='\tvar center := size * 0.5\n\tif mode == "pipe":';assert anchor in t;t=t.replace(anchor,'''\tvar center := size * 0.5
\tif visual_context == "basin_doctor" or visual_context in ["lanes_magician", "lanes_painter"]:
\t\tif visual_context == "basin_doctor":
\t\t\t_support_art_ref().basin()
\t\telse:
\t\t\t_support_art_ref().lanes()
\t\tif demo_active:
\t\t\t_draw_demo_finger()
\t\treturn
\tif mode == "pipe":''')
anchor='\tif visual_context.ends_with("_chef"):\n\t\t_chef_art_ref().draw_hand(at)';assert anchor in t;t=t.replace(anchor,'''\tif visual_context.get_slice("_", visual_context.get_slice_count("_") - 1) in ["doctor", "farmer", "magician", "painter"]:
\t\t_support_art_ref().guide(at, pressing)
\t\treturn
'''+anchor)
# Display/input geometry follows source pictures. Preserve the original sampling/progress/tolerance algorithms.
for context,old,call in [('doctor','return Vector2(size.x * lerpf(0.18, 0.82, amount),\n\t\t\t\tsize.y * (0.28 + amount * 0.45 + sin(amount * TAU) * 0.07))','doctor_trace_point(amount)'),('magician','return Vector2(size.x * lerpf(0.16, 0.84, amount),\n\t\t\t\tsize.y * (0.27 + (1.0 - pow(2.0 * amount - 1.0, 2.0)) * 0.42))','rope_point(amount)')]:
 assert old in t;t=t.replace(old,'return _support_art_ref().'+call)
 old='\t\t"trace_'+context+'":\n\t\t\treturn clampf(inverse_lerp(size.x * '+('0.18, size.x * 0.82' if context=='doctor' else '0.16, size.x * 0.84')+', point.x), 0.0, 1.0)'
 new='\t\t"trace_'+context+'":\n\t\t\treturn clampf(inverse_lerp(_trace_demo_point(0.0).x, _trace_demo_point(1.0).x, point.x), 0.0, 1.0)';assert old in t;t=t.replace(old,new)
 pattern=r'(\t\t"trace_'+context+r'":\n)\t\t\tvar amount := inverse_lerp\(.*?\n\t\t\treturn absf\(point.y - expected_y\) <= size.y \* 0.14'
 match=re.search(pattern,t,re.S);assert match,context
 body='\t\t"trace_'+context+'":\n\t\t\tvar amount := inverse_lerp(_trace_demo_point(0.0).x, _trace_demo_point(1.0).x, point.x)\n\t\t\tif amount < 0.0 or amount > 1.0:\n\t\t\t\treturn false\n\t\t\treturn absf(point.y - _trace_demo_point(amount).y) <= size.y * 0.14'
 t=t[:match.start()]+body+t[match.end():]
# Remove only the separate painted cabinet's duplicate slab/arrow and code confetti/fallback.
replace_function('_draw_magic_cabinet','''func _draw_magic_cabinet() -> void:
\tassert(magic_cabinet_closed_texture != null and magic_cabinet_reveal_texture != null)
\tvar bounds := _cabinet_prop_bounds()
\tif cabinet_open_t < 1.0:
\t\tdraw_texture_rect(magic_cabinet_closed_texture,
\t\t\t_contain_rect(magic_cabinet_closed_texture, bounds), false,
\t\t\tColor(1.0, 1.0, 1.0, 1.0 - cabinet_open_t))
\tif cabinet_complete:
\t\tvar alpha := clampf((cabinet_open_t - 0.55) / 0.45, 0.0, 1.0)
\t\tdraw_texture_rect(magic_cabinet_reveal_texture,
\t\t\t_contain_rect(magic_cabinet_reveal_texture, bounds), false, Color(1.0, 1.0, 1.0, alpha))
\tset_meta("support_painted_route", "magician_cabinet")
''')
t=t.replace('if visual_context == "chapter2_basket_fill":\n\t\tvar bounds := Rect2', 'if visual_context == "chapter2_basket_fill" or widget_mover.resource_path.ends_with("castle_banner_rainbow.png"):\n\t\tvar bounds := Rect2')
anchor='func _draw_progress_overlay(texture: Texture2D, progress: float, horizontal: bool) -> void:\n';assert anchor in t;t=t.replace(anchor,anchor+'''\tif texture.resource_path.ends_with("castle_banner_rainbow.png"):
\t\tvar bounds := _contain_rect(texture, Rect2(Vector2.ZERO, size))
\t\tdraw_texture_rect(texture, bounds, false, Color(1.0, 1.0, 1.0, clampf(progress, 0.0, 1.0)))
\t\treturn
''')
p.write_text(t,encoding='utf-8')
# Keep the original left-to-right trace direction.
p=r/'scripts/support_career_painted_art.gd';v=p.read_text();v=v.replace('lerpf(0.93, 0.79, amount)','lerpf(0.79, 0.93, amount)');p.write_text(v,encoding='utf-8')
p=r/'scripts/opera_world_hotspot_2d.gd';v=p.read_text();anchor='\tvar local_rect := Rect2(-draw_size * 0.5, draw_size)';assert anchor in v;v=v.replace(anchor,'''\tif object_texture != null and source_path.ends_with("castle_banner_rainbow.png"):
\t\tvar factor := minf(draw_size.x / object_texture.get_width(), draw_size.y / object_texture.get_height())
\t\tdraw_size = object_texture.get_size() * factor
'''+anchor);p.write_text(v,encoding='utf-8')
p=r/'scripts/opera_career_world_2d.gd';v=p.read_text();old='career_id in ["teacher", "geologist", "chef", "nursery"]';assert old in v;v=v.replace(old,'career_id in ["teacher", "geologist", "chef", "nursery", "doctor", "farmer", "magician", "painter"]');p.write_text(v,encoding='utf-8')
p=r/'scripts/opera_world_backdrop_2d.gd';v=p.read_text();v=v.replace('["chef", "nursery", "boxer"]','["chef", "nursery", "boxer", "doctor", "farmer", "magician", "painter"]');v=v.replace('["nursery", "boxer"]','["nursery", "boxer", "doctor", "farmer", "magician", "painter"]');p.write_text(v,encoding='utf-8')
def functions(v):return {m[1]:m[0] for m in re.finditer(r'^func ([^(]+).*?(?=^func |\Z)',v,re.M|re.S)}
before=functions(original);after=functions(t);changed=[n for n in before if before[n]!=after.get(n)];geometry=['_trace_demo_point','_trace_progress_for_point','_trace_corridor_contains','_paint_canvas_rect'];note={'baseline':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'changed_original_functions':changed,'new_functions':sorted(set(after)-set(before)),'explicit_source_input_geometry_alignment':geometry,'unchanged_original_functions':[n for n in before if n not in changed],'limits':'Render wiring candidate. Input ownership, progression thresholds/tolerances, phase/timer/save/reward handlers remain byte-identical except four named geometry helpers; actual source-context/contact/fullmotion/passive/device/owner not accepted. Painter cloud cells map actual painting interior/full-banner aspect so all required visible cells remain reachable.'};(s/'render_scope01.json').write_text(json.dumps(note,indent=2)+'\n')
p=r/'design/audit_impacts/job-art-support-careers-20261019.json';d=json.loads(p.read_text());d['scope']+=' Painter paint-cell sampling now follows the actual framed painting interior (or whole aspect-correct ChapterTwo banner) through _paint_canvas_rect; original10x6cells/requiredcount/touchownership/signals preserved. Four explicit source geometry helpers and render-only changes are inventoried in render_scope01.json, not claimed mechanically identical.';d['files']=sorted(set(d['files']+['scripts/support_career_painted_art.gd','scripts/opera_gesture_surface.gd','scripts/opera_world_hotspot_2d.gd','scripts/opera_career_world_2d.gd','scripts/opera_world_backdrop_2d.gd']+[x.relative_to(r).as_posix() for x in s.rglob('*') if x.is_file()]+[x.relative_to(r).as_posix() for x in (r/'assets/opera/worlds/support_quality_20261019').glob('*.png')]));p.write_text(json.dumps(d,indent=2)+'\n')
print('Wired candidate',len(changed),'changed original functions; explicit source geometry',geometry)
