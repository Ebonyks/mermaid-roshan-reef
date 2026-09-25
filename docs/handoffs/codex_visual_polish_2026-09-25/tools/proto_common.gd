extends RefCounted
## Shared helpers for the aesthetics prototypes (scratch only, not project code).

const WATER_SHADER := """
shader_type canvas_item;
render_mode unshaded, blend_mix;
uniform sampler2D screen_tex : hint_screen_texture, filter_linear_mipmap;
uniform sampler2D ripple_tex : repeat_enable, filter_linear_mipmap;
uniform sampler2D caustics_tex : repeat_enable, filter_linear_mipmap;
uniform float distort_px = 2.2;
uniform float caustic_strength = 0.26;
uniform float sweep_strength = 0.07;
void fragment() {
	float mask = texture(TEXTURE, UV).r;
	vec2 p = vec2(UV.x * 3.0, UV.y * 5.5);
	vec2 n1 = texture(ripple_tex, p * 0.30 + vec2(TIME * 0.030, TIME * 0.018)).rg - 0.5;
	vec2 n2 = texture(ripple_tex, p * 0.47 - vec2(TIME * 0.022, -TIME * 0.015)).rg - 0.5;
	vec2 offs = (n1 + n2) * distort_px * SCREEN_PIXEL_SIZE;
	vec3 base = texture(screen_tex, SCREEN_UV + offs).rgb;
	float c1 = texture(caustics_tex, p * 0.42 + vec2(TIME * 0.035, TIME * 0.022)).r;
	float c2 = texture(caustics_tex, p * 0.61 - vec2(TIME * 0.028, TIME * 0.017)).r;
	float c = pow(min(c1, c2), 1.5) * caustic_strength;
	float sweep_pos = fract(TIME * 0.06) * 2.6 - 0.8;
	float sweep = smoothstep(0.10, 0.0, abs(UV.x * 0.85 + UV.y * 0.35 - sweep_pos)) * sweep_strength;
	COLOR = vec4(base + vec3(0.80, 0.98, 1.0) * (c + sweep), mask);
}
"""

const RAYS_SHADER := """
shader_type canvas_item;
render_mode unshaded, blend_add;
uniform vec3 tint = vec3(0.80, 0.96, 1.0);
uniform float strength = 0.30;
uniform float slant_amount = 0.22;
void fragment() {
	float m = texture(TEXTURE, UV).r;
	float rays = 0.0;
	for (int i = 0; i < 5; i++) {
		float fi = float(i);
		float x = fract(0.1 + fi * 0.21 + sin(TIME * 0.17 + fi * 1.7) * 0.04);
		float w = 0.035 + 0.02 * sin(TIME * 0.43 + fi);
		float slant = (UV.x - x) - UV.y * slant_amount;
		rays += smoothstep(w, 0.0, abs(slant)) * (0.55 + 0.45 * sin(TIME * 0.8 + fi * 2.1));
	}
	float fade = smoothstep(1.0, 0.05, UV.y);
	COLOR = vec4(tint * rays * fade * strength * m, 1.0);
}
"""

const FLOW_SHADER := """
shader_type canvas_item;
render_mode unshaded, blend_add;
uniform sampler2D noise_tex : repeat_enable, filter_linear_mipmap;
uniform vec4 box = vec4(0.0, 0.0, 1.0, 1.0);
uniform vec2 dir = vec2(0.0, 1.0);
uniform float speed = 0.45;
uniform float strength = 0.40;
void fragment() {
	float a = texture(TEXTURE, UV).a;
	float inside = step(box.x, UV.x) * step(UV.x, box.z) * step(box.y, UV.y) * step(UV.y, box.w);
	vec2 q = vec2(UV.x * 2.6, UV.y * 0.7) - dir * TIME * speed;
	float s1 = texture(noise_tex, q).r;
	float s2 = texture(noise_tex, q * 1.7 + vec2(0.31, 0.17) - dir * TIME * speed * 0.6).r;
	float s = smoothstep(0.62, 0.98, max(s1, s2));
	COLOR = vec4(vec3(1.0) * s * strength * a * inside, 1.0);
}
"""

const GLOW_SHADER := """
shader_type canvas_item;
render_mode unshaded, blend_add;
uniform vec3 tint = vec3(1.0, 0.82, 0.55);
uniform float strength = 0.35;
uniform float phase = 0.0;
void fragment() {
	float d = length(UV - vec2(0.5)) * 2.0;
	float g = pow(clamp(1.0 - d, 0.0, 1.0), 2.2);
	float breathe = 0.82 + 0.18 * sin(TIME * 1.3 + phase) + 0.05 * sin(TIME * 7.1 + phase * 3.0);
	COLOR = vec4(tint * g * strength * breathe, 1.0);
}
"""

const VIGNETTE_SHADER := """
shader_type canvas_item;
render_mode unshaded;
uniform float strength = 0.30;
void fragment() {
	vec2 d = UV - vec2(0.5, 0.52);
	d.x *= 1.35;
	float v = smoothstep(0.42, 0.95, length(d));
	COLOR = vec4(0.30, 0.20, 0.52, v * strength);
}
"""

const BEAM_SHADER := """
shader_type canvas_item;
render_mode unshaded, blend_add;
uniform vec3 tint = vec3(1.0, 0.93, 0.80);
uniform float strength = 0.16;
void fragment() {
	float across = abs(UV.x - 0.5) * 2.0;
	float body = smoothstep(1.0, 0.15, across) * smoothstep(1.0, 0.0, UV.y) * smoothstep(0.0, 0.12, UV.y);
	float shimmer = 0.85 + 0.15 * sin(TIME * 0.9 + UV.y * 6.0);
	COLOR = vec4(tint * body * strength * shimmer, 1.0);
}
"""

const IRIS_SHADER := """
shader_type canvas_item;
render_mode unshaded;
uniform sampler2D from_tex : filter_linear;
uniform float progress : hint_range(0.0, 1.0) = 0.0;
uniform vec2 center = vec2(0.5, 0.6);
uniform float aspect = 1.777;
void fragment() {
	vec2 d = UV - center;
	d.x *= aspect;
	float r = progress * 1.35;
	float wobble = 0.012 * sin(atan(d.y, d.x) * 9.0 + TIME * 4.0);
	float edge = length(d) - (r + wobble);
	vec4 from_col = texture(from_tex, UV);
	float ring = smoothstep(0.03, 0.0, abs(edge)) * step(0.001, progress) * step(progress, 0.999);
	vec3 col = mix(vec3(0.0), from_col.rgb, step(0.0, edge));
	col += vec3(1.0, 0.95, 0.85) * ring * 0.9;
	float a = max(step(0.0, edge), ring);
	COLOR = vec4(col, a);
}
"""

static func shader(code: String) -> ShaderMaterial:
	var sh := Shader.new()
	sh.code = code
	var mat := ShaderMaterial.new()
	mat.shader = sh
	return mat

static func file_texture(path: String) -> ImageTexture:
	var img := Image.load_from_file(path)
	img.convert(Image.FORMAT_RGBA8)
	return ImageTexture.create_from_image(img)

static func soft_dot(size: int, ring: bool) -> ImageTexture:
	var img := Image.create(size, size, false, Image.FORMAT_RGBA8)
	var c := Vector2(size, size) * 0.5
	for y in range(size):
		for x in range(size):
			var d := Vector2(x + 0.5, y + 0.5).distance_to(c) / (size * 0.5)
			var a := 0.0
			if ring:
				a = clampf(1.0 - absf(d - 0.78) / 0.22, 0.0, 1.0) * 0.9 + clampf(0.35 - d, 0.0, 0.35)
			else:
				a = clampf(1.0 - d, 0.0, 1.0)
				a = a * a
			img.set_pixel(x, y, Color(1, 1, 1, a))
	return ImageTexture.create_from_image(img)

static func sparkle_texture(size: int) -> ImageTexture:
	# Four-point white twinkle: two thin crossed diamonds plus a soft core.
	var img := Image.create(size, size, false, Image.FORMAT_RGBA8)
	var c := (size - 1) * 0.5
	for y in range(size):
		for x in range(size):
			var dx := absf(x - c) / c
			var dy := absf(y - c) / c
			var arm := maxf(clampf(1.0 - dx - dy * 7.0, 0.0, 1.0), clampf(1.0 - dy - dx * 7.0, 0.0, 1.0))
			var core := clampf(1.0 - sqrt(dx * dx + dy * dy) * 2.4, 0.0, 1.0)
			img.set_pixel(x, y, Color(1, 1, 1, clampf(arm + core * core, 0.0, 1.0)))
	return ImageTexture.create_from_image(img)

static func glow_card(pos: Vector2, radius: float, tint: Color, strength: float, phase: float) -> Sprite2D:
	var s := Sprite2D.new()
	s.texture = soft_dot(8, false)
	s.position = pos
	s.scale = Vector2.ONE * (radius * 2.0 / 8.0)
	var mat := shader(GLOW_SHADER)
	mat.set_shader_parameter("tint", Vector3(tint.r, tint.g, tint.b))
	mat.set_shader_parameter("strength", strength)
	mat.set_shader_parameter("phase", phase)
	s.material = mat
	return s

static func find_sprite(root: Node, needle: String) -> Sprite2D:
	for c in root.get_children():
		if c is Sprite2D and String(c.name).contains(needle):
			return c as Sprite2D
		var found := find_sprite(c, needle)
		if found != null:
			return found
	return null

static func finished_day_one_save(path: String) -> void:
	var clips := {}
	for id in ["d1_opening", "d1_castle", "d1_bath_arrival", "d1_bath_clean",
			"d1_pool_arrival", "d1_pool_clean", "d1_eagle_free", "d1_art_arrival",
			"d1_art_clean", "d1_rainbow_route", "d1_puff_arrival",
			"d1_puff_transformation", "d1_epilogue"]:
		clips[id] = true
	var f := FileAccess.open(path, FileAccess.WRITE)
	f.store_string(JSON.stringify({"schema_version": 1, "save_generation": 3,
		"music": false, "day_one_active": false,
		"day_one_completed_rooms": ["bathroom", "pool", "stuffie", "art"],
		"day_one_giant_dust_bunny_boss_triggered": true,
		"day_one_giant_dust_bunny_boss_defeated": true,
		"day_one_story_clips_seen": clips}))
	f.close()

static func remove_save(path: String) -> void:
	for s in ["", ".bak", ".tmp", ".old"]:
		if FileAccess.file_exists(path + s):
			DirAccess.remove_absolute(path + s)
