from pathlib import Path
import os,subprocess,json,sys
sys.stdout.reconfigure(encoding='utf-8');S=Path(r'C:/Users/Peter/AppData/Local/Temp/reef-flat-vector-wardrobe-material-reuse-20261015')
for unlocked,width,teardown in [(False,1600,False),(True,1280,False),(True,1600,False),(False,1280,True)]:
 env=dict(os.environ,R64_TEST_CANDIDATE='true',R64_TEST_UNLOCKED=str(unlocked).lower(),R64_TEST_WIDTH=str(width),R64_TEST_ATTEMPT='1',R64_TEST_TEARDOWN=str(teardown).lower());q=subprocess.run(['python','-B',str(S/'run_native.py')],env=env)
 print('R64_REMAINING_CASE_TERMINAL',unlocked,width,teardown,q.returncode,flush=True)
 if q.returncode:sys.exit(q.returncode)
