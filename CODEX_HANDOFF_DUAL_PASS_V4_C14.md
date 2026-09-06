# Codex Handoff — Day One V4 + C14 Dual-Pass Clips

**Status:** `COMPLETE_DUAL_PASS_A_PLUS_B`  
**Date:** 2026-09-06  
**DELIVERY_ACCEPTED:** false (motion-reference plates only)  
**Owner gate:** first frames approved via `approve all`; Pass B requested for b-roll + generation-error coverage

---

## 1. Purpose for Codex

You are receiving **two independent image-to-video takes** of the same 22 Day One shots so an editing AI can:

1. Prefer Pass A as the primary continuity plate when it holds composition/cast.
2. Swap to Pass B (b-roll) when Pass A has Grok motion artifacts (identity drift, extra limbs, wrong props, camera drift, missing action beats).
3. Intercut A/B within a shot for denser timing without re-prompting Grok mid-edit.
4. Build reels/megas with alternate coverage for the same story beats.

Do **not** treat either pass as final ship media until `DELIVERY_ACCEPTED=true`.

---

## 2. Source of truth

| Item | Location |
|------|----------|
| **GitHub Release** | https://github.com/Ebonyks/mermaid-roshan-reef/releases/tag/day1-v4-c14-3sets-2026-09-06 |
| **Orphan branch** | https://github.com/Ebonyks/mermaid-roshan-reef/tree/day1-v4-c14-3sets-complete-2026-09-06 |
| **Publication doc** | https://github.com/Ebonyks/mermaid-roshan-reef/blob/d9e44a12761f76c910779eb5803721e8aedabae7/design/GROK_HANDOFF_PUBLICATION_2026-09-05.md |
| **Content commit (packets)** | `1ec777f76fcdd76cbb4e31cce6a59dfb7d1ddfc0` |

### Machine manifests (prefer JSON over this prose)

- `manifests/V4_C14_DUAL_PASS_COMPLETION.json` — full A+B pairing
- `manifests/V4_C14_FULL_COMPLETION.json` — Pass A only
- `manifests/BROLL_FULL_COMPLETION.json` — Pass B only
- `manifests/SET{1,2,3}_COMPLETION.json` — Pass A by set
- `manifests/SET{1,2,3}_BROLL_COMPLETION.json` — Pass B by set
- `manifests/V4_C14_THREE_SETS_WORKPLAN.json` — shot packets + openings + SHA

---

## 3. Naming & pairing rules

| Pass | Suffix | Role |
|------|--------|------|
| **A (PRIMARY)** | `*_APPROVED.mp4` | Default edit plate |
| **B (BROLL)** | `*_BROLL.mp4` | Alternate take / error fix / splice coverage |

**Pair by shot_id**, not by filename order. Example:

- `C11_S01_v4_four_room_trails_APPROVED.mp4` ↔ `C11_S01_v4_four_room_trails_BROLL.mp4`
- `C14_S06_c14_look_what_we_did_APPROVED.mp4` ↔ `C14_S06_c14_look_what_we_did_BROLL.mp4`

Both shares:

- Same approved opening still (filename + SHA-256 verified)
- Same PROMPT.txt timing / camera / negatives
- Same 16:9 storybook pastel pearl-palace style
- Independent generation seed (motion will differ)

---

## 4. Shot inventory (22 × 2 = 44)

### SET1 — P0 hall + arena + suds/rainbow finale (6)

| shot_id | Pass A | Pass B | tool dur |
|---------|--------|--------|---------:|
| D1-C11-S01 | C11_S01_v4_four_room_trails_APPROVED.mp4 | …_BROLL.mp4 | 6 |
| D1-C11-S02 | C11_S02_v4_royal_arch_approach_APPROVED.mp4 | …_BROLL.mp4 | 6 |
| D1-C11-S03 | C11_S03_v4_empty_dusty_arena_APPROVED.mp4 | …_BROLL.mp4 | 6 |
| D1-C11-S04 | C11_S04_v4_puff_lands_APPROVED.mp4 | …_BROLL.mp4 | 6 |
| D1-C13-S04 | C13_S04_v4_team_suds_build_APPROVED.mp4 | …_BROLL.mp4 | 6 |
| D1-C13-S05 | C13_S05_v4_one_friend_reveal_APPROVED.mp4 | …_BROLL.mp4 | **10** |

### SET2 — P1 rooms / pool / rescue / desk (10)

| shot_id | Pass A | Pass B | tool dur |
|---------|--------|--------|---------:|
| D1-C01-S04 | C01_S04_v4_closed_door_arrival_APPROVED.mp4 | …_BROLL.mp4 | 6 |
| D1-C03-S02 | C03_S02_v4_bathroom_threshold_APPROVED.mp4 | …_BROLL.mp4 | 6 |
| D1-C03-S03 | C03_S03_v4_swimming_bunny_APPROVED.mp4 | …_BROLL.mp4 | 6 |
| D1-C03-S04 | C03_S04_v4_basket_precontact_APPROVED.mp4 | …_BROLL.mp4 | 6 |
| D1-C05-S01 | C05_S01_v4_dirty_pool_entry_APPROVED.mp4 | …_BROLL.mp4 | 6 |
| D1-C05-S03 | C05_S03_v4_skimmer_contact_APPROVED.mp4 | …_BROLL.mp4 | 6 |
| D1-C06-S05 | C06_S05_v4_two_fronts_converge_APPROVED.mp4 | …_BROLL.mp4 | 6 |
| D1-C08-S06 | C08_S06_v4_eagle_wingbeat_APPROVED.mp4 | …_BROLL.mp4 | 6 |
| D1-C09-S03 | C09_S03_v4_four_supplies_APPROVED.mp4 | …_BROLL.mp4 | 6 |
| D1-C10-S05 | C10_S05_v4_desk_handgap_APPROVED.mp4 | …_BROLL.mp4 | 6 |

### SET3 — C14 team cleanup coda (6)

| shot_id | Pass A | Pass B | tool dur |
|---------|--------|--------|---------:|
| C14-S01 | C14_S01_c14_new_friend_shared_job_APPROVED.mp4 | …_BROLL.mp4 | 6 |
| C14-S02 | C14_S02_c14_smallest_helper_first_diff_APPROVED.mp4 | …_BROLL.mp4 | 6 |
| C14-S03 | C14_S03_c14_brush_and_breeze_APPROVED.mp4 | …_BROLL.mp4 | 6 |
| C14-S04 | C14_S04_c14_water_shared_wipe_APPROVED.mp4 | …_BROLL.mp4 | 6 |
| C14-S05 | C14_S05_c14_coordinated_final_sweep_APPROVED.mp4 | …_BROLL.mp4 | 6 |
| C14-S06 | C14_S06_c14_look_what_we_did_APPROVED.mp4 | …_BROLL.mp4 | 6 |

---

## 5. Layout on GitHub

```
clips/
  ALL/          # 44 files: *_APPROVED.mp4 + *_BROLL.mp4
  SET1/         # Pass A only (legacy)
  SET2/
  SET3/
  BROLL/
    ALL/        # 22 *_BROLL.mp4
    SET1|SET2|SET3/
first_frames/   # approved openings (shared by A and B)
manifests/      # dual + per-set completions + workplan
CODEX_HANDOFF_DUAL_PASS_V4_C14.md  # this file
```

Release assets: individual MP4 downloads (preferred over cloning for bandwidth).

---

## 6. Editing AI policy (how to use A vs B)

### Prefer Pass A when
- Cast count/identity matches packet
- Camera ≤1 move as specified
- First-frame composition holds through hold frames
- Hard constraints hold (e.g. C13-S05: giant dust body fully gone; one tiny rainbow friend only; two shell windows)

### Prefer Pass B when Pass A shows
- Extra/missing companions
- Tool grip reverse (hands on bristles)
- Bunny morph (arms, human legs, vacuum mouth)
- Camera pan/orbit/second move not authored
- Premature cleanup / magic dissolve
- HUD/text/watermark
- Wrong room geometry (door count, window type, moat vs dry landing)

### Splice strategy
1. Align A and B on first frame (same opening still → near-zero slate drift).
2. Cut on action or hold (never mid-identity morph).
3. Prefer continuous camera lock; for C13-S04 / C14-S06 the only allowed move is the authored gentle push-in / 4% pullback — if one pass drifts, stay on the other for the move section.
4. Trim tool durations down to packet `duration_seconds` when assembling game-facing timelines (most packets are 3–6s; tool forced 6 or 10).

### Hard constraints reminder (do not invent workarounds)
- **C13-S05:** giant body/face/ears gone by end; cast = Roshan + Daddy + Baby Eagle + Rumi + **one** tiny rainbow friend; arena keeps **two shell-topped side windows**
- **C14:** physical contact cleaning only; tiny friend has **no arms**; brush grip behind ferrule
- Never bind boards, contact sheets, endpoint candidates, or HUD as generation pixels (already respected in these plates)

---

## 7. Technical facts

| Property | Value |
|----------|-------|
| Aspect | 16:9 |
| Generation mode | image_to_video from approved OPENING_CANDIDATE |
| Resolution intent | 720p class (1280×720 target; generator may emit ~1264×720) |
| Style | 2D storybook pastel pearl-palace |
| Audio | Bake intent only in prompt (soft SFX); treat as temp reference |
| Continuity | Single-shot per clip; ≤1 camera move |

---

## 8. Recommended Codex next steps

1. Ingest `V4_C14_DUAL_PASS_COMPLETION.json` and build a pairing table `(shot_id → A path, B path, target_duration, camera)`.
2. QC pass: score each A/B against SHOT_PACKET negatives; mark `preferred_pass` per shot.
3. Assemble SET1 / SET2 / SET3 reels with FFmpeg normalize+concat using preferred plates.
4. For any shot where both A and B fail hard constraints → flag for human re-approve / re-gen (do not silently invent new openings).
5. When owner sets `DELIVERY_ACCEPTED=true`, promote preferred plates into game cinematic import path under content commit policy.

---

## 9. Do not

- Re-run pure text-to-image for named cast (always first-frame bind)
- Montages of contact sheets as IMAGE_1
- Claim delivery acceptance without owner message
- Upscale with ffmpeg scale (use super-res path only if asked)
- Stitch >60s in one Codex request without checkpoints

---

## 10. Contact / resume strings

Owner phrases that resume this pipeline:

- `approve all` / `approve all SET{n}` — first-frame gate
- `regenerate pass B` / `b-roll` — this dual-pass job
- `delivery accepted` — flip flag after QC
- `densify C13 S02–S04 2×` — prior densify pattern for other packets

**Generator:** Grok Imagine image_to_video · **Stager:** Grok sandbox handoff_v4_stage · **Repo:** Ebonyks/mermaid-roshan-reef
