"""Update document authority and per-file attribution for this static revision."""
from pathlib import Path
import json,hashlib
V=Path(__file__).resolve().parent;R=V.parents[4]
p=R/'design/05_DOC_LEDGER.md';s=p.read_text('utf8')
replacements={
'books/chapter_one/DESIGN_LANGUAGE.md':('🟢','BINDING_DOMAIN','Static-book source/identity/layout rules and scoped owner exceptions. Owner decisions2026-10-19 and2026-10-25 preserve manuscript/character standards and govern V38 A1–A10; final trim open. Second-AI compliance review is supporting evidence, not new creative authority; no game/cinematic authority.'),
'books/chapter_one/README.md':('🔵','SUPPORTING_CURRENT','V38 static review: A1–A8/A10 implemented, A9 resolution held; exact manuscript; owner/child/SLP/trim/print open.'),
'books/chapter_one/landscape/PAGE_PLAN.md':('🔵','SUPPORTING_CURRENT','V38 exact 32-page owner words/order, hand-broken18/22 and preserved V34 source mapping.'),
'books/chapter_one/landscape/REVIEW.md':('🔵','SUPPORTING_CURRENT','V38 fresh five-pass review, separate iterative second-AI critique, strict checks and explicit A9/owner/print holds.'),
'books/chapter_one/landscape/STORY_COMPREHENSION_AUDIT.md':('🔵','SUPPORTING_CURRENT','V38 editorial continuity/readability analysis; child and professional SLP evidence open.'),
'books/chapter_one/landscape/revisions/v37_consistency_20261022/README.md':('⚪','HISTORICAL_EVIDENCE','Sealed V37 review and native/proof/evidence packet. V38 owns current scoped review; original files unchanged.'),
'books/chapter_one/landscape/revisions/v37_consistency_20261022/STRESS_REPORT.md':('⚪','HISTORICAL_EVIDENCE','Original twenty-run/seven-cycle V37 review, unchanged. V38 adds a separate five-pass review; no independent or final acceptance.'),
'books/chapter_one/landscape/revisions/v38_audit_fixes/README.md':('🔵','SUPPORTING_CURRENT','V38 scoped entry, A1–A8/A10 implementation, A9 hold, source/proof/contrast/export/publication evidence; no owner/child/SLP/print acceptance.'),
'books/chapter_one/landscape/revisions/v38_audit_fixes/BUILD_REPORT.md':('🔵','SUPPORTING_CURRENT','A1–A10 outcomes/evidence, exact V37 preservation, five focused passes, composed caption counts and explicit acceptance gaps.'),
'books/chapter_one/landscape/revisions/v38_audit_fixes/peer_review/README.md':('🔵','SUPPORTING_CURRENT','Owner-requested second-AI critique, versioned rounds/corrections, exact-artifact handback and separate publication verification; A9/owner/child/SLP/trim/print holds retained.')
}
found=set();lines=[]
for line in s.splitlines():
 match=next((k for k in replacements if line.startswith('| `'+k+'` |')),None)
 if match:
  icon,status,note=replacements[match];line=f'| `{match}` | {icon} | `{status}`; {note} |';found.add(match)
 lines.append(line)
for key in replacements.keys()-found:
 icon,status,note=replacements[key];lines.append(f'| `{key}` | {icon} | `{status}`; {note} |')
p.write_text('\n'.join(lines)+'\n',encoding='utf8',newline='\n')
p=R/'ASSET_LICENSES.md';s=p.read_text('utf8')
for asset in sorted(V.rglob('*')):
 if not asset.is_file() or not (asset.suffix.lower() in ['.png','.jpg','.pdf'] or '.pdf.part' in asset.name):continue
 rel=asset.relative_to(R).as_posix()
 if '`'+rel+'`' in s:continue
 if asset.parent.name=='art':
  source='OpenAI image_gen; references/hashes, attempts and selections in V38 generation_evidence.json';mods='Native bytes retained. Selected local polygons only, or rejected trial preserved.'
 elif asset.parent.name=='inputs':
  source='Exact project-source crop or read-only source-coordinate diagnostic';mods='Crop/grid diagnostic; input_crops.json and diagnostic_provenance.json. Originals unchanged.'
 else:
  source='Deterministic source-attributed V38 book composition, render/export, review crop or exact master binary part';mods='Layout/text/alpha clipping, read-only crop/scaling and disclosed PDF encoding. Protected originals untouched.'
 s+=f'| `{rel}` | {source} | Underlying project rights unchanged; generated pixels under OpenAI output terms | https://openai.com/policies/terms-of-use/ | {mods} |\n'
p.write_text(s,encoding='utf8',newline='\n')
p=V/'diagnostic_provenance.json';rows=json.loads(p.read_text('utf8'));sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
for n,source in [(0,V.parent/'v36_rear_composition_20261021/rear_scene_attempt1.png'),(1,V/'art/rear_additions_attempt1.png')]:
 asset=V/f'inputs/rear_coordinate_diagnostic_{n}.png';rel=asset.relative_to(R).as_posix()
 rows=[q for q in rows if q['path']!=rel]
 rows.append(dict(path=rel,source=source.relative_to(R).as_posix(),source_sha256=sha(source),operation='Coordinate grid diagnostic; source unchanged; not generation input or delivery pixels',sha256=sha(asset)))
p.write_text(json.dumps(rows,indent=2)+'\n',encoding='utf8',newline='\n')
print('Authority and per-file asset rows updated')
