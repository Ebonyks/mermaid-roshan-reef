// fairy_wing.gdshader — GEN2 fairy wing card (Mobile-safe).
//
// A textured wing plate that FLAPS as a RIGID ROTATION around its inner
// (hinge) edge — the butterfly-card approach. Plate rotation, not a fold or
// curl: the whole wing sweeps like a real insect wing (owner spec).
// The quad is built with its hinge edge at local x=0 (center_offset), so
// rotating around the local Y axis at the origin IS the hinge.
shader_type spatial;
render_mode cull_disabled, unshaded, depth_prepass_alpha;

uniform sampler2D wing_tex : source_color, filter_linear_mipmap;
uniform float flap_speed = 3.4;
uniform float flap_base = 0.5;     // resting splay away from the back (radians)
uniform float flap_amount = 0.55;  // sweep either side of the splay
uniform float phase = 0.0;
uniform float flip = 0.0;          // 1.0 mirrors the art for the right wing

void vertex() {
	float ang = flap_base + sin(TIME * flap_speed + phase) * flap_amount;
	float c = cos(ang);
	float s = sin(ang);
	vec3 v = VERTEX;
	VERTEX.x = v.x * c - v.z * s;
	VERTEX.z = v.x * s + v.z * c;
}

void fragment() {
	vec2 uv = UV;
	uv.x = abs(flip - uv.x);
	vec4 t = texture(wing_tex, uv);
	ALBEDO = t.rgb;
	ALPHA = t.a;
}
