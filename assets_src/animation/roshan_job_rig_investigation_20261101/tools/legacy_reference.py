"""Compare 27 legacy outfits at ten authored arm/blink/tail times to v8.

The reference actor/shader/rest/weights are immutable seed bytes. Only resource
URLs are relocated into this disposable standalone project. No new rig design.
"""
from pathlib import Path
import json,shutil,subprocess,hashlib,sys,time
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[1]
S=R/'evidence/scratch/seed_reference';S.mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source=(R/'contract/seed_study.gd.txt').read_text()
study=source.replace('res://../art/','res://art/').replace('res://../../../native_rig_stress_20261031/art/','res://art/')
(S/'study.gd').write_text(study)
shutil.copy2(R/'contract/seed_costume.gdshader.txt',S/'costume.gdshader')
shutil.copy2(R/'demo/project.godot',S/'project.godot')
rig=json.loads((R/'contract/seed_rig.json').read_text())
for mesh in rig['meshes']:mesh['texture']='art/'+Path(mesh['texture']).name
(S/'rig.json').write_text(json.dumps(rig))
(S/'art').mkdir(exist_ok=True)
for p in (R/'demo/art').glob('*.png'):shutil.copy2(p,S/'art'/p.name)
shutil.copy2(R/'tools/legacy_capture.gd',S/'legacy_capture.gd')
# The same capture script may run outside the candidate res:// root.
engine='C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/godot-4.7.2/editor/Godot_v4.7.2-stable_win64.exe'
rows=[]
for name,project in [('reference',S),('candidate',R/'demo')]:
    out=R/'evidence/scratch'/('legacy_'+name);out.mkdir(exist_ok=True)
    start=time.monotonic()
    with (R/'evidence'/('legacy_'+name+'.log')).open('w') as log:
        run=subprocess.run([engine,'--path',str(project),'--rendering-method','mobile','--disable-vsync','--max-fps','240','-s',str(R/'tools/legacy_capture.gd'),'--',str(out),name],stdout=log,stderr=subprocess.STDOUT,timeout=900)
    rows.append({'mode':name,'exit':run.returncode,'seconds':time.monotonic()-start})
    if run.returncode:raise SystemExit(run.returncode)
out=R/'evidence/scratch';index=json.loads((out/'legacy_reference/index.json').read_text());comparisons=[]
for item in index:
    a=out/'legacy_reference'/item['file'];b=out/'legacy_candidate'/item['file']
    changed=int(np.any(np.array(Image.open(a).convert('RGBA'))!=np.array(Image.open(b).convert('RGBA')),axis=2).sum())
    comparisons.append({'file':item['file'],'seed_png_sha256':sha(a),'candidate_png_sha256':sha(b),'changed_pixels':changed})
report={'seed_revision':'b700b846d1d2f4b1843279f268e2bb12e4b1f4ec','seed_study_sha256':sha(R/'contract/seed_study.gd.txt'),'seed_shader_sha256':sha(R/'contract/seed_costume.gdshader.txt'),'seed_rig_sha256':sha(R/'contract/seed_rig.json'),'reference_relocation':'Only res:// texture resource paths changed to art/<basename>; original shader/rest/weights/curves/selectors unchanged. Standalone disposable reference project.','renderer':'Godot4.7.2 Mobile native1024 RGBA','captures':rows,'comparisons':comparisons,'snapshots':len(comparisons),'mismatch_snapshots':sum(x['changed_pixels']!=0 for x in comparisons),'pass':all(x['changed_pixels']==0 for x in comparisons),'limit':'Ten times per legacy outfit; does not establish continuous motion quality or compatibility of new mixed garments.'}
(R/'evidence/legacy_seed_pixel_comparison.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='comparisons'},indent=2))
sys.exit(0 if report['pass'] else 1)
