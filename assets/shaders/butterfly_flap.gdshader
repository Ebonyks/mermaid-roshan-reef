// GEN2 butterfly: a single quad lying in the XZ plane (wings along ±X)
// folded along the body line by a vertex sine — a wing flap with zero
// CPU cost. Unshaded cutout, runs identically under the mobile renderer.
shader_type spatial;
render_mode cull_disabled, unshaded, depth_prepass_alpha;

uniform sampler2D wing_tex : source_color, filter_linear_mipmap;
uniform float flap_speed = 9.0;
uniform float flap_amount = 0.9;
uniform float phase = 0.0;

void vertex() {
	float a = sin(TIME * flap_speed + phase) * flap_amount;
	VERTEX.y += abs(VERTEX.x) * sin(a);
	VERTEX.x *= cos(a);
}

void fragment() {
	vec4 c = texture(wing_tex, UV);
	ALBEDO = c.rgb;
	ALPHA = c.a;
	ALPHA_SCISSOR_THRESHOLD = 0.35;
}
