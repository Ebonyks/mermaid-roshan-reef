shader_type canvas_item;
render_mode unshaded;
uniform sampler2D motion_field : filter_linear, repeat_disable;
uniform float displacement_px = 0.0;
void fragment() {
	float weight = texture(motion_field, UV).r;
	vec2 source_uv = UV - vec2(displacement_px * weight / 512.0, 0.0);
	COLOR = texture(TEXTURE, source_uv);
}
