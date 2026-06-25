// hair_rainbow.gdshader — rainbow streaks for Roshan's hair.
//
// Each hair strand carries its strand index in vertex-colour RED (0..1), baked in
// Blender per the tools/build_roshan_base.py contract. This shader maps that index
// to a hue around the colour wheel, so 10-15 strands fan across a full rainbow, and
// slowly cycles the whole set over time. Motion is handled separately by the spring
// physics in scripts/hair.gd (this only does colour + a little underwater shading).
shader_type spatial;
render_mode cull_disabled;

uniform float saturation : hint_range(0.0, 1.0) = 0.85;
uniform float value : hint_range(0.0, 1.0) = 1.0;
uniform float cycle_speed = 0.04;     // hue drift per second (0 = static rainbow)
uniform float band_sharpness = 1.0;   // 1 = smooth gradient across strands
uniform float emission_amt = 0.35;    // gentle glow so streaks read underwater
uniform sampler2D caustic : source_color;

vec3 hsv2rgb(vec3 c) {
	vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
	vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
	return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
}

void fragment() {
	// strand index (0..1) -> hue, plus a slow global drift
	float idx = COLOR.r;
	float hue = fract(idx * band_sharpness + TIME * cycle_speed);
	vec3 rgb = hsv2rgb(vec3(hue, saturation, value));
	ALBEDO = rgb;
	EMISSION = rgb * emission_amt;
	// subtle caustic shimmer so hair sits in the same light as the reef
	vec3 wp = (INV_VIEW_MATRIX * vec4(VERTEX, 1.0)).xyz;
	float c = texture(caustic, wp.xz * 0.02 + vec2(TIME * 0.01, -TIME * 0.007)).r;
	EMISSION += smoothstep(0.5, 0.95, c) * rgb * 0.25;
	ROUGHNESS = 0.65;
	RIM = 0.5;
}
