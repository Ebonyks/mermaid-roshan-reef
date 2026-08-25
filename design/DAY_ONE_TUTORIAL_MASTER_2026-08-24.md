# Day One Tutorial Master — design and implementation audit

Date: 2026-08-24

Branch: `codex/tutorial-master`
Authority: `audit/MASTER_AUDIT_2026-08-09.md`,
`design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md`, and repository `AGENTS.md`.

## Decision

Day One teaches one stable grammar: **look at the glowing real object, then use
one finger to tap it or sweep the rainbow tool across it**. The lesson is a
short performed gesture over the live room, not a reading screen. Every
segment plays automatically once, and one press anywhere skips exactly that
segment without touching the activity below it.

The rainbow brush remains the best shared teaching tool in the current game.
It has a large authored silhouette, high warm/cool contrast, a continuous
rainbow trail that exposes direction and distance, and it works for both a
stationary tap and a deliberate sweep. The magnifier precedes it because a
search gesture is calm, non-hostile, and lets the child learn finger-to-object
correspondence before any dust bunny is framed as an opponent.

## Existing-material audit

| Existing material | Before | Strong evidence | Master-design gap before this branch |
|---|---:|---|---|
| Bathroom | 1.0/5 | Physical room and approved magnifier asset existed | Day One completed a placeholder; no live search, truthful discoveries, restored partial progress, or first-entry lesson |
| Dirty Art Room | 2.8/5 | Broad targets, moving pointer, spoken prompts, approved rainbow brush | Counter grime accepted a tap despite saying “scrub”; no performed swipe demonstration or brush trail |
| Stuffie Room | 2.0/5 | Authored Baby Eagle rescue, two visible dust bunnies, large local targets | Existing instruction taught swim/contact; no Day One tap-plus-swipe activity, no separate wake/clean states |
| Pool Room | 4.0/5 | Best existing Day One activity: real skimmer drag, waterfall scrub, seahorse taps, truthful scene repair and restored progress | Three verbs arrived without a first-entry performed gesture; skip/lifecycle ownership was absent |
| Bunny Boss | 3.2/5 tutorial / 3.0/5 audited arena | Ghost-hand choreography, flashing vulnerability, no-loss mercy ramp, strong feedback | Existing combat tutorial is spatial migration debt, is not one-press skippable, and the boss accepted tap only; swipe was demonstrated nowhere |

These are design-review scores, not owner acceptance. `DL-VIS-07` reserves 5/5
for accepted runtime evidence.

## Point-by-point age-four standard

| Requirement | Selected language | Implementation evidence |
|---|---|---|
| Non-reader (`DL-AGE-01`) | Moving ghost hand, glowing ring, recognizable tool, short spoken/caption support | Transparent Canvas overlay performs the exact tap or sweep over the visible room |
| One finger (`DL-AGE-02`, `DL-UI-04`) | One owned touch from press through release; second touches ignored | Overlay and new activities track a single touch id and cancel stale ownership |
| No punishment (`DL-AGE-03`) | Wrong input produces a local wiggle/ripple and leaves the target ready | No timer, lives, loss screen, reset, or lost collected object was added |
| Demo cannot win (`DL-AGE-04`, `DL-INT-06`) | Demonstration draws its own tool/hand but never calls activity progress | Overlay owns no reward, room completion, or activity callback |
| Intentional play is faster (`DL-AGE-05`) | Real target intersection and minimum sweep distance advance immediately | Bathroom reveals only under the lens; art needs 42 source pixels; stuffie needs wake plus a 90-pixel crossing swipe |
| Short lifecycle (`DL-AGE-06`, `DL-SAVE-03`) | One action per 3.15-second segment; automatic advance; any press skips one segment | Reasoned world-control gate, focus/back cancellation, teardown, and first-entry save ownership are explicit |
| Immediate response (`DL-AGE-07`, `DL-INT-02`) | Ring/trail/tool follows the finger; a real object reveals, cleans, or flinches | Bathroom reveal, rainbow art dabs, stuffie wake/clean states, and boss vulnerable-hit path are truthful |
| Large local geometry (`DL-UI-03`, `DL-INT-01`, `DL-INT-04`) | At least 110-pixel targets/bands tied to visible objects | Magnifier radius 82, stuffie targets 190x170 with 110-pixel sweep band, existing pool sockets, generous boss screen circle |
| Stable visual language (`DL-VIS-01`–`05`) | Warm gold focus, aqua/lavender feedback, rounded rings, approved painted tools | No new generated art and no protected source modification; approved assets are reused non-destructively |
| Save compatibility (`DL-SAVE-01`) | Add-only `day_one_tutorial_seen` plus bathroom/stuffie partial masks | Old completed-room membership is preserved while the route changes to the new order |

## Comparable preschool patterns

- Sago Mini Bug Builder invites a tap with a wiggling egg, then lets the child
  draw directly with a finger and introduces a sponge as the next visible
  action. This supports object-led invitation and performed direct
  manipulation rather than a modal instruction page:
  <https://sagomini.com/article/bug-builder-letter-to-parents/>.
- Sago Mini Monsters uses tap-to-color, finger drawing, dragging parts, and a
  toothbrush scrub in one forgiving play chain. This supports reusing one
  visible verb at a time and making the result immediate:
  <https://sagomini.com/article/monsters-letter-to-parents/>.
- Android's ABCmouse case study says prereaders need visual/audio guidance,
  large forgiving targets, familiar character guidance, and clear progress:
  <https://developer.android.com/design/ui/gallery/reading/abcmouse>.
- LEGO DUPLO/StoryToys describes frequent preschool playtesting and a positive
  learning-through-play approach. That supports treating device/child review
  as an acceptance gate, not inferring it from a desktop probe:
  <https://www.lego.com/cdn/cs/set/assets/blt7f52a3f525787f33/bits_n_bricks_s03e36_feature_and_transcript.pdf>.

The reusable pattern is therefore: **visible invitation -> performed gesture
on the real target -> child action -> immediate truthful response -> next
single verb**.

## Five-event implementation

| Order | First-entry demonstration | Live child contract | Persistence |
|---:|---|---|---|
| 1 Bathroom | Tap the centered magnifier; sweep it across the three authored supply positions | Drag the lens to reveal the magic brush, skimmer, and waterfall scrubber | 3-bit supply mask; room completes only after all three |
| 2 Dirty Art Room | Tap the real loose-supply socket; sweep the rainbow brush across the left grime socket | Tap four visible supplies, then swipe each grime patch before opening the desk | Existing art dictionaries; tap alone no longer cleans grime |
| 3 Stuffie Room | Tap the left pinning bunny to wake it; sweep the brush across that same bunny | Each of the two authored bunnies requires tap-to-wake followed by a crossing swipe | 2-bit cleanup mask; completion reuses Baby Eagle rescue clears |
| 4 Pool Room | Sweep skimmer, scrub waterfall, tap seahorse | Existing three-stage activity remains the live authority | Existing skimmer/waterfall/seahorse progress fields |
| 5 Bunny Boss | Watch the flash and tap three times; alternative rainbow sweep is shown | Tap or a 90-pixel crossing swipe only counts during the existing vulnerable flash | Existing boss state; tutorial seen flag is independent of rewards |

The order is now bathroom -> art -> stuffie -> pool -> boss. Completion
membership, rather than an obsolete prefix, is preserved when older saves used
bathroom -> pool -> stuffie -> art.

## Sol acceptance review

| Tutorial slice | Interaction design | Lifecycle/save | Visual fit | Tutorial-specific result |
|---|---:|---:|---:|---:|
| Bathroom | 4.7 | 4.7 | 4.6 | **4.7/5 candidate** |
| Dirty Art Room | 4.7 | 4.6 | 4.7 | **4.7/5 candidate** |
| Stuffie Room | 4.6 | 4.6 | 4.6 | **4.6/5 candidate** |
| Pool Room | 4.7 | 4.6 | 4.6 | **4.6/5 candidate** |
| Bunny Boss tutorial layer | 4.5 | 4.6 | 4.5 | **4.5/5 candidate** |

All tutorial-specific candidates meet the requested 4.5 threshold after the
art swipe, stuffie activity, boss swipe, automatic segment progression, exact
target alignment, and tap-through fixes. This does **not** reclassify the
underlying legacy boss arena or game-wide 3D inventory; the master audit stays
`UNSATISFIED` until its separate strict-2D work is complete.

`FIXED_PENDING_VERIFICATION` is the highest justified state. Required closure
still includes exact Godot 4.7.1 runtime probes, Mobile/Speedy capture on the
Lenovo Tab M11, a four-year-old play pass, owner visual acceptance, and exact
human voice recordings for the generic stuffie/pool and currently absent boss
event clips. Protected family voice assets were not altered or substituted.
