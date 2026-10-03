from pathlib import Path
import datetime, hashlib, json, subprocess, re
B=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
BASE='6c5c1bd4a0951964a08043e72ae6472d2d402a9e'
P=B/'audit/job_final_action_consistency_v1_20261003'
RULES=['DL-AUTH-05','DL-AUTH-06','DL-AUTH-07','DL-ASSET-01','DL-ASSET-02','DL-ASSET-03','DL-VIS-01','DL-VIS-02','DL-VIS-03','DL-VIS-04','DL-VIS-05','DL-VIS-06','DL-INT-01','DL-INT-02','DL-INT-03','DL-INT-04','DL-MOT-09','DL-MOT-10','DL-MOT-11','DL-MOT-12','DL-MOT-13','DL-QA-03','DL-QA-04','DL-QA-05','DL-QA-06','DL-QA-07']
AUTH=['audit/MASTER_AUDIT_2026-08-09.md','design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md','audit/findings/ACTIVE_FINDINGS_2026-08-13.md','design/05_DOC_LEDGER.md','design/AUDIT_DEVELOPMENT_CONTRACT.md','design/animation/ANIMATION_PRODUCTION_PROTOCOL.md','design/animation/ROSHAN_MOVEMENT_LANGUAGE.md','design/CHAPTER2_EIGHT_CAREER_PRODUCTION_SPINE_2026-08-30.md','design/CHAPTER2_CAKE_VISUAL_PROGRESSION_2026-08-31.md']
def sha(data):return hashlib.sha256(data).hexdigest()
def put(path,data):
 path.parent.mkdir(parents=True,exist_ok=True)
 path.write_bytes((json.dumps(data,indent=2,ensure_ascii=False)+'\n').encode())
def git(*args):return subprocess.run(['git',*args],cwd=B,capture_output=True,check=True).stdout
assert git('rev-parse','HEAD').decode().strip()==BASE
assert not git('diff','--cached','--name-only','-z')
P.mkdir(parents=True,exist_ok=True)
authority=[]
for name in AUTH:
 data=(B/name).read_bytes(); text=data.decode('utf-8-sig'); lines=text.splitlines()
 if name.endswith('MASTER_AUDIT_2026-08-09.md'):
  headings=[(i,l) for i,l in enumerate(lines) if l.startswith('#') and ('Planning entry' in l or 'task index' in l.lower() or 'repair and regression' in l or 'satisfaction gate' in l)]
  excerpt=[]
  for i,l in headings:excerpt.extend(lines[i:i+32])
 elif 'ACTIVE_FINDINGS' in name:
  excerpt=[]
  for finding in ['MA-VIS-006','MA-PLAY-004']:
   start=next(i for i,l in enumerate(lines) if l=='## '+finding)
   end=next((i for i in range(start+1,len(lines)) if lines[i].startswith('## ')),len(lines))
   excerpt.extend(lines[start:end])
 elif 'COMPREHENSIVE' in name:
  excerpt=[]
  for i,l in enumerate(lines):
   if any(('`'+rule+'`') in l for rule in RULES):excerpt.extend(lines[i:i+8])
 else:excerpt=lines
 authority.append(dict(path=name,sha256=sha(data),bytes=len(data),read_excerpt='\n'.join(excerpt)))
put(P/'AUTHORITY_START.json',dict(baseline=BASE,checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),scope='Record owner-selected shared Roshan final-action format and inspect current layout/completion callers. Plan job-by-job rollout without changing runtime, scores or acceptance.',rules=RULES,findings=['MA-VIS-006','MA-PLAY-004'],authority=authority,required_evidence=['Current phase and route census with literal source hashes','Existing small-card versus full-stage layout source trace','Native wrapping canvas in context','All-job final-action plan, with child-input and specialist ownership preserved','No source/motion/runtime acceptance transfer','Document authority and development coverage gates','Review page/browser proof','Immutable publication and byte verification'],owner_direction='Use the same final-action sequence everywhere, with Roshan visibly finishing each task (recommended).',runtime_implementation='PENDING'))
put(B/'design/audit_impacts/job-final-action-consistency-20261003.json',dict(id='job-final-action-consistency-20261003',scope='Owner-selected consistent Roshan final-action presentation across all jobs and Opera training. Versioned operational brief, source-derived phase coverage and full-stage layout comparison. No gameplay or art replacement in this planning revision.',baseline=BASE,rules=RULES,findings=['MA-VIS-006','MA-PLAY-004'],files=['audit/job_final_action_consistency_v1_20261003/AUTHORITY_START.json'],validation=[dict(command='Authority and caller review at task start',result='PASS',evidence='audit/job_final_action_consistency_v1_20261003/AUTHORITY_START.json'),dict(command='Source-derived coverage, browser proof and document gates',result='PENDING',evidence='Not yet built or run')],acceptance_gaps='Shared runtime migration, exact authored actions, all individual artwork refinements, complete ordinary job/training routes, device/child/owner and comprehensive report approval remain open. Owner chose direction, not product acceptance.'))
print(json.dumps(dict(status='SCOPE_RECORDED_BEFORE_IMPLEMENTATION',baseline=BASE,authority_sources=len(authority),rules=RULES)))
