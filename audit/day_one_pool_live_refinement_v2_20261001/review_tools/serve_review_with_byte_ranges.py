from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote,urlsplit
ROOT=Path(__file__).resolve().parents[1]
PREFIXES=('/audit/job_artwork_refinement_20261001/','/audit/day2_job_contexts_2026-09-30/','/audit/day2_art_library_2026-09-30/',
 '/audit/day2_action_continuity_20261001/','/assets_src/imagegen/day2_refinement_20261001/',
 '/audit/day2_nursery_contact_20261001/','/audit/day2_authored_launch_20261001/',
 '/assets_src/imagegen/day2_nursery_body_20261001/',
 '/assets_src/imagegen/day2_replacements_batch1_20260930/','/assets_src/local_motion/day2_batch1_20260930/')
PREFIXES+=("/audit/day2_nursery_action_v4_20261001/","/audit/job_artwork_refinement_live/","/assets_src/imagegen/day2_nursery_motionkeys_20261001/","/assets_src/imagegen/day2_nursery_lower_bridge_20261001/","/assets/opera/worlds/nursery/refinement_v2/")
import json
import hashlib,subprocess,mimetypes
IMAGE_PATHS={'/'+x['path'] for x in json.loads((ROOT/'audit/day2_job_contexts_2026-09-30/inventory.json').read_text())['items']}
SPARSE=json.loads((ROOT/'tmp/verified_capture_sparsity.json').read_text())
GIT_CAPTURES={'/'+x['path']:x for x in SPARSE['files']}
ACTION_SPARSE=json.loads((ROOT/'tmp/verified_action_capture_sparsity.json').read_text())
GIT_CAPTURES.update({'/'+x['path']:{**x,'revision':ACTION_SPARSE['revision']} for x in ACTION_SPARSE['files']})
NURSERY_SPARSE=json.loads((ROOT/'tmp/verified_nursery_capture_sparsity.json').read_text())
GIT_CAPTURES.update({'/'+x['path']:x for x in NURSERY_SPARSE['files']})
PREFIXES+=('/assets_src/imagegen/day2_nursery_babies_v2_20261001/','/audit/day2_nursery_baby_fit_v1_20261001/')
PREFIXES+=('/audit/day_one_job_art_census_20261001/',)
DAY_ONE=json.loads((ROOT/'audit/day_one_job_art_census_20261001/inventory.json').read_text())
for row in DAY_ONE['items']:
 IMAGE_PATHS.add('/'+row['path'])
 if not (ROOT/row['path']).is_file():
  GIT_CAPTURES['/'+row['path']]={**row,'size_bytes':row['bytes'],'revision':DAY_ONE['production_revision']}
PREFIXES+=('/assets_src/imagegen/day2_nursery_faron_v2_20261001/',)
PREFIXES+=('/assets_src/imagegen/day2_nursery_lower_bridge_v2_20261001/',)
PREFIXES+=('/assets_src/imagegen/day2_nursery_faron_motionkeys_20261001/',)
PREFIXES+=('/audit/day_one_job_art_census_v2_20261001/','/assets_src/imagegen/day1_pool_trash_v2_20261001/','/audit/job_art_current_source_reconciliation_20261001/')
DAY_ONE_V2=json.loads((ROOT/'audit/day_one_job_art_census_v2_20261001/inventory.json').read_text())
for row in DAY_ONE_V2['items']:
 IMAGE_PATHS.add('/'+row['path'])
 if not (ROOT/row['path']).is_file():
  GIT_CAPTURES['/'+row['path']]={**row,'size_bytes':row['bytes'],'revision':DAY_ONE_V2['production_revision']}
PREFIXES+=('/assets_src/imagegen/day1_pool_skimmer_v2_20261001/',)
CURRENT_NATIVE=json.loads((ROOT/'audit/day_one_job_art_census_v2_20261001/NATIVE_RESOURCE_CATALOG.json').read_text())
for row in CURRENT_NATIVE['items']:
 assert row['path'].startswith(('assets/','assets_src/')) and '..' not in row['path'].split('/')
 IMAGE_PATHS.add('/'+row['path'])
PREFIXES+=('/audit/day_one_pool_live_refinement_v2_20261001/','/assets/castle/day_one_pool/activities/refinement_v2/')
IMAGE_PATHS.add('/design/audit_impacts/day-one-pool-live-refinement-v2-20261001.json')
class Handler(SimpleHTTPRequestHandler):
 def __init__(self,*a,**kw):super().__init__(*a,directory=str(ROOT),**kw)
 def byte_span(self,size):
  import re
  value=self.headers.get('Range')
  if not value:return None
  match=re.fullmatch(r'bytes=(\d*)-(\d*)',value.strip())
  if not match or not any(match.groups()) or size<=0:raise ValueError('Invalid byte range')
  first,last=match.groups()
  if first:
   start=int(first);end=min(int(last),size-1) if last else size-1
  else:
   count=int(last)
   if count<=0:raise ValueError('Invalid suffix range')
   start=max(0,size-count);end=size-1
  if start>=size or end<start:raise ValueError('Unsatisfiable byte range')
  return start,end
 def send_head(self):
  self.range_remaining=None
  if not self.headers.get('Range'):return super().send_head()
  path=Path(self.translate_path(self.path)).resolve()
  if not path.is_relative_to(ROOT.resolve()) or not path.is_file():
   self.send_error(404);return None
  size=path.stat().st_size
  try:span=self.byte_span(size)
  except ValueError:
   self.send_response(416);self.send_header('Content-Range',f'bytes */{size}');self.send_header('Content-Length','0');self.end_headers();return None
  start,end=span
  source=path.open('rb');source.seek(start)
  self.range_remaining=end-start+1
  self.send_response(206)
  self.send_header('Content-Type',self.guess_type(str(path)))
  self.send_header('Content-Length',str(self.range_remaining))
  self.send_header('Content-Range',f'bytes {start}-{end}/{size}')
  self.send_header('Accept-Ranges','bytes')
  self.end_headers()
  return source
 def copyfile(self,source,outputfile):
  remaining=getattr(self,'range_remaining',None)
  if remaining is None:return super().copyfile(source,outputfile)
  while remaining>0:
   chunk=source.read(min(65536,remaining))
   if not chunk:break
   outputfile.write(chunk);remaining-=len(chunk)
 def permitted(self):
  p=unquote(urlsplit(self.path).path)
  return '..' not in p.split('/') and (any(p.startswith(x) for x in PREFIXES) or p in IMAGE_PATHS)
 def do_GET(self):
  if not self.permitted():self.send_error(404);return
  if self.git_capture(False):return
  super().do_GET()
 def do_HEAD(self):
  if not self.permitted():self.send_error(404);return
  if self.git_capture(True):return
  super().do_HEAD()
 def git_capture(self,head):
  p=unquote(urlsplit(self.path).path)
  if p not in GIT_CAPTURES:return False
  row=GIT_CAPTURES[p]
  raw=subprocess.run(['git','show',row.get('revision',SPARSE['revision'])+':'+row['path']],cwd=ROOT,capture_output=True,check=True).stdout
  if len(raw)!=row['size_bytes'] or hashlib.sha256(raw).hexdigest()!=row['sha256']:
   self.send_error(500,'Verified Git object mismatch');return True
  try:span=self.byte_span(len(raw))
  except ValueError:
   self.send_response(416);self.send_header('Content-Range',f'bytes */{len(raw)}');self.send_header('Content-Length','0');self.end_headers();return True
  total=len(raw)
  self.send_response(206 if span is not None else 200)
  if span is not None:
   start,end=span;raw=raw[start:end+1]
   self.send_header('Content-Range',f'bytes {start}-{end}/{total}')
  self.send_header('Accept-Ranges','bytes')
  self.send_header('Content-Type',mimetypes.guess_type(row['path'])[0] or 'application/octet-stream')
  self.send_header('Content-Length',str(len(raw)))
  self.end_headers()
  if not head:self.wfile.write(raw)
  return True
 def list_directory(self,path):self.send_error(404);return None
ThreadingHTTPServer(('127.0.0.1',8877),Handler).serve_forever()

