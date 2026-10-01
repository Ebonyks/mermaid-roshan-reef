from pathlib import Path
r=Path(__file__).resolve().parents[1]
s=(r/'tmp/capture_wash_bubble_reuse_v1.gd').read_text()
s=s.replace('res://tmp/wash_bubble_reuse_v1/native_views/','res://tmp/wash_foam_native_fit_v1/native_views/')
s=s.replace('const ATLAS := "res://assets/sprites/fx_water/fx_water_bubble_burst_atlas.png"','const CANDIDATE := "res://assets_src/imagegen/day2_wash_foam_v1_20261001/attempt_02_whole_canvas_1024x608.png"')
s=s.replace('var atlas: Texture2D = load(ATLAS) as Texture2D\n\tassert(atlas.get_size() == Vector2(1024, 512))','var candidate_texture: Texture2D = ImageTexture.create_from_image(Image.load_from_file(CANDIDATE))\n\tassert(candidate_texture.get_size() == Vector2(1024, 608))')
s=s.replace('[{"name":"original", "cell":-1, "extent":0.0}, {"name":"cell0_131", "cell":0, "extent":131.0}, {"name":"cell2_131", "cell":2, "extent":131.0}, {"name":"cell2_180", "cell":2, "extent":180.0}]','[{"name":"original", "cell":-1, "extent":0.0}, {"name":"fresh_foam02", "cell":-2, "extent":0.0}]')
s=s.replace('if cell < 0:', 'if cell == -1:')
old='\t\t\t\t\tvar candidate: AtlasTexture = AtlasTexture.new()\n\t\t\t\t\tcandidate.atlas = atlas\n\t\t\t\t\tcandidate.region = Rect2(float(cell % 4) * 256.0, float(cell / 4) * 256.0, 256.0, 256.0)\n\t\t\t\t\thotspot.object_texture = candidate\n\t\t\t\t\thotspot.object_size = Vector2.ONE * float(variant["extent"])'
assert old in s
s=s.replace(old,'\t\t\t\t\thotspot.object_texture = candidate_texture\n\t\t\t\t\thotspot.object_size = original_size')
s=s.replace('hotspot.source_path if cell < 0 else ATLAS','hotspot.source_path if cell == -1 else CANDIDATE')
start=s.index('\t\t\tworld._open_task()');end=s.index('\t\t\tworld.close()',start)
s=s[:start]+'\t\t\tassert(main.opera_stars == saved_stars)\n'+s[end:]
s=s.replace('assert(views.size() == 20)','assert(views.size() == 8)').replace('TWENTY_UNBOUND_EXISTING_ART_AND_ACTIVITY_VIEWS','EIGHT_UNBOUND_FRESH_FOAM_INVITATION_VIEWS').replace('WASH_BUBBLE_REUSE_NATIVE|PASS 20 unbound source/native views','FRESH_FOAM_NATIVE_FIT|PASS 8 unbound source/native views')
assert 'ATLAS' not in s and 'candidate_texture' in s
(r/'tmp/capture_foam_native_fit_v1.gd').write_text(s,encoding='utf-8')
p=(r/'tmp/run_wash_bubble_reuse_v1.py').read_text()
p=p.replace("tmp/wash_bubble_reuse_v1'","tmp/wash_foam_native_fit_v1'").replace('tmp/capture_wash_bubble_reuse_v1.gd','tmp/capture_foam_native_fit_v1.gd')
p=p.replace("'assets/sprites/fx_water/fx_water_bubble_burst_atlas.png',","'assets_src/imagegen/day2_wash_foam_v1_20261001/attempt_02_native.png','assets_src/imagegen/day2_wash_foam_v1_20261001/attempt_02_whole_canvas_1024x608.png',")
p=p.replace('Unbound existing bubble-atlas source reuse in doctor/nursery actual invitation nodes; four original activity initial views to check whether the same source is used during work.','Unbound fresh matte foam02 in doctor/nursery actual invitation nodes, at exact original220x131 canvas size; eight original/candidate full native views. Placement and complete actions remain separate priorities.')
p=p.replace('No new art, runtime source change, creative score, complete action','Fresh source draft4.6 remains unbound; no runtime source change, native score or complete action')
(r/'tmp/run_foam_native_fit_v1.py').write_text(p,encoding='utf-8')
print('EIGHT_VIEW_FOAM_NATIVE_FIT_PREPARED',flush=True)
