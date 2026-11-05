shader_type canvas_item;
// Pearl Canal Circuit ground: each pixel below the horizon is projected onto
// the flat course plane as seen from a camera behind the kart. One full-width
// Canvas rectangle; no spatial nodes, lights or meshes.
//
// The original Canal samples its painted floor. Room courses use their own
// materials. Every floor also samples the road-distance field for the shared
// curb, direction chevrons and ground start/finish plane.

uniform vec2 rect_size = vec2(1280.0, 452.0);
uniform vec2 cam_pos = vec2(480.0, 1565.0);
uniform vec2 cam_forward = vec2(1.0, 0.0);
uniform vec2 cam_right = vec2(0.0, 1.0);
uniform float cam_height = 34.0;
uniform float focal = 560.0;
uniform float world_size = 2048.0;
uniform bool use_painted = false;
uniform int room_pattern = 0;
uniform vec2 finish_pos;
uniform vec2 finish_forward;
uniform vec4 boundary_ink : source_color = vec4(0.17, 0.12, 0.28, 1.0);
uniform vec4 bridge_a;
uniform vec4 bridge_b;
uniform sampler2D painted_floor : source_color, filter_linear_mipmap, repeat_disable;
uniform sampler2D field : filter_linear, repeat_disable;
uniform float road_edge = 0.5;
uniform float rail_edge = 0.625;
uniform float lane_line = 0.1786;
uniform float time = 0.0;
uniform vec4 water_a : source_color = vec4(0.443, 0.863, 0.839, 1.0);
uniform vec4 water_b : source_color = vec4(0.369, 0.792, 0.808, 1.0);
uniform vec4 lane_paint : source_color = vec4(0.808, 0.957, 0.937, 1.0);
uniform vec4 foam : source_color = vec4(0.882, 0.976, 0.957, 1.0);
uniform vec4 curb_a : source_color = vec4(0.914, 0.827, 0.659, 1.0);
uniform vec4 curb_b : source_color = vec4(0.863, 0.753, 0.576, 1.0);
uniform vec4 wall_a : source_color = vec4(0.725, 0.639, 0.851, 1.0);
uniform vec4 wall_b : source_color = vec4(0.608, 0.510, 0.769, 1.0);
uniform vec4 pearl_stud : source_color = vec4(0.957, 0.933, 0.980, 1.0);
uniform vec4 sand_a : source_color = vec4(0.906, 0.812, 0.624, 1.0);
uniform vec4 sand_b : source_color = vec4(0.863, 0.753, 0.549, 1.0);
uniform vec4 coral_pink : source_color = vec4(0.937, 0.400, 0.553, 1.0);
uniform vec4 coral_orange : source_color = vec4(0.969, 0.553, 0.384, 1.0);
uniform vec4 coral_teal : source_color = vec4(0.247, 0.722, 0.651, 1.0);
uniform vec4 rock_purple : source_color = vec4(0.490, 0.420, 0.690, 1.0);
uniform vec4 haze : source_color = vec4(0.475, 0.788, 0.902, 1.0);
uniform float haze_start = 650.0;
uniform float haze_end = 2100.0;

float checker(vec2 w, float cell) {
	vec2 c = floor(w / cell);
	return mod(c.x + c.y, 2.0);
}

float hash(vec2 p) {
	return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453);
}

float soft_checker(vec2 point, float cell) {
	vec2 at = fract(point / cell * 0.5) * 2.0;
	vec2 spread = clamp(fwidth(point) / cell, vec2(0.01), vec2(0.5));
	vec2 half_cell = smoothstep(vec2(1.0) - spread, vec2(1.0) + spread, at);
	vec2 wrap_cell = smoothstep(vec2(2.0) - spread, vec2(2.0), at)
		+ (1.0 - smoothstep(vec2(0.0), spread, at));
	half_cell = mix(half_cell, vec2(0.5), wrap_cell);
	return half_cell.x + half_cell.y - 2.0 * half_cell.x * half_cell.y;
}

bool on_bridge(vec2 world, vec4 limits) {
	return all(greaterThan(world, limits.xy)) && all(lessThan(world, limits.zw));
}

vec4 room_floor(vec2 world, float d, float detail) {
	float tile = soft_checker(world, 52.0);
	float waves = 0.5 + 0.5 * sin(world.x * 0.032 + sin(world.y * 0.028) * 2.2 + time);
	float floor_pattern = mix(tile, waves, float(room_pattern == 3));
	vec4 ground = mix(sand_a, sand_b, mix(0.5, floor_pattern, detail * 0.64));
	float road_pattern = mix(tile, waves, float(room_pattern == 3));
	if (room_pattern == 4) {
		vec2 stitch = abs(fract((world + vec2(world.y, -world.x)) / 78.0) - 0.5);
		road_pattern = smoothstep(0.39, 0.48, max(stitch.x, stitch.y));
	}
	vec4 road = mix(water_a, water_b, mix(0.5, road_pattern, detail * 0.38));
	bool bridge = on_bridge(world, bridge_a) || on_bridge(world, bridge_b);
	if (bridge) {
		float seam = smoothstep(0.86, 0.97, fract(world.x / 28.0));
		float grain = hash(vec2(floor(world.x / 28.0), 7.0));
		road = mix(vec4(0.77, 0.52, 0.34, 1.0), vec4(0.53, 0.32, 0.23, 1.0),
			mix(0.35, grain * 0.47 + seam * 0.53, detail));
	}
	float edge = max(fwidth(d), 0.006);
	float road_mask = 1.0 - smoothstep(road_edge - edge, road_edge + edge, d);
	float apron = 1.0 - smoothstep(rail_edge - edge, rail_edge + edge, d);
	float stripes = mix(0.55, 0.36 + tile * 0.35, detail);
	vec4 color = mix(ground, mix(foam, curb_b, stripes), apron);
	color = mix(color, road, road_mask);
	return color;
}

vec4 race_markings(vec2 world, float d, vec4 color) {
	float aa = max(fwidth(d), 0.004);
	// Both sides have a dark contour, broad alternating curb, and pale
	// inner edge. Their thresholds use the same lane and rail radii as physics.
	float outer = 1.0 - smoothstep(rail_edge + 0.018, rail_edge + 0.018 + aa, d);
	float inner = smoothstep(road_edge - 0.036 - aa, road_edge - 0.036, d);
	float ring = outer * inner;
	float curb = smoothstep(road_edge + aa, road_edge + 0.024 + aa, d)
		* (1.0 - smoothstep(rail_edge - 0.020 - aa, rail_edge - 0.020, d));
	float stripe = soft_checker(world, 38.0);
	vec4 curb_color = mix(foam, wall_a, stripe * 0.85);
	color = mix(color, boundary_ink, ring);
	color = mix(color, curb_color, curb);
	float edge_paint = (1.0 - smoothstep(road_edge - 0.050 - aa, road_edge - 0.050, d))
		* smoothstep(road_edge - 0.077 - aa, road_edge - 0.077, d);
	color = mix(color, foam, edge_paint);
	vec2 from_line = world - finish_pos;
	float along = dot(from_line, finish_forward);
	float across = dot(from_line, vec2(-finish_forward.y, finish_forward.x));
	float on_road = 1.0 - smoothstep(road_edge - aa, road_edge + aa, d);
	float gold_frame = (1.0 - smoothstep(34.0, 38.0, abs(along)))
		* (1.0 - smoothstep(108.0, 112.0, abs(across)));
	color = mix(color, curb_a, gold_frame * on_road);
	float finish_mask = (1.0 - smoothstep(25.0, 28.0, abs(along)))
		* (1.0 - smoothstep(108.0, 112.0, abs(across)));
	float squares = soft_checker(vec2(along, across), 18.0);
	vec4 finish = mix(boundary_ink, foam, squares);
	color = mix(color, finish, finish_mask * on_road);
	// Three chevrons run toward the common start/finish plane.
	float arrow_station = -90.0 - floor(clamp((-along - 70.0) / 92.0, 0.0, 2.0)) * 92.0;
	float head = abs(along - arrow_station + abs(across) * 0.72);
	float arrow = (1.0 - smoothstep(4.0, 7.0, head))
		* (1.0 - smoothstep(24.0, 29.0, abs(across)));
	float approach = step(-340.0, along) * step(along, -65.0);
	color = mix(color, foam, arrow * approach * on_road);
	return color;
}

void fragment() {
	vec2 pixel = UV * rect_size;
	float dy = max(pixel.y, 0.75);
	float depth = cam_height * focal / dy;
	float lateral = (pixel.x - rect_size.x * 0.5) * depth / focal;
	vec2 world = cam_pos + cam_forward * depth + cam_right * lateral;
	vec2 uv = world / world_size;
	bool inside = uv.x >= 0.0 && uv.y >= 0.0 && uv.x <= 1.0 && uv.y <= 1.0;
	// Distant texels shimmer; fade fine patterns out as depth grows.
	float detail = 1.0 - smoothstep(380.0, 1100.0, depth);
	vec4 color;
	if (use_painted) {
		color = inside ? texture(painted_floor, uv) : mix(sand_a, sand_b, 0.5);
	} else if (room_pattern > 0) {
		float d = inside ? texture(field, uv).r : 1.0;
		color = room_floor(world, d, detail);
	} else {
		float d = inside ? texture(field, uv).r : 1.0;
		if (d < road_edge - 0.05) {
			float ripple = 0.5 + 0.5 * sin(world.x * 0.045 + world.y * 0.03 + time * 1.6);
			color = mix(water_a, water_b, mix(0.5, ripple, detail));
			float line = 1.0 - smoothstep(0.004, 0.011, abs(d - lane_line));
			color = mix(color, lane_paint, line * mix(0.4, 0.85, detail));
		} else if (d < road_edge) {
			color = foam;
		} else if (d < rail_edge) {
			float joint = step(0.9, fract(dot(world, vec2(0.7071, 0.7071)) / 40.0));
			color = mix(mix(curb_a, curb_b, mix(0.5, hash(floor(world / 20.0)), detail * 0.6)),
				curb_b * 0.9, joint * detail);
		} else if (d < rail_edge + 0.05) {
			float stud = step(0.82, fract(dot(world, vec2(0.7071, 0.7071)) / 34.0));
			color = mix(mix(wall_a, wall_b, mix(0.5, checker(world, 26.0), detail)), pearl_stud, stud * detail);
		} else {
			vec2 cell = floor(world / 26.0);
			float roll = hash(cell);
			color = mix(sand_a, sand_b, mix(0.5, hash(cell + 7.0), detail));
			if (roll > 0.9) {
				float pick = hash(cell + 3.0);
				vec4 spot = pick < 0.25 ? coral_pink : (pick < 0.5 ? coral_orange
					: (pick < 0.75 ? coral_teal : rock_purple));
				color = mix(color, spot, detail * 0.85);
			}
		}
	}
	float distance_field = inside ? texture(field, uv).r : 1.0;
	color = race_markings(world, distance_field, color);
	float h = smoothstep(haze_start, haze_end, depth);
	COLOR = vec4(mix(color.rgb, haze.rgb, h * 0.86), 1.0);
}
