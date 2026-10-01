"""Render the source-bound review packet; this tool never generates artwork grades."""
from pathlib import Path
import argparse, hashlib, html, json
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "assets_src/imagegen/day2_replacements_batch1_20260930"
def sha(path):
	return hashlib.sha256(path.read_bytes()).hexdigest()
def preview_size(x):
	return 36 if x["id"]=="D2A-0495" else 64 if x["id"] in ("D2A-0635","D2A-0636","D2A-0637") else 116 if x["id"]=="D2A-0446" else 112
def check(data):
	assert (BASE / ".gdignore").exists()
	assert data["owner_approval"] is None and not data["runtime_integration"]
	assert len(data["items"]) == len({x["id"] for x in data["items"]}) == 8
	for x in data["items"]:
		assert sha(ROOT/x["source_path"]) == sha(ROOT/x["source_reference"]) == x["source_sha256"]
		assert sha(ROOT/x["selected_candidate"]) == x["selected_sha256"] == x["visual_reviewed_sha256"]
		assert 4.5 <= x["quality_score"] < 5 and x["source_review_complete"] and x["owner_approval"] is None
		assert all(4.5 <= value < 5 for value in x["criteria_scores"].values())
		im=Image.open(ROOT/x["selected_candidate"])
		assert im.mode == "RGBA" and im.size == (1024,1024)
		alpha=im.getchannel("A")
		assert alpha.getextrema() == (0,255)
		assert all(im.getpixel(p)[3] == 0 for p in [(0,0),(1023,0),(0,1023),(1023,1023)])
		bbox=alpha.point(lambda value:255 if value>=8 else 0).getbbox()
		assert bbox and bbox[0]>0 and bbox[1]>0 and bbox[2]<1024 and bbox[3]<1024
		assert sha(ROOT/x["mobile_candidate"]) == x["mobile_sha256"] == x["mobile_visual_reviewed_sha256"]
		assert 4.5 <= x["mobile_quality_score"] < 5
		mobile=Image.open(ROOT/x["mobile_candidate"])
		edge=512 if x["id"] in ("D2A-0394","D2A-0056","D2A-0057") else 256
		assert mobile.mode == "RGBA" and mobile.size == tuple(x["mobile_dimensions"]) == (edge,edge)
		assert all(mobile.getpixel(p)[3] == 0 for p in [(0,0),(edge-1,0),(0,edge-1),(edge-1,edge-1)])
		bounds=mobile.getchannel("A").point(lambda value:255 if value>=8 else 0).getbbox()
		assert bounds and bounds[0]>0 and bounds[1]>0 and bounds[2]<edge and bounds[3]<edge
		for a in x["attempts"]:
			assert sha(ROOT/a["native_path"]) == a["native_sha256"]
			assert sha(ROOT/a["prompt_path"]) == a["prompt_sha256"]
			assert all(sha(ROOT/r["path"]) == r["sha256"] for r in a["bound_references"])
			if not a["bound_references"]:
				assert a["input_images"]==0 and "fresh text-to-image" in a["generation_method"]
		for old in x.get("retained_rejected_derivatives",[]):
			assert sha(ROOT/old["selected_path"])==old["selected_sha256"]
			assert sha(ROOT/old["mobile_path"])==old["mobile_sha256"]
		if "prior_owner_rejected_candidate" in x:
			old=x["prior_owner_rejected_candidate"]
			assert sha(ROOT/old["selected_path"])==old["selected_sha256"]
			assert sha(ROOT/old["mobile_path"])==old["mobile_sha256"]
		a=next(a for a in x["attempts"] if a["attempt"]==x["selected_attempt"])
		assert a["score"]==x["quality_score"]
		if x.get("source_style_status")=="OWNER_REJECTED_TOO_LIFELIKE":
			assert a["review"]=="OWNER_REJECTED_TOO_LIFELIKE" and x["source_target_met"] is False
			assert x["owner_feedback"]["candidate_sha256"]==x["selected_sha256"]
		else:
			assert a["review"]=="SELECTED_CANDIDATE_MEETS_DRAFT_SOURCE_TARGET"
	assert data["generation_count"]==sum(len(x["attempts"]) for x in data["items"])
	assert data["quality_gate"]["all_selected_meet_source_target"] is False
	assert data["quality_gate"]["owner_style_rejected_ids"]==["D2A-0446"]
	print(f'DAY2_REPLACEMENTS|PASS|8 preserved review masters +8 mobile candidates; {data["generation_count"]} native attempts; exact hashes; RGBA/margins; nursery owner style rejection; approval pending')
def relative(path):
	return Path(path).relative_to(BASE.relative_to(ROOT)).as_posix()
def build(data):
	check(data)
	board=Image.new("RGB",(1024,2048),"#faf7ed")
	pen=ImageDraw.Draw(board)
	for index,x in enumerate(data["items"]):
		y=index*256
		pen.text((14,y+6),f'{x["id"]} {x["name"]}  {x["source_score"]} -> {x["quality_score"]}/5',fill="#29253e")
		for left,key,label in [(10,"source_reference","Original"),(265,"selected_candidate","Current candidate")]:
			pen.text((left,y+25),label,fill="#29253e")
			pic=Image.open(ROOT/x[key]).convert("RGBA")
			pic.thumbnail((230,212),Image.Resampling.LANCZOS)
			board.paste(pic,(left+(235-pic.width)//2,y+42+(212-pic.height)//2),pic)
		size=preview_size(x)
		for left,color,label in [(530,"#fff8e4","Light"),(777,"#18203b","Dark")]:
			pen.text((left,y+25),f'{label} {size}px mobile proxy',fill="#29253e")
			pen.rectangle((left,y+44,left+234,y+244),fill=color)
			pic=Image.open(ROOT/x["mobile_candidate"]).resize((size,size),Image.Resampling.LANCZOS)
			board.paste(pic,(left+(234-size)//2,y+44+(200-size)//2),pic)
	board.save(BASE/"comparison_board.png")
	lines=["# Day Two replacement artwork — first approval batch","","Status: **candidate files ready for user review; user approval pending**. Eight separate replacement files address named source-image defects. No live game texture or protected original is changed. The original 637-image audit and 432-item inclusive priority queue retain their history.","","[Illustrated before/after review](index.html) · [Exact manifest and prompts](MANIFEST.json) · [Public GitHub verification receipt](REMOTE_VERIFICATION.json)","","## Result and scoring","","Eight selected candidates score **4.5–4.7/5** in Codex source review, meeting the requested minimum **4.5/5**. Twelve built-in imagegen calls were used: nine image edits and three fresh nursery text-to-image generations with zero image bindings. The first Kitchen attempt is retained and rejected at4.3 for emblem drift. The first nursery candidate retains its historical4.6 Codex opinion but is owner-rejected for game-style mismatch; it is no longer the selected candidate. The first two fresh trials are retained and rejected at4.3 for native-edge artifacts; the third fresh trial is selected at4.5 with tiny remaining specks disclosed.","","The five criteria are identity/visual role, contour/isolation, palette/value, painted material finish and small-scale readability. Each also meets 4.5 in this draft. These are authored visual opinions bound to exact selected hashes; this tool checks the binding and never grades a new image. No 5/5 or owner/runtime acceptance is claimed under DL-VIS-07 and DL-VIS-08.","","## Individual results","","| Item | Original score | Selected score | Attempts |","|---|---:|---:|---:|"]
	for x in data["items"]:
		lines.append(f'| {x["id"]} — {x["name"]} | {x["source_score"]}/5 | {x["quality_score"]}/5 | {len(x["attempts"])} |')
	lines += ["","![Before/after and small-scale inspection](comparison_board.png)","","The board and HTML show inspection-only composites on neutral cream/navy mats. These are source readability proxies, not current runtime screenshots or generation inputs. Wheel previews use the actual36px draw size, nursery arms use116px, badges use64px and other proxies use112px. Comparison-board pixels never become replacement art.",""]
	cards=[]
	for x in data["items"]:
		before,after=relative(x["source_reference"]),relative(x["selected_candidate"])
		mobile=relative(x["mobile_candidate"])
		lines += [f'## {x["id"]} — {x["name"]}',"",f'**Before {x["source_score"]}/5 → candidate {x["quality_score"]}/5.** {x["evaluation"]}',"",f'**Interaction/integration review:** {x["runtime_review_required"]}',"",f'[Original comparison reference]({before}) · [Selected 1024px RGBA candidate]({after})',"","Criterion scores: "+"; ".join(f'{k.replace("_"," ")} {v}/5' for k,v in x["criteria_scores"].items())+".","",f'Source: {x["source_path"]}. Source SHA-256: {x["source_sha256"]}. Selected SHA-256: {x["selected_sha256"]}.',""]
		size=preview_size(x)
		attempts="".join(f'<li>Attempt {a["attempt"]}: {html.escape(a["review"])} · {a["score"]}/5 · <a href="{relative(a["native_path"])}">native PNG</a> · <a href="{relative(a["prompt_path"])}">exact prompt</a></li>' for a in x["attempts"])
		cards.append(f'''<article id="{x["id"]}"><h2>{x["id"]} · {html.escape(x["name"])}</h2><p class="score">{x["source_score"]}/5 → {x["quality_score"]}/5 <span>Draft source review · owner approval pending</span></p><div class="pair"><figure><div class="mat"><img src="{before}" alt="Original {html.escape(x["name"])}"></div><figcaption>Existing source</figcaption></figure><figure><div class="mat"><a href="{after}"><img src="{after}" alt="Selected {html.escape(x["name"])}"></a></div><figcaption>Selected candidate · click for full size</figcaption></figure></div><p>{html.escape(x["evaluation"])}</p><div class="proxies"><div class="light"><img src="{after}" style="width:{size}px;height:{size}px" alt="Light small-scale proxy"></div><div class="dark"><img src="{after}" style="width:{size}px;height:{size}px" alt="Dark small-scale proxy"></div></div><p class="small">{size}px source proxy; not a runtime capture.</p><details><summary>Interaction, attempts and provenance</summary><p>{html.escape(x["runtime_review_required"])}</p><ul>{attempts}</ul><p class="hash">Original SHA-256 {x["source_sha256"]}<br>Selected SHA-256 {x["selected_sha256"]}</p></details></article>''')
	lines += ["## Reuse, provenance and technical handling","",f'Task baseline: exact integration {data["source_revision"]}. Existing sources, physical-door/elevator manifest, source masters, Tree Book and specialist draw routes were inventoried. Nine earlier edits bind existing artwork; the three fresh nursery trials use only written briefs and zero bound images, as explicitly commissioned by the owner. No new baby, face, torso, unrelated scene or full actor redesign is commissioned.',""]
	lines += [f'- **{key.title()}:** {reason}' for key,reason in data["source_gap_and_reuse"].items()]
	lines += ["","Every native 1254×1254 generated PNG is preserved byte-for-byte. Selected textures are whole-canvas aspect-preserving reductions to 1024×1024. No subject is cropped, shifted, warped, keyed, composited or locally repaired in post-processing. Native/selected hashes, complete prompts, bound reference roles/hashes and attempt decisions are in MANIFEST.json. The .gdignore keeps native, rejected and review art outside runtime import.","","Selected files have true RGBA, transparent corners and a complete visible alpha>=8 footprint inside the canvas. Very faint alpha 1–7 residue can extend outside that footprint; it is recorded rather than silently deleted. The reviewed light/dark proxies show no visible plates, bars or solid edge clipping. Actual game sampling and device presentation still need review.","","## Remaining queue and next decisions","","This is the initial eight-item set, not a claim that all 432 priorities are repaired. The remaining **424** original queue entries include **149 inactive, retired or reference alternatives**, plus actor atlases, background families, vector/procedural graphics and context-dependent items. Each needs its own usage/reuse decision.","","The faceted racer portrait D2A-0054 should first be compared with the existing painted racer-imp family and real draw route. The ballet flower disc, Detective spotlight, opaque Painter brush and Candy cart remain route-dependent candidates. Old tail-cropped Roshan cards should give way to existing full-tail atlases where applicable. Protected doll originals remain intact; later isolation needs separate attributed derivatives. Background families require native-coverage, composition and seam review and cannot be regenerated tile by tile. None is silently marked repaired by this batch.","","## Verification and user approval","","Machine evidence is in [VERIFICATION.json](VERIFICATION.json): exact source/reference/prompt/output hashes, 1024 and256/512 RGBA/margins, original preservation, browser/image decoding, document authority, change coverage and the shrinking 2D gate. Full CI results are linked when available. Checks never supply visual ratings or user approval.","","**User decision requested:** approve this report and the eight selected source candidates, or name item IDs for another revision. Approval must come from the user. All owner_approval fields remain null until that response. Runtime integration, live motion/contact, target device, child and whole-game acceptance are separate. No finding is closed and no release is authorized by this draft.",""]
	lines.insert(lines.index("## Remaining queue and next decisions"), "## Mobile replacement files\n\nThe mobile copies were separately inspected on light/dark mats at 36px (wheel), 116px (nursery arms), 64px (badges) and112px (other cues). All eight retain their 4.5–4.7/5 draft source grades after reduction. Their exact reviewed hashes are recorded separately. The originals, 1254px native generations and 1024px review masters remain intact.\n\n| Mobile file | Size | Draft source score |\n|---|---:|---:|\n" + "\n".join(f'| [{x["id"]}]({relative(x["mobile_candidate"])}) | {x["mobile_dimensions"][0]}×{x["mobile_dimensions"][1]} | {x["mobile_quality_score"]}/5 |' for x in data["items"]) + "\n\nOne whole-canvas Lanczos reduction directly from each selected native generation makes these copies. The eight mobile textures total **4.25 MiB of decoded RGBA**, compared with **32 MiB** for eight 1024px textures. This is a dimension-based estimate, not measured APK/VRAM savings or a device frame-rate result. Live game sampling, overlap and target-device performance remain to be tested when integration is commissioned.\n")
	# Direct owner feedback supersedes historical source scores for acceptance.
	lines[2]="Status: **seven source candidates await review; nursery v4 remains style rejected**. The owner finds it improved but still too lifelike. Historical scores and all image bytes are preserved; no source or motion candidate has owner approval."
	result_index=lines.index("## Result and scoring")+2
	lines[result_index]="Historical Codex source opinions for the eight preserved candidates are **4.5–4.7/5**. Owner feedback supersedes the nursery v4 opinion for current style acceptance: **D2A-0446 needs simpler illustrated forms and remains an update priority**. Its4.5 score is retained as history, not a current style pass. Twelve imagegen calls and all rejected attempts remain preserved. The other seven source candidates are unchanged and await owner review."
	lines.insert(lines.index("## Individual results"), "## Local motion queue\n\nThe owner requests studies through the developed local ComfyUI workflow. [Five individual briefs and source plates](../../local_motion/day2_batch1_20260930/index.html) cover boxing puff, nursery gesture, mounted wheel, maple and dogwood. [Timestamped queue snapshot](../../local_motion/day2_batch1_20260930/QUEUE_SNAPSHOT.json) distinguishes local FIFO entries from native prompt submission. All outputs are LOCAL_MOTION_REFERENCE_ONLY. Nursery uses the rejected v4 still only to study a gentle catching gesture; motion cannot repair or approve its appearance. Navigation badges stay static.\n")
	for i,line in enumerate(lines):
		if line.startswith("**User decision requested:**"):
			lines[i]="**Owner review remains open.** Nursery v4 is explicitly rejected for lifelike styling and needs a later simpler still revision. The other seven source candidates and the written report await owner review. All owner_approval fields remain null. Queuing or rendering a reference does not grant visual, contact, device, child, runtime or cinematic delivery acceptance. No finding is closed and no release is authorized."
		if line.startswith("The five criteria are"):
			lines[i]=line.replace("Each also meets 4.5 in this draft.","Their recorded values describe the earlier Codex draft review; nursery owner feedback overrides style acceptance.")
		if "All eight retain their 4.5–4.7/5 draft source grades after reduction." in line:
			lines[i]=line.replace("All eight retain their 4.5–4.7/5 draft source grades after reduction.","Historical4.5–4.7/5 source opinions remain recorded after reduction; nursery is currently style rejected.")
	(BASE/"REPORT.md").write_text("\n".join(lines).rstrip()+"\n",encoding="utf-8")
	page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Day Two replacement artwork approval batch</title><style>*{box-sizing:border-box}body{margin:0;background:#fbf8ef;color:#29253e;font:17px/1.6 system-ui}header,main{max-width:1120px;margin:auto;padding:30px}h1{font-family:Georgia,serif;font-size:clamp(30px,5vw,56px);line-height:1.15}h2{font-size:22px}a{color:#5b397d}.notice{background:#eee5f3;border-left:5px solid #765596;padding:18px}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:28px}article{background:white;border:1px solid #d8cfe1;border-radius:16px;padding:20px;min-width:0}article p{overflow-wrap:anywhere}.score{font-weight:bold;font-size:24px}.score span{display:block;font-size:14px;font-weight:normal}.pair{display:grid;grid-template-columns:1fr 1fr;gap:12px}figure{margin:0}.mat{background:#e7deef;border-radius:9px;display:flex;align-items:center;justify-content:center;height:220px}.mat img{width:100%;height:210px;object-fit:contain}.mat a{display:block;width:100%;height:100%}figcaption,.small{font-size:13px}.proxies{display:grid;grid-template-columns:1fr 1fr;gap:12px}.proxies>div{height:145px;display:flex;align-items:center;justify-content:center;border-radius:8px}.light{background:#fff8e4}.dark{background:#18203b}.proxies img{object-fit:contain}.hash{font:12px/1.6 monospace;overflow-wrap:anywhere}summary{cursor:pointer;font-weight:600}.board{max-width:100%;height:auto}@media(max-width:700px){header,main{padding:18px}.grid{grid-template-columns:1fr}.mat{height:190px}.mat img{height:180px}}</style><header><p>Mermaid Roshan · 30 September 2026</p><h1>Eight replacement candidates<br>ready for your review</h1><p>Before/after artwork, scores, small-scale checks and every generation attempt.</p><p class="notice">All eight meet the 4.5/5 draft source target. Your approval is pending. Originals, gameplay and saves are preserved; these are separate review files.</p><p><a href="REPORT.md">Comprehensive report</a> · <a href="MANIFEST.json">Manifest and provenance</a> · <a href="VERIFICATION.json">Machine verification</a> · <a href="REMOTE_VERIFICATION.json">GitHub receipt</a> · <a href="selected/">Selected files</a></p><p>Approve the report and all eight candidates in chat, or name IDs for revision. This page never records approval on your behalf.</p></header><main><div class="grid">CARDS</div><details><summary>Full comparison board</summary><img class="board" src="comparison_board.png" alt="Eight before/after comparisons and small source proxies"></details></main></html>'''.replace("CARDS","".join(cards))
	for x in data["items"]:
		after=relative(x["selected_candidate"]);mobile=relative(x["mobile_candidate"])
		page=page.replace(f'<figcaption>Selected candidate · click for full size</figcaption>', '<figcaption>Review master · click for full size</figcaption>', 1)
		page=page.replace(f'<p class="small">{preview_size(x)}px source proxy; not a runtime capture.</p>',f'<p class="small"><a href="{mobile}">Mobile replacement · {x["mobile_dimensions"][0]}px</a> · {x["mobile_quality_score"]}/5. Source proxy; not a runtime capture.</p>',1)
		page=page.replace(f'src="{after}" style=',f'src="{mobile}" style=')
	page=page.replace('<a href="selected/">Selected files</a>','<a href="mobile/">Mobile replacement files</a> · <a href="selected/">1024px review masters</a>')
	page=page.replace("All eight meet the 4.5/5 draft source target. Your approval is pending.","Nursery v4 is improved but still too lifelike per owner feedback: style revision required. Historical4.5–4.7 scores do not establish approval.")
	page=page.replace("Approve the report and all eight candidates in chat, or name IDs for revision. This page never records approval on your behalf.","Seven sources await owner review. Nursery remains style rejected. <a href=\"../../local_motion/day2_batch1_20260930/index.html\">Five local ComfyUI motion studies and queue</a> are separate references; no artwork approval is recorded on your behalf.")
	page=page.replace("4.5/5 <span>Draft source review · owner approval pending</span>","4.5/5 <span>Historical source opinion · owner rejects lifelike nursery styling</span>")
	(BASE/"index.html").write_text(page,encoding="utf-8")
	print("Rendered report and illustrated approval page; authored scores unchanged.")
if __name__=="__main__":
	parser=argparse.ArgumentParser();parser.add_argument("--check",action="store_true");args=parser.parse_args()
	data=json.loads((BASE/"MANIFEST.json").read_text(encoding="utf-8"))
	check(data) if args.check else build(data)
