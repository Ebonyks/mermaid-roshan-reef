import os,runpy,sys
from pathlib import Path
root=Path(r"C:\Users\Peter\AppData\Local\Programs\MermaidReefTools\ComfyUI\0.34.0\ComfyUI_windows_portable\ComfyUI")
os.chdir(root);sys.path.insert(0,str(root));sys.path.insert(0,str(Path(__file__).parent))
import comfy.options
comfy.options.enable_args_parsing()
import nodes
from study_nodes import StudyLTXAdaIN
nodes.NODE_CLASS_MAPPINGS["StudyLTXAdaIN"]=StudyLTXAdaIN
sys.argv[0]=str(root/"main.py");runpy.run_path(str(root/"main.py"),run_name="__main__")
