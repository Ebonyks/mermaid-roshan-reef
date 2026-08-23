// A single bounded Mermaid Pool surface pass for the Mobile renderer.
//
// The approved room painting remains the color authority. This pass only adds
// quiet moving caustic highlights and two low-contrast source ripples inside an
// analytic pool oval; it never samples the screen or draws over room actors.
shader_type canvas_item;
render_mode unshaded, blend_mix;

uniform sampler2D ripple : hint_normal, repeat_enable, filter_linear_mipmap;
uniform sampler2D caustics : repeat_enable, filter_linear_mipmap;
uniform vec3 shimmer_color : source_color = vec3(0.80, 0.99, 1.0);
uniform float shimmer_alpha : hint_range(0.0, 0.20) = 0.105;
uniform float motion_speed : hint_range(0.0, 1.0) = 0.16;

float source_ring(vec2 uv, vec2 source, float phase) {
	// Screen-space circles read as flattened ellipses on the pool plane.
	vec2 delta = uv - source;
	float radius = length(vec2(delta.x, delta.y * 3.55));
	float crest = 0.5 + 0.5 * sin(radius * 92.0 - TIME * 2.35 + phase);
	float band = smoothstep(0.78, 0.98, crest);
	return band * (1.0 - smoothstep(0.04, 0.34, radius));
}

void fragment() {
	vec2 oval = (UV - vec2(0.5)) / vec2(0.5);
	float pool_mask = 1.0 - smoothstep(0.91, 1.0, length(oval));
	vec2 drift = vec2(TIME * motion_speed, TIME * motion_speed * 0.61);
	float caustic = texture(caustics, UV * vec2(2.15, 1.48) + drift).g;
	float wave = texture(ripple,
		UV * vec2(3.35, 2.10) - drift * vec2(0.72, 0.45)).g;
	float moving_light = smoothstep(0.48, 0.88,
		caustic * 0.74 + wave * 0.34);
	float rings = source_ring(UV, vec2(0.69, 0.13), 0.0)
		+ source_ring(UV, vec2(0.34, 0.07), 2.4);
	float alpha = pool_mask * shimmer_alpha
		* clamp(0.24 + moving_light * 0.76 + rings * 0.34, 0.0, 1.0);
	COLOR = vec4(shimmer_color, alpha);
}
