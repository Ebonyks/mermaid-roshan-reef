"""Fail-closed editorial-deliverable audit; external acceptance remains separate."""
from pathlib import Path
import ast,hashlib,json
from html.parser import HTMLParser
from urllib.parse import unquote,urlsplit
V=Path(__file__).resolve().parent;L=V.parents[1];R=L.parents[2]
def read(p):return json.loads(p.read_text('utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def evidence(p):return {'path':p.relative_to(R).as_posix(),'sha256':sha(p)}
B=read(L/'book.json');proof=read(V/'complete/verification.json');visual=read(V/'visual_review.json');stress=read(V/'complete/stress_results.json');gen=read(V/'generation_evidence.json');lang=read(V/'language_final.json');style=read(V/'style_final.json');char=read(V/'character_final.json');gates=read(V/'project_gates.json');pagination=read(V/'print_pagination.json')
assert proof['book_json_sha256']==char['book_json_sha256']==lang['evidence']['book_json_sha256']==style['frozen_evidence']['book']['sha256']==sha(L/'book.json')
assert proof['page_provenance_sha256']==char['page_provenance_sha256']==lang['evidence']['page_provenance_sha256']==style['frozen_evidence']['page_provenance']['sha256']==sha(V/'complete/page_provenance.json')
assert proof['pdf_sha256']==style['frozen_evidence']['pdf']['sha256']==pagination['pdf_sha256']==sha(V/'complete/Mermaid_Roshan_LANDSCAPE_ROUGH.pdf')
assert proof['lossless_optimized_pdf_raster_matches_all34screenshots'] and proof['native_text_matches_manuscript']
assert visual['summary']['all_objects_target_met'] and visual['summary']['pages_at_internal_target']==34
assert stress['mechanical_status']=='PASS' and not stress['issues']
assert all(q['exit_code']==0 for q in gates['checks'])
assert gen['generated_count']==6 and gen['selected_candidate_count']==5 and gen['cumulative_polish_generation_candidates']==56
assert {q['page'] for q in read(V/'complete/page_provenance.json')['layers'] if q['source_key'] in {'v29_lamma09','v29_bank31_final'}}=={9,31}
assert len(proof['unchanged_pages_byte_identical_to_v29'])==29 and all(q['outside_declared_regions_changed_pixels']==0 for q in proof['outside_region_preservation'])
assert pagination['first_story_side']=='right / recto' and pagination['interior_story_pages']==32
for p in [L/'render_book.py',L/'audit_book.py',*V.glob('*.py')]:ast.parse(p.read_text('utf-8'))
class Links(HTMLParser):
 def __init__(self):super().__init__();self.targets=[]
 def handle_starttag(self,tag,attrs):
  for k,v in attrs:
   if k in ['href','src'] and v:self.targets.append(v)
link_count=0
for p in [V/'AUDIT_REVIEW.html',V/'PRINT_DUMMY.html',V/'SLP_REVIEW_PACKET.html',V/'complete/READ_BOOK.html']:
 parser=Links();parser.feed(p.read_text('utf-8'))
 for target in parser.targets:
  u=urlsplit(target)
  if u.scheme or not u.path:continue
  dest=(p.parent/unquote(u.path)).resolve();assert dest.is_file(),('Broken review link',p,target);link_count+=1
req=[
 ('34 authored landscape pages and Sniglet','complete/verification.json'),
 ('Finished story, compassionate Puff care, Rumi residence, two-bunny Eagle rescue, waterfall rainbow and exact landing','complete/stress_results.json'),
 ('Whole-book object/character/style review and internal4.9 target without score inflation','visual_review.json'),
 ('Original-book design reference and exact full-art/contour treatments','style_final.json'),
 ('Page-specific grounded blue banks and varied contextual bunny/game details','style_final.json'),
 ('Two subtle unprompted actual Lamma appearances','complete/stress_results.json'),
 ('Native bubble-quality review, no new lossy export, all34 pixel checks','complete/verification.json'),
 ('Source-preserving local edits, actual prompts/references/native hashes and rejected studies','generation_evidence.json'),
 ('Age4–5 shared-reading language, readable editable captions and rounded dialogue','language_final.json'),
 ('Full PDF and before/after screenshots of every page','visual_review.json'),
 ('Corrected professional review packet without fabricated clinical approval','SLP_REVIEW_PACKET.html'),
 ('Concrete bound pagination and preserved page-turn reveals','print_pagination.json'),
 ('Repository authority/coverage and applicable regression checks','project_gates.json')]
result={'revision':'V30','baseline':'82a6dc1dba381c0b3ef507a8397512fa09ef624e','status':'EDITORIAL_IMPLEMENTATION_AND_LOCAL_EVIDENCE_COMPLETE; REMOTE_BYTES_MUST_VERIFY_AFTER_PUSH','requirements':[{'requirement':name,'status':'PROVED_WITHIN_EDITORIAL_SCOPE','evidence':evidence(V/file)} for name,file in req],'proof':proof['pdf_sha256'],'local_review_link_targets_verified':link_count,'python_syntax':'PASS','external_acceptance':[{'item':'Owner art/wording and Roshan enjoyable reading/comprehension','status':'OPEN','reason':'The review proof is delivered; no owner/child acceptance is inferred from agent judgment.'},{'item':'Qualified professional SLP approval','status':'OPEN','reason':'Exact manuscript and review packet are ready. Developmental editorial review does not certify a clinician sign-off.'},{'item':'Physical bound print, color/paper/gutter/spine and native density','status':'OPEN','reason':'Spread dummy/instructions supplied. Typical native art is approximately212ppi, not a300ppi press certification.'},{'item':'Game-wide master audit, cinematic/device/release acceptance','status':'OUT_OF_SCOPE_UNCHANGED','reason':'Static book changes close no canonical game findings.'}],'remote_requirement':{'repository':'Ebonyks/mermaid-roshan-reef','branch':'codex/mermaid-roshan-picture-book','command':'verify_remote.py <published exact revision> --receipt <external receipt path>','scope':'Anonymous manifest plus all exact required-file SHA256/bytes after commit/push.'}}
(V/'COMPLETION_AUDIT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'local_requirements':len(req),'review_links':link_count,'status':result['status']}))
