import os,runpy,sys
from pathlib import Path
root=Path(r"H:\MermaidReefTools\LocalVideo\ltx25\ComfyUI")
os.chdir(root);sys.path.insert(0,str(root));sys.path.insert(0,str(root.parent/"python_deps"))
print("ISOLATED_CORE",str(root),flush=True)
sys.argv[0]=str(root/"main.py");runpy.run_path(str(root/"main.py"),run_name="__main__")
