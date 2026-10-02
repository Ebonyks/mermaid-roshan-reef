from pathlib import Path
import datetime, hashlib, json, shutil
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
s=b/'assets_src/imagegen/geologist_river_junctions_v1_20261001'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
target='assets_src/imagegen/geologist_river_junctions_v1_20261001/wet_attempt_01/native_generated.png'
straight='assets_src/imagegen/geologist_river_components_v1_20261001/attempt_02/native_generated.png'
assert sha(b/target)=='6dd4207ebe976b3e5db429051c81f06a1f644191be94f86f789766e2988fe05d'
assert sha(b/straight)=='8890c70609f171321182242584e0a1eb3cc50b4f07e7b8754d252715bd80d254'
attempt=s/'wet_attempt_02';attempt.mkdir(exist_ok=False)
prompt='''Use case: precise-object-edit
Asset type: transparent 2D painted river junction atlas for a preschool storybook game.
Input image1 is the EDIT TARGET: the existing complete wet endcap, elbow, T and cross junction atlas. Preserve its exact four-object layout, outline silhouettes, channel widths, open port positions, ochre rounded earth banks, plum outlines and alpha background. Image2 is material context only: the matching straight-channel family.
Change only the aqua water painting inside all four objects to make repeated connections calm and seamless. Use the same even medium-light turquoise aqua base across all four water interiors, including every open port. Keep softly hand-painted low-contrast pigment variation, a few broad quiet value bands and a gentle fine aqua waterline. Remove every white/cream specular glint and all diagonal white streaks. Avoid local bright-to-dark gradients along a branch: every port must have the same calm aqua value as every other port, whether rotated or straight. Preserve the existing rounded warm banks and their painted lavender shadows exactly as closely as possible.
Polished 2D illustrated children’s storybook raster painting, warm earth and cool graphic water. Retain paint character; no flat vector replacement, no photorealistic texture or 3D. Exactly the same four objects, no additional props, no text or labels, no ground plate, no closed port lips. Full intact contours and transparent exterior. This is a targeted surface-lighting correction, not a redesign.
'''
p=s/'PROMPT_WET_ATTEMPT_02.txt';p.write_text(prompt,encoding='utf-8',newline='\n')
pending=dict(status='PRE_GENERATION_NAMED_GAP',attempt=2,method='BUILTIN_CODEX_IMAGEGEN_TARGETED_WATER_LIGHTING_EDIT',prompt_path=p.relative_to(b).as_posix(),prompt_sha256=sha(p),reference_paths=[target,straight],reference_sha256=[sha(b/target),sha(b/straight)],transparent_background=True,runtime_bound=False,named_gap='Every106 native isolated river studies directly reviewed. V5 bed4.6 but wet joints4.4: rectangular glint/value discontinuities at old straight/new branch and rotated branch ports. Existing same-family source4.6 is unsuitable for repeat joins without this targeted water-lighting correction. Preserve all earlier sources and failed assemblies.',review_evidence='audit/job_river_join_study_v1_20261001/REVIEW_V5.json',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
write(attempt/'GENERATION_PENDING.json',pending)
shutil.copyfile(__file__,s/Path(__file__).name)
ip=b/'design/audit_impacts/job-geology-river-junction-source-20261001.json';d=read(ip);d['scope']+=' Target only failed repeated-port water lighting in a separately preserved wet atlas revision and matching straight-water source; every106 native study views records wet4.4 and bed4.6. No redesign of approved silhouettes or runtime acceptance.';d['files']=sorted(set(d['files'])|{x.relative_to(b).as_posix() for x in s.rglob('*') if x.is_file()});d['validation'].append(dict(command='Pre-generation reuse and assembled seam gap review',result='PASS',evidence=pending['review_evidence']+';'+(attempt/'GENERATION_PENDING.json').relative_to(b).as_posix()));write(ip,d)
print(prompt)
