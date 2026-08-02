# Pearl Opera job #12 — Moonbeam Nursery

Date: 2026-08-01
Status: implemented; static/art gates pass locally; Godot runtime probes require
the configured CI runner when no local Godot binary is available.

## Outcome

Nursery Nurse is the twelfth displayed Roshan career. Roshan and Nurse Faron
work as a team: wash hands, catch five gently falling babies, feed them, burp
them, and tuck them into cribs. There is no opponent and no fail state. Pop Star
moves to displayed job #13; its original save bit and every earlier bit remain
unchanged.

The old Doctor career is now explicitly **Stuffie Surgeon**. Its plush-patient,
X-ray, cast, and bandage mechanics remain the variation of the existing Doctor
engine. Nursery Nurse never uses those modes, props, actor art, or competitive
win language.

## Existing-code and trope audit

| Area audited | Existing contract retained | Nursery-specific decision |
| --- | --- | --- |
| `scripts/opera_house.gd` | career configs, three floors, boss gating, stable star bitmask | append act index 15 but place it fourth on the five-card Grand Gallery, making it displayed job #12 without shifting old bits |
| `scripts/opera_lobby_2d.gd` | direct picture-first cards, no navigation/read gate | retain four cards on floors 1–2; responsive five-card layout on floor 3; finale requires all five floor shows |
| `scripts/opera_career_world_2d.gd` | short practice beat, final performance pacing, spoken prompt per phase, one-finger gestures, graded curtain call | Faron remains visible from the first beat; competition director runs as a cooperative team score |
| `scripts/opera_competition.gd` | 72–104 second career par-time band and applause tiers | use the established upper-band 104-second pace; complete both partner bars together and never say Roshan beat Faron |
| `scripts/games/dolls.gd` | live-input memory, no passive catch, safe pillows, Faron miss cue, slower/nearer mercy drops | expand from three to five catches, introduce two simultaneous fallers after two catches, keep all safety/mercy behavior |
| `scripts/save_state.gd` | additive/defaulted save migration and no removed keys | widen only the accepted ranges to 16 stars / `0xffff`; old bits 0–14 retain exact meaning |
| Opera probes/catalog | every career, lobby gate, stage, lifecycle, living-world entry | update counts/order and add focused no-passive/no-fail/cooperative nursery coverage |

The protected sources `assets/characters/friends/mama_baby.png`,
`assets/book/baby_doll.png`, `baby_doll2.png`, and `baby_doll3.png` were inventoried
and used only as identity/age references. `assets/book/nursery_bg.jpg` is portrait
and below the runtime background coverage requirement; the nursery room is
therefore a scalable code-native set. Full generated-art provenance is in
`assets_src/concepts/opera_nursery_2026-08-01/GENERATED_ART.md`.

The existing Dolls client itself cannot be embedded unchanged: it deliberately
builds the real 3D player, side-on camera and `SideScrollStage`, while shipping
Opera careers are pure Canvas worlds with no 3D children. Nursery therefore
reuses its tested behavioral contract and timing constants in a Canvas-native
phase, rather than silently pulling a second camera/player stack into Opera.


## Player-facing pacing
| Beat | Existing Opera grammar | Goal and child-readable feedback |
| --- | --- | --- |
| Wash hands | hold practice before the scored finale | 2.0 hold units; basin, bubbles, persistent pointer and spoken prompt |
| Catch babies | expanded Dolls falling-object verb | five catches; one faller initially, then up to two; three authored baby sprites; every miss lands on pillows and returns safely |
| Feed | hold | 4.2 hold units; bottle tableau, Roshan/Faron acting and spoken prompt |
| Burp | broad timing window | three gentle pats; baby/hand tableau; off-beat input still advances a little |
| Bedtime | swipe | 3.0 swipe units; three crib/blanket tableaux and a downward tuck arrow |
| Curtain call | existing graded audience beat | team score and “THE BABIES ARE COZY!”; warm cheers through standing ovation, never a loss |

`FINALE_START["nursery"] == 1`, so handwashing remains the calm unscored
orientation beat and the catch/feed/burp/bed span uses the normal Opera audience
and timing system. The 104-second par matches the longest established care-job
pace rather than introducing a new timing model.

## Art and performance decisions

- Generated only the three missing packages: Nursery Nurse Roshan, Nurse Faron,
  and a three-baby isolated sheet. Deterministic runtime derivatives are
  512×512 actors and 320×320 babies.
- Reused the Opera Canvas framework and code-native set drawing. No new light,
  physics body, full-screen alpha plate, or undersized raster background is
  introduced.
- The nursery palette, moon mobile, bottle shelves, rounded cribs and pillows
  distinguish it from Stuffie Surgeon's teal clinic, X-ray and cast language.
- Runtime art validation requires transparent corners, plausible coverage and
  zero material green-key residue. Hashes and derivation are recorded beside
  the sources.

## Blocking checks

- `python tools/prepare_opera_nursery_art.py --check-only`
- `python -m gdtoolkit.parser` on every changed GDScript
- `python tools/lint_inference.py` on every changed GDScript
- `scripts/probe_opera.gd` for stable order, doors, boss gating and full
  completion
- `scripts/probe_opera_2d.gd` for all thirteen career worlds and five-card floor
- `scripts/probe_opera_nursery.gd` for no passive catches, pillow-safe mercy,
  all care verbs, Faron partnership, and cooperative curtain call
- `scripts/probe_living_world.gd` for the sixteenth stable act entry

The cinematic full-frame validator does not apply: no authored cinematic frame
was created or changed.
