from pathlib import Path
import datetime, hashlib, json, shutil, subprocess, sys, time

r = Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
staging = Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/day2_graphics_audit_20260930/tmp')
out = r / 'audit/job_review_v2_20261001/final_native_supplement_gates_v3'
assert out.is_dir() and not (out / 'RECEIPT.json').exists()
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def write(p, d): p.write_text(json.dumps(d, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p): return p.relative_to(r).as_posix()
revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=r, text=True).strip()
assert revision == '56d66f63e375b61cf02936b426a05a2b92c14d3b'
failure = out / 'scope_preparation_attempt01_failure'
failure.mkdir()
write(failure / 'FAILURE.json', dict(status='FAIL_PRESERVED', recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), observed_exception='AssertionError: two authorized existing audit impact modifications omitted from helper exact scope whitelist', omitted_paths=['design/audit_impacts/job-review-current-remote-receipt-20261001.json', 'design/audit_impacts/job-wash-contact-study-20261001.json'], failed_helper=rel(out / 'executed_prepare_and_check_native_supplement_v80.py'), qualification='Observed prior tool result; no fabricated stdout archive. Fresh fetch and source guard had succeeded. No parser/inference/import/authority/development/game2d commands or staging had run. Existing coherent screenshots, license rows and metadata were retained. Diff inspection confirms these two records cover the already authorized C remote receipt and reaching-contact attempt04.'))
shutil.copyfile(Path(__file__), out / 'executed_resume_native_supplement_gates_v81.py')
recordfile = r / 'design/audit_impacts/job-native-final-supplement-gates-20261001.json'
record = read(recordfile)
record['scope'] += ' Preserve failed preparation scope guard and recover by explicitly including the two existing authorized impact records; no source/art/score change in recovery.'
record['files'] = sorted(rel(p) for p in out.rglob('*') if p.is_file()) + ['design/05_DOC_LEDGER.md']
write(recordfile, record)
snapshot = read(r / 'audit/job_review_v2_20261001/full_ci_candidate_retry_v2/SOURCE_BEFORE.json')
assert len(snapshot['source_files']) == 325
before = {x['path']: sha(r / x['path']) for x in snapshot['source_files']}
assert all(before[x['path']] == x['sha256'] for x in snapshot['source_files'])
boundary = read(out / 'SOURCE_AND_BRANCH_BOUNDARY.json')
assert boundary['baseline'] == revision and boundary['all_literal_sources_match_passing_full_suite']
assert (out / 'fetch.stdout.log').is_file() and (out / 'fetch.stderr.log').is_file()
original = (staging / 'prepare_and_check_native_supplement_v80.py').read_text(encoding='utf-8')
suffix = original[original.index("folders=['audit/job_shared_source_native_review_v1_20261001'"):]
suffix = suffix.replace("ids=['job-shared-native-source-review-20261001'", "ids=['job-review-current-remote-receipt-20261001','job-wash-contact-study-20261001','job-shared-native-source-review-20261001'")
suffix = suffix.replace('native_supplement_scope_v80.json', 'native_supplement_scope_v81.json')
exec(compile(suffix, str(out / 'executed_prepare_and_check_native_supplement_v80.py') + ':resumed_suffix_v81', 'exec'))
