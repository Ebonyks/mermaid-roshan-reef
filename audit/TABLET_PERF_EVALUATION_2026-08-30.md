# Tablet performance evaluation — Lenovo Tab M11 emulation standard

- **Evaluation ID:** `TPE-2026-08-30`
- **Date:** 2026-08-30
- **Branch:** `tablet-performance` (dev head `0ddbe656` + protocol commit)
- **Standard applied:** `audit/LENOVO_TAB_M11_EMULATION_PROTOCOL_2026-08-30.md`
  (`TEP-2026-08-30`) — confirmed unit: Tab M11 11", Helio G88, Mali-G52 MC2,
  4 GB RAM, 64 GB eMMC, 1920×1200 @ 90 Hz.
- **Method:** five independent evaluation lanes (GPU/fill-rate, script CPU and
  structure, assets/memory/APK, production/animation/design workflow, and a
  master-audit delta extraction) run in parallel against the dev head,
  cross-checked against `audit/MASTER_AUDIT_2026-08-09.md`,
  `audit/MASTER_AUDIT_2026-08-26.md`, and
  `audit/findings/ACTIVE_FINDINGS_2026-08-13.md`; plus fresh
  `tools/audit_game_2d.py` and APK-content measurements
  (local 2026-08-29 export, 574,238,773 bytes, 3,917 entries,
  632.7 MB uncompressed).
- **Authority:** SUPPORTING_CURRENT evaluation. Lifecycle ownership stays with
  the master audit; nothing here closes or reclassifies a finding. Device
  numbers remain estimates until the protocol's Lane D matrix runs
  (`MA-PERF-001`).

## 1. Headline

The game currently asks the Tab M11 to do roughly **three times the intended
work three different ways at once**: the engine free-runs against the 90 Hz
panel with no frame cap, the full 3D reef both renders and ticks underneath
almost every opaque 2D surface, and 81% of a 596 MB APK is texture data — a
third of it never tuned because the tuned import sidecars are gitignored and
CI silently exports importer defaults. None of these is hard to fix, all
three compound each other, and every one is invisible on a desktop dev
machine — which is why the emulation protocol exists.

The structural story matches the master audits: `main.gd` has regressed to
10,907 lines (+408 since the 2026-08-26 round measured 10,499 at `9a1754c1`;
`MA-CODE-001`), the Mode Platform ratchet (`tools/audit_structure.py`,
`DL-CODE-12`) was never built, and of the known extraction backlog exactly
**one** extraction converts into frame time — the reef ambient tick block.
The 3D-model purge, by contrast, is essentially done: 0 model files at this
head (was 513), 56 production 3D files remain (`MA-2D-002`).

## 2. Major weaknesses (ranked)

### W1 — No frame-pacing decision: the engine free-runs at up to 90 fps

`project.godot` sets no `application/run/max_fps`, no vsync override, and no
script anywhere touches `Engine.max_fps`. The design language writes its
budgets *as if* a 30 fps cap exists (P95 ≤ 33.3 ms in `DL-PERF-02`; the
two-frame touch rule `DL-AGE-07`), but on the M11's 90 Hz panel the engine
attempts up to 3× the designed frame work — spent directly as heat and
battery in a passively cooled 12 nm tablet, for smoothness a four-year-old
cannot perceive. 30 divides 90 exactly (3-vblank cadence, no judder).
**Impact: HIGH. Effort: one line plus an owner pacing decision and probe
gating.**

### W2 — Two worlds at once: the 3D reef renders AND ticks under 2D surfaces

The two heaviest lanes converged on this independently:

- **GPU:** no code path ever de-currents the reef `Camera3D`, hides the 3D
  world roots, or disables 3D on the viewport. Castle rooms build an opaque
  full-rect stage on CanvasLayer 14 (`scripts/arena/castle_rooms_25d.gd:931`)
  but hide only the player and HUD; melody, opera, and the picture games do
  the same. The Mobile renderer burns a full 3D frame — terrain, water
  sheets, omnilights, glow chain — and then covers 100% of it with opaque
  canvas.
- **CPU:** `main.gd:9593` gives only kart an early return before the reef
  tick block; galaxy/ember/combat/stuffie/dungeon/opera `pass` at
  `main.gd:9679-9692` and then fall through to the full ambient block
  (`main.gd:9695-9707`) plus the pearls/friends loops above the chain —
  an estimated 2–4 ms of script per frame for an invisible world, paid in
  exactly the modes whose own tick is most expensive. The code comments the
  behavior at `main.gd:2450-2453`.

The suspend pattern already exists in-tree three times (kart at 9596;
galaxy/ember via `PROCESS_MODE_DISABLED` at `main.gd:2941` and `3147`), so
the fix is a mechanical generalization, one mode per probe-gated commit.
**Impact: HIGH — the single largest recoverable cost on both processors.**

### W3 — Speedy tier leaves the expensive GPU luxuries on

`_apply_quality` (`main.gd:3649`) tiers shadows, resolution scale, and
plankton — but on Speedy the game still pays for:

- the reef terrain drawn **twice**: `_add_caustics()` (`main.gd:1700-1728`)
  re-instances the whole ~24k-tri terrain with an additive transparent
  shader, unconditionally, on every tier — unlike god rays, which are gated;
- the glow post-chain enabled in every environment (`main.gd:1454-1461`
  clamps intensity but never disables; only kart does it right:
  `scripts/kart.gd:584`);
- lit-transparent `toon_water` sheets (reef ceiling alpha 0.52 at
  `main.gd:1785`; four lagoon sheets) whose shader writes
  `NORMAL_MAP`/`ROUGHNESS`/`METALLIC` — the most expensive pixel class on
  Mobile — over terrain already shaded once;
- inverted-hull outlines as `next_pass` on every gen2 prop and creature
  (double draw calls/vertices on a 2-EE GPU);
- 38 `OmniLight3D.new()` sites across 8 production scripts (lagoon keeps 6+
  lanterns live on Speedy over that lit water);
- and one tap on the HUD quality button flips the tablet to "sparkly":
  2-split PSSM shadows on three suns plus full-res 3D — a latent 30 fps
  breaker with no mobile clamp.

**Impact: HIGH in the lagoon/reef, MED elsewhere. Most items are one-line
tier gates following precedents already in the file.** (`MA-PERF-003` and
`DL-CODE-08` already name the tier-coverage gap; the newest child-facing
surfaces — melody, Day One, side_scroll — contain zero tier references.)

### W4 — Per-frame server-write and allocation churn in ambient systems

The script budget bleeds through many small, mechanical leaks:
84 MultiMesh fish transforms rewritten every frame with fresh `Transform3D`s
and ~350 trig calls, undistance-gated (`main.gd:10211-10221`); friend pillar
materials and beacon lights rewritten every frame at unchanged values
(`main.gd:8398-8420`); a growing mover fleet — ~50+ on a mature save — doing
per-frame transform writes and greet distance checks (`main.gd:2458-2490`),
meaning **the richest save plays worst**; collection markers writing
`visible`/`modulate` per critter per frame
(`scripts/collection_system.gd:110-143`); ~20 joypad polls per frame each
allocating an Array on a device with no gamepad (`main.gd:876-905`);
`player.gd` interrogating its parent with ~20 dynamic `"x" in node` lookups
per frame (`player.gd:556-611`); and the audited `_sparkle_burst` allocation
churn — `CPUParticles3D` + `BoxMesh` + `StandardMaterial3D` per call, 141
call sites, no pooling, no tier gate (`main.gd:8437`, `MA-PERF-002`) — still
byte-identical to its 2026-08-26 description and still the cheapest
high-confidence hitch fix in the corpus. **Impact: HIGH in aggregate; each
item is a small in-place change using cadence idioms the file already has**
(half-rate god rays at `main.gd:10420`, staggered seabed at `main.gd:2471`).

### W5 — The 596 MB APK: untuned, duplicated, and debug-built

Measured composition: **81% textures** (485 MB uncompressed), 74 MB engine
libs, 31 MB audio. The specific defects, in causal order:

1. **The pipeline defect that blocks every texture fix:** `.gitignore`
   ignores `*.import`; 729 of 1,685 texture sidecars are untracked, so CI
   regenerates them with defaults (lossless) and every locally tuned
   compression decision silently never ships. Until sidecars are committed,
   texture optimization on this game is a no-op.
2. 232.5 MB of the APK is **lossless** texture data (800 files) that also
   decodes to full RGBA8 in shared RAM at runtime.
3. **68 MB of byte-identical duplicates** ship twice — the entire castle
   background tile set exists under both `assets/flats/castle/rooms/` and
   `assets/flats/castle/interactions_v4/` (~55 MB), and runtime reads only
   one of them.
4. `assets/opera/worlds` alone is **147 MB (~25% of the APK)** for 16 career
   minigames.
5. The phone receives a **debug** engine build (`--export-debug` in
   `android.yml`; 76 MB `libgodot_android.so`, roughly double release size,
   with debug-cost execution on the G88).
6. ~16.6 MB ships with zero runtime references (`assets/galaxy/` — grep
   finds nothing loading it — plus `docs/` images not covered by the `*.md`
   exclude).

Realistic end state from the non-destructive fixes alone: **~300–350 MB**,
with protected `assets/book/`, `assets/audio/voices/`, and
`assets/characters/friends/` untouched (`MA-ASSET-001`, `DL-PERF-06`,
`DL-PERF-07`). **Impact: HIGH for install/update on the 64 GB family device;
MED for runtime memory.**

### W6 — Castle working set and main-thread decode freeze

The castle hall loads all 16 lossless 910×1024 NPOT tiles at build
(`scripts/arena/castle_rooms_25d.gd:1282`): ~57 MB RGBA8 resident for the
hall background alone before props, and 1–2 s of main-thread WebP decode on
two A75 cores at entry — a frozen-touch window for the child. Re-cutting the
same approved master into POT 1024² crops with VRAM compression drops it to
~15 MB and removes the decode stall (pixels unchanged; needs the tiling
change signed off under the full-frame rule). Room-tile release on exit is
already correct. **Impact: MED-HIGH on a 4 GB device.**

### W7 — The 16:10 device is structurally invisible to the workflow

The expand stretch gives 1280×800 of design space on the tablet, but:
hardcoded `720` layout math persists in measured spots (audience rows, card
clamps, `feet.y/720` depth in the opera world); the `project.godot` test
override is 1920×1080 (16:9); and **every committed visual-evidence capture
is 1280×720** — the acceptance workflow never sees what the target tablet
shows. Protocol Lane A plus a 1280×800 capture lane fixes the blindness;
deriving layout constants from `get_visible_rect()` fixes the math.
**Impact: MED (correctness on device, and all overdraw math is 11%
optimistic before the 1.5× device scale).**

### W8 — Production/animation choices that spend device budget for no
child-visible gain

- Standing full-screen translucent layers as an Opera habit: a permanent
  10%-alpha full-rect shade, per-career spotlight alpha polygons, stacked
  full-rect FX layers, an 84%-alpha top bar — measured chrome at **50.8% of
  the screen** in the framing audit, blended every frame on a GPU where each
  full-screen blend is 2.3M pixels. The framing audit's own redesign lands at
  13.9% — the perf fix and the approved beauty fix are the same change.
- The full-screen `fade_rect` idles at alpha 0 but is never hidden —
  ~2.3 Mpx of pointless blended fill on every frame of the entire game
  (`main.gd:3497-3502`; gates test alpha, not visibility).
- The opera backdrop recomposes four 1024×2048 tiles plus vector spotlights
  via `queue_redraw()` every 0.08 s (`scripts/opera_world_backdrop_2d.gd:89`)
  instead of rendering once to a static texture.
- The detective lens forces a full-canvas screen copy per frame via
  `hint_screen_texture` to feed a 260 px widget
  (`scripts/opera_career_world_2d.gd:824-841`).
- Future cinematics: Theora is CPU-decoded (~a large fraction of one A75
  core at 720p), and the current handoff pattern plays the video **over the
  still-built, still-rendering room**
  (`scripts/day_one_bathroom_movie_handoff.gd:185-197`; no `.ogv` files have
  landed yet). Suspending the scene under the player is free; authoring new
  timelines at 12 fps (a classic storybook cadence that divides both 30 and
  90) would cut decode cost and cut the number of full frames to generate
  and human-review per second by a third — the binding full-frame rule
  untouched, since no rule pins timeline fps.

**Impact: MED-HIGH in aggregate, and most items improve the child's view.**

### W9 — Structure is regressing against the audited restructuring plan

`main.gd` grew +408 lines in the 71 commits since the 2026-08-26 round
(`MA-CODE-001` target < 2,500; G7 checkpoint ≤ 9,000 not started).
`tools/audit_structure.py` — the append-only ratchet `DL-CODE-12` specifies —
does not exist, so nothing arrests the growth. Of the extraction backlog,
intro/HUD/craft/wardrobe/arena-builder moves are pure maintainability (no
per-frame cost); the one extraction that pays frame time is pulling the reef
ambient block (`_tick_life`/`_tick_movers`/`_tick_aquatic`/`_tick_guide` +
pearls/friends loops) into a Phase-7 satellite with a single `tick()` entry,
because a single call site makes W2's mode gate a one-line, kart-identical,
probe-tolerated change. Scheduling note from the 2026-08-26 handoff: the
`_sparkle_burst` fix is assigned to WP-C4 (FxService) — coordinate so it is
not fixed twice. **Impact: MED directly, HIGH as the enabler for W2/W4.**

### W10 — Dead and lost systems still billed at boot

`_tick_wind`, `_tick_wind_streaks`, `_tick_surf_rings`, and `_tick_sleep`
have no callers anywhere in this tree (`_tick_sleep`'s caller lived in
`scripts/arena/castle_hall.gd`, which no longer exists here — its `.uid`
remains), yet their pools are still built at boot (`main.gd:984-985`) and
the `wind_dir`/`wind_gust` shader globals never update. This looks like a
lost-in-merge regression, not a decision — **surface to the owner before
anyone deletes or "optimizes" it**. Boot also builds the entire reef
synchronously before the start menu (`main.gd:969-1061`) — cold-boot cost on
eMMC that lazy/deferred idempotent spawns would trim. **Impact: LOW runtime
today; owner-attention item.**

## 3. What is already healthy

Credit where the codebase has the right idioms: the model purge is done
(513 → 0 model files); zero NPOT+VRAM-compress deadlock candidates in 1,685
sidecars; arenas/lagoon/castle build lazily on entry and castle room tiles
release on exit; melody/slide/promenade/kart show correct full suspension;
half-rate and staggered cadence idioms exist and are copyable; Jolt's 3D
space steps essentially empty (< 0.1 ms — removal is hygiene, not perf);
audio is proportionate (30.8 MB shipped) with only five music loops below
the 64 kbps floor; and `preload()` discipline is good. The evaluation found
no evidence against the no-fail-state, touch-first design — the perf debt is
implementation and pipeline, not concept.

## 4. Priority sequence (impact ÷ effort, respecting repo rules)

| # | Action | Weakness | Effort | Expected gain |
|---|---|---|---|---|
| 1 | Commit `.import` sidecars (unignore `assets/**/*.import`) | W5.1 | Small | Unblocks all texture work; makes APK reproducible |
| 2 | Frame-pacing decision + `run/max_fps` | W1 | One line + owner call | ~3× frame work, heat, battery |
| 3 | Reef suspend gate, one mode per commit (kart pattern) | W2 | Small ×7 | 2–4 ms script + a full 3D frame per covered mode |
| 4 | Speedy gates: caustics, glow, water shader branch, outlines, `fade_rect.visible` | W3, W8 | One-liners | Largest GPU fill recovery |
| 5 | Export excludes (`assets/galaxy/*`, `docs/*`) + castle-tile dedupe | W5.3/5.6 | Small | −80 MB APK, zero risk |
| 6 | Release-mode export for the stable channel (keystore) | W5.5 | Owner setup | −35 MB APK + faster engine |
| 7 | Lossy/VRAM import pass over non-protected flats | W5.2 | Medium | −150–180 MB APK, less RAM |
| 8 | Server-write/allocation guards (fish cadence, friend cache, joypad cache, label guard) | W4 | Small each | ~2–3 ms script |
| 9 | `_sparkle_burst` pooling — inside WP-C4 per the 2026-08-26 handoff | W4 | Medium | Hitch source removed |
| 10 | Reef-ambient satellite extraction + structure ratchet tool | W9 | Medium | Enables 3 and future zone suspension |
| 11 | Castle tiles → POT crops + threaded load (full-frame sign-off) | W6 | Medium | −42 MB resident, no entry freeze |
| 12 | 1280×800 capture lane + `get_visible_rect()` math sweep | W7 | Medium | Device-true acceptance |
| 13 | Opera chrome cuts as DL-PERF-03 overdraw recovery; static backdrop compose; lens without screen copy | W8 | Medium | Opera fill budget restored |
| 14 | Cinematic staging rule (suspend under player) + 12 fps timeline default for new shots | W8 | Doc + small | Decode headroom + ⅓ fewer frames to produce/review |
| 15 | Lane D device baseline run per protocol | all | Owner session | Calibrates every estimate; unblocks `MA-PERF-001` |

## 5. Relation to open findings

This evaluation adds evidence toward, and proposes no lifecycle change for:
`MA-PERF-001` (the protocol's Lane D is its matrix), `MA-PERF-002`
(re-verified byte-identical), `MA-PERF-003` (re-verified tier-blind),
`MA-ASSET-001` (duplicate/orphan measurements above), `MA-ASSET-004`,
`MA-2D-002` (fresh inventory 0/56), `MA-CODE-001` (10,907 lines),
`MA-CODE-002`, `MA-TOUCH-002` (unguarded swim branch re-verified at
`scripts/games/side_scroll.gd:158-167`), and `MA-RELEASE-001`. New
owner-attention items with no existing finding id: the untracked-sidecar
export defect (W5.1), the missing frame cap (W1), the dead wind/surf/sleep
tick systems (W10), and the debug-build stable channel (W5.5).
