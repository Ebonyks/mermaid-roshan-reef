shader_type canvas_item;
render_mode unshaded, blend_mix;

uniform sampler2D fixture_texture : source_color, filter_linear_mipmap_anisotropic;
uniform vec4 fixture_tint : source_color = vec4(1.0);
uniform vec4 fixture_uv_rect = vec4(0.0, 0.0, 1.0, 1.0);
uniform vec3 emission_color : source_color = vec3(1.0, 0.72, 0.38);
uniform float emission_energy : hint_range(0.0, 8.0, 0.05) = 4.0;

vec2 fixture_uv(vec2 uv) {
	vec2 texel = 1.0 / vec2(textureSize(fixture_texture, 0));
	return clamp(
		uv,
		fixture_uv_rect.xy + texel * 1.5,
		fixture_uv_rect.zw - texel * 1.5
	);
}

float fixture_alpha(vec2 uv) {
	return texture(fixture_texture, fixture_uv(uv)).a;
}

void fragment() {
	vec4 fixture = texture(fixture_texture, fixture_uv(UV));
	float highlight = smoothstep(
		0.52,
		0.96,
		max(fixture.r, max(fixture.g, fixture.b))
	);
	vec2 near_step = vec2(0.018);
	vec2 far_step = vec2(0.045);
	float near_a = (
		fixture_alpha(UV + vec2(near_step.x, 0.0))
		+ fixture_alpha(UV - vec2(near_step.x, 0.0))
		+ fixture_alpha(UV + vec2(0.0, near_step.y))
		+ fixture_alpha(UV - vec2(0.0, near_step.y))
		+ fixture_alpha(UV + near_step)
		+ fixture_alpha(UV - near_step)
		+ fixture_alpha(UV + vec2(near_step.x, -near_step.y))
		+ fixture_alpha(UV + vec2(-near_step.x, near_step.y))
	) * 0.125;
	float far_a = (
		fixture_alpha(UV + vec2(far_step.x, 0.0))
		+ fixture_alpha(UV - vec2(far_step.x, 0.0))
		+ fixture_alpha(UV + vec2(0.0, far_step.y))
		+ fixture_alpha(UV - vec2(0.0, far_step.y))
		+ fixture_alpha(UV + far_step)
		+ fixture_alpha(UV - far_step)
		+ fixture_alpha(UV + vec2(far_step.x, -far_step.y))
		+ fixture_alpha(UV + vec2(-far_step.x, far_step.y))
	) * 0.125;
	float aura = clamp(
		near_a * 0.30 + far_a * 0.14,
		0.0,
		0.22
	) * (1.0 - fixture.a);
	vec3 fixture_emission = mix(
		fixture.rgb,
		emission_color,
		0.46
	) * emission_energy * mix(0.10, 1.0, highlight) * fixture.a;
	COLOR = vec4(mix(
		emission_color,
		fixture.rgb * fixture_tint.rgb,
		fixture.a
	) + fixture_emission
		+ emission_color * emission_energy * 1.20 * aura,
		max(fixture.a * fixture_tint.a, aura));
}
