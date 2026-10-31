from pathlib import Path
import json,subprocess,hashlib,datetime
T=Path.cwd();P=T/'docs/handoffs/codex_flat_vector_art_2026-10-07/r91_critter_insect_tab_runtime';B='d5e63a1ec6e79745da504ee3c3945e59ae35ea79'
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def git(*a):return subprocess.check_output(['git',*a],stderr=subprocess.PIPE)
def sha(b):return hashlib.sha256(b).hexdigest()
names=git('diff','--cached','--name-only',B).decode().splitlines();pin=rd(P/'CANDIDATE_SOURCE_PIN.json');assert sorted(x for x in names if x.startswith(('scripts/','assets/')))==sorted(pin['changed_from_baseline']);manifest=P/'MANIFEST.json';entries={}
def add(rev,path,b,role):
 key=(rev,path);x={'revision':rev,'path':path,'bytes':len(b),'sha256':sha(b),'role':role}
 if key in entries:assert entries[key]['sha256']==x['sha256']
 entries[key]=x
required=['assets/mg/butterfly.png','assets/mg/butterfly.png.import','assets/fashion/skin_engine_v2/ui/wardrobe_card.png','assets/fashion/skin_engine_v2/ui/wardrobe_panel.png','scripts/games/picture_games.gd','scripts/ci.sh','tools/godot_baseline.json','tools/resolve_godot.py','project.godot','design/reference/games.json','scripts/main.gd','scripts/save_state.gd','scripts/navigation_controller.gd','scripts/pause_menu.gd','scripts/storybook_ui.gd','scripts/audio_director.gd','scripts/living_world.gd','scripts/living_world_catalog.gd','scripts/living_world_canvas.gd','scenes/main.tscn','design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md','design/AUDIT_DEVELOPMENT_CONTRACT.md','AGENTS.md','SECURITY.md']
for path in sorted(set(names+required)-{manifest.relative_to(T).as_posix()}):
 b=git('show',':'+path);add(None,path,b,'R91 current payload or required baseline source/context/rule; one leaf candidate only')
 raw=(T/path).read_bytes()
 if raw!=b:entries[(None,path)].update(local_raw_sha256=sha(raw),local_raw_bytes=len(raw),git_transport_note='Exact tested raw source to canonical Git LF mapping is explicit in GIT_SOURCE_BINDING.json. Raw.log evidence must be byte-identical.')
 if path.endswith('.log'):assert raw==b, 'Raw log rewritten by Git: '+path
context=rd(P/'CONTEXT_PREREQUISITE.json');payload=context['payload_revision'];root='docs/handoffs/codex_flat_vector_art_2026-10-07/r89_critter_glyph_context/'
for name in ['README.md','CONGRUENCY_REVIEW.json','SOURCE_ACCEPTANCE.json','CONTEXT_REFERENCE.json','GLYPH_CONSUMERS.json','SOURCE_BINDINGS.json']:
 path=root+name;add(payload,path,git('show',payload+':'+path),'Direct pre-edit R89 source/scene/neighbor evidence; unchanged historical archive remains an immutable reference')
refs=json.loads(git('show',payload+':'+root+'SOURCE_BINDINGS.json'))['inputs']
for x in refs:
 path=x['path']
 if ('/native/attempt7_saved_full_1600/' in path) or path in ['assets/mg/butterfly.png','assets_src/imagegen/pass35_2026-07-16/chroma/butterfly.png','assets/fashion/skin_engine_v2/ui/wardrobe_card.png','assets/fashion/skin_engine_v2/ui/wardrobe_panel.png']:
  b=git('show',x['revision']+':'+path);assert len(b)==x['bytes']and sha(b)==x['sha256'];add(x['revision'],path,b,'Exact directly required pre-edit viewport or existing reused/neighbor/source-provenance input')
source=rd(P/'older_source_review/SOURCE.json');b=git('show',source['revision']+':'+source['path']);assert sha(b)==source['sha256'];add(source['revision'],source['path'],b,'Exact older source reuse-fit comparison; no approval or removal transfer by pathname')
d={'schema':'reef.runtime_trial_delivery/1','baseline':B,'payload_revision':'Bound by immutable REMOTE_VERIFICATION.json; final receipt metadata independently verified','created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'entry':P.relative_to(T).as_posix()+'/README.md','files':list(entries.values()),'required_files':len(entries),'required_bytes':sum(x['bytes']for x in entries.values()),'source_scope':'Inherited exact public F tree; only collection visualconstructor and declared mipmetadata change. Every known tested raw runtime/sidecar path maps to canonical Git blobs. Direct required R89 pre-edit source/scene inputs are reverified; unrelated immutable historical archives are referenced without recursive redeclaration. No source/acceptance transfer by pathname.','source_complete_baseline_tree':'https://github.com/Ebonyks/mermaid-roshan-reef/tree/'+B,'acceptance':'One local native750/local82 leaf candidate; no source/newuse/formalQA11/device/child/owner acceptance, complete category site/family closure, devintegration or accepted removal.'};manifest.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n');print('R91_RUNTIME_MANIFEST',len(entries),d['required_bytes'],flush=True)
