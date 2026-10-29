from pathlib import Path
import hashlib,json
r=Path.cwd();s=r/'assets_src/imagegen/job_art_support_careers_20261019';p=r/'scripts/opera_gesture_surface.gd';t=p.read_text(encoding='utf-8');original=t
def replace(old,new):
 global t
 assert t.count(old)==1,old[:120]
 t=t.replace(old,new)
replace('\t\t# Reuse Lamb-a\'s approved Seek identity, preserving the atlas pixels.\n\t\tvar lamba_atlas := AtlasTexture.new()\n\t\tlamba_atlas.atlas = _load_widget_texture(\n\t\t\t"res://assets/minigames/seek/lamma_animation.png")\n\t\tlamba_atlas.region = Rect2(0, 0, 256, 256)\n\t\tmagic_vanish_lamba_texture = lamba_atlas', '\t\t# Same source-bound Lamb-a identity, with the commissioned painted finish.\n\t\tmagic_vanish_lamba_texture = _support_art_ref().art("widget_lamba_magician")')
replace('\t\tmagic_cabinet_reveal_texture = _load_widget_texture(\n\t\t\t"res://assets/opera/worlds/widgets/widget_magic_cabinet_reveal.png")','\t\tmagic_cabinet_reveal_texture = _support_art_ref().art("widget_cabinet_magician_reveal")')
replace('func _draw_anchored_targets() -> void:\n','func _draw_anchored_targets() -> void:\n\tif visual_context == "target_farmer":\n\t\t_support_art_ref().picnic_targets()\n\t\treturn\n')
replace('func _draw_magic_vanish_scene(center: Vector2) -> void:\n\t_draw_causal_backdrop(Color("#20183f"), Color("#3b2557"))','func _draw_magic_vanish_scene(center: Vector2) -> void:')
start=t.index('\tvar magic_alpha :=',t.index('func _draw_magic_vanish_scene('));end=t.index('\n\nfunc ',start)
old=t[start:end]
assert 'draw_arc' in old and 'draw_circle' in old
new='''\tif success_amount > 0.0:
\t\tvar painted := _support_art_ref()
\t\tpainted.feedback.invitation(self, hat_center, hat_side * 1.15,
\t\t\tmini(3, int(success_amount * 4.0)))
\t\tpainted.picture("widget_portal_magician_overlay", hat_center,
\t\t\that_side * 0.80, success_amount)
'''
t=t[:start]+new+t[end:]
replace('func _draw_farm_lob() -> void:\n\t_support_art_ref().picnic()\n\t_draw_farm_vegetable()', 'func _draw_farm_lob() -> void:\n\t_support_art_ref().picnic()\n\t# A landed snack is consumed; never leave its final projectile over a face.\n\tif not farm_complete and not completion_accepted and farm_pause <= 0.0:\n\t\t_draw_farm_vegetable()')
# Render only: same tap marks, free placement, goals and event ownership.
replace('\t\t"trace":\n\t\t\twidget_overlay = _load_widget_texture("%s_lit.png" % prefix)', '\t\t"trace":\n\t\t\twidget_overlay = _load_widget_texture("%s_lit.png" % prefix)') if False else None
needle='\t\t\twidget_stamp = _load_widget_texture("%s_mark.png" % prefix)'
replace(needle,needle+'\n\t\t\tif visual_context == "target_painter":\n\t\t\t\twidget_stamp = _support_art_ref().art("widget_stamp_painter")')
assert original!=t
(s/'source_versions/gesture_before_context_repairs01.gd.txt').write_text(original,encoding='utf-8')
p.write_text(t,encoding='utf-8')
record={'scope':'Rendering/resource selection only; existing source-bound Lamb-a local finish, fullopacity Farmer picnic, painted native feedback and completed projectile occlusion. No goal/input/hitmap/progress/save changes.','new_runtime':'runtime_provenance04.json56PNG/C2PASS','magician_fixed_geometry':'cabinet_registration01.json158fixed featuresp95<2pxat512','old_vanish_render_tail':old,'source_before_sha256':hashlib.sha256(original.encode()).hexdigest(),'source_after_sha256':hashlib.sha256(t.encode()).hexdigest(),'limits':'New exactcurrent capture/fullnative checks/motion/4.5 audit pending.'}
(s/'context_repairs01.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print('Wired context repairs, preserve rejected old captures and sources')
