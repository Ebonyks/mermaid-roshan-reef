shader_type canvas_item;
render_mode unshaded;
uniform sampler2D water_mask : filter_linear, repeat_disable;
uniform vec2 surface_center;
uniform vec2 sprite_size = vec2(192.0);
uniform vec2 atlas_cell;
void fragment() {
	vec2 cell_uv = UV * vec2(4.0, 2.0) - atlas_cell;
	vec2 master_uv = (surface_center + (cell_uv - vec2(0.5)) * sprite_size) / vec2(6144.0, 2048.0);
	float in_bounds = step(0.0, master_uv.x) * step(master_uv.x, 1.0) * step(0.0, master_uv.y) * step(master_uv.y, 1.0);
	COLOR.a *= texture(water_mask, clamp(master_uv, vec2(0.0), vec2(1.0))).a * in_bounds;
}
