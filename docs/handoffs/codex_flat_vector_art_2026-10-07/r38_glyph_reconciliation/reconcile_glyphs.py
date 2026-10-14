"""Ordered raw-lexeme/source glyph reconciliation; never visual/art acceptance."""
from pathlib import Path
from collections import defaultdict,Counter
import ast,json,hashlib,subprocess,datetime,unicodedata,importlib.metadata
from gdtoolkit.parser import parser
from lark import Tree
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;O=H/'r37_current_source_inventory';BASE='8f48a0003a8a098658a3414414bd3da3c94f29c2';HIST='92c9fe70319ef46bfaa8f61348a6f51512141ec3'
def sha(b):return hashlib.sha256(b).hexdigest()
def wr(name,d):(P/name).write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
import importlib.util
_bounded_spec=importlib.util.spec_from_file_location('bounded_audit_json',P/'bounded_json.py');_bounded=importlib.util.module_from_spec(_bounded_spec);_bounded_spec.loader.exec_module(_bounded)
def rd(p):return _bounded.read_document(p)
def raw_content(literal):
 if literal[:3] in ['"""',"'''"]:return literal[3:-3]
 return literal[1:-1]
def parse_literals(path,raw):
 text=raw.decode('utf-8-sig');lines=text.splitlines();tree=parser.parse(text,gather_metadata=True);funcs=[];strings=[]
 def funcs_visit(node,prefix=''):
  kind=str(node.data)
  if kind=='class_def':prefix+=str(node.children[0])+'.'
  if kind=='func_def':
   header=next(x for x in node.children if isinstance(x,Tree) and str(x.data) in ['func_header','static_func_header']);end=min(len(lines),node.meta.end_line-(1 if node.meta.end_column==1 else 0));funcs.append({'name':prefix+str(header.children[0]),'start_line':node.meta.line,'end_line':end,'source_sha256_lf':sha(('\n'.join(lines[node.meta.line-1:end])+'\n').encode())})
  for child in node.children:
   if isinstance(child,Tree):funcs_visit(child,prefix)
 funcs_visit(tree)
 def get_scope(line):
  found=[f for f in funcs if f['start_line']<=line<=f['end_line']];return max(found,key=lambda f:f['start_line'])['name'] if found else 'FILE_SCOPE'
 def visit(node,ancestors=[]):
  kind=str(node.data)
  if kind=='string':
   literal=str(node.children[0])
   try:value=ast.literal_eval(literal);decode_status='PYTHON_LITERAL_DECODED_GDSCRIPT_RUNTIME_MAPPING_NOT_EXECUTED'
   except (ValueError,SyntaxError):value=None;decode_status='DECODE_UNRESOLVED'
   statements=[a for a in ancestors if str(a.data) in ['assign_stmt','var_stmt','const_stmt','expr_stmt','return_stmt']];statement=statements[-1] if statements else node;meta=statement.meta;st=text[meta.start_pos:min(meta.end_pos,len(text))];call=next((a for a in reversed(ancestors) if str(a.data).endswith('_call') or str(a.data)=='call'),None);calltext='' if call is None else text[call.meta.start_pos:min(call.meta.end_pos,len(text))]
   hint='DATA_OR_TYPOGRAPHY_CANDIDATE_ROLE_REQUIRES_CONTEXT'
   if '.text' in st and '=' in st:hint='TEXT_PROPERTY_WRITE_RECEIVER_ROLE_AND_REACH_UNPROVEN'
   if 'style_icon_button' in calltext:hint='ICON_BUTTON_ARGUMENT_SOURCE_ROLE_NOT_VISUAL_ACCEPTANCE'
   row={'id':'FVGL-'+sha((path+'|'+str(node.meta.start_pos)+'|'+literal).encode())[:12].upper(),'line':node.meta.line,'column':node.meta.column,'start_pos':node.meta.start_pos,'end_pos':min(node.meta.end_pos,len(text)),'scope':get_scope(node.meta.line),'literal':literal,'raw_content':raw_content(literal),'decoded_value':value,'decode_status':decode_status,'statement':{'start_line':meta.line,'end_line':min(meta.end_line,len(lines)),'bytes':len(st.encode()),'sha256_lf':sha(st.encode()),'excerpt':st[:3000],'excerpt_truncated':len(st)>3000,'ast_kind':str(statement.data)},'enclosing_call_expression':calltext[:1200],'enclosing_call_expression_truncated':len(calltext)>1200,'source_role_hint':hint,'ast_ancestry':[str(a.data) for a in ancestors[-8:]]};strings.append(row)
  for child in node.children:
   if isinstance(child,Tree):visit(child,ancestors+[node])
 visit(tree);return {'path':path,'bytes':len(raw),'raw_sha256':sha(raw),'source_sha256_lf':sha(text.replace('\r\n','\n').encode()),'functions':sorted(funcs,key=lambda f:f['start_line']),'strings':sorted(strings,key=lambda x:x['start_pos'])}
def ordered_match(wants,available):
 chosen=[];cursor=0
 for want in wants:
  found=next((i for i in range(cursor,len(available)) if want in [available[i]['raw_content'],available[i]['decoded_value']]),None)
  if found is None:return None
  chosen.append(available[found]);cursor=found+1
 return chosen

def reconcile(row,hist,current):
 historical=ordered_match(row['strings'],[x for x in hist['strings'] if x['line']==row['line']])
 if historical is None:return {'status':'HISTORICAL_SOURCE_GROUP_UNPROVEN','historical':[],'current_candidates':[],'reason':'Frozen row cannot be proven at recorded historical source line.'}
 scope=historical[0]['scope'];wants=[x['raw_content'] for x in historical]
 if hist['raw_sha256']==current['raw_sha256']:
  lookup={x['start_pos']:x for x in current['strings']};matches=[lookup[x['start_pos']] for x in historical];assert [x['literal'] for x in matches]==[x['literal'] for x in historical]
  return {'status':'CURRENT_LITERAL_POSITIONS_BYTE_IDENTICAL_SOURCE','historical':historical,'current_candidates':[matches],'reason':'Exact file bytes and ordered literal positions preserved;no grouping/reordering assumption.'}
 groups=defaultdict(list)
 for x in current['strings']:
  if x['scope']==scope:groups[x['line']].append(x)
 candidates=[m for values in groups.values() if (m:=ordered_match(wants,values)) is not None]
 if len(candidates)==1:return {'status':'CURRENT_SCOPED_LITERAL_GROUP_REBOUND','historical':historical,'current_candidates':candidates,'reason':'Only exact qualified historical function scope is searched;line shift/string-subset does not imply removal.'}
 if candidates:return {'status':'CURRENT_SCOPE_GROUP_AMBIGUOUS','historical':historical,'current_candidates':candidates,'reason':'Multiple scoped groups satisfy ordered historical literals;all retained without choosing a runtime occurrence.'}
 return {'status':'CURRENT_SCOPED_GROUP_ABSENT_REQUIRES_RETIREMENT_PROOF','historical':historical,'current_candidates':[],'reason':'Literal absent from its actual historical source scope;same symbol elsewhere is not a replacement or accepted retirement.'}
def source_projection(data):
 retained=[x for x in data['strings'] if any(ord(c)>127 for c in x['raw_content']) or isinstance(x['decoded_value'],str) and any(ord(c)>127 for c in x['decoded_value'])]
 return dict(data,strings=retained,ordered_literal_count_total=len(data['strings']),retained_unicode_literal_count=len(retained),projection_scope='Ordered Unicode-literal candidates in these38 frozen-glyph sourcefiles,including punctuation/typography. ASCII literals omitted from this projection but exactfullGit sources are declared inputs. Not global/live glyph coverage or artwork count.')
def git_inputs(revision,paths):
 query=''.join(revision+':'+p+'\n' for p in paths).encode();raw=subprocess.check_output(['git','cat-file','--batch'],input=query,cwd=R);data={};pos=0
 for p in paths:
  end=raw.index(b'\n',pos);head=raw[pos:end].decode().split();assert head[1]=='blob',p;size=int(head[-1]);pos=end+1;data[p]={'bytes':raw[pos:pos+size],'blob':head[0]};pos+=size+1
 assert pos==len(raw);return data

def run():
 old=rd(H/'glyph_inventory.json')['sites'];paths=sorted({x['path'] for x in old});historical_raw=git_inputs(HIST,paths);current_raw=git_inputs(BASE,paths);historical={};current={};inputs=[]
 for path in paths:
  for revision,data,out in [(HIST,historical_raw,historical),(BASE,current_raw,current)]:
   out[path]=parse_literals(path,data[path]['bytes']);inputs.append({'path':path,'revision':revision,'bytes':len(data[path]['bytes']),'sha256':sha(data[path]['bytes']),'git_blob':data[path]['blob']})
 r37=rd(O/'GLYPH_SCOPE_GAPS.json');prior={x['id']:x for x in r37['rows']};graph=rd(O/'RESOURCE_CALLER_GRAPH.json');incoming=defaultdict(list)
 for x in graph['calls']:
  for target in x['callee_candidates']:incoming[(target['path'],target['function'])].append({'path':x['path'],'scope':x['scope'],'line':x['line'],'expression':x['expression'],'binding':x['binding'],'source_role':x['source_role'],'evidence_revision':'efd1f89827ee1dc7d0531474b210c6d457c5a903','evidence_path':(O/'RESOURCE_CALLER_GRAPH.json').relative_to(R).as_posix(),'scope_limit':'Potential same-script/project-class name;not runtime/native/receiver closure.'})
 rows=[];retired=[]
 for row in old:
  path=row['path'];binding=reconcile(row,historical[path],current[path]);reasons=[];hist=binding['historical'];matches=binding['current_candidates'];full_current_group=[]
  if matches:
   first=matches[0][0];full_current_group=[x for x in current[path]['strings'] if x['line']==first['line'] and x['scope']==first['scope']]
  if any('\\' in x['raw_content'] and x['raw_content']!=x['decoded_value'] for x in hist):reasons.append('RAW_ESCAPE_VERSUS_DECODED_VALUE')
  if hist and [x['literal'] for x in hist]!=sorted(x['literal'] for x in hist):reasons.append('AST_ALPHABETICAL_GROUP_ORDER_DIFFERS_FROM_SOURCE_ORDER')
  if any(ord(c)>127 and not unicodedata.category(c).startswith('S') for x in hist for c in x['raw_content']):reasons.append('NON_SYMBOL_CATEGORY_CODEPOINT_PRESENT_SOURCE_ROLE_STILL_REVIEW_REQUIRED')
  if matches and any(x['raw_content'] not in row['strings'] and isinstance(x['decoded_value'],str) and any(ord(c)>127 and unicodedata.category(c).startswith('S') for c in x['decoded_value']) for x in full_current_group):reasons.append('FROZEN_GLYPH_SUBSET_OF_CURRENT_STATEMENT')
  if matches and matches[0][0]['line']!=row['line']:reasons.append('CURRENT_SOURCE_LINE_SHIFT')
  if binding['status']=='CURRENT_SCOPED_GROUP_ABSENT_REQUIRES_RETIREMENT_PROOF' and row['id']=='FVG-868EDDAC69D5':
   before_rev='a587e4ec5e82dbc86d52115ba41f3ae37e2e24f1';retire_rev='2354ee4c5b62ee1adb80ae194f0e37a1ad459e2d';before_raw=subprocess.check_output(['git','show',before_rev+':'+path],cwd=R);after_raw=subprocess.check_output(['git','show',retire_rev+':'+path],cwd=R);before=parse_literals(path,before_raw);after=parse_literals(path,after_raw);a=reconcile(row,historical[path],before);b=reconcile(row,historical[path],after);assert a['current_candidates'] and not b['current_candidates'] and sha(after_raw)==current[path]['raw_sha256'];diff=subprocess.check_output(['git','diff',before_rev,retire_rev,'--',path],cwd=R).decode('utf-8');assert '-\tsparkle.text = "✦"' in diff
   evidence={'id':row['id'],'known_piece_id':'FV-619466CA433F','before_revision':before_rev,'retirement_payload_revision':retire_rev,'current_revision':BASE,'path':path,'before_sha256':sha(before_raw),'retired_source_sha256':sha(after_raw),'current_source_sha256':current[path]['raw_sha256'],'exact_diff_utf8':diff,'diff_sha256_utf8':sha(diff.encode()),'retained_review':{'revision':'ecb9839a374d3260161a19d44039325d561a3509','path':(H/'r32_startup_ui_retirement/REVIEW.json').relative_to(R).as_posix()},'scope':'Already-published bounded menu source statement retirement; no new/accepted artwork removal,global caller/device/child/owner/QA11 acceptance staysopen.'};retired.append(evidence);binding['status']='RETAINED_R32_SCOPED_SOURCE_STATEMENT_RETIREMENT_NOT_ART_ACCEPTANCE';binding['reason']='Exact before/after commit removes sparkle.text in original function;current source bytes match that retirement. Sparkly quality glyph elsewhere remainslive/sourcebound.';reasons.append('PRIOR_BOUNDED_SOURCE_RETIREMENT_NOT_NEW_ART_REMOVAL')
  scope=hist[0]['scope'] if hist else row['scope'];rows.append({'id':row['id'],'path':path,'historical_line':row['line'],'historical_frozen_scope':row['scope'],'historical_strings':row['strings'],'historical_source_revision':HIST,'current_source_revision':BASE,'historical_source_sha256':historical[path]['raw_sha256'],'current_source_sha256':current[path]['raw_sha256'],'prior_r37_status':prior[row['id']]['status'],'binding':binding,'scanner_difference_reasons':reasons,'current_function':[f for f in current[path]['functions'] if f['name']==scope],'potential_incoming_calls':incoming.get((path,scope),[]),'font_and_semantic_role':'NEEDS_ACTUAL_RECEIVER_FONT_FALLBACK_SCENE_AND_ROLE_REVIEW','runtime_occurrence_count':None,'visible_art_piece_count':None,'accepted_removed':0})
 statuses=Counter(x['binding']['status'] for x in rows);open_statuses={'HISTORICAL_SOURCE_GROUP_UNPROVEN','CURRENT_SCOPE_GROUP_AMBIGUOUS','CURRENT_SCOPED_GROUP_ABSENT_REQUIRES_RETIREMENT_PROOF'};open_rows=[x['id'] for x in rows if x['binding']['status'] in open_statuses];prior_gaps=[x for x in rows if x['prior_r37_status'].startswith('HISTORICAL')]
 summary={'schema':'reef.glyph_source_reconciliation/1','revision':'FV-AUDIT-20261014-R38','baseline':BASE,'historical_source_baseline':HIST,'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'parser_package_version':importlib.metadata.version('gdtoolkit'),'frozen_glyph_rows':len(rows),'source_files':len(paths),'source_revision_file_pairs':len(inputs),'source_binding_counts':dict(statuses),'prior_r37_exact_group_gaps':len(prior_gaps),'prior_gaps_current_bound':sum(bool(x['binding']['current_candidates']) for x in prior_gaps),'prior_gap_retained_source_retirements':sum(x['binding']['status'].startswith('RETAINED_R32') for x in prior_gaps),'remaining_source_provenance_gap_ids':open_rows,'remaining_source_provenance_gap_count':len(open_rows),'source_current_glyph_rows':sum(bool(x['binding']['current_candidates']) for x in rows),'retained_bounded_source_statement_retirements':len(retired),'new_accepted_artwork_removals':0,'individual_piece_total':None,'current_distinct_screen_total':None,'mission_complete':False,'source_provenance_status':'ALL_FROZEN_ROWS_SOURCE_ACCOUNTED_FOR' if not open_rows else 'SOURCE_PROVENANCE_GAPS_OPEN','acceptance_scope':'Only frozen glyph-source provenance. Typography/pictogram role,actual reach,receiver/native/guard/font/fallback/style/QA11/device/child/owner/globalsceneclosure remainunreviewed.'}
 wr('GLYPH_RECONCILIATION.json',dict(summary,rows=rows));wr('GLYPH_SOURCE_FILES.json',{'schema':'reef.glyph_source_files/1','inputs':inputs,'historical_files':[source_projection(x) for x in historical.values()],'current_files':[source_projection(x) for x in current.values()],'ordered_literal_count_is_art_piece_count':False});wr('RETAINED_SOURCE_RETIREMENT.json',{'status':'PRIOR_BOUNDED_SOURCE_RETIREMENT_ONLY_NOT_ART_ACCEPTANCE','records':retired,'new_source_retirements':0,'accepted_removed':0,'individual_piece_total':None});wr('GLYPH_SUMMARY.json',summary);print('R38_GLYPH_RECONCILIATION',json.dumps(summary,sort_keys=True),flush=True)
if __name__=='__main__':run()
