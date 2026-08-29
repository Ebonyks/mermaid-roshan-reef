shader_type canvas_item;

// The dirty and clean cards share the exact registered 2x8 source geometry.
// A single background draw therefore reveals authored clean pixels in place;
// no opaque patch or second plate is stacked over the hall.
uniform sampler2D clean_texture : source_color, filter_linear;
uniform vec4 reveal_rect_0 = vec4(-2.0, -2.0, 0.0, 0.0);
uniform vec4 reveal_rect_1 = vec4(-2.0, -2.0, 0.0, 0.0);
uniform vec4 reveal_rect_2 = vec4(-2.0, -2.0, 0.0, 0.0);
uniform vec4 reveal_rect_3 = vec4(-2.0, -2.0, 0.0, 0.0);
uniform float reveal_progress_0 = 0.0;
uniform float reveal_progress_1 = 0.0;
uniform float reveal_progress_2 = 0.0;
uniform float reveal_progress_3 = 0.0;

float reveal_shape(vec2 uv, vec4 rect, float progress) {
	if (rect.z <= 0.0 || rect.w <= 0.0 || progress <= 0.0) {
		return 0.0;
	}
	vec2 center = rect.xy + rect.zw * 0.5;
	vec2 radius = rect.zw * 0.5;
	vec2 p = (uv - center) / max(radius, vec2(0.0001));
	float ellipse = 1.0 - smoothstep(0.80, 1.08, dot(p, p));
	// A tiny deterministic edge variation makes a reveal feel like a wipe of
	// the authored surface, while the clean texture supplies all appearance.
	float grain = sin(uv.x * 173.0 + uv.y * 97.0) * 0.035;
	return smoothstep(0.08, 0.98, progress) * smoothstep(0.0, 0.16,
		ellipse + grain);
}

void fragment() {
	vec4 dirty = texture(TEXTURE, UV);
	vec4 clean = texture(clean_texture, UV);
	float reveal = max(
		reveal_shape(UV, reveal_rect_0, reveal_progress_0),
		max(reveal_shape(UV, reveal_rect_1, reveal_progress_1),
			max(reveal_shape(UV, reveal_rect_2, reveal_progress_2),
				reveal_shape(UV, reveal_rect_3, reveal_progress_3))));
	COLOR = mix(dirty, clean, clamp(reveal, 0.0, 1.0));
}
