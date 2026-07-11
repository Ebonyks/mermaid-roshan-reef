// creature_sway.gdshader — GEN2 swimming creature (Mobile-safe).
//
// The family-style Meshy animals are statics: this gives them life with a
// tail-weighted body wave in the vertex stage — the head (-Y in model space,
// the multi-view front) holds steady while the tail end swings. Flat toon
// response matches the world; pair with outline.gdshader as next_pass.
shader_type spatial;
render_mode cull_back, diffuse_toon, specular_toon;

uniform sampler2D albedo_tex : source_color, hint_default_white;
uniform vec4 tint : source_color = vec4(1.0);
uniform float sway_speed = 4.2;
uniform float sway_amount = 0.09;   // in model units (Meshy bodies are ~1.1 long)
uniform float phase = 0.0;

void vertex() {
	float t = clamp(VERTEX.y / 0.55 * 0.5 + 0.5, 0.0, 1.0);
	VERTEX.x += sin(TIME * sway_speed + phase + VERTEX.y * 2.4) * sway_amount * t * t;
}

void fragment() {
	ALBEDO = texture(albedo_tex, UV).rgb * tint.rgb;
	ROUGHNESS = 1.0;
	SPECULAR = 0.0;
}
