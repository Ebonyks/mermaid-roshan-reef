shader_type canvas_item;
render_mode unshaded;
uniform sampler2D palette_selector : filter_linear, repeat_disable;
uniform vec4 body_choice : source_color = vec4(0.4,0.7,1.0,1.0);
uniform vec4 fin_choice : source_color = vec4(1.0,0.6,0.2,1.0);
uniform bool body_rainbow = false;
uniform bool fin_rainbow = false;
vec3 rgb_hsv(vec3 c) {
	vec4 K = vec4(0.0,-1.0/3.0,2.0/3.0,-1.0);
	vec4 p = mix(vec4(c.bg,K.wz),vec4(c.gb,K.xy),step(c.b,c.g));
	vec4 q = mix(vec4(p.xyw,c.r),vec4(c.r,p.yzx),step(p.x,c.r));
	float d=q.x-min(q.w,q.y);
	return vec3(abs(q.z+(q.w-q.y)/(6.0*d+0.000001)),d/(q.x+0.000001),q.x);
}
vec3 hsv_rgb(vec3 c) {
	vec3 p=abs(fract(c.xxx+vec3(0.0,2.0/3.0,1.0/3.0))*6.0-3.0);
	return c.z*mix(vec3(1.0),clamp(p-1.0,0.0,1.0),c.y);
}
vec3 painted_choice(vec3 source_rgb,vec3 chosen,bool rainbow,float shine) {
	vec3 source_hsv=rgb_hsv(source_rgb);
	vec3 wanted=rgb_hsv(chosen);
	if (rainbow) { wanted.x=fract(TIME/2.4); }
	vec3 out_rgb=hsv_rgb(vec3(wanted.x,source_hsv.y,source_hsv.z));
	vec3 weights=vec3(0.2126,0.7152,0.0722);
	float source_luma=clamp(dot(source_rgb,weights)*shine,0.0,0.97);
	float out_luma=dot(out_rgb,weights);
	if (out_luma<source_luma) {
		out_rgb=mix(out_rgb,vec3(1.0),clamp((source_luma-out_luma)/max(1.0-out_luma,0.0001),0.0,1.0));
	} else {
		out_rgb*=source_luma/max(out_luma,0.0001);
	}
	return clamp(out_rgb,vec3(0.0),vec3(1.0));
}
void fragment() {
	vec4 original=texture(TEXTURE,UV);
	vec3 selector=texture(palette_selector,UV).rgb;
	float ink=1.0-smoothstep(0.14,0.26,dot(original.rgb,vec3(0.2126,0.7152,0.0722)));
	float protected_identity=max(selector.b,ink);
	float fin_weight=selector.r;
	float shimmer=1.0+0.06*(1.0+sin(TIME*8.975979));
	vec3 body=painted_choice(original.rgb,body_choice.rgb,body_rainbow,1.0);
	vec3 fins=painted_choice(original.rgb,fin_choice.rgb,fin_rainbow,shimmer);
	vec3 painted=mix(body,fins,fin_weight);
	painted=mix(painted,original.rgb,clamp(protected_identity,0.0,1.0));
	COLOR=vec4(painted,original.a);
}
