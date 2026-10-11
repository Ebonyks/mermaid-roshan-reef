from pathlib import Path
from PIL import Image
import numpy as np,sys,json
root=Path.cwd();sys.path.insert(0,str(root/'tools'));import ltx_wave_experiment as runner
folder=root/'assets_src/animation/roshan_wave_repair_20261010/rife_midpoint_01'
pairs=[(6,3),(14,12),(10,12)]
reviews=[]
notes=[('REJECTED_MIDPOINT_HAND_CONTOUR','The large lowering span synthesizes a narrow partly closed palm, while the endpoints switch from a spread hand to rest. The intermediate thumb and fingertip contour is less clearly authored than the endpoints. No LTX-like broad smear, but insufficient clean-hand evidence for this span.'),('PROMISING_SOURCE_STUDY_ONLY','Short raised-hand transition retains painted finger separation, elbow silhouette and figure outline at native256px. No obvious doubled hand outline in the inspected midpoint. Existing source arm foreshortening and scale rejection still apply.'),('PROMISING_SOURCE_STUDY_ONLY','Short raised-hand transition retains readable finger separation and the forearm contour at native256px. No obvious doubled hand outline in the inspected midpoint. Existing source arm foreshortening and scale rejection still apply.')]
for (a,b),(verdict,note) in zip(pairs,notes):
 p=folder/'take_01'/f'pair_{a:04d}_{b:04d}'
 endpoints=[]
 for i,s in [(0,a),(2,b)]:
  source=np.array(Image.open(folder/'inputs/neutral_gray'/f'{s:04d}.png').convert('RGB')).astype(int)
  target=np.array(Image.open(p/f'{i:04d}.png').convert('RGB')).astype(int)
  d=np.abs(source-target)
  endpoints.append({'input_index':s,'output_index':i,'decoded_rgb_exact':bool(np.array_equal(source,target)),'absolute_channel_difference_max':int(d.max()),'changed_pixel_count':int((d>0).any(2).sum()),'explanation':'Load/save float roundtrip can alter channels by1; source PNG preserved separately.'})
 artifacts=[{'index':i,'path':runner.relative(root,p/f'{i:04d}.png'),'sha256':runner.sha(p/f'{i:04d}.png'),'role':'generated_midpoint' if i==1 else 'source_endpoint_roundtrip'} for i in range(3)]
 reviews.append({'pair':[a,b],'artifact_verdict':verdict,'model_observation':note,'artifacts':artifacts,'endpoints':endpoints})
receipt=runner.read_json(folder/'take_01/receipt.json')
runner.write_json(folder/'review.json',{'schema':'reef.rife-midpoint-model-review.v1','reviewer':'Codex whole_frame_interpolation subagent','reviewer_kind':'model_observation','reviewed_at_utc':runner.utc(),'scope':'Three source-only complete-frame midpoint method tests, not a wave delivery or human/device acceptance','receipt_path':runner.relative(root,folder/'take_01/receipt.json'),'receipt_sha256':runner.sha(folder/'take_01/receipt.json'),'workflow_sha256':runner.sha(folder/'workflow.api.json'),'method_invocations':{'queue_items':1,'independent_pair_model_inferences':3,'campaign_take_reservations':1},'elapsed_seconds':receipt['elapsed_seconds'],'sampled_total_card_peak_mib':receipt['sampled_card_peak_mib'],'results':reviews,'hard_limits':{'W1':'Internal bidirectional full-frame warping and per-pixel mask lerp disclosed. One PNG/layer does not prove one complete authored drawing; no acceptance given.','source_anatomy_and_scale':'Family02 draft01 already rejected before this study; interpolation cannot repair its source proportions.','alpha':'RGB-only neutral-gray output; transparent alpha propagation not implemented or accepted.','full_motion':'No complete41-frame animation made or accepted from this study.','owner_device_child_runtime_delivery_accepted':False},'next_method_use':'Test close, anatomically coherent whole-frame repaired keys; reject large source-pose jumps that collapse fingers. Do not combine parts or interpolate independently estimated mattes.'})
print(json.dumps({'elapsed_seconds':receipt['elapsed_seconds'],'peak_sampled_mib':receipt['sampled_card_peak_mib'],'endpoints':[x['endpoints'] for x in reviews]},indent=2))
