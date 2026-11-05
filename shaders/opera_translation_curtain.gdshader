shader_type canvas_item;
render_mode unshaded;
#include "res://shaders/opera_translation_palette.gdshaderinc"
uniform float phase = 0.0;
uniform vec2 pixel_to_legacy = vec2(1.0);
varying vec4 vertex_tint;

void vertex() {
	vertex_tint = COLOR;
	VERTEX.x += sin(phase + VERTEX.y * 0.055 * pixel_to_legacy.y)
		* (1.25 / pixel_to_legacy.x)
		* smoothstep(0.0, 60.0 / pixel_to_legacy.y, VERTEX.y);
}

void fragment() {
	vec4 painted = texture(TEXTURE, UV);
	COLOR = vec4(opera_palette(painted.rgb), painted.a) * vertex_tint;
}
