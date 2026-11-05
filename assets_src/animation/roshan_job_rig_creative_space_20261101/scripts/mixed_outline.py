"""The original one-figure silhouette floor, independently of swap determinism."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
from audit_study import pixel_checks
P=Path(__file__).resolve().parents[1];folder=P/'evidence/raw/mixed'
rows=[]
for row in json.loads((folder/'samples.json').read_text()):
    path=folder/row['file'];pixels=pixel_checks(Image.open(path).convert('RGBA'))
    rows.append(dict(**row,png_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),pixels=pixels,passed=pixels['large_components']==1 and pixels['edge_alpha_pixels']==0))
bad=[r for r in rows if not r['passed']]
out=P/'evidence/mixed';out.mkdir(exist_ok=True)
for index,row in enumerate(bad[:12]):(out/row['file']).write_bytes((folder/row['file']).read_bytes())
board=Image.new('RGB',(1280,960),'#172033');draw=ImageDraw.Draw(board)
for index,row in enumerate(bad[:12]):
    source=Image.open(folder/row['file']).convert('RGBA');bg=Image.new('RGBA',source.size,'#dbe3ea');bg.alpha_composite(source);bg.thumbnail((320,290));x=(index%4)*320;y=(index//4)*320;board.paste(bg.convert('RGB'),(x,y));draw.text((x+5,y+292),row['head']+'/'+row['body']+'/'+row['tail'],fill='white')
board.save(out/'failures_board.jpg',quality=93)
result=dict(passed=len(rows)==375 and not bad,cases=len(rows),failed_cases=len(bad),rows=rows,thresholds='Unmodified original pixel_checks: alpha>96, connected components>12 pixels, exactly one figure and no edge alpha.',diagnosis='Fresh-versus-live equality does not prove a valid outline. Legacy v8 body/tail domain joins already fail some mixtures; new combinations are checked at the same floor. The shared contract/waist join owner must resolve compatibility; this packet does not modify legacy fixture art or fork a skeleton.',limits='Snapshots at 1.5s, 125 mixtures x three original clips; not every-frame mixed geometry or artistic/device/child/owner acceptance.')
(out/'audit.json').write_text(json.dumps(result,indent=2)+'\n')
print('MIXED OUTLINE',result['passed'],'cases',len(rows),'failed',len(bad))
raise SystemExit(0 if result['passed'] else 1)
