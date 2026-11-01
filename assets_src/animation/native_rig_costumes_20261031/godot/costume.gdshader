shader_type canvas_item;
uniform sampler2D body_paint : source_color, filter_linear;
uniform sampler2D tail_paint : source_color, filter_linear;
void fragment() {
	vec4 base = texture(TEXTURE, UV);
	vec4 tail = texture(tail_paint, UV);
	vec4 body = texture(body_paint, UV);
	base.rgb = mix(base.rgb, tail.rgb, tail.a);
	base.rgb = mix(base.rgb, body.rgb, body.a);
	COLOR = base;
}
