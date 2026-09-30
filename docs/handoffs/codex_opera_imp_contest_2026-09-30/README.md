# Codex handoff: Opera imp contests (2026-09-30)

- **From:** Claude. Written design, analysis and specification only: no game changes and no
  images.
- **To:** Codex, for implementation, including any image or voice generation it needs.
- **Owner:** approves the open decisions and accepts the result on the phone.

**Status:**
- `PROPOSED / CANDIDATE`. Publication is not creative acceptance.
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

**To confirm with the owner:** this design restarts the *contest only*. Earlier activities,
stars, pearls and saves are kept. See [CONTEST_DESIGN.md §1](CONTEST_DESIGN.md) and §7.4.

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

**Winning and losing**
- **She wins:** he staggers and flops with his existing "bop" line; her cheer tier becomes
  audible and visible. Then an existing flourish or the curtain call follows.
- **He wins:** a victory hop of at most 2 s, "I won! I won! Let's play again!", and the
  contest resets at once. She stays where she is, and he is slower each time.

**Reuse**
- All art already exists: 156 of the 178 imp pose files would appear, against 41 today
  (167 if the owner picks Nursery option B).
- 36 of the 56 existing imp lines would play, against 2 today (39 with Nursery option B).
- Only 25 short new lines are needed (27 with Nursery option B).

## What is in this folder

| Path | What it is |
|---|---|
| [CONTEST_DESIGN.md](CONTEST_DESIGN.md) | The specification: contract C1 to C14, shared mechanics, code integration, the twelve contests, owner decisions, retirements, tests, governance, work order and acceptance |
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
5. **W7:** the 25 new voice lines through the existing filler pipeline, with licences and
   audio-ledger rows.
6. **W8:** fix the balance probe (H4), tune `base_seconds`, update the canon counts (H8), and
   merge to `dev` when CI is green.

## Owner decisions still open

These are covered in [CONTEST_DESIGN.md §7](CONTEST_DESIGN.md).

- **Nursery:** stay co-op, race the plain mischief imp, or commission a nursery imp.
- **Geologist:** the same three options.
- **Teacher:** recommended no contest.
- **Restart scope:** contest only, or the whole career.
- **Hall stage-long race:** retire it (recommended), or keep it as no-loss.
- **Rematch mercy curves.**

## Governance recorded with this handoff

**Canon changes**
- **`DL-INT-14`** is added to
  [design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md](../../../design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md)
  as the owner-decided target contract. Implementation is pending.
- Pointer sentences are added to `DL-INT-08`, `DL-INT-09` and `DL-INT-10`.
- The "Competition is scoped" bullet in `design/01_GAME_DESIGN.md` is amended.
- Notes are added to the master index and the master-audit planning entry.
- Ledger rows are added for this packet's documents.

**The CLAUDE.md role rule**
- It records the owner's 2026-09-30 decision that Claude hands Codex written descriptions
  and builds no images. Its ledger row is updated to match.

**Impact record:**
[design/audit_impacts/codex-opera-imp-contest-handoff-20260930.json](../../../design/audit_impacts/codex-opera-imp-contest-handoff-20260930.json).

## Checking this packet

```sh
python3 -B docs/handoffs/codex_opera_imp_contest_2026-09-30/tools/build_packet_data.py --check
```

The check prints `PACKET_CHECK|OK` when every file matches `MANIFEST.json`, the inventories
regenerate unchanged, and the folder contains no image.
