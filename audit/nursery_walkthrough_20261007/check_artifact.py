from pathlib import Path
import json,hashlib,re,base64,sys,xml.etree.ElementTree as ET
from html.parser import HTMLParser
from urllib.parse import unquote,urlsplit
A=Path(__file__).resolve().parent;R=A.parents[1]
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
snapshot_only='--snapshot-only' in sys.argv
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=set()
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if 'id' in d:self.ids.add(d['id'])
  for k in ['src','href']:
   if k in d:self.links.append(d[k])
l=Links();l.feed((A/'index.html').read_text());checked=0
for x in l.links:
 if urlsplit(x).scheme:continue
 p,_,frag=x.partition('#')
 if p:assert (A/unquote(p)).is_file(),x
 else:assert frag in l.ids,x
 checked+=1
steps=json.loads((A/'STEPS.json').read_text());assert [s['number'] for s in steps]==list(range(1,25))
assert sum(s['evidence_class']=='HISTORICAL_NATIVE_FIXTURE' for s in steps)==8
assert sum(s['evidence_class']=='COVERAGE_GAP' for s in steps)==16
media=json.loads((A/'MEDIA_PROVENANCE.json').read_text())['originals']
for m in media:
 assert H(A/m['path'])==m['sha256'],m['path']
 if not snapshot_only:assert H(R/m['source_path'])==m['sha256'],m['path']
for s in steps:
 root=ET.parse(A/s['panel']).getroot();imgs=root.findall('{http://www.w3.org/2000/svg}image')
 expected=['originals/captures/'+s['shot']+'.png'] if s['shot'] else ['originals/assets/'+k+'.png' for k in s['assets']]
 assert len(imgs)==len(expected)
 for im,p in zip(imgs,expected):assert hashlib.sha256(base64.b64decode(im.attrib['href'].split(',',1)[1])).hexdigest()==H(A/p)
 assert s['evidence_class'] in (A/s['panel']).read_text()
for x in json.loads((A/'SOURCE_BINDINGS.json').read_text())['runtime']:
 if not snapshot_only:assert H(R/x['path'])==x['sha256']
for label,path in re.findall(r'\[([^\]]+)\]\(([^)]+)\)',(A/'README.md').read_text()):
 if not urlsplit(path).scheme:assert (A/path).resolve().is_file(),path
result=dict(status='PASS',steps=24,native_fixture_panels=8,coverage_gap_panels=16,html_links_checked=checked,originals_sha256_verified=len(media),svg_embedded_pngs_verified=True,source_snapshot_availability="LOCAL_ONLY_OMITTED_FROM_PUBLIC",live_original_comparison=not snapshot_only,no_native_capture_or_generation=True,limits='Artifact verification only; current natural gameplay and independent4.6/device/child/owner acceptance remain open.')
(A/'ARTIFACT_CHECK.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
