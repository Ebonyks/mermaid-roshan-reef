shader_type canvas_item;
render_mode unshaded, blend_mix;

// Each seeded swipe receives a different phase, and screen position shifts the
// color across its individual glints. Geometry and animation stay on the 2D
// canvas and remain inexpensive under the Mobile renderer.
uniform float phase : hint_range(0.0, 1.0, 0.001) = 0.0;
uniform float shimmer_speed : hint_range(0.0, 2.0, 0.05) = 0.65;

vec3 iridescent(float offset) {
	return vec3(0.68) + vec3(0.32) * cos(
		TAU * (vec3(0.00, 0.34, 0.67) + offset)
	);
}

void fragment() {
	vec4 base = COLOR;
	float travel = fract(
		SCREEN_UV.x * 1.45
		+ SCREEN_UV.y * 0.85
		+ TIME * shimmer_speed
		+ phase
	);
	float gleam = 1.0 - abs(travel * 2.0 - 1.0);
	gleam = smoothstep(0.55, 1.0, gleam);
	vec3 pearl = iridescent(travel + phase * 0.35);
	COLOR.rgb = mix(base.rgb, pearl, 0.52 + gleam * 0.32);
	COLOR.a = base.a * (0.72 + gleam * 0.28);
}
