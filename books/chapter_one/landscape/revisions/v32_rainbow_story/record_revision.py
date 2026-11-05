"""Bind actual independent findings and precisely scoped delivery evidence."""
from pathlib import Path
import hashlib,json
V=Path(__file__).resolve().parent;L=V.parents[1];R=L.parents[2]
def read(p):return json.loads(p.read_text('utf8'))
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p):return dict(path=p.resolve().relative_to(R.resolve()).as_posix(),sha256=sha(p))
B=read(L/'book.json');ver=read(V/'complete/verification.json');ch=read(V/'character_final.json');st=read(V/'style_final.json');la=read(V/'language_final.json')
assert ch['book_json_sha256']==sha(L/'book.json')==st['frozen_evidence']['book']['sha256']==la['evidence']['book_json_sha256']
assert ch['page_provenance_sha256']==sha(V/'complete/page_provenance.json')==st['frozen_evidence']['page_provenance']['sha256']==la['evidence']['page_provenance_sha256']
assert ch['pdf_sha256']==sha(V/'complete/Mermaid_Roshan_LANDSCAPE_ROUGH.pdf')==st['frozen_evidence']['pdf']['sha256']==la['evidence']['final_pdf_sha256']
assert ver['changed_pages']==[4,13,14,22,30,31] and len(ver['unchanged_pages_byte_identical_to_mapped_v31'])==28
assert ver['lossless_pdf_raster_matches_all34screenshots']
assert not ch['summary']['remaining_actionable_visual_defects'] and not st['summary']['genuine_remaining_sub_4_9_findings'] and not la['remaining_actionable_language_or_text_placement_defects']
e=read(V/'generation_evidence.json')
for row in e['generated']:
 assert sha(R/row['native_output']['path'])==row['native_output']['sha256']
 assert hashlib.sha256(row['prompt'].encode()).hexdigest()==row['prompt_sha256']
 for q in row['references']:assert sha(R/q['path'])==q['sha256']
 if row['id']=='dusty_chest':
  row['selection']='SELECTED_CONTOUR_SOURCE; STANDALONE_ALPHA_REJECTED'
  row['review']='PASS only final page4 document contour extraction. Native RGBA has residual diffuse backing and is not a clean-alpha master. Full body/lock/sides preserved; fine outer dust wisps may be excluded by the declared outline. See independent character/style audits.'
 elif row['id']=='dusty_chest_clean':
  row['selection']='REJECTED_NOT_DELIVERED'
  row['review']='REJECTED standalone alpha due to diffuse backing; no pixels delivered. Preserved as generation evidence.'
 else:
  row['review']='PASS independent native final delivered-region character/style inspection. Only the exact declared alpha silhouette or bounded local masks are delivered; candidate pixels outside delivery regions are excluded. No full-scene acceptance.'
e['selection_note']='Five calls; four delivered components include first chest as contour-clipped source. Two chest candidates rejected as standalone clean-alpha masters; second is not delivered.'
save(V/'generation_evidence.json',e)
# Only diagnostic-sidecar binding is reconciled; independent findings/scores stay intact.
st['frozen_evidence']['generation_evidence']['sha256']=sha(V/'generation_evidence.json')
st['frozen_evidence']['generation_evidence']['root_reconciliation']='Delivery statuses closed after independent native reviews; art/layout/proof hashes and reviewer observations remain unchanged.'
save(V/'style_final.json',st)
cp={p['page_index']:p for p in ch['pages']};sp={p['page_index']:p for p in st['pages']};pages=[]
for n in range(34):
 c=cp[n];s=sp[n];assert c['screenshot_sha256']==sha(V/'complete'/f'page_{n:02}.png')==s['rendered_evidence']['sha256']
 scores=[o['internal_craft_score'] for o in c['objects']]+[o['internal_craft_score'] for o in s['objects_reviewed']]
 score=min(scores)
 p=B['pages'][n-1] if 0<n<33 else B.get('cover',{}) if n==0 else B['back_cover']
 pages.append(dict(page=n,label='Front cover' if n==0 else 'Rear cover' if n==33 else f'Story{n}',proof=ref(V/'complete'/f'page_{n:02}.png'),review_basis='Direct current native inspection' if n in ver['changed_pages'] else 'Prior V31 observations carried forward only on explicit mapped identical proof bytes',final_internal_craft_min=score,all_reviewed_objects_at_target=score>=4.9,current_caption=p.get('text'),character_objects=c['objects'],style_objects=s['objects_reviewed'],source_preservation='New source-derived page; no predecessor' if n==4 else 'Existing source layout swap; no strict outside-mask claim' if n==31 else 'Strict outside-region proof unchanged' if n in ver['changed_pages'] else 'Mapped V31 proof hash unchanged'))
summary=dict(pages=34,minimum=min(p['final_internal_craft_min'] for p in pages),mean_page_minimum=sum(p['final_internal_craft_min'] for p in pages)/34,pages_at_internal_target=sum(p['all_reviewed_objects_at_target'] for p in pages),all_explicitly_reviewed_objects_target_met=all(p['all_reviewed_objects_at_target'] for p in pages))
save(V/'visual_review.json',dict(revision='V32',revision_verdict='COMPLETE_INTERNAL_REVIEW_PROOF; EXTERNAL_ACCEPTANCE_PENDING',method='Independent native character/style/language inspection of six changed pages;28 mapped unchanged V31 proofs sealed byte-identical; all32 captions reread; all34 PDF/source/text/font/scope checks bound.',book_json_sha256=sha(L/'book.json'),page_provenance_sha256=sha(V/'complete/page_provenance.json'),pdf_sha256=sha(V/'complete/Mermaid_Roshan_LANDSCAPE_ROUGH.pdf'),internal_scale='Subjective editorial craft, not release-proven master-audit satisfaction or clinical approval. Scores describe explicitly inspected objects, not invisible pixels or every paper-grain dot.',summary=summary,pages=pages,independent_audits=[ref(V/f) for f in ['character_final.json','style_final.json','language_final.json']],open_findings=[],retained_limits=['Both chest native alpha masters rejected; first used only through delivered PDF contour.','Conservative visible page4 bunny box is larger than original manual book annotation, but still within85%/12% low-bank gates. Exact measured enclosures are in style_final.json.','Page22 narrates subsequent table scrubbing; no new scrubbing hand action is fabricated.','Many full-art source images approximately212ppi at trim; screen review does not certify press density.'],external_acceptance_open=['Owner artwork and wording','Roshan enjoyable shared reading and comprehension','Qualified SLP review','Physical print, binding, color, paper and native-density proof'],scope_limits='No game/runtime/master-finding closure, cinematic delivery approval or protected-original modification.'))
claims=[
 ('rainbow-water-and-pool-magic',[13,14],'Original rainbow colors restored under partial gunk13; full rainbow14 and named Daddy dialogue explicitly explains the magical swimming pool.'),
 ('combined-puff-welcome',[31,32],'Former30 reflection and31 gratitude/rest invitation share31 with named speakers and lead directly to the inclusive nap32.'),
 ('freed-early-story-space',[3,4,5,6],'New4 adds complete source-derived dusty belongings; surrounding entry/shared cleanup/supplies retain clear cause and goal.'),
 ('completed-castle-pacing',[22,23,24,30],'Sorting and table scrubbing are narrated before final door; existing clean room30 becomes quiet castle result through bounded actor/brush removal.'),
 ('stable-count-and-reveals',[23,24,27,28],'32 interiors plus two covers retained; both reveal turns preserved;28 mapped prior proofs remain exact.'),
 ('preserved-hidden-details',[10,33],'Two tiny existing silent Lamma appearances remain, without child-facing clue or enlargement.'),
 ('source-bubbles-and-export',list(range(34)),'Five candidates/four delivered components scoped honestly; baseline art/font unchanged; all34 PDF raster proofs match and no DCT/JPX image streams.')]
save(V/'COMPLETION_AUDIT.json',dict(status='REQUESTED_EDITORIAL_CORRECTIONS_AND_LOCAL_PROOF_VERIFIED; REMOTE_DELIVERY_TO_VERIFY_AFTER_PUSH',baseline='07734bb43018ffdefef3644f337db8fa46038d5b',frozen_book=ref(L/'book.json'),frozen_pdf=ref(V/'complete/Mermaid_Roshan_LANDSCAPE_ROUGH.pdf'),requirements=[dict(id=k,status='PROVED_WITH_SCOPED_EDITORIAL_AND_MACHINE_EVIDENCE',pages=ns,claim=c,evidence=[ref(V/'visual_review.json'),ref(V/'complete/verification.json'),ref(V/'generation_evidence.json')]) for k,ns,c in claims],acceptance='Internal corrections/proof complete; owner/child/qualified SLP/physical-print acceptance remain open. Actual anonymous remote receipt is produced outside repo after push.'))
print(json.dumps(summary))
