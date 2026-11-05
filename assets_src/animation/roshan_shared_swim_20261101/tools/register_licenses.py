"""Append exact source/derived asset paths; preserve the existing ledger bytes."""
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parents[2]


def main():
    ledger=REPO/'ASSET_LICENSES.md';raw=ledger.read_bytes()
    marker=b'## Shared native Roshan two-skin prototype (2026-11-01)'
    assert marker not in raw,'License block already exists; review additions explicitly rather than duplicate it'
    names=subprocess.check_output(['git','ls-files','--others','--exclude-standard',str(ROOT.relative_to(REPO))],cwd=REPO,text=True,encoding='utf-8').splitlines()
    suffixes={'.png','.mp4','.mkv','.aseprite','.zip','.f32'}
    rows=[]
    for name in sorted(names):
        if Path(name).suffix not in suffixes:continue
        relative=name.removeprefix(ROOT.relative_to(REPO).as_posix()+'/')
        if relative.startswith('references/'):
            source='Exact non-destructive copy of the existing project identity/Fashion Designer master; original rights and acceptance scope retained. See references/source_manifest.json.'
        elif relative.startswith('art_source/'):
            source='Owner-authorized built-in OpenAI ImageGen source candidate from existing project identity/costume designs; prompts/input bindings and reported call metadata retained. No art/performance acceptance granted.'
        elif '/review/' in '/'+relative or relative.startswith('review/'):
            source='Labelled QA composite/contact sheet of native Godot output; original character pixels retained in lossless archives. Grid/labels are instrumentation, never generator appearance or runtime background pixels.'
        elif Path(name).suffix=='.f32':
            source='Project-generated numeric signed-distance/nearest-interior-source-coordinate analysis of the authored fin alpha; shader data, not newly painted art.'
        elif Path(name).suffix=='.zip':
            source='Lossless RGBA XOR diagnostic archive of native output against its named/hash-pinned paired-track base; every reconstructed frame verified exact. Rejected technical evidence only.'
        elif Path(name).suffix in {'.mkv','.mp4'}:
            source='Native Godot source-prototype capture derived from the same shared rig and licensed source candidates; lossless native RGB/alpha archive or labelled review export as named. History remains rejected evidence.'
        else:
            source='Native Aseprite isolation/registration or exact retained source-prototype snapshot from the four named ImageGen source gaps. Original sheets preserved; no per-costume anatomy or character builder. See task provenance and exact isolation receipt.'
        rows.append(f'| `{name}` | {source} | Project asset/derivative rights retained; tool outputs under applicable OpenAI terms; no third-party art relicensing. | [Source provenance](assets_src/animation/roshan_shared_swim_20261101/README.txt) | Source-only candidate/review; originals unchanged. |')
    block='\n\n'+marker.decode()+'\n\nEvery path below is source-only or review evidence; it is not production/owner acceptance. Generated model revision/seed/monetary usage were not exposed. Four built-in calls, no paid API jobs. Existing protected originals are unchanged.\n\n| Asset | Source / modifications | Rights | Provenance | Scope |\n|---|---|---|---|---|\n'+'\n'.join(rows)+'\n'
    with ledger.open('ab') as out:out.write(block.encode('utf-8'))
    print('EXACT_NEW_ASSET_LICENSE_ROWS',len(rows),flush=True)


if __name__=='__main__':main()
