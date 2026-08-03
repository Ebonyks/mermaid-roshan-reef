// Castle fixture water for front-facing 2.5D props.
//
// This is deliberately UV driven: castle sinks, bowls, tubs, fountains and
// waterfall ribbons face the camera instead of lying on the world's XZ plane.
// It reuses the reef's approved ripple and caustic textures. Exact per-fixture
// masks bound every card, and depth_draw_never prevents translucent water from
// erasing Roshan or another cutout behind it on the Mobile renderer.
shader_type spatial;
render_mode unshaded, cull_disabled, depth_draw_never;

uniform sampler2D shape_mask : source_color, filter_linear;
uniform sampler2D ripple : hint_normal, repeat_enable, filter_linear_mipmap;
uniform sampler2D caustics : repeat_enable, filter_linear_mipmap;
uniform vec3 deep_color : source_color = vec3(0.12, 0.54, 0.76);
uniform vec3 shallow_color : source_color = vec3(0.48, 0.88, 0.94);
uniform vec3 foam_color : source_color = vec3(0.96, 1.0, 1.0);
uniform float flow_amount : hint_range(0.0, 1.0) = 0.0;
uniform float fill_amount : hint_range(0.0, 1.0) = 1.0;
uniform float turbulence : hint_range(0.0, 2.0) = 0.65;
uniform float vortex_strength : hint_range(0.0, 2.0) = 0.0;
uniform float edge_foam : hint_range(0.0, 1.0) = 0.35;
uniform float alpha_base : hint_range(0.0, 1.0) = 0.84;
uniform float flow_speed : hint_range(0.0, 4.0) = 1.0;
uniform vec2 flow_axis = vec2(0.0, 1.0);
uniform bool stream_mode = false;
uniform bool reveal_from_top = false;

void fragment() {
	float mask_alpha = texture(shape_mask, UV).a;
	vec2 centered = UV - vec2(0.5);
	float radius = max(length(centered), 0.001);
	float angle = atan(centered.y, centered.x);
	vec2 vortex_uv = vec2(
		cos(angle + TIME * vortex_strength),
		sin(angle + TIME * vortex_strength)) * radius;
	vec2 travel = flow_axis * TIME * flow_speed * 0.22;
	vec2 uv_a = UV * 3.2 + travel + vortex_uv * vortex_strength * 0.65;
	vec2 uv_b = UV * 5.1 - travel * 0.63 - vortex_uv * vortex_strength * 0.34;
	float wave_a = texture(ripple, uv_a).g;
	float wave_b = texture(ripple, uv_b).b;
	float painted_ripple = mix(wave_a, wave_b, 0.48);
	float sparkle = texture(caustics, uv_a * 0.83).g
		* texture(caustics, uv_b * 0.61).g;
	float shimmer = smoothstep(0.34, 0.82, sparkle + painted_ripple * 0.20);
	float stream_edge = 1.0 - smoothstep(0.24, 0.49, abs(UV.x - 0.5));
	float basin_edge = 1.0 - smoothstep(0.0, 0.10,
		min(min(UV.x, 1.0 - UV.x), min(UV.y, 1.0 - UV.y)));
	float stream_selector = 0.0;
	if (stream_mode) {
		stream_selector = 1.0;
	}
	float foam = mix(basin_edge, stream_edge, stream_selector) * edge_foam;
	float bottom_fill = smoothstep(1.0 - fill_amount - 0.025,
		1.0 - fill_amount + 0.025, UV.y);
	float top_reveal = 1.0 - smoothstep(fill_amount - 0.025,
		fill_amount + 0.025, UV.y);
	float reveal_selector = 0.0;
	if (reveal_from_top) {
		reveal_selector = 1.0;
	}
	float reveal = mix(bottom_fill, top_reveal, reveal_selector);
	float visible = flow_amount * reveal * mask_alpha;
	vec3 base = mix(deep_color, shallow_color,
		clamp(0.24 + painted_ripple * 0.72, 0.0, 1.0));
	base = mix(base, foam_color, clamp(foam + shimmer * 0.28, 0.0, 1.0));
	ALBEDO = base;
	EMISSION = base * (0.16 + shimmer * 0.10) + foam_color * foam * 0.16;
	ROUGHNESS = 0.18;
	METALLIC = 0.08;
	ALPHA = alpha_base * visible * (0.78 + painted_ripple * turbulence * 0.20);
}
