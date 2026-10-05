"""Small study-only latent AdaIN adapter; arithmetic follows pinned official LTXVideo multiscale code."""
import torch
class StudyLTXAdaIN:
 @classmethod
 def INPUT_TYPES(cls):return {"required":{"samples":("LATENT",),"reference":("LATENT",)}}
 RETURN_TYPES=("LATENT",);FUNCTION="apply";CATEGORY="Mermaid/source-study"
 def apply(self,samples,reference):
  x=samples["samples"];r=reference["samples"].to(x)
  rs,rm=torch.std_mean(r,dim=tuple(range(2,r.ndim)),keepdim=True)
  xs,xm=torch.std_mean(x,dim=tuple(range(2,x.ndim)),keepdim=True)
  if torch.any(xs==0):raise ValueError("Zero-variance latent; cannot perform official AdaIN")
  out=samples.copy();out["samples"]=(x-xm)/xs*rs+rm;return (out,)

class StudyChunkFeedForward:
 @classmethod
 def INPUT_TYPES(cls):return {"required":{"model":("MODEL",),"chunk_tokens":("INT",{"default":512,"min":64,"max":4096})}}
 RETURN_TYPES=("MODEL",);FUNCTION="apply";CATEGORY="Mermaid/source-study"
 def apply(self,model,chunk_tokens):
  import types
  from comfy.ldm.lightricks.model import FeedForward
  m=model.clone();count=0
  for name,module in m.get_model_object("diffusion_model").named_modules():
   if not isinstance(module,FeedForward):continue
   original=module.forward
   def forward(this,x,_original=original,_chunk=chunk_tokens):
    if x.shape[1]<=_chunk:return _original(x)
    return torch.cat([_original(y) for y in x.split(_chunk,dim=1)],dim=1)
   m.add_object_patch("diffusion_model."+name+".forward",types.MethodType(forward,module));count+=1
  if not count:raise ValueError("No LTX FeedForward modules found")
  print("STUDY_CHUNK_FEED_FORWARD",count,"modules",chunk_tokens,"tokens",flush=True)
  return (m,)
