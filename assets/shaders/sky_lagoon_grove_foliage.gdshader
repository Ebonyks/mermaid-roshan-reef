shader_type canvas_item;
render_mode unshaded;

// The lower edge is pinned. Wind affects the canopy, never its ground contact.
uniform float breeze;
uniform float reach = 6.0;
uniform float spatial_wave = 0.0;
uniform bool cleanup_magenta = false;
uniform bool harvest_palette = false;
uniform float tree_height = 0.0;
varying vec4 card_tint;

void vertex() {
	float source_y = UV.y;
	if (tree_height > 0.0) {
		source_y = 1.0 + VERTEX.y / tree_height;
	}
	float rooted = (1.0 - source_y) * (1.0 - source_y);
	float phase = breeze + MODEL_MATRIX[3].x * spatial_wave;
	VERTEX.x += rooted * reach * (sin(phase + source_y * 2.0) + sin(phase * 1.9) * 0.27);
	// Shared seam positions, with a phase delay down the branch tiers.
	if (tree_height > 0.0) {
		VERTEX.x += rooted * reach * 0.34 * sin(phase * 1.31 + source_y * 6.0);
	}
	card_tint = COLOR;
}

vec3 storybook_harvest(vec3 paint) {
	float value = dot(paint, vec3(0.299, 0.587, 0.114));
	float red = smoothstep(0.07, 0.24, paint.r - paint.g);
	float blossom = smoothstep(0.58, 0.83, value)
		* (1.0 - smoothstep(0.10, 0.23, max(paint.r, paint.g) - paint.b));
	vec3 leaf = mix(vec3(0.19, 0.29, 0.23), vec3(0.39, 0.53, 0.31), smoothstep(0.17, 0.44, value));
	leaf = mix(leaf, vec3(0.67, 0.73, 0.43), smoothstep(0.48, 0.76, value));
	vec3 berry = mix(vec3(0.49, 0.18, 0.23), vec3(0.88, 0.36, 0.33), smoothstep(0.19, 0.47, value));
	berry = mix(berry, vec3(0.98, 0.63, 0.45), smoothstep(0.51, 0.79, value));
	return mix(mix(leaf, vec3(1.0, 0.91, 0.71), blossom), berry, red);
}

void fragment() {
	vec4 paint = texture(TEXTURE, UV);
	if (cleanup_magenta) {
		float pink = smoothstep(0.10, 0.24, min(paint.r, paint.b) - paint.g);
		paint.a *= 1.0 - pink * smoothstep(0.42, 0.67, paint.r);
	}
	if (harvest_palette) {
		vec4 broad_paint = texture(TEXTURE, UV, 1.35);
		vec3 simplified = mix(paint.rgb, broad_paint.rgb, broad_paint.a * 0.72);
		paint.rgb = storybook_harvest(simplified);
	}
	COLOR = paint * card_tint;
}

