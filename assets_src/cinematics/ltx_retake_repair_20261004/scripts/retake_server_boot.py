import faulthandler,os,runpy,sys,socket,threading,time
from pathlib import Path
root=Path(r'C:\Users\Peter\AppData\Local\Programs\MermaidReefTools\ComfyUI\0.34.0\ComfyUI_windows_portable\ComfyUI')
os.chdir(root);sys.path.insert(0,str(root));sys.argv[0]=str(root/'main.py');faulthandler.enable();faulthandler.dump_traceback_later(60,repeat=True)
def ready():
 for _ in range(180):
  try:
   with socket.create_connection(('127.0.0.1',8191),timeout=1):faulthandler.cancel_dump_traceback_later();return
  except OSError:time.sleep(1)
threading.Thread(target=ready,daemon=True).start();runpy.run_path(str(root/'main.py'),run_name='__main__')
