shader_type canvas_item;

uniform sampler2D broad_image : source_color, filter_linear;
uniform sampler2D edge_image : source_color, filter_linear;
uniform sampler2D cup_image : source_color, filter_linear;
uniform sampler2D broad_distance : filter_linear;
uniform sampler2D edge_distance : filter_linear;
uniform sampler2D cup_distance : filter_linear;
uniform sampler2D broad_nearest : filter_nearest;
uniform sampler2D edge_nearest : filter_nearest;
uniform sampler2D cup_nearest : filter_nearest;
uniform float turn_weight = 0.0;
uniform float cup_weight = 0.0;

vec3 projected_colour(sampler2D art, sampler2D distances, sampler2D nearest,
                     vec2 uv, float current_distance, float own_distance) {
    vec2 step_size = vec2(1.0/512.0);
    vec2 gradient = vec2(
        texture(distances, uv+vec2(step_size.x,0.0)).r-texture(distances, uv-vec2(step_size.x,0.0)).r,
        texture(distances, uv+vec2(0.0,step_size.y)).r-texture(distances, uv-vec2(0.0,step_size.y)).r);
    gradient /= max(length(gradient),0.0001);
    vec2 source_uv = clamp(uv-gradient*(own_distance-current_distance)/512.0,vec2(0.0),vec2(1.0));
    vec2 valid_uv = texture(nearest,source_uv).rg;
    return texture(art,valid_uv).rgb;
}

void fragment() {
    vec3 weights = vec3((1.0-turn_weight)*(1.0-cup_weight),turn_weight*(1.0-cup_weight),cup_weight);
    if (weights.x > 0.9999) {
        COLOR = texture(broad_image,UV);
    } else if (weights.y > 0.9999) {
        COLOR = texture(edge_image,UV);
    } else if (weights.z > 0.9999) {
        COLOR = texture(cup_image,UV);
    } else {
        vec3 distances = vec3(texture(broad_distance,UV).r,texture(edge_distance,UV).r,texture(cup_distance,UV).r);
        float distance_value = dot(weights,distances);
        float alpha = 1.0-smoothstep(-0.65,0.65,distance_value);
        vec3 colour = projected_colour(broad_image,broad_distance,broad_nearest,UV,distance_value,distances.x)*weights.x
                    +projected_colour(edge_image,edge_distance,edge_nearest,UV,distance_value,distances.y)*weights.y
                    +projected_colour(cup_image,cup_distance,cup_nearest,UV,distance_value,distances.z)*weights.z;
        COLOR = vec4(colour,alpha);
    }
}
