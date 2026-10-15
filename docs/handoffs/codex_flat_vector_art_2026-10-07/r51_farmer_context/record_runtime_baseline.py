from pathlib import Path
import os,json,hashlib,subprocess,datetime
R=Path.cwd();P=R/'docs/handoffs/codex_flat_vector_art_2026-10-07/r51_farmer_context';W=Path(r'C:/Users/Peter/.codex/worktrees/flat-vector-dev-context-20261015/mermaid-roshan-reef');S=Path(r'C:/Users/Peter/AppData/Local/Temp/reef-flat-vector-farmer-context-20261015');D='5120b6d59885dd057937aaf284e73681d8eac9f5'
def wr(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
def hashes(path):
 data=path.read_bytes();return hashlib.sha256(data).hexdigest(),hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest(),data
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=W,text=True).strip()==D and not subprocess.check_output(['git','status','--porcelain'],cwd=W,text=True).strip()
roots=['assets','scripts','scenes','shaders','addons','project.godot'];entries=[]
for row in subprocess.check_output(['git','ls-tree','-r','-z',D,'--',*roots],cwd=W).split(b'\0'):
 if row:
  head,path=row.split(b'\t',1);mode,kind,oid=head.decode().split();path=path.decode();f=W/path;digest,blob,b=hashes(f);state='RAW_EXACT'if blob==oid else('NEWLINE_ONLY_EXACT'if hashlib.sha1(b'blob '+str(len(b.replace(b'\r\n',b'\n'))).encode()+b'\0'+b.replace(b'\r\n',b'\n')).hexdigest()==oid else'BYTE_MISMATCH');assert state!='BYTE_MISMATCH',path;entries.append({'path':path,'git_blob':oid,'worktree_sha256':digest,'bytes':len(b),'match':state})
sidecars={}
for root,dirs,files in os.walk(W):
 dirs[:]=[x for x in dirs if x not in {'.git','.godot','__pycache__','.secrets','.aws','.codex','.claude'}]
 for name in files:
  f=Path(root)/name
  if f.suffix in {'.uid','.import'}:sidecars[f.relative_to(W).as_posix()]=hashlib.sha256(f.read_bytes()).hexdigest()
normal=Path(os.environ['APPDATA'])/'Godot/app_userdata/Mermaid Roshan Reef of Light/reef_save.json';normals={x:hashlib.sha256(Path(str(normal)+x).read_bytes()).hexdigest()if Path(str(normal)+x).is_file()else'absent'for x in ['', '.bak','.tmp','.tmp0','.tmp1','.old','.bak.tmp','.bak.old']}
wr(S/'PRE_IMPORT_GUARD.json',{'source_revision':D,'runtime_files':entries,'sidecars':sidecars,'normal_save_hashes':normals,'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
wr(P/'RUNTIME_WORKTREE.json',{'operation_id':'3308e392-eab2-4725-a6f6-54aaf4e1b85d','path':str(W),'source_revision':D,'clean_at_creation':True,'runtime_file_count':len(entries),'raw_exact':sum(x['match']=='RAW_EXACT'for x in entries),'newline_only':sum(x['match']=='NEWLINE_ONLY_EXACT'for x in entries),'sidecar_count_before_initial_import':len(sidecars),'no_other_checkout_modified':True,'scope':'Owned clean managed capture checkout;local staging only. All authoritative exchange output is published on the durable audit branch;no other editor or primary checkout reset.'})
plan=json.loads((P/'PLAN.json').read_text());plan['runtime_worktree_path']=str(W);plan['runtime_worktree_source_verified']=D;wr(P/'PLAN.json',plan)
print('R51_RUNTIME_BASELINE',len(entries),'files',sum(x['match']=='RAW_EXACT'for x in entries),'raw',sum(x['match']=='NEWLINE_ONLY_EXACT'for x in entries),'newline-only',len(sidecars),'sidecars',flush=True)
print('GODOT_RESOLVER',subprocess.check_output(['python','-B','tools/resolve_godot.py'],cwd=W,text=True).strip(),flush=True)
