// outline.gdshader — inverted-hull ink outline (Godot 4.4, Mobile-safe).
//
// The classic toon outline: render back-faces only, grown along the normal, in a
// flat colour. Attach as a material's `next_pass` so it draws around the mesh.
// This is the reliable per-object outline approach (works in the Mobile renderer).
shader_type spatial;
render_mode cull_front, unshaded, shadows_disabled;

uniform float width : hint_range(0.0, 0.2) = 0.025;   // in local units * model scale
uniform vec4 line_color : source_color = vec4(0.02, 0.03, 0.05, 1.0);

void vertex() {
	// push each back-face vertex outward along its normal -> a shell behind the mesh
	VERTEX += normalize(NORMAL) * width;
}

void fragment() {
	ALBEDO = line_color.rgb;
	// NO ALPHA write: any ALPHA assignment moves the shell into the transparent
	// pass (per-frame depth sorting + no early-Z for every outlined prop). The
	// old fade_with_depth branch wrote a constant 1.0 alpha, paying that cost
	// for zero visual difference (lighting audit 2026-07-18).
}
