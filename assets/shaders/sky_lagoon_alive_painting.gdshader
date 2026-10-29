// Sky Lagoon "alive painting" demo shader (true-2D Canvas, Mobile renderer).
//
// Draws the unchanged approved v5 panorama tiles as one continuous 6144x2048
// master-pixel surface so displaced samples never smear at tile seams. Motion
// is restrained 2D idle motion (DL-MED-05): the authored pixels are only
// re-sampled a few master pixels away, never relit or recoloured, except for a
// small additive glint/ripple highlight on open water.
//
// Material masks are computed from the painting's own colours plus coarse
// master-pixel regions. No mask image exists in the repository: a hand-painted
// motion mask is a named Codex gap in docs/handoffs/codex_sky_lagoon_alive_2026-10-18/.
// The same shader runs twice. With mask_pass on, it draws once into a small
// SubViewport (rgb = foliage/water/cloud, a = depth), sampling the painting on
// a coarse grid so the field is smooth and leaves do not "boil" independently.
// The visible pass then reads that buffer with linear filtering: two texture
// reads per pixel instead of re-classifying every frame.
shader_type canvas_item;
render_mode unshaded, blend_disabled;

// Row-major: index = row * 6 + column. Constant-index access only (see tile()).
uniform sampler2D tiles[12] : source_color, filter_linear, repeat_disable;
uniform vec2 master_size = vec2(6144.0, 2048.0);
// Seconds supplied by the demo script so ripple start times share one clock.
uniform float now = 0.0;
// 0 = painting exactly as authored; 1 = full demo motion. Lets the owner A/B.
uniform float motion_amount : hint_range(0.0, 1.0) = 1.0;
// Camera position across the panorama, -1 (left) .. 1 (right).
uniform float camera_norm = 0.0;
uniform float parallax_px = 30.0;
uniform float sway_px = 9.0;
uniform float water_px = 5.0;
uniform float cloud_px = 10.0;
uniform float glint_strength = 0.22;
// Per-object nudges: xy master centre, z radius, w strength (0 = unused).
// Used for "this bush shakes" after a tap; decays in the script.
uniform vec4 shakes[4];
// Tap ripples: xy master position, z start time (same clock as now), w strength.
uniform vec4 ripples[6];
uniform bool mask_pass = false;
uniform sampler2D motion_mask : filter_linear, repeat_disable;

const float GRID = 20.0;
const float RIPPLE_LIFE = 1.6;
const float RIPPLE_SPEED = 620.0;

varying vec2 master_pos;

void vertex() {
	master_pos = VERTEX;
}

vec4 tile(vec2 p) {
	p = clamp(p, vec2(0.5), master_size - vec2(0.5));
	int column = int(p.x / 1024.0);
	int row = int(p.y / 1024.0);
	vec2 uv = (p - vec2(float(column), float(row)) * 1024.0) / 1024.0;
	int index = row * 6 + column;
	// Constant indices keep sampler-array access legal on every Mobile GPU.
	if (index == 0) { return texture(tiles[0], uv); }
	if (index == 1) { return texture(tiles[1], uv); }
	if (index == 2) { return texture(tiles[2], uv); }
	if (index == 3) { return texture(tiles[3], uv); }
	if (index == 4) { return texture(tiles[4], uv); }
	if (index == 5) { return texture(tiles[5], uv); }
	if (index == 6) { return texture(tiles[6], uv); }
	if (index == 7) { return texture(tiles[7], uv); }
	if (index == 8) { return texture(tiles[8], uv); }
	if (index == 9) { return texture(tiles[9], uv); }
	if (index == 10) { return texture(tiles[10], uv); }
	return texture(tiles[11], uv);
}

vec3 rgb_to_hsv(vec3 c) {
	vec4 k = vec4(0.0, -1.0 / 3.0, 2.0 / 3.0, -1.0);
	vec4 p = mix(vec4(c.bg, k.wz), vec4(c.gb, k.xy), step(c.b, c.g));
	vec4 q = mix(vec4(p.xyw, c.r), vec4(c.r, p.yzx), step(p.x, c.r));
	float d = q.x - min(q.w, q.y);
	float e = 1.0e-10;
	return vec3(abs(q.z + (q.w - q.y) / (6.0 * d + e)), d / (q.x + e), q.x);
}

float band(float x, float lo, float hi, float soft) {
	return smoothstep(lo - soft, lo, x) * (1.0 - smoothstep(hi, hi + soft, x));
}

// x = foliage, y = water, z = cloud. Thresholds were measured from the v5
// painting (sky h188 s0.65 v0.89; water h189 s0.98; lawn h72 v0.69;
// shrubs h150-170 v0.35-0.40; cloud sea / sky clouds s<0.2 v>0.88).
vec3 classify(vec2 p) {
	vec3 hsv = rgb_to_hsv(tile(p).rgb);
	float hue = hsv.x * 360.0;
	float in_lakes = max(
		band(p.x, -100.0, 700.0, 60.0) * band(p.y, 1120.0, 1480.0, 40.0),
		band(p.x, 4450.0, 6300.0, 80.0) * band(p.y, 960.0, 1620.0, 40.0));
	float water = in_lakes * band(hue, 178.0, 200.0, 6.0)
		* smoothstep(0.62, 0.8, hsv.y) * band(hsv.z, 0.38, 0.92, 0.05);
	float foliage = band(hue, 82.0, 205.0, 10.0) * smoothstep(0.3, 0.45, hsv.y)
		* (1.0 - smoothstep(0.5, 0.64, hsv.z)) * smoothstep(240.0, 320.0, p.y);
	foliage *= 1.0 - water;
	// The left fir reaches into the sky; only it may sway above the horizon.
	foliage *= max(smoothstep(860.0, 960.0, p.y), 1.0 - smoothstep(330.0, 420.0, p.x));
	// Sky clouds are near-white; the cloud sea carries blue shading (s<=0.35).
	float sky_white = (1.0 - smoothstep(0.12, 0.22, hsv.y)) * smoothstep(0.86, 0.92, hsv.z);
	float sea_white = (1.0 - smoothstep(0.32, 0.42, hsv.y)) * smoothstep(0.82, 0.88, hsv.z);
	float sky_clouds = (1.0 - smoothstep(720.0, 800.0, p.y))
		* max(1.0 - smoothstep(4300.0, 4420.0, p.x),
			band(p.x, 5050.0, 5800.0, 40.0) * (1.0 - smoothstep(330.0, 380.0, p.y)));
	// Starts below the hazy far peaks so mountains stay still.
	float cloud_sea = band(p.x, 480.0, 3450.0, 120.0) * band(p.y, 930.0, 1300.0, 50.0);
	float cloud = max(sky_white * sky_clouds, sea_white * cloud_sea);
	return vec3(foliage, water, cloud);
}

vec3 smooth_class(vec2 p) {
	vec2 cell = floor(p / GRID);
	vec2 f = fract(p / GRID);
	vec3 a = classify((cell + vec2(0.5, 0.5)) * GRID);
	vec3 b = classify((cell + vec2(1.5, 0.5)) * GRID);
	vec3 c = classify((cell + vec2(0.5, 1.5)) * GRID);
	vec3 d = classify((cell + vec2(1.5, 1.5)) * GRID);
	vec2 s = f * f * (3.0 - 2.0 * f);
	return mix(mix(a, b, s.x), mix(c, d, s.x), s.y);
}

// 0 = sky/far, 1 = nearest painted foreground. Smooth so parallax warps
// instead of tearing; the near fir is lifted toward the viewer.
float depth(vec2 p) {
	float ground = smoothstep(760.0, 2048.0, p.y);
	float fir = (1.0 - smoothstep(330.0, 460.0, p.x)) * smoothstep(40.0, 260.0, p.y) * 0.55;
	return max(ground * ground * 0.8 + ground * 0.2, fir);
}

vec3 animate(vec2 p, float foliage, float water, float cloud, float near) {
	vec2 offset = vec2(camera_norm * (near - 0.35) * parallax_px, 0.0);

	float phase = p.x * 0.0035 + p.y * 0.0012;
	float gust = 0.65 + 0.35 * sin(now * 0.37 + p.x * 0.0004);
	offset.x += foliage * sway_px * (0.35 + near) * gust
		* (sin(now * 1.25 + phase) + 0.35 * sin(now * 2.7 + phase * 2.3));
	offset.y += foliage * sway_px * 0.25 * sin(now * 1.6 + phase * 1.7);
	for (int i = 0; i < 4; i++) {
		vec4 s = shakes[i];
		if (s.w <= 0.0) {
			continue;
		}
		float reach = 1.0 - smoothstep(s.z * 0.45, s.z, distance(p, s.xy));
		offset.x += foliage * reach * s.w * sway_px * 2.2 * sin(now * 15.0 + p.y * 0.02);
	}

	offset += water * water_px * vec2(
		sin(p.y * 0.085 + now * 1.7) * 0.6 + sin(p.x * 0.012 + now * 0.9) * 0.4,
		sin(p.x * 0.045 - now * 1.3) * 0.35);
	offset += cloud * cloud_px * vec2(
		sin(now * 0.31 + p.y * 0.008),
		0.35 * sin(now * 0.47 + p.x * 0.0025));

	float lift = 0.0;
	for (int i = 0; i < 6; i++) {
		vec4 r = ripples[i];
		if (r.w <= 0.0) {
			continue;
		}
		float age = now - r.z;
		if (age < 0.0 || age > RIPPLE_LIFE) {
			continue;
		}
		vec2 d = p - r.xy;
		float dist = length(d);
		float ring = exp(-pow((dist - age * RIPPLE_SPEED) / 55.0, 2.0));
		float fade = (1.0 - age / RIPPLE_LIFE) * r.w;
		float responsive = 0.25 + 0.75 * max(max(water, foliage), cloud);
		offset += (d / max(dist, 1.0)) * ring * fade * 16.0 * responsive;
		lift += ring * fade * water * 0.22;
	}

	vec3 color = tile(p + offset * motion_amount).rgb;
	float sparkle = smoothstep(0.93, 1.0,
		sin(p.x * 0.041 + now * 2.1) * sin(p.y * 0.12 - now * 1.45));
	return color + vec3(water * sparkle * glint_strength + lift) * motion_amount;
}

void fragment() {
	vec2 p = master_pos;
	if (mask_pass) {
		COLOR = vec4(smooth_class(p - vec2(GRID * 0.5)), depth(p));
	} else if (motion_amount <= 0.0) {
		COLOR = vec4(tile(p).rgb, 1.0);
	} else {
		vec4 m = texture(motion_mask, p / master_size);
		COLOR = vec4(animate(p, m.r, m.g, m.b, m.a), 1.0);
	}
}
