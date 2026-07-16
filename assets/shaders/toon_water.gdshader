// toon_water.gdshader — Phase 5 storybook water for rivers, ponds and the sea.
//
// Base: "Toon Water" from godotshaders.com/shader/toon-water/ (CC0), which
// contributes the depth-difference shoreline technique (scene depth vs the
// water fragment's own depth -> foam right where water meets the banks).
// Adapted here: pastel two-tone depth fade, sparkle dots from the caustics
// map, scrolling ripple normal maps, and a use_depth switch so the Speedy
// quality tier (and the mobile renderer at its lowest setting) runs with
// zero depth-texture reads. No SCREEN_TEXTURE anywhere — no forced copy on
// the mobile renderer.
shader_type spatial;
render_mode cull_disabled;

uniform vec3 deep_color : source_color = vec3(0.14, 0.46, 0.66);
uniform vec3 shallow_color : source_color = vec3(0.42, 0.78, 0.86);
uniform vec3 foam_color : source_color = vec3(0.97, 1.0, 1.0);
uniform float foam_width : hint_range(0.1, 8.0) = 2.2;   // world units of shoreline foam
uniform float depth_fade : hint_range(0.5, 30.0) = 9.0;  // shallow->deep tint distance
uniform float alpha_base : hint_range(0.0, 1.0) = 0.78;
uniform float wobble_speed = 1.1;
uniform float wobble_height = 0.45;
uniform float scroll_speed = 0.05;
uniform float ripple_scale = 0.05;
uniform float sparkle = 0.35;                             // 0 disables the dot pass
uniform bool use_depth = true;                            // Speedy tier flips this off
uniform bool mesh_edge_foam = false;                      // cheap shoreline fallback for authored ribbons/rings
uniform float mesh_edge_width : hint_range(0.01, 0.35) = 0.10;
uniform sampler2D ripple : hint_normal, repeat_enable;
uniform sampler2D caustics : repeat_enable;
uniform sampler2D depth_texture : hint_depth_texture;
// GEN2: painted water albedo (family-style texture) blended over the two-tone
// gradient. albedo_mix 0 = legacy look, so every existing sheet is unchanged.
uniform sampler2D albedo_tex : source_color, repeat_enable, filter_linear_mipmap;
uniform float albedo_mix : hint_range(0.0, 1.0) = 0.0;
uniform float albedo_scale = 0.02;   // world-units -> UV tiling for albedo_tex

varying vec2 wxz;

void vertex() {
	vec3 wp = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
	VERTEX.y += sin(TIME * wobble_speed + wp.x * 0.11 + wp.z * 0.07) * wobble_height;
	wxz = wp.xz;
}

void fragment() {
	// scrolling normals: two ripple layers drifting against each other
	vec2 uv1 = wxz * ripple_scale + vec2(TIME * scroll_speed, TIME * scroll_speed * 0.6);
	vec2 uv2 = wxz * ripple_scale * 1.7 - vec2(TIME * scroll_speed * 0.8, -TIME * scroll_speed * 0.5);
	NORMAL_MAP = mix(texture(ripple, uv1).rgb, texture(ripple, uv2).rgb, 0.5);
	NORMAL_MAP_DEPTH = 0.7;
	float shore = 0.0;
	float shallow = 0.45;
	if (use_depth) {
		// depth-difference shoreline (from the CC0 Toon Water base)
		float depth_raw = texture(depth_texture, SCREEN_UV).x;
		vec3 ndc = vec3(SCREEN_UV * 2.0 - 1.0, depth_raw);
		vec4 view = INV_PROJECTION_MATRIX * vec4(ndc, 1.0);
		view.xyz /= view.w;
		vec3 ondc = vec3(SCREEN_UV * 2.0 - 1.0, FRAGCOORD.z);
		vec4 oview = INV_PROJECTION_MATRIX * vec4(ondc, 1.0);
		oview.xyz /= oview.w;
		float diff = (-view.z) - (-oview.z);
		shore = 1.0 - smoothstep(0.0, foam_width, diff);
		shallow = 1.0 - smoothstep(0.0, depth_fade, diff);
	}
	if (mesh_edge_foam) {
		// River and moat meshes author UV.x from bank to bank. This keeps both
		// shores obvious on Speedy, where scene-depth reads are intentionally off.
		float edge_dist = min(UV.x, 1.0 - UV.x);
		shore = max(shore, 1.0 - smoothstep(0.0, mesh_edge_width, edge_dist));
	}
	// storybook sparkle dots, same trick as the reef surface (caustics green)
	float sp = texture(caustics, uv1 * 2.3).g * texture(caustics, uv2 * 2.1).g;
	float dots = step(0.34, sp) * sparkle;
	vec3 base = mix(deep_color, shallow_color, shallow);
	if (albedo_mix > 0.001) {
		// drift the painted water slowly so it reads alive even on Speedy
		vec3 paint = texture(albedo_tex, wxz * albedo_scale + vec2(TIME * scroll_speed * 0.3)).rgb;
		base = mix(base, paint, albedo_mix);
	}
	base = mix(base, foam_color, clamp(shore + dots, 0.0, 1.0));
	ALBEDO = base;
	EMISSION = base * 0.22 + foam_color * shore * 0.18;
	ROUGHNESS = 0.12;
	METALLIC = 0.2;
	ALPHA = clamp(alpha_base + shore * 0.18, 0.0, 1.0);
}
