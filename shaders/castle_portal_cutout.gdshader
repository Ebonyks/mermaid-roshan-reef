shader_type spatial;
render_mode unshaded, blend_mix, depth_prepass_alpha, cull_disabled, shadows_disabled, fog_disabled;

uniform sampler2D portal_texture : source_color, filter_linear_mipmap_anisotropic;

float box_mask(vec2 uv, vec2 minimum, vec2 maximum) {
	vec2 lower = smoothstep(minimum - vec2(0.004), minimum, uv);
	vec2 upper = 1.0 - smoothstep(maximum, maximum + vec2(0.004), uv);
	return lower.x * lower.y * upper.x * upper.y;
}

float ellipse_mask(vec2 uv, vec2 center, vec2 radius) {
	float distance_from_center = length((uv - center) / radius);
	return 1.0 - smoothstep(0.98, 1.0, distance_from_center);
}

void fragment() {
	vec4 portal = texture(portal_texture, UV);
	// The reused source contains a complete portal plus wall, floor, and carpet.
	// Keep only the authored arch/corridor silhouette so this Sprite3D bridges
	// the screen join without drawing an opaque rectangular stage patch.
	float lower_arch = box_mask(
		UV,
		vec2(0.095, 0.275),
		vec2(0.905, 0.858)
	);
	float arch_crown = ellipse_mask(
		UV,
		vec2(0.5, 0.292),
		vec2(0.405, 0.210)
	);
	float emblem = ellipse_mask(
		UV,
		vec2(0.5, 0.150),
		vec2(0.295, 0.125)
	);
	float silhouette = max(lower_arch, max(arch_crown, emblem));
	ALBEDO = portal.rgb;
	ALPHA = portal.a * silhouette;
}
