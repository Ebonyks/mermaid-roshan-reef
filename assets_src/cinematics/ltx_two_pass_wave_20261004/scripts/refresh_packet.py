"""Inventory completed, real source-study artifacts; no future evidence placeholders."""
from pathlib import Path
import json,hashlib,struct,subprocess
from PIL import Image
p=Path(__file__).resolve().parents[1];r=p.parents[2]
def sha(f):
 with Path(f).open("rb") as stream:return hashlib.file_digest(stream,"sha256").hexdigest()
media={".png",".mp4",".aseprite",".latent"}
previous=p.parent/"ltx_registered_wave_20261004"
old=json.loads((previous/"manifest.json").read_text());old_by_sha={}
for row in old["payload"]:old_by_sha.setdefault(row["sha256"],[]).append((previous/row["path"]).relative_to(r).as_posix())
frames={};payload=[];rows=[]
for f in sorted(p.rglob("*")):
 if not f.is_file() or f.name in {"manifest.json","remote_verification.json","remote_receipt_publication.json"}:continue
 rel=f.relative_to(p).as_posix();repo=f.relative_to(r).as_posix();h=sha(f);parents=old_by_sha.get(h,[])[:4]
 item={"path":rel,"sha256":h,"bytes":f.stat().st_size,"acceptance":"SOURCE_ONLY; owner/device/child acceptance absent"}
 if rel.startswith("inputs/"):
  role="complete_figure_reference_or_editable_guide";mod="Aseprite complete-figure guide/canvas normalization; registration does not freeze body parts."
  if f.name=="missing_lowering_native.png":
   role="native_imagegen_missing_complete_figure_key";mod="One named missing whole-figure pose; transparent1024x1536 native retained; owner review pending."
   parents=["assets/characters/roshan_25d/roshan_gesture_a.png",str(p.relative_to(r)/"inputs/portrait_rgba_02.png"),str(p.relative_to(r)/"inputs/portrait_rgba_03.png")]
  elif f.name.startswith("guide_"):
   idx=int(f.stem.split("_")[-1]);source="portrait_key_00.png" if idx in [0,3,36,40] else {7:"portrait_key_01.png",17:"portrait_key_02.png",22:"portrait_key_mid.png",27:"portrait_key_03.png"}[idx]
   parents=[(p/"inputs"/source).relative_to(r).as_posix()]
  elif "missing_lowering" in f.name:parents=[(p/"inputs/missing_lowering_native.png").relative_to(r).as_posix()]
  elif f.name in {"portrait_rgba_mid.png","portrait_key_mid.png"}:parents=[(p/"inputs/missing_lowering_native.png").relative_to(r).as_posix()]
  elif f.name.startswith("portrait_"):parents=[(previous/f"inputs/figure_rgba_{i:02d}.png").relative_to(r).as_posix() for i in range(4)]
  elif f.name=="wave_guides.aseprite":parents=[(p/f"inputs/guide_{i:04d}.png").relative_to(r).as_posix() for i in [0,3,7,17,22,27,36,40]]
 elif rel.startswith("results/"):
  take=rel.split("/")[1];base=p/"results"/take
  role="model_output_or_native_editable_review";mod="Complete native generated frames or declared whole-frame encoding/cadence; no isolated limb repair."
  if "_frames/" in rel:
   role="native_model_frame" if "requested_canvas_frames" not in rel else "declared_whole_canvas_recipe_output"
   item.update(timeline_index=int(f.stem),generation_record=(base/"receipt.json").relative_to(r).as_posix(),workflow_record=(base/"workflow.api.json").relative_to(r).as_posix())
   parents=[(p/f"inputs/guide_{i:04d}.png").relative_to(r).as_posix() for i in [0,3,7,17,22,27,36,40]]
  else:parents=[(base/"receipt.json").relative_to(r).as_posix()];parents=[] if f.name=="receipt.json" else parents
  if f.suffix in {".mp4",".aseprite"}:item["cadence_record"]=(base/"cadence.json").relative_to(r).as_posix() if (base/"cadence.json").exists() else "Canonical24fps PNG timeline"
 elif rel.startswith("comparison/"):
  role="native_unscaled_same_content_comparison";mod="Native complete source frames padded side by side, no spatial resampling."
 else:role="workflow_or_actual_evidence";mod="Source-side instructions/receipts/code; no production pixel acceptance."
 parents=[x.replace("\\","/") for x in parents]
 if any(not (r/x).is_file() for x in parents):raise ValueError((rel,"Missing source parent",parents))
 item.update(role=role,modification_status=mod,source_paths=parents,source_sha256={x:sha(r/x) for x in parents if (r/x).is_file()},license_provenance="Project-owned Roshan derivative; ImageGen where declared; LTXVideo OpenWeights0.X for2B/upscaler; LTX Community License and Gemma terms for2.3. Model weights not redistributed. Source code retains its own license.")
 if f.suffix==".png":
  with Image.open(f) as im:item.update(dimensions=list(im.size),mode=im.mode)
 if f.suffix==".aseprite":
  header=f.read_bytes()[:14];item.update(dimensions=list(struct.unpack_from("<HH",header,8)),frames=struct.unpack_from("<H",header,6)[0])
 if f.suffix==".mp4":
  ff=r"C:\Users\Peter\AppData\Local\Programs\MermaidReefTools\FFmpeg\8.1.2\bin\ffprobe.exe"
  d=json.loads(subprocess.run([ff,"-v","error","-show_streams","-of","json",str(f)],capture_output=True,text=True,check=True).stdout);v=next(x for x in d["streams"] if x["codec_type"]=="video");item.update(dimensions=[v["width"],v["height"]],frames=int(v["nb_frames"]),fps=v["avg_frame_rate"])
 if f.suffix in media:rows.append(f'| `{repo}` | Project-owned Roshan; ImageGen/LTX derivative as declared; LTXVideo OpenWeights0.X or LTX Community License/Gemma terms by receipt | https://github.com/Ebonyks/mermaid-roshan-reef/tree/8a2f30cb0df44ece3b1172ed2dbcb9a55fc5d622/assets/characters/roshan_25d | {mod} Source-only; no runtime acceptance. |')
 payload.append(item)
license_path=r/"ASSET_LICENSES.md";text=license_path.read_text(encoding="utf-8");marker="\n## Two-pass portrait refinement comparison — 2026-10-04\n"
if marker in text:text=text[:text.index(marker)]
text+=marker+"\n| Asset | Source/license | Source URL | Modifications |\n|---|---|---|---|\n"+"\n".join(rows)+"\n";license_path.write_text(text,encoding="utf-8")
manifest={"schema":"source-study-payload-v1","status":"REFERENCE_ONLY","baseline":"8a2f30cb0df44ece3b1172ed2dbcb9a55fc5d622","payload":payload,"payload_sha256":hashlib.sha256("\n".join(x["path"]+" "+x["sha256"] for x in payload).encode()).hexdigest(),"acceptance":"No production, runtime, owner/device/child acceptance; see exact per-take reviews.","model_weights_redistributed":False,"previous_evidence":["assets_src/cinematics/ltx_registered_wave_20261004/manifest.json","assets_src/cinematics/ltx_retake_repair_20261004/manifest.json"]}
(p/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
i=r/"design/audit_impacts/ltx-two-pass-wave-20261004.json";impact=json.loads(i.read_text());impact["files"]=[f.relative_to(r).as_posix() for f in sorted(p.rglob("*")) if f.is_file()]+["ASSET_LICENSES.md","audit/animation/README.md","audit/MASTER_AUDIT_2026-08-09.md","design/05_DOC_LEDGER.md","design/animation/ANIMATION_PRODUCTION_PROTOCOL.md"];i.write_text(json.dumps(impact,indent=2)+"\n");print("INVENTORY",len(payload),"actual files",len(rows),"asset rows",flush=True)
