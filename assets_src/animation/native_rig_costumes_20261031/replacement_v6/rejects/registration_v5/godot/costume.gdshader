shader_type canvas_item;
uniform sampler2D body_paint : source_color, filter_linear;
uniform sampler2D tail_paint : source_color, filter_linear;
uniform sampler2D scalp_paint : source_color, filter_linear;
uniform sampler2D ownership : filter_nearest;
void fragment() {
	vec4 owner = texture(ownership, UV);
	vec4 skin = texture(TEXTURE, UV);
	// Exclusive full RGBA skin selection. No original garment remains underneath.
	if (owner.r > 0.5) { skin = texture(body_paint, UV); }
	else if (owner.g > 0.5) { skin = texture(tail_paint, UV); }
	else if (owner.b > 0.5) { skin = texture(scalp_paint, UV); }
	COLOR = skin;
}
