"""Bound named source paths; unknown mutation/native/runtime domains stay open."""
from pathlib import Path
import hashlib,json,subprocess,importlib.util,collections,re
from lark import Tree,Token
P=Path(__file__).resolve().parent;R=P.parents[3];BASE='61d12c5b7d29cd106a817d8d0064aa60f48f3ed2'
spec=importlib.util.spec_from_file_location('dispatch45',P.parent/'r45_dispatch_semantics_audit/classify_dispatch.py');D=importlib.util.module_from_spec(spec);spec.loader.exec_module(D)
FIELDS={'encounter_press','encounter_cancel','encounter_motion','world_press_probe','world_press_release','world_press_drag','world_drag_end','world_press_cancel','castle_royal_hall_event_entry','touch_ui'}
APIS={'set_encounter_controls','arm_royal_hall_event'}
MUTATORS={'set','set_deferred','set_indexed','set_script'}
def sha(b):return hashlib.sha256(b).hexdigest()
ANALYZER_SHA256=sha(Path(__file__).read_bytes())
def wr(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
def raw_source(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=R,stderr=subprocess.PIPE)
def terminal(node):
 node=D.unwrap(node)
 if isinstance(node,Token):return str(node)
 if not isinstance(node,Tree):return None
 if str(node.data)=='getattr':return str(node.children[-1])
 if str(node.data)=='subscr_expr':return D.literal(node.children[-1])
 return None
def property_literal(node):
 literal=D.literal(node)
 if literal is not None:return literal
 node=D.unwrap(node)
 if isinstance(node,Tree) and str(node.data)=='standalone_call' and str(node.children[0]) in {'NodePath','StringName'} and len(node.children)==2:return D.literal(node.children[1])
 return None
class Facts:
 def __init__(self,text,path):
  self.sf=D.ScriptFacts(text,path,BASE);self.text=text;self.path=path;self.rows=[];self.ordinal=collections.Counter();self.walk(self.sf.tree,'<top>',self.sf.root_class,None)
 def row(self,node,function,kind,**values):
  self.ordinal[(function,kind)]+=1;body=self.sf.excerpt(node)
  if kind=='DISPATCH_INVOCATION_CANDIDATE':values['r45_binding_id']=next(x['binding_id'] for x in self.sf.calls if x['node'] is node)
  x={'id':'FVW-'+sha((self.path+'::'+function+'::'+kind+'::'+str(self.ordinal[(function,kind)])).encode())[:12].upper(),'path':self.path,'function':function,'line':node.meta.line,'end_line':node.meta.end_line,'kind':kind,'source':body,'source_sha256':sha(body.encode()),**values};self.rows.append(x);return x
 def walk(self,node,function,klass,parent):
  if not isinstance(node,Tree):return
  kind=str(node.data)
  if kind=='class_def':klass+='::'+str(node.children[0])
  if kind=='func_def':
   header=next(c for c in node.children if isinstance(c,Tree) and str(c.data)=='func_header');function=str(header.children[0])
  if kind=='assnmnt_expr' and len(node.children)>=3:
   lhs=D.unwrap(node.children[0]);field=terminal(lhs)
   if field in FIELDS:
    owner='UNPROVEN_MEMBER_OR_ALIAS'
    if isinstance(lhs,Token):
     a=next((x for x in self.sf.assignments if x['line']==node.meta.line and x['symbol']==field),None);decls=self.sf.lookup(a['scope'],field,node.meta.line) if a else []
     owner='CLASS_FIELD' if decls and all(d['kind'].startswith('class_var') for d in decls) else 'LOCAL_OR_SHADOWED_SYMBOL'
    elif isinstance(lhs,Tree) and str(lhs.data)=='getattr' and str(lhs.children[0])=='self':owner='EXPLICIT_SELF_MEMBER'
    self.row(node,function,'NAMED_WRITE',field=field,owner_evidence=owner,lhs_AST=lhs.pretty().strip() if isinstance(lhs,Tree) else str(lhs),value_AST=D.unwrap(node.children[-1]).pretty().strip() if isinstance(D.unwrap(node.children[-1]),Tree) else str(D.unwrap(node.children[-1])))
   elif isinstance(lhs,Tree) and str(lhs.data)=='subscr_expr' and field is None:
    self.row(node,function,'COMPUTED_INDEX_WRITE',field=None,lhs_AST=lhs.pretty().strip(),scope_limit='Dictionary/array/object identity unresolved here; not automatically a callback-port write or safe exclusion')
  if kind.startswith('class_var_') and node.children and str(node.children[0]) in FIELDS:
   self.row(node,function,'PORT_OR_OWNER_DECLARATION',field=str(node.children[0]),declaring_class=klass)
  if kind in {'standalone_call','getattr_call'}:
   name,receiver,args,receiver_ast=D.call_parts(node)
   if name in APIS:self.row(node,function,'API_CALLER',api=name,receiver_AST=receiver_ast,arguments_AST=[x.pretty().strip() if isinstance(x,Tree) else str(x) for x in args])
   if name in MUTATORS:
    key=property_literal(args[0]) if args and name!='set_script' else None
    self.row(node,function,'PROPERTY_MUTATOR',api=name,property=key,selected_field=(any(part in FIELDS for part in re.split(r'[:/]',key)) if name=='set_indexed' else key in FIELDS) if key is not None else None,receiver_AST=receiver_ast,scope_limit='Candidate spelling/property literal only; receiver/override/alias/native semantics are not closed here. Unknowns retain mutation risk')
   if name in {'call','callv','call_deferred','call_thread_safe','call_deferred_thread_group'}:
    key=property_literal(args[0]) if args else None
    self.row(node,function,'DISPATCH_INVOCATION_CANDIDATE',first_argument_literal=key,possible_mutator_literal=key in MUTATORS if key is not None else None,target_method_inferred=False,receiver_AST=receiver_ast,scope_limit='Receiver semantics unresolved here: first literal may be Callable payload, never a proven method edge. See original R45 typed semantics.')
   if name=='Callable' and len(args)>=2:
    selector=property_literal(args[1])
    if selector in MUTATORS or selector is None:self.row(node,function,'CALLABLE_MUTATOR_OR_COMPUTED_SELECTOR',selector_literal=selector,scope_limit='Computed constructor selector/native mutator may escape named-write census')
  if kind=='getattr' and str(node.children[-1]) in MUTATORS and parent!='getattr_call':self.row(node,function,'MUTATOR_METHOD_REFERENCE',member=str(node.children[-1]),scope_limit='A stored native setter method can be invoked through a callback')
  for child in node.children:self.walk(child,function,klass,kind)
def method(path,name):
 raw=raw_source(path);s=raw.decode('utf-8-sig');a=s.index('func '+name+'(');b=s.find('\nfunc ',a+1);b=len(s) if b<0 else b
 return {'path':path,'revision':BASE,'function':name,'file_sha256':sha(raw),'body_sha256':sha(s[a:b].encode()),'start_line':s[:a].count('\n')+1,'end_line':s[:b].count('\n')+1}
def main():
 old=json.loads((P.parent/'r44_creature_route_caller_audit/SOURCE_CALL_GRAPH.json').read_text(encoding='utf-8'));files=[];facts=[]
 for x in old['files']:
  raw=raw_source(x['path']);assert sha(raw)==x['sha256'],x['path'];facts.append(Facts(raw.decode('utf-8-sig'),x['path']));files.append({'path':x['path'],'revision':BASE,'sha256':sha(raw),'bytes':len(raw),'r44_revision':x['revision'],'r44_sha256':x['sha256'],'parse':'PASS','probe_label':x['probe']})
 active=[x for x in subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'--','scripts','scenes','addons'],cwd=R,text=True).splitlines() if x.endswith('.gd')];assert set(active)=={x['path'] for x in files}
 wr(P/'SOURCE_EQUIVALENCE.json',{'baseline':BASE,'files':files,'exact_active_folder_script_set':True,'scope':'312 current tracked scripts/scenes/addons files; disabled addon and doc fixtures excluded from product-source set. All probe labels retained, not normal-reachability evidence.'})
 rows=[r for f in facts for r in f.rows];wr(P/'MUTATION_CENSUS.json',{'baseline':BASE,'source_files':len(files),'analyzer_sha256':ANALYZER_SHA256,'r45_helper_sha256':D.EXECUTION_SOURCE_SHA,'rows':rows,'counts':dict(collections.Counter(x['kind'] for x in rows)),'limits':'AST inventory of named writes/API callers plus computed-index/property/indirect-dispatch risks. No universal alias/native/resource/runtime closure is claimed.'})
 oldports=json.loads((P.parent/'r45_dispatch_semantics_audit/CALLBACK_PORTS.json').read_text(encoding='utf-8'))['ports'];selected=[x for x in oldports if x['path']=='scripts/touch_ui.gd' or x['id']=='FVP-5FA6C9E6E469'];assert len(selected)==9
 target={'world_press_probe':('scripts/main.gd','_on_world_press'),'world_press_release':('scripts/main.gd','_on_world_press_release'),'world_press_drag':('scripts/main.gd','_on_world_press_drag'),'world_drag_end':('scripts/main.gd','_on_world_drag_end'),'world_press_cancel':('scripts/main.gd','_on_world_press_cancel'),'encounter_press':('scripts/games/dust_boss.gd','on_world_tap'),'encounter_cancel':('scripts/games/dust_boss.gd','_cancel_world_move'),'encounter_motion':('scripts/games/dust_boss.gd','on_world_drag'),'entry':('scripts/day_one_flow.gd','_day_one_trigger_boss')}
 out=[]
 for port in selected:
  field=port['receiver_declarations'][0]['name'];path,name=target[field];stored='castle_royal_hall_event_entry' if field=='entry' else field
  relevant=[x for x in rows if x.get('field')==stored or x['kind']=='API_CALLER' and x['api']==('arm_royal_hall_event' if field=='entry' else 'set_encounter_controls') and (field=='entry' or field.startswith('encounter_'))]
  out.append({'port_id':port['id'],'source_path':port['path'],'stored_field':stored,'invocation_ids':[x['binding_id'] for x in port['invocation_sites']],'invocation_lines':[x['line'] for x in port['invocation_sites']],'status':'NAMED_SOURCE_PATH_VALUE_DOMAIN_BOUND_FULL_CLOSURE_OPEN','standard_target':method(path,name),'empty_inactive_default':True,'source_evidence_ids':[x['id'] for x in relevant],'source_path_scope':'Main constructed TouchUI plus Main._init_touch_experiment five direct bindings; DustBoss stage-open/reset sets three encounter slots; DayOneFlow arms Royal Hall hook. Test/probe and alternate writes stay in census. Source excerpt evidence must be reviewed, not inferred as normal reachability.','full_write_caller_value_closure':False,'native_alias_resource_runtime_closure':False})
 wr(P/'CALLBACK_DOMAINS.json',{'schema':1,'baseline':BASE,'analyzer_sha256':ANALYZER_SHA256,'r45_helper_sha256':D.EXECUTION_SOURCE_SHA,'ports':out,'selected_port_groups':9,'selected_invocation_sites':14,'named_source_path_method_targets':9,'original_R45_pending_invocations':57,'R45_sites_outside_this_traced_subset':43,'full_runtime_domains_still_open':57,'new_artwork_or_capture_credit':0,'accepted_removed':0,'limits':'The fourteen named standard-path value bindings do not close aliases, arbitrary external writes/native/resource reachability, per-route dispatch, full compositor closure or runtime/QA11/art acceptance.'})
 print('R49_SOURCE_CENSUS',len(files),'files',len(rows),'rows',dict(collections.Counter(x['kind'] for x in rows)),'9ports14sites source-path-bound',flush=True)
if __name__=='__main__':main()
