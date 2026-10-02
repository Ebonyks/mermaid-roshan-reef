from pathlib import Path
from html.parser import HTMLParser
import datetime, hashlib, html, json, posixpath, re, shutil, sys
root=Path(sys.argv[1]);family=root/'audit/job_geology_painted_work_v1_20261001'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
d=read(family/'REVIEW.json')
order=['river_invitation','river_task_open','river_earned_completion','fossil_invitation','fossil_task_open','fossil_partial_brush','fossil_brushed','fossil_one_piece','fossil_two_pieces','fossil_earned_completion','pan_invitation','pan_task_open','pan_pan_right','pan_pan_left','pan_partial_pan','pan_earned_completion','geode_invitation','geode_task_open','geode_five_seams_ready','geode_early_crack','geode_middle_open','geode_full_interior_before_award','geode_earned_completion']
d['current_views'].sort(key=lambda x:(order.index(x['state']),x['width']));write(family/'REVIEW.json',d)
p=family/'index.html';s=p.read_text(encoding='utf-8')
cards={m.group(1):m.group(0) for m in re.finditer(r'<article id="([^"]+)">.*?</article>',s,re.S)}
for phase in ['river','fossil','pan','geode']:
 begin='<h2>'+phase.title()+'</h2><div class="grid">';start=s.index(begin)+len(begin);end=s.index('</div>',start)
 text=''
 for x in d['current_views']:
  if not x['state'].startswith(phase+'_'):continue
  card=cards[x['id']];label=x['state'].replace('pan_pan_','pan_').replace('_',' ').title()+' · '+str(x['width'])+' × 720'
  card=card.replace('<h3>'+x['id']+'</h3>','<h3>'+label+'</h3>');text+=card
 s=s[:start]+text+s[end:]
# Three comparisons against the previously accepted local machine boundary, actual images only.
compare='<section id="comparison"><h2>Actual-game before and after</h2><p>These are direct native captures from the prior H source boundary and the current painted-work candidate. They show the exact scope of this change; earlier and current scores stay in their respective reports.</p><div class="grid">'
for state in ['fossil_task_open','pan_task_open','geode_full_interior_before_award']:
 for prior in [True,False]:
  target=('../job_geode_runtime_v1_20261001/attempt_03/native_views/' if prior else 'attempt_04/native_views/')+'geologist_1280_'+state+'.webp'
  compare+='<article><h3>'+state.replace('_',' ').title()+(' — previous H' if prior else ' — current')+'</h3><a href="'+target+'"><img loading="lazy" src="'+target+'" alt="'+state+(' before' if prior else ' after')+'"></a></article>'
compare+='</div></section>'
if 'id="comparison"' not in s:s=s.replace('<section id="priorities">',compare+'<section id="priorities">')
class ProseSpacing(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=False);self.output=[];self.suppressed=[]
 def handle_starttag(self,tag,attrs):
  self.output.append(self.get_starttag_text())
  if tag in ['script','style','code']:self.suppressed.append(tag)
 def handle_endtag(self,tag):
  self.output.append('</'+tag+'>')
  if self.suppressed and self.suppressed[-1]==tag:self.suppressed.pop()
 def handle_data(self,text):
  if not self.suppressed and not text.strip().startswith('GEO-WORK-') and not re.fullmatch('[a-f0-9]{64}',text.strip()):
   text=re.sub(r'(?<=[A-Za-z])(?=\d)', ' ',text).replace('2 D','2D').replace('3 D','3D')
   text=re.sub(r'(?<=[,;:])(?=[A-Za-z0-9])',' ',text)
  self.output.append(text)
 def handle_entityref(self,name):self.output.append('&'+name+';')
 def handle_charref(self,name):self.output.append('&#'+name+';')
 def handle_decl(self,decl):self.output.append('<!'+decl+'>')
parser=ProseSpacing();parser.feed(s);p.write_text(''.join(parser.output),encoding='utf-8',newline='\n')
# Link the current report prominently from the living library; preserve older report descriptions.
p=root/'audit/job_artwork_refinement_live/index.html';s=p.read_text(encoding='utf-8')
marker='<section id="painted-work-latest"><h2>Geology: painted work now mounted</h2><p>Seven exact painted runtime sources and all 46 current ordinary-input native stills directly inspected. Geode cavities reveal embedded crystals; material 4.6 is separate from room 2.8, detached contact 2.7 and clearing 3.9. Known source register: 1,586 entries / 1,206 unique files / 580 inclusive source priorities / 388 source opinions still unassigned. These include shared, rejected and unbound references; they do not claim exhaustive actual-use acceptance.</p><p><a href="../job_geology_painted_work_v1_20261001/index.html">Every current image, individual evaluations and remaining weak items</a></p></section>'
if 'id="painted-work-latest"' not in s:
 anchor=re.search(r'<h1>Mermaid Roshan jobs artwork .*? live review entry</h1>',s).group(0);s=s.replace(anchor,'<h1>Mermaid Roshan jobs artwork — live review entry</h1>'+marker,1);p.write_text(s,encoding='utf-8',newline='\n')
shutil.copyfile(Path(__file__),family/'review_tools'/Path(__file__).name)
# Verify all explicit local report references, their literal paths and internal anchors.
class Refs(HTMLParser):
 def __init__(self):super().__init__();self.refs=[];self.ids=set()
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if a.get('id'):self.ids.add(a['id'])
  for k in ['href','src']:
   if a.get(k):self.refs.append(a[k])
files=[family/'index.html',root/'assets_src/imagegen/geologist_painted_rebuild_v1_20261001/index.html']
records=[]
for page in files:
 f=Refs();f.feed(page.read_text());missing=[]
 for ref in f.refs:
  if ref.startswith(('http:','https:','data:','mailto:')):continue
  path,sep,anchor=ref.partition('#');actual=(page.parent/path).resolve() if path else page.resolve()
  exists=actual.is_file();ok=exists
  if ok and anchor and actual.suffix=='.html':
   t=Refs();t.feed(actual.read_text());ok=anchor in t.ids
  if not ok:missing.append(ref)
 records.append(dict(path=page.relative_to(root).as_posix(),explicit_references=len(f.refs),missing=missing))
receipt=dict(status='PASS' if all(not x['missing'] for x in records) else 'FAIL',checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),pages=records,native_order='Invitation, task open, partial input, earned completion in phase order;1280/1600 paired per state.',qualification='Literal local links/anchors only. Browser render QA separately recorded; not gameplay or owner acceptance.')
write(family/'LIBRARY_LINK_QA.json',receipt)
p=root/'design/audit_impacts/job-geology-painted-work-20261001.json';d=read(p);d['files']=sorted(set(d['files'])|{x.relative_to(root).as_posix() for x in family.rglob('*') if x.is_file()}|{'audit/job_artwork_refinement_live/index.html'});write(p,d)
print(json.dumps(receipt,ensure_ascii=False))
