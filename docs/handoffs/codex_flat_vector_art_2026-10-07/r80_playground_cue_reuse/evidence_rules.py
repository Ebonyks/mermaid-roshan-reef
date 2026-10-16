"""Fail closed on source/prototype lane confusion or a non-clickable/recolored reuse card."""
import math
SOURCE='ORIGINAL_SOURCE';CANDIDATE='LOCAL_NONRUNTIME_STAR_REUSE';ASSET='res://assets/mg/star.png'
def validate_lane(mode,lane):
 if mode==SOURCE:
  if lane not in {'BOUNDED_CURRENT_ORIGINAL_CUE_INPUT','EXCLUDED_BOOTSTRAP_CONTROL'}:raise ValueError('wrong source lane')
 elif mode==CANDIDATE:
  if lane!='EXCLUDED_NONRUNTIME_PAINTED_CUE_PROTOTYPE':raise ValueError('prototype cannot count as source')
 else:raise ValueError('unknown mode')
def validate_card(row):
 if row['texture_path']!=ASSET or row['source_dimensions']!=[1024.0,1008.0]:raise ValueError('wrong source bitmap')
 if row['rgba'][:3]!=[1.0,1.0,1.0]or not 0<=row['rgba'][3]<=1:raise ValueError('source RGB changed')
 if not row['original_cue_texture_null']or row['original_pointer_child_count']!=0:raise ValueError('flat cue residue')
 radius={'slide':118.0,'swing':110.0,'seesaw':110.0}.get(row['consumer'])
 if radius is None or row['native_hit_radius']!=radius:raise ValueError('wrong consumer radius')
 corners=row['native_corners'];center=row['equipment_hit_center']
 if len(corners)!=4 or any(math.dist(p,center)>radius+.0001 for p in corners):raise ValueError('card outside original hit disk')
 width=math.dist(corners[0],corners[1]);height=math.dist(corners[1],corners[2])
 if height<=0 or abs(width/height-1024/1008)>.0001:raise ValueError('source aspect changed')
 if row['production_integration']or not row['visual_override_only']:raise ValueError('prototype accepted as production')
 return True