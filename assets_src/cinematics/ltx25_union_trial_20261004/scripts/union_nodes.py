"""Study-only loading/patch execution receipts; no vendor source edits."""
import json,hashlib,time
from pathlib import Path
import torch
import numpy as np
from PIL import Image
import comfy.lora
R=Path(r'H:\MermaidReefTools\LocalVideo\ltx25');OUT=R/'results/union_trial'
CALLS={'all':0,'cuda':0,'keys':set()};original=comfy.lora.calculate_weight
def measured(patches,weight,key,*args,**kwargs):
 if patches:
  CALLS['all']+=1;CALLS['cuda']+=int(weight.device.type=='cuda');CALLS['keys'].add(key)
 return original(patches,weight,key,*args,**kwargs)
comfy.lora.calculate_weight=measured
class UnionGuideBatch:
 @classmethod
 def INPUT_TYPES(cls):return {'required':{'lane':(['quarter','half'],),'frames':('INT',{'default':41,'min':9,'max':41,'step':8})}}
 RETURN_TYPES=('IMAGE',);FUNCTION='load';CATEGORY='Mermaid/study'
 def load(self,lane,frames):
  files=[R/f'input/union_trial/guide_{lane}/{i:04d}.png' for i in range(frames)]
  a=torch.stack([torch.from_numpy(np.array(Image.open(f).convert('RGB'),dtype=np.float32)/255) for f in files])
  assert tuple(a.shape)==(frames,224 if lane=='quarter' else 448,160 if lane=='quarter' else 320,3)
  return (a,)
class UnionModelProof:
 @classmethod
 def INPUT_TYPES(cls):return {'required':{'model':('MODEL',),'downscale':('FLOAT',{'default':2})}}
 RETURN_TYPES=('MODEL',);FUNCTION='check';CATEGORY='Mermaid/study'
 def check(self,model,downscale):
  assert downscale==2 and len(model.patches)>0,'No actual adapter patches/incorrect control scale'
  OUT.mkdir(exist_ok=True);j={'status':'PATCH_INSTALL_PASS_EXECUTION_PENDING','patch_keys':len(model.patches),'downscale_factor':downscale,'new_engine':'LTX-2.5 W4A8','sampler_execution_proved':False}
  (OUT/'patch_install.json').write_text(json.dumps(j,indent=2)+'\n');print('UNION_PATCH_INSTALL',j,flush=True)
  return (model,)
class UnionOutputProof:
 @classmethod
 def INPUT_TYPES(cls):return {'required':{'images':('IMAGE',)}}
 RETURN_TYPES=('IMAGE',);FUNCTION='check';CATEGORY='Mermaid/study'
 def check(self,images):
  assert torch.isfinite(images).all() and CALLS['cuda']>0,'No GPU LoRA application proved'
  j={'status':'GPU_LORA_WEIGHT_APPLICATION_PASS','total_patch_calls':CALLS['all'],'cuda_patch_calls':CALLS['cuda'],'unique_weight_keys':len(CALLS['keys']),'output_shape':list(images.shape),'quality_accepted':False}
  (OUT/'patch_execution.json').write_text(json.dumps(j,indent=2)+'\n');print('UNION_GPU_PATCH_EXECUTION',j,flush=True)
  return (images,)
NODE_CLASS_MAPPINGS={'UnionGuideBatch':UnionGuideBatch,'UnionModelProof':UnionModelProof,'UnionOutputProof':UnionOutputProof}
