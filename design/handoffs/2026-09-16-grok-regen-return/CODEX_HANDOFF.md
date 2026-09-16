# Codex handoff — Grok regen return 2026-09-16

**DELIVERY_ACCEPTED: false**  
**GENERATION_READY: false**  
**Disposition: motion reference only — sampled QC, not full-frame acceptance**

Grok inspected the private archive (`Ebonyks/mermaid-roshan-grok-videos`) plus the Sept 9 audit QC and the Sept 12 overnight recut notes, then regenerated **only the clips that QC already marked REGENERATE / MOTION FAIL / WEAK**. This is not a batch remake of all 331 historical clips or of the 36 first-frame-pending library shots.

Clips are **not** in `assets_src/`. They live on the GitHub release attached to this tag and in the private archive. Do not copy them into the game tree.

Release: https://github.com/Ebonyks/mermaid-roshan-reef/releases/tag/grok-regen-return-2026-09-16  
Private mirror: `Ebonyks/mermaid-roshan-grok-videos` → `videos/regen-2026-09-16/`

## Why these six

| Return | Maps to | Prior defect | IMAGE_1 source |
|---|---|---|---|
| C14-S01 | five-character setup | Extra large rainbow rabbit / second bird by 1s | `C14-S01_QCFIX2_LOCKED_STILL` f0 (five-cast still) |
| C14-S05 | coordinated clean | Tools redeposit pink/mud; dirty endpoint | `C14-S05_APPROVED` f0 (messy start) |
| D1-C02-R02 v2 | bathroom invitation | Pool drop AND pearls both glow | `D1-C02-R02_APPROVED` f0 |
| D1-C13-S04 | cup-free team around intact giant | Rumi white cup / sip | `D1-C13-S04_APPROVED` f0 |
| R14 | SHOT-TEAM-WALL | Overnight WEAK: floor puddle, not wall wipe | overnight `R14_SPONGE_PRIMARY` f0 |
| R16 | SHOT-TEAM-FINISH | MOTION FAIL: beard, extra cast, bunny drift; only a locked still existed | `R16_CLEAN_WIDE_LOCKED_STILL` f0 |

Not regenerated (keep prior primaries / trims): D1-C02-R01 map-only, D1-C03-S03, D1-C04-R01, D1-C09-R01, D1-C10-R01 trim-before-contact, D1-C12-R01, owner-locked C13-S05 assembled 10s, overnight R01–R13 / R15 / R17–R18 passes.

## Primaries

| Shot | File | SHA-256 | Bytes | Sampled note |
|---|---|---|---|---|
| C14-S01 | `C14-S01_REGEN_2026-09-16_6s.mp4` | `e77d4d4d9603f5a51030357349dcb8b15502e13537284d084657a1284f7a9502` | 3174920 | t0/t3/t55: five cast, one tiny friend, no second rabbit |
| C14-S05 | `C14-S05_REGEN_2026-09-16_6s.mp4` | `46f89b0e1435aa6e60435c1a896c43930c313ee1fbc0d8945bf12c2c122117b6` | 5970008 | t3 contact; t55 cleaner floor, no pink pour-back in samples |
| D1-C02-R02 | `D1-C02-R02_REGEN_v2_2026-09-16_6s.mp4` | `1f6fbd84b3e2dd42c79a7c5f5d016168fa1ed64513a4f90396c37be05dff2833` | 4076439 | pearls dominate; pool drop stays darker than v1 |
| D1-C13-S04 | `D1-C13-S04_REGEN_2026-09-16_6s.mp4` | `190d55a95b72c194a6d3a63310b2aba19fae7160c227041d589c2b4551829a63` | 4796327 | no white cup in t3/t55; giant intact at last sample |
| R14 | `R14_TEAM_WALL_REGEN_2026-09-16_6s.mp4` | `472959a34811eb9ac9623c6342ea75b19e63498ea72b43b55e9cb5b2afb5a8cf` | 5558951 | sponge on wall stain; still rough |
| R16 | `R16_TEAM_FINISH_REGEN_2026-09-16_6s.mp4` | `e9ec8deda1d02c4c6ce475228a56f5c004b0ebe73bb90391ce0c2a69439f282b` | 3781735 | clean-shaven Daddy; no extra giant; five-cast settle |

**Superseded (do not cut):** `D1-C02-R02_REGEN_2026-09-16_6s.mp4` sha `0edfedbfd87468f9bdd7b8f37362048d1261e589c598147e15d68f1fdd25cbbf` — dual glow still competing. Kept only as a rejected attempt.

## What Codex should do

1. Intake the six primaries + IMAGE_1 stills against the SHA-256 table. Do not accept on filename.
2. Watch each at 24fps; inspect t0, contact, last 12 frames vs the defect column above.
3. Record exact zero-based end-exclusive native frame spans for any remaining miss. One shot per review.
4. Do **not** put clips into `assets_src/cinematics/`. Keep media on the release / private archive.
5. Do **not** set `DELIVERY_ACCEPTED` or swap runtime media from this packet.
6. If a shot still fails identity/contact, write a `REGENERATE` review with reconstruction — do not interpolate or composite a patch.
7. SHOT-BUNNY-SOAP A001 remains a planning request only; it was not generated this round (overnight R09 already passed as a soap contact ref).

## Claims kept separate

- Implemented: inspect existing QC, generate six returns from locked/opening IMAGE_1s, sampled frame review, GitHub handoff + clip upload.
- Outstanding: owner first-frame approval, exhaustive native-frame review, sound review, runtime seam, full-frame provenance.
