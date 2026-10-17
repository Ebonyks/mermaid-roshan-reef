shader_type canvas_item;
render_mode unshaded;

// The old filled selection mask becomes a thin edge: the hall stays visible.
float mask_alpha(sampler2D mask_texture, vec2 uv) {
	if (any(lessThan(uv, vec2(0.0))) || any(greaterThan(uv, vec2(1.0)))) {
		return 0.0;
	}
	return texture(mask_texture, uv).a;
}

void fragment() {
	vec4 tint = COLOR;
	vec2 step_uv = TEXTURE_PIXEL_SIZE * 2.0;
	float center = texture(TEXTURE, UV).a;
	float inset = min(min(mask_alpha(TEXTURE, UV + vec2(step_uv.x, 0.0)),
		mask_alpha(TEXTURE, UV - vec2(step_uv.x, 0.0))),
		min(mask_alpha(TEXTURE, UV + vec2(0.0, step_uv.y)),
		mask_alpha(TEXTURE, UV - vec2(0.0, step_uv.y))));
	COLOR = vec4(tint.rgb, tint.a * max(center - inset, 0.0));
}
