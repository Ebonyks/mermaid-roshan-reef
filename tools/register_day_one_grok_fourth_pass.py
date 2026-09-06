"""Mechanical registration of generated V4 document and asset inventory."""
from pathlib import Path
import json
import re

ROOT=Path(__file__).resolve().parents[1]
REL=Path('assets_src/cinematics/day_one_grok_handoff_v4_2026-09-05')
PACKET=ROOT/REL


def replace_block(path, label, text):
	start=f'<!-- {label}_START -->';end=f'<!-- {label}_END -->'
	old=path.read_text(encoding='utf-8-sig')
	old=re.sub(re.escape(start)+r'.*?'+re.escape(end)+r'\s*','',old,flags=re.S).rstrip()
	path.write_text(old+'\n\n'+start+'\n'+text+'\n'+end+'\n',encoding='utf-8',newline='\n')


def main():
	docs=sorted(PACKET.rglob('*.md'))
	rows=['## V4 Day One replacement handoff - scoped candidate records\n','| Doc | | Note |','|---|---|---|']
	for path in docs:
		rel=path.relative_to(ROOT).as_posix()
		rows.append(f'| `{rel}` | 🟣 | `PROPOSED_CANONICAL`; scoped draft reshoot packet, human first-frame approval pending; no runtime or delivery authority. |')
	replace_block(ROOT/'design/05_DOC_LEDGER.md','DAY_ONE_GROK_V4_DOCS','\n'.join(rows))
	packet=json.loads((PACKET/'HANDOFF_PACKET.json').read_text(encoding='utf-8'))
	rows=[]
	for item in packet['assets']:
		if 'dimensions' not in item and Path(item['path']).suffix.lower() not in {'.mp4', '.mov', '.webm', '.ogv', '.ogg', '.wav', '.mp3'}:continue
		rows.append(f"- `{REL.as_posix()}/{item['path']}` — {item['role']}; source `{item['source_path']}`; {item['license_provenance']}; modifications: {item['modifications']}; SHA-256 `{item['sha256']}`. Reference/review only; no delivery approval.")
	replace_block(ROOT/'ASSET_LICENSES.md','DAY_ONE_GROK_V4_ASSETS','\n'.join(rows))
	print(f'Registered {len(docs)} Markdown documents and {len(rows)} visual/media assets.')


if __name__=='__main__':main()
