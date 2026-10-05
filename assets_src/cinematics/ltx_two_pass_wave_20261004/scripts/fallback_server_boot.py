import os,runpy,sys
from pathlib import Path
root=Path(r"C:\Users\Peter\AppData\Local\Programs\MermaidReefTools\ComfyUI\0.34.0\ComfyUI_windows_portable\ComfyUI")
os.chdir(root);sys.path.insert(0,str(root));sys.path.insert(0,str(Path(__file__).parent))
import comfy.options
comfy.options.enable_args_parsing()
import nodes
from study_nodes import StudyLTXAdaIN, StudyChunkFeedForward
from ltx_nag_vendor import LTX2_NAG
nodes.NODE_CLASS_MAPPINGS["StudyLTXAdaIN"]=StudyLTXAdaIN
nodes.NODE_CLASS_MAPPINGS["StudyChunkFeedForward"]=StudyChunkFeedForward
nodes.NODE_CLASS_MAPPINGS["LTX2_NAG"]=LTX2_NAG
# Log the first actual NAG application; math remains the pinned vendor function.
import ltx_nag_vendor
_nag_original=ltx_nag_vendor.normalized_attention_guidance
_nag_calls=0
def measured_nag(self,pos,neg):
 global _nag_calls
 if _nag_calls==0:print("STUDY_NAG_ACTUAL_ATTENTION",float((pos-neg).abs().mean()),flush=True)
 _nag_calls+=1
 return _nag_original(self,pos,neg)
ltx_nag_vendor.normalized_attention_guidance=measured_nag
sys.argv[0]=str(root/"main.py");runpy.run_path(str(root/"main.py"),run_name="__main__")
