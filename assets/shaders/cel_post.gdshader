// cel_post.gdshader — full-screen Wind-Waker cel post-process (Forward+ only).
//
// Runs once over the whole rendered frame: posterizes colours into flat toon
// bands (brightness preserved — this does NOT darken the scene) and draws thin
// ink outlines wherever the depth buffer has an edge. Applied to a fullscreen
// QuadMesh parented to the camera. Tunable uniforms: bands, saturation,
// edge_threshold, edge_strength, line_color.
shader_type spatial;
render_mode unshaded, cull_disabled, fog_disabled, depth_test_disabled, depth_draw_never;

uniform sampler2D screen_tex : hint_screen_texture, filter_linear;
uniform sampler2D depth_tex : hint_depth_texture, filter_nearest;
uniform float bands : hint_range(2.0, 16.0) = 6.0;          // colour quantisation steps
uniform float saturation : hint_range(1.0, 2.0) = 1.18;     // pop the palette
uniform float edge_threshold = 0.6;                         // world-units depth delta = edge
uniform float edge_strength : hint_range(0.0, 1.0) = 0.85;
uniform vec3 line_color : source_color = vec3(0.02, 0.03, 0.05);

void vertex() {
	// QuadMesh is 1x1 centred at origin -> *2 gives clip-space -1..1 (fullscreen)
	POSITION = vec4(VERTEX.xy * 2.0, 1.0, 1.0);
}

float lindepth(vec2 uv) {
	float raw = texture(depth_tex, uv).r;
	vec4 ndc = vec4(uv * 2.0 - 1.0, raw, 1.0);
	vec4 v = INV_PROJECTION_MATRIX * ndc;
	return -(v.xyz / v.w).z;
}

void fragment() {
	vec2 uv = SCREEN_UV;
	vec2 ps = 1.0 / VIEWPORT_SIZE;
	vec3 col = texture(screen_tex, uv).rgb;
	// flat toon bands (keeps brightness — it rounds, it doesn't darken)
	vec3 q = floor(col * bands + 0.5) / bands;
	float l = dot(q, vec3(0.299, 0.587, 0.114));
	q = clamp(mix(vec3(l), q, saturation), 0.0, 1.0);
	// depth-based ink outline
	float dc = lindepth(uv);
	float e = abs(dc - lindepth(uv + vec2(ps.x, 0.0)))
			+ abs(dc - lindepth(uv - vec2(ps.x, 0.0)))
			+ abs(dc - lindepth(uv + vec2(0.0, ps.y)))
			+ abs(dc - lindepth(uv - vec2(0.0, ps.y)));
	float ink = smoothstep(edge_threshold, edge_threshold * 2.0, e) * edge_strength;
	ALBEDO = mix(q, line_color, ink);
}
