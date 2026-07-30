# Sky Lagoon Living-Card Animation — v2 Acceptance Document (2026-07-28)

> **SUPERSEDED by `SKY_LAGOON_LIVING_CARD_ANIMATION_V3_2026-07-28.md`**,
> which carries this design language forward and adds the concrete panorama
> v5 extraction inventory, the isolate→heal→re-slice workflow, and hard
> tablet performance budgets. Implement from v3.

**For:** codex production. **Target stage:** `SkyLagoonPromenade`
(`scripts/arena/sky_lagoon_promenade.gd`, 6×2 Sprite3D promenade lineage of
`codex/sky-lagoon-reductive-extraction`, commit `08c9adaa`).
**Supersedes:** `SKY_LAGOON_AMBIENT_ANIMATION_HANDOFF_2026-07-28.md` (v1).
v1 remains as design-intent reference only; its GLB/MultiMesh/particle
prescriptions targeted the retired `claude/sky-lagoon-pnw-runtime` stage and
must not be implemented. This v2 keeps v1's behavioral goals and acceptance
tests, restated for the Sprite3D-only world.

---

## Resolved architecture decisions

Two contradictions flagged in review are settled by the promenade's own
architecture — no new machinery is introduced:

1. **No particle systems, and none needed.** Ephemeral effects (smoke puffs,
   drifting leaves) are ordinary Sprite3D cards driven by the existing
   ambient tick or looping Tweens. At promenade scale (single-digit counts)
   this is cheaper to audit and identical in cost. `probe_l2.gd`'s node-type
   inventory stays authoritative: **every card added by this document updates
   the inventory table in the same PR.**
2. **No global player-position shader uniform.** Reactive motion rides
   `_tick_ambient_life`, which already iterates the tagged ambient cards
   each frame. The rule is restated precisely: **one bounded stage tick over
   tagged cards; no per-frame allocation; no per-frame work proportional to
   anything but the (small, probe-asserted) ambient card count.** Roshan's x
   position is already on hand in the tick — reactive bend is a comparison,
   not a system.

## The Living Card contract (required design language)

Every animated world-art object is a **living card** — an unshaded Sprite3D
at a deliberate depth plane (`CLOUD_Z`…`NEAR_Z`), carrying:

- a clean silhouette with baked ink outline and warm-light/cool-shadow cel
  color (shadow tones toward the palette navy-purple, never gray);
- a bottom-center anchor with the visual root line flush to the texture's
  bottom edge (**the crop is the rig** — see art pipeline);
- recorded source aspect, measured content-height fraction, target world
  height, and (if interactive) touch footprint;
- a matching contact-shadow card (`CONTACT_SHADOW_TEX`,
  `_add_contact_shadow`/`_sync_contact_shadow`) whenever grounded;
- exactly one motion class and one intensity class (table below);
- a **deterministic phase token**: `phase = wrapf(pos.x * 0.73 + pos.z * 1.31, 0.0, TAU)`
  from placement coordinates — never `randf()`. Identical builds must
  produce identical probe captures.
- no added ornament unless it improves navigation, interaction, or
  emotional staging.

## Motion architecture — three layers

1. **Ambient** (weather + depth): slow foliage sway, cloud drift, smoke.
   Establishes that wind exists. Runs unconditionally.
2. **Reactive** (playfulness): near-foliage acknowledges Roshan passing.
   Never moves collision, never shifts a registered touch target's bounds.
3. **Authored** (staging): playground equipment, plane arrival/departure,
   castle-door moments. Unique character animation, strongest timing.
   Already implemented (`_start_playground_animation`, plane sequence) —
   this document adds nothing here and must not dilute their dominance.

**Wind coherence:** one stage-level wind state in the promenade object —
direction sign (+x) and a gust factor lerping 1.0→~1.5 on a deterministic
schedule (seeded from a build constant, not wall clock) for 2–3s every
15–40s. All ambient amplitudes and smoke drift multiply by it. Lifecycle
rule: wind state, ambient card lists, and tint are initialized in `build()`
and owned by the stage object; nothing persists past stage teardown.

### Motion classes

| Class | mechanism | intensity guide |
|---|---|---|
| `foliage_far` (DRESS_Z trees) | existing whole-card `rotation.z` sine | ±0.008–0.012 rad, speed ~0.5 |
| `foliage_near` (NEAR_Z) | tip-bend vertex shader (below) | 0.10–0.16u at tips, speed ~0.9 |
| `cloud` | existing x-drift in corridor (`CLOUD_DRIFT_MIN/MAX_X`) | as shipped |
| `smoke` | rise + fade tween loop | see smoke spec |
| `reactive_bend` | added into `foliage_near` shader | see reactive spec |

**Tip-bend shader (`lagoon_card_sway.gdshader`, the one new shader):** a
Sprite3D ShaderMaterial port of `seagrass_sway.gdshader` — `tip = 1.0 - UV.y`,
bottom row pinned, tips displace on `sin(TIME * speed + phase)`; plus a
`bend` uniform (reactive, below) and a base-AO darken of the bottom ~15%.
Whole-card rotation is fine at DRESS_Z distance but reads as a rocking
poster at NEAR_Z, where cards are large and player-adjacent — tip-bend is
reserved for exactly that plane. TIME-driven, so it costs no tick work.

## Per-screen motion budget (hard rule)

Per playable screen: **one dominant moving landmark, at most three quiet
supporting loops, calm negative space along the walk band and around every
touch target.** Never a full-screen sway or particle field.

| Screen | dominant | quiet loops (≤3) |
|---|---|---|
| 1 Runway | water motion; plane during Day One arrival only | 1 cloud drift, 1 near-foliage sway |
| 2 Playground | authored equipment animation | restrained near-foliage sway, 1 cabin smoke column |
| 3 Castle | castle invitation / door moment | cloud drift, distant smoke or flag, minimal flora |

## Work items (this stage)

1. **`lagoon_card_sway.gdshader`** on the NEAR_Z foliage cards, phases from
   placement coords, amplitudes per the motion-class table, gust multiplier.
2. **Cabin smoke** — one column: 3 puff Sprite3D cards at the painted
   chimney position, each on a staggered rise-grow-fade tween loop
   (lifetime ~5s offset by thirds, rise ~2.5u, scale 1.0→2.0, alpha out in
   the last 40%). Discrete storybook puffs, not a stream. Puff albedo ≤
   (0.92, 0.90, 0.88) — pale surfaces bloom-clip on Android. New puff
   texture ≤256px through the art pipeline. Smoke leans with wind sign.
   Placement must not overlap any painted landmark silhouette or touch
   target; it is new ornament above a painted chimney, not a re-sticker of
   a painted object.
3. **Reactive brush-past** — in `_tick_ambient_life`, for `foliage_near`
   cards only: when `abs(card.x - roshan.x) < 2.5` and Roshan is in the walk
   band, ramp the card's `bend` uniform toward
   `sign(card.x - roshan.x) * strength` (tips push away, ~0.3u max), decay
   back over ~0.6s after she passes. A stateless overshoot term in the
   shader (`sin(TIME*9.0) * bend * (1-bend) * 0.3`) gives the spring-back
   wobble. Bend is visual only — touch targets and collision untouched.
4. **Wind gust state** — the deterministic gust schedule + amplitude
   multiplication described above.
5. **Night congruence** — when `m.is_night`, multiply ambient/foliage card
   `modulate` toward dusk blue-lavender at build time (backdrop mural is
   repainted/tinted by its own pass; cards must not stay daylight-bright).

Optional embellishments (owner call, not required language): a second
drifting cloud on screen 3; 2–3 emissive glint cards (flower centers,
castle window) under the `glow_bloom 0.05` cap; falling-leaf card pair near
the playground treeline. Each consumes a quiet-loop slot — the budget table
wins every conflict.

## Art pipeline (carried from v1, amended for the promenade)

Unchanged in substance — flat source → RGBA card is still: **(0)** generate
on near-white with root line visible, no border-touching shadow, baked
outline + cel conventions; **(1)** cutout via `tools/polish_sprite.py` /
`tools/extract_connected_chroma.py`, mandatory fringe check over a dark
swatch; **(2)** anchor: bottom-flush root line, centered stem, tight top
crop, **measured** content fractions; **(3)** manifest entry (now including
depth plane, motion class, intensity class, touch footprint); **(4)** import:
Fix Alpha Border ON, mipmaps ON, **≤1024px longest side or POT per
AGENTS.md**, VRAM compress only if POT; **(5)** probe gate before use.

Promenade-specific amendments:

- **Extraction rule compliance (AGENTS.md):** a card must be either (a)
  approved art extracted from the master with the background healed behind
  it, or (b) new ornament (smoke, leaves, glints) that does not duplicate
  any painted object. Never a card over a painted copy of the same object.
- **Background masters:** per-screen ≥2048×2048 native coverage, panorama
  ratio preserved, runtime tiles never rescaled — this document adds no
  backdrop art and must not trigger a mural repaint.
- v1's silhouette backdrop rings are **dead**: the mural already paints the
  aerial perspective; extra rings would re-create the sticker-over-painting
  problem. Depth reads come from the real z-planes and value separation.

## Acceptance tests

Extends `probe_l2.gd`'s existing assertions (inventory, overdraw budget,
cloud corridor, route, occlusion). Every item below is a gate:

1. **Inventory:** node-type table updated for every added card; MeshInstance3D
   and shaded-Sprite3D world-art counts remain 0.
2. **Determinism:** two cold builds produce pixel-identical probe captures
   at t=0 (phases and gust schedule are coordinate/seed-derived).
3. **Pinned bases:** two captures 1s apart — root-line pixels of every
   swaying card static while tips move.
4. **Touch clearance:** no moving card's rect intersects any registered
   touch target's bounds at motion extremes; walk band clear of new cards.
5. **Budget:** per screen, ≤1 dominant + ≤3 quiet loops, counted in the probe.
6. **Night congruence:** night build capture — no daylight-bright card
   against the dusk mural. Hard gate.
7. **Grounding:** every grounded living card has a contact-shadow card.
8. **Layer separation:** wide capture per screen in greyscale — near
   foliage, playground plane, and mural separate as distinct value bands.
9. **Bloom:** no smoke/glint white clipping under the Android glow profile.
10. **Lifecycle:** build → exit → rebuild leaves no stray tweens, meta, or
    wind state (assert ambient card list length and tween count after
    teardown).
11. **Perf:** whole package < 1ms/frame on the speedy-tier proxy; suspects
    are tick work and overdraw, never the TIME shader.

## Portability

The Living Card contract, three-layer motion architecture, per-screen
budget, deterministic tokens, and this pipeline are the **required design
language for all future stages** (tropical reef, northern kingdom, castle
rooms). Screen choreography tables and embellishment lists are per-stage.
