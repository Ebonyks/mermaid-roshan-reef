# Grok asset workgroup

This directory is the context-light asset exchange for the Mermaid Roshan Grok Project. It prevents Grok from having to crawl the game repository, infer which files are canonical, or orchestrate dozens of downloads.

## Download packs

1. [`01_CHARACTER_LIBRARY.zip`](downloads/01_CHARACTER_LIBRARY.zip) — all current tracked character identities and motion authorities: Roshan, Daddy Mermaid, Huluu, Rumi, Boss Dust Bunny, Rainbow Dust Bunny, Ember King, and Ember Prince.
2. [`02_SKY_LAGOON_LOCATION.zip`](downloads/02_SKY_LAGOON_LOCATION.zip) — accepted Sky Lagoon geography, exact four-tower castle, full panorama, airplane, and current style bible.
3. [`03_PNW_FULL_2D_PACK.zip`](downloads/03_PNW_FULL_2D_PACK.zip) — complete accepted 2D PNW visual pack: 12 trees, 12 shrub variants, two master sheets, four plant-motion atlases, five fauna families in full-resolution and runtime motion sets, contact sheet, prompts, manifests, and audit notes.
4. [`04_OPENING_SEQUENCE_MODULE.zip`](downloads/04_OPENING_SEQUENCE_MODULE.zip) — the opening-flight storyboard, 15-second plan, prompt set, continuity ledger, review gates, and airplane reference. It deliberately reuses packs 01 and 02 rather than duplicating them.
5. [`05_OPENING_V2_REBUILD.zip`](downloads/05_OPENING_V2_REBUILD.zip) — complete audit of the 46.5-second Grok trial, visual evidence sheets, twenty-segment defect ledger, and the fifteen-shot fresh-generation replacement script.

Exact hashes are in `DOWNLOADS_SHA256.txt`. Every file inside the PNW archive is inventoried in `PNW_PACK_MANIFEST.csv`.

## Direct visual previews

Grok should inspect these three lightweight authorities before requesting individual PNW assets:

- [`PNW_TREE_MASTER_SHEET.png`](previews/PNW_TREE_MASTER_SHEET.png)
- [`PNW_SHRUB_MASTER_SHEET.png`](previews/PNW_SHRUB_MASTER_SHEET.png)
- [`PNW_FAUNA_CONTACT_SHEET.png`](previews/PNW_FAUNA_CONTACT_SHEET.png)

The preview sheets communicate family design and palette. For a production shot, attach the specific individual character, plant, animal, location, or prior-frame image required by that shot.

## Scope of “full PNW pack”

The PNW archive contains all accepted 2D visual authorities useful to Grok: the complete 24-card flora family, accepted masters, current and historical approved sway atlases, and all five accepted fauna families. Raw green-screen/chroma generations and deprecated GLB/3D implementations are intentionally excluded because they are production intermediates or superseded media, not additional visual canon.

## Context-budget rule

Do not paste the contents of every pack into one Grok conversation. Give Grok `GROK_ASSET_BOOTSTRAP.md`, let it inspect the three PNW previews and workgroup manifest, then attach only two to four controlling images to each Imagine generation.
