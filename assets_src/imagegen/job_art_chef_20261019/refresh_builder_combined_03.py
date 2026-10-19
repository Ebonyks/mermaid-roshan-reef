"""Materialize only strict-gate mismatches, preserving unrelated delivery bytes."""
from pathlib import Path
import contextlib,hashlib,importlib.util,io,json,sys
root=Path(__file__).resolve().parents[3]
spec=importlib.util.spec_from_file_location('chef_art_builder',root/'tools/prepare_opera_minigame_art.py')
gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
original=gate._check_bytes_match
mismatches={}
def capture(path,actual,expected):
    matched=original(path,actual,expected)
    if not matched:
        mismatches[path]=expected
    return matched
gate._check_bytes_match=capture
sys.argv=['prepare_opera_minigame_art.py','--check-only']
output=io.StringIO()
with contextlib.redirect_stdout(output):
    result=gate.main()
src=Path(__file__).resolve().parent
(src/'builder_combined_03_initial_strict_check.log').write_text(output.getvalue())
allowed={gate.SOURCE_DIR/name for name in ['OPERA_MINIGAME_ART_CONTACT_SHEET_2026-08-09.png','PROVENANCE.json','REVIEW.md']}
assert result==1 and set(mismatches)==allowed,(result,list(mismatches))
records=[]
for path,data in mismatches.items():
    records.append({'path':path.relative_to(root).as_posix(),
        'before_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
        'after_sha256':hashlib.sha256(data).hexdigest(),
        'method':'Exact expected bytes captured from unchanged strict comparator; no unrelated rebuild/recompression'})
    path.write_bytes(data)
(src/'builder_combined_03_refresh.json').write_text(json.dumps({'strict_initial_exit':result,'records':records},indent=2)+'\n')
print('Updated',len(records),'dependent review artifacts only; runtime replacement already matched')
