"""Adversarial checks for source-only inventory boundaries."""
from pathlib import Path
import importlib.util,json,hashlib,subprocess
P=Path(__file__).resolve().parent;spec=importlib.util.spec_from_file_location('scan_current',P/'scan_source_inventory.py');scan=importlib.util.module_from_spec(spec);spec.loader.exec_module(scan)
checks=[]
def record(name,condition):
 assert condition,name;checks.append({'case':name,'result':'PASS'})
fixture='''class_name SourceCase
extends Node2D
# draw_circle(Vector2.ZERO, 9.0, Color.WHITE)
# load("res://comment-only.png")
func glyph_only(flag: bool) -> String:
	return "♫" if flag else "♫̸"
func raster_only(image: Image) -> void:
	image.fill(Color.WHITE)
func paths(key: String) -> void:
	load("res://present.png")
	load("res://assets/%s.png" % key)
	load("uid://unknown")
	call("_hidden")
func ordinary_text() -> String:
	return "one + one = two"
'''
d=scan.parse_script('scripts/case.gd',fixture.encode())
record('comment draw/load excluded from AST',not any(x['line'] in [3,4] for x in d['calls']) and not any('comment-only' in x['value'] for x in d['strings']))
record('glyph-only function independently retained',any(x['scope']=='glyph_only' and scan.pictogram(x['value']) for x in d['strings']))
record('function bounds do not absorb next header',next(x for x in d['functions'] if x['name']=='glyph_only')['end_line']<next(x for x in d['functions'] if x['name']=='raster_only')['start_line'])
record('raster API remains candidate not artwork',any('RASTER_OR_IMAGE_API_CANDIDATE_RECEIVER_UNPROVEN' in scan.categories(x) for x in d['calls'] if x['scope']=='raster_only'))
load=[x for x in d['calls'] if x['callee_expression']=='load']
record('literal load first argument recognized',any(x['literal_first_argument']=='res://present.png' for x in load))
record('formatted load not treated as exact literal',any('% key' in x['expression'] and x['literal_first_argument'] is None for x in load))
record('unknown UID remains explicit source reference',any(x['value']=='uid://unknown' for x in d['strings']))
record('dynamic dispatch retained without callee proof',any(x['callee_expression']=='call' and x['literal_first_argument']=='_hidden' for x in d['calls']))
record('ordinary ASCII operators not pictogram candidates',not scan.pictogram('one + one = two'))
summary=json.loads((P/'SOURCE_SUMMARY.json').read_text(encoding='utf-8'))
reconcile=json.loads((P/'SOURCE_SCOPE_RECONCILIATION.json').read_text(encoding='utf-8'));glyph=json.loads((P/'GLYPH_SCOPE_GAPS.json').read_text(encoding='utf-8'));R=P.parents[3];H=P.parent
old=json.loads((H/'source_scopes.json').read_text(encoding='utf-8'))['scopes'];oldglyph=json.loads((H/'glyph_inventory.json').read_text(encoding='utf-8'))['sites']
record('all 369 frozen scope IDs preserved in order',[x['id'] for x in reconcile['rows']]==[x['id'] for x in old] and len(old)==369)
record('all 348 frozen glyph IDs preserved in order',[x['id'] for x in glyph['rows']]==[x['id'] for x in oldglyph] and len(oldglyph)==348)
record('source-only denominator remains unknown',summary['individual_piece_total'] is None and summary['accepted_removed']==0 and not summary['mission_complete'])
record('probe and nonprobe additional scope counts separate',summary['additional_source_candidate_scopes']==summary['additional_nonprobe_source_candidate_scopes']+summary['additional_probe_source_candidate_scopes'])
record('glyph-only StartMenu synchronization gap recorded',any(x['path']=='scripts/start_menu.gd' and x['scope']=='_sync_option_labels' for x in glyph['additional_glyph_only_function_scopes']))
record('current input parse failures explicit and zero',summary['parse_failures']==0 and summary['parse_status']=='ALL_ENUMERATED_GDSCRIPT_PARSED')
shader=b'// "res://comment.tres"\n/* "res://block.tres" */\nuniform sampler2D art : source_color = "res://actual.png"; // "uid://comment"\n'
record('shader comments excluded while quoted source retained',scan.resource_literals(shader,'.gdshader')==[{'line':3,'scope':'RESOURCE_FILE','reference':'res://actual.png','reference_kind':'LEXICAL_RESOURCE_OR_SHADER_STRING_NOT_RUNTIME_PROOF'}])
serialized=b'; "res://comment.tres"\npath="res://actual.tres" # "res://inline.tres"\n'
record('serialized full-line and inline comments excluded',len(scan.resource_literals(serialized,'.tres'))==1 and scan.resource_literals(serialized,'.tres')[0]['reference']=='res://actual.tres')
nested=scan.parse_script('nested.gd',b'extends Node2D\nclass Alpha:\n\textends Node2D\n\tfunc _draw() -> void:\n\t\tdraw_circle(Vector2.ZERO, 1.0, Color.WHITE)\nclass Beta:\n\tfunc _draw() -> void:\n\t\tdraw_rect(Rect2(), Color.WHITE)\nfunc next() -> void:\n\tpass\n')
record('nested class methods retain distinct qualified scopes',[(x['name'],x['class_scope']) for x in nested['functions']]==[('Alpha._draw','Alpha'),('Beta._draw','Beta'),('next','')] and {x['scope'] for x in nested['calls'] if scan.categories(x)}=={'Alpha._draw','Beta._draw'})
out={'status':'PASS_SOURCE_ONLY_NO_ART_OR_RUNTIME_ACCEPTANCE','cases':checks,'case_count':len(checks),'scanner_sha256':hashlib.sha256((P/'scan_source_inventory.py').read_bytes()).hexdigest(),'source_summary_sha256':hashlib.sha256((P/'SOURCE_SUMMARY.json').read_bytes()).hexdigest(),'coverage_scope':'Adversarial syntax/source boundaries only;not visual/receiver/native/dynamic/device/child/owner acceptance.'};(P/'SOURCE_STRESS.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n');print('R37_SOURCE_STRESS',len(checks),'PASS')
