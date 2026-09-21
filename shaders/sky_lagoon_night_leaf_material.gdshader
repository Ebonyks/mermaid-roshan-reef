shader_type canvas_item;
render_mode unshaded;
void fragment() {
	vec4 source = texture(TEXTURE, UV);
	float green = smoothstep(1.18, 1.6, source.g / max(source.r, 0.01));
	green *= smoothstep(1.08, 1.35, source.g / max(source.b, 0.01));
	float value = dot(source.rgb, vec3(0.2126, 0.7152, 0.0722));
	float painted_shadow = smoothstep(0.04, 0.12, value) * (1.0 - smoothstep(0.22, 0.50, value));
	COLOR.rgb += vec3(0.012, 0.022, 0.028) * green * painted_shadow;
}
