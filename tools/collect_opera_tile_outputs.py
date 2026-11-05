from pathlib import Path
import json,shutil,hashlib,sys
from PIL import Image
r=Path(__file__).resolve().parents[1]
d=r/"assets_src/review/opera_exploration_v1/tiled_detail"
data=json.loads((d/sys.argv[1]).read_text(encoding="utf-8"))
output=d/"tile_outputs";output.mkdir(exist_ok=True)
ledger=d/"generation_log.json"
allrows=json.loads(ledger.read_text(encoding="utf-8")) if ledger.exists() else []
for row in data:
 source=Path(row["source_path"])
 if not source.resolve().is_relative_to(Path(r"C:/Users/Peter/.codex/generated_images").resolve()):raise ValueError("Unexpected generated output root")
 ident=row["id"]
 target=output/(ident+".png") if ident.startswith("r") else d/(ident+"_raw.png")
 if target.exists() and target.read_bytes()!=source.read_bytes():raise ValueError("Refusing to overwrite a different native output")
 shutil.copy2(source,target)
 row.update(saved_path=target.relative_to(r).as_posix(),sha256=hashlib.sha256(target.read_bytes()).hexdigest(),native_size=list(Image.open(target).size))
 if not any(a["id"]==ident for a in allrows):allrows.append(row)
ledger.write_text(json.dumps(allrows,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"collected":len(data),"total_calls":len(allrows),"native_outputs":[{"id":a["id"],"size":a["native_size"]} for a in data]}))

