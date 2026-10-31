import torch
class StudyFiniteImages:
 @classmethod
 def INPUT_TYPES(cls):return {"required":{"images":("IMAGE",)}}
 RETURN_TYPES=("IMAGE",);FUNCTION="check";CATEGORY="Mermaid/source-study"
 def check(self,images):
  if not torch.isfinite(images).all():raise ValueError("Nonfinite decoded image values")
  print("DECODE_FINITE",tuple(images.shape),"min",float(images.min()),"max",float(images.max()),"std",float(images.std()),flush=True)
  if float(images.std())<0.01:raise ValueError("Near-constant/black decoder output")
  return (images,)
class StudyTemporalRetakeMask:
 @classmethod
 def INPUT_TYPES(cls):return {"required":{"samples":("LATENT",),"first_latent":("INT",{"default":3,"min":0,"max":1000}),"last_latent":("INT",{"default":4,"min":0,"max":1000})}}
 RETURN_TYPES=("LATENT",);FUNCTION="apply";CATEGORY="Mermaid/source-study"
 def apply(self,samples,first_latent,last_latent):
  x=samples["samples"];assert not x.is_nested and x.ndim==5
  assert 0<=first_latent<=last_latent<x.shape[2]
  mask=torch.zeros((x.shape[0],1,x.shape[2],x.shape[3],x.shape[4]),device=x.device,dtype=x.dtype)
  mask[:,:,first_latent:last_latent+1]=1
  out=samples.copy();out["noise_mask"]=mask
  print("FULL_FIGURE_TEMPORAL_RETAKE_MASK",first_latent,last_latent,"of",x.shape[2],flush=True)
  return (out,)

class StudyRuntimeReceipt:
 @classmethod
 def INPUT_TYPES(cls):return {"required":{"label":("STRING",{"default":"preflight"})}}
 RETURN_TYPES=("STRING",);FUNCTION="check";CATEGORY="Mermaid/source-study";OUTPUT_NODE=True
 def check(self,label):
  import comfy.memory_management as mem,comfy.model_management as mm,comfy.cli_args as cli
  import json,sys,importlib.metadata,datetime
  from pathlib import Path
  a=cli.args
  j={"label":label,"at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"core_nodes_file":__import__("nodes").__file__,"argv":sys.argv,"dynamic_vram_effective":mem.aimdo_enabled,"vram_state":mm.vram_state.name,"async_offload_streams":mm.NUM_STREAMS,"bf16_vae_requested":a.bf16_vae,"pinned_memory_disabled":a.disable_pinned_memory,"allocator":torch.cuda.memory.get_allocator_backend(),"torch":torch.__version__,"gpu":torch.cuda.get_device_name(0),"packages":{n:importlib.metadata.version(n) for n in ["transformers","tokenizers","huggingface-hub","comfy-kitchen","comfy-aimdo"]}}
  Path(r"H:\MermaidReefTools\LocalVideo\ltx25\results\runner_effective_configuration.json").write_text(json.dumps(j,indent=2)+"\n")
  assert j["dynamic_vram_effective"] and j["async_offload_streams"]==2 and j["bf16_vae_requested"] and not j["pinned_memory_disabled"] and j["allocator"]=="cudaMallocAsync",j
  print("EFFECTIVE_RUNTIME_PASS",json.dumps(j),flush=True)
  return ("PASS",)
NODE_CLASS_MAPPINGS={"StudyFiniteImages":StudyFiniteImages,"StudyTemporalRetakeMask":StudyTemporalRetakeMask,"StudyRuntimeReceipt":StudyRuntimeReceipt}
