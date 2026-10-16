from pathlib import Path
import json,hashlib,subprocess,importlib.util,collections,os
from gdtoolkit.parser import parser
from lark import Tree,Token
P=Path(__file__).resolve().parent;R=P.parents[3];D='dd799b2d43871b29d1d6e0503646308a194dad1e'
sp=importlib.util.spec_from_file_location('a77scan',P/'bounded_json.py');A=importlib.util.module_from_spec(sp);sp.loader.exec_module(A)
OUT=Path(os.environ.get('R77_ANALYSIS_OUTPUT',str(P)));OUT.mkdir(exist_ok=True,parents=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
def literal(node):
 if isinstance(node,Tree)and str(node.data)=='string'and node.children:
  try:return json.loads(str(node.children[0]))
  except Exception:return None
 return None
TARGETS={'_build_intro','_build_start_menu','_launch_from_start_menu','_prepare_start_menu_launch','_perform_new_game','_request_new_game','_continue_game','_skip_intro'}
DISPATCH={'call','callv','call_deferred','call_thread_safe','call_deferred_thread_group','Callable'}
def scan(text,path):
 lines=text.splitlines();tree=parser.parse(text,gather_metadata=True);calls=[];refs=[];rawdispatch=[]
 def walk(node,func='<top>',guards=()):
  if not isinstance(node,Tree):return
  kind=str(node.data)
  if kind=='func_def':
   h=next(c for c in node.children if isinstance(c,Tree)and str(c.data)=='func_header');func=str(h.children[0])
  if kind in ['if_branch','elif_branch','else_branch','match_branch']:
   test=node.children[0].pretty()if node.children and isinstance(node.children[0],Tree)and str(node.children[0].data)=='expr'else'NO_DIRECT_CONDITION_FOR_THIS_BRANCH'
   guards=(*guards,{'kind':kind,'line':node.meta.line,'condition_AST':test.strip()})
  if kind in ['getattr_call','standalone_call']:
   if kind=='standalone_call':name=str(node.children[0]);receiver='self';args=node.children[1:]
   else:
    head=node.children[0];name=str(head.children[-1])if isinstance(head,Tree)and str(head.data)=='getattr'else'';receiver=head.pretty().strip()if isinstance(head,Tree)else str(head);args=node.children[1:]
   row={'path':path,'function':func,'line':node.meta.line,'end_line':node.meta.end_line,'method':name,'receiver_AST':receiver,'guards':list(guards),'excerpt':'\n'.join(lines[node.meta.line-1:node.meta.end_line])}
   if name in TARGETS:calls.append(row)
   if name in DISPATCH:
    ix=1 if name=='Callable'else 0;value=literal(args[ix])if len(args)>ix else None;rawdispatch.append(dict(row,literal_selector_or_payload=value,semantic_classification='RAW_SYNTAX_ONLY_NOT_INVOCATION_OR_UNREACHABILITY_COUNT'))
  for child in node.children:
   if isinstance(child,Token)and str(child)in TARGETS and kind!='func_header':refs.append({'path':path,'function':func,'line':getattr(child,'line',node.meta.line),'name':str(child),'AST_parent':kind,'guards':list(guards)})
   walk(child,func,guards)
 walk(tree);return calls,refs,rawdispatch
paths=[x for x in git('ls-tree','-r','--name-only',D,'--','scripts').decode().splitlines()if x.endswith('.gd')];files=[];calls=[];refs=[];rawdispatch=[];source_refs=[]
# One exact Git blob per source file; all corpus hashes are published for replay.
for path in paths:
 raw=git('show',D+':'+path);text=raw.decode('utf-8-sig');probe=Path(path).name.startswith('probe')or Path(path).stem.endswith('_test_case');cs,rs,ds=scan(text,path)
 for rows in [cs,rs,ds]:
  for row in rows:row['probe_or_test_filename']=probe
 files.append({'path':path,'revision':D,'sha256':sha(raw),'bytes':len(raw),'probe_or_test_filename':probe,'parse':'PASS'});calls.extend(cs);refs.extend(rs);rawdispatch.extend(ds)
 if len(files)%100==0:print('R77_AST_PARSED',len(files),'of',len(paths),flush=True)
resource_rows=[]
for path in [x for x in git('ls-tree','-r','--name-only',D,'--','scenes','project.godot').decode().splitlines()if x.endswith(('.tscn','.godot'))]:
 raw=git('show',D+':'+path);lines=raw.decode('utf-8-sig').splitlines();matches=[{'line':i+1,'text':x}for i,x in enumerate(lines)if any(t in x for t in ['intro_overlay','start_menu','run/main_scene'])]
 if matches:resource_rows.append({'path':path,'revision':D,'sha256':sha(raw),'bytes':len(raw),'matches':matches})
prod=[x for x in calls if not x['probe_or_test_filename']];intro=[x for x in prod if x['method']=='_build_intro'];ready=[x for x in intro if x['path']=='scripts/main.gd'and x['function']=='_ready'];assert len(ready)==1 and any('headless'in g['condition_AST']and g['kind']=='if_branch'for g in ready[0]['guards'])
doc={'schema':'reef.intro_named_entry_graph/1','source_revision':D,'files':files,'target_names':sorted(TARGETS),'named_calls':calls,'method_reference_candidates':refs,'raw_reflective_syntax':rawdispatch,'resource_entry_references':resource_rows,'summary':{'parsed_scripts':len(files),'named_target_calls':len(calls),'non_test_candidate_target_calls':len(prod),'main_ready_build_intro_named_calls':len(ready),'current_main_ready_intro_guard':'DisplayServer.get_name() == headless','normal_display_startup':'_build_start_menu else branch','raw_dispatch_semantics_recomputed':False,'global_unreachability_proved':False},'limits':'AST named callee and guard evidence; method references are not extra invocations. Non-test filename does not prove normal entry. Raw call/Callable syntax includes constructors and callback data; do not resurrect the R44raw95 as unresolved invocation count. R45 semantic closure remains separate; dynamic/native/external/debug paths are not globally closed here. Current display absence is proven only for recorded original entry/reentry controls. No four-page source pixels are force-captured or accepted.'};A.write_document(OUT/'SOURCE_ENTRY_GRAPH.json',doc)
print('R77_SOURCE_ENTRY_GRAPH',doc['summary'],flush=True)
for row in intro:print('INTRO_NAMED_CALL',row['path'],row['function'],row['line'],'guard',json.dumps(row['guards'],ensure_ascii=True)[:350])
