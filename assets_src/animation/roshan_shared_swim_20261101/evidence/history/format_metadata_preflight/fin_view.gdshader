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

vec3 source_colour(sampler2D art, sampler2D nearest, vec2 uv) {
    // Keep authored pigment coordinates fixed. Gradient-based UV projection
    // folds at the medial axis and repeats painted veins during the turn.
    vec4 authored = texture(art,uv);
    vec2 valid_uv = texture(nearest,uv).rg;
    return authored.a > 0.5 ? authored.rgb : texture(art,valid_uv).rgb;
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
        vec3 colour = source_colour(broad_image,broad_nearest,UV)*weights.x
                    +source_colour(edge_image,edge_nearest,UV)*weights.y
                    +source_colour(cup_image,cup_nearest,UV)*weights.z;
        // A narrow shared contour follows the interpolated silhouette. It is
        // not a second fin or a cross-faded full-character layer.
        colour *= mix(0.65,1.0,smoothstep(0.0,1.5,-distance_value));
        COLOR = vec4(colour,alpha);
    }
}
