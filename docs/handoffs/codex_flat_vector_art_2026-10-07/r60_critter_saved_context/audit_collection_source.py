"""Exact AST occurrence/caller evidence; never whole-domain reachability proof."""
from pathlib import Path
from collections import Counter
from lark import Tree,Token
import importlib.util,importlib.metadata,json,subprocess,hashlib
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;D='5120b6d59885dd057937aaf284e73681d8eac9f5'
sp=importlib.util.spec_from_file_location('r57_original_game_facts',H/'r57_catalogue_selector_crosswalk/audit_game_values.py');G=importlib.util.module_from_spec(sp);sp.loader.exec_module(G)
def sha(b):return hashlib.sha256(b).hexdigest()
def wr(n,d):(P/n).write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
def scan():
 paths=[x for x in subprocess.check_output(['git','ls-tree','-r','--name-only',D,'--','scripts','scenes','addons'],cwd=R,text=True).splitlines()if x.endswith('.gd')];files=[];calls=[];symbols=[];functions=[]
 raw=subprocess.check_output(['git','cat-file','--batch'],input=''.join(D+':'+x+'\n'for x in paths).encode(),cwd=R);pos=0
 for path in paths:
  end=raw.index(b'\n',pos);length=int(raw[pos:end].split()[-1]);pos=end+1;b=raw[pos:pos+length];pos+=length+1;sf=G.D.ScriptFacts(b.decode('utf-8-sig'),path,D);files.append({'path':path,'revision':D,'bytes':len(b),'sha256':sha(b),'parse':'PASS','filename_probe':Path(path).name.startswith('probe')});ordinals=Counter()
  def walk(node,method='<top>'):
   if not isinstance(node,Tree):return
   if str(node.data)=='func_def':
    header=next(x for x in node.children if isinstance(x,Tree)and str(x.data)=='func_header');method=str(header.children[0]);excerpt=sf.excerpt(node)
    if any(x in excerpt for x in ['critter_collection','_collection_ref()','_spawn_context(','func _context()']):functions.append({'path':path,'function':method,'line':node.meta.line,'end_line':node.meta.end_line,'sha256':sha(excerpt.encode()),'source_excerpt':excerpt,'whole_source_sha256':sha(b),'filename_probe':Path(path).name.startswith('probe')})
   if str(node.data)in ['standalone_call','getattr_call']:
    name,recv,args,_=G.D.call_parts(node);tokens=[str(x)for x in recv.scan_values(lambda v:isinstance(v,Token))]if isinstance(recv,Tree)else([str(recv)]if recv is not None else[])
    if name in ['_collection_ref','_spawn_context','_catch','_context','open_book','close_book']or '_collection_ref'in tokens:
     ordinals[(method,'call')]+=1;excerpt=sf.excerpt(node);calls.append({'id':'FVCC-'+sha((path+'::'+method+'::call::'+str(ordinals[(method,'call')])).encode())[:12].upper(),'path':path,'function':method,'line':node.meta.line,'end_line':node.meta.end_line,'call_name':name,'receiver_ast':recv.pretty()if isinstance(recv,Tree)else(str(recv)if recv is not None else None),'literal_arguments':[G.D.literal(x)for x in args],'source_excerpt':excerpt,'source_excerpt_sha256':sha(excerpt.encode()),'filename_probe':Path(path).name.startswith('probe'),'dispatch_and_reachability_proved':False})
   for child in node.children:
    if isinstance(child,Token)and str(child)=='critter_collection':symbols.append({'path':path,'function':method,'line':child.line,'token':'critter_collection','filename_probe':Path(path).name.startswith('probe')})
    else:walk(child,method)
  walk(sf.tree)
 assert pos==len(raw)and len(files)==312
 wr('COLLECTION_SOURCE_CENSUS.json',{'source_revision':D,'analyzer_sha256':sha(Path(__file__).read_bytes()),'gdtoolkit_version':importlib.metadata.version('gdtoolkit'),'scope_helper':{'path':(H/'r45_dispatch_semantics_audit/classify_dispatch.py').relative_to(R).as_posix(),'sha256':sha((H/'r45_dispatch_semantics_audit/classify_dispatch.py').read_bytes())},'files':files,'calls':calls,'collection_field_symbol_occurrences':symbols,'functions':functions,'counts':{'files':len(files),'calls':len(calls),'symbols':len(symbols),'functions':len(functions)},'limits':'Syntactic occurrence and original full function context only. Lexical calls can be aliases/overrides; same method spelling is not dispatch. Filename_probe is labeling, not authority. Dynamic/native/escaped-loader/resource/inherited paths remain unresolved. No global absence/unreachability, alias merge, complete current species acquisition or artwork count/acceptance proof.'})
 print('R60_SOURCE_CENSUS',len(files),len(calls),len(symbols),len(functions),flush=True)
if __name__=='__main__':scan()
