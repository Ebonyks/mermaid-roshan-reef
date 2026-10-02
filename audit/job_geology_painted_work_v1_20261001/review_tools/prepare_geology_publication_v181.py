from pathlib import Path
import datetime, hashlib, json, re, shutil, subprocess, sys
from html.parser import HTMLParser
root=Path(sys.argv[1]);family=root/'audit/job_geology_painted_work_v1_20261001'
base='e1b431f49258eef1d293b11a732353f0a3aa12e9'
write=lambda p,d:p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
git=lambda *args:subprocess.check_output(['git',*args],cwd=root)
# Prepare the proven exact-path publisher for this new source boundary; it still cannot run without a sealed index.
old=root/'tmp/geode_runtime_publish_v164/executed_publish_geode_runtime_v164.py'
pub=old.read_text(encoding='utf-8')
pub=pub.replace('geode_runtime_publish_v164','geology_work_publish_v183').replace('geode_runtime_remote_v164','geology_work_remote_v183').replace('geode_runtime_v163_sealed.json','geology_work_v182_sealed.json').replace('executed_publish_geode_runtime_v164.py','executed_publish_geology_work_v183.py')
pub=pub.replace('audit/job_geode_runtime_v1_20261001/full_ci_v2/SOURCE_BEFORE.json','audit/job_geology_painted_work_v1_20261001/full_ci_v1/SOURCE_BEFORE.json').replace('==334','==349').replace("'source_count':334","'source_count':349")
start=pub.index("msg.write_text(");end=pub.index("\nrun('commit'",start)
pub=pub[:start]+"msg.write_text('Bind painted geology work and audit every current state\\n\\nReuse six reviewed painted derivatives at new exact runtime paths for fossil, pan, grain, mineral, layered specimen and stone slab. Add one selected deep painted soil cover after preserving the rejected shallow first attempt. Preserve source aspect, the conserved fossil thirds, pan basin containment, existing input/save/reward semantics and other careers. Geode cavities continue to reveal embedded crystals without loot drops.\\n\\nReview all46 current native four-phase career stills at1280/1600; retain174 capture archives with83direct/91unreviewed and every source attempt. Painted material4.6 remains separate from room2.8/contact2.7/soil clearing3.9/pan action3.8 and provisional assembly/opening4.5. Expand the individual register to1586 entries without counting repeated prop instances as new images.\\n\\nFresh unmodified official Godot4.7.2 full suite and exact349-source before/after receipt are included. Raw diagnostics remain unfiltered. Parser/inference/import/analyzer/authority/development/2D no-regression gates are separately recorded. Reversible topic candidate only; full timed motion/training/story/device/child/owner/all-job report/integration/release remain open.\\n',encoding='utf-8')"+pub[end:]
pub=pub.replace('/audit/job_geode_runtime_v1_20261001/index.html','/audit/job_geology_painted_work_v1_20261001/index.html')
pub=pub.replace("shutil.copyfile(__file__,out/'executed_publish_geology_work_v183.py')","shutil.copyfile(__file__,out/'executed_publish_geology_work_v183.py')")
pubpath=family/'review_tools/executed_publish_geology_work_v183.py';pubpath.write_text(pub,encoding='utf-8',newline='\n')
shutil.copyfile(Path(__file__),family/'review_tools'/Path(__file__).name)
p=root/'design/audit_impacts/job-geology-painted-work-20261001.json';d=json.loads(p.read_text());d['files']=sorted(set(d['files'])|{x.relative_to(root).as_posix() for x in family.rglob('*') if x.is_file()});write(p,d)
print('PUBLICATION181|proven scoped publisher prepared; full-suite PASS and sealed exact index still required')
