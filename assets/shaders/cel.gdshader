// cel.gdshader — Wind-Waker-style toon shading for 3D meshes (Godot 4.4, Mobile-safe).
//
// Hard-banded diffuse (1-2 tones) + a soft Fresnel rim, keeping each mesh's own
// albedo/texture. Pair with outline.gdshader as a `next_pass` for the ink line.
// Apply via material_override or surface override; see CEL_SHADING.md.
shader_type spatial;
render_mode cull_back, diffuse_toon, specular_toon;

uniform sampler2D albedo_tex : source_color, hint_default_white;
uniform vec4 tint : source_color = vec4(1.0);
uniform int bands : hint_range(1, 4) = 2;     // number of light steps
uniform float rim_strength : hint_range(0.0, 2.0) = 0.15;
uniform vec4 rim_color : source_color = vec4(1.0);
uniform float rim_width : hint_range(0.0, 1.0) = 0.35;

void fragment() {
	vec4 t = texture(albedo_tex, UV);
	ALBEDO = t.rgb * tint.rgb;
	// no ALPHA write: assigning ALPHA would move every mesh into the transparent
	// pass (z-sort artifacts on opaque props); gen2 props are solid meshes
	ROUGHNESS = 0.9;
	SPECULAR = 0.0;   // no toon specular blob — another white hotspot on pastels
	// soft rim light so silhouettes glow underwater (added in fragment, view-based)
	float f = pow(1.0 - clamp(dot(normalize(NORMAL), normalize(VIEW)), 0.0, 1.0), 3.0);
	EMISSION += rim_color.rgb * smoothstep(1.0 - rim_width, 1.0, f) * rim_strength;
}

void light() {
	// posterize N·L into hard bands -> the cel "two-tone" read.
	// NO per-light brightness floor: a floor stacks additively across every
	// light in range (the reef is full of glow orbs), which blew the colors
	// out (playtest 2026-07-11). Ambient lifts the shadow side instead.
	float ndl = clamp(dot(normalize(NORMAL), normalize(LIGHT)), 0.0, 1.0);
	float stepped = floor(ndl * float(bands) + 0.5) / float(bands);
	DIFFUSE_LIGHT += ALBEDO * LIGHT_COLOR * ATTENUATION * stepped;
}
