from pathlib import Path
import datetime, hashlib, json, shutil, subprocess, sys

b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
f=b/'audit/job_geode_supported_celebration_v1_20261002'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
source=b/'tools/audit_game_2d.py';tests=b/'tools/tests/test_audit_game_2d.py'
ip=b/'design/audit_impacts/job-geode-supported-celebration-20261002.json'
impact=read(ip)
extension=' Necessary verification-tool repair: restrict XML model signatures to an XML document prefix so random compressed WebP bytes do not become invented model debt; retain disguised XML and binary model detection. No debt ceiling, manifest, trusted gameplay probe or source painting changes. Preserve the failed full suite2 and audit2dv2.'
impact['scope']+=extension
impact['findings']=sorted(set(impact['findings'])|{'MA-2D-002'})
impact['files']=sorted(set(impact['files'])|{'tools/audit_game_2d.py','tools/tests/test_audit_game_2d.py'})
write(ip,impact)
plan=read(f/'PLAN.json');plan['scope']+=extension;plan['findings']=impact['findings'];plan['verification_tool_repair']='MODEL_SNIFF_FALSE_POSITIVE_V328.json';write(f/'PLAN.json',plan)
for p in [source,tests]:shutil.copyfile(p,f/'baseline'/p.name)
s=tests.read_text();anchor='\tdef test_disguised_glb_magic_is_model_debt(self) -> None:\n';assert anchor in s
new='''\tdef test_compressed_image_xml_tag_bytes_are_not_model_debt(self) -> None:
\t\t# The published real WebP frame contains b"<X3d" at offset 49958.
\t\t# Compression bytes are not an XML document, regardless of suffix.
\t\tfor prefix in (b"RIFF\\x18\\0\\0\\0WEBPVP8 ", b"\\x89PNG\\r\\n\\x1a\\n"):
\t\t\tsample = prefix + b"\\0compressed<X3d\\x80random<COLLADA\\0"
\t\t\tself.assertFalse(game_2d._sample_is_model(sample))

\tdef test_model_xml_disguised_as_image_still_is_model_debt(self) -> None:
\t\ttemp, root, manifest = self.fixture(with_debt=False)
\t\tself.addCleanup(temp.cleanup)
\t\tassets = root / "assets"
\t\tassets.mkdir()
\t\t(assets / "hidden.webp").write_bytes(
\t\t\tb"\\xef\\xbb\\xbf \\n<?xml version='1.0'?><x:X3D xmlns:x='urn:x3d'><x:Scene/></x:X3D>")
\t\t(assets / "hidden.png").write_bytes(
\t\t\tb" \\n<!-- leading comment --><COLLADA><asset/></COLLADA>")
\t\tself.assertEqual(game_2d.discover(root).model_files,
\t\t\t("assets/hidden.png", "assets/hidden.webp"))
\t\tself.assertIn("G2D101", self.finding_ids(game_2d.audit(root, manifest)))

'''
tests.write_text(s.replace(anchor,new+anchor),encoding='utf-8',newline='\n')
cmd=[sys.executable,'-X','utf8','-B','-m','unittest','tools.tests.test_audit_game_2d.Game2DAuditTests.test_compressed_image_xml_tag_bytes_are_not_model_debt','tools.tests.test_audit_game_2d.Game2DAuditTests.test_model_xml_disguised_as_image_still_is_model_debt']
gate=f/'runtime_gate'
def run(label):
 p=subprocess.run(cmd,cwd=b,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
 for name,data in [('stdout',p.stdout),('stderr',p.stderr)]: (gate/(label+'.'+name+'.log')).write_bytes(data)
 write(gate/(label+'.receipt.json'),{'status':'PASS' if p.returncode==0 else 'FAIL_PRESERVED','command':cmd,'process_exit':p.returncode,'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'stdout_sha256':hashlib.sha256(p.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(p.stderr).hexdigest()})
 return p
before=run('model_sniff_beforev1');assert before.returncode==1 and b'FAILED (failures=1)' in before.stderr,before.stderr.decode()
s=source.read_text();old='\tif COLLADA_XML_RE.search(sample) or X3D_XML_RE.search(sample):\n\t\treturn True\n';assert old in s
new='\t# XML tags inside compressed image/binary bytes are not model documents.\n\t# Keep suffix-independent detection of actual XML, including BOM, comments\n\t# and namespaced roots, without inventing model debt from random payloads.\n\tif stripped.startswith(b"<") and (\n\t\t\tCOLLADA_XML_RE.search(sample) or X3D_XML_RE.search(sample)):\n\t\treturn True\n'
source.write_text(s.replace(old,new),encoding='utf-8',newline='\n')
after=run('model_sniff_afterv1');assert after.returncode==0,after.stderr.decode()
sys.path.insert(0,str(b/'tools'));import audit_game_2d as audit
image=b/'audit/job_geode_route_emblem_runtime_v1_20261002/attempt_02/native_frames/geode_1600_0035.webp'
from PIL import Image
im=Image.open(image);im.load();assert im.format=='WEBP' and im.size==(1600,720)
assert not audit._has_model_magic(image)
record={'status':'XML_DOCUMENT_PREFIX_REPAIR_FOCUSED_TESTS_PASS','checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'image':{'path':image.relative_to(b).as_posix(),'sha256':sha(image),'bytes':image.stat().st_size,'decoded_format':im.format,'dimensions':list(im.size),'coincidental_signature_offset':image.read_bytes().index(b'<X3d')},'cause':'A four-byte case-insensitive X3D tag prefix inside compressed VP8 image data was treated as an XML model. The previous full suite ran before this review screenshot was tracked; the next tracked-file discovery exposed the false positive.','repair':'Require the model XML document sample to begin with < after BOM/whitespace removal. Binary model magic, named model extensions, actual XML hidden under image suffixes, archive checks and the shrinking debt ceiling stay enforced.','before':'runtime_gate/model_sniff_beforev1.receipt.json','after':'runtime_gate/model_sniff_afterv1.receipt.json','failed_full_suite':'full_ci_v2/RECEIPT.json','qualification':'Verification tool repair only. All 375 rendered runtime/fixture/source hashes remain unchanged. Fresh full suite3 will add the two changed audit-tool files to its separate 377-file machine boundary. No new artwork, inherited machine pass, true-zero-debt or owner acceptance.'}
write(f/'MODEL_SNIFF_FALSE_POSITIVE_V328.json',record)
snapshot=read(f/'SOURCE_CURRENT_BEFORE_CAPTURES.json');assert len(snapshot['source_files'])==375 and all(sha(b/x['path'])==x['sha256'] for x in snapshot['source_files'])
machine=json.loads(json.dumps(snapshot));machine['source_files']+= [{'path':p.relative_to(b).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size} for p in [source,tests]]
machine['source_files'].sort(key=lambda x:x['path']);machine['status']='CURRENT_377_FILE_MACHINE_BOUNDARY';machine['qualification']='Same 375 unchanged captured runtime/fixture/art source files plus the corrected model detector and its focused regression tests. This machine boundary is separate from the unchanged direct visual capture boundary.'
write(f/'SOURCE_CURRENT_MACHINE_V3.json',machine)
shutil.copyfile(Path(__file__),f/'review_tools'/Path(__file__).name)
runner=f/'review_tools/run_supported_geode_full_ci_v329.py';s=(f/'review_tools/run_supported_geode_full_ci_v322.py').read_text();s=s.replace("folder=family/'full_ci_v2'","folder=family/'full_ci_v3'").replace("family/'SOURCE_CURRENT_BEFORE_CAPTURES.json'","family/'SOURCE_CURRENT_MACHINE_V3.json'").replace('==375','==377').replace('375-file','377-file').replace('full_ci_v2/process.exit','full_ci_v3/process.exit').replace('full suite2 scripts/ci.sh','full suite3 scripts/ci.sh');runner.write_text(s,encoding='utf-8',newline='\n')
impact=read(ip);impact['files']=sorted(set(impact['files'])|{p.relative_to(b).as_posix() for p in f.rglob('*') if p.is_file()})
impact['validation']+=[{'command':'XML model recognition compressed-image negative test before repair','result':'FAIL','evidence':record['before']+'; one expected failure proves the original false-positive.'},{'command':'XML model recognition compressed-image and disguised-XML regressions after repair','result':'PASS','evidence':record['after']+'; actual published WebP also fully decoded and retained byte-exact.'}]
write(ip,impact)
print('Focused detector repair passes both regression cases; 375 visual sources unchanged. Prepared separate 377-file machine boundary.')
