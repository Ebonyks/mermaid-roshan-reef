from pathlib import Path
import json,subprocess,hashlib,datetime
T=Path.cwd();P=T/'docs/handoffs/codex_flat_vector_art_2026-10-07/r88_critter_book_runtime';B='dd799b2d43871b29d1d6e0503646308a194dad1e';F='684e34f06ebce6a70065847b5ecb69547ea8a128'
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def git(*a):return subprocess.check_output(['git',*a],stderr=subprocess.PIPE)
def sha(b):return hashlib.sha256(b).hexdigest()
names=git('diff','--cached','--name-only',B).decode().splitlines();pin=rd(P/'CANDIDATE_SOURCE_PIN.json');assert [p for p in names if p.startswith('scripts/')]==pin['changed_from_baseline'];manifest=P/'MANIFEST.json';exclude={manifest.relative_to(T).as_posix()};entries={}
def add(rev,path,blob,role):
 key=(rev,path);row={'revision':rev,'path':path,'bytes':len(blob),'sha256':sha(blob),'role':role}
 if key in entries:assert entries[key]['sha256']==row['sha256']
 entries[key]=row
required=['assets/fashion/skin_engine_v2/ui/wardrobe_card.png','assets/fashion/skin_engine_v2/ui/wardrobe_panel.png','assets_src/fashion_designer/skin_engine_v2/derivations.json','assets_src/fashion_designer/skin_engine_v2/generation_briefs.json','assets_src/fashion_designer/skin_engine_v2/native/wardrobe_card.png','assets_src/fashion_designer/skin_engine_v2/native/wardrobe_panel.png','scripts/ci.sh','tools/godot_baseline.json','tools/resolve_godot.py','project.godot','design/reference/games.json','scripts/main.gd','scripts/save_state.gd','scripts/audio_director.gd','scripts/living_world.gd','scripts/living_world_catalog.gd','scripts/living_world_canvas.gd','scenes/main.tscn','design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md','design/AUDIT_DEVELOPMENT_CONTRACT.md','AGENTS.md','SECURITY.md']
# Preserve the separately published source-only caller matrix's exact scope.
root='docs/handoffs/codex_flat_vector_art_2026-10-07/r86_navigation_runtime/'
matrix=json.loads(git('show',F+':'+root+'NAVIGATION_CALLER_MATRIX.json'));required+=[x['path']for x in matrix['source_files']]
for path in sorted(set(names+required)-exclude):
 blob=git('show',':'+path);add(None,path,blob,'R88 current payload/evidence or required existing active source/provenance/rule')
 raw=(T/path).read_bytes()
 if raw!=blob:entries[(None,path)].update({'local_raw_sha256':sha(raw),'local_raw_bytes':len(raw),'git_transport_note':'Canonical Git blob bytes; every known tested raw source/sidecar path is separately bound by GIT_SOURCE_BINDING.json, including literal CRLF-to-LF where necessary.'})
for item in rd(P/'CONTEXT_PREREQUISITE.json')['files']:
 blob=git('show',item['revision']+':'+item['path']);assert len(blob)==item['bytes'] and sha(blob)==item['sha256'];add(item['revision'],item['path'],blob,'Immutable already-published current scene/source prerequisite; no new context/coverage credit')
for item in rd(P/'NEXT_BOOK_REUSE_AUDIT.json')['source_files']:
 blob=git('show',item['revision']+':'+item['path']);assert len(blob)==item['bytes']and sha(blob)==item['sha256'];add(item['revision'],item['path'],blob,'Existing viewed future-reuse source with explicit unresolved acceptance/fit; no new art, sample or implementation credit')
for item in rd(P/'CATALOGUE_UNION_PREREQUISITE.json')['files']:
 blob=git('show',item['revision']+':'+item['path']);assert len(blob)==item['bytes']and sha(blob)==item['sha256'];add(item['revision'],item['path'],blob,'Unchanged frozen catalogue IDinventory and last explicit92-IDpartial union; bookkeeping source only, no new runtime/visual review')
for item in rd(P/'R62_ALIAS_PREREQUISITE.json')['files']:
 blob=git('show',item['revision']+':'+item['path']);assert len(blob)==item['bytes']and sha(blob)==item['sha256'];add(item['revision'],item['path'],blob,'Existing published R62 catalogue alias semantics and exact currentNcatalogue; no new review or coverage credit')
for item in rd(P/'NAVIGATION_DEPENDENCY.json')['files']:
 blob=git('show',F+':'+item['path']);assert sha(blob)==item['after_sha256'];add(F,item['path'],blob,'Verbatim published navigation dependency code')
for name in ['README.md','REMOTE_VERIFICATION.json','GATES.json','SOURCE_PIN.json','GIT_SOURCE_BINDING.json','NAVIGATION_CALLER_MATRIX.json','full_ci_attempt2/FULL_CI_RESULT.json']:
 path=root+name;add(F,path,git('show',F+':'+path),'Separately published R86 dependency provenance/machine evidence; historical scope, not current combined pass')
data={'schema':'reef.runtime_trial_delivery/1','baseline':B,'payload_revision':'Immutable commit named in REMOTE_VERIFICATION.json; no recursive self hash','created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'entry':P.relative_to(T).as_posix()+'/README.md','files':list(entries.values()),'required_files':len(entries),'required_bytes':sum(x['bytes']for x in entries.values()),'source_scope':'Full project inherited from exact publicN. Four named runtime scripts are the book visual constructor plus verbatim published navigation dependency. Every known tested raw runtime/sidecar file maps to staged/committed Git blobs; every changed payload file and selected required source/rule/provenance/current-context dependency is declared. This does not claim new whole-game inventory or fresh re-verification of the entire separately published R87 historical archive.','source_complete_baseline_tree':'https://github.com/Ebonyks/mermaid-roshan-reef/tree/'+B,'post_payload_own_metadata':'Final receipt/gate/impact metadata is checked separately at its final immutable revision; this manifest is hashed and byte-verified by the receipt.','acceptance':'Review candidate; no dev integration, accepted removal, whole-game denominator, formalQA11/device/child/owner or release acceptance.'};manifest.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8',newline='\n');print('R88_RUNTIME_MANIFEST',len(entries),data['required_bytes'],flush=True)
