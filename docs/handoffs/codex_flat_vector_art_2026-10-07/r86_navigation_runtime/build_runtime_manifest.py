from pathlib import Path
import subprocess,json,hashlib,datetime
T=Path.cwd();P=T/'docs/handoffs/codex_flat_vector_art_2026-10-07/r86_navigation_runtime';B='dd799b2d43871b29d1d6e0503646308a194dad1e'
def git(*args):return subprocess.check_output(['git',*args],stderr=subprocess.PIPE)
def sha(b):return hashlib.sha256(b).hexdigest()
names=git('diff','--cached','--name-only',B).decode().splitlines();expected=['scripts/navigation_controller.gd','scripts/pause_menu.gd','scripts/storybook_ui.gd'];assert [p for p in names if p.startswith('scripts/')]==expected
manifest=P/'MANIFEST.json';exclude={manifest.relative_to(T).as_posix()};rows=[]
required=['assets/fashion/skin_engine_v2/ui/wardrobe_card.png','assets_src/fashion_designer/skin_engine_v2/derivations.json','assets_src/fashion_designer/skin_engine_v2/generation_briefs.json','assets_src/fashion_designer/skin_engine_v2/native/wardrobe_card.png','scripts/ci.sh','tools/godot_baseline.json','tools/resolve_godot.py','project.godot','scripts/main.gd','scripts/save_state.gd','scenes/main.tscn','design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md','design/AUDIT_DEVELOPMENT_CONTRACT.md','AGENTS.md','SECURITY.md']
matrix=json.loads((P/'NAVIGATION_CALLER_MATRIX.json').read_text());required+= [x['path']for x in matrix['source_files']]
for path in sorted(set(names+required)-exclude):
 blob=git('show',':'+path);raw=(T/path).read_bytes();row={'revision':None,'path':path,'bytes':len(blob),'sha256':sha(blob),'role':'R86 scoped implementation and complete review evidence payload'if path in names else'Required existing source/provenance/rule reference'}
 if raw!=blob:row.update({'local_raw_sha256':sha(raw),'local_raw_bytes':len(raw),'git_transport_note':'Manifest binds canonical Git blob bytes; exact tested raw source is separately bound by SOURCE_PIN and native/fullCI receipts.'})
 rows.append(row)
prereq=json.loads((P/'CONTEXT_PREREQUISITE.json').read_text());seen={(x['revision'],x['path'])for x in rows}
for item in prereq['files']:
 key=(item['revision'],item['path'])
 if key in seen:continue
 blob=git('show',item['revision']+':'+item['path']);assert len(blob)==item['bytes']and sha(blob)==item['sha256'];rows.append({**{k:item[k]for k in ['revision','path','bytes','sha256']},'role':'Previously published exact source-state/sample prerequisite; no new context or coverage credit'});seen.add(key)
data={'schema':'reef.runtime_trial_delivery/1','baseline':B,'payload_revision':'Immutable commit named in REMOTE_VERIFICATION.json; no recursive self hash','created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'entry':P.relative_to(T).as_posix()+'/README.md','files':rows,'required_files':len(rows),'required_bytes':sum(x['bytes']for x in rows),'source_scope':'Full project inherited from exact public baseline; only three named GD files change runtime behavior/material. Tested raw source and sidecars are bound by SOURCE_PIN and exact import/native/fullCI guards. Manifest covers every changed payload path and the selected required source/rule/provenance/current-context dependencies. It does not claim a new whole-game visual inventory or fresh verification of every file in the separately published R85 historical archive.','source_complete_baseline_tree':'https://github.com/Ebonyks/mermaid-roshan-reef/tree/'+B,'post_payload_own_metadata':'REMOTE_VERIFICATION and later receipt/gate/impact metadata are separately checked at their final immutable revision. Manifest itself is verified by exact length/hash in the receipt.','acceptance':'Work-branch review only; no dev integration, accepted removal, whole-game denominator, formalQA11/device/child/owner or release acceptance.'}
manifest.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8',newline='\n');print('R86_RUNTIME_MANIFEST',len(rows),data['required_bytes'],flush=True)
