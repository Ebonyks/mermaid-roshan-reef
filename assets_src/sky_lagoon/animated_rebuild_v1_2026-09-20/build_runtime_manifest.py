from pathlib import Path
import hashlib,json,re
from PIL import Image
W=Path(__file__).resolve().parents[3]
D=W/'assets/sprites/sky_lagoon/animated_v1'
contract=(W/'scripts/arena/sky_lagoon_candidate_manifest.gd').read_text(encoding='utf8')
required=re.findall(r'^\t"([^"\n]+\.png)": Vector2i\((\d+), (\d+)\)',contract,re.M)
assert len(required)==16
rows=[]
for name,width,height in sorted(required):
 p=D/name;size=Image.open(p).size;assert size==(int(width),int(height)),name
 rows.append({'file':name,'size':list(size),'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(D/'manifest.json').write_text(json.dumps({'schema':1,'art_version':'animated_v1','assets':rows,'hash_scope':'authoring provenance; runtime validates schema, completeness, resource decoding and dimensions'},indent=2)+'\n')
print('SKYPACK|complete16-texture manifest matches runtime contract|PASS')
