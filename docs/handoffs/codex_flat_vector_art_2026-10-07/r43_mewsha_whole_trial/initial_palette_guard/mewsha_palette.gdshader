shader_type canvas_item;
render_mode unshaded;
uniform vec4 body_choice : source_color = vec4(0.95,0.70,0.85,1.0);
uniform vec4 horn_choice : source_color = vec4(0.60,0.40,0.90,1.0);
uniform vec4 heart_choice : source_color = vec4(0.97,0.96,0.93,1.0);
uniform vec4 body_anchor : source_color = vec4(0.95,0.70,0.85,1.0);
uniform vec4 horn_anchor : source_color = vec4(0.60,0.40,0.90,1.0);
uniform vec4 heart_anchor : source_color = vec4(0.65,0.50,0.86,1.0);
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

float ellipse(vec2 p, vec2 center, vec2 radii) {
 return 1.0-smoothstep(0.90,1.0,length((p-center)/radii));
}
vec3 choose_painted(vec3 original,vec3 wanted,vec3 base) {
 vec3 s=rgb_hsv(original); vec3 w=rgb_hsv(wanted);vec3 b=rgb_hsv(base);
 float saturation=clamp(s.y*w.y/max(b.y,0.1),0.0,1.0);
 float value=clamp(s.z*w.z/max(b.z,0.1),0.0,1.0);
 return hsv_rgb(vec3(fract(s.x+w.x-b.x),saturation,value));
}
void fragment() {
 vec4 original=texture(TEXTURE,UV);
 float luma=dot(original.rgb,vec3(0.2126,0.7152,0.0722));
 float protected_ink=1.0-smoothstep(0.14,0.26,luma);
 float protected_eye=max(ellipse(UV,vec2(0.365,0.465),vec2(0.13,0.14)),ellipse(UV,vec2(0.60,0.425),vec2(0.14,0.14)));
 bool purple=original.b>original.r*1.025 && original.b>original.g*1.025;
 bool horn=purple && UV.x>=0.20 && UV.x<=0.50 && UV.y>=0.075 && UV.y<=0.32;
 bool heart=purple && UV.x>=0.42 && UV.x<=0.69 && UV.y>=0.675 && UV.y<=0.85;
 vec3 wanted=body_choice.rgb;vec3 base=body_anchor.rgb;
 if(horn){wanted=horn_choice.rgb;base=horn_anchor.rgb;}
 if(heart){wanted=heart_choice.rgb;base=heart_anchor.rgb;}
 vec3 painted=choose_painted(original.rgb,wanted,base);
 painted=mix(painted,original.rgb,clamp(max(protected_ink,protected_eye),0.0,1.0));
 COLOR=vec4(painted,original.a);
}
