shader_type canvas_item;
render_mode unshaded;

// Keep the original painted round rim; discard the square crop's wall corners.
void fragment() {
	vec4 painted = texture(TEXTURE, UV);
	painted.a *= 1.0 - smoothstep(0.46, 0.49, length(UV - vec2(0.5)));
	COLOR = painted;
}
