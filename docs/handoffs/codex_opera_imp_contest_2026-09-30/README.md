# Codex handoff: Opera imp contests (2026-09-30)

- **From:** Claude. Written design, analysis and specification only: no game changes and no
  images.
- **To:** Codex, for implementation, including any image or voice generation it needs.
- **Owner:** approves the open decisions and accepts the result on the phone.

**Status:**
- `PROPOSED / CANDIDATE`. Publication is not creative acceptance.
- **Revision 4 (2026-09-30)** adds the owner's fourth decision (OD-D): lean into silly
  humor, with silly questions like "which smells the worst?" and sillier imp lines.
- **Revision 3** (`86732a47`) folded in the Day Two art review's corrections: reuse only the
  current full-tail and borderless art routes, and show the imp touching his own job object
  ([CONTEST_DESIGN.md §4.16](CONTEST_DESIGN.md)).
- **Revision 2** (`df01b7ce`) added the owner's third decision (OD-C): a Teacher imp who
  teaches wrong things for the child to fix, applied to the learning careers. Revision 1
  was `7ec82d46`.
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

**To confirm with the owner:**
- **Restart scope:** this design restarts the *contest only*. Earlier activities, stars,
  pearls and saves are kept.
- **Educational scope:** "similar educational type games" is read as the Teacher's four
  lesson kinds plus the Geologist, the other learning career.
- **Silly questions:** they alternate with the math lessons rather than replacing them.

See [CONTEST_DESIGN.md §1](CONTEST_DESIGN.md), §7.2 and §7.4.

## The design in brief

**The contest**
- Each career's costumed imp stays hidden until the final act, then runs in and watches her
  work.
- The final act ends in one head-to-head contest built from the job's own verb, at the real
  object she walked to. Examples:
  - topping two cakes;
  - finding sparkles with rival magnifiers;
  - a twirl-off;
  - a bandage race;
  - a hat duel;
  - a sing-off.
- He works on his own small copy of the activity.
- Two wordless pearl rows show who is ahead.

**How he behaves**
- He freezes when she stops, so zero input never decides anything.
- He makes one funny mistake per attempt, using his existing recorded "copy" line. That is
  her comeback moment.

**Learning careers invert (OD-C)**
- **Teacher, IMP'S LESSON:** the imp becomes the teacher at the lesson board. He teaches
  pattern, counting, adding and matching lessons, each with one deliberate mistake, which he
  shows proudly. She finds the right answer, counting pearls where needed. Her correct first
  pick fixes his lesson and scores her point; a wrong first pick is his point, then the
  golden help shows the answer and she places it.
- **Geologist, FIELD GUIDE MIX-UP (pending confirmation):** the field-guide imp shows a
  fossil with one piece upside down, or three "same" rocks where one differs, and she taps
  the mistake.
- **No clock, and truth last:** every round ends with the right answer on the board, placed
  by her.

**Silly humor (OD-D)**
- **Silly questions** alternate with the Teacher's math lessons. The first is the owner's
  own: "Which smells the worst? Farts, garbage, old diapers, or rotten cheese?"
  - The imp proudly picks a pretty rose. Any stinky answer beats him: he sniffs it, cries
    "Pee-yew!" and faints. The fart card plays the game's existing fart sound.
  - Seven more follow the same pattern: loudest (he says a mouse), biggest (an ant),
    stickiest (a feather), coldest (the sun), slowest (a rocket), squishiest (a rock) and
    yuckiest to eat (a cupcake).
- **Every imp line gets sillier:** "One, two, three... eleventy-twelve!", "Two plus one
  makes... a banana!", "It's a dinosaur's belly button!"
- **The joke is always on the imp or the thing**, never on the child.

**Winning and losing**
- **She wins:** he staggers and flops with his existing "bop" line; her cheer tier becomes
  audible and visible. Then an existing flourish or the curtain call follows.
- **He wins:** a victory hop of at most 2 s, "I won! I won! Let's play again!", and the
  contest resets at once. She stays where she is, and he is slower each time.

**Reuse**
- No new art is needed to ship: 167 of the 178 imp pose files would appear, against 41
  today. The Teacher uses the plain mischief imp until an optional teacher costume is
  approved.
- 36 of the 56 existing imp lines would play, against 2 today (39 with Nursery option B).
- 67 short new lines are needed (32 of them for the silly questions): 9 more if the
  Geologist contest is confirmed, 2 more for Nursery option B.
- The silly questions need one new set of 40 cartoon picture icons, plus 3 for the
  Geologist's silly rocks. Codex makes them after checking existing art. You approve the
  first five, for the smell question.

## What is in this folder

| Path | What it is |
|---|---|
| [CONTEST_DESIGN.md](CONTEST_DESIGN.md) | The specification: contract C1 to C15, shared mechanics (including inverted contests), code integration, the twelve costumed contests plus the Teacher and Geologist, owner decisions, retirements, tests, governance, work order and acceptance |
| [CURRENT_STATE_ANALYSIS.md](CURRENT_STATE_ANALYSIS.md) | The formula today, strengths, weaknesses, findings H1 to H10 with code anchors, and imp art and voice use in numbers |
| [data/contest_spec.json](data/contest_spec.json) | The same contest design in machine-readable form |
| [data/imp_art_inventory.json](data/imp_art_inventory.json) | Every imp pose file: path, bytes, SHA-256, size, shown today (with code evidence) and planned contest roles |
| [data/imp_voice_inventory.json](data/imp_voice_inventory.json) | Every imp line: text, hashes, routing today and planned use; plus the new lines with exact texts |
| [tools/build_packet_data.py](tools/build_packet_data.py) | Text-only script that regenerates the two inventories and checks the manifest (`--check`) |
| [MANIFEST.json](MANIFEST.json) | SHA-256 of every file in this folder |

Nothing in this folder is loaded by the game; a `.gdignore` keeps Godot from importing it.

## Work queue for Codex

The full table with gates is in [CONTEST_DESIGN.md §11](CONTEST_DESIGN.md).

1. **W0:** owner answers on restart scope, the Hall stage-long race and rematch mercy.
   Defaults apply if these are unanswered.
2. **W1:** the `OperaImpContest` logic class, the additive `opera_phase_checkpoints` save key,
   the Chapter 2 opt-out and the new probe's logic checks.
3. **W2 and W3:** shared presentation, then three pilots on the phone:
   - Chef (tap race);
   - Detective (lens race; retires the harsh timed retry, H1);
   - Magician (points duel; fixes shuffle taps, H9).
4. **W4 to W6:** surface contracts, the remaining seven contests, then Boxer points and the
   Racer finish rule.
5. **W6b:** the inverted contests: the Teacher's IMP'S LESSON, then the Geologist's FIELD
   GUIDE MIX-UP once the owner confirms it.
6. **W7:** the new voice lines through the existing filler pipeline, with licences and
   audio-ledger rows, plus any teacher or geologist imp costume the owner approves.
7. **W8:** fix the balance probe (H4), tune `base_seconds`, update the canon counts (H8), and
   merge to `dev` when CI is green.

## Owner decisions still open

These are covered in [CONTEST_DESIGN.md §7](CONTEST_DESIGN.md).

- **Nursery:** stay co-op, race the plain mischief imp, or commission a nursery imp.
- **Geologist:** confirm the inverted FIELD GUIDE MIX-UP, or keep it co-op.
- **Imp costumes:** a new teacher imp (recommended) and optionally a geologist imp, or keep
  the stand-ins.
- **Silly icons:** approve the style of the first five pictures (the smell question).
- **Silly scope:** silly questions alternating with math (this design), or all silly.
- **Restart scope:** contest only, or the whole career.
- **Hall stage-long race:** retire it (recommended), or keep it as no-loss.
- **Rematch mercy curves.**

## Governance recorded with this handoff

**Canon changes**
- **`DL-INT-14`** is added to
  [design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md](../../../design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md)
  as the owner-decided target contract. Implementation is pending.
- Revision 2 extends `DL-INT-14` with the inverted format for learning careers.
- Pointer sentences are added to `DL-INT-08`, `DL-INT-09` and `DL-INT-10`.
- The "Competition is scoped" bullet in `design/01_GAME_DESIGN.md` is amended.
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

## Checking this packet

```sh
python3 -B docs/handoffs/codex_opera_imp_contest_2026-09-30/tools/build_packet_data.py --check
```

The check prints `PACKET_CHECK|OK` when every file matches `MANIFEST.json`, the inventories
regenerate unchanged, and the folder contains no image.
