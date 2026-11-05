"""Check the proposal's unchanged baseline, real sources, art and text geometry."""
from pathlib import Path
import hashlib, json
from PIL import Image
import numpy as np
V=Path(__file__).resolve().parent;R=V.parents[4];L=V.parents[1]
def read(p):return json.loads(p.read_text('utf8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf8',newline='\n')
baseline=read(V/'baseline_seal.json');cover=read(V/'cover_proposal.json');story=read(V/'story_review.json');layout=read(V/'layout_checks.json')
assert baseline['baseline']=='4f65c502beabb38bb3365920005e2e6f90ea13f0'
for q in baseline['files']:assert sha(R/q['path'])==q['sha256'],q['path']
prior=read(L/'revisions/v34_editorial_polish/complete/verification.json')
for q in prior['source_seal']:assert sha(R/q['path'])==q['sha256'],q['path']
assert sha(L/'book.json')==prior['manuscript_sha256']
assert story['status']=='PROPOSAL_ONLY_OWNER_THEME_RESPONSE_PENDING'
assert len(story['proposed_changes'])==12
assert all(q['status']=='PROPOSED_NOT_APPLIED' for q in story['proposed_changes'])
assert cover['status']=='TWO_REVIEW_CANDIDATES_NOT_APPLIED_TO_CURRENT_BOOK'
checks=[]
for c,g in zip(cover['candidates'],layout):
 assert c['id']==g['id'] and g['font']
 assert sha(R/c['base'])==c['base_sha256']
 a=np.array(Image.open(R/c['base']).convert('RGB')).astype(int)
 b=np.array(Image.open(V/'proofs'/('rear_'+c['id']+'_art.png')).convert('RGB')).astype(int)
 assert a.shape==b.shape==(1060,1484,3)
 diff=np.any(np.abs(a-b)>1,axis=2);allowed=np.zeros((1060,1484),bool)
 if c['id']=='A':allowed[655:680,1033:1057]=True
 assert not np.any(diff&~allowed),(c['id'],int(np.sum(diff&~allowed)))
 if c['id']=='A':assert int(diff.sum())>=30,'Cameo not visible'
 else:assert not diff.any()
 inset=24*1484/504
 assert min(g['text']['x'],g['text']['y'])-.35>=inset
 assert g['text']['x']+max(g['lineWidths'])+.35<=1484-inset
 assert g['text']['bottom']+.35<=1060-inset
 assert len(g['copy'].splitlines())==2
 assert all(w<=g['text']['width'] for w in g['lineWidths'])
 checks.append(dict(candidate=c['id'],changed_art_pixels=int(diff.sum()),outside_declared_cameo_pixels=int(np.sum(diff&~allowed)),native_size=[1484,1060],font='Sniglet 20 logical pt',safe_inset_logical_pt=24,proof_sha256=sha(V/'proofs'/('rear_'+c['id']+'.png'))))
e=read(V/'generation_evidence.json')
assert e['attempts']==2
for q in [e['native_output'],e['additional_native_output']]:assert sha(R/q['path'])==q['sha256']
assert sha(R/cover['font'])==cover['font_sha256']
record=dict(status='PASS',baseline=baseline['baseline'],source_files_unchanged=len(prior['source_seal']),manuscript_unchanged=True,master_and_email_pdf_unchanged=True,cover_checks=checks,generation_calls=2,selected_derivatives=1,spoiler_review='Root direct full-cover review: both candidates show only the beginning; no Grand Puff, washing or finale.',visual_review='Root inspected full cover A/B, actual cameo occlusion at enlargement and review page. First generated scene/extraction excluded; exterior haze excluded from the second. Source and text checks are mechanical; theme/cover choice remain open.',acceptance='Proposal review only; owner emphasis, wording, cover selection and later layout/art implementation remain open. No clinical or print acceptance.')
save(V/'verification.json',record)
print(json.dumps({k:v for k,v in record.items() if k not in ['cover_checks','visual_review','acceptance']}))
