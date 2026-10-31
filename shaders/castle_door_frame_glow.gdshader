shader_type canvas_item;
render_mode unshaded;

uniform float motion_time = 0.0;
uniform float frame_family = 0.0;
uniform float cue_mode = 0.0;
uniform float cue_alpha = 0.36;
uniform float feedback_strength = 0.0;
uniform float shimmer_period = 4.6;

float frame_region(vec2 uv) {
	if (frame_family < 0.5) {
		float top = (1.0 - smoothstep(0.37, 0.43, uv.y))
			* smoothstep(0.03, 0.10, uv.x)
			* (1.0 - smoothstep(0.89, 0.96, uv.x));
		float left_post = (1.0 - smoothstep(0.28, 0.33, uv.x))
			* smoothstep(0.25, 0.31, uv.y);
		float right_post = smoothstep(0.66, 0.71, uv.x)
			* (1.0 - smoothstep(0.89, 0.94, uv.x))
			* smoothstep(0.25, 0.31, uv.y);
		return max(top, max(left_post, right_post));
	}
	if (frame_family < 1.5) {
		float top = (1.0 - smoothstep(0.28, 0.34, uv.y));
		float left_post = (1.0 - smoothstep(0.22, 0.27, uv.x))
			* smoothstep(0.18, 0.24, uv.y);
		float right_post = smoothstep(0.73, 0.78, uv.x)
			* smoothstep(0.18, 0.24, uv.y);
		return max(top, max(left_post, right_post));
	}
	float shell_crown = (1.0 - smoothstep(0.19, 0.25, uv.y))
		* smoothstep(0.18, 0.25, uv.x)
		* (1.0 - smoothstep(0.75, 0.82, uv.x));
	float arch = smoothstep(0.12, 0.19, uv.y)
		* (1.0 - smoothstep(0.33, 0.39, uv.y))
		* smoothstep(0.03, 0.08, uv.x)
		* (1.0 - smoothstep(0.92, 0.97, uv.x));
	float left_column = (1.0 - smoothstep(0.28, 0.33, uv.x))
		* smoothstep(0.24, 0.30, uv.y)
		* (1.0 - smoothstep(0.76, 0.81, uv.y));
	float right_column = smoothstep(0.67, 0.72, uv.x)
		* smoothstep(0.24, 0.30, uv.y)
		* (1.0 - smoothstep(0.76, 0.81, uv.y));
	return max(max(shell_crown, arch), max(left_column, right_column));
}

float ellipse_mask(vec2 point, vec2 center, vec2 radius) {
	vec2 normalized = (point - center) / radius;
	return 1.0 - smoothstep(0.91, 1.02, length(normalized));
}

float opening_region(vec2 uv) {
	if (frame_family < 0.5) {
		float arch = ellipse_mask(uv, vec2(0.50, 0.39), vec2(0.275, 0.19))
			* (1.0 - smoothstep(0.39, 0.43, uv.y));
		float body = smoothstep(0.215, 0.245, uv.x)
			* (1.0 - smoothstep(0.755, 0.785, uv.x))
			* smoothstep(0.37, 0.41, uv.y)
			* (1.0 - smoothstep(0.94, 0.985, uv.y));
		return max(arch, body);
	}
	if (frame_family < 1.5) {
		float arch = ellipse_mask(uv, vec2(0.50, 0.31), vec2(0.345, 0.19))
			* (1.0 - smoothstep(0.31, 0.36, uv.y));
		float body = smoothstep(0.145, 0.18, uv.x)
			* (1.0 - smoothstep(0.82, 0.855, uv.x))
			* smoothstep(0.28, 0.33, uv.y)
			* (1.0 - smoothstep(0.94, 0.985, uv.y));
		return max(arch, body);
	}
	float arch = ellipse_mask(uv, vec2(0.50, 0.31), vec2(0.285, 0.16))
		* (1.0 - smoothstep(0.31, 0.36, uv.y));
	float body = smoothstep(0.215, 0.255, uv.x)
		* (1.0 - smoothstep(0.745, 0.785, uv.x))
		* smoothstep(0.29, 0.34, uv.y)
		* (1.0 - smoothstep(0.72, 0.77, uv.y));
	return max(arch, body);
}

float painted_frame_mask(vec4 sample_color, vec2 uv) {
	float luma = dot(sample_color.rgb, vec3(0.299, 0.587, 0.114));
	float warmth = sample_color.r - max(sample_color.g * 0.88,
		sample_color.b);
	float pearl_or_gold = smoothstep(0.025, 0.145, warmth)
		* smoothstep(0.44, 0.76, luma);
	return pearl_or_gold * frame_region(uv) * sample_color.a;
}

vec3 rainbow(float hue) {
	return 0.56 + 0.44 * cos(6.2831853
		* (hue + vec3(0.00, 0.67, 0.33)));
}

void fragment() {
	vec4 vertex_color = COLOR;
	float opening = opening_region(UV);
	float drift = 0.5 + 0.5 * sin(UV.y * 24.0 + motion_time * 0.72
		+ sin(UV.x * 15.0 - motion_time * 0.31) * 1.7);
	float cross_drift = 0.5 + 0.5 * cos(UV.x * 18.0
		- motion_time * 0.46 + UV.y * 5.0);
	vec3 fog_color = mix(vec3(0.105, 0.075, 0.23),
		vec3(0.39, 0.35, 0.61), drift * 0.42 + cross_drift * 0.18);
	vec4 fog_result = vec4(fog_color, opening * (0.28 + drift * 0.17 + feedback_strength * 0.10)
		* vertex_color.a);
	vec4 source = texture(TEXTURE, UV);
	float core = painted_frame_mask(source, UV);
	vec2 spread = TEXTURE_PIXEL_SIZE * 5.0;
	float halo = core;
	halo = max(halo, painted_frame_mask(texture(TEXTURE,
		UV + vec2(spread.x, 0.0)), UV + vec2(spread.x, 0.0)) * 0.34);
	halo = max(halo, painted_frame_mask(texture(TEXTURE,
		UV - vec2(spread.x, 0.0)), UV - vec2(spread.x, 0.0)) * 0.34);
	halo = max(halo, painted_frame_mask(texture(TEXTURE,
		UV + vec2(0.0, spread.y)), UV + vec2(0.0, spread.y)) * 0.34);
	halo = max(halo, painted_frame_mask(texture(TEXTURE,
		UV - vec2(0.0, spread.y)), UV - vec2(0.0, spread.y)) * 0.34);

	float red_pulse = 0.72 + 0.28 * sin(motion_time * 1.427997);
	vec3 bonus_color = vec3(1.0, 0.025, 0.075) * (0.86 + red_pulse * 0.25);
	float sweep_position = fract(motion_time / shimmer_period);
	float sweep_axis = fract(UV.y * 0.84 + UV.x * 0.28);
	float sweep_distance = abs(fract(sweep_axis - sweep_position + 0.5) - 0.5);
	float sheen = 1.0 - smoothstep(0.025, 0.115, sweep_distance);
	vec3 spectral = rainbow(fract(UV.y * 0.74 + UV.x * 0.46
		- motion_time * 0.11));
	vec3 plot_color = mix(vec3(1.0, 0.60, 0.065), spectral,
		sheen * 0.82) * (0.98 + sheen * 0.32);
	vec3 cue_color = mix(bonus_color, plot_color,
		step(0.5, cue_mode));
	float plot_pulse = 0.84 + 0.16 * sin(motion_time * 1.963495);
	float state_pulse = mix(red_pulse, plot_pulse, step(0.5, cue_mode));
	float core_strength = mix(0.64, 0.68 + sheen * 0.24,
		step(0.5, cue_mode));
	float final_alpha = max(core * core_strength, halo * 0.22)
		* (cue_alpha + feedback_strength * 0.10) * state_pulse * vertex_color.a;
	float plot_gate = step(0.5, cue_mode);
	float plot_interior_alpha = opening * plot_gate
		* (0.085 + plot_pulse * 0.035) * vertex_color.a;
	float combined_alpha = max(final_alpha, plot_interior_alpha);
	vec3 combined_color = mix(vec3(1.0, 0.60, 0.09), cue_color,
		final_alpha / max(0.0001, final_alpha + plot_interior_alpha));
	vec4 highlight_result = vec4(combined_color, combined_alpha);
	COLOR = mix(highlight_result, fog_result, step(1.5, cue_mode));
}
