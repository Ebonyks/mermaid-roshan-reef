shader_type canvas_item;
render_mode unshaded;
#include "res://shaders/opera_translation_palette.gdshaderinc"
varying vec4 vertex_tint;
uniform vec2 source_offset = vec2(0.0);
uniform vec2 source_span = vec2(256.0, 288.0);
uniform float phase = 0.0;
uniform bool motion_enabled = true;
uniform bool apply_palette = true;
uniform vec2 selected_door = vec2(-100.0,-1.0);
uniform float door_open = 0.0;
uniform float tea_reaction = 0.0;
uniform float bell_reaction = 0.0;

void vertex() {
	vertex_tint = COLOR;
}

float inside(vec2 p, vec2 low, vec2 high) {
	vec2 a = smoothstep(low, low + vec2(2.0), p);
	vec2 b = vec2(1.0) - smoothstep(high - vec2(2.0), high, p);
	return a.x*a.y*b.x*b.y;
}

void fragment() {
	vec2 p = source_offset + UV * source_span;
	vec2 sample_uv = UV;
	float fabric = 0.0;
	if(p.x>330.0 && p.x<700.0 && p.y>78.0 && p.y<400.0){
		float x=357.0;
		if(p.x>408.0){x=459.0;}
		if(p.x>512.0){x=565.0;}
		if(p.x>616.0){x=667.0;}
		float low_y=81.0;
		float high_y=130.0;
		if(p.y>160.0){low_y=205.0;high_y=252.0;}
		if(p.y>290.0){low_y=341.0;high_y=397.0;}
		fabric=inside(p,vec2(x-20.0,low_y),vec2(x+20.0,high_y));
	}
	if (motion_enabled) {
		if(p.y>42.0 && p.y<86.0){
			float hanging=inside(p,vec2(232.0,43.0),vec2(283.0,85.0))
				+inside(p,vec2(743.0,43.0),vec2(792.0,85.0));
			sample_uv.x += sin(phase*0.7)*0.65/source_span.x*hanging*smoothstep(43.0,82.0,p.y);
		}
		if(p.x>474.0 && p.x<532.0 && p.y>426.0 && p.y<464.0){
			float leaves=inside(p,vec2(474.0,426.0),vec2(532.0,464.0));
			vec4 rest_pixel=texture(TEXTURE,UV);
			float green=smoothstep(0.025,0.13,rest_pixel.g-rest_pixel.r);
			// Vertical leaf deformation stays continuous across the central card join.
			sample_uv.y += sin(phase*0.75+(p.y-426.0)*0.035)*1.4/source_span.y*leaves*green;
		}
	}
	vec4 pixel = texture(TEXTURE, sample_uv);
	if (apply_palette) {
		pixel.rgb = opera_palette(pixel.rgb);
	}
	float candle = 0.0;
	if(p.x>296.0 && p.x<726.0 && p.y>90.0 && p.y<376.0){
		float x=303.0+clamp(floor((p.x-303.0)/104.0+0.5),0.0,4.0)*104.0;
		float low_y=92.0;
		float high_y=113.0;
		if(p.y>160.0){low_y=220.0;high_y=242.0;}
		if(p.y>290.0){low_y=350.0;high_y=374.0;}
		candle=inside(p,vec2(x-5.0,low_y),vec2(x+5.0,high_y));
	}
	float crystals = inside(p, vec2(232.0,42.0),vec2(283.0,85.0))
		+ inside(p, vec2(743.0,42.0),vec2(792.0,85.0));
	float brightness = smoothstep(0.55,0.9,dot(pixel.rgb,vec3(0.299,0.587,0.114)));
	if (motion_enabled) {
		pixel.rgb += vec3(1.0,0.70,0.30)*(0.04+0.04*sin(phase*1.7+p.x))*candle;
		pixel.rgb += vec3(1.0,0.92,0.66)*0.065*(0.5+0.5*sin(phase*0.9+p.x*0.7+p.y*0.4))*crystals*brightness;
	}
	// The fabric is drawn exactly once by independent original-pixel cards.
	// This dark backing becomes visible only when those two panels part.
	pixel.rgb=mix(pixel.rgb,vec3(0.27,0.12,0.17),clamp(fabric,0.0,1.0));
	float tea=inside(p,vec2(925.0,432.0),vec2(975.0,477.0));
	pixel.rgb += vec3(0.08,0.06,0.02)*tea*tea_reaction*(0.5+0.5*sin(phase*8.0));
	float bell=inside(p,vec2(233.0,358.0),vec2(269.0,398.0));
	pixel.rgb += vec3(0.12,0.08,0.02)*bell*bell_reaction*(0.5+0.5*sin(phase*10.0));
	// Fragment COLOR already contains the texture. Preserve vertex tint separately
	// so the painted image is sampled/multiplied exactly once.
	COLOR = pixel * vertex_tint;
}
