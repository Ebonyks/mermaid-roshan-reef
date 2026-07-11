// seagrass_sway.gdshader — GEN2 crossed-quad sea grass (Mobile-safe).
//
// The family-style seaweed sprite on two crossed quads, base pinned, tips
// swaying on a vertex sine — the classic cheap flora that reads storybook
// (unshaded cutout, like the character language) and costs no CPU.
shader_type spatial;
render_mode cull_disabled, unshaded, depth_prepass_alpha;

uniform sampler2D tex : source_color, filter_linear_mipmap;
uniform vec4 tint : source_color = vec4(1.0);
uniform float sway_speed = 1.1;
uniform float sway_amount = 0.30;   // world units at the tips
uniform float phase = 0.0;

void vertex() {
	// QuadMesh UV.y is 0 at the top: tips move, the planted base stays put
	float tip = 1.0 - UV.y;
	VERTEX.x += sin(TIME * sway_speed + phase) * sway_amount * tip * tip;
	VERTEX.z += cos(TIME * sway_speed * 0.7 + phase * 1.3) * sway_amount * 0.4 * tip;
}

void fragment() {
	vec4 t = texture(tex, UV) * tint;
	ALBEDO = t.rgb;
	ALPHA = t.a;
}
