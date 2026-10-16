"""Evidence rules for a source-owned transient flash; no device or visual acceptance."""
import math

def validate_trial(t):
 a=t['onset'];b=t['decay'];p=t['native_point']
 if not t['actual_input']or t['visual_override']or not t['source_controller_unchanged']or not t['freed']:raise ValueError('source/lifetime boundary')
 if a['class']!='Panel'or a['size']!=[110.0,110.0]or a['corner_radius']!=55:raise ValueError('not source flash geometry')
 if len(a['rgba'])!=4 or any(abs(x-y)>1e-6 for x,y in zip(a['rgba'],[1.0,.95,.5,.5])):raise ValueError('not source flash material')
 rect=a['native_rect'];center=[rect[0]+rect[2]*.5,rect[1]+rect[3]*.5]
 if math.dist(center,p)>.001:raise ValueError('flash not at actual input')
 if not 0<b['modulate_alpha']<a['modulate_alpha']<=1:raise ValueError('natural fade not observed')
 if a['instance_id']!=t['instance_id']or b['instance_id']!=t['instance_id']:raise ValueError('instance identity mismatch')
 return True

def validate_lane(mode,lane):
 if mode!='ORIGINAL_SOURCE'or lane not in {'BOUNDED_CURRENT_ORIGINAL_TOUCH_FLASH','EXCLUDED_BOOTSTRAP_CONTROL'}:raise ValueError('not original source context')
