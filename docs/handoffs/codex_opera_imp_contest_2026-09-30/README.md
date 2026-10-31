# Codex handoff: Opera imp contests (2026-09-30)

- **From:** Claude. Written design, analysis and specification only: no game changes and no
  images.
- **To:** Codex, for implementation, including any image or voice generation it needs.
- **Owner:** approves the open decisions and accepts the result on the phone.

**Status:**
- `PROPOSED / CANDIDATE`. Publication is not creative acceptance.
- **Revision 5 (2026-10-04)** adds the owner's fifth decision (OD-E):
  - the Teacher's imp game cannot be lost and is always silly;
  - the Chef's imp sneaks gross things into her recipe, and noisy imps try to wake the
    Nursery's sleeping babies: two new defense contests;
  - the Geologist races the imp for the same geode;
  - only the contest restarts when he wins, and after two failures he slows down radically.
  - Any optional new imp costume follows the owner's 2026-10-03 animation-workflow policy in
    `AGENTS.md` (`DL-MOT-14` to `DL-MOT-16`), added when revision 5 was merged with `dev`.
- **Revision 4** (`1fbcc9db`) added OD-D: silly questions such as "which smells the worst?"
  and sillier imp lines.
- **Revision 3** (`86732a47`) folded in the Day Two art review's corrections: reuse only the
  current full-tail and borderless art routes, and show the imp touching his own job object
  ([CONTEST_DESIGN.md §4.16](CONTEST_DESIGN.md)).
- **Revision 2** (`df01b7ce`) added OD-C, the inverted Teacher contest. Revision 1 was
  `7ec82d46`.
- No visual, device, child or owner acceptance is claimed.
- Implementation follows `CLAUDE.md`, `AGENTS.md` and the master-audit development contract:
  impact records, gates, CI, then integration into `dev`.

**Evidence baseline:** `dev` at `55032e88936b22723fd9af5282c61ba6696b3d43` (2026-09-29).

**Written material only.** Following the owner's 2026-09-30 rule in `CLAUDE.md` ("Codex
handoffs: Claude writes, Codex builds images"), this packet contains no mock-ups, boards or
other images. Each contest is described in words: who stands where, which existing pose file
and art, and what the child sees change ([CONTEST_DESIGN.md §6](CONTEST_DESIGN.md)). Codex
builds any image the work needs.

## Owner direction

- **OD-A:** "No, I think imp comes in during the final act, there should be a contest at
  the end that reflects part of the skill of the job that's a challenge against the imp"
- **OD-B:** "If imp wins, the game restarts immediately afterwards."
- **OD-C:** "The teacher should have an imp, but the game inverts, he teaches information
  that's wrong and it's your job to figure it out, which beats the imp. Similar
  educational type games"
- **OD-D:** "Lean into silly humor here, questions like, which smells the worst, farts,
  garbage, old diapers or rotten cheese?"
- **OD-E (2026-10-04):** "The imp teacher games can't be lost by design, and should always
  be silly. Imp maybe tries to mess up your recipes and put gross things in the food?
  Geologist should be competing for time with Roshan for the same goal. You should stop
  the imps from being too noisy when the babies are sleeping. Imp just restarts contest at
  end, after two failures, imp should radically slow down."

**OD-E settles** the restart scope (contest only), the educational scope (the inverted
format is the Teacher's alone), the silly scope (every Teacher round is silly), the
rematch mercy and the Nursery.

**To confirm with the owner:** the recipe idea is applied to the Chef by default (YUCKY
RECIPE replaces the topping race). If it was meant for the Teacher, the Chef keeps the
topping race and the Teacher gains a silly recipe round instead. See
[CONTEST_DESIGN.md §1](CONTEST_DESIGN.md) and §7.2.

## The design in brief

**The contest**
- Each career's costumed imp stays hidden until the final act, then runs in and watches her
  work.
- The final act ends in one head-to-head contest built from the job's own verb, at the real
  object she walked to. Four kinds:
  - **races:** finding sparkles with rival magnifiers, a twirl-off, a bandage race, opening
    the same geode first (Geologist), and more;
  - **points duels:** a title bout, a hat duel, a sing-off;
  - **defense (new):** keeping gross things off her cake (Chef) and noisy imps away from the
    sleeping babies (Nursery);
  - **the inverted Teacher game**, which cannot be lost.
- Wordless pearl rows show who is ahead.

**How he behaves**
- He freezes when she stops, so zero input never decides anything. In the defense contests
  every hazard is announced first, removed with one tap, and held still while she is idle.
- He makes one funny mistake per attempt, using his existing recorded "copy" line. That is
  her comeback moment.

**Defense contests (OD-E)**
- **Chef, YUCKY RECIPE:** she puts toppings on her cake while the chef-imp lobs a stinky
  sock, a wiggly worm, a fish skeleton or an old boot onto it. One tap flicks each one back
  to bonk him. He wins only if three gross things sit on the cake at once. It is built after
  the Chef repair the owner asked for on 2026-10-03.
- **Nursery, QUIET TIME:** after BEDTIME, plain mischief and captain imps tiptoe up to the
  cribs with a drum, a trumpet, cymbals or a squeaky duck. She taps each one to shush him
  before he makes his noise. Three noises would wake the babies; Faron stays at her side.

**The Geologist (OD-E)**
- **GEODE RACE:** one geode, two diggers. She taps the seam spots and pulls it open, as in
  GEODE today; the field-guide imp chips purple marks on its other side. Whoever opens it
  first gets the crystals.

**The Teacher (OD-C, OD-D, OD-E)**
- **IMP'S LESSON:** the imp becomes the teacher at the lesson board. Four rounds, every one
  silly: silly questions alternate with silly lessons.
  - The first is the owner's own: "Which smells the worst? Farts, garbage, old diapers, or
    rotten cheese?" He picks a pretty rose; any stinky answer makes him cry "Pee-yew!" and
    faint. Seven more questions follow the same pattern.
  - In the silly lessons he puts a sock or a banana in the pattern, counts his own nose,
    plonks a banana on a wrong sum, or calls a pizza slice a shape's twin. She finds the
    right answer, counting pearls where needed.
- **It cannot be lost:** a wrong pick only earns his silly gloat, then the golden help shows
  the answer. Every round ends with her pearl, and he never scores.
- **The joke is always on the imp or the thing**, never on the child.

**Winning and losing**
- **She wins:** he staggers and flops with his existing "bop" line; her cheer tier becomes
  audible and visible. Then an existing flourish or the curtain call follows.
- **He wins** (never in the Teacher's game): a victory hop of at most 2 s, "I won! I won!
  Let's play again!", and only the contest resets, at once. She stays where she is. The
  first restart is the same; after two failures he slows down radically: races at 0.4 of
  his pace, half-speed cues, far fewer hazards, the Racer at half speed.

**Reuse**
- No new imp art is needed to ship: all 178 imp pose files would appear, against 41 today.
  The Nursery uses the plain mischief and captain imps, which no shipping phase shows today;
  the Teacher borrows the mischief imp until an optional teacher costume is approved.
- 39 of the 56 existing imp lines would play, against 2 today.
- 77 short new lines are needed (61 imp, 16 Roshan; 32 of them for the silly questions).
- One shared set of up to 47 cartoon picture icons serves the silly questions, the silly
  lessons, the Chef's gross things and the Nursery's noisy toys. Codex makes it after
  checking existing art (a banana and a rubber duck already exist). You approve the first
  five, for the smell question.
- The Nursery's noises reuse existing gentle sounds, including the castle's duck squeak.

## What is in this folder

| Path | What it is |
|---|---|
| [CONTEST_DESIGN.md](CONTEST_DESIGN.md) | The specification: contract C1 to C16, shared mechanics (including the inverted and defense contests and the mercy table), code integration, the twelve costumed contests plus the Teacher, Geologist and Nursery, owner decisions, retirements, tests, governance, work order and acceptance |
| [CURRENT_STATE_ANALYSIS.md](CURRENT_STATE_ANALYSIS.md) | The formula today, strengths, weaknesses, findings H1 to H10 with code anchors, and imp art and voice use in numbers |
| [data/contest_spec.json](data/contest_spec.json) | The same contest design in machine-readable form |
| [data/imp_art_inventory.json](data/imp_art_inventory.json) | Every imp pose file: path, bytes, SHA-256, size, shown today (with code evidence) and planned contest roles |
| [data/imp_voice_inventory.json](data/imp_voice_inventory.json) | Every imp line: text, hashes, routing today and planned use; plus the new lines with exact texts |
| [tools/build_packet_data.py](tools/build_packet_data.py) | Text-only script that regenerates the two inventories and checks the manifest (`--check`) |
| [MANIFEST.json](MANIFEST.json) | SHA-256 of every file in this folder |

Nothing in this folder is loaded by the game; a `.gdignore` keeps Godot from importing it.

## Work queue for Codex

The full table with gates is in [CONTEST_DESIGN.md §11](CONTEST_DESIGN.md).

1. **W0:** owner answers on the recipe idea, the costumes, the silly icon style and the Hall
   stage-long race. Defaults apply if these are unanswered.
2. **W1:** the `OperaImpContest` logic class (race, points, defense and inverted archetypes,
   and the mercy table), the additive `opera_phase_checkpoints` save key, the Chapter 2
   opt-out and the new probe's logic checks.
3. **W2 and W3:** shared presentation, then one pilot per archetype on the phone:
   - Detective (race; retires the harsh timed retry, H1);
   - Magician (points; fixes shuffle taps, H9);
   - Nursery QUIET TIME (defense, on the plain imps).
4. **W4 to W6:** surface contracts, the remaining contests (including the Geologist's race,
   and the Chef once its repair has landed), then Boxer points and the Racer finish rule.
5. **W6b:** the Teacher's IMP'S LESSON, piloted with the smell question once its five icons
   are approved.
6. **W7:** the new voice lines through the existing filler pipeline, with licences and
   audio-ledger rows; the shared silly icon set; any teacher or geologist imp costume the
   owner approves.
7. **W8:** fix the balance probe (H4), tune `base_seconds` and the hazard timings, update the
   canon counts (H8), and merge to `dev` when CI is green.

## Owner decisions still open

These are covered in [CONTEST_DESIGN.md §7.2](CONTEST_DESIGN.md).

- **The recipe idea:** the Chef's YUCKY RECIPE (default), or a silly recipe round for the
  Teacher.
- **Imp costumes:** a new teacher imp (recommended) and optionally a geologist imp, or keep
  the stand-ins.
- **Silly icons:** approve the style of the first five pictures (the smell question).
- **Hall stage-long race:** retire it (recommended), or keep it as no-loss.

## Governance recorded with this handoff

**Canon changes**
- **`DL-INT-14`** is added to
  [design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md](../../../design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md)
  as the owner-decided target contract. Implementation is pending.
- Revisions 2, 4 and 5 amend `DL-INT-14`: the inverted Teacher format, the humor rule, and
  OD-E (the Teacher cannot lose, defense contests, the Geologist's race, the radical
  slowdown).
- Pointer sentences are added to `DL-INT-08`, `DL-INT-09` and `DL-INT-10`.
- The "Competition is scoped" bullet in `design/01_GAME_DESIGN.md` is amended, with pointers
  on its Geologist and Nursery bullets.
- Notes are added to the master index and the master-audit planning entry.
- Ledger rows are added for this packet's documents.

**The CLAUDE.md role rule**
- It records the owner's 2026-09-30 decision that Claude hands Codex written descriptions
  and builds no images. Its ledger row is updated to match.

**Impact records:**
- Revision 1:
  [design/audit_impacts/codex-opera-imp-contest-handoff-20260930.json](../../../design/audit_impacts/codex-opera-imp-contest-handoff-20260930.json).
- Revision 2:
  [design/audit_impacts/codex-opera-imp-contest-handoff-rev2-20260930.json](../../../design/audit_impacts/codex-opera-imp-contest-handoff-rev2-20260930.json).
- Revision 3:
  [design/audit_impacts/codex-opera-imp-contest-handoff-rev3-20260930.json](../../../design/audit_impacts/codex-opera-imp-contest-handoff-rev3-20260930.json).
- Revision 4:
  [design/audit_impacts/codex-opera-imp-contest-handoff-rev4-20260930.json](../../../design/audit_impacts/codex-opera-imp-contest-handoff-rev4-20260930.json).
- Revision 5:
  [design/audit_impacts/codex-opera-imp-contest-handoff-rev5-20261004.json](../../../design/audit_impacts/codex-opera-imp-contest-handoff-rev5-20261004.json).

## Checking this packet

```sh
python3 -B docs/handoffs/codex_opera_imp_contest_2026-09-30/tools/build_packet_data.py --check
```

The check prints `PACKET_CHECK|OK` when every file matches `MANIFEST.json`, the inventories
regenerate unchanged, and the folder contains no image.
