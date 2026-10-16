from pathlib import Path
import json,hashlib,subprocess,re,datetime,importlib.util,os
from gdtoolkit.parser import parser
from lark import Tree,Token
R=Path.cwd();H=R/'docs/handoffs/codex_flat_vector_art_2026-10-07';P=Path(os.environ.get('FVHC_OUTPUT',str(H/'r73_hand_consumer_audit')));D='5120b6d59885dd057937aaf284e73681d8eac9f5'
sha=lambda b:hashlib.sha256(b).hexdigest()
wr=lambda p,d:p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
paths=subprocess.check_output(['git','ls-tree','-r','--name-only',D,'--','scripts','scenes','shaders','project.godot'],text=True).splitlines();src={};trees={};funcs={};classes={}
for path in paths:
 if Path(path).suffix not in ['.gd','.tscn','.tres','.gdshader','.godot']:continue
 raw=subprocess.check_output(['git','show',D+':'+path]);src[path]={'raw':raw,'text':raw.decode('utf-8'),'sha256':sha(raw)}
 if path.endswith('.gd'):
  t=parser.parse(src[path]['text'],gather_metadata=True);trees[path]=t;rows=[];lines=src[path]['text'].splitlines(keepends=True)
  for child in t.iter_subtrees_topdown():
   if child.data=='classname_stmt':classes[path]=str(child.children[0])
   if child.data=='func_def':
    header=child.children[0];name=str(header.children[0]);a=child.meta.line;b=child.meta.end_line;body=''.join(lines[a-1:b]);rows.append({'function':name,'start_line':a,'end_line':b,'body':body,'body_sha256':sha(body.encode())})
  funcs[path]=rows
asset='res://assets/castle/training/ghost_hand.png';refs=[];consumers=[];selected_bodies={}
for path,s in src.items():
 if 'ghost_hand.png' not in s['text']:continue
 lines=s['text'].splitlines();literal=[{'line':i+1,'text':l} for i,l in enumerate(lines) if 'ghost_hand.png' in l]
 if not path.endswith('.gd'):raise AssertionError(('Unexpected nonGD reference; inspect',path))
 t=trees[path];aliases=[]
 for node in t.iter_subtrees_topdown():
  if node.data in ['const_stmt','class_var_stmt']:
   a=node.meta.line;b=node.meta.end_line;body='\n'.join(lines[a-1:b])
   if asset in body:
    names=[str(v) for v in node.scan_values(lambda x:isinstance(x,Token) and x.type=='NAME')];aliases.extend(names[:1])
 tokens=set(aliases);selected=[]
 for row in funcs[path]:
  if asset in row['body'] or any(re.search(r'\b'+re.escape(n)+r'\b',row['body']) for n in tokens):selected.append(row)
 # Resolve only explicit same-function assignment links from a known literal/constant.
 # Local names do not leak across functions; only declared class fields select additional methods.
 fields=set()
 for decl in t.children:
  if isinstance(decl,Tree) and decl.data=='class_var_stmt':
   names=[str(v) for v in decl.scan_values(lambda x:isinstance(x,Token) and x.type=='NAME')]
   if names:fields.add(names[0])
 derived=set();locals_seen=set();binding_edges=[]
 for row in list(selected):
  known=set(tokens);lines_body=row['body'].splitlines()
  for _ in range(4):
   for offset,line in enumerate(lines_body):
    m=re.match(r"\s*(?:var\s+)?([A-Za-z_]\w*)(\.texture)?\s*(?::[^=\n]+)?(?::)?=\s*(.*)$",line)
    if not m:continue
    name,prop,rhs=m.groups()
    if rhs.rstrip().endswith('(') and offset+1<len(lines_body) and 'ghost_hand.png' in lines_body[offset+1]:rhs+=' '+lines_body[offset+1]
    if 'ghost_hand.png' not in rhs and not any(re.search(r'\b'+re.escape(n)+r'\b',rhs) for n in known):continue
    if name not in known:
     known.add(name)
     binding_edges.append({'function':row['function'],'line':row['start_line']+offset,'target':name+('.texture' if prop else ''),'text':line,'rhs_scope':'EXPLICIT_SAME_FUNCTION_SOURCE_VALUE_CANDIDATE'})
    if name in fields:derived.add(name)
    else:locals_seen.add(name)
 selected_names={x['function'] for x in selected}
 for row in funcs[path]:
  if row['function'] not in selected_names and any(re.search(r'\b'+re.escape(n)+r'\b',row['body']) for n in derived):selected.append(row)
 for row in selected:selected_bodies[(path,row['function'])]=dict(row,path=path,file_sha256=s['sha256'],revision=D)
 refs.extend(dict(v,path=path,file_sha256=s['sha256'],revision=D,function=next((r['function'] for r in funcs[path] if r['start_line']<=v['line']<=r['end_line']),'TOP_LEVEL')) for v in literal)
 class_name=classes.get(path);incoming=[]
 for other,os in src.items():
  if other==path:continue
  for i,line in enumerate(os['text'].splitlines(),1):
   # Class identifier occurrences are checked against parser tokens, excluding comments/string-only lookalikes.
   class_match=class_name and re.search(r'\b'+re.escape(class_name)+r'\b',line)
   class_valid=class_match and other in trees and any(str(v)==class_name and getattr(v,'line',None)==i for v in trees[other].scan_values(lambda x:isinstance(x,Token) and x.type=='NAME'))
   literal_match='res://'+path in line
   if class_valid or literal_match:
    f=next((r for r in funcs.get(other,[]) if r['start_line']<=i<=r['end_line']),None)
    incoming.append({'path':other,'line':i,'text':line,'file_sha256':os['sha256'],'revision':D,'matched_as':'AST_CLASS_IDENTIFIER' if class_valid else 'LITERAL_SCRIPT_RESOURCE','function':f['function'] if f else 'TOP_LEVEL','body_sha256':f['body_sha256'] if f else None})
    if f:selected_bodies[(other,f['function'])]=dict(f,path=other,file_sha256=os['sha256'],revision=D)
 # Follow a top-level script-resource alias to its same-file functions. This is still a source-only candidate edge.
 for edge in list(incoming):
  if edge['function']!='TOP_LEVEL' or edge['path'] not in trees:continue
  other=edge['path'];olines=src[other]['text'].splitlines(keepends=True)
  for decl in trees[other].children:
   if not isinstance(decl,Tree) or decl.data not in ['const_stmt','class_var_stmt'] or not (decl.meta.line<=edge['line']<=decl.meta.end_line):continue
   names=[str(v) for v in decl.scan_values(lambda x:isinstance(x,Token) and x.type=='NAME')]
   if not names:continue
   alias=names[0]
   for f in funcs[other]:
    for offset,line in enumerate(f['body'].splitlines()):
     if re.search(r'\b'+re.escape(alias)+r'\b',line):
      i=f['start_line']+offset
      incoming.append({'path':other,'line':i,'text':line,'file_sha256':src[other]['sha256'],'revision':D,'matched_as':'SAME_FILE_TOP_LEVEL_SCRIPT_ALIAS','script_alias':alias,'alias_declaration_line':decl.meta.line,'function':f['function'],'body_sha256':f['body_sha256']})
      selected_bodies[(other,f['function'])]=dict(f,path=other,file_sha256=src[other]['sha256'],revision=D)
 consumers.append({'path':path,'class_name':class_name,'file_sha256':s['sha256'],'revision':D,'literal_reference_count':len(literal),'top_level_asset_aliases':sorted(set(aliases)),'declared_field_bindings':sorted(derived),'local_binding_names':sorted(locals_seen),'binding_edges':binding_edges,'selected_local_functions':[r['function'] for r in selected],'incoming_source_candidates':incoming,'reachability_status':'SOURCE_BRANCHES_ONLY_NO_RUNTIME_OR_ALLCALLER_CLOSURE'})
wr(P/'SOURCE_CENSUS.json',{'source_revision':D,'listed_root_paths':len(paths),'scanned_text_files':len(src),'parsed_gd_files':len(trees),'files':[{'path':p,'sha256':s['sha256'],'bytes':len(s['raw'])} for p,s in sorted(src.items())],'predicate':'Git-declared scripts/scenes/shaders/project.godot text suffixes .gd/.tscn/.tres/.gdshader/.godot. Excludes docs/export/assets/JSON/native/UID loader/content rules. Basename plus exact path source check, not complete resource/semantic reachability.'})
wr(P/'SOURCE_BODIES.json',{'source_revision':D,'function_count':len(selected_bodies),'functions':[selected_bodies[k] for k in sorted(selected_bodies)]})
old=json.loads((H/'r17_pointer_callers/SOURCE_AUDIT.json').read_text(encoding='utf-8'));oldpaths={r['path'] for r in old['old_hand_path_references']};currentpaths={r['path'] for r in refs};same=oldpaths&currentpaths
for row in consumers:
 row['consumer_id']='FVHC-'+sha((asset+'\t'+row['path']).encode())[:12].upper()
 row['classification']='PROBE_ASSET_REQUIREMENT' if Path(row['path']).name.startswith('probe_') else 'CANDIDATE_RENDERING_SOURCE_NOT_RUNTIME_PROOF'
 row['individual_artwork_role_split']='UNRESOLVED_NOT_ADDED_TO_ARTWORK_DENOMINATOR'
 row['scope_note']='Incoming class/type/resource/alias occurrences are source candidates; binding expansion is lexical and does not resolve aliases through arbitrary values, inheritance/native code or indirect dispatch. No absence-of-link retirement claim.'
wr(P/'CONSUMER_MAP.json',{'source_revision':D,'resource':asset,'literal_rows':refs,'consumers':consumers,'prior_r17_source':old['source_revision'],'prior_r17_paths':sorted(oldpaths),'same_non_probe_paths':sorted(same),'added_reference_paths':sorted(currentpaths-oldpaths),'removed_reference_paths':sorted(oldpaths-currentpaths),'method':'AST bounded function/constant data plus explicit local loading-property occurrence expansion and one-edge incoming script/class references. These are source candidates, not proofs of execution. Missing alias/value/native/dynamic/cancel/fallback closure stays open.'})
# Retain the transcript correction as evidence rather than calling probe additions new production consumers.
wr(P/'INTAKE_CORRECTION.json',{'claim_corrected':'R17 predates sourceD, but already listed all16 non-probe resource-reference files including pool activities. The two extra current references are explicit probe requirements. No new production consumer, new art role or new visible context follows from that difference.','old_non_probe_paths':len(oldpaths),'current_reference_paths':len(currentpaths),'same_paths':len(same),'added_paths':sorted(currentpaths-oldpaths),'prior_historical_counts_preserved':True})
print('SCANNED',len(paths),len(src),len(trees),'handrefs',len(refs),'files',len(consumers),'bodybindings',len(selected_bodies))
for c in consumers:print(c['path'],'aliases',c['top_level_asset_aliases'],'bindings',c['declared_field_bindings'],'functions',c['selected_local_functions'],'incoming',[(x['path'],x['function']) for x in c['incoming_source_candidates']])
