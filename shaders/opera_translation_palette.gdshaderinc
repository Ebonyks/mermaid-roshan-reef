const float OPERA_SATURATION = 0.940000;
const vec3 OPERA_GAIN = vec3(0.965000, 0.955000, 0.970000);

vec3 opera_palette(vec3 painted) {
	float value = dot(painted, vec3(0.2126, 0.7152, 0.0722));
	return clamp(mix(vec3(value), painted, OPERA_SATURATION) * OPERA_GAIN, vec3(0.0), vec3(1.0));
}
