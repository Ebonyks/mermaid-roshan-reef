from __future__ import annotations
from pathlib import Path
import copy, datetime, hashlib, json, re

PREP = Path('H:/CodexWorktrees/job-platform-jp1-preparation-20261001')
PROJECT = Path('H:/CodexWorktrees/mermaid-roshan-reef-job-platform-jp1-20261001')
OUT = PREP / 'publish-evidence'
DEST = 'audit/evidence/job-platform-jp1-20261001'
FOCUSED = PREP / 'runtime/evidence'
FIXTURES = PREP / 'fixtures'
BASELOG = Path('H:/CodexWorktrees/job-platform-jp0-evidence-20260930/baseline/probes-ci.log')
REVIEW = Path('C:/Users/Peter/Documents/mermaid-roshan-reef/.scratch/job-platform-jp1-review')
ARTIFACTS = []
PATH_MAP = {}

def sha(data): return hashlib.sha256(data).hexdigest()
def write(rel, data):
    path = OUT / rel
    assert path.resolve().is_relative_to(OUT.resolve())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return path

def register(source, rel, role, normalize=False):
    source = Path(source)
    raw = source.read_bytes()
    data = raw.decode('utf-8-sig').replace('\r\n','\n').replace('\r','\n').encode('utf-8') if normalize else raw
    write(rel, data)
    ARTIFACTS.append({'path': rel, 'role': role, 'raw_sha256': sha(raw), 'published_sha256': sha(data), 'bytes': len(data), 'normalization': 'UTF-8 without BOM; LF line endings only' if normalize else 'NONE: exact bytes'})
    PATH_MAP[str(source).replace('\\','/')] = DEST + '/' + rel
    return rel

def mapped(value):
    if isinstance(value, dict): return {k:mapped(v) for k,v in value.items()}
    if isinstance(value, list): return [mapped(v) for v in value]
    if isinstance(value, str):
        clean = value.replace('\\','/')
        if clean in PATH_MAP: return PATH_MAP[clean]
        if clean == str(PROJECT).replace('\\','/'): return DEST + '/source-snapshot'
    return value

def json_capture(source, rel, role):
    source = Path(source)
    raw_rel = rel.removesuffix('.json') + '.raw.json.txt'
    register(source, raw_rel, role + ' immutable raw capture')
    # Hash-bound references intentionally target the exact raw capture.
    return source, rel, role

OUT.mkdir(parents=True, exist_ok=True)
pending_json = []
register(BASELOG, 'baseline/probes-ci.raw.txt', 'Immutable underlying GitHub Actions log from baseline run36791771742')
base_text = BASELOG.read_text(encoding='utf-8-sig')
for name, marker in [('opera','OPERA|'),('save-recovery','SAVE_RECOVERY|')]:
    rows = [line[line.index(marker):] for line in base_text.splitlines() if marker in line]
    write('baseline/' + name + '.original-verdicts.txt', ('\n'.join(rows)+'\n').encode('utf-8'))
for name in ['cleanup','probe-opera','probe-save-recovery','probe-load']:
    for stream in ['stdout','stderr']:
        source = FOCUSED / (name + '.' + stream + '.log')
        register(source, 'focused/' + name + '.' + stream + '.raw.txt', 'Clean focused native ' + name + ' ' + stream)
        register(source, 'focused/' + name + '.' + stream + '.txt', 'Readable focused native ' + name + ' ' + stream, normalize=True)
for name in ['probe-opera','probe-save-recovery']:
    register(FOCUSED/(name+'.original-verdicts.txt'), 'focused/'+name+'.original-verdicts.txt', 'Original verdict-only comparison text', normalize=True)
for stream in ['stdout','stderr']:
    register(FOCUSED/('opera-cleanup.'+stream+'.log'), 'historical/pre-import/cleanup.'+stream+'.raw.txt', 'FAILED historical pre-import attempt; excluded from acceptance')
register(PREP/'runtime/fixtures/opera_cleanup_probe.gd','fixtures/opera_cleanup_probe.gd.txt','Native completion callback fixture source; .txt is evidence only')
pending_json.append(json_capture(FOCUSED/'JP1_FOCUSED_RECEIPT.json','focused/JP1_FOCUSED_RECEIPT.json','Original48-test focused run receipt'))

source_receipt = json.loads((FOCUSED/'JP1_FOCUSED_RECEIPT.json').read_text())
for rel, expected in source_receipt['source_hashes'].items():
    current = PROJECT/rel
    if sha(current.read_bytes()) != expected:
        candidates = [OUT/'historical/focused48-source'/(rel+'.txt'), OUT/'historical/final49-source'/(rel+'.txt')]
        if rel.endswith('content_source_refs.py'):
            candidates.insert(0,OUT/'historical/content_source_refs_48test_run.py.txt')
        old = next((path for path in candidates if path.exists() and sha(path.read_bytes()) == expected),None)
        assert old is not None,rel
        register(old,'historical/focused48-source/'+rel+'.txt','Exact source used by focused48 test run')
    register(current,'source-snapshot/'+rel+'.txt','Frozen current candidate source snapshot; evidence only')
register(PROJECT/'tools/content_gd_literals.py','source-snapshot/tools/content_gd_literals.py.txt','Frozen current compiler literal/parser dependency')
for relative in ['tools/audit_document_authority.py','tools/tests/test_audit_document_authority.py']:
    register(PROJECT/relative,'source-snapshot/'+relative+'.txt','Frozen planning gate/control dependency used by read-only static preview')
for prefix in ['focused50','planning']:
    for stream in ['stdout','stderr']:
        register(REVIEW/(prefix+'-preview.'+stream+'.raw.txt'),'static-preview/'+prefix+'.'+stream+'.raw.txt','Read-only exact final C helper preview '+prefix+' '+stream)
for file in ['run_test_controls.py','run_planning_controls.py']:
    register(REVIEW/file,'static-preview/'+file+'.txt','Read-only injected final C helper test harness; evidence only')
for leaf in ['content_build','content_source_refs','content_gd_literals']:
    assert (PROJECT/'tools'/(leaf+'.py')).read_bytes() == (REVIEW/'final/after/tools'/(leaf+'.py')).read_bytes(),leaf
assert (PROJECT/'tools/tests/test_content_build.py').read_bytes() == (REVIEW/'tools/tests/test_content_build.py').read_bytes()
planning_preview=(REVIEW/'planning-preview.stdout.raw.txt').read_text(encoding='utf-8-sig')
for relative in ['tools/audit_document_authority.py','tools/tests/test_audit_document_authority.py']:
    assert 'SOURCE|'+(PROJECT/relative).as_posix()+'|'+sha((PROJECT/relative).read_bytes()) in planning_preview,relative
preview={'schema':'reef.jp1-static-preview.v1','mode':'Final C compiler helper modules injected in memory; H catalogue/runtime/authority read-only; only temporary fixture writes. This precedes authorized application and the final normal full50 module run.','compiler_tests':3,'planning_tests':9,'compiler_stdout':DEST+'/static-preview/focused50.stdout.raw.txt','compiler_stderr':DEST+'/static-preview/focused50.stderr.raw.txt','planning_stdout':DEST+'/static-preview/planning.stdout.raw.txt','planning_stderr':DEST+'/static-preview/planning.stderr.raw.txt','source_hashes':{relative:sha((PROJECT/relative).read_bytes()) for relative in ['tools/content_build.py','tools/content_source_refs.py','tools/content_gd_literals.py','tools/tests/test_content_build.py','tools/audit_document_authority.py','tools/tests/test_audit_document_authority.py']},'control_scope':'Three focused compiler tests cover lexical declaration/function/site spoofing, original and migrated checkpoint insertion order, and actual global clamp/loop occurrence guards. Both commissioned count producers reject arithmetic/float/underscore/suffix RHS. Four new DOC072 tests and five neighboring original planning tests preserve fail-closed and stale fact behavior.'}
write('static-preview/RECEIPT.json',(json.dumps(preview,indent=2)+'\n').encode())
register(FIXTURES/'baseline_save_state.source','source-snapshot/baseline-save-state.gd.txt','Exact Git7f068cb8 baseline SaveState source')
register(FIXTURES/'candidate_save_state.source','source-snapshot/native-candidate-save-state.gd.txt','Exact native fixture candidate source')
register(FIXTURES/'probe_jp1_baseline_receipt.gd','fixtures/probe_jp1_baseline_receipt.gd.txt','Uninstrumented native transactional fixture source')
register(FIXTURES/'probe_jp1_raw_clamp.gd','fixtures/probe_jp1_raw_clamp.gd.txt','Separate instrumented supplemental fourth-clamp observer source')

for lane, folder in [('baseline','baseline-native-final-7f068cb8'),('candidate','candidate-native-final'),('synthetic','synthetic-native-final')]:
    source_dir = FIXTURES/folder
    pending_json.append(json_capture(source_dir/'native_receipt.json','native/'+lane+'/native_receipt.json','Final uninstrumented '+lane+' native receipt'))
    for file in sorted(source_dir.glob('*')):
        if file.is_file() and file.name!='native_receipt.json':
            register(file,'native/'+lane+'/saves/'+file.name,'Actual native '+lane+' primary/backup bytes')
    for ext, name in [('.log','stdout'),('.errors.log','stderr')]:
        register(FIXTURES/(folder+ext),'native/'+lane+'/'+name+'.raw.txt','Clean final '+lane+' native '+name)
    pending_json.append(json_capture(FIXTURES/('raw-clamp-'+lane+'.json'),'native/supplemental/raw-clamp-'+lane+'.json','Supplemental instrumented '+lane+' raw-clamp receipt'))
    for ext, name in [('.log','stdout'),('.errors.log','stderr')]:
        register(FIXTURES/('raw-clamp-'+lane+ext),'native/supplemental/raw-clamp-'+lane+'.'+name+'.raw.txt','Clean supplemental '+lane+' '+name)
for file in ['JP1_NATIVE_SAVE_COMPARISON.json','JP1_NATIVE_RAW_CLAMP_COMPARISON.json','baseline_source_receipt.json','synthetic_provider_transform_receipt.json']:
    pending_json.append(json_capture(FIXTURES/file,'native/'+file,'Native source/transform/comparison metadata'))

synthetic = PREP/'compiler/synthetic'
for source in sorted(synthetic.rglob('*')):
    if not source.is_file():continue
    rel=source.relative_to(synthetic).as_posix()
    if rel=='manifest.json':
        pending_json.append(json_capture(source,'synthetic/manifest.json','Synthetic compiler fixture manifest'))
    else:
        register(source,'synthetic/'+rel+('.txt' if rel.endswith('.gd') else ''),'Synthetic compiler input or exact emitted data; no shipping allocation')
register(PROJECT/'build/jp1_native_fixture/synthetic_job_catalog_data.gd','native/synthetic_job_catalog_data.gd.txt','Native synthetic provider; only class_name removal from compiler emission')

# All native receipt source paths are now mapped to durable, hash-bound copies.
for source, rel, role in pending_json:
    raw=source.read_bytes()
    data=(json.dumps(mapped(json.loads(raw)),indent=2,ensure_ascii=False)+'\n').encode('utf-8')
    write(rel,data)
    ARTIFACTS.append({'path':rel,'role':role+' remapped display copy','raw_sha256':sha(raw),'published_sha256':sha(data),'bytes':len(data),'normalization':'JSON pretty print UTF-8/LF; exact absolute artifact paths replaced with eventual publication references; hash-bound references use immutable raw captures'})

historical = {'schema':'reef.jp1-historical-pre-import.v1','result':'FAIL','counts_as_acceptance':False,'process_exit_code':0,'misleading_stdout_marker':'OPERA CLEANUP FIXTURE: PASS','reason':'Fresh worktree lacked asset .import remap sidecars. stderr contains dependent-script preload/parser/compile errors. Exit0 and callback assertions do not establish a clean native run.','stdout':DEST+'/historical/pre-import/cleanup.stdout.raw.txt','stderr':DEST+'/historical/pre-import/cleanup.stderr.raw.txt','resolution':'Root performed a clean exact4.7.2 headless import; final focused cleanup run uses its own clean stdout/stderr artifacts.'}
write('historical/pre-import/RESULT.json',(json.dumps(historical,indent=2)+'\n').encode())

normalization = {'schema':'reef.jp1-evidence-normalization.v1','publication_destination':DEST,'raw_policy':'*.raw.txt and *.raw.json.txt preserve input bytes exactly. Raw JSON captures retain original local execution paths as provenance. Remapped JSON receipts are separate display artifacts. Raw-vs-published hashes are listed per artifact in MANIFEST.json.','text_policy':'Readable .txt log copies change only UTF-8 BOM and newline representation to UTF-8/LF; content and verdict text are preserved. Sources ending .gd.txt/.py.txt are exact source-byte snapshots, not executable project files.','verdict_policy':'From the exact baseline Actions log, keep text beginning at OPERA| or SAVE_RECOVERY|. Strip only the Actions job/step/time prefix. On candidate Opera exclude only OPERA|JP0 proof rows when comparing the167 inherited verdicts. Preserve every remaining byte of verdict text and order; terminate each line with LF. All85 SAVE_RECOVERY verdicts compare in order.','native_policy':'Uninstrumented primary receipts preserve complete serialized strings, key order and actual disk bytes. JSON display formatting does not change embedded serialized strings. Class_name-removal transforms and synthetic preload substitution are explicit in fixture receipts. Supplemental raw-clamp observation inserts one set_meta call in isolated source only, and is separate from the uninstrumented primary lane.','path_policy':'Receipt references are remapped to '+DEST+'; references accompanied by raw SHA256 point to byte-exact raw captures. No ignored build/preparation file is represented as published delivery.','known_existing_behavior':'Unknown numeric arrays serialize as integers on first write and as floats after JSON reread/rewrite. Baseline and candidate agree at both stages; this preexisting conversion is preserved.','historical_policy':'Failed pre-import execution is retained separately and contributes no PASS evidence. Intermediate earlier baseline fixture revisions are not final native acceptance.'}
write('NORMALIZATION_NOTES.json',(json.dumps(normalization,indent=2)+'\n').encode())

attribution={'schema':'reef.jp1-baseline-attribution.v1','repository':'Ebonyks/mermaid-roshan-reef','revision':'7f068cb80766edd52a110cc1cb3958158f829822','ci_run_id':36791771742,'ci_url':'https://github.com/Ebonyks/mermaid-roshan-reef/actions/runs/36791771742','log_step':'probes / Run trusted probes','raw_log':DEST+'/baseline/probes-ci.raw.txt','raw_log_sha256':sha(BASELOG.read_bytes()),'attribution_origin':'Exact immutable baseline and downloaded Actions log supplied/verified in parent JP0 work; reused as underlying baseline, not relabeled as JP1 remote CI.','engine':json.loads((FIXTURES/'JP1_NATIVE_SAVE_COMPARISON.json').read_text())['engine'],'engine_executable_sha256':json.loads((FIXTURES/'JP1_NATIVE_SAVE_COMPARISON.json').read_text())['engine_executable_sha256'],'candidate_source_status':'Focused native candidate source identified by file hashes; no exact-head JP1remote CI or integration claim in this bundle.'}
write('BASELINE_ATTRIBUTION.json',(json.dumps(attribution,indent=2)+'\n').encode())

# Preserve the final50 suite raw output and publish its observed result only after completion.
compiler_log=(OUT/'compiler50.stderr.raw.txt').read_text(encoding='utf-8-sig')
match=re.search(r'Ran 50 tests in ([0-9.]+)s',compiler_log)
if not match or not compiler_log.rstrip().endswith('OK'):raise RuntimeError('Final50 compiler suite is not complete and green')
compiler_receipt={'schema':'reef.jp1-compiler-controls.v1','command':'python -B -m unittest tools.tests.test_content_build','result':'PASS','tests':50,'elapsed_seconds':float(match.group(1)),'focused_new_test':'test_legacy_literal_checkpoint_proof_requires_exact_unconditional_order_and_site','focused_new_test_result':'PASS;1test in0.320s','lexical_control':'test_save_source_proof_ignores_quoted_code_and_rejects_lexical_spoofs','historical49_receipt':DEST+'/historical/COMPILER_CONTROLS_49.json','stdout':DEST+'/compiler50.stdout.raw.txt','stderr':DEST+'/compiler50.stderr.raw.txt','compiler_sha256':sha((PROJECT/'tools/content_build.py').read_bytes()),'resolver_sha256':sha((PROJECT/'tools/content_source_refs.py').read_bytes()),'test_module_sha256':sha((PROJECT/'tools/tests/test_content_build.py').read_bytes()),'historical48_receipt':DEST+'/focused/JP1_FOCUSED_RECEIPT.json','meaningful_controls':'Original fixed literal order/site passes; conditional, swapped, relocated, wrong-validator and duplicate normalization fail. Quoted declaration/function/site spoofing fails; escaped/single/double/triple/prefixed string/comment decoys are ignored, unterminated strings fail. All previous49 controls remain green.'}
write('COMPILER_CONTROLS.json',(json.dumps(compiler_receipt,indent=2)+'\n').encode())
summary={'schema':'reef.jp1-publication-evidence.v1','status':'STAGED_FOR_PARENT_PUBLICATION; not delivered until committed/pushed and remote bytes verified','destination':DEST,'baseline_attribution':DEST+'/BASELINE_ATTRIBUTION.json','focused_receipt':DEST+'/focused/JP1_FOCUSED_RECEIPT.json','native_comparison':DEST+'/native/JP1_NATIVE_SAVE_COMPARISON.json','instrumented_supplement':DEST+'/native/JP1_NATIVE_RAW_CLAMP_COMPARISON.json','compiler_controls':DEST+'/COMPILER_CONTROLS.json','normalization_notes':DEST+'/NORMALIZATION_NOTES.json','historical_failure':DEST+'/historical/pre-import/RESULT.json','observed_results':{'original_opera_verdicts_equal':167,'original_save_recovery_verdicts_equal':85,'cleanup_cases_pass':9,'compiler_controls_pass':50,'uninstrumented_native_checks':{'baseline':196,'candidate':197,'synthetic':226},'serialized_stages_equal':48,'primary_backup_files_equal':36,'supplemental_raw_clamp':{'baseline':262143,'candidate':262143,'synthetic':262144}},'snapshot_notes':'The focused run receipt captured the earlier48-test state and then-open independent native lane. Final50 COMPILER_CONTROLS.json and JP1_NATIVE_SAVE_COMPARISON.json supersede those historical pending fields. Uninstrumented raw native run receipts also retain a candidate_comparison=PENDING capture-time placeholder; the separate final comparison is authoritative. Runtime/generated bytes remained unchanged through strict legacy-literal and lexical resolver controls.','remaining':'Exact-head fullJP1suite, remoteCI, integration, device/child/owner acceptance remain parent-owned independent gates. No production/asset/save fixture acceptance is inferred for the hidden synthetic job.'}
write('EVIDENCE_INDEX.json',(json.dumps(summary,indent=2)+'\n').encode())

files={}
for p in sorted(OUT.rglob('*'), key=lambda path:path.relative_to(OUT).as_posix()):
    if p.is_file() and p.name!='MANIFEST.json':
        rel=p.relative_to(OUT).as_posix()
        data=p.read_bytes()
        files[rel]={'bytes':len(data),'sha256':sha(data)}
payload='\n'.join(rel+'\t'+entry['sha256']+'\t'+str(entry['bytes']) for rel,entry in files.items())+'\n'
manifest={'schema':'reef.jp1-evidence-manifest.v1','publication_destination':DEST,'status':'STAGED_ONLY','created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'payload_sha256':sha(payload.encode()),'payload_algorithm':'SHA256 over sorted UTF-8 lines path<TAB>sha256<TAB>bytes<LF>, excluding MANIFEST.json itself','files':files,'raw_vs_published':ARTIFACTS}
write('MANIFEST.json',(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n').encode())
# Check all remapped references; immutable raw captures intentionally retain local provenance.
missing=[]
for p in OUT.rglob('*.json'):
    text=p.read_text(encoding='utf-8')
    for ref in re.findall(re.escape(DEST)+r'/[^"\n]+',text):
        target=OUT/ref[len(DEST)+1:]
        if not target.exists():missing.append((p.relative_to(OUT).as_posix(),ref))
assert not missing,missing
print(json.dumps({'files':len(files),'bytes':sum(v['bytes'] for v in files.values()),'payload_sha256':manifest['payload_sha256'],'manifest_sha256':sha((OUT/'MANIFEST.json').read_bytes()),'output':str(OUT)},indent=2))
