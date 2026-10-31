"""Bounded exported-landmark feedback; always re-render from native pixels."""
import json,sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
from prepare import P,fit
plan=json.loads((P/'registration_plan.json').read_text())
verified=json.loads((P/'verification.json').read_text())
(P/'initial_verification.json').write_text(json.dumps(verified,indent=2)+'\n',encoding='utf-8')
for i in verified['registration_failures']:
    row=plan['frames'][i];observed=verified['frames'][i]['observed_landmarks']
    assert 'raster_feedback' not in row,'One bounded feedback update only'
    correction=fit(observed,row['target_landmarks'])
    old_s=row['uniform_scale'];old_t=np.array(row['translation'])
    row['raster_feedback']={'attempt':1,'initial_uniform_scale':old_s,'initial_translation':old_t.tolist(),
                            'exported_observation':observed,'correction':correction,
                            'render_source':'Original native frame, never first resample pixels'}
    row['uniform_scale']=old_s*correction['uniform_scale']
    row['translation']=(old_t*correction['uniform_scale']+correction['translation']).tolist()
    mapped=np.array(row['source_foreground_bounds']).reshape(2,2)*row['uniform_scale']+row['translation']
    assert np.all(mapped[0]>=0) and np.all(mapped[1]<=[575,831]),'Feedback introduces clipping'
    row['mapped_foreground_bounds']=mapped.tolist()
(P/'registration_plan.json').write_text(json.dumps(plan,indent=2)+'\n',encoding='utf-8')
print('One native re-render feedback for',verified['registration_failures'])
