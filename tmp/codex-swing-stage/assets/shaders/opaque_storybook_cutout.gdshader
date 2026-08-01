shader_type spatial;
render_mode unshaded, cull_disabled, depth_draw_opaque, shadows_disabled;

uniform sampler2D albedo_texture : source_color, filter_linear;
uniform vec4 tint : source_color = vec4(1.0);
uniform float alpha_threshold : hint_range(0.0, 1.0, 0.01) = 0.24;

void fragment() {
	vec4 painted = texture(albedo_texture, UV) * tint;
	if (painted.a < alpha_threshold) {
		discard;
	}
	// Generated storybook cutouts contain soft alpha inside their painted
	// silhouettes. Once a pixel passes the silhouette threshold it must be an
	// opaque piece of playground equipment, not a translucent overlay.
	ALBEDO = painted.rgb;
}
