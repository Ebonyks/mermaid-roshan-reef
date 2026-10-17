from pathlib import Path
import json,hashlib,subprocess,datetime,collections
T=Path.cwd();S=Path(__file__).parent;P=T/'docs/handoffs/codex_flat_vector_art_2026-10-07/r83_touch_flash_runtime';B='dd799b2d43871b29d1d6e0503646308a194dad1e'
def sha(b):return hashlib.sha256(b).hexdigest()
def wr(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
pre=json.loads((S/'SOURCE_PIN.json').read_text(encoding='utf-8'));diff=json.loads((S/'IMPORT_SOURCE_DIFFERENCES.json').read_text(encoding='utf-8'))['changed'];paths=[r['path']for r in diff]
assert paths and all(p.endswith('.import')for p in paths),collections.Counter(Path(p).suffix for p in paths)
data=subprocess.check_output(['git','cat-file','--batch'],input=('\n'.join(B+':'+p for p in paths)+'\n').encode('utf-8'));offset=0;rows=[]
for p in paths:
 end=data.index(b'\n',offset);header=data[offset:end].split();assert header[1]==b'blob';size=int(header[2]);blob=data[end+1:end+1+size];offset=end+1+size+1
 current=(T/p).read_bytes();crlf=blob.replace(b'\r\n',b'\n').replace(b'\n',b'\r\n');before=pre['runtime_hashes'][p]
 assert current==blob,p
 assert sha(crlf)==before and sha(blob)!=before,p
 rows.append({'path':p,'pre_import_raw_sha256':before,'post_import_raw_sha256':sha(current),'git_blob_sha256':sha(blob),'pre_import_equals_exact_git_with_CRLF':True,'post_import_equals_exact_git_blob_LF':True,'semantic_changes':False})
assert offset==len(data)
now={p:sha((T/p).read_bytes())for p in pre['runtime_hashes']};actual=[p for p,v in now.items()if v!=pre['runtime_hashes'][p]];assert sorted(actual)==sorted(paths)
record={'schema':'reef.import_eol_binding/1','baseline':B,'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pre_import_pin_sha256':sha((S/'SOURCE_PIN.json').read_bytes()),'mismatch_count':len(rows),'extensions':dict(collections.Counter(Path(p).suffix for p in paths)),'differences':rows,'all_differences_exact_CRLF_to_LF_only':True,'all_post_import_bytes_exact_baseline_git_blobs':True,'all_other_runtime_raw_bytes_unchanged':True,'failed_native_attempt':'First queue exited in source preflight before job directory creation/Main/Godot launch; zero captures; retained separately.','scope':'Exact raw-byte mapping, not discarded guard failures or accepted visual/runtime/device/child/owner evidence. Original pre-import pin remains immutable. A separate post-import pin binds subsequent native source.'}
wr(S/'IMPORT_EOL_BINDING.json',record);wr(P/'IMPORT_EOL_BINDING.json',record)
post=dict(pre);post.update({'runtime_hashes':now,'pin_kind':'POST_IMPORT_EXACT_RAW_SOURCE','pre_import_pin_sha256':record['pre_import_pin_sha256'],'import_eol_binding_sha256':sha((S/'IMPORT_EOL_BINDING.json').read_bytes()),'known_import_eol_only_paths':paths,'created_at_utc':record['checked_at_utc']});wr(S/'SOURCE_POST_IMPORT_PIN.json',post)
print('R83_IMPORT_BINDING',len(rows),'import sidecars only; exact CRLF-to-LF; all other runtime bytes unchanged; baseline Git content exact')
