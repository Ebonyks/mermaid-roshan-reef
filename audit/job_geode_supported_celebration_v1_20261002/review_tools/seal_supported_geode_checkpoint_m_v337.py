from pathlib import Path
import datetime,hashlib,json,shutil,subprocess,sys
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');f=b/'audit/job_geode_supported_celebration_v1_20261002';contact=b/'assets_src/imagegen/geologist_geode_contact_v1_20261002'
out=b/'tmp/supported_geode_checkpoint_m_seal_v337';out.mkdir(exist_ok=False)
baseline='bc2d14160a3f532895ed95c5db646e8cf0b451ad';mp='audit/job_review_v2_20261001/GEOLOGY_SUPPORTED_GEODE_SUPPLEMENT_FILES_V11.json';prior='audit/job_review_v2_20261001/GEOLOGY_GEODE_ROUTE_EMBLEM_SUPPLEMENT_FILES_V10.json'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def git(*args,input=None):return subprocess.run(['git',*args],cwd=b,input=input,capture_output=True,check=True).stdout
sha=lambda raw:hashlib.sha256(raw).hexdigest()
assert git('rev-parse','HEAD').decode().strip()==baseline and git('branch','--show-current').decode().strip()=='codex/job-art-review-v2-20261001'
assert not git('diff','--cached','--name-only').strip(),'Do not absorb unrelated staged work.'
ci=read(f/'full_ci_v3/RECEIPT.json');assert ci['status']=='PASS_UNMODIFIED_CURRENT_FULL_SUITE' and ci['source_unchanged'] and len(ci['source_checks'])==377 and len(ci['probe_results'])==82 and all(x['process_exit']==0 for x in ci['probe_results'])
assert all(sha((b/x['path']).read_bytes())==x['before_sha256'] for x in ci['source_checks'])
for label in ['parserv2','inferencev2','importartv2','contractv2','capture1280v2','capture1600v2','analyzerv3','audit2dv3']:
 assert read(f/f'runtime_gate/{label}.receipt.json')['status']=='PASS',label
target=f/'review_tools'/Path(__file__).name;shutil.copyfile(__file__,target)
ipaths=[b/'design/audit_impacts'/name for name in ['job-geode-supported-celebration-20261002.json','job-geode-contact-source-20261002.json']]
bridge=f/'PUBLICATION_SOURCE_NEWLINE_BRIDGE_FINAL_V337.json';write(bridge,{'status':'EXACT_STAGED_SOURCE_BRIDGE_PREPARED'})
write(b/mp,{'status':'SCOPED_MANIFEST_PREPARED'})
d=read(ipaths[0]);d['files']=sorted(set(d['files'])|{mp,target.relative_to(b).as_posix(),bridge.relative_to(b).as_posix()}|{x.relative_to(b).as_posix() for x in f.rglob('*') if x.is_file()});write(ipaths[0],d)
for label in ['authorityv5','developmentv5']:
 p=subprocess.run([sys.executable,'-X','utf8','-B',str(f/'review_tools/run_supported_geode_gates_v322.py'),label],cwd=b,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
 (out/(label+'.stdout.log')).write_bytes(p.stdout);(out/(label+'.stderr.log')).write_bytes(p.stderr);print(p.stdout.decode().strip(),flush=True);assert p.returncode==0
scope=set().union(*(set(read(p)['files'])|{p.relative_to(b).as_posix()} for p in ipaths))
for path in scope:
 assert (b/path).resolve().is_relative_to(b.resolve()) and (b/path).is_file(),path
 assert not path.startswith(('.git/','.secrets/','.codex/','.claude/','.github/')),path
paths=''.join(p+'\0' for p in sorted(scope)).encode();git('add','-f','--pathspec-from-file=-','--pathspec-file-nul',input=paths);git('add','--renormalize','-f','--pathspec-from-file=-','--pathspec-file-nul',input=paths)
source_checks=[]
for x in ci['source_checks']:
 raw=(b/x['path']).read_bytes();staged=git('show',':'+x['path']);text=Path(x['path']).suffix.lower() in {'.gd','.godot','.import','.json','.tres','.tscn','.sh','.py'}
 normal=lambda data:data.replace(b'\r\n',b'\n') if text else data
 assert normal(raw)==normal(staged),x['path']
 source_checks.append({'path':x['path'],'literal_local_sha256':sha(raw),'exact_git_blob_sha256':sha(staged),'bytes_git':len(staged),'declared_text_newline_comparison':text,'literal_bytes_match':raw==staged,'canonical_equivalence':True})
write(bridge,{'status':'PASS_ALL377_STAGED_SOURCE_EQUIVALENCE','source_count':377,'checks':source_checks,'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'qualification':'Original full-CI hashes remain literal frozen Windows checkout bytes. Ordinary declared source text may store LF in Git; only CRLF-to-LF comparison is allowed, never binary image/audio changes. Remote checks verify the exact Git blob bytes listed here. This is source equivalence, not a hosted probe result or visual acceptance.'});git('add','-f','--',bridge.relative_to(b).as_posix())
changed={p.decode() for p in git('diff','--cached','--name-only','-z').split(b'\0') if p};assert changed<=scope and mp in changed
def blobs(ref,paths):
 data=git('cat-file','--batch',input=''.join(ref+':'+p+'\n' for p in paths).encode());off=0;result={}
 for p in paths:
  end=data.index(b'\n',off);header=data[off:end].split();assert header[1]==b'blob',p;n=int(header[2]);off=end+1;raw=data[off:off+n];off+=n+1;result[p]=[n,sha(raw)]
 assert off==len(data);return result
files=blobs('',sorted(changed-{mp}))
for folder in [f,contact]:
 for p in folder.rglob('*'):
  path=p.relative_to(b).as_posix()
  if p.is_file() and path in files:assert files[path]==[p.stat().st_size,sha(p.read_bytes())],path
for name in ['stdout','stderr']:assert files[f.relative_to(b).as_posix()+'/full_ci_v3/'+name+'.log'][1]==ci[name+'_sha256']
rawprior=git('show','HEAD:'+prior);old=json.loads(rawprior);refs=set(old['files'])|set(old.get('unchanged_required_files',{}))|{prior}
registry=read(b/'audit/job_artwork_refinement_live/ALL_ITEMS.json');assert len(registry['items'])==1729
for item in registry['items']:
 refs.add(item['image_path']);refs.update(p.split('#')[0] for p in item['original_reports'])
refs.update(x['path'] for x in source_checks);refs-=set(files);refs.discard(mp)
for p in refs:assert not p.startswith(('.secrets/','.git/','.codex/','.claude/')),p
unchanged=blobs('HEAD',sorted(refs))
formula=''.join(p+'\t'+str(v[0])+'\t'+v[1]+'\n' for p,v in sorted(files.items())).encode()
m={'schema':'reef.immutable-review-supplement.v1','base_revision':baseline,'prior_closed_map':prior,'prior_closed_map_sha256':sha(rawprior),'required_files':len(files),'required_payload_bytes':sum(x[0] for x in files.values()),'payload_sha256':sha(formula),'payload_hash_formula':'SHA256 UTF8 sorted path TAB bytes TAB SHA256 LF','files':files,'required_unchanged_files':len(unchanged),'unchanged_required_files':unchanged,'qualification':'Reversible supported Geologist celebration: crystals stay rooted inside both halves; unchanged painting mounted on the same painted slab without generic prop bounce. Supported specimen/slab4.5 provisional, material4.6; whole stage4.1/room2.8/contact2.7/clearing3.9/pan3.8/caption4.0/native background coverage remain open. All58 current selected stills/316 opening-celebration-real-return frames/37 boards/eight native details/25 individual opinions directly inspected at1280/1600 against375 unchanged rendered sources. Broader room-prop trial rejected for duplicate invitations/actor overlap; only four trial views directly reviewed. Separate new contact A1 pose4.3/scale4.1/far reach4.3 rejected; regenerated A2 static pose4.5/material4.6 provisional and UNBOUND, no current game/action improvement. V33 known1729 entries/1247 sources/328 pose cells/50 runtime regions/104 source regions;678 source/cell/region inclusive priorities/385 source reviews unassigned/four additional mounted priorities, not weak-live-object counts or exhaustive use. Full suite2 stopped before gameplay probes at a tracked valid WebP false-positive; failure/raw evidence preserved. Scanner requires a credible XML document prefix, retains disguised actual models, no debt-ceiling/manifest/gameplay-probe waiver. Focused negative baseline fails and repaired tests pass. Corrected officialGodot4.7.2 unmodified local suite3 passes82/82 on377 unchanged frozen local files; exact staged Git source equivalence and raw streams checked separately; raw engine diagnostics retained. Prior complete2074-frame dated WASH review preserved; no current washing repair. Anonymous verification includes every changed payload, priorL packet/references, current register source previews/report entries and all377 exact canonical Git source bytes. No finding closure, whole-job/device/child/owner/integration/release acceptance.'}
write(b/mp,m);git('add','-f','--',mp);raw=git('show',':'+mp);assert {x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x}==set(files)|{mp}
seal={'status':'EXACT_SCOPED_M_BLOBS_SEALED','base_revision':baseline,'map_path':mp,'map_sha256':sha(raw),'payload_sha256':m['payload_sha256'],'payload_files':len(files),'payload_bytes':m['required_payload_bytes'],'unchanged_required_files':len(unchanged),'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'qualification':'Exact scoped topic candidate; publication repeats staged-blob/377-source/82-probe checks and anonymously verifies all immutable remote payload and required reference bytes.'}
write(b/'tmp/supported_geode_checkpoint_m_sealed.json',seal);write(out/'RECEIPT.json',seal);print(json.dumps(seal),flush=True)
