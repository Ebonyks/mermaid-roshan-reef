"""Apply the unchanged original silhouette floor to all complete native swap snapshots."""
from pathlib import Path
import json,hashlib,importlib.util
from PIL import Image
R=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('original_auditor',R/'scripts/audit_study.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
rows=[]
for p in sorted((R/'evidence/swaps_v8').glob('*.png')):
 pixels=m.pixel_checks(Image.open(p).convert('RGBA'))
 rows.append({'file':p.name,'png_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'large_components':pixels['large_components'],'secondary_component_pixels':pixels['secondary_component_pixels'],'pass':pixels['large_components']==1 and pixels['edge_alpha_pixels']==0})
bad=[x for x in rows if not x['pass']]
report={'pass':len(rows)==81 and not bad,'candidate':'render_v8','cases':len(rows),'failed_cases':len(bad),'rows':rows,'thresholds':'Unmodified original pixel_checks: alpha>96, connected components>12pixels, exactly one figure and no edge alpha.','diagnosis':'Some mixed body/tail combinations leave waist gaps. Equality with a fresh instance does not establish outline coverage. Complete same-theme sets remain separately passed; shared join/ownership correction and all-mix re-audit required before wardrobe compatibility.','limits':'Snapshots at1.5s for27mixes x3clips; not every-frame mixed geometry or human/device acceptance.'}
(R/'evidence/mixed_slot_outline_audit_v8.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print('MIXED_SLOT_OUTLINE',report['pass'],'cases',len(rows),'failed',len(bad));raise SystemExit(0 if report['pass'] else 1)
