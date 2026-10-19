from pathlib import Path
import json,re,shutil,hashlib
r=Path.cwd();s=r/'assets_src/imagegen/job_art_support_careers_20261019';p=r/'scripts/support_career_painted_art.gd';versions=s/'source_versions';versions.mkdir(exist_ok=True);assert not (versions/'support_career_painted_art_pre_extra01.gd.txt').exists();shutil.copyfile(p,versions/'support_career_painted_art_pre_extra01.gd.txt');t=p.read_text('utf-8')
def function(name,body):
 global t
 match=re.search(r'^func '+name+r'\(.*?(?=^func |\Z)',t,re.M|re.S);assert match,name;t=t[:match.start()]+body+'\n\n'+t[match.end():]
t=t.replace('Vector2(surface.size.x * 0.84, surface.size.y * 0.84)','Vector2(surface.size.x * 1.12, surface.size.y * 1.12)').replace('surface.size * Vector2(0.5, 0.49) - bed_size * 0.5','surface.size * Vector2(0.5, 0.47) - bed_size * 0.5')
function('rope','''func rope() -> void:
\tvar reference := rope_rect()
\tvar amount := value("trace_journey")
\tvar key := 2 if complete() or amount >= 0.999 else (1 if amount >= 0.45 else 0)
\t# Common POT canvas pads the exact original rope by256x64; doubled whole
\t# destination preserves its original visible body, sockets and input path.
\tvar destination := Rect2(reference.get_center() - reference.size, reference.size * 2.0)
\tsurface.draw_texture_rect(art("widget_rope_magician_" + str(key)), destination, false)
\tpearls(3, progress_key(amount))
\tsurface.set_meta("support_painted_route", "magician_rope")
\tsurface.set_meta("support_painted_key", key)
''')
function('herd','''func herd() -> void:
\tvar finish: Vector2 = surface.call("_long_push_end")
\tvar amount := value("widget_fill")
\tvar side := minf(surface.size.y * 0.72, surface.size.x * 0.28)
\tpicture("widget_barn_gate_" + ("open" if amount >= 0.98 or complete() else "closed"),
\t\tVector2(finish.x, surface.size.y * 0.48), side)
\tvar group: Rect2 = surface.call("_long_push_group_rect", amount)
\tvar key := "b" if amount > 0.0 and amount < 0.999 and int(amount * 12.0) % 2 == 1 else "a"
\t# Two complete authored step poses, with fixed heads and changing hoof support.
\t# Their measured opaque footprint stays within the old group rectangle.
\tpicture("widget_herd_farmer_" + key, group.get_center(), maxf(group.size.x,group.size.y) * 1.20)
\tsurface.set("last_contextual_draw_route", "push:push_farmer")
\tsurface.set_meta("support_painted_route", "farmer_herd")
\tsurface.set_meta("support_painted_key", key)
''')
# Draw the invitation behind the complete object; no circles or translucent duplicate portraits.
t=t.replace('var magician := String(surface.get("visual_context")) == "lanes_magician"','var magician := String(surface.get("visual_context")) == "lanes_magician"\n\tvar doctor := String(surface.get("visual_context")) == "lanes_doctor"')
old='\t\tif magician:\n\t\t\tpicture("widget_hat_magician_" + str(index % 3), at, side)';new='''\t\tif index == target and (value("choice_flash") > 0.0 or bool(surface.get("demo_active")) or complete()):
\t\t\tfeedback.invitation(surface, at, side * 1.18, int(value("demo_t") * 4.0) % 4)
\t\tif doctor:
\t\t\tvar states := ["concerned", "sleepy", "happy_cap"]
\t\t\tpicture("widget_find_doctor_" + String(states[index % 3]), at, side)
\t\telif magician:
\t\t\tpicture("widget_hat_magician_" + str(index % 3), at, side)''';assert old in t;t=t.replace(old,new)
old='\t\tif index == target and (value("choice_flash") > 0.0 or bool(surface.get("demo_active")) or complete()):\n\t\t\tfeedback.invitation(surface, at, side * 1.18, int(value("demo_t") * 4.0) % 4)\n\tif shuffle:';assert old in t;t=t.replace(old,'\tif shuffle:')
t=t.replace('"magician_hats" if magician else "painter_gallery"','"magician_hats" if magician else ("doctor_find" if doctor else "painter_gallery")')
t=t.replace('func clipped_cloud(texture: Texture2D, destination: Rect2, window: Rect2) -> void:','func clipped_cloud(texture: Texture2D, destination: Rect2, window: Rect2, alpha: float = 1.0) -> void:').replace('surface.draw_texture_rect_region(texture, clipped, uv)','surface.draw_texture_rect_region(texture, clipped, uv, Color(1.0, 1.0, 1.0, alpha))')
function('paint','''func paint() -> void:
\tvar texture: Texture2D = surface.get("paint_reveal_texture")
\tassert(texture != null)
\tsurface.draw_texture_rect(texture, painting_rect(), false)
\tvar window := paint_window()
\tvar cells: Array = surface.get("paint_cells")
\tvar positions: Array[Vector2] = [Vector2(0.18,0.16), Vector2(0.76,0.14),
\t\tVector2(0.47,0.43), Vector2(0.08,0.78), Vector2(0.88,0.72), Vector2(0.47,0.92)]
\tvar totals: Array[int] = [0,0,0,0,0,0]
\tvar cleared: Array[int] = [0,0,0,0,0,0]
\t# Existing60touch cells still own all earning. Their spatial regions fade
\t# six whole irregular puffs, rather than repeating a puff sixty times.
\tfor row in range(6):
\t\tfor col in range(10):
\t\t\tvar normalized := Vector2((float(col)+0.5)/10.0,(float(row)+0.5)/6.0)
\t\t\tvar nearest := 0
\t\t\tvar distance := INF
\t\t\tfor index in range(positions.size()):
\t\t\t\tvar candidate := normalized.distance_squared_to(positions[index])
\t\t\t\tif candidate < distance:
\t\t\t\t\tdistance = candidate
\t\t\t\t\tnearest = index
\t\t\ttotals[nearest] += 1
\t\t\tif cells[row * 10 + col]:
\t\t\t\tcleared[nearest] += 1
\tif not bool(surface.get("paint_complete")):
\t\tvar scales: Array[float] = [1.05,0.94,1.12,1.00,1.12,1.07]
\t\tfor index in range(positions.size()):
\t\t\tvar alpha := 1.0 - float(cleared[index]) / maxf(1.0,float(totals[index]))
\t\t\tif alpha <= 0.001:
\t\t\t\tcontinue
\t\t\tvar side := maxf(window.size.x,window.size.y) * scales[index]
\t\t\tvar center := window.position + window.size * positions[index]
\t\t\tclipped_cloud(art("widget_paint_cloud_" + str(index)),
\t\t\t\tRect2(center - Vector2.ONE * side * 0.5,Vector2.ONE * side),window,alpha)
\tvar required: int = surface.call("_paint_required_cells")
\tpearls(8,mini(8,int(8.0 * value("paint_covered") / maxf(1,required))),0.94)
\tsurface.set_meta("support_painted_route", "painter_cloud_reveal")
''')
p.write_text(t,encoding='utf-8');p=r/'scripts/opera_gesture_surface.gd';v=p.read_text('utf-8');shutil.copyfile(p,versions/'opera_gesture_surface_pre_extra01.gd.txt');v=v.replace('visual_context in ["lanes_magician", "lanes_painter"]','visual_context in ["lanes_magician", "lanes_painter", "lanes_doctor"]');old='\tif visual_context.get_slice("_", visual_context.get_slice_count("_") - 1) in ["doctor", "farmer", "magician", "painter"]:';assert old in v;v=v.replace(old,'\tif mode in ["garden_plant", "magic_cabinet", "paint_reveal"] or visual_context == "magic_vanish" \\\n\t\t\tor visual_context.get_slice("_", visual_context.get_slice_count("_") - 1) in ["doctor", "farmer", "magician", "painter"]:');p.write_text(v,encoding='utf-8')
p=r/'design/audit_impacts/job-art-support-careers-20261019.json';d=json.loads(p.read_text('utf-8'));d['scope']+=' Extra53runtimePNG technical53/53C2PASS (55builtin calls, allnative/rejects retained). Bed uniform fit1.12/currentcentre.47 contains originalfiveholes; HERDtwo whole-group gait keys replace tiny clones within unchanged group/hit footprint; FINDthree full-opacity portraits replace torn/ghosted atlas; six whole puffs each drawnonce/faded by original60earnedcells instead of60repetitions; ropehalf/full endknots actually open with exactoriginalbody/socket mapping on1024x256POT canvas. No warp/paint/alpha cleanup in technicalderivation; originalpixels preserved. Actualnewcontext/motion/finalgates still pending.';d['files']=sorted(set(d['files']+[x.relative_to(r).as_posix() for x in s.rglob('*') if x.is_file()]+[x.relative_to(r).as_posix() for x in (r/'assets/opera/worlds/support_quality_20261019').glob('*') if x.is_file()]));p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8');print('Wired extra pictures and render-fit repairs; no input-earning edits in this step',flush=True)
