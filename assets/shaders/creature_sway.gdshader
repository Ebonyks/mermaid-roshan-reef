// creature_sway.gdshader — GEN2 swimming creature (Mobile-safe).
//
// The family-style Meshy animals are statics: this is their SWIM. Godot mesh
// space is Y-up with the body length along Z (head +Z after the glTF axis
// conversion — the first version wrongly bent by height). Four species modes,
// and an `excite` uniform the greeting system ramps when Roshan swims close.
shader_type spatial;
render_mode cull_back, diffuse_toon, specular_toon;

uniform sampler2D albedo_tex : source_color, hint_default_white;
uniform vec4 tint : source_color = vec4(1.0);
uniform int sway_mode = 0;          // 0 tail-wave, 1 wing undulation, 2 jelly pulse, 3 waddle rock
uniform float sway_speed = 4.2;
uniform float sway_amount = 0.09;   // in model units (Meshy bodies are ~1.1 long)
uniform float phase = 0.0;
uniform float excite = 0.0;         // 0..1 greeting boost (faster + bigger)
// craft-studio repaint. Two modes:
//  * luma mode (no zone_mask): light zones take the fin colour — the fish.
//  * zone mode (zone_mask bound, use_zones=1): mask R/G/B = body / accent /
//    third-colour regions baked from geometry (tools/bake_zone_mask.py), so
//    the coloration matches the book art (white kitty muzzle, pink wings...).
//    Black mask = fixed features (horn, feet, beak) keep the baked texture.
uniform float paint_mix = 0.0;
uniform float paint_contrast = 1.0;
uniform vec4 paint_body : source_color = vec4(1.0);
uniform vec4 paint_fin : source_color = vec4(1.0);
uniform vec4 paint_third : source_color = vec4(1.0);
uniform int use_zones = 0;
uniform sampler2D zone_mask : hint_default_black;

void vertex() {
	float sp = sway_speed * (1.0 + excite * 1.6);
	float am = sway_amount * (1.0 + excite * 0.8);
	// tail weight: head (+Z) steady, tail (-Z) swings
	float t = clamp(-VERTEX.z / 0.55 * 0.5 + 0.5, 0.0, 1.0);
	if (sway_mode == 0) {
		VERTEX.x += sin(TIME * sp + phase + VERTEX.z * 2.4) * am * t * t;
	} else if (sway_mode == 1) {
		VERTEX.y += sin(TIME * sp + phase + VERTEX.z * 2.0) * am * t;
		VERTEX.y += sin(TIME * sp * 0.7 + phase + VERTEX.x * 2.6) * am * 0.6;
	} else if (sway_mode == 2) {
		VERTEX *= 1.0 + sin(TIME * sp + phase) * am * 0.6;
	} else {
		VERTEX.x += sin(TIME * sp + phase) * am * VERTEX.y * 0.9;
	}
}

void fragment() {
	vec3 alb = texture(albedo_tex, UV).rgb;
	if (paint_mix > 0.001) {
		float luma = dot(alb, vec3(0.35, 0.5, 0.15));
		vec3 paint;
		float zone_w = 1.0;
		if (use_zones == 1) {
			vec3 zw = texture(zone_mask, UV).rgb;
			zone_w = clamp(zw.r + zw.g + zw.b, 0.0, 1.0);
			paint = (zw.r * paint_body.rgb + zw.g * paint_fin.rgb + zw.b * paint_third.rgb)
				/ max(zone_w, 0.001);
		} else {
			paint = mix(paint_body.rgb, paint_fin.rgb, smoothstep(0.55, 0.8, luma));
		}
		// near-black texels are FEATURES (eyes, nose, mouth, stitches) — keep
		// them, or every painted friend comes out eyeless (playtest 2026-07-13)
		float dark = 1.0 - smoothstep(0.06, 0.22, luma);
		alb = mix(mix(alb, paint * (0.55 + luma * 0.9), paint_mix * zone_w), alb, dark);
	}
	alb = clamp((alb - vec3(0.5)) * paint_contrast + vec3(0.5), vec3(0.0), vec3(1.0));
	ALBEDO = alb * tint.rgb;
	ROUGHNESS = 1.0;
	SPECULAR = 0.0;
}
