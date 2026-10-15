from pathlib import Path
import json,hashlib,subprocess,datetime,collections
from gdtoolkit.parser import parser
from lark import Tree,Token
R=Path.cwd();P=R/'docs/handoffs/codex_flat_vector_art_2026-10-07/r44_creature_route_caller_audit';B='ccbe6d60e4021977c520844797d4d36086ad6e73'
targets={'_make_creature_node','_stuffie_cutout','creature_for','make_creature','_tick_room','_build_room','_tick_follower','_follow_ctx','tick_canvas_care','_start_stuffie_battle','sync_castle_companion_card','_add_creature_preview'};dispatch={'call','callv','call_deferred','call_thread_safe','call_deferred_thread_group','Callable'}
rows=[];dynamic=[];files=[];strings=[];ordinal=collections.Counter()
def sha(b):return hashlib.sha256(b).hexdigest()
def literal(node):
 if isinstance(node,Tree) and str(node.data)=='string' and node.children:
  try:return json.loads(str(node.children[0]))
  except Exception:return None
 return None
def call_name(node):
 if str(node.data)=='standalone_call':return str(node.children[0]),'self',list(node.children[1:])
 head=node.children[0]
 if isinstance(head,Tree) and str(head.data)=='getattr':return str(head.children[-1]),head.pretty().strip(),list(node.children[1:])
 return '',str(head),list(node.children[1:])
for p in sorted((R/'scripts').rglob('*.gd')):
 path=p.relative_to(R).as_posix();raw=subprocess.check_output(['git','show',B+':'+path],stderr=subprocess.PIPE);text=raw.decode('utf-8-sig');lines=text.splitlines();tree=parser.parse(text,gather_metadata=True);probe=p.name.startswith('probe');files.append({'path':path,'revision':B,'sha256':sha(raw),'probe':probe,'parse':'PASS'})
 def walk(node,func='<top>'):
  if not isinstance(node,Tree):return
  kind=str(node.data)
  if kind=='func_def':
   header=next((c for c in node.children if isinstance(c,Tree) and str(c.data)=='func_header'),None)
   if header is not None:func=str(header.children[0])
  if kind in ['getattr_call','standalone_call']:
   name,receiver,args=call_name(node);line=node.meta.line;end=node.meta.end_line;full='\n'.join(lines[line-1:end]);ordinal[(path,func,name)]+=1;key=path+'::'+func+'::'+name+'::'+str(ordinal[(path,func,name)]);row={'binding_id':'FVC-'+sha(key.encode())[:12].upper(),'path':path,'revision':B,'function':func,'line':line,'end_line':end,'method':name,'receiver_AST':receiver[:700],'source_excerpt':full[:900],'full_excerpt_sha256':sha(full.encode()),'probe':probe}
   if name in targets or (name=='tick' and ('companion' in full or path.endswith('companion.gd'))):rows.append(row)
   if name in dispatch:
    argument_index=1 if name=='Callable' else 0;value=literal(args[argument_index]) if len(args)>argument_index else None;row.update(literal_target=value,resolution='LITERAL_TARGET' if value is not None else 'DYNAMIC_TARGET_UNRESOLVED_BY_THIS_SCAN');dynamic.append(row)
  if kind=='string':
   value=literal(node)
   if value is not None and any(x in value for x in targets):strings.append({'path':path,'function':func,'line':node.meta.line,'value':value[:600],'probe':probe})
  for child in node.children:walk(child,func)
 walk(tree)
prod=[x for x in rows if not x['probe']];unknown=[x for x in dynamic if not x['probe'] and x['literal_target'] is None];doc={'schema':'reef.creature_qualified_source_calls/1','baseline':B,'generated_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'Installedgdtoolkit actualASTparse forallcurrent scripts/*.gd;qualifiedowner/function/receiverAST/method/namedCallable/constantcall targets retained. Probeclassification byfilename. Dynamicunknownsites explicitlyretained,not guessed.','files':files,'target_method_names':sorted(targets),'qualified_calls':rows,'dispatch_sites':dynamic,'target_string_references':strings,'summary':{'parsed_files':len(files),'production_files':sum(not x['probe'] for x in files),'target_call_sites':len(rows),'production_target_call_sites':len(prod),'probe_target_call_sites':len(rows)-len(prod),'production_dynamic_target_sites_unresolved':len(unknown),'production_named_start_stuffie_calls':sum(x['method']=='_start_stuffie_battle' for x in prod),'production_named_tick_room_calls':sum(x['method']=='_tick_room' for x in prod)},'limits':'Missingnamedcallalone doesnotproveunreachable;nonliteraldispatch/plugin/external/debug/route reachability requireseparatequalification. Sourcecallers arenotartpieces ornormaldisplaycontext/acceptance. No frozen IDs/dispositions changed byscan.','accepted_removed':0};(P/'SOURCE_CALL_GRAPH.json').write_text(json.dumps(doc,indent=2)+'\n',encoding='utf-8',newline='\n');print('R44_AST_SOURCE',doc['summary'],flush=True)
for x in prod:
 if x['method'] in ['_start_stuffie_battle','_tick_room','_build_room','make_creature','_stuffie_cutout']:print(x['path'],x['function'],x['line'],x['method'])
print('UNRESOLVED_DISPATCH_SOURCE_FILES',sorted({x['path'] for x in unknown}))
