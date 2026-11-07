shader_type canvas_item;

// Roadside faces carry UV/depth plus a split-precision reciprocal depth in
// their vertex color. Other Canvas draws on this layer use ordinary UVs.
varying vec4 paint;

void vertex() {
	paint = COLOR;
}

void fragment() {
	if (UV.x >= 2.0 && UV.y >= 2.0) {
		float reciprocal_depth = max(0.0001, paint.r + paint.g / 255.0);
		vec2 atlas_uv = (UV - vec2(2.0)) / reciprocal_depth;
		COLOR = texture(TEXTURE, atlas_uv) * vec4(vec3(paint.b), 1.0);
	} else {
		COLOR = texture(TEXTURE, UV) * paint;
	}
}
