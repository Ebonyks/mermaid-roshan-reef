# Codex — building the next generation of opera objects

**Supersedes `CODEX_ART_WORKORDER_2026-07-25.md`** for the twelve career acts.
That document was a hand-typed prop list. It went stale in under a day, because
the acts were redesigned underneath it (see `OPERA_ACT_REDESIGN_2026-07-25.md`)
and nobody retyped it. This document does not list props. It describes **how an
object is constructed**, and points at a file that is regenerated from the game
code and always tells the truth about *which* objects are needed.

## The feedback loop

```
  game code (OperaAct beats, OperaHouse.ACTS)
        │
        │  $GODOT --headless -s scripts/probe_art_manifest.gd
        ▼
  audit/opera_art_manifest.json     ← the single source of truth
        │  + a 16-char fingerprint
        ▼
  codex reads the diff, redesigns only what moved
        │
        ▼
  .glb dropped at the manifest's own `path`, states as child nodes
        │
        ▼
  probe suite (scripts/ci.sh) → green → next loop
```

The manifest is **generated, never written by hand**. It is emitted by
`scripts/probe_art_manifest.gd`, a generator (not a gate — it never prints
FAIL), and published by the probes workflow as the `opera-art-manifest`
artifact on every push, so the newest one is always downloadable from the
Actions tab without a Godot install.

### The fingerprint is the whole point

The manifest's last field is a 16-character digest of everything above it.

- **Fingerprint unchanged** → no act changed its beats, gestures or objects.
  Nothing needs redesigning. Do not re-cut art.
- **Fingerprint changed** → diff the two manifests. The diff *is* the work
  order. Objects that appear are new, objects whose `states` array grew need
  extra poses, objects that vanish were designed out — do not ship them.

Every time art is delivered, record the fingerprint it was built against in the
`ASSET_LICENSES.md` line. Then a future reviewer can tell at a glance whether a
shipped object predates a redesign.

### Reading the manifest

```jsonc
"chef": {
  "career": "Pastry Chef", "name": "The Great Cake Show",
  "engine": "cook",
  "rescues": "the farmers", "gift": "carrots",
  "uses_gift_for": "they go in the bowl — it becomes a carrot cake",
  "beats": [
    { "beat": "stir", "gesture": "circular drag",
      "objects": {
        "batter": { "states": ["loose","ribboning","thick","peaked"],
                    "path": "assets/opera/jobs/pastry_chef/opera_pastry_chef_batter.glb",
                    "exists": false } } }
  ]
}
```

- `beats` are **in play order**. An act is a chain; beat 1 art is seen first
  and sets the act's read.
- `gesture` is the contract. The art exists to make that gesture legible.
- `built` says whether a child can play that beat today. `false` means the
  beat is designed and specified but not yet playable — its art is still
  wanted, it just isn't what unblocks anything this week. **Sort by `built`
  first.** A `built: true` beat running on a toon primitive is a beat the
  child is looking at right now.
- `states` are the visual states the finger drives. **Every state in that array
  must exist as a togglable child node.** A missing state is a dead beat.
- `path` is where the file goes. Not "somewhere like this" — exactly this. The
  loader builds it from the same rule.
- `exists: false` means the game currently falls back to a toon primitive.
- `rescues` / `gift` / `uses_gift_for` are the act's story rhythm. Every act
  opens with freeing someone from imps; they hand over a thing; the act is made
  of that thing. The gift object must be recognisably the *same object* in the
  rescue beat and in the beat that consumes it — same carrot, same paint pot.

**Current state of the world:** 12 acts, 55 beats (47 playable today, 8
specified and pending), 139 objects, 300 states. *(These figures are a
snapshot; the `ARTMANIFEST|` line on the newest probes run is the authority.)* **136 objects do not exist
yet.** The three that do — `pastry_chef_bowl`, `pastry_chef_oven`,
`astronaut_rocket` — are single-pose gen1 models with no state children, so
they are rebuilds, not skips.

---

## The construction contract

Anything delivered against the manifest must satisfy all of this. This section
is the actual "how to build one".

### 1. Naming and placement

```
assets/opera/jobs/<jobdir>/opera_<jobdir>_<object>.glb
```

`<jobdir>` and `<object>` come verbatim from the manifest's `path`. Note the
chef's folder is `pastry_chef` while its costume key is `chef` — always take
the path from the manifest, never reconstruct it from the act name.

### 2. States are child nodes, not separate files

One object = one `.glb`. Inside it, one child node per state, named
`State<Name>` in PascalCase from the manifest's snake_case:

```
opera_pastry_chef_batter.glb
└── Batter                (root, always visible: the bowl's contents volume)
    ├── StateLoose        \
    ├── StateRibboning     |  exactly one visible at a time,
    ├── StateThick         |  toggled by the game
    └── StatePeaked       /
```

- `elbow_ne` → `StateElbowNe`. `layer1` → `StateLayer1`.
- Ship every state in the array. Four names, four nodes.
- Extra child nodes that are not states are fine (`Shadow`, `Sparkle`), as long
  as no name collides with `State*`.
- All states share the object's origin. The game swaps visibility only — it
  does not re-place, re-scale or re-orient them.

### 3. Pivot and scale

- Origin at the **contact point**: where the object meets the deck for props,
  the grip for held things, the centre for things that spin.
- +Z is toward the audience (the camera). +Y up. Author facing the camera.
- Real scale in metres, Roshan ≈ 1.1 m tall. Do not export at 100×.
- Anything the finger targets must be at least **0.55 m across** on its
  narrowest readable axis. Four-year-old, phone screen, imprecise finger. When
  in doubt make it bigger; the difficulty in this game is speed and quantity,
  never precision.

### 4. Budget (mobile renderer, 3–4-year-old Android phone)

- ≤ 900 triangles per state. A hero object may reach 1,500 across all states.
- One material per object where possible; four hard cap.
- Textures ≤ 1024 px longest side **or** power-of-two. VRAM compression only if
  power-of-two — a non-power-of-two texture with compress mode 2 **deadlocks
  the headless importer**, which takes CI down, not just your asset.
- **No lights.** None. Glow is emissive material only. The act-one node budget
  is hard (`_descendants(act) < 170`); an object that explodes into 40 nodes
  will be rejected even if it looks perfect.
- No skeletons, no animation tracks. Motion is code-driven tween on the root.

### 5. Style (unchanged, binding)

Pastel toy playset: rounded geometry, toon materials, navy/purple outlines,
aqua/lavender shadows, oversized child-readable props. CC0 sources or original,
restyled through the `_toonify` pastel pipeline. Wind Waker is a *rendering*
reference only — no Zelda assets, symbols, UI, music or character designs.
Never modify book art, family voices, or friend cutouts.

Match the act's existing stage palette (`deck` / `pillar` / `beam` / `backdrop`
/ `wing` / `crest` / `pool` in `OperaAct.STAGE_SETS`). Props read **against**
their stage: the detective's clue glint must be warm because its room is dark
indigo; the astronaut's pipe pieces must be high-contrast because the launch
pad is pale.

### 6. Licensing

One line in `ASSET_LICENSES.md` per asset — source, license, URL,
modifications — **in the same commit that adds the asset**, plus the manifest
fingerprint it was built against.

---

## How a gesture decides what the art must do

This is the rule that generated every `states` array. Use it when a new beat
appears in the manifest and you have to invent the object list yourself.

| Gesture | What the art owes the child | Minimum states |
| --- | --- | --- |
| tap | a before and an after, plus a burst | 2 + effect |
| timed tap | a *visible ramp* the child reads to know when — the cake browning, the lamp pulsing | 3+ across the ramp |
| hold | a filling meter that is part of the object, not a floating UI bar | empty / filling / full (+ an overfill giggle) |
| drag | the object must follow the finger and look **held** — tilt, a lifted shadow | idle / held / settled |
| drag-and-drop | the target must show hover, accept and reject, all without words | loose / carried / placed, target: idle / hover / accept / reject |
| circular drag | a **rotating decal or swirl**. This is the only feedback that says the *circle* worked, not the tap | the material changing through the turns |
| trace | a dotted guide ahead of the finger and a solid line behind it | guide / following / complete |
| scrub | a shake, and falling particles that prove the back-and-forth | still / shaking + a falling element |
| charge-and-release | a drawn-back pose and an aim arc | slack / drawn + flight / landed |
| rotational drag | the twist must be visible in the silhouette | loose / twisting / sealed |
| swipe up / down | the thing swiped and the thing avoided, both huge | incoming / passed |
| rhythm tap | an off-beat and an on-beat pose, high contrast; the beat must be readable with the sound off | off / pulse / hit |
| track + tap | a trail that survives the motion so the eye can follow | swirling + a reveal burst |
| steering | livery and lap pips only — the kart engine owns the rest | 1 |
| walk / carry | the carried thing visible in arms from the game camera | in_arms |

Two rules on top:

1. **No gesture appears twice in one act.** If two beats want the same verb,
   one of them is wrong — flag it rather than making the art twice.
2. **No fail states.** There is no "wrong" pose, no red X, no broken object. A
   miss is a giggle, a slide-back, a puff, a leak or a pause. `reject` means
   "hmm?" and slides home, never "you lost". Never author a sad, broken or
   scolding state.

---

## Tier 1 — build these first

One or two objects per act carry the gesture. If only these exist, every act
still reads. They are also the objects a toon primitive fallback fails hardest.

| Act | Object | Why it is tier 1 |
| --- | --- | --- |
| Pastry Chef | `batter` (4 states) + a **stir swirl** decal | the child looks at the bowl for ~40 s; the swirl is the only proof the circle worked |
| Detective | `clue_glint`, `dwell_ring` | clues are invisible outside the lens, and the hold is invisible without the ring |
| Ballerina | `ribbon_arc` (guide/traced) | the trace has no shape without its guide |
| Candy Maker | `chute` (idle/hover/accept/reject) + `collar_ring` colours | the whole sort is colour-matching; the collar is what gets matched |
| Doctor | `bone` (sound/cracked/named) + `crack_pulse` | the diagnosis beat is *reading a picture*; if the crack is not obvious there is nothing to read |
| Farmer | `sling_pull` (slack/drawn) + `aim_dot` arc | charge-and-release is unlearnable without a drawn-back pose |
| Boxer | `beat_lamp` (off/pulse) | the rhythm must be playable with the phone muted |
| Magician | `knotted_rope` (knotted/loosening/straight) | the pull-apart drag is a silhouette change or it is nothing |
| Painter | `brush_stamp` + `loaded_brush` colours | the paint texture is stamped per drag sample; a bad stamp ruins every stroke |
| Astronaut | `pipe_piece` (6 shapes) + `bubble_flow` | six shapes must be distinguishable at thumb size, at a glance, under a burning fuse |
| Racecar | `opera_kart` livery | the only bespoke art in a borrowed engine |
| Pop Star | `arrow_glyph` (4) + `hold_note_tail` | direction must read instantly at speed |

Tier 2 is everything else in the manifest. Tier 3 is backgrounds — the twelve
stages already exist as toon primitives in `STAGE_SETS` and are **replaced in
place**: same positions, same colour roles. Do not re-place them, and keep all
scenery in the envelope (`|x| ≥ 19`, `z ≤ -15.5`, or `z ≥ 17`) — inside that
box it collides with gameplay props.

---

## Handback checklist

Before a batch is handed back:

- [ ] Every file sits at the manifest's exact `path`.
- [ ] Every state in the manifest's `states` array exists as a `State<Name>`
      child, and exactly one is visible in the exported default.
- [ ] Origin at the contact point, real metres, ≥ 0.55 m on the target axis.
- [ ] ≤ 900 tris/state, ≤ 4 materials, textures ≤ 1024 or POT, **no lights**,
      no skeletons, no animation tracks.
- [ ] No state depicts failure, damage-as-punishment, or a scolding face.
- [ ] `ASSET_LICENSES.md` line added in the same commit, with the manifest
      fingerprint built against.
- [ ] `$GODOT --headless --import .` completes (watch for the NPOT deadlock),
      then `scripts/ci.sh` is green.

## Running the loop by hand

```sh
GODOT=./Godot_v4.4.1-stable_linux.x86_64
$GODOT --headless -s scripts/probe_art_manifest.gd
# → audit/opera_art_manifest.json
#   ARTMANIFEST|acts=12 objects=139 states=300 missing=136 fingerprint=…
git diff -- audit/opera_art_manifest.json     # this diff is the work order
```

No Godot handy? Download the `opera-art-manifest` artifact from the newest
probes run on the Actions tab.

## When the game changes, this document does not

If an act gains a beat, the manifest gains the beat and the fingerprint moves.
Nothing here needs editing — the rules above still generate the right art from
the new beat. The only reason to touch this file is if the *rules* change: a
new gesture class, a new budget, a new style decision from the owner.
