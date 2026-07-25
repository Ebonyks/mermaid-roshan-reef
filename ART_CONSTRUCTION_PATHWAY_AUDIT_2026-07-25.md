# Game-wide art construction-pathway audit — 2026-07-25

Scope: every art family in the game, scored against the construction pathway
the project settled on during the 2026-07-18…23 Codex passes. Machine-readable
companion: `audit/art_construction_pathway_2026-07-25.csv`.

Branch audited: `claude/game-art-audit-impl-j6p6ly`, taken from `origin/dev`
(`6de38d1`) plus the nine unmerged branches integrated in this pass (§4).

---

## 1. The pathway

The rule the project converged on — stated most explicitly in
`CLAUDE_EMBER_FORTRESS_BLENDER_HANDOFF_2026-07-22.md`, which **rejected a
finished 39-model kit for skipping stage 1** — is:

| Stage | Artifact | Evidence tier | Who |
|---|---|---|---|
| 1 | Approved **2D concept board / flat card**, prompts + ledger recorded | E1 (never scored for runtime quality) | Codex |
| 2 | **Editable authoring source** (`assets_src/blender/*.blend` or a deterministic `tools/build_*.py`) | — | Claude |
| 3 | **Runtime asset** exported to `assets/…` with parsed geometry metrics | E2 (max 2/5) | Claude |
| 4 | **Isolated QA render** per asset, plus a family contact sheet | E2 | Claude |
| 5 | **Runtime wiring** + a probe that fails when the asset is missing or wrong | E3 | Claude |
| 6 | **Forward-Mobile runtime capture** in the real scene | E4 (permits 4/5) | CI |
| 7 | **Owner acceptance** | 5/5 — only the owner may award it | Owner |

Two rules ride on top and are the ones most often broken:

- **A 2D board is not optional and cannot be added retroactively to bless a
  mesh.** That is the exact finding that killed the `codex/bowser-world-graphics`
  Ember kit.
- **Isolated renders are never runtime evidence.** Several families are
  currently sitting at E2 while their audits read as if they were done.

---

## 2. Where every family stands

Counts are live file counts, not doc claims.

| Family | 2D concepts | Runtime assets | Stage | Verdict |
|---|---|---|---|---|
| Pearl Castle — pearl_kit | 0 | 58 GLB | E4 | Shipped; predates the 2D gate |
| Pearl Castle — **Cleaning Day skins** | 100 | 96 PNG | **E3 (wired this pass)** | Was E1-orphaned; now live |
| Pearl Castle — natatorium 2D | 1 atlas | 1 atlas | E4 | Shipped |
| Sky Lagoon — quality kit | 17 | 61 GLB | E4 (4.5–4.8) | Complete |
| Sky Lagoon — PNW trees + shrubs | 24 | 24 GLB | E4 | Complete — 12 trees + 12 shrubs all landed |
| Northern Kingdom | 2 | 25 GLB | E4 (4.50–4.74) | Complete; refinement queue open |
| **Opera House — lobby + stage** | **185** | 18 GLB live + 15 built-unwired | **E2 for 1 of 11 families** | Architecture family modelled; wiring blocked on the OPERAGATE teardown cost |
| Opera House — 12 job packs | 612 | 53 GLB | E3/E4 partial | 10 of 12 jobs have prop kits |
| **Ember Fortress** | 51 | 79 GLB | **E3 enrichment + E4 core** | 40 enrichment cards now modelled; the 39 core remain off-pathway |
| Reef districts / ocean kingdoms | 5 | 7 GLB | E4 | Complete |
| CC0 replacement kit | 18 | 24 GLB | E3 | Wired, isolated renders only |
| Fairy pond / Butterfly World | 15 | 9 GLB | E4 | Complete, hard-gated in `ci.sh` |
| Dungeon art v2 | 0 | 12 GLB | E4 | Shipped; predates the gate |
| Kitchen / bathroom props | 0 | 66 GLB | E4 | Shipped; predates the gate |
| Art pass 3.5 library | 14 | 229 GLB | E4 | Shipped |
| Full-texture-regen candidate | 61 | 137 GLB | E2 | Deliberately unwired; failed review |
| **UI / HUD** | 10 | procedural | **E3 divergent** | Two rival implementations |
| Characters / NPCs | — | 11 GLB | E4 partial | Cutout fallbacks remain |
| Stuffie companions | — | protected | n/a | Generation forbidden by policy |

---

## 3. The four findings that matter

### 3.1 The Cleaning Day pack was finished art with no consumer — now wired

`codex/dirty-castle-2d` (2026-07-23, 332 files) delivered 96 runtime sprites,
41 of them **exact transparent renders of the shipped GLBs** with grime
alpha-composited on top (silhouette recall 1.0, changed-pixel ratio 2–5%), a
scene-resemblance ledger binding each skin to its GLB, and an explicit Godot
handoff. `manifest.json` carried `"runtime_integration": "not_wired"`, and
nothing in `scripts/` referenced the directory. The narrative chain behind it
(`STORY_DAYS.md` → `CLEANING_ASSET_REQUESTS_2026-07-22.md`) was also
design-only.

This pass implements it: `scripts/games/clean.gd` + `scripts/probe_clean.gd`.
See §5.

### 3.2 The Opera House lobby is the largest un-modelled pack in the project

`assets_src/concepts/opera_house_flat/` holds 13 sheets sliced into 172 cards,
all `accepted` in `audit/opera_house_flat_prototype_ledger_2026-07-21.csv`
across 11 families (architecture, front_of_house, lobby_furniture,
lobby_services, lobby_decor, upper_access, stage, floor1–3, crest).
`CLAUDE_OPERA_HOUSE_3D_CONTINUATION_2026-07-21.md` maps them onto five
existing builders in `scripts/opera_house.gd`.

Nothing has been modelled. `opera_house.gd` still dresses the lobby from the
18 art-3.5-era GLBs in `assets/art35/opera/`, and there is no
`assets_src/blender/opera_house*.blend`. `CODEX_ASSET_REQUESTS_2026-07-21.md`
is the owner's own full order for this replacement.

Rough size: ~172 cards → a realistic modular kit of 40–60 GLBs (many cards are
state variants of one mesh). This is a multi-session job and the single highest
-value remaining art task.

**Progress in this pass:** the 12-card architecture family is modelled
(`tools/build_opera_house_kit.py`, 15 GLBs — the portal and medallion cards
each carry two states, the carpet card two modules — plus 30 isolated QA
renders). That is stages 2–4 complete for one family of eleven.

**It is built but NOT wired, and the reason is worth recording.** Wiring 28
dressing props into `_build_lobby` turned `probe_l2`'s OPERAGATE return leg
red: `blocked/rearm/open/return` went `true/true/true/true` on run 681 to
`true/true/true/FALSE` on run 682, with the lobby dressing as the only opera
change between them. The leg builds and tears the whole lobby down inside a
single frame, and the extra GLB instancing lengthens that teardown enough that
one frame of level2 physics drags Roshan past the gate's 9-unit "placed aside"
radius. Per the CLAUDE.md refactor rule the addition was reverted rather than
the probe relaxed.

That is a real constraint on the whole Opera continuation, not a one-off: any
future lobby kit has to account for the cost of building and freeing itself
inside the OPERAGATE leg. The likely fixes, in order of preference, are to
build the lobby dressing lazily (or keep it resident across a leave/return
instead of rebuilding), or to give `_end_opera` a settle that survives a long
frame. Both are gameplay changes and need to be their own probed commit.

### 3.3 Ember Fortress: enrichment built, core provenance still open

`assets/ember_fortress/` originally held 39 GLBs (wired through
`DungeonArt.EMBER_PATHS`, `probe_ember` + `probe_ember_art` green, Mobile
captures on file) built by `codex/bowser-world-graphics` — the chain that
`CLAUDE_EMBER_FORTRESS_BLENDER_HANDOFF_2026-07-22.md` explicitly rejected
"because it skipped 2D design approval". The approved boards specify **79
exports Claude owns**: 39 core + 40 enrichment.

**The 40 enrichment exports are now built** (`tools/build_ember_expansion_kit.py`,
`assets_src/blender/ember_expansion_kit.blend`) straight from the approved
expansion cards, every row inside its manifest triangle budget, wired at each
row's `max_placements` through `_build_enrichment()` with the handoff's Speedy
sector cap of 28 visible instances, and gated by new checks in `probe_ember`.
That half of the pack is on-pathway end to end.

**The 39 core exports are untouched and still off-pathway.** Rebuilding them
is a governance call, not a visual emergency — what ships looks fine and is
probe-covered — so it stays an owner decision:

- **Option A (cheap):** grandfather the shipped 39, and treat the 2026-07-22
  core boards as the reference for future Ember work only.
- **Option B (expensive, as written):** rebuild all 39 from the boards, one
  focal family at a time in the mandated pilot order (planet/plazas, Great
  Gate/frame/veil, lantern assembly, home ring, arena/door, King, boss).

Nothing else in the project is blocked on this choice.

### 3.4 The UI prototypes have two rival implementations

`gen2/ui_prototypes_2026-07-19/` (10 mockups) produced:

- **On `dev`:** a partial "gold slice" — corner-owned HUD tray, picture
  objective card, resting joystick — drawn directly in `main.gd` / `touch_ui.gd`.
- **On `codex/menu-system` (unmerged, 3 commits, 21 files):** a fuller
  `scripts/storybook_ui.gd` with a shared panel/label style system, a storybook
  pause menu, a stuffie Tamagotchi care menu, and its own `probe_ui_system.gd`.

They rewrite the same lines. Merging is not mechanical, and the branch's
`ci.sh` edit also drops `probe_ocean_kingdoms` and `probe_ui`. **I did not
merge it** — picking a HUD direction is the owner's call. Once picked, the
loser's edits should be reverted rather than blended.

---

## 4. Integration performed in this pass

Nine branches carrying Codex art or its direct follow-ups were merged into the
work branch. What was in each, and what it needed:

| Branch | Content | Resolution |
|---|---|---|
| `codex/dirty-castle-2d` | 96 sprites + 4 handoff docs + ledgers | merged, then **implemented** (§5) |
| `claude/game-narrative-day-structure-v2k7w4` | `STORY_DAYS.md`, `CLEANING_ASSET_REQUESTS` | merged (docs only) |
| `claude/remove-cc0-assets-regen-sieh6e` | 24 authored CC0 replacements + `build_cc0_replacement_kit.py` | merged; 3 conflicts resolved |
| `codex/fairy-texture-continuity` | continuous pond textures + audit gate | merged clean |
| `codex/roshan-pool-pnw` | natatorium + PNW marsh art | merged clean |
| `claude/opera-house-stage-kp3oq3` | marquee return-gate fix | merged; conflict resolved |
| `claude/todo-implementation-i4hkmh` | socket-bone parenting in the cosmetics baker | merged clean |
| `codex/menu-system` | storybook UI | **not merged** — see §3.4 |

Conflict resolutions worth recording:

- `scripts/kart.gd` — took the new `assets/props/gen2/crystal*` paths, kept
  dev's decision that `soft_barrier.glb` stays unplaced (owner 2026-07-18).
  Dropped the branch's re-introduced `KART_BARRIER_GLB` constant.
- `scripts/probe_opera.gd` — kept dev's bone-attached-costume/puppet checks,
  adopted the branch's node budget raise to `<210` for the dressing-card art.
  `origin/dev`'s tip was red on exactly this; the fix rides in.
- `ASSET_LICENSES.md` — both sides' new rows kept.

---

## 5. Cleaning Day implementation (this pass)

`scripts/games/clean.gd` — `CastleCleanup`, a Phase-7 satellite that receives
`main` by reference and keeps all state on `main`.

- **30 room-bound object skins** across the six rooms the handoff names, laid
  over fixtures `CastleHall` already builds. No room geometry, collider,
  OmniLight or gameplay node is created or moved. Bindings follow the
  scene-resemblance ledger rather than filenames — the handoff warns that
  several filenames predate the strict audit (the Library "cart" slot is bound
  to the live library table, the Playroom "tea set" to the live shell drum, the
  "wheeled toy" to the live sailboat).
- **Render contract as specified:** unshaded `Sprite3D`, billboard for props,
  laid-flat quads for floor/counter marks, non-billboard overlays for skins that
  include their own fixture, linear filter, depth testing on, never relit or
  colour-graded.
- **Interaction:** swim within 6 units, then a tap **or** a stick rub; three
  strokes dissolve a skin. No timer, no fail state, no wrong tool. Every
  accepted input answers with bubbles/dust, a dust bunny hops aside (never
  squashed), and `fx_clean_ring` plus the room's tool card mark the target so a
  non-reader always sees the goal. Room intro is voiced and shown as the room
  vignette, which dissolves before individual targets are worked.
- **Progress** is the pack's pearl cards, never numerals.
- **Save:** new `clean_done` dictionary, written the instant *one object*
  finishes. Added with a default and deliberately kept out of
  `KNOWN_KEYS`/`CORE_KEYS`, the Ember/critter precedent, so older saves still
  read as schema-complete. A cleaned object never re-dirties.

`scripts/probe_clean.gd` covers pack resolution and the 512px render contract,
absence of lights/bodies in the layer, a tap target, a rub target, room
completion, per-object save, reload restoring the exact set, and the agency
rule — three seconds of zero input standing on a target cleans nothing.

What is deliberately **not** in this pass: the Week-of-Light day gating
(`STORY_DAYS.md` W1–W3), the soot sprites and gremlin chase, and the
Crown-Light hand-off to the lantern ring. Those are narrative plumbing that
touches the whole map; the art layer stands alone and additive without them.

---

## 6. Recommended order of remaining work

1. **Owner decision — UI direction** (§3.4). Cheapest, unblocks a merged branch.
2. **Owner decision — Ember core provenance** (§3.3). The 40 enrichment
   exports are done; only the 39 core exports are still in question.
3. **Opera House lobby kit** (§3.2). Largest real modelling job; the flat cards,
   the ledger, the code map and the owner's asset order all already exist. The
   architecture family is built — the next step is the lobby lifetime change
   that lets dressing be wired without lengthening the OPERAGATE teardown
   frame, as its own probed commit.
4. **CC0 kit finish:** re-render the 24 replacements with a real Eevee pass,
   verify the kart `yaw_fix` values in a Mobile capture, generate the remaining
   15 queued items, then take the Group-0 deletion of 63 dead files to the owner.
5. **Northern refinement queue** — the 9 families under 4.55 in
   `NORTHERN_BLENDER_HANDOFF_FOR_CLAUDE_2026-07-20.md`.
6. **Opera job packs** — farmer and racer have outfits only.
7. **Retro-document** the four pre-gate families (pearl_kit, dungeon v2, kitchen
   and bathroom props, art35). They are good, shipped and probe-covered; they
   only lack a stage-1 board. Record them as grandfathered so a future audit
   does not read them as gaps and rebuild them.

## 7. Housekeeping notes

- 137 full-texture-regen models and 63 art-3.5 cards/dressing GLBs have no live
  call site. Both are inventory, not bugs — the regen pack is a recorded failed
  candidate, the art35 cards are source stock. Neither should be wired.
- No Godot or Blender binary exists in the remote dev container. Blender 4.4 is
  reachable as the pip `bpy` module (verified this session, GLB export works),
  which is how any of the modelling work above can be done here; Godot probes
  continue to run only in CI.

## 8. Provenance

Counts were taken by walking the tree, not from prior audits. Stage
classification uses the evidence tiers defined in
`assets/ART_GENERATION_CONTRACT.md` and the Ember handoff. No score in this
document is self-awarded above 4/5; owner acceptance remains a separate gate.
