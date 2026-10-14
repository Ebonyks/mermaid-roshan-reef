"""Current source-only inventory. Counts are syntax/resource units, never artwork removal."""
from pathlib import Path
from collections import Counter,defaultdict
import json,hashlib,subprocess,ast,re,unicodedata,datetime,importlib.metadata
from gdtoolkit.parser import parser
from lark import Tree,Token
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;BASE='01f670d7ab4933fe2c2e6605bbca4ef2105f200f'
def sha(b):return hashlib.sha256(b).hexdigest()
def ident(prefix,*parts):return prefix+'-'+sha('|'.join(str(x) for x in parts).encode())[:12].upper()
def wr(name,d):(P/name).write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
def rd(path):return json.loads(path.read_text(encoding='utf-8'))
def parse_script(path,raw):
 text=raw.decode('utf-8-sig');lines=text.splitlines();tree=parser.parse(text,gather_metadata=True)
 funcs=[];classes=[];strings=[];calls=[]
 def visit(node,class_scope=''):
  kind=str(node.data)
  if kind=='class_def':class_scope=class_scope+str(node.children[0])+'.'
  if kind=='classname_stmt' and not class_scope:classes.append(str(node.children[0]))
  if kind=='func_def':
   header=next(x for x in node.children if isinstance(x,Tree) and str(x.data) in ['func_header','static_func_header'])
   end=min(len(lines),node.meta.end_line-(1 if node.meta.end_column==1 else 0));name=str(header.children[0]);funcs.append({'name':class_scope+name,'method_name':name,'class_scope':class_scope.rstrip('.'),'start_line':node.meta.line,'end_line':end,'source_sha256_lf':sha(('\n'.join(lines[node.meta.line-1:end])+'\n').encode())})
  for child in node.children:
   if isinstance(child,Tree):visit(child,class_scope)
 visit(tree)
 def scope(line):
  matches=[x for x in funcs if x['start_line']<=line<=x['end_line']]
  return max(matches,key=lambda x:x['start_line'])['name'] if matches else 'FILE_SCOPE'
 for node in tree.iter_subtrees():
  kind=str(node.data)
  if kind=='string':
   literal=str(node.children[0])
   try:value=ast.literal_eval(literal)
   except (ValueError,SyntaxError):value=None
   if isinstance(value,str):strings.append({'line':node.meta.line,'scope':scope(node.meta.line),'value':value,'literal':literal})
  if kind.endswith('_call') or kind=='call':
   expr=text[node.meta.start_pos:min(node.meta.end_pos,len(text))];callee=expr.split('(',1)[0].strip()
   args=[x for x in node.children[1:] if isinstance(x,Tree)]
   first=args[0] if args else None;direct=None
   if first is not None and str(first.data)=='string':
    try:direct=ast.literal_eval(str(first.children[0]))
    except (SyntaxError,ValueError):pass
   calls.append({'line':node.meta.line,'scope':scope(node.meta.line),'callee_expression':callee,'expression':expr[:1400],'literal_first_argument':direct,'ast_kind':kind})
 return {'path':path,'raw_sha256':sha(raw),'source_sha256_lf':sha(text.replace('\r\n','\n').encode()),'bytes':len(raw),'lines':len(lines),'classes':classes,'functions':sorted(funcs,key=lambda x:(x['start_line'],x['name'])),'strings':sorted(strings,key=lambda x:(x['line'],x['literal'])),'calls':sorted(calls,key=lambda x:(x['line'],x['expression']))}
DRAW={'draw_line','draw_polyline','draw_multiline','draw_arc','draw_circle','draw_ellipse','draw_rect','draw_polygon','draw_colored_polygon','draw_texture','draw_texture_rect','draw_texture_rect_region','draw_string','draw_char','draw_mesh','draw_primitive'}
RASTER={'fill','fill_rect','set_pixel','set_pixelv','blit_rect','blit_rect_mask','blend_rect','blend_rect_mask','create_from_image'}
STYLE={'StyleBoxFlat','ColorRect','Polygon2D','Line2D','Gradient','GradientTexture1D','GradientTexture2D','ImmediateMesh','SurfaceTool'}
DYNAMIC={'load','preload','call','call_deferred','callv','Callable','get_node','get_node_or_null','get_script'}
def categories(call):
 callee=call['callee_expression'];parts=callee.split('.');last=parts[-1];owner=parts[-2] if len(parts)>1 else ''
 result=[]
 if last in DRAW:result.append('CANVAS_DRAW_SYNTAX')
 if last in RASTER:result.append('RASTER_OR_IMAGE_API_CANDIDATE_RECEIVER_UNPROVEN')
 if last in STYLE or last=='new' and owner in STYLE:result.append('STYLE_OR_VISUAL_CONSTRUCTOR')
 if last in DYNAMIC:result.append('LOAD_DISPATCH_OR_NODE_LOOKUP')
 return result
def pictogram(value):return any(ord(c)>127 and unicodedata.category(c).startswith('S') for c in value)
def resource_literals(raw,ext):
 """Lexical quoted references with comments skipped; not a shader/resource parser."""
 text=raw.decode('utf-8-sig');shader=ext in ['.gdshader','.gdshaderinc']
 pattern=r'"(?:\\.|[^"\\])*"|//[^\n]*|/\*[\s\S]*?\*/' if shader else r'"(?:\\.|[^"\\])*"|[;#][^\n]*'
 rows=[]
 for token in re.finditer(pattern,text):
  value=token.group()
  if not value.startswith('"'):continue
  try:reference=json.loads(value)
  except (ValueError,json.JSONDecodeError):continue
  if reference.startswith(('res://','uid://')):rows.append({'line':text.count('\n',0,token.start())+1,'scope':'RESOURCE_FILE','reference':reference,'reference_kind':'LEXICAL_RESOURCE_OR_SHADER_STRING_NOT_RUNTIME_PROOF'})
 return rows
def run():
 entries=subprocess.check_output(['git','ls-tree','-r',BASE],cwd=R).decode('utf-8').splitlines();blobs={}
 for line in entries:
  head,path=line.split('\t',1);mode,kind,obj=head.split();
  if kind=='blob':blobs[path]=obj
 ignore={Path(p).parent.as_posix() for p in blobs if Path(p).name=='.gdignore'}
 def ignored(path):return any(path==d or path.startswith(d+'/') for d in ignore if d!='.')
 roots=('scripts/','scenes/','shaders/','assets/','addons/')
 text_ext={'.gd','.tscn','.tres','.gdshader','.gdshaderinc','.godot','.uid','.import'}
 inputs=sorted(p for p in blobs if (p.startswith(roots) or p=='project.godot') and Path(p).suffix in text_ext and not ignored(p))
 request=''.join(BASE+':'+p+'\n' for p in inputs).encode();out=subprocess.check_output(['git','cat-file','--batch'],input=request,cwd=R);data={};pos=0
 for path in inputs:
  end=out.index(b'\n',pos);header=out[pos:end].decode();size=int(header.split()[-1]);pos=end+1;data[path]=out[pos:pos+size];pos+=size+1
 assert pos==len(out)
 scripts=[];failures=[];resources=[];refs=[];uidmap=defaultdict(set)
 for path,raw in data.items():
  ext=Path(path).suffix
  if ext=='.uid':
   uid=raw.decode('utf-8-sig').strip()
   if uid.startswith('uid://'):uidmap[uid].add(path[:-4])
  elif ext=='.import':
   txt=raw.decode('utf-8-sig');uid=re.search(r'^uid="([^"]+)"',txt,re.M);src=re.search(r'^source_file="res://([^"]+)"',txt,re.M)
   if uid and src:uidmap[uid[1]].add(src[1])
 for path,raw in data.items():
  ext=Path(path).suffix
  if ext in ['.uid','.import']:continue
  resources.append({'path':path,'git_blob':blobs[path],'bytes':len(raw),'raw_sha256':sha(raw),'role':'PROBE_SOURCE' if Path(path).name.startswith('probe') else 'CURRENT_PROJECT_SOURCE_OR_RESOURCE'})
  if ext=='.gd':
   try:d=parse_script(path,raw);scripts.append(d)
   except Exception as error:failures.append({'path':path,'error_type':type(error).__name__,'message':str(error)[:500],'status':'PARSE_COVERAGE_GAP'});continue
   for x in d['strings']:
    if x['value'].startswith(('res://','uid://')):refs.append(dict(x,source=path,reference=x['value'],reference_kind='AST_STRING_REFERENCE_NOT_RUNTIME_LOAD_PROOF'))
  else:
   for row in resource_literals(raw,ext):refs.append(dict(row,source=path))
 classmap=defaultdict(list)
 for d in scripts:
  for name in d['classes']:classmap[name].append(d['path'])
 filemap={d['path']:d for d in scripts};calls=[];scopes=[];glyphs=[]
 for d in scripts:
  grouped=defaultdict(list);api=defaultdict(set)
  for x in d['calls']:
   cats=categories(x);callee=x['callee_expression'];parts=callee.split('.');last=parts[-1];candidates=[];binding='BUILTIN_INHERITED_OR_DYNAMIC_UNRESOLVED'
   local_prefix=x['scope'].rsplit('.',1)[0]+'.' if '.' in x['scope'] else ''
   local_names=[local_prefix+last,last] if local_prefix else [last]
   local_match=next((n for n in local_names if any(f['name']==n for f in d['functions'])),None)
   if len(parts)==1 and local_match:candidates=[{'path':d['path'],'function':local_match}];binding='SAME_SCRIPT_NAME_POTENTIAL_ONLY'
   elif len(parts)==2 and len(classmap.get(parts[0],[]))==1:
    target=classmap[parts[0]][0];candidates=[{'path':target,'function':last}];binding='PROJECT_CLASS_NAME_POTENTIAL_ONLY'
   row=dict(x,path=d['path'],source_role=('PROBE_NAMED_SOURCE' if Path(d['path']).name.startswith('probe') else 'NONPROBE_PROJECT_SOURCE'),categories=cats,callee_candidates=candidates,binding=binding)
   calls.append(row)
   for cat in cats:api[x['scope']].add(cat)
  for x in d['strings']:
   if pictogram(x['value']):grouped[(x['scope'],x['line'])].append(x)
  for (scope,line),values in grouped.items():
   api[scope].add('SYMBOL_STRING_CANDIDATE_ROLE_UNREVIEWED');glyphs.append({'id':ident('FVGS',d['path'],scope,line,*(v['value'] for v in values)),'source_role':('PROBE_NAMED_SOURCE' if Path(d['path']).name.startswith('probe') else 'NONPROBE_PROJECT_SOURCE'),'path':d['path'],'scope':scope,'line':line,'strings':[v['value'] for v in values],'source_sha256_lf':d['source_sha256_lf'],'status':'SOURCE_GLYPH_OR_TYPOGRAPHY_CANDIDATE_NOT_PIECE_COUNT','note':'Symbols may be text/instructions/pictograms; source scan does not determine visible flat art, font fallback, occurrence count or acceptance.'})
  for scope,kinds in api.items():
   funcs=[f for f in d['functions'] if f['name']==scope];scopes.append({'id':ident('FVCS',d['path'],scope),'source_role':('PROBE_NAMED_SOURCE' if Path(d['path']).name.startswith('probe') else 'NONPROBE_PROJECT_SOURCE'),'path':d['path'],'scope':scope,'categories':sorted(kinds),'current_functions':funcs,'source_sha256_lf':d['source_sha256_lf'],'status':'CURRENT_SOURCE_CANDIDATE_NEEDS_ROLE_CALLER_AND_RUNTIME_CONTEXT','instance_count':None,'individual_piece_count':None})
 for x in refs:
  ref=x['reference'];targets=[]
  if ref.startswith('uid://'):
   targets=sorted(uidmap.get(ref,set()));status='UID_UNRESOLVED_OR_AMBIGUOUS' if len(targets)!=1 else ('UID_MAPPING_TARGET_MISSING_NEEDS_REVIEW' if targets[0] not in blobs else 'COMMITTED_UID_SOURCE_MAPPING_ONLY')
  else:
   target=ref[6:]
   if re.search(r'%|[{}*]',target):status='FORMATTED_OR_WILDCARD_PATH_RUNTIME_ENUMERATION_REQUIRED'
   elif target in blobs:status='EXACT_GIT_PATH_EXISTS_SOURCE_ONLY';targets=[target]
   elif any(p.startswith(target.rstrip('/')+'/') for p in blobs):status='DIRECTORY_PREFIX_RUNTIME_ENUMERATION_REQUIRED'
   elif target.startswith('.godot/'):status='ENGINE_GENERATED_IMPORT_ARTIFACT_NOT_GIT_SOURCE'
   else:status='MISSING_LITERAL_PATH_OR_REFERENCE_FRAGMENT_NEEDS_REVIEW'
  x.update(resolution=status,targets=[{'path':t,'git_blob':blobs.get(t),'ignored_source':ignored(t)} for t in targets])
 old=rd(H/'source_scopes.json')['scopes'];current={(d['path'],d['scope']):d for d in scopes};reconciled=[]
 for x in old:
  d=filemap.get(x['path']);funcs=[] if d is None else [f for f in d['functions'] if f['name']==x['scope']];now=current.get((x['path'],x['scope']))
  state='SOURCE_FILE_MISSING_OR_UNPARSED' if d is None else ('CURRENT_FILE_SCOPE_REBOUND' if x['scope']=='FILE_SCOPE' else ('CURRENT_FUNCTION_REBOUND' if len(funcs)==1 else ('FUNCTION_MISSING_CURRENT_SOURCE' if not funcs else 'FUNCTION_NAME_AMBIGUOUS_NEEDS_REVIEW')))
  reconciled.append({'id':x['id'],'path':x['path'],'scope':x['scope'],'historical_source_sha256_lf':x['source_sha256_lf'],'current_source_sha256_lf':d['source_sha256_lf'] if d else None,'source_byte_identity':d is not None and d['source_sha256_lf']==x['source_sha256_lf'],'binding_status':state,'historical_bounds':[x['start_line'],x['end_line']],'current_functions':funcs,'current_categories':now['categories'] if now else [],'inventory_disposition_unchanged':True,'runtime_acceptance':None})
 oldkeys={(x['path'],x['scope']) for x in old};additional=[x for x in scopes if (x['path'],x['scope']) not in oldkeys];glyph_only=[x for x in additional if x['categories']==['SYMBOL_STRING_CANDIDATE_ROLE_UNREVIEWED']]
 oldglyph=rd(H/'glyph_inventory.json')['sites'];lookup=defaultdict(list)
 for x in glyphs:lookup[(x['path'],tuple(x['strings']))].append(x)
 glyph_reconcile=[]
 for x in oldglyph:
  matches=lookup.get((x['path'],tuple(x['strings'])),[]);glyph_reconcile.append({'id':x['id'],'path':x['path'],'historical_line':x['line'],'historical_scope':x['scope'],'strings':x['strings'],'current_candidate_rows':matches,'status':'EXACT_STRING_CANDIDATES_REBOUND_SOURCE_ONLY' if matches else 'HISTORICAL_STRING_ROW_NOT_EXACTLY_REBOUND_NEEDS_REVIEW','rendered_art_piece_count':None})
 summary={'schema':'reef.current_source_inventory/1','baseline':BASE,'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'parser_package_version':importlib.metadata.version('gdtoolkit'),'tracked_git_files':len(blobs),'input_source_and_sidecar_files':len(inputs),'parsed_gd_files':len(scripts),'parse_failures':len(failures),'production_gd_files':sum(not Path(d['path']).name.startswith('probe') for d in scripts),'probe_gd_files':sum(Path(d['path']).name.startswith('probe') for d in scripts),'frozen_source_scopes':len(old),'frozen_glyph_rows':len(oldglyph),'current_api_or_symbol_candidate_scopes':len(scopes),'additional_source_candidate_scopes':len(additional),'additional_nonprobe_source_candidate_scopes':sum(x['source_role']=='NONPROBE_PROJECT_SOURCE' for x in additional),'additional_probe_source_candidate_scopes':sum(x['source_role']=='PROBE_NAMED_SOURCE' for x in additional),'additional_glyph_only_function_scopes':len(glyph_only),'additional_nonprobe_glyph_only_function_scopes':sum(x['source_role']=='NONPROBE_PROJECT_SOURCE' for x in glyph_only),'current_symbol_string_rows':len(glyphs),'literal_reference_rows':len(refs),'reference_resolution_counts':dict(Counter(x['resolution'] for x in refs)),'caller_rows':len(calls),'caller_binding_counts':dict(Counter(x['binding'] for x in calls)),'parse_status':'ALL_ENUMERATED_GDSCRIPT_PARSED' if not failures else 'PARSE_COVERAGE_GAPS_OPEN','coverage_status':'SOURCE_ONLY_DYNAMIC_NATIVE_RUNTIME_CLOSURE_OPEN','individual_piece_total':None,'accepted_removed':0,'mission_complete':False,'role_limit':'Nonprobe/probe tags are filename categories,not proof of live or unreachable runtime. NonASCII symbol strings remain typography/pictogram candidates,notartpieces.','scope_limit':'Nonignored Git sources in scripts/scenes/assets/shaders/addons plusproject.godot. Probes kept separate. AST and lexical serialized/shader references do not prove active runtime reach, class/receiver binding, guard outcomes, raster appearance, font fallback or device/child/owner acceptance.'}
 wr('CURRENT_SOURCE_INVENTORY.json',dict(summary,files=resources,input_files=[{'path':p,'git_blob':blobs[p],'bytes':len(data[p]),'raw_sha256':sha(data[p])} for p in inputs],scripts=scripts,parse_failure_records=failures,ignored_ancestor_directories=sorted(ignore)))
 wr('SOURCE_SCOPE_RECONCILIATION.json',{'schema':'reef.source_scope_reconciliation/1','baseline':BASE,'frozen_scope_ids_preserved':len(reconciled),'rows':reconciled,'additional_source_candidates':additional,'disposition_change_count':0,'individual_piece_total':None,'accepted_removed':0})
 wr('GLYPH_SCOPE_GAPS.json',{'schema':'reef.glyph_scope_gaps/1','baseline':BASE,'frozen_glyph_ids_preserved':len(glyph_reconcile),'rows':glyph_reconcile,'current_symbol_candidates':glyphs,'additional_glyph_only_function_scopes':glyph_only,'font_identity_and_runtime_closure':'UNRESOLVED','individual_piece_total':None})
 wr('RESOURCE_CALLER_GRAPH.json',{'schema':'reef.resource_caller_graph/1','baseline':BASE,'literal_references':refs,'calls':calls,'class_name_catalog':dict(classmap),'uid_source_mapping':{k:sorted(v) for k,v in uidmap.items()},'binding_scope':'Source-onlypotentialbinding;untyped/typedreceivers,dynamicdispatch,guards/runtimecatalogue andnativecallbacks unclosed. Nevercountthese aspieces orscreens.','accepted_removed':0})
 wr('SOURCE_SUMMARY.json',summary);print('R37_SOURCE_SCAN',json.dumps({k:v for k,v in summary.items() if k not in ['scope_limit','reference_resolution_counts','caller_binding_counts']},sort_keys=True),flush=True)
if __name__=='__main__':run()
