shader_type canvas_item;
render_mode unshaded;
uniform sampler2D stream_mask : filter_nearest;
varying vec4 item_modulate;
void vertex() {
	item_modulate = COLOR;
}
void fragment() {
	vec4 pixel = texture(TEXTURE, UV);
	// Only the manifest-measured water arc is stopped. The approved fountain's
	// head, tail, paint, coral and base keep their exact canonical source pixels.
	pixel.a *= 1.0 - texture(stream_mask, UV).a;
	COLOR = pixel * item_modulate;
}
