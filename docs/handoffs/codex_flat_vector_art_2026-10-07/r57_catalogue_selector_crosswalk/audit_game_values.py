"""AST source facts for the Main game field; never normal-route or artwork proof."""
from pathlib import Path
from collections import Counter
import json,hashlib,subprocess,importlib.util,importlib.metadata
from lark import Tree,Token
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;REV='5120b6d59885dd057937aaf284e73681d8eac9f5'
spec=importlib.util.spec_from_file_location('dispatch45_immutable',H/'r45_dispatch_semantics_audit/classify_dispatch.py');D=importlib.util.module_from_spec(spec);spec.loader.exec_module(D)
def sha(b):return hashlib.sha256(b).hexdigest()
def wr(name,d):(P/name).write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
class Facts:
 def __init__(self,text,path,revision=REV):
  self.sf=D.ScriptFacts(text,path,revision);self.rows=[];self.ordinal=Counter();self.walk(self.sf.tree,'<top>',self.sf.root_class,self.sf.root_class)
 def owner(self,lhs,scope,line,klass):
  lhs=D.unwrap(lhs)
  if isinstance(lhs,Token):
   decls=self.sf.lookup(scope,str(lhs),line)
   if self.sf.global_name=='ReefMain' and klass==self.sf.root_class and decls and all(d['scope']==self.sf.root_class and d['kind'].startswith('class_var_') for d in decls):return 'MAIN_CLASS_FIELD'
   return 'LOCAL_SHADOW_OR_OTHER_CLASS'
  if isinstance(lhs,Tree)and str(lhs.data)=='getattr'and len(lhs.children)==3 and str(lhs.children[-1])=='game':return self.receiver(D.unwrap(lhs.children[0]),scope,line,klass)
  return 'INDEX_OR_RECEIVER_UNPROVEN'
 def receiver(self,node,scope,line,klass):
  node=D.unwrap(node)
  if isinstance(node,Token):
   if str(node)=='self':return 'MAIN_CLASS_FIELD'if self.sf.global_name=='ReefMain'and klass==self.sf.root_class else 'OTHER_SELF_CLASS'
   decls=self.sf.lookup(scope,str(node),line)
   if decls and all(d['type']=='ReefMain'for d in decls):return 'EXPLICIT_TYPED_REEFMAIN_RECEIVER'
  return 'RECEIVER_OR_ALIAS_UNPROVEN'
 def row(self,node,method,kind,owner,**extra):
  self.ordinal[(method,kind)]+=1;source=self.sf.excerpt(node);key=self.sf.path+'::'+method+'::'+kind+'::'+str(self.ordinal[(method,kind)]);self.rows.append({'id':'FVGAME-'+sha(key.encode())[:12].upper(),'path':self.sf.path,'function':method,'line':node.meta.line,'end_line':node.meta.end_line,'kind':kind,'owner_evidence':owner,'source_excerpt':source,'source_excerpt_sha256':sha(source.encode()),**extra})
 def walk(self,node,method,scope,klass):
  if not isinstance(node,Tree):return
  kind=str(node.data);outer=scope;blocks={'if_branch','elif_branch','else_branch','match_branch','while_stmt','for_stmt','for_stmt_typed'}
  if kind in blocks:scope+='/'+kind+'@'+str(node.meta.line)+':'+str(node.meta.column)
  if kind=='class_def':klass+='::'+str(node.children[0]);scope=klass
  if kind=='func_def':
   header=next(c for c in node.children if isinstance(c,Tree)and str(c.data)=='func_header');method=str(header.children[0]);scope=klass+'/'+method+'@'+str(node.meta.line)+':'+str(node.meta.column)
  if kind=='lambda':scope+='/lambda@'+str(node.meta.line)+':'+str(node.meta.column)
  assert scope in self.sf.scopes,(self.sf.path,kind,scope)
  if kind.startswith(('class_var_','func_var_')) and node.children and str(node.children[0])=='game':
   expr=[c for c in node.children if isinstance(c,Tree)and str(c.data)=='expr'];value=D.literal(expr[-1])if expr else None;own=self.owner(node.children[0],scope,node.meta.line,klass);self.row(node,method,'GAME_DECLARATION',own,operator='initializer',literal_string_value=value,full_literal_write=value is not None and own=='MAIN_CLASS_FIELD')
  if kind=='assnmnt_expr'and len(node.children)>=3:
   lhs=D.unwrap(node.children[0]);is_game=isinstance(lhs,Token)and str(lhs)=='game' or isinstance(lhs,Tree)and str(lhs.data)=='getattr'and str(lhs.children[-1])=='game';indexed=isinstance(lhs,Tree)and str(lhs.data)=='subscr_expr'and D.literal(lhs.children[-1])=='game'
   if is_game or indexed:
    own=self.owner(lhs,scope,node.meta.line,klass);op=str(node.children[1]);value=D.literal(node.children[-1]);self.row(node,method,'GAME_ASSIGNMENT'if is_game else'INDEXED_GAME_KEY_ASSIGNMENT',own,operator=op,literal_string_value=value,full_literal_write=is_game and op=='='and value is not None and own in {'MAIN_CLASS_FIELD','EXPLICIT_TYPED_REEFMAIN_RECEIVER'},rhs_ast=str(D.unwrap(node.children[-1]).data)if isinstance(D.unwrap(node.children[-1]),Tree)else'token')
  if kind in {'standalone_call','getattr_call'}:
   name,recv,args,_=D.call_parts(node)
   if name in {'set','set_deferred','set_indexed'}and args and D.literal(args[0])=='game':self.row(node,method,'REFLECTIVE_GAME_WRITE_SPELLING_CANDIDATE',self.receiver(recv if recv is not None else Token('NAME','self'),scope,node.meta.line,klass),operator=name,literal_string_value=D.literal(args[1])if len(args)>1 else None,full_literal_write=False,limit='Native/override identity not proved by spelling; not a producer-domain closure')
  for index,child in enumerate(node.children):
   header=kind in blocks and isinstance(child,Tree)and str(child.data)=='expr'and index<(3 if kind=='for_stmt_typed'else 2);self.walk(child,method,outer if header else scope,klass)
def scan():
 paths=[p for p in subprocess.check_output(['git','ls-tree','-r','--name-only',REV,'--','scripts','scenes','addons'],cwd=R,text=True).splitlines()if p.endswith('.gd')];files=[];rows=[]
 raw=subprocess.check_output(['git','cat-file','--batch'],input=''.join(REV+':'+p+'\n'for p in paths).encode(),cwd=R);pos=0
 for path in paths:
  end=raw.index(b'\n',pos);size=int(raw[pos:end].split()[-1]);pos=end+1;b=raw[pos:pos+size];pos+=size+1;f=Facts(b.decode('utf-8-sig'),path);files.append({'path':path,'revision':REV,'sha256':sha(b),'bytes':len(b),'filename_probe':Path(path).name.startswith('probe'),'parse':'PASS'});rows.extend(f.rows)
 assert pos==len(raw)and len(paths)==312
 nonprobe=[r for r in rows if not Path(r['path']).name.startswith('probe')];literal=[r for r in nonprobe if r['full_literal_write']];values=sorted({r['literal_string_value']for r in literal});wr('SOURCE_GAME_CENSUS.json',{'revision':REV,'analyzer_sha256':sha(Path(__file__).read_bytes()),'scope_helper_sha256':sha((H/'r45_dispatch_semantics_audit/classify_dispatch.py').read_bytes()),'gdtoolkit_version':importlib.metadata.version('gdtoolkit'),'files':files,'rows':rows,'counts':dict(Counter(r['kind']for r in rows)),'nonprobe_filename_candidates':len(nonprobe),'bound_literal_main_field_write_rows':len(literal),'bound_literal_main_values':values,'full_game_value_domain_closed':False,'limits':'All312 files parsed; confirmed declaration/typed-member literal writes are source producers only. Nonliteral writes, aliases/native/overrides/callback/resource reachability remain open. Non-probe filename is not normal gameplay proof. No counts represent artwork/screens/removal.'});print('R57_AST',len(files),'files',len(rows),'rows',len(literal),'typed/main literal writes',len(values),'values',flush=True)
if __name__=='__main__':scan()
