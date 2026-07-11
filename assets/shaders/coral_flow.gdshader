// coral_flow.gdshader — two-layer life for GEN2 flora (Mobile-safe).
//
// One mesh, two behaviours (owner 2026-07-11): the GREEN growth (mushroom
// stalks, fronds) flows with the ocean like the sea grass, while the rocky
// body stays rigid. The vertex stage samples the albedo and lets greenness
// gate the sway - no mesh editing, works on every coral automatically.
// Fragment/light are the standard cel pair (pair with outline next_pass).
shader_type spatial;
render_mode cull_back, diffuse_toon, specular_toon;

uniform sampler2D albedo_tex : source_color, hint_default_white;
uniform vec4 tint : source_color = vec4(1.0);
uniform int bands : hint_range(1, 4) = 2;
uniform float rim_strength : hint_range(0.0, 2.0) = 0.15;
uniform vec4 rim_color : source_color = vec4(1.0);
uniform float rim_width : hint_range(0.0, 1.0) = 0.35;
uniform float flow_speed = 1.7;
uniform float flow_amount = 0.055;   // model units (Meshy props are ~1.1)
uniform float phase = 0.0;

void vertex() {
	vec3 alb = textureLod(albedo_tex, UV, 0.0).rgb;
	// greenness gate: stalks/fronds sway, rock stays put
	float leafy = clamp((alb.g - max(alb.r, alb.b)) * 6.0, 0.0, 1.0);
	float w = sin(TIME * flow_speed + phase + VERTEX.x * 1.4 + VERTEX.z * 1.1);
	VERTEX.x += w * flow_amount * leafy;
	VERTEX.z += cos(TIME * flow_speed * 0.8 + phase + VERTEX.x * 1.2) * flow_amount * 0.5 * leafy;
}

void fragment() {
	vec4 t = texture(albedo_tex, UV);
	ALBEDO = t.rgb * tint.rgb;
	ROUGHNESS = 0.9;
	SPECULAR = 0.0;
	float f = pow(1.0 - clamp(dot(normalize(NORMAL), normalize(VIEW)), 0.0, 1.0), 3.0);
	EMISSION += rim_color.rgb * smoothstep(1.0 - rim_width, 1.0, f) * rim_strength;
}

void light() {
	float ndl = clamp(dot(normalize(NORMAL), normalize(LIGHT)), 0.0, 1.0);
	float stepped = floor(ndl * float(bands) + 0.5) / float(bands);
	DIFFUSE_LIGHT += ALBEDO * LIGHT_COLOR * ATTENUATION * stepped;
}
