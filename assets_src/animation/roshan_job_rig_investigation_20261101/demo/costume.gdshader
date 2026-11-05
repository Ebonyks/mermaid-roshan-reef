shader_type canvas_item;
uniform sampler2D body_paint : source_color, filter_linear;
uniform sampler2D tail_paint : source_color, filter_linear;
uniform sampler2D scalp_paint : source_color, filter_linear;
uniform sampler2D ownership : filter_nearest;
uniform bool new_body_binding = false;
vec4 over(vec4 under, vec4 garment) {
	if (garment.a <= 0.0) { return under; }
	float a = garment.a + under.a * (1.0 - garment.a);
	vec3 rgb = (garment.rgb * garment.a + under.rgb * under.a * (1.0 - garment.a)) / max(a, 0.00001);
	return vec4(rgb,a);
}
void fragment() {
	vec4 owner = texture(ownership, UV);
	// TEXTURE is anatomy.png: every original garment pixel is erased.
	vec4 anatomy = texture(TEXTURE, UV);
	vec4 skin = over(anatomy, texture(tail_paint,UV));
	skin = over(skin,texture(body_paint,UV));
	// Original hair, face, exposed skin, hands and fins remain in front.
	if (owner.a > 0.5 && (!new_body_binding || UV.y < 0.342 || UV.y > 0.49)) { skin = anatomy; }
	if (owner.b > 0.5) { skin = texture(scalp_paint,UV); }
	COLOR = skin;
}
