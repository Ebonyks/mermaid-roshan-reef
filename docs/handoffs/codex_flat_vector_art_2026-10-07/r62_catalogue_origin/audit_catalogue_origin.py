"""Read-only reconstruction of published audit catalogue IDs; never execute its historical scripts."""
from pathlib import Path
import ast,collections,hashlib,json,re,subprocess
A='92c9fe70319ef46bfaa8f61348a6f51512141ec3';D='5120b6d59885dd057937aaf284e73681d8eac9f5';B='d0f2e17433557d5775463f44576fe7ebf03cf3df';OLD='5e5140fb0f0b636825354b6db8d28da0e9c07446'
STAGE_PATTERN=r'\s*\["([\w.]+)",\s*"([^"]+)",\s*(.*)'
def sha(b):return hashlib.sha256(b).hexdigest()
def git(r,*args):return subprocess.check_output(['git',*args],cwd=r,stderr=subprocess.PIPE)
def doc(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def constant_recipe(text):
 tree=ast.parse(text);ui=[n.value for n in tree.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='ui'for t in n.targets)];assert len(ui)==1
 ui=ast.literal_eval(ui[0]);assert all(len(x)==3 and all(isinstance(v,str)for v in x)for x in ui)
 loops=[n for n in tree.body if isinstance(n,ast.For)and isinstance(n.target,ast.Name)and n.target.id=='g'and isinstance(n.iter,ast.Name)and n.iter.id=='games'];assert len(loops)==1
 body=loops[0].body;assert len(body)==1 and isinstance(body[0],ast.Expr);call=body[0].value;assert isinstance(call,ast.Call)and isinstance(call.func,ast.Attribute)and isinstance(call.func.value,ast.Name)and call.func.value.id=='routes'and call.func.attr=='append'
 row=call.args[0];assert isinstance(row,ast.Dict);fields={k.value:v for k,v in zip(row.keys,row.values)};expr=fields['id'];expected=ast.parse("'game.'+g['id']",mode='eval').body;assert ast.dump(expr)==ast.dump(expected),'Unsupported game ID recipe'
 pat=[n.args[0].value for n in ast.walk(tree)if isinstance(n,ast.Call)and isinstance(n.func,ast.Attribute)and isinstance(n.func.value,ast.Name)and n.func.value.id=='re'and n.func.attr=='match'and n.args and isinstance(n.args[0],ast.Constant)and n.args[0].value==STAGE_PATTERN];assert len(pat)==1
 assert "design/reference/games.json"in text and "scripts/living_world_catalog.gd"in text
 standalone=[n for n in ast.walk(tree)if isinstance(n,ast.BinOp)and isinstance(n.left,ast.Constant)and n.left.value=='standalone.'];assert len(standalone)==1 and ast.unparse(standalone[0])=="'standalone.' + Path(p).stem"
 return {'ui':ui,'stage_pattern':pat[0],'game_prefix':expr.left.value,'game_loop_lines':[loops[0].lineno,loops[0].end_lineno],'ui_assignment_line':next(n.lineno for n in tree.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='ui'for t in n.targets)),'game_id_expression':ast.unparse(expr)}
def reconstruct(recipe,stage_text,catalogue,scenes):
 rows=[]
 for i,l in enumerate(stage_text.splitlines(),1):
  m=re.match(recipe['stage_pattern'],l)
  if m:rows.append({'id':m[1],'origin_kind':'REGISTERED_STAGE_ROW','origin_path':'scripts/living_world_catalog.gd','origin_line':i,'declared_name':m[2],'caller_expression':m[3].strip(),'limits':'Literal source row; neither fresh rendered stage nor complete dynamic/native route.'})
 for ident,name,path in recipe['ui']:rows.append({'id':'ui.'+ident,'origin_kind':'AUDIT_AUTHORED_UI_OVERLAY','origin_path':'build_review_packet.py','origin_line':recipe['ui_assignment_line'],'declared_name':name,'declared_module':path,'limits':'Explicit audit list and source module; does not establish every display/lifecycle path.'})
 for index,g in enumerate(catalogue['games']):rows.append({'id':recipe['game_prefix']+g['id'],'origin_kind':'REFERENCE_GAME_CATALOGUE_LABEL','origin_path':'design/reference/games.json','catalogue_index':index,'catalogue_id':g['id'],'declared_name':g['name'],'declared_family':g['family'],'declared_sources':g.get('sources',[]),'declared_hosts':g.get('host',[]),'limits':'Reference catalogue label, not a promise Main.game equals its suffix. Historical route/state/scores remain assertions at their recorded scope.'})
 for p in scenes:
  if p.endswith('.tscn'):rows.append({'id':'standalone.'+Path(p).stem,'origin_kind':'GIT_SCENE_PATH','origin_path':p,'limits':'Tracked scene existence; production entry/reachability not established.'})
 ids=[r['id']for r in rows];assert len(ids)==len(set(ids)),'Duplicate IDs';return rows

def batch(r,rev,paths):
 q=subprocess.run(['git','cat-file','--batch'],input=''.join(rev+':'+p+'\n'for p in paths).encode(),stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=r);assert q.returncode==0;b=q.stdout;pos=0;out={}
 for p in paths:
  end=b.index(b'\n',pos);head=b[pos:end].decode().split();pos=end+1
  if len(head)==2 and head[1]=='missing':out[p]=None;continue
  assert len(head)==3 and head[1]=='blob';size=int(head[2]);out[p]=b[pos:pos+size];pos+=size;assert b[pos:pos+1]==b'\n';pos+=1
 assert pos==len(b);return out

def function(text,name):
 ls=text.splitlines();hits=[i for i,l in enumerate(ls)if re.match(r'^func '+re.escape(name)+r'\(',l)];assert len(hits)==1,name;start=hits[0];end=next((i for i in range(start+1,len(ls))if ls[i].startswith('func ')),len(ls));body='\n'.join(ls[start:end])+'\n';return {'function':name,'start_line':start+1,'end_line':end,'sha256_lf':sha(body.encode()),'text':body}

def bind_critter(games,main,pause,collection):
 rows=[x for x in games['games']if x['id']=='critters'];assert len(rows)==1;g=rows[0];assert g['name']=='Critter Book collection'and g['family']=='system'and g['sources']==['scripts/collection_system.gd']and'scripts/main.gd'in g['host']
 assert 'const CollectionSystemLogic = preload("res://scripts/collection_system.gd")'in main
 ref=function(main,'_collection_ref');assert 'CollectionSystemLogic.new(self)'in ref['text']and'return _collection_system'in ref['text']
 build=function(pause,'_build_pause');ls=build['text'].splitlines();ix=next(i for i,l in enumerate(ls)if 'var critter_btn :='in l);block=[]
 for l in ls[ix:]:
  if block and re.match(r'\tvar \w+ :=',l):break
  block.append(l)
 callback='\n'.join(block)+'\n';assert 'critter_btn.name = "MenuCritterBookButton"'in callback and'critter_btn.pressed.connect(func():'in callback and'm._collection_ref().open_book()'in callback and'toggle_pause()'in callback
 opened=function(collection,'open_book');draw=function(collection,'_draw_book');context=function(collection,'_context');assert'm._navigation_push("critter_book", self,'in opened['text']and'_draw_book()'in opened['text']and'"🐚  My Critter Book   %d / %d"'in draw['text']
 assert not re.search(r'm\.game\s*=(?!=)',opened['text']+callback),'Book entry cannot be bound by writing a synthetic game token'
 return {'catalogue_id':'game.critters','module':'scripts/collection_system.gd','semantics':'Catalogue subsystem record includes collection/acquisition and saved Critter Book; evidence below binds only saved-book consumer. The catalogue label alone does not prove a Main.game token; dynamic domains remain open.','main_reference':ref,'pause_function_range':[build['start_line'],build['end_line']],'button_callback':callback,'button_callback_sha256_lf':sha(callback.encode()),'open_book':opened,'draw_book':draw,'acquisition_context':context,'overlap':'ui.collection explicitly names same module in original audit list. Retain both catalogue IDs; do not merge or treat acquisition as a shown book state.','partial_only':True,'acquisition_closed':False,'normal_route_closed':False,'QA11':None,'device':None,'child':None,'owner':None}

def analyze(p):
 r=p.parents[3];h=p.parent;source=p/'historical_source/build_review_packet.py.txt';text=source.read_text(encoding='utf-8-sig');recipe=constant_recipe(text);original_cat=json.loads(git(r,'show',A+':design/reference/games.json'));current_cat=json.loads(git(r,'show',D+':design/reference/games.json'));stage=git(r,'show',A+':scripts/living_world_catalog.gd').decode('utf-8-sig');scenes=git(r,'ls-tree','-r','--name-only',A,'--','scenes').decode().splitlines();rows=reconstruct(recipe,stage,original_cat,scenes);frozen=doc(h/'scene_coverage.json')['entries'];assert [x['id']for x in rows]==[x['id']for x in frozen]
 assert git(r,'show',A+':design/reference/games.json')==git(r,'show',D+':design/reference/games.json')and git(r,'show',A+':scripts/living_world_catalog.gd')==git(r,'show',D+':scripts/living_world_catalog.gd');assert original_cat==current_cat
 write(p/'CATALOGUE_ORIGINS.json',{'schema':'reef.catalogue_origin/1','revision':'FV-AUDIT-20261015-R62','original_published_collector':{'revision':OLD,'path':h.relative_to(r).as_posix()+'/build_review_packet.py','sha256':sha(source.read_bytes()),'executed':False,'recipe':recipe},'declared_original_source_revision':A,'current_source_revision':D,'frozen_id_count':len(rows),'origin_counts':dict(collections.Counter(x['origin_kind']for x in rows)),'rows':rows,'scope':'Reconstructed original ID construction at its declared baseline, matched exactly to frozen176IDs. Does not assert historical working-tree execution bytes beyond the verified published files, runtime reachability, rendering or accepted screen/art totals.'})
 catalogue_paths=sorted({q for g in current_cat['games']for key in ['sources','host','evidence']for q in ([e['path']for e in g.get(key,[])]if key=='evidence'else g.get(key,[]))});raws=batch(r,D,catalogue_paths);assert all(b is not None for b in raws.values());eref=[]
 for g in current_cat['games']:
  for e in g.get('evidence',[]):
   b=raws[e['path']];eref.append({'catalogue_id':'game.'+g['id'],'path':e['path'],'declared_historical_sha256':e['sha256'],'current_sha256_git_bytes':sha(b),'current_sha256_lf':sha(b.replace(b'\r\n',b'\n')),'raw_match':sha(b)==e['sha256'],'lf_match':sha(b.replace(b'\r\n',b'\n'))==e['sha256']})
 write(p/'CATALOGUE_SOURCE_BINDINGS.json',{'catalogue_revision':D,'catalogue_header':{k:v for k,v in current_cat.items()if k!='games'},'family_counts':dict(collections.Counter(g['family']for g in current_cat['games'])),'catalogue_rows':60,'declared_source_host_paths':len({q for g in current_cat['games']for key in ['sources','host']for q in g.get(key,[])}),'declared_source_host_evidence_paths':len(raws),'current_paths':[{'path':q,'bytes':len(raws[q]),'sha256':sha(raws[q])}for q in catalogue_paths],'historical_evidence_references':len(eref),'unique_historical_path_hash_pairs':len({(e['path'],e['declared_historical_sha256'])for e in eref}),'current_exact_raw_matches':sum(x['raw_match']for x in eref),'current_exact_lf_matches':sum(x['lf_match']for x in eref),'historical_evidence':eref,'limits':'209reference occurrences include repeated files and differing historical hashes; not209artworks/defects. Matching source bytes do not refresh historical scores/routes or establish current reachability. Differing hashes are stale binding facts, not automatic runtime regressions. All60labels are reference IDs, irrespective of family or suffix resemblance.'})
 current_raw=batch(r,D,['scripts/main.gd','scripts/pause_menu.gd','scripts/collection_system.gd']);binding=bind_critter(current_cat,*(current_raw[q].decode('utf-8-sig')for q in ['scripts/main.gd','scripts/pause_menu.gd','scripts/collection_system.gd']));binding['source_revision']=D;binding['source_hashes']={q:sha(b)for q,b in current_raw.items()};cases=[]
 for mode in ['partial','full']:
  for width in [1280,1600]:
   n=h/'r60_critter_saved_context/native'/f'attempt1_critter_saved_{mode}_{width}'/'capture_manifest.json';d=doc(n);assert d['source_revision']==D and d['saved_mode']==mode and d['aspect']==[width,720]and d['engine']['hash']=='ed1daf0bf001b61586d9930840f2f1394092c079'and d['renderer']=='mobile'and d['time_scale']==1 and not d['normal_route_proved']and not d['actual_child_data']and not d['errors']and len(d['checks'])==35 and all(c['pass']for c in d['checks']);books=[s for s in d['states']if s['snapshot']['book_exists']];assert len(books)==20
   for s in books:
    snap=s['snapshot'];assert snap['game']=='level2'and snap['phase']=='hall'and snap['navigation_top']=='critter_book'and snap['category']in['fish','insect','bird']and snap['caught_count']==(6 if mode=='partial'else 18)and snap['collection_nodes']==0
   cases.append({'revision':B,'path':n.relative_to(r).as_posix(),'sha256':sha(n.read_bytes()),'saved_mode':mode,'aspect':d['aspect'],'checks':35,'book_state_observations':len(books),'already_counted_native_event_files':len(d['states']),'reused_book_states':[{'id':s['id'],'sha256':s['sha256'],'navigation_top':s['snapshot']['navigation_top'],'game':s['snapshot']['game'],'phase':s['snapshot']['phase']}for s in books]})
 binding['original_saved_book_cases']=cases;binding['existing_book_states']=80;binding['new_native_frames']=0;binding['new_artwork_credit']=0;binding['new_partial_alias_credit']='game.critters';write(p/'CRITTER_ALIAS_BINDING.json',binding)
 prior=doc(h/'r57_catalogue_selector_crosswalk/CATALOGUE_CROSSWALK.json');old={x['id']for x in prior['rows']if x['current_partial_slice_retained']};assert len(old)==85 and'game.critters'not in old and'ui.collection'in old;new=old|{'game.critters'};assert len(new)==86
 write(p/'CURRENT_CATALOGUE_CONTEXT_UNION.json',{'schema':'reef.catalogue_partial_union/1','count_unit':'Overlapping named catalogue IDs, not distinct screens or artwork','prior_revision':B,'prior_crosswalk':'r57_catalogue_selector_crosswalk/CATALOGUE_CROSSWALK.json','prior_partial_ids':sorted(old),'new_partial_ids':['game.critters'],'new_evidence':'CRITTER_ALIAS_BINDING.json: explicit original construction+current callback+original R60saved consumer; no suffix inference','current_partial_ids':sorted(new),'current_partial_count':86,'without_current_slice_count':90,'complete_count':0,'entry_count':176,'all_entries_still_incomplete':176,'new_native_files':0,'accepted_removed':0,'mission_complete':False})
 write(p/'SOURCE_PARITY.json',{'baseline':B,'current_source_revision':D,'runtime_changed_paths':git(r,'diff','--name-only',B,'--','scripts','scenes','assets','shaders','project.godot').decode().splitlines(),'no_new_godot_run':True,'normal_profile_read_or_write':False,'new_native_captures':0,'historical_native_guards':'R60SOURCE_PARITY and R61immutable receipts retain per-run4420runtime/4041sidecar/normal8hash proof; not a new native/normal profile measurement.','old_frozen5_exact':all(git(r,'show',B+':'+(h/n).relative_to(r).as_posix())==(h/n).read_bytes()for n in ['per_piece.json','scene_coverage.json','tally.json','source_scopes.json','glyph_inventory.json'])})
 return {'origin_rows':len(rows),'origin_counts':dict(collections.Counter(x['origin_kind']for x in rows)),'catalogue_rows':60,'declared_source_host_paths':105,'declared_source_host_evidence_paths':108,'historical_evidence_references':len(eref),'current_exact_evidence_refs':sum(x['raw_match']for x in eref),'current_different_evidence_refs':sum(not x['raw_match']for x in eref),'new_partial_alias_credits':1,'catalogue_partial':86,'catalogue_without_current_slice':90,'catalogue_complete':0,'existing_original_book_states_rebound':80,'new_native_files':0,'accepted_removed':0,'mission_complete':False}
if __name__=='__main__':
 p=Path(__file__).resolve().parent;write(p/'ANALYSIS_SUMMARY.json',analyze(p));print('R62_CATALOGUE_ORIGIN_ANALYZED176ids60catalogue_labels; explicit game.critters saved-book partial only; no new native/art credit')
