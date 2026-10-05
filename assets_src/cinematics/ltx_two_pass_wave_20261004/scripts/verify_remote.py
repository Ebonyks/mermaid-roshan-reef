"""Anonymous immutable-GitHub delivery verification for this complete source study."""
from pathlib import Path
import argparse,json,hashlib,urllib.request,urllib.parse,concurrent.futures,time,re,subprocess
from datetime import datetime,timezone
p=Path(__file__).resolve().parents[1];r=p.parents[2]
a=argparse.ArgumentParser();a.add_argument('revision');args=a.parse_args();rev=args.revision
if not re.fullmatch('[0-9a-f]{40}',rev):raise SystemExit('Requires exact 40-character commit revision')
base='https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/'+rev+'/'
man=json.loads((p/'manifest.json').read_text());prefix=p.relative_to(r).as_posix()+'/'
paths=[prefix+'manifest.json']+[prefix+x['path'] for x in man['payload']]
paths += sorted({source for row in man["payload"] for source in row.get("source_paths",[])})
paths += ['assets/characters/roshan_25d/roshan_gesture_a.png','ASSET_LICENSES.md','AGENTS.md','CLAUDE.md','SECURITY.md','audit/MASTER_AUDIT_2026-08-09.md','audit/animation/README.md','audit/findings/ACTIVE_FINDINGS_2026-08-13.md','design/05_DOC_LEDGER.md','design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md','design/AUDIT_DEVELOPMENT_CONTRACT.md','design/animation/ANIMATION_PRODUCTION_PROTOCOL.md','design/animation/ROSHAN_MOVEMENT_LANGUAGE.md','design/animation/WORKFLOW_OPTIONS_2026-10-03.md','design/templates/ANIMATION_JOB_CARD_V1.md','design/audit_impacts/ltx-two-pass-wave-20261004.json']
for previous_name in ['ltx_registered_wave_20261004','ltx_retake_repair_20261004']:
 previous=p.parent/previous_name;previous_manifest=json.loads((previous/'manifest.json').read_text());previous_prefix=previous.relative_to(r).as_posix()+'/'
 paths += [previous_prefix+'manifest.json',previous_prefix+'remote_verification.json']
# External source licenses/official configs are saved in the new payload or pinned primary URLs.
paths=sorted(set(paths));rows=[];fail=[]
expected_payload={prefix+x['path']:x['sha256'] for x in man['payload']}

def fetch(path):
 expected=expected_payload.get(path)
 if expected is None:
  blob=subprocess.run(['git','show',rev+':'+path],cwd=r,capture_output=True,check=True).stdout
  expected=hashlib.sha256(blob).hexdigest()
 for attempt in range(3):
  try:
   with urllib.request.urlopen(urllib.request.Request(base+urllib.parse.quote(path,safe='/'),headers={'User-Agent':'MermaidReef-public-source-packet-check'}),timeout=60) as f:
    content=f.read();status=f.status
   actual=hashlib.sha256(content).hexdigest()
   if actual!=expected:raise ValueError('SHA-256 mismatch '+actual+' expected '+expected)
   return {'path':path,'sha256':actual,'bytes':len(content),'http_status':status,'anonymous_access':'PASS'}
  except Exception as e:
   if attempt==2:return {'path':path,'error':str(e)}
   time.sleep(1+attempt)
started=datetime.now(timezone.utc).isoformat();print('VERIFYING',len(paths),'immutable remote files',flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
 for n,item in enumerate(pool.map(fetch,paths),1):
  (fail if 'error' in item else rows).append(item)
  if n%50==0:print('REMOTE_PROGRESS',n,'/',len(paths),'failures',len(fail),flush=True)
receipt={'status':'ARCHIVE_COMPLETE' if not fail else 'HANDOFF_BLOCKED','repository':'Ebonyks/mermaid-roshan-reef','branch':'codex/ltx-two-pass-wave-20261004','remote_revision':rev,'tree_url':'https://github.com/Ebonyks/mermaid-roshan-reef/tree/'+rev+'/'+prefix.rstrip('/'),'manifest_url':base+prefix+'manifest.json','started_at_utc':started,'checked_at_utc':datetime.now(timezone.utc).isoformat(),'access_mode':'Anonymous HTTPS, no Authorization header or login; public owner-authorized repository.','payload_sha256':man['payload_sha256'],'verified_file_count':len(rows),'verified_bytes':sum(x['bytes'] for x in rows),'files':rows,'failures':fail,'generation_claim':'Executed source-only repair trials; completed footage remains rejected/reference-only, failed attempts have no invented footage.','delivery_accepted':False,'device_child_owner_acceptance':'Not granted by this archive/public-access verification.','receipt_not_part_of_payload':'Receipt is written after verification and committed separately to avoid self-hash cycles.'}
(p/'remote_verification.json').write_text(json.dumps(receipt,indent=2)+'\n');print(receipt['status'],len(rows),'files',receipt['verified_bytes'],'bytes',flush=True)
if fail:raise SystemExit(1)
