shader_type canvas_item;
render_mode unshaded;

uniform vec4 atlas_uv_rect = vec4(0.0, 0.0, 1.0, 1.0);
uniform vec3 water_color : source_color = vec3(0.23, 0.68, 0.70);
uniform float immersion : hint_range(0.0, 1.0) = 1.0;
uniform bool suppress_aura = true;
varying vec4 item_modulate;

void vertex() {
	item_modulate = COLOR;
}

void fragment() {
	vec4 pixel = texture(TEXTURE, UV);
	vec2 local_uv = (UV - atlas_uv_rect.xy) / atlas_uv_rect.zw;
	// Remove the low-alpha product-photo aura, retaining painted antialiasing.
	if (suppress_aura) {
		pixel.a *= smoothstep(0.08, 0.32, pixel.a);
	}
	float value = dot(pixel.rgb, vec3(0.2126, 0.7152, 0.0722));
	pixel.rgb = mix(pixel.rgb, vec3(value), 0.17);
	// A shallow submerged lower edge shares the water's colour and transparency.
	float wet_edge = smoothstep(0.57, 0.85, local_uv.y) * immersion;
	pixel.rgb = mix(pixel.rgb, water_color, wet_edge * 0.26);
	pixel.a *= 1.0 - wet_edge * 0.22;
	COLOR = pixel * item_modulate;
}
