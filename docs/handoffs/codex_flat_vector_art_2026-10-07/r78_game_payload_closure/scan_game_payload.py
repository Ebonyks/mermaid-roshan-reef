"""Named source edges only. Never infer global reachability from missing names."""
from pathlib import Path
import json,hashlib,subprocess,os,importlib.metadata
from gdtoolkit.parser import parser
from lark import Tree,Token
P=Path(__file__).resolve().parent;R=P.parents[3];D="dd799b2d43871b29d1d6e0503646308a194dad1e"
TARGETS={"_start_game","_start_game_now","_l2_start_slide","_touch_open_picture"}
FIELDS={"fairy_fr","dust_boss_fr"}
REFLECT={"call","callv","call_deferred","call_thread_safe","call_deferred_thread_group","Callable"}
BODIES=TARGETS|{"_fade_cut","_end_galaxy","_on_day_one_hook_event","_day_one_drain_story_clips","_add_wall_picture","_tick_level2","_mg2d_open","_activate_touch_interactable","_prepare_touch_transition"}
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(["git",*a],cwd=R,stderr=subprocess.PIPE)
def literal(n):
 if isinstance(n,Tree)and str(n.data)=="string":
  try:return json.loads(str(n.children[0]))
  except (ValueError,IndexError):return None
 return None

def scan(text,path):
 lines=text.splitlines();tree=parser.parse(text,gather_metadata=True)
 out={k:[]for k in ["named_calls","literal_reflective_calls","ambiguous_literal_dispatch_arguments","target_references","field_references","field_literal_property_access","declarations","function_bodies"]}
 def pretty(n):return n.pretty().strip()if isinstance(n,Tree)else str(n)
 def walk(n,func="<top>",guards=(),ancestors=()):
  if not isinstance(n,Tree):return
  k=str(n.data)
  if k=="func_def":
   hd=next(c for c in n.children if isinstance(c,Tree)and str(c.data)=="func_header");func=str(hd.children[0])
   if func in BODIES:
    end=min(n.meta.end_line,len(lines))
    # gdtoolkit DEDENT metadata can include the next top-level declaration.
    if end>n.meta.line and lines[end-1]and not lines[end-1][0].isspace()and not lines[end-1].startswith("#"):end-=1
    out["function_bodies"].append({"path":path,"function":func,"line":n.meta.line,"end_line":end,"text":"\n".join(lines[n.meta.line-1:end])})
  if k in ["if_branch","elif_branch","else_branch","match_branch"]:
   cond=pretty(n.children[0])if n.children and isinstance(n.children[0],Tree)and str(n.children[0].data)=="expr"else"NO_DIRECT_CONDITION"
   guards=(*guards,{"kind":k,"line":n.meta.line,"condition_AST":cond})
  base={"path":path,"function":func,"line":n.meta.line,"end_line":n.meta.end_line,"guards":list(guards)}
  if k in ["class_var_stmt","func_var_stmt"]:
   decl=n.children[0]
   if isinstance(decl,Tree)and decl.children:
    name=str(decl.children[0]);ds=list(decl.find_data("dict"))
    if name in FIELDS or (func=="_l2_start_slide"and name=="fr"):
     vals={}
     if len(ds)==1:
      for e in ds[0].children:
       if isinstance(e,Tree)and str(e.data)=="c_dict_element"and len(e.children)==2:vals[literal(e.children[0])]=literal(e.children[1])
     out["declarations"].append(dict(base,name=name,AST=pretty(decl),literal_string_pairs={k:v for k,v in vals.items()if isinstance(k,str)and isinstance(v,str)}))
  if k in ["standalone_call","getattr_call"]:
   if k=="standalone_call":name=str(n.children[0]);receiver="self";args=n.children[1:]
   else:
    head=n.children[0];name=str(head.children[-1])if isinstance(head,Tree)and str(head.data)=="getattr"else"";receiver=pretty(head);args=n.children[1:]
   row=dict(base,method=name,receiver_AST=receiver,argument_AST=[pretty(x)for x in args],excerpt="\n".join(lines[n.meta.line-1:n.meta.end_line]))
   if name in TARGETS:out["named_calls"].append(row)
   if name in REFLECT:
    index=1 if name=="Callable"else 0
    sel=literal(args[index])if len(args)>index else None
    if sel in TARGETS:
     object_form=k=="standalone_call"or(name=="Callable")or(k=="getattr_call"and isinstance(n.children[0],Tree)and str(n.children[0].children[0])=="self")
     if object_form:out["literal_reflective_calls"].append(dict(row,selector=sel,classification="Object literal selector candidate; normal entry still unproved"))
     else:out["ambiguous_literal_dispatch_arguments"].append(dict(row,literal_argument=sel,classification="Unknown receiver may be Callable; literal can be callback payload, not selector. No invocation or reachability count."))
   if name in ["get","set","set_deferred","get_indexed","set_indexed"]and args and literal(args[0])in FIELDS:out["field_literal_property_access"].append(row)
  for c in n.children:
   if isinstance(c,Token):
    value=str(c);row=dict(base,line=getattr(c,"line",n.meta.line),name=value,AST_parent=k,ancestor_kinds=list(ancestors[-5:]))
    if value in TARGETS and k!="func_header":out["target_references"].append(row)
    if value in FIELDS:out["field_references"].append(row)
   walk(c,func,guards,(*ancestors,k))
 walk(tree);return out

def main():
 out={k:[]for k in ["named_calls","literal_reflective_calls","ambiguous_literal_dispatch_arguments","target_references","field_references","field_literal_property_access","declarations","function_bodies"]};files=[]
 paths=[p for p in git("ls-tree","-r","--name-only",D,"--","scripts").decode().splitlines()if p.endswith(".gd")]
 for i,path in enumerate(paths,1):
  raw=git("show",D+":"+path);probe=Path(path).name.startswith("probe")or Path(path).stem.endswith("_test_case");rows=scan(raw.decode("utf-8-sig"),path)
  files.append({"path":path,"revision":D,"bytes":len(raw),"sha256":sha(raw),"probe_or_test_filename":probe,"parse":"PASS"})
  for k,rs in rows.items():out[k].extend(dict(x,probe_or_test_filename=probe)for x in rs)
  if i%100==0:print("R78_PARSED",i,"of",len(paths),flush=True)
 resources=[]
 for path in git("ls-tree","-r","--name-only",D,"--","scenes","project.godot").decode().splitlines():
  if not path.endswith((".tscn",".tres",".godot")):continue
  raw=git("show",D+":"+path);hits=[{"line":i+1,"text":l}for i,l in enumerate(raw.decode("utf-8-sig").splitlines())if any(x in l for x in TARGETS|FIELDS)]
  resources.append({"path":path,"revision":D,"bytes":len(raw),"sha256":sha(raw),"target_text_candidates":hits,"scope":"Text references only, no native/external/resource dynamic closure"})
 summary={"parsed_scripts":len(files),"named_calls":len(out["named_calls"]),"literal_reflective_candidates":len(out["literal_reflective_calls"]),"non_test_named_calls":sum(not x["probe_or_test_filename"]for x in out["named_calls"]),"non_test_literal_reflective_candidates":sum(not x["probe_or_test_filename"]for x in out["literal_reflective_calls"]),"resource_files_checked":len(resources),"non_test_field_references":sum(not x["probe_or_test_filename"]for x in out["field_references"]),"global_unreachability_proved":False,"dictionary_mutation_alias_domain_closed":False}
 doc={"schema":"reef.game_payload_source_graph/1","source_revision":D,"scanner_sha256":sha(Path(__file__).read_bytes()),"parser_version":importlib.metadata.version("gdtoolkit"),"target_names":sorted(TARGETS),"files":files,**out,"resources":resources,"summary":summary,"limits":"Exact named syntax/arguments/guards and initializer proof only. Method references are not extra invocations. Non-test filenames include debug code. A mutable Dictionary is not a frozen payload. Reflected variable selectors, receiver aliases, external/native paths and all other game writers stay open. No absent-name test or source producer grants runtime reachability, scene coverage, art/style/replacement or acceptance credit."}
 dest=Path(os.environ.get("R78_ANALYSIS_OUTPUT",str(P)));dest.mkdir(exist_ok=True,parents=True);(dest/"SOURCE_PAYLOAD_GRAPH.json").write_text(json.dumps(doc,indent=2)+"\n",encoding="utf-8",newline="\n")
 print("R78_SOURCE_SUMMARY",json.dumps(summary),flush=True)
if __name__=="__main__":main()
