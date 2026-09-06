"""Build the replacement-only Day One archive without granting approval.

Narrative target-frame plans are not generated frames, measured source motion,
or cinematic delivery provenance. Human approval is deliberately fail-closed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import re
import shutil
import subprocess
from collections import Counter
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
REL = Path('assets_src/cinematics/day_one_grok_handoff_v4_2026-09-05')
PACKET = ROOT / REL
PRIOR = ROOT / 'assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04'
DRAFT = ROOT / 'assets_src/cinematics/day_one_davinci_draft_2026-09-04'
AUDIT = ROOT / '.tmp/grok_next_audit'
EXPECTED = ['C01-S04','C03-S02','C03-S03','C03-S04','C05-S01','C05-S03','C06-S05','C08-S06','C09-S03','C10-S05','C11-S01','C11-S02','C11-S03','C11-S04','C13-S04','C13-S05']
RASTER = {'.png','.jpg','.jpeg','.webp'}


def digest(path: Path) -> str:
	with path.open('rb') as handle:
		return hashlib.file_digest(handle, 'sha256').hexdigest()


def read(path: Path):
	return json.loads(path.read_text(encoding='utf-8-sig'))


def write(path: Path, value):
	path.parent.mkdir(parents=True, exist_ok=True)
	text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2) + '\n'
	if path.suffix == '.md':
		text = re.sub(r'(?m)(\|)\n\n(?=\|)', r'\1\n', text)
	path.write_text(text, encoding='utf-8', newline='\n')


def copy(source: Path, target: Path):
	assert source.is_file(), f'Missing source: {source}'
	target.parent.mkdir(parents=True, exist_ok=True)
	if target.exists():
		assert digest(source) == digest(target), f'Refusing changed copy target: {target}'
	else:
		shutil.copyfile(source, target)


def inside(path: str) -> Path:
	target = (PACKET / path).resolve()
	target.relative_to(PACKET.resolve())
	assert target.is_file(), target
	return target


def normalize_id(value: str) -> str:
	return value if value.startswith('D1-') else 'D1-' + value


def frame_plan(shot: dict) -> dict:
	count = round(shot['duration_s'] * 24)
	phases = shot['phases']
	assert len(phases) >= 1
	# Design points become explicitly named time spans. Prefer authored ranges.
	if all('range' in p for p in phases):
		ranges = [p['range'] for p in phases]
	else:
		assert len(phases) == 4, 'Non-four-phase shots require explicit ranges'
		ranges = [[0,count//4],[count//4,count//2],[count//2,count-18],[count-18,count]]
	assert ranges[0][0] == 0 and ranges[-1][1] == count
	assert all(a < b for a,b in ranges)
	assert all(ranges[i][1] == ranges[i+1][0] for i in range(len(ranges)-1))
	frames = []
	for index in range(count):
		pi = next(i for i,(a,b) in enumerate(ranges) if a <= index < b)
		a,b = ranges[pi]
		phase = phases[pi]
		hold = shot['shot'] == 'C09-S03' or phase.get('state') == 'hold' or (pi == 3 and 'hold' in phase['instruction'].lower())
		instruction = (f"Create one complete flattened 16:9 frame for {normalize_id(shot['shot'])}, "
			f"target f{index:04d} at {index/24:.6f}s of {shot['duration_s']}s. "
			f"Phase {pi+1}, target time position {index-a+1}/{b-a}: {phase['instruction']} Camera: {shot['camera']}. "
			+ ' Preserve: ' + '; '.join(shot['invariants']) + '. ' +
			('Intentional stillness for inspection/settle only; do not substitute this hold for the preceding action. ' if hold else 'Advance only the declared action while fixed geometry and identity remain unchanged. ') +
			'Use the approved first-frame layout, subject/prop identities and immediately adjacent ACCEPTED full-frame references when available. '
			'Use only actually accepted neighbors; leave unavailable neighbor bindings empty for explicit review, never invent acceptance. The approved opening is the seed for target frame zero. Regenerate the whole frame; no blending, interpolation, cutout animation, masks or pixel warping. '
			'No HUD, text or undeclared characters. Audit exact identity, topology, contact gap and neighboring continuity before accepting.')
		frames.append({'target_frame':index,'time_seconds':round(index/24,6),'phase':pi+1,'phase_range_half_open':[a,b],
			'action_state':'intentional_hold' if hold else 'action','hold_purpose':'countable inspection or stable cut seam' if hold else None,
			'reconstruction_prompt':instruction,'candidate_path':None,'candidate_sha256':None,'accepted_neighbors':[],
			'human_review':'pending','delivery_accepted':False})
	return {'schema':'cinematic-target-frame-plan-v1','shot_id':normalize_id(shot['shot']),'fps':24,'target_frame_count':count,
		'range_convention':'zero-based half-open; [a,b) includes a through b-1','scope':'Editorial target prompts only. Not source-frame measurements, not exact Grok frame control, not audit_cinematic generation evidence.',
		'frames':frames}


def asset_row(path: Path, source: str, role: str, license_text: str, modifications: str) -> dict:
	row = {'path':path.relative_to(PACKET).as_posix(),'sha256':digest(path),'bytes':path.stat().st_size,
		'source_path':source,'role':role,'license_provenance':license_text,'modifications':modifications,
		'used_as_delivery_pixels':False,'media_type':mimetypes.guess_type(path.name)[0] or 'application/octet-stream'}
	if path.suffix.lower() in RASTER:
		with Image.open(path) as im:
			row['dimensions'] = list(im.size)
	return row


def diagnostic_sheet(shot: dict, assembly: dict) -> dict | None:
	"""Exact selected source samples, explicitly diagnostic, never art pixels."""
	if not shot.get('original_source'):
		return None
	source_info=assembly['sources'][shot['original_source']]
	source=DRAFT/source_info['file']
	assert digest(source)==source_info['sha256']
	a,b=shot['original_range']
	indices=sorted(set(shot.get('inspected_frames',[])+[a,a+(b-a)//4,a+(b-a)//2,a+3*(b-a)//4,b-1]))
	assert all(isinstance(i,int) and a <= i < b for i in indices)
	sid=normalize_id(shot['shot']);folder=PACKET/'audit/source_frames'/sid
	folder.mkdir(parents=True,exist_ok=True)
	ffmpeg=shutil.which('ffmpeg') or 'C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/FFmpeg/8.1.2/bin/ffmpeg.exe'
	frames=[]
	for index in indices:
		target=folder/f'f{index:04d}.png'
		if not target.exists():
			subprocess.run([ffmpeg,'-v','error','-i',str(source),'-vf',f'select=eq(n\\,{index})','-frames:v','1','-fps_mode','vfr',str(target)],check=True,capture_output=True)
		frames.append({'index':index,'time_seconds':index/source_info['fps'],'path':target.relative_to(PACKET).as_posix(),'sha256':digest(target)})
	cols=4;width=400;height=250;sheet=Image.new('RGB',(cols*width,((len(frames)+cols-1)//cols)*height),'#172032')
	draw=ImageDraw.Draw(sheet)
	for i,row in enumerate(frames):
		with Image.open(PACKET/row['path']) as picture:
			picture=picture.convert('RGB');picture.thumbnail((400,225))
			x=(i%cols)*width;y=(i//cols)*height
			sheet.paste(picture,(x+(width-picture.width)//2,y))
			draw.text((x+8,y+229),f"{sid}  source f{row['index']:04d}  {row['time_seconds']:.3f}s",fill='white')
	target=folder/'AUDIT_SAMPLES.jpg';sheet.save(target,quality=92)
	result={'source_path':source_info['file'],'source_sha256':source_info['sha256'],'source_fps':source_info['fps'],
		'selected_range_half_open':[a,b],'frames':frames,'sheet':target.relative_to(PACKET).as_posix(),
		'role':'diagnostic_source_samples_only','used_as_generation_pixels':False,'used_as_delivery_pixels':False,
		'method':'Exact zero-based ffmpeg source-frame decode; sheet is whole-frame thumbnail arrangement with frame labels. No synthesized motion or subject repair.'}
	write(folder/'SAMPLE_MANIFEST.json',result)
	return result


def walk_records(value):
	if isinstance(value,dict):
		yield value
		for item in value.values():yield from walk_records(item)
	elif isinstance(value,list):
		for item in value:yield from walk_records(item)


def generation_index(add_ref) -> dict:
	"""Normalize actual recorded prompts/inputs, without guessing missing data."""
	index=[]
	for record_path in sorted((PACKET/'generation_records').glob('*.json')):
		if record_path.name.startswith('SOL_') or 'boundary' in record_path.name:continue
		for rec in walk_records(read(record_path)):
			if not any(k in rec for k in ['prompt','full_prompt','exact_tool_prompt','prompt_path','generation_method','method','attempt']):continue
			output=next((rec.get(k) for k in ['output','output_path','path','file'] if isinstance(rec.get(k),str)),None)
			if not output and isinstance(rec.get('packet_output'),dict):output=rec['packet_output'].get('path')
			if set(rec).issubset({'path','sha256','dimensions','bytes'}):continue # Nested asset descriptor, not a generation record.
			if not output:continue
			candidates=[PACKET/output,ROOT/output,Path(output)]
			path=next((p.resolve() for p in candidates if p.is_file() and p.resolve().is_relative_to(PACKET.resolve())),None)
			if path is None or path.suffix.lower() not in RASTER or 'references' in path.relative_to(PACKET).parts:continue
			sha=digest(path);declared=rec.get('output_sha256',rec.get('sha256'))
			if declared and declared.lower()!=sha:continue # Retained historical record for overwritten path; never relabel.
			prompt=rec.get('exact_tool_prompt') or rec.get('full_prompt') or rec.get('prompt')
			pp=rec.get('prompt_path')
			if pp:
				prompt_file=next((p for p in [ROOT/pp,PACKET/pp] if p.is_file()),None)
				if prompt_file:prompt=prompt_file.read_text(encoding='utf-8-sig')
			inputs=[]
			for key in ['referenced_image_paths','referenced_images','input_paths','references','inputs','reference_paths','input','reference','exact_reference_paths']:
				values=rec.get(key,[])
				if isinstance(values,str):values=[values]
				if not isinstance(values,list):continue
				for item in values:
					name=(item.get('path') or item.get('source_path') or item.get('path_passed')) if isinstance(item,dict) else item
					if not isinstance(name,str):continue
					source=next((p.resolve() for p in [ROOT/name,PACKET/name,Path(name)] if p.is_file()),None)
					if source is None or source.suffix.lower() not in RASTER:continue
					if not (source.is_relative_to(ROOT.resolve()) or 'generated_images' in source.parts):continue
					if source.is_relative_to(PACKET.resolve()):local=source.relative_to(PACKET).as_posix()
					else:local=add_ref(source,'recorded_image_generation_input')
					if any(i['path']==local for i in inputs):continue
					with Image.open(source) as im:dimensions=list(im.size)
					inputs.append({'source_path':name,'path':local,'sha256':digest(source),'dimensions':dimensions,'used_as_delivery_pixels':False})
			with Image.open(path) as im:dimensions=list(im.size)
			index.append({'path':path.relative_to(PACKET).as_posix(),'sha256':sha,'dimensions':dimensions,
				'generation_record':record_path.relative_to(PACKET).as_posix(),'attempt':rec.get('attempt'),
				'prompt':prompt,'prompt_sha256':hashlib.sha256(prompt.encode()).hexdigest() if prompt else None,
				'prompt_precision':'unavailable; retained summary only' if rec.get('exact_tool_prompt','__absent__') is None else 'as recorded in linked tool provenance',
				'input_images':inputs,'native_output_path':next((rec.get(k) for k in ['raw_path','raw_generated_path','source_generated_path','native_output_path'] if rec.get(k)),None) or (rec.get('native_output',{}).get('path') if isinstance(rec.get('native_output'),dict) else None),
				'generation_method':'builtin_image_gen','human_decision':'pending','delivery_accepted':False})
	result={'schema':'v4-normalized-generation-provenance-v1','scope':'Actual available tool records, not all-frame cinematic acceptance. Unknown fields stay null; rejected records remain preserved.', 'assets':index}
	write(PACKET/'GENERATION_PROVENANCE.json',result)
	return result


def build() -> dict:
	design = read(PACKET / 'SHOT_DESIGN.json')
	shots = design['shots']
	assert [s['shot'] for s in shots] == EXPECTED, 'Unexpected replacement slate'
	visuals = read(PACKET / 'VISUAL_SELECTIONS.json')
	assembly = read(DRAFT / 'ASSEMBLY_MANIFEST.json')
	copy(DRAFT / 'ASSEMBLY_MANIFEST.json', PACKET / 'audit/CURRENT_ASSEMBLY.json')
	copy(ROOT / 'design/templates/IMAGINE_SHOT_CARD_V1.md', PACKET / 'written_guide/IMAGINE_SHOT_CARD_V1.txt')
	# Resolved current audit only; preliminary conflicting reports are not generator authority.
	write(PACKET / 'audit/UNIFIED_AUDIT.json', read(AUDIT / 'UNIFIED_AUDIT.json'))
	write(PACKET / 'audit/UNIFIED_AUDIT.txt', (AUDIT / 'UNIFIED_AUDIT.md').read_text(encoding='utf-8-sig'))
	unified = read(AUDIT / 'UNIFIED_AUDIT.json')
	assert len(unified['shots']) == 50
	for row in unified['shots']:
		source = assembly['sources'][row['source']]
		row['source_sha256'] = source['sha256']
		row['source_url'] = source.get('source_url')
		row['source_evidence_kind'] = source['kind']
		row['all_frame_acceptance'] = False
	unified['authority_status']='Baseline assembly snapshot. Current owner revisions in CURRENT_REPLACEMENT_DECISIONS.json override these earlier decisions where a shot is listed; old counts are historical, not the current reshoot queue.'
	write(PACKET / 'audit/ACTIVE_SELECTIONS_HASH_BOUND.json', unified)
	write(PACKET/'audit/CURRENT_REPLACEMENT_DECISIONS.json',{
		'schema':'day-one-current-replacement-decisions-v1','baseline':'ACTIVE_SELECTIONS_HASH_BOUND.json',
		'authority':'../SHOT_DESIGN.json','scope':'Current owner-directed replacement-only slate; does not retroactively change the factual baseline review or claim new video was rendered.',
		'shot_count':len(shots),'jobs':[{'shot_id':normalize_id(s['shot']),'decision':'RESHOOT' if s.get('original_source') else 'ADD_MISSING_COVERAGE',
			'reason':s['reason'],'source':s.get('original_source'),'source_sha256':assembly['sources'][s['original_source']]['sha256'] if s.get('original_source') else None,
			'selected_range_half_open':s.get('original_range'),'duration_seconds':s['duration_s'],'shot_card':f"../shots/{normalize_id(s['shot'])}/SHOT_PACKET.json"} for s in shots],
		'generation_ready':False,'delivery_accepted':False})
	provenance = {}
	def add_ref(source: Path, role='archive_visual_reference', inherited=None):
		key = source.resolve().as_posix()
		name = digest(source)[:10] + '_' + source.name
		target = PACKET / 'references' / name
		copy(source,target)
		provenance[target.relative_to(PACKET).as_posix()] = asset_row(target,source.relative_to(ROOT).as_posix() if source.is_relative_to(ROOT) else key,
			role,(inherited or {}).get('license_provenance','Project source authority; inherits ASSET_LICENSES.md restrictions; no new rights granted.'),'byte-identical non-destructive copy')
		if inherited:
			provenance[target.relative_to(PACKET).as_posix()]['original_provenance'] = inherited
		return target.relative_to(PACKET).as_posix()
	# Copy actual prior room, character, prop, style and runtime-boundary references.
	for scene in sorted({s['shot'][:3] for s in shots}):
		old = PRIOR / f'scenes/D1-{scene}/visuals'
		manifest = read(old / 'HANDOFF_PACKET.json')
		for item in manifest['assets']:
			source = old / item['path']
			if source.suffix.lower() not in RASTER or not source.is_file():
				continue
			if item.get('appearance_authority') or item['path'].startswith('handoff_art/') or 'runtime' in item['path'].lower():
				add_ref(source, item.get('role','archive_visual_reference'), item)
		for filename in ['SHARED_STYLE_AND_CHARACTER_GUIDE.txt','SCENE_GUIDE.txt']:
			source = old / 'written_guide' / filename
			if source.is_file():
				copy(source,PACKET / 'written_guide' / f'{scene}_{filename}')
	gen_provenance=generation_index(add_ref)
	# Every current job links source visual evidence separately from bindings.
	claim_rows=[]
	gallery=['# First-frame approval gallery\n','Every image below is a draft opening, not an accepted keyframe. Approve by shot ID and candidate filename/hash. Sol recommendation is not human approval. Rejected visuals remain in the archive but are never enabled as generation bindings.\n', '[Owner-requested revisions and opening reuse](OWNER_REVISION_SUMMARY.md). The active finale is shared teamwork, not isolated helper cuts.\n']
	changed_gallery=['# Latest castle and teamwork revisions for approval\n','These four revised openings replace the earlier castle-route/approach and finale candidates. All remain human-pending. Approving these does not approve the other shots or any generated video. Boards show narrative intent only, never generation pixels.\n','[Actual game layout and detailed event/camera contract](CURRENT_CAMERA_AND_EVENT_AUTHORITY.md) | [All 16 first frames](FIRST_FRAME_APPROVAL.md)\n']
	readme=['# Day One V4 - replacement-only Grok handoff\n',
		'ARCHIVE_COMPLETE: false (local content; see later immutable remote-verification sidecar). GENERATION_READY: false. DELIVERY_ACCEPTED: false.\n',
		'This revision audits the **50 current assembly selections**, including owner Downloads/DaVinci selects. It does not re-label all 159 historical source files as current shots. The earlier V3 archive remains historical evidence.\n',
		'[Review the four latest changes](LATEST_REVISIONS_FOR_APPROVAL.md) | [All first frames](FIRST_FRAME_APPROVAL.md) | [Current replacement decisions](audit/CURRENT_REPLACEMENT_DECISIONS.json) | [Baseline source audit](audit/ACTIVE_SELECTIONS_HASH_BOUND.json) | [Payload and provenance](HANDOFF_PACKET.json)\n',
		'[New C14 team-cleanup coda](../d1_c14_castle_team_cleanup_v1/README.md): separate six-shot, 31-second development packet following the C13 friendship reveal. First-frame approval and runtime integration remain pending; this addition does not approve or replace the V4 jobs.\n',
		'[Latest C13 reveal correction: one bunny, not two](audit/C13_BOSS_DISAPPEARANCE_CORRECTION.md): corrected storyboard, endpoint candidate and actual two-window arena reference. Giant body, face and ears are absent by the final hold; only the four helpers and one tiny rainbow friend remain. All visuals remain approval-pending.\n',
		'## Owner revision now controlling this packet\n','[Revision details](OWNER_REVISION_SUMMARY.md) | [Current castle and suds-finale authority](CURRENT_CAMERA_AND_EVENT_AUTHORITY.md): reuse the otter opening; dry Sky Lagoon castle; distinct Art Room views; actual August 3 Main Hall; restored dusty arena; team lather, rinse and rainbow-friend reveal. Old copied closed-door guides and solo jobs are historical only.\n',
		'## Earlier assembly audit snapshot\n','The earlier 50-select audit recorded 23 keep, 7 provisional, 7 trim, 11 reshoot and 2 omit. Those counts describe that assembly before the owner revisions, not the revised edit below. C09-S04 and C10-S02 remain omitted for reversed game-event order.\n',
		'## Active replacement jobs\n',f'{len(shots)} jobs. C11-S02 is now included because its old door conflicts with the actual hall. C13-S04 builds suds over five seconds; C13-S05 removes them and reveals the tiny friend over eight seconds from a distinct elevated angle. No isolated helper jobs are enabled. The otter opening is reused, not regenerated. C13 remains runtime-disabled pending review and integration.\n',
		'| Shot | Purpose | First-frame review |\n|---|---|---|\n']
	for shot in shots:
		short=shot['shot']; sid=normalize_id(short); jobdir=PACKET / 'shots' / sid
		selected=visuals[short]
		first=inside(selected['first_frame']); board=inside(selected['storyboard'])
		bindings=[{'id':'IMAGE_1','path':first.relative_to(PACKET).as_posix(),'sha256':digest(first),
			'role':'approved_clean_first_frame','role_status':'intended_role_pending_human_approval','hud_present':False,'human_decision':'pending'}]
		for i,bind in enumerate(selected['identity_sources'],start=2):
			ref=add_ref(ROOT / bind['path'],bind['role'])
			bindings.append({'id':f'IMAGE_{i}','path':ref,'sha256':digest(PACKET/ref),'role':bind['role'],
				'hud_present':False,'human_decision':'pending','source_authority_not_automatic_shot_approval':True})
		assert 2 <= len(bindings) <= 4
		game=[]
		for name in shot['game_references']:
			source=ROOT/name
			assert source.is_file(), f'{sid}: missing game reference {name}'
			if source.suffix.lower() in RASTER:
				game.append({'source_path':name,'path':add_ref(source,'underlying_game_asset')})
			else:
				target=PACKET/'written_guide'/(digest(source)[:10]+'_'+source.name+'.txt')
				copy(source,target);game.append({'source_path':name,'path':target.relative_to(PACKET).as_posix()})
		write(jobdir/'PROMPT.txt',shot['prompt'].rstrip()+'\n')
		plan=frame_plan(shot);write(jobdir/'FRAME_PLAN.json',plan)
		write(jobdir/'FRAME_PROMPTS.txt','\n\n'.join(f"FRAME {f['target_frame']:04d}\n{f['reconstruction_prompt']}" for f in plan['frames'])+'\n')
		diagnostics=diagnostic_sheet(shot,assembly)
		if diagnostics:
			for frame in diagnostics['frames']:
				provenance[frame['path']]=asset_row(PACKET/frame['path'],diagnostics['source_path'],'diagnostic_source_frame',
					'Owner-supplied Grok/DaVinci source footage; inherits source restrictions in CURRENT_ASSEMBLY.json and ASSET_LICENSES.md.',f"Exact source frame {frame['index']} decode; no pixel repairs")
			provenance[diagnostics['sheet']]=asset_row(PACKET/diagnostics['sheet'],diagnostics['source_path'],'diagnostic_contact_sheet',
				'Inherits selected source footage restrictions; audit only.',diagnostics['method'])
		review=read(PACKET/'generation_records/SOL_FIRST_FRAME_REVIEW.json')['assets']
		match=[r for r in review if r.get('path')==first.relative_to(PACKET).as_posix() and r['sha256'].lower()==digest(first)]
		decision=match[-1]['sol_decision'] if match else 'NOT_YET_REVIEWED'
		card={'schema':'imagine-shot-packet-v1','movie_id':sid[:6],'shot_id':sid,'status':'DRAFT','mode':'image_to_video',
			'output_disposition':'motion_reference_only','duration_seconds':shot['duration_s'],'aspect_ratio':'16:9','delivery_size':[1280,720],
			'bound_references':bindings,'camera':{'verb':'push_in' if shot.get('camera_move_count') else 'locked','move_count':shot.get('camera_move_count',0),'description':shot['camera']},'must_move':shot['phases'][1]['instruction'],
			'must_not_move':shot['invariants'],'end_state':shot['end_state'],'negative_constraints':shot['invariants'],
			'prompt_path':(jobdir/'PROMPT.txt').relative_to(PACKET).as_posix(),'prompt_sha256':digest(jobdir/'PROMPT.txt'),
			'non_pixel_references':[{'path':board.relative_to(PACKET).as_posix(),'used_as_pixel_reference':False,'role':'narrative_storyboard'}],
			'storyboard_caveat':selected.get('storyboard_caveat'),
			'game_asset_comparison':game,'source_selection':{'filename':shot.get('original_source'),'range_half_open':shot.get('original_range')},
			'weak_source_frames':shot.get('weak_source_frames',[]),'inspected_source_frames':shot.get('inspected_frames',[]),
			'source_visual_evidence':diagnostics,
			'sol_first_frame_decision':decision,'human_decision':'pending','generation_ready':False,'delivery_accepted':False}
		if card['source_selection']['filename']:
			card['source_selection']['sha256']=assembly['sources'][card['source_selection']['filename']]['sha256']
		write(jobdir/'SHOT_PACKET.json',card)
		md=[f"# {sid} - {shot['title']}\n",'DRAFT - human first-frame approval pending. Motion reference only.\n',
			f"{shot['reason']}\n",f"Game seam: {shot['seam']}\n",f"Source: {shot.get('original_source') or 'Missing coverage; no current source frames'}; zero-based half-open select {shot.get('original_range')}.\n",
			f"Weak source evidence: {shot.get('weak_source_frames',[])}. Sampled visual evidence, not every-frame acceptance.\n",
			'## First frame for approval\n',f"Sol: {decision}. Candidate SHA-256: `{digest(first)}`.\n",f"![{sid} opening](../../{first.relative_to(PACKET).as_posix()})\n",
			'## Narrative board - never bind to Grok\n',f"![{sid} board](../../{board.relative_to(PACKET).as_posix()})\n",
			(selected['storyboard_caveat']+'\n') if selected.get('storyboard_caveat') else '',
			('## Endpoint composition candidate - review only\n\n![Corrected endpoint](../../'+selected['endpoint_candidate']+')\n\n[Exact event correction and arena reference](../../audit/C13_BOSS_DISAPPEARANCE_CORRECTION.md). This is not an IMAGE binding or accepted delivery frame.\n') if selected.get('endpoint_candidate') else '',
			'## Bind only these images after approval\n']
		for ref in bindings: md.append(f"- [{ref['id']} - {ref['role']}](../../{ref['path']})\n")
		md += ['\n## Shot and frame instructions\n','[Paste-ready single-shot prompt](PROMPT.txt) | [Every target-frame prompt](FRAME_PROMPTS.txt) | [Frame plan JSON](FRAME_PLAN.json) | [Shot card](SHOT_PACKET.json)\n',
			'```text\n'+shot['prompt']+'\n```\n','## Direct underlying game references\n']
		for ref in game: md.append(f"- [{Path(ref['source_path']).name}](../../{ref['path']}) - source `{ref['source_path']}`\n")
		if diagnostics:
			md += ['\n## Current source frames - audit only\n',f"![Exact source-frame samples](../../{diagnostics['sheet']})\n",f"[Individual source frames and index manifest](../../audit/source_frames/{sid}/SAMPLE_MANIFEST.json)\n"]
		md += ['\nThe source game assets above control event/state and location. A gameplay capture or generated board must never supply generation pixels. The first frame controls the new shot only after your explicit approval.\n']
		write(jobdir/'README.md','\n'.join(md))
		readme.append(f"| [{sid}](shots/{sid}/README.md) | {shot['title']} | {decision}; human pending |\n")
		gallery += [f"## {sid} - {shot['title']}\n",f"{decision}; **human pending**. `{first.name}` / SHA `{digest(first)}`.\n",f"![{sid}]({first.relative_to(PACKET).as_posix()})\n",f"[Shot context and storyboard](shots/{sid}/README.md)\n"]
		if short in {'C11-S01','C11-S02','C13-S04','C13-S05'}:
			changed_gallery += [f"## {sid} - {shot['title']}\n",f"{shot['reason']}\n",f"Camera: {shot['camera']}. Duration: {shot['duration_s']} seconds.\n",f"Sol: {decision}; human approval pending. `{first.name}` / SHA `{digest(first)}`.\n",f"![{sid} revised first frame]({first.relative_to(PACKET).as_posix()})\n",f"![{sid} narrative board]({board.relative_to(PACKET).as_posix()})\n",f"[Complete shot handoff](shots/{sid}/README.md) | [Timeline prompt](shots/{sid}/PROMPT.txt) | [Frame-by-frame reconstruction prompts](shots/{sid}/FRAME_PROMPTS.txt)\n"]
			if selected.get('storyboard_caveat'):changed_gallery.append(selected['storyboard_caveat']+'\n')
		claim_rows.append({'shot_id':sid,'card':f'shots/{sid}/SHOT_PACKET.json','human_approval_pending':True,'sol_decision':decision})
	write(PACKET/'README.md','\n'.join(readme)+ '\n\n## Scope and evidence\n\nFrame plans are authored 24-fps editorial targets, not source measurements or exact Grok frame control. Existing clips are optional motion-analysis inputs only; do not extract them as first-frame identity/layout authority. Review regenerated output against the source game references, opening and endpoint. No output is production-accepted by this packet.\n')
	write(PACKET/'FIRST_FRAME_APPROVAL.md','\n'.join(gallery))
	write(PACKET/'LATEST_REVISIONS_FOR_APPROVAL.md','\n'.join(changed_gallery))
	write(PACKET/'IMAGINE_HANDOFF.json',{'schema':'imagine-handoff-v1','archive_status':'incomplete','generation_status':'blocked',
		'delivery_status':'not_accepted','blocking_findings':['Exact first-frame human approval is pending for every job.','C13 extension and rainbow identity need owner confirmation.','See DRAFT_VALIDATION.json for every individual pending card; rejected visuals cannot be enabled.'],
		'shot_packets':[],'pending_shot_packets':[r['card'] for r in claim_rows],
		'note':'No executable jobs enabled. All pending cards are individually structurally checked; empty executable list is not a claim they passed approval.'})
	# Capture current visual provenance plus every payload file, including rejected candidates.
	for path in sorted(PACKET.rglob('*')):
		if not path.is_file() or path.name in {'HANDOFF_PACKET.json','DRAFT_VALIDATION.json','REMOTE_VERIFICATION.json'} or path.suffix in {'.import','.uid'}: continue
		rel=path.relative_to(PACKET).as_posix()
		if rel not in provenance:
			role='archive_sidecar'
			license_text='Project-authored scoped handoff documentation; references inherit original source restrictions.'
			if path.suffix.lower() in RASTER:
				role='narrative_storyboard' if 'storyboard' in rel else 'first_frame_candidate' if 'first_frames' in rel else 'endpoint_composition_candidate' if 'endpoint_frames' in rel else 'audit_or_normalized_reference'
				license_text='Project-requested OpenAI built-in image generation or attributed non-destructive reference derivative; see generation_records and normalization sidecars. Human pending, no delivery approval.'
			provenance[rel]=asset_row(path,rel,role,license_text,'see generation record; native generated candidate preserved' if 'first_frames' in rel or 'storyboards' in rel or 'endpoint_frames' in rel else 'project-authored sidecar or attributed derivative')
			if rel.startswith('references/owner_opening/') and path.suffix.lower()=='.mp4':
				provenance[rel]=asset_row(path,'C:/Users/Peter/Downloads/'+path.name,'preserved_owner_selected_motion_reference',
					'Owner-supplied Grok/DaVinci review master; retain original source restrictions. No final-delivery or license-transfer claim. See audit/OTTER_EDIT_PLAN.json.',
					'Byte-identical source copy; no re-encoding, trimming or pixel changes.')
		matches=[r for r in gen_provenance['assets'] if r['path']==rel and r['sha256']==digest(path)]
		if matches:
			provenance[rel]['generation_provenance_records']=list(dict.fromkeys(r['generation_record'] for r in matches))
			provenance[rel]['source_path']=next((r['native_output_path'] for r in matches if r['native_output_path']),matches[-1]['generation_record'])
	rows=[provenance[k] for k in sorted(provenance)]
	payload=''.join(f"{r['path']}\t{r['sha256']}\t{r['bytes']}\n" for r in rows).encode()
	write(PACKET/'HANDOFF_PACKET.json',{'schema':'external-animation-visual-packet-v1','packet_id':REL.name,'runtime_asset':False,
		'archive_complete':False,'generation_ready':False,'delivery_accepted':False,'assets':rows,'payload_sha256':hashlib.sha256(payload).hexdigest(),
		'payload_hash_formula':'SHA256 of sorted UTF-8 path TAB sha256 TAB bytes LF; excludes this manifest, DRAFT_VALIDATION.json, REMOTE_VERIFICATION.json, and generated .import/.uid sidecars.',
		'approval_gate':'Approve exact first-frame filename and hash per shot; Sol recommendation never authorizes generation.',
		'authority_order':['underlying implemented game event/state and approved identities','human-approved shot first frame','written single-shot action and seam','narrative boards (no generation pixels)'],
		'jobs':claim_rows})
	return validate()


def validate() -> dict:
	from audit_imagine_handoff import audit_shot, audit_handoff
	manifest=read(PACKET/'HANDOFF_PACKET.json'); findings=[]; pending=[]
	for row in manifest['assets']:
		path=inside(row['path'])
		if digest(path)!=row['sha256']: findings.append('stale payload: '+row['path'])
	for job in manifest['jobs']:
		for error in audit_shot(PACKET,PACKET/job['card']):
			if error.endswith('must be human accepted'): pending.append(error)
			else: findings.append(error)
		card=read(PACKET/job['card']);sid=card['shot_id']
		frames=read(PACKET/f'shots/{sid}/FRAME_PLAN.json')['frames']
		if [f['target_frame'] for f in frames]!=list(range(round(card['duration_seconds']*24))): findings.append(sid+' missing target frames')
		if card['human_decision']!='pending' or card['generation_ready'] or card['delivery_accepted']:findings.append(sid+' invalid approval claim')
	findings += audit_handoff(PACKET)
	result={'schema':'pending-handoff-structural-validation-v1','structural_errors':findings,'expected_human_approval_blocks':pending,
		'job_count':len(manifest['jobs']),'target_frame_count':sum(read(PACKET/f"shots/{j['shot_id']}/FRAME_PLAN.json")['target_frame_count'] for j in manifest['jobs']),
		'payload_sha256':manifest['payload_sha256'],'structural_pass':not findings,'generation_ready':False,'delivery_accepted':False}
	write(PACKET/'DRAFT_VALIDATION.json',result)
	assert not findings, '\n'.join(findings)
	return result


if __name__ == '__main__':
	parser=argparse.ArgumentParser();parser.add_argument('--validate-only',action='store_true');args=parser.parse_args()
	result=validate() if args.validate_only else build()
	print(json.dumps({k:v for k,v in result.items() if k!='expected_human_approval_blocks'},indent=2))
