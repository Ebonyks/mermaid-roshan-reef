# Cleaning Day — asset & minigame requests (Codex handoff)

Owner request 2026-07-22. Audience: the code-generation agent (Codex)
producing the Day 1 "Cleaning Day" art pass. Read
`assets/ART_GENERATION_CONTRACT.md` FIRST — pipeline split, scoring loop,
palette anchors, and audit-memory rules all bind here. Narrative source of
truth: `STORY_DAYS.md` §3 Day 1 (the frame: gremlins snuck into the Pearl
Castle over winter, sooted it up, and Roshan cleans it for the Festival of
Lights; the relit chandelier is the week's first Light).

House rules recap (binding): pastel toy playset look, flat multi-material
Blender-generated geometry (texture-free where possible), any texture
≤1024px POT, no new OmniLights, ASSET_LICENSES.md line per asset in the
same commit, Mobile-renderer captures before any score above 2/5, and the
Mali-G52 transparent-overdraw budget is a hard limit — grime and bubbles
are transparency-heavy, so this pass must be disciplined about overlay
count and size. Protected zones untouched as always: `assets/book/`,
`assets/audio/voices/`, `assets/characters/friends/`.

Stand-in note (CLAUDE.md owner decision 2026-07-22): the soot sprite is a
tracked Ghibli-likeness stand-in (STORY_DAYS.md §5 ledger). Generate
resemblance only — never trace, sample, or import franchise art — and let
each iteration drift the design toward its original release identity
(pastel tint, pearl texture, reef-flavored details are good drift moves).

Target paths: models `assets/cleaning/`, generator scripts
`tools/build_cleaning_kit.py` (one deterministic script, contract-style),
SFX `assets/audio/sfx/`. Engine consumer: the planned
`scripts/games/clean.gd` satellite (STORY_DAYS.md §9 W4); placeholder node
names below are the contract for its blockout so art drops in one-for-one.

---

## 1. Critters

### 1a. Castle gremlins — REUSE, accessory pass only
The gremlins ARE the shipped mischief imps (`assets/dungeon/mischief_imp.glb`
+ the two `r052` dungeon variants) — owner decision, same pattern as the
opera's backstage pests ("they get everywhere"). No new creature. Requests:
- **Soot-dusted palette variant** (material-slot recolor, not a new mesh):
  smudged cheeks, grey dust motes on the head fuzz.
- **Soot-trail emitter** (`ImpSootTrail`): a few dark puffs that fall
  behind a scurrying imp and land as new soot-sprite spawn markers.
- **Pop burst** (`ImpPopBurst`): reuse/retint the opera confetti-pop —
  pastel star flash, no smoke, never scary.
- **Stolen-decoration carry props**: mini garland loop, mini lantern (the
  §3 items an imp drops when popped — see 3b).

### 1b. Soot sprites — NEW (stand-in, see header note)
The mess made adorable: round black fuzzball, oversized white eyes, tiny
stick limbs optional. States/deliverables:
- `soot_sprite.glb` — fuzzy sphere silhouette (shader/fin-shell fuzz, not
  alpha-card hair), 2 sizes (hand-size, cushion-size), ≤1.5k tris each.
- Clips or engine-driven poses: idle jiggle, scurry-hop, hide-peek
  (squash behind props), caught-wiggle.
- **Scrub transformation twin** `stardust_puff.glb`: the cleaned form —
  pearl-white/pastel puff with sleepy-happy eyes that floats to the
  rafters. Same topology recolored/retextured is fine; the pop moment is
  a particle cross-fade (`SootScrubBurst`), bubbles + sparkles.
- Rafter roost cluster (`PuffRoost`): 3–5 puffs huddled on a beam,
  gentle bob — becomes ambient decoration and returns on Festival Day.

### 1c. Dust bunnies — NEW (generic, no stand-in flag)
Passive dirt, distinct from the sprites: pearl-grey lint wads that drift
in corners and under furniture, no eyes until disturbed — then two shy
blinks. One tap → `whoosh` scatter into motes (no chase, instant clear;
the beginner-friendliest critter and the first thing the tutorial points
at). Deliverables: `dust_bunny.glb` ≤600 tris, corner-cluster variant,
scatter-mote burst (`BunnyWhoosh`).

## 2. Grime on the walls — the dirty layer (and how it wipes)

All grime is a REMOVABLE OVERLAY on existing castle surfaces — never a
repaint of the castle materials themselves. Wipe-reveal is one shared
shader: a radial alpha mask driven by touch strokes (`grime_amount` 1→0),
so each asset below is a decal/mesh family, not a per-state texture set.
Keep individual decals small and localized (overdraw budget); the castle
must read dirty from composition, not from a full-screen film.

- **Soot smudge decal family** (`GrimePatch0..N`): 4 hand-painted-look
  smudge shapes (POT alpha sheet, one 512 atlas for the whole family),
  navy-grey, soft edges, scaled/rotated instances — floors, walls, throne.
- **Cobwebs** (`CobwebCorner`, `CobwebSwag`): corner triangle + hanging
  swag, chunky child-readable strands (geometry ribbons preferred over
  alpha cards where silhouette allows), pastel-grey.
- **Tarnish state for gold trim** (`TarnishTrim`): darkened satin material
  variant for the Grand Hall's gold accents — a material swap on wipe,
  zero new textures.
- **Foggy window panes** (`FoggyPane`): frosted material variant on the
  existing window assets + one finger-squiggle reveal mask; wiping shows
  the reef outside sparkling through.
- **Sooty chandelier state** (`ChandelierSooty`): grey-dimmed material
  variant of the existing chandelier + its relight moment (see 4d).
- **Scrub feedback**: `SparkleCleanBurst` (chime-synced sparkle wipe that
  follows the finger), fat soap-bubble particles, squeegee streak flash.

## 3. The reward layer — walls get BEAUTIFUL, not just clean

Cleaning should transform the castle, not restore a beige default. Two
sub-families:

### 3a. Revealed wall dressing
Under the grime, wipe-reveals uncover authored wall art (these are the
"extra textures on the wall" — POT ≤1024, storybook-flat, original):
- Framed pastel portraits ×4 (`WallFrame0..3`): seahorse, shell crown,
  the Pearl Castle itself, a starfish family — original paintings in the
  book-adjacent style, NEVER book art copies.
- Mosaic tile banding (`MosaicStrip`): aqua/lavender wave motif strips
  for the Grand Hall dado line.
- Tapestry pair (`TapestryL/R`): woven-look hangings with the festival
  lantern-ring motif — foreshadows Day 7.

### 3b. Festival decorations the gremlins stole (return on imp pop)
- Garland strands (`GarlandHook0..N`): pearl-and-shell swags that fly
  back to their hooks.
- Festival lanterns (`LanternHook0..N`): the lantern-ring language from
  STORY_DAYS.md §1, unlit until Day 7.
- Bunting triangles (`BuntingRun`): courtyard run, kart-flag palette.

## 4. Cleaning tools & effects (Roshan's verbs made visible)

- 4a. **Bubble brush** (`BubbleBrush`): a chunky pastel scrub brush with a
  soap-bubble crown that appears in Roshan's hand during scrub strokes
  (verb-layer attachment, same slot as the fetch ball). No new rig work.
- 4b. **Soap bucket** (`SoapBucket`): courtyard refill prop, purely
  flavor — tap for a bubble fountain giggle.
- 4c. **Companion feather duster** (`DusterProp`): the stuffie companion's
  helper prop — it dusts high shelves (STUN-equivalent flavor; agency
  rule holds, only Roshan's touch actually cleans).
- 4d. **Chandelier relight moment** (`ChandelierRelight`): the Day-1
  payoff — warm emissive ramp + slow sparkle rain + the Crown Light
  detaching and floating to the lantern ring. Emissive material
  animation ONLY — no new OmniLights (hard rule).
- 4e. **HUD picture meter** (`hud_clean_meter`): sooty-castle →
  sparkling-castle picture pair + fill sweep, non-reader progress at a
  glance (never a number).

## 5. Cleaning minigames (design contract for clean.gd)

Core beat (both required for the Crown Light, both fail-free):
1. **Gremlin Chase** — pop the imps. 100% reuse of the brawl engine's imp
  verb (helpers stun, ONLY Roshan's tap pops — the probe agency rule).
  Needs: 1a assets only.
2. **Sparkle Scrub** — wipe grime patches (hold-rub OR repeated taps both
  work, one finger). Needs: §2 shader + decals, 4a, 4e.

Room-sized bonus games (optional, replayable in free play; each reuses a
proven engine verb, each is its own small asset packet):
3. **Window Wipe** (music room) — finger-squiggle the fog off panes;
  free-draw in the fog first is allowed and rewarded with giggles.
  Verb: picture-games touch-draw path. Needs: `FoggyPane`.
4. **Cobweb Sweep** (corridor) — one swipe per web, dust bunnies scatter.
  Verb: seek/tap. Needs: cobwebs, 1c.
5. **Treasure Polish** (throne room) — rub a tarnished crown/goblet/mirror
  until it flashes gold, 3 items. Verb: picture-games rub. Needs:
  `TarnishTrim` props + polish flash.
6. **Cushion Toss** (playroom laundry) — throw scattered cushions into a
  wash bubble; it burps bubbles. Verb: fetch throw arc. Needs: cushion
  props ×4, wash-bubble goal.
7. **Toy Tidy** (playroom) — drag toppled toys to the toy chest. Verb:
  dolls drag. Needs: toy props reuse (Toy Castle set), open chest.

Every game: voice line + golden pointer on start (`_say()` hard rule), no
timer, no fail, `probe_passive.gd` must clear NOTHING with zero input.

## 6. Audio requests (OGG, music ≥64kbps, loop-tagged)

- Cleaning-day music loop: light, bouncy, brushes-and-pizzicato feel,
  sits under the existing castle theme family.
- SFX: scrub squeak-squeak, soap bubble pops (small/big), sparkle chime
  (patch done), dust-bunny whoosh, imp giggle + pop (reuse opera pair),
  cobweb fwip, polish shine sting, cushion fwomp + wash-bubble burp,
  chandelier relight ta-daa (the big one — make it feel like the week's
  first Light).

## 7. Voice lines — NOT Codex scope

Family recordings, listed in STORY_DAYS.md §6 (help-me ask, cleaning
praise, gremlin-pop cheer, all-clean ta-da, week-opener). Ship against the
existing synth/fallback path until recordings land. Do not generate voice
audio.

## 8. Acceptance

Per the contract's scoring loop: deterministic generator in `tools/`,
Mobile-renderer near/mid/gameplay captures via the CI capture probes,
visual review gates every score above 2/5, two or three rejected
iterations is normal. Extra gates for this pass: a worst-case
grime-dressed Grand Hall capture must hold the transparent-overdraw
budget on the M11 profile, `probe_audit.gd` gains the Day-1 core-beat leg
when clean.gd lands (W4 — probe change is the explicit goal of that
commit), and every asset lands with its ASSET_LICENSES.md line.
