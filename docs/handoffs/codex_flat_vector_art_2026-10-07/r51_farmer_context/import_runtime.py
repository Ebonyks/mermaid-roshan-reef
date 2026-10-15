from pathlib import Path
import subprocess,json,datetime,hashlib,os,re
R=Path.cwd();P=R/'docs/handoffs/codex_flat_vector_art_2026-10-07/r51_farmer_context';W=Path(r'C:/Users/Peter/.codex/worktrees/flat-vector-dev-context-20261015/mermaid-roshan-reef');S=Path(r'C:/Users/Peter/AppData/Local/Temp/reef-flat-vector-farmer-context-20261015');G=r'C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe'
def wr(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
job=P/'initial_import';job.mkdir();version=subprocess.check_output([G,'--version'],text=True).strip();assert version=='4.7.2.stable.official.ed1daf0bf',version
cmd=[G,'--headless','--path',str(W),'--editor','--import','--verbose'];wr(job/'LAUNCH.json',{'command':cmd,'engine_version':version,'runtime_source_revision':'5120b6d59885dd057937aaf284e73681d8eac9f5','started_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Initial fresh owned-worktree import/cache construction only;no Main scene/game instance,art,route or performance acceptance.'})
try:
 with(job/'import.log').open('wb')as out:q=subprocess.run(cmd,cwd=W,stdout=out,stderr=subprocess.STDOUT,timeout=190,creationflags=0x08000000)
 result={'exit_code':q.returncode,'timed_out':False}
except subprocess.TimeoutExpired:result={'exit_code':None,'timed_out':True,'scope':'Only the owned importer subprocess timed out;last verbose importing-file line retained for diagnosis.'}
raw=(job/'import.log').read_bytes();result.update(checked_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),log_sha256=hashlib.sha256(raw).hexdigest(),log_bytes=len(raw),script_or_shader_errors=bool(re.search(rb'SCRIPT ERROR|SHADER ERROR|(?m:^ERROR:)',raw)));wr(job/'RESULT.json',result);print('R51_INITIAL_IMPORT',result,raw.decode(errors='replace')[-1800:],flush=True)
assert result['exit_code']==0 and not result['timed_out'] and not result['script_or_shader_errors']
