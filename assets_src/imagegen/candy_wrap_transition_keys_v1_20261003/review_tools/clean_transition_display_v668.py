from pathlib import Path
import collections,hashlib,json,re
B=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');P=B/'assets_src/imagegen/candy_wrap_transition_keys_v1_20261003';L=B/'audit/job_artwork_refinement_live'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
protected=[L/'ALL_ITEMS.json',L/'CURRENT_BOUNDARY_REFRESH.json',*P.glob('*_attempt*/DIRECT_REVIEW.json'),*P.glob('*_attempt*/GENERATION_RECEIPT.json'),*P.glob('*_attempt*/GENERATION_REQUEST.json'),*P.glob('*_attempt*/PROMPT.txt'),*P.glob('*_attempt*/native.png')]
before={p.relative_to(B).as_posix():sha(p) for p in protected}
# Only the separately rendered display text changes;all source/review/register data stay literal.
p=P/'index.html';raw=p.read_bytes();s=raw.decode();pairs={
'Rejected:better':'Rejected: better','Rejected:unrequested':'Rejected: unrequested',
'midpoint:near-finished':'midpoint: near-finished','opaque oval,but':'opaque oval, but',
'groups;no':'groups; no','paper,with':'paper, with','rest,although':'rest, although',
'thanA2,but several curvedbands':'than A2, but several curved bands',
'broadly samefamily,not literal fixedshapes':'broadly the same family, not literal fixed shapes',
'stays ontable':'stays on the table',
'release:improvedneckmaterial,but reference contamination shifts both hands to finalwidestill':'release: improved neck material, but the second reference shifts both hands to the final wide still',
'ornamentation4.4':'ornamentation 4.4'}
for a,b in pairs.items():s=s.replace(a,b)
attrs=lambda text:collections.Counter(re.findall(r'(?:href|src)="([^"]+)"',text))
assert attrs(s)==attrs(raw.decode()) and s.count('class="component-opinion"')==88 and s.count('class="neighbor-opinion"')==6
backup=P/'DISPLAY_BEFORE_WORD_SPACING.html';assert not backup.exists();backup.write_bytes(raw)
t=p.with_name('index.v668_next');t.write_bytes(s.encode());t.replace(p)
assert before=={q.relative_to(B).as_posix():sha(q) for q in protected}
(P/'DISPLAY_COPY_EDIT.json').write_text(json.dumps(dict(status='HTML_TEXT_ONLY_ALL_REVIEW_REGISTER_SOURCE_PROMPT_NATIVE_BYTES_UNCHANGED',protected_members=before,link_and_image_reference_multiplicities_unchanged=True,component_rows=88,neighbor_rows=6),indent=2)+'\n',encoding='utf8',newline='\n')
(P/'review_tools'/Path(__file__).name).write_bytes(Path(__file__).read_bytes())
print('SAFE_DISPLAY_ONLY_WORD_SPACING_ALL_AUDIT_DATA_LITERAL_UNCHANGED')
