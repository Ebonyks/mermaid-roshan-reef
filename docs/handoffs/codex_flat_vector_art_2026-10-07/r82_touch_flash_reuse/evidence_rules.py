"""Scope guards for original flash versus a local whole-ring material prototype."""
import math
SOURCE='ORIGINAL_SOURCE';CANDIDATE='LOCAL_NONRUNTIME_PAINTED_RING';ASSET='res://assets/opera/worlds/props/fx_telegraph_ring.png'
def validate_lane(mode,lane):
 if mode==SOURCE:
  if lane not in {'BOUNDED_CURRENT_ORIGINAL_TOUCH_FLASH','EXCLUDED_BOOTSTRAP_CONTROL'}:raise ValueError('wrong source lane')
 elif mode==CANDIDATE:
  if lane!='EXCLUDED_NONRUNTIME_PAINTED_RING_PROTOTYPE':raise ValueError('candidate cannot count as source')
 else:raise ValueError('unknown mode')
def validate_trial(t):
 a=t['onset'];b=t['decay'];blue=t['source_blueprint'];mode=t['mode']
 if mode not in {SOURCE,CANDIDATE}or not t['actual_input']or not t['source_controller_unchanged']or not t['freed']:raise ValueError('input/lifecycle boundary')
 if t['visual_override']!=(mode==CANDIDATE):raise ValueError('visual lane mismatch')
 if blue['instance_id']!=t['instance_id']or len(blue['rgba'])!=4 or blue['class']!='Panel'or blue['active_style_class']!='StyleBoxFlat'or blue['size']!=[110.0,110.0]or blue['corner_radius']!=55 or any(abs(x-y)>1e-6 for x,y in zip(blue['rgba'],[1,.95,.5,.5])):raise ValueError('original source blueprint changed')
 rect=a['native_rect'];p=t['native_point'];center=[rect[0]+rect[2]/2,rect[1]+rect[3]/2]
 if math.dist(center,p)>.001 or rect!=blue['native_rect']:raise ValueError('original placement changed')
 if not 0<b['modulate_alpha']<a['modulate_alpha']<=1 or a['instance_id']!=t['instance_id']or b['instance_id']!=t['instance_id']:raise ValueError('natural alpha/instance mismatch')
 c=a['candidate']
 if mode==SOURCE:
  if a['active_style_class']!='StyleBoxFlat'or a['rgba']!=blue['rgba']or c:raise ValueError('source not original')
 else:
  if a['active_style_class']!='StyleBoxEmpty'or not c['original_flat_style_retired']:raise ValueError('flat style residue')
  if c['texture_path']!=ASSET or c['source_dimensions']!=[512.0,512.0]or c['rect_size']!=[110.0,110.0]or c['native_rect']!=rect:raise ValueError('source bitmap/geometry mismatch')
  if c['modulate_rgba']!=[1,1,1,1]or c['self_modulate_rgba']!=[1,1,1,1]:raise ValueError('source RGB/own alpha changed')
  if not c['parent_is_original_panel']or not c['mouse_filter_ignored']or not c['whole_source_bitmap']or not c['visual_override_only']or c['production_integration']:raise ValueError('ownership/acceptance boundary')
  if abs(c['parent_panel_alpha']-a['modulate_alpha'])>1e-6:raise ValueError('separate alpha owner')
 return True
