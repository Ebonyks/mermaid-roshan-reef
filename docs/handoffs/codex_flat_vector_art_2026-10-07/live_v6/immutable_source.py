"""Read exact historical source bytes; never substitutes a mutable branch."""
import subprocess,urllib.request
from functools import lru_cache
@lru_cache(maxsize=None)
def source_bytes(root,revision,path):
 if len(revision)!=40 or any(c not in '0123456789abcdef' for c in revision):raise ValueError('immutable full SHA required')
 if path.startswith('/') or '..' in path.split('/'):raise ValueError('unsafe source path')
 try:return subprocess.check_output(['git','show',revision+':'+path],cwd=root,stderr=subprocess.DEVNULL)
 except subprocess.CalledProcessError:
  url='https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/'+revision+'/'+path
  with urllib.request.urlopen(url,timeout=60) as response:
   if response.status!=200:raise ValueError('source access failure')
   return response.read()
