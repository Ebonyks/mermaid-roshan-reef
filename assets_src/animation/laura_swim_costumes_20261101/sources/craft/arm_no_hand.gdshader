shader_type canvas_item;
uniform vec2 wrist_source_px;
uniform vec2 fore_axis;
void fragment() {
	vec4 paint = texture(TEXTURE,UV);
	// Retain the painted forearm; the authored grip view owns the wrist/hand.
	if (dot(UV*1024.0-wrist_source_px,fore_axis)>0.0) { paint = vec4(0.0); }
	COLOR = paint;
}
