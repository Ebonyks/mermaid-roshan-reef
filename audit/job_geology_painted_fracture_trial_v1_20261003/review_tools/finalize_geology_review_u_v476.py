from pathlib import Path
import json,hashlib,datetime,subprocess,shutil
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');J=R/'audit/job_geology_painted_fracture_trial_v1_20261003';L=R/'audit/job_artwork_refinement_live'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert not (J/'previous_t_remote_verified/HOSTED_T_VERIFICATION.json').exists()
raw=subprocess.check_output(['C:/Program Files/GitHub CLI/gh.exe','run','view','37090563245','--repo','Ebonyks/mermaid-roshan-reef','--json','headSha,status,conclusion,updatedAt,jobs,url'],cwd=R)
host=json.loads(raw);assert host['headSha']=='ce154e1452c92252b90f5455989a21726d94ff62' and host['status']=='completed' and host['conclusion']=='success' and all(x['conclusion']=='success' for x in host['jobs'])
host['captured_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();host['status']='EXACT_T_HOSTED_SUCCESS';host['qualification']='Exact prior T hosted machine success, both Linux probes and Windows area-music provenance. Not a new U pass, source/motion/graphics/strict-zero2D/device/child/owner acceptance, all-job completion or integration/release.'
write(J/'previous_t_remote_verified/HOSTED_T_VERIFICATION.json',host)
reg=read(L/'ALL_ITEMS.json');byid={q['id']:q for q in reg['items']}
prefixes={
 'left fragment':('GEO-FOSSIL-LEFT','The left crescent retains its broad golden shell bands and original painted outer silhouette. Its single shared internal fracture must meet the middle piece.'),
 'middle fragment':('GEO-FOSSIL-CENTRE','The middle fragment carries the recognizable central spiral. Its two different shared fracture edges must preserve that focal material through both neighboring joins.'),
 'right fragment':('GEO-FOSSIL-RIGHT','The narrow right crescent retains the painted purple outer stone rim and warm shell bands. Its one shared internal fracture must complement the middle piece without turning into a rectangular strip.')}
h=(J/'index.html').read_text(encoding='utf-8-sig')
for a in [1,2]:
 p=J/f'DIRECT_REVIEW_ATTEMPT0{a}.json';d=read(p)
 # Evaluations gain item-specific observed geometry; scores and evidence remain fixed.
 for o in d['opinions']:
  if o['item'] not in prefixes:continue
  ident,prefix=prefixes[o['item']];old=o['evaluation'];o['evaluation']=prefix+' '+old
  assert old in h;h=h.replace(old,o['evaluation'],1)
  candidate=next(x for x in byid[ident]['candidate_reviews'] if x['attempt']==a);assert candidate['evaluation']==old;candidate['evaluation']=o['evaluation']
 write(p,d)
h=h.replace('The approved intact ammonite source','The existing intact ammonite source').replace('every pixel comes from the original raster with its original UV mapping','the painted material comes from the original raster with its original UV mapping').replace('Its three fragments','Its three fragments')
addition='<p><a href="previous_t_remote_verified/HOSTED_T_VERIFICATION.json">Exact T hosted completion: Linux probes and Windows area-music both successful</a>. New U hosted verification remains separate and pending publication. <a href="BROWSER_REVIEW_V470.json">Temporary browser QA and sequence-control check</a> · <a href="BrowserLatestFragmentsV470.png">Illustrated page preview</a></p>'
needle='This receipt concerns T only; the new review’s publication and hosted status require their own exact revision evidence.</p>'
assert needle in h;h=h.replace(needle,needle+addition,1)
(J/'index.html').write_text(h,encoding='utf-8',newline='\n')
(L/'ALL_ITEMS.json').write_text(json.dumps(reg,separators=(',',':'),ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
page=(L/'all_items.html').read_text(encoding='utf-8-sig').replace('V40 has45 current Geologist opinions/38 inclusive priorities','V41 retains45 current Geologist opinions/38 inclusive priorities and adds separate unbound trial history')
(L/'all_items.html').write_text(page,encoding='utf-8',newline='\n')
proof=read(J/'REGISTER_CHANGE_PROOF_V41.json');proof['after_register_sha256']=sha(L/'ALL_ITEMS.json');proof['item_specific_candidate_evaluations']=True;write(J/'REGISTER_CHANGE_PROOF_V41.json',proof)
shutil.copyfile(Path(__file__),J/'review_tools'/Path(__file__).name)
ip=R/'design/audit_impacts/job-geology-painted-fracture-trial-20261003.json';d=read(ip);d['files']=sorted(set(d['files'])|{x.relative_to(R).as_posix() for x in J.rglob('*') if x.is_file()});d['scope']+=' Exact prior T hosted run37090563245 completed SUCCESS, both jobs; receipt separately preserved. Each fragment receives a written individual geometric evaluation with unchanged draft score.';write(ip,d)
print(json.dumps({'parent_T':'EXACT_SUCCESS','candidate_opinions':24,'item_specific_fragments':6,'current_scores_counts':'UNCHANGED','registry_bytes':(L/'ALL_ITEMS.json').stat().st_size}))
