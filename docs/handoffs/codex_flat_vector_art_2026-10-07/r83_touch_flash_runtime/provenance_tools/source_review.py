from pathlib import Path
import json,subprocess,hashlib,re,datetime
T=Path.cwd();P=T/'docs/handoffs/codex_flat_vector_art_2026-10-07/r83_touch_flash_runtime';B='dd799b2d43871b29d1d6e0503646308a194dad1e'
old=subprocess.check_output(['git','show',B+':scripts/touch_ui.gd']).decode('utf-8');new=(T/'scripts/touch_ui.gd').read_text(encoding='utf-8')
def sha(b):return hashlib.sha256(b).hexdigest()
def funcs(s):
 starts=list(re.finditer(r'^func (\w+)\(',s,re.M));return {m.group(1):s[m.start():starts[i+1].start()if i+1<len(starts)else len(s)]for i,m in enumerate(starts)}
a=funcs(old);b=funcs(new);assert a.keys()==b.keys(); changed=[k for k in a if a[k]!=b[k]];assert changed==['_flash'],changed
source_calls=[]
for k,v in a.items():
 if k!='_flash' and '_flash('in v:source_calls.append({'caller':k,'calls':v.count('_flash('),'function_unchanged':v==b[k],'sha256':sha(v.encode())})
assert sum(x['calls']for x in source_calls)==10
suffix='\tvar tw := flash.create_tween()\n\ttw.tween_property(flash, "modulate:a", 0.0, 0.35)\n\ttw.tween_callback(flash.queue_free)\n'
assert suffix in a['_flash']and suffix in b['_flash']
assert '_circle('not in b['_flash']and 'StyleBoxFlat'not in b['_flash']
raw=subprocess.check_output(['git','show',B+':assets/opera/worlds/props/fx_telegraph_ring.png']);asset=T/'assets/opera/worlds/props/fx_telegraph_ring.png';assert raw==asset.read_bytes()
out={'schema':'reef.touch_flash_source_review/1','baseline':B,'recorded_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_path':'scripts/touch_ui.gd','baseline_git_sha256':sha(old.encode()),'trial_raw_sha256':sha((T/'scripts/touch_ui.gd').read_bytes()),'function_count':len(a),'changed_functions':changed,'all_other_functions_exact':True,'unchanged_local_named_callers':source_calls,'local_flash_call_count':10,'exact_original_tween_free_suffix':suffix,'flash_has_flat_factory_fallback':False,'circle_other_consumers_unchanged':a['_circle']==b['_circle'],'whole_bitmap_source':str(asset.relative_to(T)).replace('\\','/'),'asset_sha256':sha(raw),'asset_bytes':len(raw),'asset_exact_baseline':True,'profile':'Exact approved Godot4.7.2 Mobile/Speedy gates separately recorded','limits':'Narrow named-call/source comparison, not all runtime caller/state closure, visual acceptance, whole-game inventory or accepted removal.'}
(P/'SOURCE_REVIEW.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
I=T/'design/audit_impacts/flat-vector-touch-runtime-20261016.json';d=json.loads(I.read_text(encoding='utf-8'));key=str((P/'SOURCE_REVIEW.json').relative_to(T)).replace('\\','/');d['files']=sorted(set(d['files']+[key]));I.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
print('R83_SOURCE_REVIEW',len(a),'functions;only _flash changed;10callers and original tween unchanged;source exact')
