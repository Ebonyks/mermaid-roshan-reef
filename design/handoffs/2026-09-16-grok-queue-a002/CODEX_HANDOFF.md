# Codex handoff — Grok queue A002 (2026-09-16 night)

Historical producer report, preserved for provenance. The attic/rainbow missing
asset claims and monitor status below are superseded; do not act on them now.
Use [repaired V2](../../cinematics/v2/README.md) for current requests and references.

**DELIVERY_ACCEPTED: false**
**GENERATION_READY: false**
**FULL AUDIT: NOT PASSED.** Do not copy into `assets_src/`.

Private media: https://github.com/Ebonyks/mermaid-roshan-grok-videos
Release: https://github.com/Ebonyks/mermaid-roshan-grok-videos/releases/tag/grok-queue-a002-2026-09-16
Commit: `cdee5f84ef880c67f3f06328d7f737272b8b08bb`

This is attempt **A002** after owner notes: dirty rooms, Sky Lagoon crop, character refresh, dynamic camera, overnight branch watch.

## Owner notes addressed

| Note | Finding |
|---|---|
| A001 used clean rooms | Confirmed. Location plates `current_*_full_room` are the restored flats. |
| Use dirty versions | Dirty bathroom plate **was already in the builder packet** and unused: `REF-90bcc501e471b8d8` `room_bubble_bath_dirty_day_one.png`. A002 bath shots bind that plate. |
| Sky Lagoon missing / unused | Panorama master **exists** (`REF-017532ae864e534d`, 6144×2048 3×1). A001 squeezed it. A002 uses a 16:9 landing-patch crop (full-height window, not the underwater strip). **No dedicated landing-patch still is registered as IMAGE_1.** Game repo has `assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v5_tile_*.png`; the packet marks career tiles as comparison-only, not IMAGE_1. |
| Character continuity | Identity restated per scene. A001 invented extra mermaids and a unicorn-horn tiara. A002 stills from the dirty bathroom plate hold **one Roshan**. I2V **reintroduces extra cast** on arrival and pool. |
| Dynamic camera | A002 uses one move per shot (push-in / closer insert / downward settle). A001 was locked-wide on every card. |

## Sourced dirty plates

**In the builder packet (now bound):**
- Dirty bathroom full room: `media/90bcc501e471b8d8.png`
- Sink / tub grime overlays: `fe53ef3018b9f816`, `52e8c42b0c044c1b`
- Pool algae trash: `e0ed3c7174dcfeff`
- Clogged waterfall: `df7c3147bc886761`
- Sick seahorse: `3af5ff973576d328` (this is the seahorse identity, sick state)
- Craft grime strips only: left / desk / right (`125978f082`, `586021e282`, `339f248e48`)

**In the GAME repo, not imported into the builder packet:**
- `assets/flats/castle/rooms/room_bubble_bath_dirty_drained_day_one.png`
- `assets/flats/sky_lagoon/main/` tile grid (v4/v5)
- `assets/castle/day_one_pool/pool_rim_grime.png`
- `assets/castle/dirty_cleanup_2d/targets/*`

## Unable to source (flag for Codex)

| Needed | Status |
|---|---|
| Dirty **full** Mermaid Pool room plate | Missing. Only object overlays + runtime `00_dirty_arrival.png` which is marked **never generation pixels**. |
| Dirty **full** Craft Room plate | Missing. Only three grime strips. |
| Dirty **full** Main Hall plate | **Not found** in packet or a named dirty hall flat. |
| Dedicated Sky Lagoon **landing-patch** still approved as IMAGE_1 | Missing. Only the 3×1 panorama master plus career tiles (not IMAGE_1). |
| Stone attic **interior** plate | Packet attic ref is the dusty arena still; reads as castle exterior more than the two-window interior the cards describe. |
| Rainbow friend non-contact-sheet identity | Contact sheet must not be bound. |

Until those exist, pool/hall/craft/attic openings will keep drifting to clean restored rooms or invented architecture.

## A002 motion (6 clips) — sampled QC

All 6s, one camera move, dirty opening attempted. **Not accepted.**

| Shot | Still extra-cast | Motion extra-cast | Dirty opening | Camera | Verdict |
|---|---|---|---|---|---|
| ARRIVAL-TOUCHDOWN | Cleaned (delete pass) | **FAIL** — extra mermaid returns mid-clip | Landing crop used (not squeezed 3×1) | Downward settle | REGEN |
| BATH-SINK | PASS (solo Roshan) | **PASS sampled** — solo Roshan at t3, sink still dirty, local scrub | Dirty bathroom plate | Push-in | **ROUGH_HOLD for owner** |
| BATH-TUB | PASS still | pending full-span | Dirty plate | Closer on tub | REGEN/review |
| BATH-DRAIN | PASS still | pending full-span | Dirty plate (drained flat lives in game repo) | Drain insert | REGEN/review |
| BATH-TOILET | PASS still | pending full-span | Dirty plate | Toilet insert | REGEN/review |
| POOL-SKIM | Cleaned still | **FAIL** — extra mermaids return mid-clip | Overlay slime; no full dirty pool plate | Coping push | REGEN |

Decor extras (hanging plants, extra starfish) remain on bath stills. Not extra cast, still not delivery-clean.

## Not in A002 (queue remains)

Falls 1–3, plug pull, eagle free/wing, craft pick/scrub/customize, bunny soap/jump/land, hall paper/web/wall/finish, C2-01–09. HOLD: C2-02, C2-06, C2-07, bunny land.

**Do not treat this packet as audit-passed.** Only BATH-SINK is a rough owner-review candidate. Overnight 15-minute GitHub watch is running.
