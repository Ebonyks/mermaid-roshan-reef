"""Build an exact R6 packet manifest, including immutable earlier captures and reuse sources."""
from pathlib import Path
import hashlib,json,subprocess
P=Path(__file__).resolve().parent;R=P.parents[2];R5='5e5140fb0f0b636825354b6db8d28da0e9c07446';SOURCE='6cde8aeae04aaedcc0b1ff22a05ef93ab9bf666f';DEV='e2b3c73789707aa49a91b4f42e2a9dd4b68225df'
def sha(b):return hashlib.sha256(b).hexdigest()
def read(n):return json.loads((P/n).read_text(encoding='utf-8'))
rows=[]
for p in sorted(P.rglob('*')):
 if not p.is_file() or p.name in ['MANIFEST.json','REMOTE_VERIFICATION.json'] or '__pycache__' in p.parts:continue
 b=p.read_bytes();rows.append({'path':p.relative_to(P).as_posix(),'bytes':len(b),'sha256':sha(b)})
historical={}
archive={x['path']:x for x in read('HISTORICAL_R5_MANIFEST.json')['files']}
for e in read('scene_coverage.json')['entries']:
 for x in e.get('captures',[]):
  n=x if isinstance(x,str) else x['path']
  if (P/n).is_file():continue
  if n not in archive:raise ValueError('Unresolved historical capture '+n)
  historical[n]={'path':P.relative_to(R).as_posix()+'/'+n,'revision':R5,'bytes':archive[n]['bytes'],'sha256':archive[n]['sha256'],'role':'required historical native capture;diagnostic only'}
refs={}
def source(n,rev,expected=None,role='required immutable source/provenance'):
 b=subprocess.check_output(['git','show',rev+':'+n],cwd=R,stderr=subprocess.PIPE)
 digest=sha(b)
 extra={}
 if expected is not None and digest!=expected:
  working=(R/n).read_bytes()
  if Path(n).suffix.lower() not in ['.svg','.gd','.json','.md','.gdshader','.tscn','.tres','.import'] or sha(working)!=expected or working.replace(b'\r\n',b'\n')!=b.replace(b'\r\n',b'\n'):raise ValueError('source hash differs '+n)
  extra={'recorded_worktree_sha256':expected,'line_endings':'historical native worktree CRLF;immutable Git export LF;every canonical settings/source byte identical'}
 refs[rev+':'+n]={'path':n,'revision':rev,'bytes':len(b),'sha256':digest,'role':role,**extra}
for group,key in [('hud_fashion/REUSE_INVENTORY.json','native_file_backed_sources'),('room_routes/REUSE_INVENTORY.json','sources'),('party_props/SOURCE_ASSET_INVENTORY.json','sources')]:
 for x in read('live_v6/'+group)[key]:source(x['path'],SOURCE,x['sha256'])
for x in read('GEOLOGIST_REUSE_20261012.json')['source_references']:source(x['path'],x['revision'],x['sha256'])
for x in read('ROOT_CONTEXT_REVIEW_20261012.json')['source_bindings']:source(x['path'],SOURCE)
for x in read('live_v6/MACHINE.json')['sources']:source(x['path'],x['revision'],x['git_blob_sha256'],role='exact bound native-capture source')
for x in read('source_scopes.json')['scopes']:source(x['path'],SOURCE,role='required stable369source-scope inventory script/shader dependency;not an artwork count')
for x in read('live_v6/R5_PRESERVATION_PROOF.json')['checks']:source(x['path'],R5,x['reconstructed_bytes_sha256'],role='immutable R5 metadata original required for literal-derivative integrity;unchanged archive')
picture=read('root_picture_review_20261012/review.json')
for x in picture['source_files']:source(x['path'],picture['source_revision'],role='immutable runtime/script or historical Git license;working license snapshot explicitly separate in PICTURE_IMPORT_PREFLIGHT.json')
for x in picture['reuse_inventory']:
 if 'runtime' in x:source(x['runtime'],picture['source_revision'],x['runtime_sha256']);source(x['alternate'],picture['source_revision'],x['alternate_sha256'])
 else:source(x['source'],picture['source_revision'],x['sha256'])
for x in read('root_picture_actions_review_20261012/review.json')['reuse_inventory']:source(x['path'],SOURCE,x['sha256'],role='required action-context reuse/appearance reference;protected originals unchanged')
for x in read('GARDEN_CLAY_POT_BINDING.json')['input_refs']+read('GARDEN_CLAY_POT_BINDING.json')['reuse_inspections']:
 if 'repository_reference' in x:source(x['repository_reference'],x['immutable_revision'],x['sha256'],role='prepared Garden job reference;not generated/accepted pixels')
required=[]
for n in ['AGENTS.md','SECURITY.md','ASSET_LICENSES.md','design/AUDIT_DEVELOPMENT_CONTRACT.md','design/05_DOC_LEDGER.md','design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md','audit/MASTER_AUDIT_2026-08-09.md','audit/findings/ACTIVE_FINDINGS_2026-08-13.md','audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md','design/audit_impacts/flat-vector-r6-standalone-20261012.json','tools/audit_document_authority.py','tools/audit_development.py','tools/audit_game_2d.py','scripts/ci.sh','project.godot']:
 b=(R/n).read_bytes().replace(b'\r\n',b'\n');required.append({'path':n,'bytes':len(b),'sha256':sha(b),'hash_mode':'Git-export LF text bytes outside literal packet'})
j={'schema':'reef.flat_vector_packet/2','revision':'FV-AUDIT-20261007-R6','repository':'https://github.com/Ebonyks/mermaid-roshan-reef','branch':'codex/flat-vector-r6-20261012','historical_capture_source':SOURCE,'prepared_against_dev':DEV,'packet_files':rows,'payload_file_count':len(rows),'payload_bytes':sum(x['bytes'] for x in rows),'payload_sha256':sha(''.join(x['path']+'\t'+x['sha256']+'\t'+str(x['bytes'])+'\n' for x in rows).encode()),'historical_required_files':list(historical.values()),'immutable_source_files':list(refs.values()),'required_project_files':required,'historical_archive':'ARCHIVE_REFERENCES.json','excluded_post_publication_record':'REMOTE_VERIFICATION.json','acceptance':'NONE;diagnostic inventory only','remote_verification':'Requires exact immutable payload revision and every required byte;receipt published separately'}
(P/'MANIFEST.json').write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');print('MANIFEST',len(rows),'payload files',j['payload_bytes'],'bytes;',len(historical),'historical captures;',len(refs),'immutable sources;',len(required),'project files')
