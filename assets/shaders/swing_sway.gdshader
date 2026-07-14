// swing_sway.gdshader — empty swing seats rocking in the breeze (Mobile-safe).
//
// The GEN2 swing is one fused Meshy sculpt (no separable seat nodes), so the
// seats pendulum at the VERTEX stage — same trick as coral_flow, but with the
// ramp inverted: a real pendulum is rooted at the TOP bar and moves most at
// the seat. Two geometric gates keep the structure rigid: only the middle
// span sways (|x| < x_max — the A-frame legs sit outside it) and only above
// y_min (the ground rails run through the middle at the base). Displacement
// grows with distance below the bar, so chain tops stay glued to the bar and
// the seats travel farthest — reads as hanging seats, not a jelly frame.
// Fragment/light are the standard cel pair (pair with outline next_pass).
shader_type spatial;
render_mode cull_back, diffuse_toon, specular_toon;

uniform sampler2D albedo_tex : source_color, hint_default_white;
uniform vec4 tint : source_color = vec4(1.0);
uniform int bands : hint_range(1, 4) = 2;
uniform float rim_strength : hint_range(0.0, 2.0) = 0.15;
uniform vec4 rim_color : source_color = vec4(1.0);
uniform float rim_width : hint_range(0.0, 1.0) = 0.35;
uniform float sway_speed = 2.1;              // rad/s of the breeze cycle
uniform float sway_angle = 0.10;             // pendulum amplitude (radians)
// local-space mesh AABB, set by _toy_anim, for the pendulum geometry gates
uniform float bar_y = 1.0;                   // top-bar height (pendulum pivot)
uniform float y_min = 0.1;                   // below this = ground rails, rigid
uniform float x_max = 0.35;                  // seat span half-width; legs outside

void vertex() {
	float arm = max(bar_y - VERTEX.y, 0.0);
	float gate = step(abs(VERTEX.x), x_max) * step(y_min, VERTEX.y);
	float ang = sin(TIME * sway_speed) * sway_angle;
	// small-angle pendulum about the bar: swing along local Z, dip along Y
	VERTEX.z += sin(ang) * arm * gate;
	VERTEX.y += (cos(ang) - 1.0) * arm * gate;
}

void fragment() {
	vec4 t = texture(albedo_tex, UV);
	ALBEDO = t.rgb * tint.rgb;
	ROUGHNESS = 0.9;
	SPECULAR = 0.0;
	float f = pow(1.0 - clamp(dot(normalize(NORMAL), normalize(VIEW)), 0.0, 1.0), 3.0);
	EMISSION += rim_color.rgb * smoothstep(1.0 - rim_width, 1.0, f) * rim_strength;
}

void light() {
	float ndl = clamp(dot(normalize(NORMAL), normalize(LIGHT)), 0.0, 1.0);
	float stepped = floor(ndl * float(bands) + 0.5) / float(bands);
	DIFFUSE_LIGHT += ALBEDO * LIGHT_COLOR * ATTENUATION * stepped;
}
