"""Refresh current navigation, delivery notes, licenses and exact change coverage."""
from pathlib import Path
import json,re,subprocess
from build_revision import V,L,R,C,OLD,BASE,PDF_NAME,EMAIL_NAME,read,save,sha

def write(p,s):p.write_text(s,encoding='utf8',newline='\n')
def main():
    b=read(V/'BOOK_CURRENT.json');scope=read(V/'revision_scope.json')
    v=read(C/'verification.json') if (C/'verification.json').exists() else {'status':'PENDING','contrast_baseline':{},'contrast_v45':{}}
    critique='[Editorial critique](EDITORIAL_CRITIQUE.md)'
    report=[]
    for q in scope['changes']:
        a=q['before_caption'];z=q['after_caption'];keys=[k for k in z if z.get(k)!=a.get(k)]
        detail=', '.join(f'{k}={z[k]}' for k in keys) or 'Original box; whitespace reflow only'
        if q['page']==11:detail+='; declared concise editorial adaptation; see EDITORIAL_ADAPTATIONS.json'
        if q['page']==21:detail+='; bubbles: Sorry! / We’ll be gentle!; single-top-caption fallback'
        report.append(f"| {q['page']} | DONE | {detail} |")
    size=(C/PDF_NAME).stat().st_size
    write(V/'README.md',f'''# Mermaid Roshan and the Dust Bunnies: V45

Status: `SUPPORTING_CURRENT`. **Story-language review draft implemented; creative acceptance remains open.**

[Read the book](complete/READ_BOOK.html) · [Reading PDF](complete/{PDF_NAME}) · [Email PDF](complete/{EMAIL_NAME}) · {critique} · [Exact checks](complete/verification.json) · [Manifest](manifest.json).

The linked V45 proposal is implemented as a review draft with all25 changed captions and page21 dialogue. Roshan starts with an overwhelming mess, helps friends in small steps, asks for help herself, and welcomes Grand Puff after they care for him together. **24changed captions match the source manuscript exactly; page11 is deliberately shortened to fit below the action.** It reads: “Rumi was stuck under the gunk. / ‘Can you help me?’ she called.” [Exact editorial adaptation](EDITORIAL_ADAPTATIONS.json) · [Applied manuscript](APPLIED_MANUSCRIPT.json) · [Preserved source proposal](MANUSCRIPT.json). Other changes are whitespace, caption placement and local text styling. No new art or generation.

The critique supports the stronger arc while retaining concerns about density, illness/blame, treating a happy chirp as proof of forgiveness, and the late magical door rule. These are documented editorial observations, not silent changes to the manuscript.

The seven unchanged story pages and both covers retain their complete PDF content, rendered pixels and controls. All34 caption-free PDF pages, encoded images and alpha streams are compared with V44. The doublewide arrival, artwork, patches, order, Sniglet,20logicalpt body and18logicalpt bubble text remain. This is a mixed-width reading review, not a lossless print master.

## Changed pages

| Story page | Result | Caption placement/style |
|---|---|---|
'''+ '\n'.join(report)+f'''

Page11 retains its two-line lower caption area, with the original concise introduction and the proposed request for help; no character is covered to force the longer introduction into place. Page9 is left-aligned to clear Roshan's crown. Page21 keeps the allowed original one-caption fallback; the proposed interleaved caption/bubble reading order is not implemented. No page is held and no type is reduced. Page11's deliberate wording adaptation remains for owner review.

## Verification and acceptance

Current machine verdict: `{v['status']}`. Actual V44 composed-caption counts: `{json.dumps(v['contrast_baseline'])}`. V45: `{json.dumps(v['contrast_v45'])}`. Same V37/V42 thresholds and composed-art sampling; no stroke is included in the contrast measurement. Every required outline is checked. [Contrast details](composed_caption_contrast.json), [source/input seal](input_verification.json), [scope](revision_scope.json), [validation](validation_results.json) and [visual inspection](visual_review.json) preserve evidence separately.

The reading and email PDFs intentionally contain identical bytes, both {size:,}bytes (under25,000,000); all original image streams are retained. The output is a reading copy, with V44's inherited image compression and print limitations unchanged.

All32 captions and dialogue were reviewed silently in sequence for cadence. **An actual oral read-through was not performed.** The critique lists phrases to listen for. Owner review of new story facts, read-aloud with Roshan, qualified speech-language review, test print, V41 printPart2 and arrival imposition/parity/gutter remain open. BK44-O01 geography and BK44-O02 fountain forehead remain open; no illustrations or game behavior were repaired or accepted.

## Publication and rollback

Destination: `Ebonyks/mermaid-roshan-reef`, established `codex/mermaid-roshan-picture-book` branch, this versioned directory. [Anonymous exact-commit byte receipt](remote_verification.json) records manifest SHA256, commit, check time, access mode and every payload file. Publication is separate from owner/child/SLP/print acceptance. No dev/master integration or game release is part of this book revision.

Baseline: `550a0b86216dee020d5070428ab4ddcfe0da4dc1`; V44 source control at `49a199846c61a39a3735e162214706b3687f12d3`. V44 artifacts and the linked work-order inputs remain untouched. Restore BOOK_BASELINE.json to ../../book.json and use the preserved V44 PDF to roll back the book controls.

The grown-up question card lives on another branch and still needs its quoted caption anchors updated. No cross-branch edit or message was sent.
''')
    write(R/'books/chapter_one/README.md',f'''# Mermaid Roshan and the Dust Bunnies

Status: `SUPPORTING_CURRENT`; [V45 story and language review](landscape/revisions/v45_story_language/README.md).

[Read](landscape/revisions/v45_story_language/complete/READ_BOOK.html) · [Reading PDF](landscape/revisions/v45_story_language/complete/{PDF_NAME}) · [Email PDF](landscape/revisions/v45_story_language/complete/{EMAIL_NAME}) · [Critique](landscape/revisions/v45_story_language/EDITORIAL_CRITIQUE.md) · [Design language](DESIGN_LANGUAGE.md).

V45 implements the proposed empathy/friendship arc: everyone needs help sometimes, and friends can do big jobs together. All25 caption changes and page21 bubbles are implemented;24captions match the proposal exactly and page11 is deliberately shortened to preserve the clear action and fixed type size. Art, covers, type sizes,32story entries and the doublewide arrival remain. Existing V44 doorway repair is retained.

The34-entry mixed-width reading review is not a print edition. Actual oral/child reading, qualifiedSLP, owner/new-story-fact acceptance, BK44-O01/O02 art continuity, arrival binding/gutter and V41 printPart2 remain open. Prior versions and originals are preserved; no game/release change.
''')
    oldplan=subprocess.check_output(['git','show',BASE+':books/chapter_one/landscape/PAGE_PLAN.md'],cwd=R).decode('utf8')
    sources={int(a):int(z) for a,z in re.findall(r'^\| (\d+) \| (\d+) \|',oldplan,re.M)}
    rows=[f"| {p['page']} | {sources[p['page']]} | "+p['text'].replace('\n',' / ')+' |' for p in b['pages']]
    write(L/'PAGE_PLAN.md','''# V45 page plan: story and language

Status: `SUPPORTING_CURRENT`. Proposed words with whitespace reflow; page11 has a declared concise editorial adaptation. [Controls](book.json) · [V45 critique and page report](revisions/v45_story_language/README.md).

| Story | V34 source story | Caption |
|---|---|---|
'''+ '\n'.join(rows)+'''

Page21 bubbles: "Sorry!" / "We’ll be gentle!". Existing one-caption reading-order fallback remains.

All art placements, covers and page order remain V44-exact. Story2 remains one28x10in PDF entry; other entries14x10in. Splitting arrival adds an interior unit, so physical pagination, reveal parity, swing/gutter and printPart2 remain held. No final print imposition is claimed.
''')
    write(L/'REVIEW.md','''# V45 story and language review

Status: `SUPPORTING_CURRENT`. [Read and changed-page report](revisions/v45_story_language/README.md) · [Editorial critique](revisions/v45_story_language/EDITORIAL_CRITIQUE.md) · [Machine checks](revisions/v45_story_language/complete/verification.json) · [Visual inspection](revisions/v45_story_language/visual_review.json).

The new text gives Roshan a relatable starting problem, links small jobs to a larger cooperative task, motivates friends returning, and pairs empathy with a promise of gentle play. Exact proposed words are retained on24changed pages and in page21 dialogue; page11 deliberately keeps a concise introduction and the proposed request for help. The longer proposal is preserved separately. The critique identifies density, apology/illness, forgiveness and magic-rule concerns, and explains the one editorial adaptation.

All34 art pages and nine unchanged complete entries are compared with V44. The original cover doorway repair, title, source art, patches, doublewide arrival and type sizes stay. Caption boxes/styles change only to fit and improve readability; no opaque text strips or new art are added.

This is a primary AI editorial and visual review, not an independent second-AI, owner, child, qualifiedSLP or print acceptance. Actual oral reading remains outstanding. The inherited geography and fountain forehead findings BK44-O01/O02 remain open. Physical arrival mapping/parity/gutter and V41 printP1–P8 stay held.
''')
    write(L/'STORY_COMPREHENSION_AUDIT.md','''# V45 story comprehension

Status: `SUPPORTING_CURRENT`; editorial evidence separate from child, owner and qualifiedSLP acceptance.

The proposed through-line is now explicit: everyone needs help sometimes, and friends can do big jobs together. Roshan's question on4 and Daddy's small-job advice on6 lead to her choice on8, the refrain on22, her request on25 and the helpers' answer on26. Pages30–32 state the two parts of the moral and show everyone resting together.

The stuck door and promise on5 connect to23. The bath bunny needs somewhere to play; the two playroom bunnies must become gentle; Grand Puff is unwell and receives help before apologizing. The page21 chirp demonstrates relief, not independently proven forgiveness. Care and belonging are not conditional on illness, appearance or a forced apology.

The waterfall clears and turns rainbow, two bunnies trap Baby Eagle, and concealment, rainbow jump, dust fall and landing retain their exact visual order. V45 invents no art. New statements about Grand Puff, his sneezes, Rumi's offer and sparkle-door magic remain draft facts for owner reading; they do not change game rules.

Child-reading questions: Why does Roshan promise to return? What changes after the bunnies say sorry? When does Roshan ask for help? Is Grand Puff welcome before he changes color? These are future observations, not measured comprehension results.

[Full critique and cadence trip points](revisions/v45_story_language/EDITORIAL_CRITIQUE.md). All32captions/dialogue were silently reviewed; actual oral read-aloud, child/SLP/owner review, inherited geography/fountain continuity, print, arrival imposition/parity/gutter and V41 printPart2 remain outstanding.
''')
    # Update status/navigation facts, preserving the original published work order.
    p=R/'books/chapter_one/DESIGN_LANGUAGE.md';s=p.read_text('utf8')
    marker='\nV45 implementation status (2026-10-31):'
    s=s.split(marker)[0].rstrip()+marker+' [V45 review draft](landscape/revisions/v45_story_language/README.md) implements24exact proposed captions and the page21 bubbles, with a declared concise page11 editorial adaptation for fit/readability. No new art. New story facts and the adaptation remain for owner reading; original rules and all acceptance holds above remain.\n'
    write(p,s)
    p=R/'audit/MASTER_AUDIT_2026-08-09.md';s=p.read_text('utf8')
    line='Scoped V45 static-book language review: [draft and critique](../books/chapter_one/landscape/revisions/v45_story_language/README.md), [impact](../design/audit_impacts/picture-book-v45-language-20261031.json).24exact proposed captions plus a declared concise page11 adaptation; unchanged art and game. Owner/child/SLP/print and inherited continuity remain open.\n\n'
    if line not in s:s=s.replace('<!-- AUDIT_TASK_INDEX_END -->',line+'<!-- AUDIT_TASK_INDEX_END -->')
    write(p,s)
    p=R/'design/05_DOC_LEDGER.md';s=p.read_text('utf8');lines=s.splitlines()
    for i,line in enumerate(lines):
        if line.startswith('| `books/chapter_one/README.md`'):lines[i]='| `books/chapter_one/README.md` | 🔵 | `SUPPORTING_CURRENT`; V45 story language with one declared concise page11 editorial adaptation and unchanged V44 art; owner/new-story-fact, child/SLP/print and inherited continuity acceptance remain open. |'
        if line.startswith('| `books/chapter_one/landscape/PAGE_PLAN.md`'):lines[i]='| `books/chapter_one/landscape/PAGE_PLAN.md` | 🔵 | `SUPPORTING_CURRENT`; V45 delivered32caption/source map; one page11 editorial adaptation; physical arrival imposition held. |'
        if line.startswith('| `books/chapter_one/landscape/REVIEW.md`'):lines[i]='| `books/chapter_one/landscape/REVIEW.md` | 🔵 | `SUPPORTING_CURRENT`; V45 primary editorial/layout review, declared page11 adaptation and unchanged art; no child/owner/SLP/print acceptance. |'
        if line.startswith('| `books/chapter_one/landscape/STORY_COMPREHENSION_AUDIT.md`'):lines[i]='| `books/chapter_one/landscape/STORY_COMPREHENSION_AUDIT.md` | 🔵 | `SUPPORTING_CURRENT`; V45 proposed empathy/friendship arc and comprehension questions; unmeasured child/SLP/owner outcomes remain open. |'
        if line.startswith('| `books/chapter_one/landscape/revisions/v44_door_and_consistency/README.md`'):lines[i]='| `books/chapter_one/landscape/revisions/v44_door_and_consistency/README.md` | ⚪ | `HISTORICAL_EVIDENCE`; sealed V44 cover repair and34-entry audit preserved. V45 supersedes story-language review; V44 art and BK44-O01/O02 findings remain applicable. |'
        if line.startswith('| `books/chapter_one/handoffs/2026-10-31_v45_story_language/README.md`'):lines[i]='| `books/chapter_one/handoffs/2026-10-31_v45_story_language/README.md` | 🔵 | `SUPPORTING_CURRENT`; preserved V45 source work order, now implemented as a review draft. Original new-story-fact/owner, child/SLP and print acceptance remains open. |'
    s='\n'.join(lines)+'\n'
    for name,note in [('README.md','Current V45 text/layout delivery, one declared editorial adaptation and acceptance holds.'),('EDITORIAL_CRITIQUE.md','Primary critique of the source proposal and silent cadence review; no oral/child/SLP acceptance.')]:
        path=(V/name).relative_to(R).as_posix()
        if f'| `{path}`' not in s:s+=f'| `{path}` | 🔵 | `SUPPORTING_CURRENT`; {note} |\n'
    write(p,s)
    # Every new rendered media file receives an individual derivative license row.
    p=R/'ASSET_LICENSES.md';s=p.read_text('utf8');start='<!-- V45_READING_EXPORTS_START -->';end='<!-- V45_READING_EXPORTS_END -->'
    if start in s:s=s[:s.index(start)]+s[s.index(end)+len(end):]
    media=sorted(q for q in C.iterdir() if q.suffix.lower() in ['.png','.jpg','.pdf'])
    license_rows=[f'| `{q.relative_to(R).as_posix()}` | Derived book review export from owner project V44 PDF; inherited per-source licenses unchanged | Existing-source reading/layout derivative; no new artwork | https://github.com/Ebonyks/mermaid-roshan-reef/tree/{BASE}/books/chapter_one/landscape/revisions/v44_door_and_consistency | Vector text replacement / PDF page proof or diagnostic contact sheet; original sources untouched; SHA256 {sha(q)} |' for q in media]
    write(p,s.rstrip()+'\n\n'+start+'\n\n| File | Source | License | URL | Modifications |\n|---|---|---|---|---|\n'+'\n'.join(license_rows)+'\n\n'+end+'\n')
    impact=R/'design/audit_impacts/picture-book-v45-language-20261031.json';d=read(impact)
    tracked=subprocess.check_output(['git','diff','--name-only',BASE],cwd=R).decode().splitlines()
    added=subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=R).decode().splitlines()
    d['files']=sorted(set(tracked+added)-{impact.relative_to(R).as_posix()})
    save(impact,d)
    print('Updated navigation, exact25-page report,',len(media),'media license rows and',len(d['files']),'covered files')
if __name__=='__main__':main()
