shader_type canvas_item;
render_mode unshaded;

uniform sampler2D surface_texture : source_color, filter_linear_mipmap, repeat_enable;
uniform sampler2D paint_detail : source_color, filter_linear_mipmap;
uniform int surface_kind;
uniform vec4 surface_tint : source_color = vec4(1.0);
uniform float water_time;
uniform vec4 water_footprint;
uniform vec4 spring_footprint;
uniform float bank_seed;
uniform vec4 patch_world;
uniform bool valley_main_trail = false;
varying vec2 ground;
varying vec4 ink;

void vertex() {
	ground = VERTEX;
	ink = COLOR;
}

float painted_shore(vec2 p) {
	vec2 delta = p - water_footprint.xy;
	if (water_footprint.w < 0.0) {
		float axis = sin(delta.y * 0.0061) * 45.0 + sin(delta.y * 0.011) * 14.0;
		float creek_width = water_footprint.z * mix(0.42, 1.0, smoothstep(944.0, 1050.0, p.y));
		float river_shore = abs(delta.x - axis) / creek_width;
		float spring_shore = length((p - spring_footprint.xy) / spring_footprint.zw);
		return p.y < spring_footprint.y + 6.0 ? spring_shore : min(spring_shore, river_shore);
	}
	vec2 local = delta / max(water_footprint.zw, vec2(1.0));
	float angle = atan(local.y, local.x);
	float uneven = 1.0 + 0.045 * sin(angle * 5.0 + bank_seed) + 0.019 * sin(angle * 11.0);
	return length(local) / uneven;
}

vec2 mirror_paint(vec2 at) {
	return 1.0 - abs(fract(at * 0.5) * 2.0 - 1.0);
}

float habitat(vec2 point, vec2 center, vec2 extent) {
	vec2 p = (point - center) / extent;
	float brush = sin(point.x * 0.019 + point.y * 0.013) * 0.08
		+ cos(point.y * 0.031 - point.x * 0.007) * 0.06;
	return 1.0 - smoothstep(0.27, 1.05, length(p) + brush);
}

void fragment() {
	vec2 p = ground;
	if (surface_kind == 0) {
		float shore = painted_shore(p);
		float flow = 0.017 * water_time;
		vec2 bend = vec2(sin(p.y * 0.012 + water_time * 0.63) * 0.034, 0.0);
		vec3 brush = texture(surface_texture, mirror_paint(p / vec2(498.0, 296.0) + bend - vec2(0.006 * water_time, flow))).rgb;
		float brush_value = dot(brush, vec3(0.30, 0.52, 0.18)) - 0.56;
		vec3 deep = vec3(0.21, 0.43, 0.51);
		vec3 shallows = vec3(0.36, 0.56, 0.56);
		vec3 water = mix(deep, shallows, smoothstep(0.47, 1.05, shore));
		water += brush_value * vec3(0.19, 0.25, 0.26);
		float glint = smoothstep(0.90, 0.98, shore) * (1.0 - smoothstep(0.99, 1.06, shore));
		float broken = 0.38 + 0.29 * sin(p.x * 0.063 + p.y * 0.037 + water_time);
		water += glint * broken * vec3(0.09, 0.10, 0.067);
		COLOR = vec4(water, 1.0);
	} else if (surface_kind == 1) {
		vec3 brush = texture(surface_texture, p / vec2(680.0, 481.0)).rgb;
		vec2 fold = 1.0 - abs(fract(p / vec2(885.0, 410.0)) * 2.0 - 1.0);
		vec3 meadow = texture(paint_detail, vec2(0.51, 0.265) + fold * vec2(0.45, 0.221)).rgb;
		float hue = 0.5 + 0.24 * sin(p.x * 0.0031 + p.y * 0.0071) + 0.19 * cos(p.y * 0.0045);
		vec3 base = mix(vec3(0.35, 0.49, 0.31), vec3(0.58, 0.67, 0.41), hue);
		vec3 paint = mix(base, meadow * vec3(0.93, 0.98, 0.90), 0.38) + (brush - vec3(0.65, 0.68, 0.51)) * 0.16;
		float fern = habitat(p, vec2(1510.0, 1073.0), vec2(425.0, 315.0));
		float pond = habitat(p, vec2(2490.0, 1334.0), vec2(450.0, 249.0));
		float woodland = habitat(p, vec2(4180.0, 1066.0), vec2(550.0, 373.0));
		float ridge = habitat(p, vec2(5094.0, 1090.0), vec2(449.0, 296.0));
		float valley = habitat(p, vec2(990.0, 1196.0), vec2(1040.0, 350.0));
		paint = mix(paint, paint * vec3(1.12, 1.05, 0.77) + vec3(0.05, 0.025, 0.0), valley);
		float shade_pockets = max(habitat(p, vec2(453.0, 1090.0), vec2(235.0, 120.0)),
			habitat(p, vec2(958.0, 1380.0), vec2(220.0, 101.0)));
		shade_pockets = max(shade_pockets, habitat(p, vec2(1532.0, 1314.0), vec2(218.0, 110.0)));
		paint *= mix(vec3(1.0), vec3(0.77, 0.86, 0.71), shade_pockets);
		paint *= mix(vec3(1.0), vec3(0.71, 0.91, 0.87), fern);
		paint *= mix(vec3(1.0), vec3(0.85, 1.02, 1.13), pond);
		paint *= mix(vec3(1.0), vec3(0.67, 0.82, 0.83), woodland);
		paint = mix(paint, paint * vec3(1.19, 1.01, 0.78) + vec3(0.033, 0.004, 0.003), ridge);
		float wooded = smoothstep(0.25, 0.8, abs(sin(p.x * 0.004 + p.y * 0.008) *
			cos(p.y * 0.006 + 1.2)));
		float cloud = smoothstep(0.2, 0.8, sin(p.x * 0.0031 + p.y * 0.0052 - water_time * 0.17));
		paint *= (1.0 - wooded * 0.17) * mix(vec3(0.94, 0.99, 1.02), vec3(1.05, 1.04, 0.92), cloud);
		COLOR = vec4(paint, 1.0) * surface_tint * ink;
	} else if (surface_kind == 6) {
		vec2 local = (p - patch_world.xy) / patch_world.zw;
		float chips = sin(p.x * 0.12 + p.y * 0.09) * sin(p.y * 0.17) * 0.025;
		float edge = 1.0 - smoothstep(0.84, 0.97, length(local) + chips);
		vec3 rock = texture(surface_texture, p / vec2(155.0, 117.0)).rgb;
		vec3 bank = mix(vec3(0.56, 0.57, 0.43), rock, 0.44);
		COLOR = vec4(bank, edge) * surface_tint;
	} else if (surface_kind == 8) {
		vec3 rock = texture(surface_texture, p / vec2(156.0, 119.0)).rgb;
		float chips = 0.07 * sin(p.x * 0.11) * sin(p.y * 0.084);
		float edge = 1.0 - smoothstep(1.04, 1.25, painted_shore(p) + chips);
		COLOR = vec4(mix(vec3(0.57, 0.58, 0.43), rock, 0.47), edge) * surface_tint;
	} else if (surface_kind == 7) {
		vec3 paving = texture(surface_texture, p / vec2(159.0, 127.0)).rgb;
		float value = dot(paving, vec3(0.31, 0.51, 0.18));
		float blocks = smoothstep(0.38, 0.80, value);
		vec3 painted = mix(vec3(0.51, 0.43, 0.41), vec3(0.78, 0.70, 0.62), blocks);
		vec3 trail = mix(painted, paving * vec3(0.99, 0.92, 0.87), 0.24);
		float dry = float(valley_main_trail) * smoothstep(630.0, 940.0, p.x) * (1.0 - smoothstep(1420.0, 1950.0, p.x));
		float grain = texture(surface_texture, p / vec2(435.0, 389.0)).r - 0.56;
		vec3 soil = vec3(0.67, 0.56, 0.40) + grain * 0.083;
		trail = mix(trail, soil, dry);
		COLOR = vec4(trail, 1.0) * surface_tint * ink;
	} else {
		vec3 stone = texture(surface_texture, p / vec2(218.0, 150.0)).rgb;
		vec2 fold = 1.0 - abs(fract(p / vec2(721.0, 246.0)) * 2.0 - 1.0);
		vec3 lilac = texture(paint_detail, vec2(0.23, 0.555) + fold * vec2(0.73, 0.10)).rgb;
		stone = mix(stone, lilac, 0.49);
		float edge = 1.0;
		if (surface_kind == 5) {
			vec2 local = (p - patch_world.xy) / patch_world.zw;
			float chips = sin(p.x * 0.10 + p.y * 0.13) * sin(p.y * 0.08) * 0.065;
			edge = 1.0 - smoothstep(0.62, 1.03, length(local) + chips);
		}
		COLOR = vec4(mix(stone, vec3(0.67, 0.60, 0.55), 0.22), edge) * surface_tint * ink;
	}
}

