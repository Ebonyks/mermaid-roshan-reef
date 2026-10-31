from pathlib import Path
import sys,shutil,json
root=Path.cwd(); sys.path.insert(0,str(root/'tools'))
import ltx_wave_experiment as runner
folder=root/'assets_src/animation/roshan_wave_repair_20261010/rife_midpoint_01'
runtime=Path('H:/MermaidReefTools/LocalVideo/ltx25')
rtinput=runtime/'input/wave_repair_20261010/rife_midpoint_01';rtinput.mkdir(parents=True,exist_ok=True)
sources=[]
for lane in ['native_rgba','neutral_gray']:
 for i in [3,6,10,12,14]:
  p=folder/'inputs'/lane/f'{i:04d}.png'
  entry={'path':p.relative_to(root).as_posix(),'sha256':runner.sha(p),'role':'complete-cel-source-candidate' if lane=='native_rgba' else 'whole-cel-neutral-background-interpolation-input','acceptance':'SOURCE_STUDY_ONLY; source family rejected for anatomy and scale'}
  if lane=='neutral_gray':
   staged=rtinput/f'{i:04d}.png';shutil.copyfile(p,staged)
   entry['runtime_path']=staged.relative_to(runtime).as_posix()
  sources.append(entry)
graph={'1':{'class_type':'FrameInterpolationModelLoader','inputs':{'model_name':'rife_v4.25.safetensors'}}}
outputs={'images':[],'latents':[]};pairs=[(6,3),(14,12),(10,12)]
for n,(a,b) in enumerate(pairs):
 ids=[str(2+n*10+i) for i in range(5)]
 graph[ids[0]]={'class_type':'LoadImage','inputs':{'image':f'wave_repair_20261010/rife_midpoint_01/{a:04d}.png'}}
 graph[ids[1]]={'class_type':'LoadImage','inputs':{'image':f'wave_repair_20261010/rife_midpoint_01/{b:04d}.png'}}
 graph[ids[2]]={'class_type':'ImageBatch','inputs':{'image1':[ids[0],0],'image2':[ids[1],0]}}
 graph[ids[3]]={'class_type':'FrameInterpolate','inputs':{'interp_model':['1',0],'images':[ids[2],0],'multiplier':2}}
 graph[ids[4]]={'class_type':'SaveImage','inputs':{'images':[ids[3],0],'filename_prefix':f'wave_repair_20261010/rife_midpoint_01/pair_{a:04d}_{b:04d}'}}
 outputs['images'].append({'node':ids[4],'name':f'pair_{a:04d}_{b:04d}','count':3,'canvas':[256,256]})
pins={'ComfyUI':'87465b8f1f64a27a46f16f22b13b410494dca66d','Comfy-Org_frame_interpolation':'219da3c9d8c357ceaf457fc1d5932c6e861b8dee','weight_file':'rife_v4.25.safetensors','weight_sha256':'1505884b9bdae956795430d2a70f7e2317b2abd8f130f8cfdb35a5759f909481','weight_size_bytes':22674688}
for name in ['nodes_frame_interpolation.py','frame_interpolation_models/ifnet.py']:
 pins['source_'+name]=runner.sha(runtime/'ComfyUI/comfy_extras'/name)
manifest={'sources':sources,'model_workflow_pins':pins,'settings':{'method':'Whole-frame learned bidirectional optical flow and spatial mask fusion','multiplier':2,'pairs':pairs,'canvas':[256,256],'background_rgb':[245,245,245],'background_flattening_tool':'Aseprite1.3.18.4-x64','stage':'RGB-only midpoint method study','alpha':'Native RGBA preserved. Aseprite composited entire cell once over neutral background. FrameInterpolate model has3-channel RGB output; no claim of transparent final.','W1_provenance':'No authored body-part layers or pasted hand. RIFE internally warps both whole frames and torch.lerp fuses them with learned sigmoid mask. This is expressly disclosed; one-flat-layer output is not whole-drawing acceptance. Any doubled contours or crossfade ghosts cause rejection.','source_anatomy':'Source draft itself already rejected for shortened arms and scale drift; this method cannot cure those source defects.','attempt_count':'Three independent midpoint nodes in one graph/queue item count as one campaign invocation; no extra submission or hidden refinement.'}}
runner.write_json(folder/'workflow.api.json',graph);runner.write_json(folder/'sources.json',manifest);runner.write_json(folder/'outputs.json',outputs)
print('Prepared3pairs; input model SHA',pins['weight_sha256'])
