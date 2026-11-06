from pathlib import Path
import subprocess,json,hashlib,datetime,sys
W=Path.cwd();T=Path(__file__).parent;F='docs/handoffs/codex_flat_vector_art_2026-10-07/r143_racer_required_painted_runtime';DEV='32588fbfc6daaa0703d9ee95a526016fc995a38b';ART='4b408d0d49ef05c9b852bc02c9d66270ce27bc6b';R=W/F/'current_dev_32588fbf/evidence'
def g(*a,input=None):return subprocess.check_output(['git','-c','core.longpaths=true','-c','core.safecrlf=false',*a],input=input,stderr=subprocess.PIPE)
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def wr(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
assert not(T/'TESTED_DEV32588_CHECKPOINT.json').exists(),'Already committed; use recorded handle'
assert g('rev-parse','HEAD').decode().strip()==DEV and g('rev-parse','MERGE_HEAD').decode().strip()==ART
assert g('branch','--show-current').decode().strip()=='codex/flat-vector-racer-dev-integration-20261105'
assert not g('diff','--name-only','--diff-filter=U').strip()and not g('diff','--name-only').strip()
r=rd(R/'RECONCILED_RESULT.json');assert r['state']=='PASS_CURRENT_DEV32588_COMBINATION_WITH_EXACT_IMPORT_TEXT_NORMALIZATION'and r['passed_exit_count']==82 and r['assertion_probe_count']==81 and r['headless_capture_skip_count']==1 and r['normal_unchanged']and not r['unexplained_runtime_drift']and r['documented_import_text_normalizations']==11 and r['original_wrapper_terminal_exit']==1 and r['strict_actual_zero_exit']
assert r['head']==DEV and r['incoming_Dev']==DEV and r['merged_source']==ART and len(r['focused'])==6
assert sha(R/'SOURCE_PIN.json')==r['source_pin_sha256']
assert sha(R/'CANONICAL_SOURCE_PIN_RECONCILIATION.json')==r['reconciliation_sha256']and len(r['runtime_drift'])==11
for row in r['results']+r['steps']+r['focused']+r['analyzers']:assert row['passed']and row['exit_code']==0 and sha(R/row['log_path'])==row['log_sha256']
meta=rd(T/'METADATA_CURRENT_PROOF.json');tree=g('write-tree').decode().strip();assert meta['state']=='ALL_CURRENT_METADATA_GATES_PASS'and meta['baseline']==DEV and meta['staged_tree']==tree
for row in meta['results']:assert row['exit_code']==0 and row['baseline']==DEV and row['staged_tree']==tree and sha(Path(row['actual_log']))==row['log_sha256']
m=rd(W/F/'MANIFEST.json');assert m['delivery_diff_base']==DEV and m['prior_verified_artifact_revision']==ART
index={}
for raw in g('ls-files','-s','-z').split(b'\0'):
 if not raw:continue
 head,path=raw.split(b'\t',1);mode,oid,stage=head.split();assert stage==b'0';index[path.decode()]=oid.decode()
ids=sorted(set(index[x['path']]for x in m['files']));raw=g('cat-file','--batch',input=('\n'.join(ids)+'\n').encode());pos=0;blobs={}
for oid in ids:
 end=raw.index(b'\n',pos);h=raw[pos:end].decode().split();assert h[:2]==[oid,'blob'];n=int(h[2]);b=raw[end+1:end+1+n];assert raw[end+1+n:end+2+n]==b'\n';pos=end+2+n;blobs[oid]=(len(b),hashlib.sha256(b).hexdigest())
assert pos==len(raw)
for x in m['files']:assert blobs[index[x['path']]]==(x['bytes'],x['sha256']),x['path']
changed=set(g('diff','--cached','--name-only',DEV).decode().splitlines());assert changed=={x['path']for x in m['files']}|{F+'/MANIFEST.json'}
roots=['scripts','assets','scenes','shaders','addons','project.godot','export_presets.cfg']
racer=g('diff','--name-only','bc02217f087b80884e07acf0cd6ea1e0789ce3a9',ART,'--',*roots).decode().splitlines()
assert len(racer)==87
for rel in racer:assert g('show',':'+rel)==g('show',ART+':'+rel),'Racer parent drift: '+rel
bubble=g('diff','--name-only','bc02217f087b80884e07acf0cd6ea1e0789ce3a9',DEV,'--',*roots).decode().splitlines();assert len(bubble)==11 and not set(bubble).intersection(racer)
for rel in bubble:assert g('show',':'+rel)==g('show',DEV+':'+rel),'Bubble parent drift: '+rel
assert g('diff','--cached','--name-only',DEV,'--',*roots).decode().splitlines()==racer
for rel,expected in [('scripts/racer/reef_kart_race.gd','736c32c3158abcc958d6c58eb13c949f5bbabef9f5a3dbd714044242bc5bbbd5'),('assets/racer/context_v2/item_capsule.png','5b356f6adb1822859b8b9db62d7b0780ce90d1b650c27470fc3e33cb128cd635'),('assets/racer/context_v2/kelp_trap.png','7a9e0b17c5282f516666e3bfce12dcf75e244aec89bb37bf6b791b3200700795'),(F+'/capture_context.gd','e2209b46299a2e8e161465d5ea9bd62ad9a762263c137c458feefef3a2bbbf71')]:
 actual=(W/rel).read_bytes();staged=g('show',':'+rel)
 if rel=='scripts/racer/reef_kart_race.gd':
  tested=rd(R/'SOURCE_PIN.json')['runtime_hashes'][rel]
  assert hashlib.sha256(actual).hexdigest()==tested and actual.replace(b'\r\n',b'\n')==staged and hashlib.sha256(staged).hexdigest()==expected,rel
  assert rd(R/'COMMIT_CONTROLLER_TEXT_IDENTITY.json')['tested_before_and_after_raw_sha256']==tested
 else:assert sha(W/rel)==expected and staged==actual,rel
sys.path.insert(0,str(W));from tools import record_owner_decision as intake
before=json.loads(g('show',DEV+':design/reference/owner_decisions.json'));after=rd(W/'design/reference/owner_decisions.json');assert not intake.append_only_issues(before,after)
assert len(before['decisions'])==122 and len(after['decisions'])==125
normal=rd(T/'NORMAL_SAVE_PIN.json');assert {k:sha(Path(normal['normal_base']+k))if Path(normal['normal_base']+k).is_file()else'absent'for k in normal['hashes']}==normal['hashes']
assert not(W/'export/flat_vector_r143/capture_context.gd').exists()
subprocess.run(['git','-c','core.safecrlf=false','commit','-m','Integrate painted Racer resources with current two-player Dev'],capture_output=True,check=True)
revision=g('rev-parse','HEAD').decode().strip();parents=g('show','-s','--format=%P','HEAD').decode().strip().split();assert parents==[DEV,ART]
wr(T/'TESTED_DEV32588_CHECKPOINT.json',dict(state='LOCALLY_VALIDATED_CURRENT_COMBINATION_NOT_PUBLISHED',revision=revision,parents=parents,manifest_sha256=sha(W/F/'MANIFEST.json'),required_manifest_files=len(m['files'])+1,command_exits=82,assertion_probes=81,capture_skip=1,focused=len(r['focused']),analyzers=len(r['analyzers']),runtime_input_count=r['runtime_input_count'],staged_tree=tree,Dev_mutated=False,source_pushed=False,at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()));print('CURRENT_COMBINED_LOCAL_CHECKPOINT',revision,flush=True)
