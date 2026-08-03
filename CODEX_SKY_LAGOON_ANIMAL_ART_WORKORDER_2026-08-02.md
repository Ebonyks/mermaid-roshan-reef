# Sky Lagoon animal realism — execution split and Codex art work order

Date: 2026-08-02
Parent audit: `docs/audits/SKY_LAGOON_ANIMAL_REALISM_2026-08-02.md` (findings,
measurements and the R1–R12 remediation plan referenced throughout)
Evidence tool: `tools/audit_sky_lagoon_animal_realism.py`

## Verdict

Nine of the twelve remediation steps need **no new art at all** — they are
promenade code, coordinates, and probe work, and they contain every one of the
critical findings. Three steps are art-blocked and belong to Codex, which owns
the 2D channel these animals came from (the shipped atlases were OpenAI image
generation; see `assets_src/sky_lagoon/ambient_animals_2026-07-29/README.md`).
One step needs owner-sourced CC0 **audio**, which is not Codex's channel.

The order matters: the art half is worth commissioning now because it is the
long pole, but the code half is what makes the animals visible and grounded at
all, and none of the art pays off until it lands.

## The split

| Step | Needs new art? | Owner | Why |
|---|---|---|---|
| R1 reachability (page → visibility binding) | No | Claude | Pure camera/frustum logic plus a probe fix. Unblocks 3 of 5 species. |
| R2 grounding (painted-ground validator, re-sited paths) | No* | Claude | Coordinates + a ground polyline sampled from the existing panorama. *See decision D1. |
| R3 mural socket lock | No | Claude | One `_register_mural_socket` call and a per-tick anchor, identical to the playground cards. |
| R4 atlas baseline normalisation | No | Claude | A measured per-frame `Sprite3D.offset` table fixes the shipped drift losslessly, without regeneration. |
| R5 gait rebuild | Partly | Claude now, Codex to finish | A believable hop needs an airborne pose. Interim: borrow the startle sheet's bound poses. Proper: the 16-pose sheet below. |
| R6 idle repertoire | Partly | Claude now, Codex to finish | Deterministic dwell variation, breathing and better use of the four existing poses are code. Forage/groom/tail/ear poses are art. |
| R7 awareness of Roshan | No | Claude | One distance term. Highest behavioural yield per line of code in the whole list. |
| R8 species-specific escapes | Partly | Claude now, Codex to finish | Timings, directions, distance grading are code. "Otter enters water" wants a ripple card; "squirrel goes up" wants a trunk to go up. |
| R9 entrances/exits from cover | **Yes** | Codex | There is nothing to enter or leave: the shrubs are painted into the flat mural and cannot be shaken or hidden behind. Needs cover standees at animal depth. |
| R10 sound + physical activation cue | **Yes**, split | Codex (cards) + owner (audio) | Dust-puff/ripple cards replace the sparkle burst. The four OGG cues are CC0 sourcing, not an image job. |
| R11 diel roster | No | Claude | Uses the existing five atlases and the already-audited night tints. |
| R12 scale pass | No* | Claude | Card `height` values only. *See decision D2 — a shrunken frog may need a bolder silhouette. |

## What I will do, in order, with no art dependency

**Batch 1 — corrective (this is the batch that matters).** R1 + R3 + R4, then R2.
Reachability first because everything else is invisible without it; socket lock
and baseline normalisation next because they are small, mechanical and remove
the two strongest "sticker" cues; grounding last in the batch because it depends
on R1's final habitat positions. Gate: the parent audit's tool re-run (footing
sheet clean, all five species framed at 16:9 / 19.5:9 / 20:9) plus the probe.

**Batch 2 — behaviour on the existing four poses.** R7 awareness, R11 diel
roster, R6 partial (deterministic dwell variation, always-on breathing via a
±1.5% `scale.y`, better mapping of the four poses), R5 partial (ballistic
forward motion, easing, turn-instead-of-flip, borrowing the startle sheet's
bound poses for hop cycles), R8 partial (per-species timings, exit directions,
tap-distance grading). This is most of the perceived life, using zero new art.

**Batch 3 — after Codex delivers.** Swap to the 16-pose sheets, add cover
standees and their enter/exit behaviour, replace the sparkle burst, wire audio.

## Two authorisations I need before Batch 1

1. **Probe edit.** `probe_sky_lagoon_animals.gd::_move_to_page()` teleports the
   camera to ±48, which the live pan clamp can never reach, so its page-0 and
   page-2 assertions certify an unreachable scene (audit finding 15). Fixing it
   is the explicit goal of R1, which the `CLAUDE.md` refactor rule permits — but
   it is a probe change and I will call it out in the commit message.
2. **CI workflow edit (high-risk under `CLAUDE.md`).** `probe_sky_lagoon_animals`
   is **not in the CI probe list** — the animals are currently ungated on every
   push. I verified the probe is headless-clean (its captures are gated behind
   the `LAGOON_ANIMAL_SHOT_OUT` env var), so adding it to the headless list in
   `.github/workflows/probes.yml` is a one-line change. Without it I cannot
   verify any of this work: there is no Godot binary in the session container.

## Three decisions for the owner

**D1 — where the shore animals live.** The otter and frog are authored at
x ≈ −62, in the far-west pond. That is unreachable above 19.3:9 and, even at
16:9, framed only in the outermost 4% of the camera's travel. The reachable
west window (x −58 … −24) is painted as stone path, grass verge and shrubs —
**no water at all**, so an otter cannot be re-sited west without new art.

- *Recommended, zero art:* move the otter and frog to the **east lake shore**
  (x ≈ 28–40), which the panorama paints as real water, rounded shore boulders
  and a stone landing, and which is comfortably framed at 20:9. The raccoon
  already lives there; the three share a shore habitat, staggered.
- *Alternative:* keep them west and commission a Codex water-pool standee. More
  art, and it still sits at the edge of frame.

**D2 — how big the frog should be.** It currently reads 12.2 cm, 2.7× life. A
truthful Pacific tree frog would render about 5 px tall on a phone — too small
for a four-year-old to see or aim at. I propose keeping it stylised at roughly
1.1 units (~14 px) and fixing the *ordering* by growing the otter and raccoon
instead. If you want it smaller than that, its silhouette needs a Codex
re-render, not a downscale.

**D3 — how far to take the escape.** "Squirrel goes up a tree" and "otter slips
into the water" are the two most convincing exits available, and both need
somewhere to go: a trunk standee near the meadow, and a ripple card at the
waterline. Say the word and they go into the order below; without them the
squirrel and otter exit sideways like everything else.

---

# Codex work order

House rules from `CODEX_BACKGROUND_FLATS_WORKORDER_2026-07-27.md` and
`CLAUDE.md` apply unchanged and are binding: project-original or CC0-derived art
only; the `ART_STYLE_GUIDE` pastel PNW palette with deep plum/navy contours; no
words, letters or digits anywhere; power-of-two sizes; one `ASSET_LICENSES.md`
line per file in the commit that adds it; a generation ledger under
`assets_src/`; never read from or write to `assets/book/`,
`assets/audio/voices/`, or `assets/characters/friends/`.

Identity is fixed. These five animals already exist and the child has seen them.
Every new sheet must preserve each species' exact markings, proportions, palette
and painted finish from the shipped
`assets/sprites/sky_lagoon/animals/*_idle_atlas.png`, which are the sole identity
reference. This is a pose expansion, not a redesign.

## A. Behaviour sheets — the blocking deliverable

Five files, one per species, replacing the current idle+startle pair:

```
assets/sprites/sky_lagoon/animals/otter_behaviour_atlas_v2.png
assets/sprites/sky_lagoon/animals/frog_behaviour_atlas_v2.png
assets/sprites/sky_lagoon/animals/hare_behaviour_atlas_v2.png
assets/sprites/sky_lagoon/animals/squirrel_behaviour_atlas_v2.png
assets/sprites/sky_lagoon/animals/raccoon_behaviour_atlas_v2.png
```

**512×512 RGBA, read as a 4×4 grid of 128 px cells — 16 poses per species.**

This costs nothing. The audit measured the shipped animals at 4.1×–7.9× linear
oversampling: they display 18–52 px tall on a 720p phone from 100–211 px source
subjects. At 128 px per cell they are still 2–4× oversampled. Sixteen poses
therefore arrive at the *same* file size, and two files per species become one,
so VRAM halves.

Frame contract (row-major; the runtime indexes these exactly):

| # | Pose | Ground |
|---|---|---|
| 0 | calm stand, neutral, facing screen-right | grounded |
| 1 | forage: nose down, sniffing the ground | grounded |
| 2 | forage: handling/chewing, head low | grounded |
| 3 | vigilance: head up, scanning, ears forward | grounded |
| 4 | walk cycle — contact A | grounded |
| 5 | walk cycle — pass/push-off A | grounded |
| 6 | walk cycle — contact B | grounded |
| 7 | walk cycle — pass/push-off B | grounded |
| 8 | hop: crouch/load | grounded |
| 9 | hop: launch, toes still down | grounded |
| 10 | hop: airborne apex, body extended | **airborne** |
| 11 | hop: landing, forelimbs reaching | grounded |
| 12 | comfort: grooming (paw to face, or tail wrap) | grounded |
| 13 | comfort: ear flick / head turned away from camera | grounded |
| 14 | startle freeze: ears up, eyes wide, playful surprise | grounded |
| 15 | escape bound: stretched, screen-right | **airborne** |

### The one requirement that matters most

`Sprite3D` centres each atlas cell, so where the subject sits *inside* its cell
decides where the animal's feet land in the world. The shipped sheets drift by
up to 21% of a cell — 0.6 world units, seventeen times the animation's own bob —
which is why the current animals detach from their own shadows twice a second.

**Every grounded pose must be drawn with its feet on one shared canvas baseline,
within ±2 px of each other.** The two airborne poses must sit *above* that
baseline by their real hop height and never below it — that lift is the hop arc,
and the runtime will use the art instead of adding a sine.

Self-check before delivery; this is the acceptance gate and it is run again on
the receiving end:

```
python3 tools/audit_sky_lagoon_animal_realism.py \
    --verify-sheet assets/sprites/sky_lagoon/animals/hare_behaviour_atlas_v2.png \
    --grid 4x4 --airborne-frames 10,15
```

It prints per-frame baseline deviation and exits non-zero on any pose outside
tolerance. Subject height is reported but not gated — a crouch really is shorter
than a bound; only identity/scale drift beyond 40% is flagged.

Also required, unchanged from the 2026-07-29 batch: exactly one animal per cell,
generous padding, nothing touching a cell edge, opaque subject with a crisp
separated silhouette, no cast or contact shadow (the engine draws it), no floor
plane, no scenery, no props, no clothing, no shell/pearl/rainbow decoration.
Expressions stay playful surprise — never tears, trembling, bared teeth or
distress.

Keep the existing ten sheets in place. The runtime will switch over in a
separate commit; they are the shipped fallback until it does.

## B. Cover standees — unblocks entrances and exits

Three files, `512×512` RGBA, alpha, **bottom edge of the painted art is the
ground line** (the engine plants it there):

```
assets/sprites/sky_lagoon/lagoon_cover_shrub_meadow_v1.png
assets/sprites/sky_lagoon/lagoon_cover_shore_rocks_v1.png
assets/sprites/sky_lagoon/lagoon_cover_reeds_lake_v1.png
```

- **shrub_meadow** — a low salal/salmonberry clump, waist-high to a hare, dense
  enough to hide one. Sits at the meadow habitat.
- **shore_rocks** — two or three rounded lake boulders with a tuft of grass,
  matching the panorama's existing shore stones.
- **reeds_lake** — a sparse reed/sedge tuft for the waterline.

These stand at the animals' depth, in front of the mural, so an animal can walk
behind one, disappear into it, and make it shake. Each must read as belonging to
the shipped `flat_sky_lagoon_main_panorama_v5` — same greens, same plum
contours, same painted leaf language — because it will sit directly against it.
Sparse silhouettes: they must never occlude Roshan's route or a tappable prop.

## C. Effect cards — retire the sparkle burst

Three files, `512×128` RGBA, four `128×128` frames left to right, alpha baked to
fade across the strip:

```
assets/sprites/sky_lagoon/lagoon_fx_dust_puff_v1.png
assets/sprites/sky_lagoon/lagoon_fx_water_ripple_v1.png
assets/sprites/sky_lagoon/lagoon_fx_leaf_flick_v1.png
```

- **dust_puff** — a small pale ochre/lavender scuff at a push-off point,
  expanding and thinning. Not a star, not a sparkle, no gold.
- **water_ripple** — an expanding aqua/white ring seen at a shallow angle, for an
  otter or frog entering the lake.
- **leaf_flick** — two or three leaves displaced upward, for something entering
  cover.

The current activation fires `_sparkle_burst` — 36 gold cubes, the game's
*reward* vocabulary — at a fleeing wild animal. These cards replace it. Keep
them physical and quiet.

## D. Conditional — only if the owner chooses it

- **`lagoon_water_pool_west_v1.png`** (512×512 standee) — only if decision D1
  keeps the otter and frog in the west. Not recommended; the panorama already
  paints reachable water in the east.
- **`lagoon_cover_trunk_meadow_v1.png`** (512×1024 standee) — a conifer trunk
  base for the squirrel to run up, if decision D3 goes that way.
- **Frog re-render** — only if decision D2 shrinks it below ~1.1 world units;
  a 5 px frog needs a bolder, simpler silhouette, not a downscale.

## Ledger and delivery

Mirroring the 2026-07-29 batch exactly:

- `assets_src/sky_lagoon/ambient_animals_v2_<date>/PROMPTS.md` — every prompt
  verbatim, with the generation mode;
- `.../manifest.csv` — source → runtime file mapping with sizes;
- `.../contact_sheet_runtime.png` — review-only, never loaded by the game;
- background removal and runtime normalisation documented as before (flat
  `#ff00ff` chroma key, `remove_chroma_key.py`, whole-canvas Lanczos to the
  final POT size — no pose individually moved, warped or composited);
- one `ASSET_LICENSES.md` line per delivered file, in the same commit;
- every sheet passing `--verify-sheet` before it is committed.

## Not Codex: the audio

Four short cues are the highest realism-per-byte item in the whole audit and the
scene currently has none: a foliage rustle, a small water entry, a tree-frog
chirp, a squirrel chatter. OGG, loop-tagged where appropriate, CC0 with an
`ASSET_LICENSES.md` line each. This is a sourcing job for the owner (or whatever
audio channel is preferred) — Codex is the image channel. I will wire the
playback and ducking against stub paths so the cues drop straight in.
