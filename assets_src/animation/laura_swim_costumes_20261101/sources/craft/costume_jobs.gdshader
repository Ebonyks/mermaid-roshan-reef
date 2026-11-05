shader_type canvas_item;
uniform sampler2D body_paint : source_color, filter_linear;
uniform sampler2D tail_paint : source_color, filter_linear;
uniform sampler2D scalp_paint : source_color, filter_linear;
uniform sampler2D ownership : filter_nearest;
vec4 over(vec4 under, vec4 garment) {
	if (garment.a <= 0.0) { return under; }
	float a = garment.a + under.a * (1.0 - garment.a);
	vec3 rgb = (garment.rgb * garment.a + under.rgb * under.a * (1.0 - garment.a)) / max(a, 0.00001);
	return vec4(rgb,a);
}
uniform bool job_hands = false;
uniform sampler2D hand_source_left : filter_nearest;
uniform sampler2D hand_source_right : filter_nearest;
uniform sampler2D arm_right_upper : filter_nearest;
uniform sampler2D arm_right_fore : filter_nearest;
void fragment() {
	vec4 owner = texture(ownership, UV);
	// TEXTURE is anatomy.png: every original garment pixel is erased.
	vec4 anatomy = texture(TEXTURE, UV);
	bool hand_pixel = job_hands && max(max(texture(hand_source_left,UV).a,texture(hand_source_right,UV).a),max(texture(arm_right_upper,UV).a,texture(arm_right_fore,UV).a))>0.0;
	if (hand_pixel) { anatomy = vec4(0.0); }
	vec4 skin = over(anatomy, texture(tail_paint,UV));
	skin = over(skin,texture(body_paint,UV));
	// Original hair, face, exposed skin, hands and fins remain in front.
	if (owner.a > 0.5 && !hand_pixel) { skin = anatomy; }
	if (owner.b > 0.5) { skin = texture(scalp_paint,UV); }
	COLOR = skin;
}
