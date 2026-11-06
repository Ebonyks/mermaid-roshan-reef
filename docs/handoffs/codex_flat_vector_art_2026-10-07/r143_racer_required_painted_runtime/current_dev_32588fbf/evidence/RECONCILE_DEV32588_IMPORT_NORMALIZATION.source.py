from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json,hashlib,subprocess,datetime,sys,re
W=Path.cwd();T=Path(__file__).parent;D=W.parent/'combined_validation_32588fbf';DEV='32588fbfc6daaa0703d9ee95a526016fc995a38b';ART='4b408d0d49ef05c9b852bc02c9d66270ce27bc6b';assert sys.argv[1:] == ['1'],'Supply only the actually observed terminal wrapper exit1; never use for an engine/test exit failure'
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def wr(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
def sha(b):return hashlib.sha256(b).hexdigest()
def fp(p):return sha(p.read_bytes())
def g(*a):return subprocess.check_output(['git','-c','core.safecrlf=false',*a],cwd=W,stderr=subprocess.PIPE)
assert not(D/'RECONCILED_RESULT.json').exists(),'Already reconciled; use its exact recorded source scope'
assert g('rev-parse','HEAD').decode().strip()==DEV and g('rev-parse','MERGE_HEAD').decode().strip()==ART
s=rd(T/'DEV32588_VALIDATION_STATE.json');assert s['stage']=='STOPPED_INSPECT_NO_AUTOMATIC_RESTART'and s['trusted_completed']==82
ob=rd(T/'DEV32588_RACER_IMPORT_NORMALIZATION_OBSERVATION.json');expected=[x['path']for x in ob['rows']];assert len(expected)==11 and all(x['after_equals_index']and x['before_reconstructed_exactly_as_CRLF']and x['after_lf_only']for x in ob['rows'])
import ast
assert sorted(ast.literal_eval(s['error']))==sorted(expected),'Only the exact final raw hash-guard mismatch is eligible; no engine/probe/timeout failure can be reconciled here'
assert not(D/'FINAL_RESULT.json').exists(),'Keep original result naming and provenance distinct'
pin=rd(D/'SOURCE_PIN.json');paths=sorted(pin['runtime_hashes']);assert sorted(set(g('ls-files','-z','--',*pin['roots']).decode().strip('\0').split('\0')))==paths
with ThreadPoolExecutor(max_workers=4)as pool:after=dict(pool.map(lambda rel:(rel,fp(W/rel)),paths))
drift=sorted(p for p in paths if after[p]!=pin['runtime_hashes'][p]);assert drift==sorted(expected)
proof=[]
for rel in drift:
 b=(W/rel).read_bytes();indexed=g('show',':'+rel);parent=g('show',ART+':'+rel)
 assert b==indexed==parent and b'\r\n'not in b and fp(W/rel)==after[rel]
 reconstructed=b.replace(b'\n',b'\r\n');assert sha(reconstructed)==pin['runtime_hashes'][rel]
 proof.append(dict(path=rel,before_sha256=pin['runtime_hashes'][rel],after_sha256=after[rel],staged_Git_sha256=sha(indexed),parent_revision=ART,parent_Git_sha256=sha(parent),before_reconstructed_exactly_from_after_by_LF_to_CRLF=True,all_settings_bytes_identical_after_canonical_text_normalization=True,settings_waiver=False))
assert fp(W/'scripts/ci.sh')==pin['ci_sha256']
normal=rd(T/'NORMAL_SAVE_PIN.json');current={k:fp(Path(normal['normal_base']+k))if Path(normal['normal_base']+k).is_file()else'absent'for k in normal['hashes']};assert current==normal['hashes']==pin['normal_before']
progress=rd(D/'RESULTS_PROGRESS.json');assert progress['completed']==progress['passed_exits']==82;results=progress['results'];ci=(W/'scripts/ci.sh').read_text(encoding='utf-8');names=re.search(r'for p in (.*?); do',ci).group(1).split();assert len(names)==82 and[n['probe']for n in results]==names
failure=re.search(r"^FAILURE_RE='(.*?)'",ci,re.M).group(1);runtime=re.search(r"^RUNTIME_ERROR_RE='(.*?)'",ci,re.M).group(1)
steps=[rd(D/n/'RESULT.json')for n in ['static','mcp_scope','mcp_inactive','parser','inference','game2d']]
focused=[]
for name in ['probe_racer_integration','probe_reef_kart_pc','probe_reef_kart_handling','probe_bubble_duel_cast','probe_bubble_duel_dual_active','probe_bubble_duel_stress']:
 row=rd(D/name/'RESULT.json');row['probe']=name;focused.append(row)
analyzers=[]
for folder in sorted(D.glob('analyzer_*')):
 row=rd(folder/'RESULT.json');row['script']=row['command'][-1].removeprefix('res://');analyzers.append(row)
assert len(analyzers)==23
for row in results+steps+focused+analyzers:
 assert row['passed']and row['exit_code']==0 and fp(D/row['log_path'])==row['log_sha256']
 if row in results+focused+analyzers or row['label']=='MCP_NO_DEBUGGER_LIFECYCLE':
  text=(D/row['log_path']).read_text(encoding='utf-8',errors='replace');assert text.strip()and not re.search(failure+'|'+runtime,text),row['label']
assert 'R143_DEV32588_CURRENT_STATIC_PREFIX_ALL_OK'in(D/'static/engine.log').read_text(encoding='utf-8',errors='replace')
for row in results:
 expected_flag='--hybrid-touch-test'if row['probe']in ['probe_passive','probe_touch_router','probe_touch_stress','probe_interaction','probe_touch_adversary']else'--classic-touch-test';assert row['command'][-3:]==['--','--touch',expected_flag]
wr(D/'ORIGINAL_RUNNER_FINAL_GUARD_FAILURE.json',dict(state=s,observed_wrapper_exit_code=1,session=69284,scope='Preserved original wrapper rejection after82healthy actual-zero trusted commands and final2D. This file never relabels that wrapper outcome or a failed engine/timeout.',original_runner_sha256=fp(T/'VALIDATE_DEV32588_COMBINED.py')))
wr(D/'CANONICAL_SOURCE_PIN_RECONCILIATION.json',dict(state='EXACT11_IMPORTER_CRLF_TO_LF_NORMALIZATIONS_ONLY_ALL_OTHER_RAW_HASHES_UNCHANGED',original_source_pin_sha256=fp(D/'SOURCE_PIN.json'),runtime_input_count=len(paths),physical_runtime_drift=drift,exact_normalizations=proof,after_runtime_hashes=after,unexplained_runtime_drift=[],normal_11_hashes_unchanged=True,source_settings_changed=False,PNG_or_script_changes=False,guard_or_validator_modified=False,engine_tests_restarted=False,formal_QA11=None,at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))
wr(D/'RECONCILED_RESULT.json',dict(state='PASS_CURRENT_DEV32588_COMBINATION_WITH_EXACT_IMPORT_TEXT_NORMALIZATION',derived_summary=True,derivation='RECONCILE_DEV32588_IMPORT_NORMALIZATION.py reads retained per-command results/logs and original pins; it does not rerun or modify any existing test, source, pin or raw outcome.',head=DEV,incoming_Dev=DEV,merged_source=ART,trusted_command_count=82,passed_exit_count=82,assertion_probe_count=81,headless_capture_skip_count=1,results=results,steps=steps,focused=focused,analyzers=analyzers,source_pin_sha256=fp(D/'SOURCE_PIN.json'),reconciliation_sha256=fp(D/'CANONICAL_SOURCE_PIN_RECONCILIATION.json'),runtime_input_count=len(paths),runtime_drift=drift,unexplained_runtime_drift=[],documented_import_text_normalizations=11,normal_unchanged=True,normal_before=normal['hashes'],normal_after=current,original_flags_order_and_classifiers=True,strict_actual_zero_exit=True,timeout_verdict_acceptance=False,original_wrapper_terminal_exit=1,original_wrapper_failure_preserved='ORIGINAL_RUNNER_FINAL_GUARD_FAILURE.json',new_native_frames=0,formal_QA11=None,device=None,child=None,owner=None,Dev_integrated=False,accepted_removed=0,completed_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))
wr(T/'DEV32588_NORMALIZATION_RECONCILIATION_STATE.json',dict(state='EXACT_IMPORT_TEXT_NORMALIZATION_RECONCILED_NO_ENGINE_REPLAY',result=str(D/'RECONCILED_RESULT.json'),raw_wrapper_exit=1,actual_trusted_zero_exits=82,normalizations=11,unexplained_drift=0,actual_normal_hashes_unchanged=True));print('EXACT11_IMPORT_NORMALIZATION_RECONCILED_82_STRICT_ENGINE_EXITS',flush=True)
