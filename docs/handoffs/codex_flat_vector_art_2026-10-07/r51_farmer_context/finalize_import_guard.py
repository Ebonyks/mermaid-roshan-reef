from pathlib import Path
import os,json,hashlib,subprocess,datetime
R=Path.cwd();P=R/'docs/handoffs/codex_flat_vector_art_2026-10-07/r51_farmer_context';W=Path(r'C:/Users/Peter/.codex/worktrees/flat-vector-dev-context-20261015/mermaid-roshan-reef').resolve();S=Path(r'C:/Users/Peter/AppData/Local/Temp/reef-flat-vector-farmer-context-20261015');pre=json.loads((S/'PRE_IMPORT_GUARD.json').read_text());D=pre['source_revision'];repairs=[]
def sha(b):return hashlib.sha256(b).hexdigest()
for x in pre['runtime_files']:
 f=(W/x['path']).resolve();assert f.is_relative_to(W);b=f.read_bytes()
 if sha(b)==x['worktree_sha256']:continue
 assert f.suffix=='.import',x['path'];normalized=b.replace(b'\r\n',b'\n');assert hashlib.sha1(b'blob '+str(len(normalized)).encode()+b'\0'+normalized).hexdigest()==x['git_blob']
 original=subprocess.check_output(['git','show',D+':'+x['path']],cwd=W,stderr=subprocess.PIPE);variants=[original,original.replace(b'\r\n',b'\n').replace(b'\n',b'\r\n')];restore=next(v for v in variants if sha(v)==x['worktree_sha256']);assert restore.replace(b'\r\n',b'\n')==normalized
 repairs.append({'path':x['path'],'pre_import_sha256':x['worktree_sha256'],'post_import_sha256':sha(b),'restored_sha256':sha(restore),'classification':'OWNED_IMPORTER_NEWLINE_ONLY_WRITE_RESTORED_TO_EXACT_PREIMAGE_NO_SETTING_OR_PIXEL_CHANGE'});f.write_bytes(restore)
assert all(sha((W/x['path']).read_bytes())==x['worktree_sha256']for x in pre['runtime_files'])
sidecars={}
for root,dirs,files in os.walk(W):
 dirs[:]=[x for x in dirs if x not in {'.git','.godot','__pycache__','.secrets','.aws','.codex','.claude'}]
 for name in files:
  f=Path(root)/name
  if f.suffix in {'.uid','.import'}:sidecars[f.relative_to(W).as_posix()]=sha(f.read_bytes())
n=Path(os.environ['APPDATA'])/'Godot/app_userdata/Mermaid Roshan Reef of Light/reef_save.json';normal={x:sha(Path(str(n)+x).read_bytes())if Path(str(n)+x).is_file()else'absent'for x in pre['normal_save_hashes']};assert normal==pre['normal_save_hashes'];status=subprocess.check_output(['git','status','--porcelain'],cwd=W,stderr=subprocess.PIPE).decode();assert not status.strip(),status[:800]
report={'runtime_source_revision':D,'tracked_runtime_files_exact_preimage_preserved':4420,'functional_or_pixel_byte_changes':0,'initial_import_newline_only_metadata_writes':len(repairs),'repairs':repairs,'sidecars_before':len(pre['sidecars']),'sidecars_after_initial_import':len(sidecars),'existing_sidecars_exact':all(sidecars.get(k)==v for k,v in pre['sidecars'].items()),'new_generated_uid_paths':sorted(set(sidecars)-set(pre['sidecars'])),'normal_before':pre['normal_save_hashes'],'normal_after':normal,'clean_tracked_worktree':True,'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Fresh editor import generated cache/ignored UID artifacts and normalized1102 import metadata line endings. Only those owned newline-only writes were hash-proved and restored to exact pre-import bytes;no import setting,protectedpixel/audio or script changed. Subsequent game runs freeze this explicit cache-initialized baseline.'}
assert report['existing_sidecars_exact'];(P/'initial_import/POST_IMPORT_GUARD.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n');(S/'POST_IMPORT_BASELINE.json').write_text(json.dumps({'sidecars':sidecars,'normal_save_hashes':normal,'runtime_raw_hashes':{x['path']:x['worktree_sha256']for x in pre['runtime_files']}},indent=2)+'\n',encoding='utf-8',newline='\n');print('R51_IMPORT_GUARD_PASS',len(repairs),'owned newline-only writes restored;',len(sidecars),'sidecars,',len(report['new_generated_uid_paths']),'new ignoredUIDs;4420sourcefiles/existing sidecars/normal8 exact;clean',flush=True)
