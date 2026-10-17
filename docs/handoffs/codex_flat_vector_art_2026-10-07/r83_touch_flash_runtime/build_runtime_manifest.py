from pathlib import Path
import subprocess,json,hashlib,datetime
T=Path.cwd();P=T/'docs/handoffs/codex_flat_vector_art_2026-10-07/r83_touch_flash_runtime';B='dd799b2d43871b29d1d6e0503646308a194dad1e'
def git(*args):return subprocess.check_output(['git',*args],stderr=subprocess.PIPE)
def sha(b):return hashlib.sha256(b).hexdigest()
names=git('diff','--cached','--name-only',B).decode().splitlines();assert 'scripts/touch_ui.gd'in names
manifest=P/'MANIFEST.json';exclude={manifest.relative_to(T).as_posix()};rows=[]
required=['assets/opera/worlds/props/fx_telegraph_ring.png','assets/opera/worlds/props/fx_telegraph_ring.png.import','assets_src/imagegen/imp_animation_states_2026-08-02/PROMPTS.md','scripts/ci.sh','tools/godot_baseline.json','tools/resolve_godot.py','project.godot','scripts/main.gd','scripts/save_state.gd','scenes/main.tscn','design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md','design/AUDIT_DEVELOPMENT_CONTRACT.md','AGENTS.md','SECURITY.md']
for path in sorted(set(names+required)-exclude):
 blob=git('show',':'+path);row={'revision':None,'path':path,'bytes':len(blob),'sha256':sha(blob),'role':'Current trial payload'if path in names else'Required existing source/rule reference'}
 raw=(T/path).read_bytes()
 if raw!=blob:row.update({'local_raw_sha256':sha(raw),'local_raw_bytes':len(raw),'git_transport_note':'Manifest SHA-256 binds canonical Git blob bytes; source raw bytes separately bound by native/CI pins.'})
 rows.append(row)
oldrev='f90b69eec617018691a8c62ffb1c22a2f6acf799';oldroot='docs/handoffs/codex_flat_vector_art_2026-10-07/r82_touch_flash_reuse'
for rel in ['README.md','REVIEW.json','CANDIDATE_SAMPLE.json','native/attempt1_entry_source_1280/source_slide_onset.png','native/attempt1_entry_source_1600/source_swing_onset.png']:
 path=oldroot+'/'+rel;blob=git('show',oldrev+':'+path);rows.append({'revision':oldrev,'path':path,'bytes':len(blob),'sha256':sha(blob),'role':'Immutable previously published source/reuse context; no new frame or acceptance credit'})
data={'schema':'reef.runtime_trial_delivery/1','baseline':B,'payload_revision':'Bound by immutable commit in REMOTE_VERIFICATION.json; no self-referential commit/hash','created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'entry':P.relative_to(T).as_posix()+'/README.md','files':rows,'required_files':len(rows),'required_bytes':sum(x['bytes']for x in rows),'source_scope':'Exact full project inherited from baseline on public repository; one function and cached texture reference differ. Native and full-CI pins bind tested raw runtime files. This review packet lists changed files and required context/rules; the full baseline is available as its immutable Git tree.','source_complete_baseline_tree':'https://github.com/Ebonyks/mermaid-roshan-reef/tree/'+B,'post_payload_own_metadata':'REMOTE_VERIFICATION.json and later receipt/gate/impact edits checked separately at their final immutable revision; no recursive self hash','acceptance':'Trial only; no dev integration, accepted removal, whole-game denominator, QA11/device/child/owner or release acceptance'}
manifest.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8',newline='\n');print('R83_RUNTIME_MANIFEST',len(rows),data['required_bytes'])
