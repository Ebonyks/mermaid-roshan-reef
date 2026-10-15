from pathlib import Path
import json,subprocess,os,sys
sys.stdout.reconfigure(encoding='utf-8');S=Path(r'C:/Users/Peter/AppData/Local/Temp/reef-flat-vector-display-entry-20261015');P=Path.cwd()/'docs/handoffs/codex_flat_vector_art_2026-10-07/r66_display_entry_context'
for mode,width in [('missing',1600),('dayone',1280),('dayone',1600),('newgame',1600),('legacy',1600)]:
 env=dict(os.environ,R66_TEST_MODE=mode,R66_TEST_WIDTH=str(width),R66_TEST_ATTEMPT='1');q=subprocess.run(['python','-B',str(S/'run_native.py')],env=env)
 status='PASS'if q.returncode==0 else'FAIL'
 if q.returncode:
  folder=P/'native'/('attempt1_'+mode+'_'+str(width));m=json.loads((folder/'capture_manifest.json').read_text(encoding='utf-8'));result=json.loads((folder/'RESULT.json').read_text(encoding='utf-8'));failed=[x['label']for x in m['checks']if not x['pass']]
  if mode=='legacy'and result['exit_code']==1 and m['errors']==failed==['legacy Continue remains outside DayOne and no opening movie']and not result['timed_out']and not result['script_or_shader_errors']and not result['source_byte_changes']and result['sidecars_exact']and result['normal_before']==result['normal_after']and result['fixture_dependencies_unchanged']:
   status='SOURCE_POLICY_FAILURE_RETAINED_EXCLUDED_NOT_PASS'
  else:sys.exit(q.returncode)
 print('R66_MATRIX_TERMINAL',mode,width,status,flush=True)
