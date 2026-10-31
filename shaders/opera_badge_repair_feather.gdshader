shader_type canvas_item;
render_mode unshaded;

void fragment() {
	vec4 painted = texture(TEXTURE, UV);
	vec2 edge = min(UV, vec2(1.0) - UV);
	painted.a *= smoothstep(0.0, 0.08, min(edge.x, edge.y));
	COLOR = painted;
}
