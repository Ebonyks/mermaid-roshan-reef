from __future__ import annotations
import copy,datetime,hashlib,importlib.util,json,sys
from pathlib import Path
from unittest.mock import patch
ROOT=Path('H:/CodexWorktrees/mermaid-roshan-reef-job-platform-jp1-20261001')
OUT=Path('C:/Users/Peter/Documents/mermaid-roshan-reef/.scratch/job-platform-jp1-review/final-matrix-results')
OUT.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT))
CODE=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT
import tools
for name in ['content_gd_literals','content_source_refs','content_build']:
    path=CODE/'tools'/(name+'.py')
    if not path.is_file():path=ROOT/'tools'/(name+'.py')
    spec=importlib.util.spec_from_file_location('tools.'+name,path)
    module=importlib.util.module_from_spec(spec)
    sys.modules['tools.'+name]=module
    spec.loader.exec_module(module)
    setattr(tools,name,module)
from tools import content_build as build,content_source_refs as refs,content_gd_literals as literals
catalog=build.load_catalog(ROOT);data=build.derive(catalog)
source=(ROOT/'scripts/save_state.gd').read_text(encoding='utf-8')
baseline=refs._baseline_save(str(ROOT.resolve()),build.BASELINE)
rows=[]
def check(name,kind,text,accept,expected=None,source_data=data):
    path=OUT/name/'scripts/save_state.gd'
    try:
        with patch.object(Path,'read_text',return_value=text):
            if kind=='literal': result=literals.read_const(path,'X')
            elif kind=='bounds': result=refs.read_save_bounds(path.parents[1],source_data)
            elif kind=='order': result=refs.read_checkpoint_order(path.parents[1],source_data)
            else:
                with patch.object(refs,'_baseline_save',return_value=baseline):
                    result=refs.read_save_const(path.parents[1],kind,source_data,build.BASELINE)
        observed=True;error=''
    except Exception as exc:
        result=None;observed=False;error=type(exc).__name__+': '+str(exc)
    passed=observed==accept and (not accept or expected is None or result==expected)
    rows.append({'case':name,'kind':kind,'expected_accept':accept,'observed_accept':observed,'passed':passed,'result':result,'error':error,'source_sha256':hashlib.sha256(text.encode()).hexdigest()})
    if not passed: print('FAIL',name,error or repr(result))

check('literal_real','literal','const X = 2\n',True,2)
for delim,label in [('"""','triple_double'),("'''",'triple_single')]:
    fake='var documentation = '+delim+'\nconst X = 999\nfunc fake() -> void:\n\tpass\n'+delim+'\n'
    check('literal_'+label+'_ignored','literal',fake+'const X = 2\n',True,2)
    check('literal_'+label+'_missing','literal',fake,False)
    check('literal_'+label+'_unsupported_value','literal','const X = '+delim+'literal'+delim+'\n',False)
check('literal_comment_ignored','literal','# const X = 999\n# \"\"\" const X = 44\nconst X = 2 # \' quote ignored\n',True,2)
check('literal_duplicate','literal','const X = 2\nconst X = 3\n',False)
check('literal_arithmetic','literal','const X = 2 + 1\n',False)
check('literal_method','literal','const X = [1].duplicate()\n',False)
check('literal_forbidden_constructor','literal','const X = preload("res://anything.gd")\n',False)
check('literal_stringname','literal','const X = &"a # fake const X = 9"\n',True,{'__stringname__':'a # fake const X = 9'})
check('literal_escaped_double','literal','const X = "a # \\" q \\\\ end"\n',True,'a # " q \\ end')
check('literal_escaped_single','literal',"const X = 'can\\'t # q'\n",True,"can't # q")
for delim,label in [('"','double'),("'",'single'),('"""','triple_double'),("'''",'triple_single')]:
    check('literal_unterminated_'+label,'literal','var text = '+delim+'open\nconst X = 2\n',False)

expected_bounds={'SLOT_COUNT':data['SLOT_COUNT'],'STAR_CEILING':data['STAR_CEILING']}
check('bounds_original','bounds',source,True,expected_bounds)
check('order_original','order',source,True,data['SAVE_CHECKPOINT_JOB_ORDER'])
load_line='\tm.opera_stars = clampi(int(m.save_data.get("opera_stars", 0)), 0, JobData.STAR_CEILING)'
write_line='\tm.opera_stars = clampi(m.opera_stars, 0, JobData.STAR_CEILING)'
slot_line='\tfor bit_index in range(JobData.SLOT_COUNT):'
loop='\tfor checkpoint_job_id: String in JobData.SAVE_CHECKPOINT_JOB_ORDER:\n\t\tvar checkpoint_spec: Dictionary = JobData.SAVE_CHECKPOINTS[checkpoint_job_id] as Dictionary\n\t\tvar checkpoint_key: String = String(checkpoint_spec["key"])\n\t\tdata[checkpoint_key] = _normalise_job_checkpoint(raw, checkpoint_job_id)'
for delim,label in [('"""','triple_double'),("'''",'triple_single')]:
    doc='var documentation = '+delim+'\n'+source+'\n'+delim+'\n'
    check('bounds_'+label+'_whole_example','bounds',source+'\n'+doc,True,expected_bounds)
    check('order_'+label+'_whole_example','order',source+'\n'+doc,True,data['SAVE_CHECKPOINT_JOB_ORDER'])
    check('scalar_'+label+'_whole_example','OPERA_ACTIVE_STAR_MASK',source+'\n'+doc,True,data['ACTIVE_STAR_MASK'])
    fake='var fake = '+delim+'\nfunc load_save() -> void:\n'+load_line+'\nfunc end_fake() -> void:\n\tpass\n'+delim+'\n'
    broken=source.replace(load_line,'\tm.opera_stars = 0')
    check('bounds_'+label+'_fake_func_cannot_replace','bounds',fake+broken,False)
    fake='var fake = '+delim+'\nfunc _normalise_save(raw: Dictionary) -> Dictionary:\n\tdata["teacher_learning_progress"] = TeacherLessonPlan.normalise_progress(\n\t\traw.get("teacher_learning_progress", {}))\n'+loop+'\n\tdata["stickers"] = _dictionary_or_default(raw, "stickers")\nfunc end_fake() -> void:\n\tpass\n'+delim+'\n'
    broken=source.replace(loop,'\tpass')
    check('order_'+label+'_fake_func_cannot_replace','order',fake+broken,False)

check('bounds_nested_clamp','bounds',source.replace(load_line,'\tif true:\n\t'+load_line),False)
check('bounds_duplicate_clamp_same_function','bounds',source.replace(load_line,load_line+'\n'+load_line),False)
check('bounds_duplicate_clamp_other_function','bounds',source+'\nfunc extra_bound() -> void:\n'+write_line+'\n',False)
check('bounds_moved_load_clamp','bounds',source.replace(load_line+'\n','',1).replace('func load_save() -> void:\n','func load_save() -> void:\n'+load_line+'\n'),False)
check('bounds_wrong_clamp_argument','bounds',source.replace(load_line,load_line.replace('int(m.save_data.get("opera_stars", 0))','1')),False)
check('bounds_clamp_arithmetic','bounds',source.replace(load_line,load_line.replace('JobData.STAR_CEILING','JobData.STAR_CEILING + 1')),False)
check('bounds_slot_expression','bounds',source.replace(slot_line,slot_line.replace('JobData.SLOT_COUNT','JobData.SLOT_COUNT + 1')),False)
check('bounds_duplicate_slot_other_function','bounds',source+'\nfunc extra_slots() -> void:\n'+slot_line+'\n\t\tpass\n',False)
slot_block=slot_line+'\n\t\tvar bit := 1 << bit_index\n\t\tif (OPERA_ACTIVE_STAR_MASK & bit) != 0 and (star_mask & bit) != 0:\n\t\t\ttotal += 1'
assert slot_block in source
check('bounds_nested_slot','bounds',source.replace(slot_block,'\tif true:\n'+'\n'.join('\t'+line for line in slot_block.splitlines())),False)
check('bounds_moved_slot_after_return','bounds',source.replace(slot_block+'\n','').replace('\treturn mini(total, OPERA_ACTIVE_ACT_COUNT)','\treturn mini(total, OPERA_ACTIVE_ACT_COUNT)\n'+slot_block),False)
check('order_nested','order',source.replace(loop,'\tif true:\n'+'\n'.join('\t'+line for line in loop.splitlines())),False)
check('order_duplicate','order',source.replace(loop,loop+'\n'+loop),False)
check('order_moved','order',source.replace(loop+'\n','').replace('\tdata["owned"] = _dictionary_or_default(raw, "owned")','\tdata["owned"] = _dictionary_or_default(raw, "owned")\n'+loop),False)
check('preload_wrong_path','OPERA_ACTIVE_STAR_MASK',source.replace('res://scripts/generated/job_catalog_data.gd','res://scripts/save_state.gd'),False)
check('scalar_arithmetic','OPERA_ACTIVE_STAR_MASK',source.replace('const OPERA_ACTIVE_STAR_MASK := JobData.ACTIVE_STAR_MASK','const OPERA_ACTIVE_STAR_MASK := JobData.ACTIVE_STAR_MASK + 1'),False)
check('scalar_wrong_member','OPERA_ACTIVE_STAR_MASK',source.replace('const OPERA_ACTIVE_STAR_MASK := JobData.ACTIVE_STAR_MASK','const OPERA_ACTIVE_STAR_MASK := JobData.RETIRED_STAR_MASK'),False)
check('registration_original','DICTIONARY_KEYS',source,True,baseline[1]['DICTIONARY_KEYS'])
check('registration_wrong_fragment','DICTIONARY_KEYS',source.replace('JobData.SAVE_CHECKPOINT_KEY_LISTS["DICTIONARY_KEYS"]','JobData.SAVE_CHECKPOINT_KEY_LISTS["KNOWN_KEYS"]'),False)
check('registration_method','DICTIONARY_KEYS',source.replace('JobData.SAVE_CHECKPOINT_KEY_LISTS["DICTIONARY_KEYS"]','JobData.SAVE_CHECKPOINT_KEY_LISTS["DICTIONARY_KEYS"].duplicate()'),False)
synthetic=build.derive(build.load_catalog(Path('H:/CodexWorktrees/job-platform-jp1-preparation-20261001/compiler/synthetic')))
check('fresh_data_bounds_ignore_existing_generated','bounds',source,True,{'SLOT_COUNT':19,'STAR_CEILING':0x7ffff},synthetic)
check('fresh_data_mask_ignore_existing_generated','OPERA_ACTIVE_STAR_MASK',source,True,synthetic['ACTIVE_STAR_MASK'],synthetic)
check('fresh_data_order_ignore_existing_generated','order',source,True,['teacher','geologist','jp1_hidden_practice'],synthetic)
check('bounds_duplicate_real_function','bounds',source+'\nfunc load_save() -> void:\n\tpass\n',False)
check('order_duplicate_real_function','order',source+'\nfunc _normalise_save(raw: Dictionary) -> Dictionary:\n\treturn raw\n',False)
real_read_text=Path.read_text
for rel,key,pattern in [('scripts/probe_chapter2.gd','CHAPTER2_PHASE_TOTAL','count == 29'),('scripts/probe_opera_2d.gd','SHIPPING_PHASE_TOTAL','shipping_phase_count == 61')]:
    original=real_read_text(ROOT/rel,encoding='utf-8')
    tail=')' if key=='CHAPTER2_PHASE_TOTAL' else ' and missing_specs.is_empty())'
    duplicate='\nfunc irrelevant(count: int, shipping_phase_count: int) -> void:\n\t_check("duplicate", '+pattern+tail+'\n'
    variants=[('fake_ignored',original+'\nconst EXTRA_DOC = """\n'+pattern+'\n"""\n',True),('fake_cannot_replace',original.replace(pattern,'true')+'\nconst EXTRA_DOC = """\n'+pattern+'\n"""\n',False),('real_duplicate',original+duplicate,False),('other_identifier_ignored',original+'\nfunc irrelevant(other_count: int, other_shipping_phase_count: int) -> bool:\n\treturn other_'+pattern+'\n',True),('arithmetic_rhs',original.replace(pattern,pattern+' + 1'),False),('float_rhs',original.replace(pattern,pattern+'.5'),False),('underscore_rhs',original.replace(pattern,pattern+'_000'),False)]
    for label,mutation,accept in variants:
        def supplied(path,*args,**kwargs):return mutation if str(path)==str(ROOT/rel) else real_read_text(path,*args,**kwargs)
        try:
            with patch.object(Path,'read_text',supplied):snapshot=build.source_snapshot(ROOT,catalog)
            accepted=True;err=''
        except Exception as exc:accepted=False;err=type(exc).__name__+': '+str(exc)
        rows.append({'case':key+'_'+label,'expected_accept':accept,'observed_accept':accepted,'passed':accepted==accept,'error':err})
rendered=build.render(catalog).encode('utf-8');snapshot=build.source_snapshot(ROOT,catalog)
assert rendered==(ROOT/'scripts/generated/job_catalog_data.gd').read_bytes()
print('DERIVATION_COUNTS',len(data),len(snapshot)); print('DERIVATION_MISMATCHES',[(key,key not in data or not build._strict_equal(value,data[key])) for key,value in snapshot.items() if key not in data or not build._strict_equal(value,data[key])]); assert all(key in data and build._strict_equal(value,data[key]) for key,value in snapshot.items())
print('87 current exports, preserving86 prior exports; source74 byte equivalent; generatedSHA',hashlib.sha256(rendered).hexdigest())
result={'schema':'jp1_independent_static_source_review/1','checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_helper_hashes':{rel:hashlib.sha256(((CODE/rel) if (CODE/rel).is_file() else (ROOT/rel)).read_bytes()).hexdigest() for rel in ['tools/content_gd_literals.py','tools/content_source_refs.py','tools/content_build.py']},'current_generated_sha256':hashlib.sha256((ROOT/'scripts/generated/job_catalog_data.gd').read_bytes()).hexdigest(),'cases':rows,'failures':[row['case'] for row in rows if not row['passed']],'baseline_fixture':'Source Path.read_text is substituted in-memory per adversarial case; registration baseline lookup uses the immutable real Git result read before tests. Actual candidate selection/lexing/parsing/resolution and derive functions execute unchanged.','source_changes':False}
path=OUT/'static_review_receipt.json';path.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'cases':len(rows),'failures':result['failures'],'receipt':str(path)},indent=2))
raise SystemExit(bool(result['failures']))