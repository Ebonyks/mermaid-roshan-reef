import json, pathlib, shutil
v = pathlib.Path(__file__).parent
rows = []
for source in [v / 'generation_outputs_all.json', *sorted(v.glob('generation_outputs_round*.json'))]:
    rows.extend(json.loads(source.read_text(encoding='utf-8')))
for row in rows:
    shutil.copy2(row['native'], v / 'art' / (row['id'] + '.png'))
print(f'Copied {len(rows)} native candidates; originals retained.')
