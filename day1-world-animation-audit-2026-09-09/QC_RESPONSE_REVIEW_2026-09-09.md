# QC-response review — 2026-09-09

The six requested trims are correctly applied. Of the four replacement jobs, two still require regeneration, one supplies a useful short cup-free team insert, and one is now a usable *rough editorial* contact-to-clean cut rather than a continuous cleanup. Keep the unchanged owner-locked C13 S05 primary.

This addendum reviews the assets uploaded at approximately **16:20 UTC** to the [same project release](https://github.com/Ebonyks/mermaid-roshan-reef/releases/tag/day1-world-animation-audit-2026-09-09). It updates the earlier QC only for these returned files; it does not erase earlier source evidence or accept the whole film.

## Intake and method

Thirteen new files were downloaded and matched to GitHub's byte counts and SHA-256 digests: eleven MP4s, `CODEX_HANDOFF_QC_RESPONSE.md`, and `QC_RESPONSE_COMPLETION.json`. Eleven MP4s comprise six trims and five replacement/endpoint files covering four jobs. `QCFIX`, `TRIM` and the completion document's pass notes are source labels/claims, not review conclusions.

All video files are 1280×720 at 24 fps. The normal new generated clips have 145 frames / 6.041667s; the C14 assembled clip has 144 frames / 6.0s. The six trims have their requested exact lengths. `INTAKE.json` binds source hashes and every archived sample to its native frame index.

Luna reviewed the trimmed endpoints; Sol reviewed the invitation and cup-free team shot; the root reviewer examined the C14 footage and exact assembled cut. Frame samples were compared to the original September 6 shot packets and source room/character references. The original world-audit source remains `6d7c5e85b6c53b6fbd4a304759ec97f7a6935b5d`; no fresh current-game runtime capture is claimed.

Every decoded frame in each trim was additionally compared with its expected earlier source range at 320×180 grayscale, including nearby offset alternatives. All six expected offsets produced the lowest error. Minimum per-frame PSNR was at least 48.49 dB. This strongly supports correct source selection after re-encoding; it is neither bit-identical preservation nor an exhaustive visual-identity audit. Native beginning/end samples were reviewed separately.

Source-frame intervals are zero-based and end-exclusive at 24 fps. Suggested further trims below have **not** been applied by this review. Audio streams exist but their content and edit continuity were not listened to here.

## Current dispositions

| File | Disposition | Scope |
|---|---|---|
| `D1-C03-S03_TRIM.mp4` | KEEP rough insert | Correct `[0,72)` / 3s dirty-bath trim. |
| `D1-C04-R01_TRIM.mp4` | KEEP rough insert | Correct `[0,48)` / 2s clean-bath trim. |
| `D1-C09-R01_TRIM.mp4` | KEEP rough insert | Correct `[0,48)` / 2s craft-room trim. |
| `D1-C12-R01_TRIM.mp4` | KEEP rough insert | Correct `[0,48)` / 2s clean-hall hug trim. |
| `D1-C10-R01_TRIM_BEFORE_CONTACT.mp4` | KEEP short approach | Correct `[0,33)` / 1.375s. Ends at the previously identified last clear-gap frame; no extra contact frame appended. Still not a three-second settled endpoint. |
| `D1-C02-R01_MAP_ONLY.mp4` | KEEP geography only | Correct old-source `[72,144)` / 3s. The earlier insufficient-dirty-state caveat remains. |
| `C14-S01_QCFIX.mp4` | REGENERATE cast-count shot | Large second bunny is gone, but a second bird appears. Six characters still occupy the shot. |
| `D1-C02-R02_QCFIX.mp4` | REGENERATE invitation shot | Pool stays dim, but the art-room palette now glows alongside the bathroom pearls. |
| `D1-C13-S04_QCFIX.mp4` | TRIM rough team insert | Cup-free, intact giant, two-window arena. Suggested `[0,48)` / 2s avoids the later pink-star-to-yellow-rounded sponge change. Longer action still carries prop-continuity debt. |
| `C14-S05_QCFIX_ASSEMBLED.mp4` | CONDITIONAL rough contact/result edit | Clean endpoint achieved across a hard cut at f60 / 2.5s, not by continuously shown dirt removal. Suggested total `[0,96)` / 4s if this editorial construction is wanted. |
| `C14-S05_CLEAN_ENDPOINT_HOLD.mp4` | Endpoint alternate only | Do not append it again after the assembled version. It has movement and changing poses; its filename does not establish a static hold. |

The unchanged `D1-C13-S05_FIX_ASSEMBLED_10s.mp4` remains the owner-selected C13 primary. S04 must still end with the giant intact; the single-shot S05 draft is not reinstated.

## Remaining priority 1: C14-S01 adds a second bird

At **f0**, the image has Daddy, Roshan, Rumi, the existing small rainbow bird and the tiny cloud friend: five actors. At **f24 / 1.000s**, an additional large red/blue bird with a white face and yellow beak stands at the foot of the Royal stairs, while the original small bird remains near Roshan. Both birds are still visible in f48, f72, f96, f120 and f144. The missing large rabbit was replaced by a different extra character, so the manifest claim that f24/end have five actors is contradicted by the actual footage.

Retain the useful hall geography, open Royal arch and tiny friend's small scale. The next complete-frame regeneration must bind **exactly three mermaids, exactly one bird and exactly one tiny rainbow bunny**. The one bird is Baby Eagle, matching its approved identity reference; that identity image describes the bird already visible in IMAGE_1, not a second arrival. All five begin on screen. Use a shared look toward the next mess instead of anyone entering. No additional bird, parrot, rabbit, reflection-double or growth. Count actors at the first frame, every occlusion/entrance, and endpoint—not merely whether a second bunny is absent.

Secondary final-identity debt: the tiny friend still presents a forehead jewel rather than the source concept's orange curl. Keep that distinction visible in a future identity review; do not treat small size alone as complete identity fidelity.

![Two birds and six actors at one second](frames/C14-S01_QCFIX/sample_002.png)

## Remaining priority 2: C02-R02 moves the wrong glow to another portal

The first frame has bathroom pearls already lit and the palette and drop dark. By **f24 / 1.000s**, the **palette** has gained a conspicuous golden halo while the bathroom pearls remain lit. Both stay highlighted in the subsequent one-second samples. The drop is now correctly dim, but that alone does not satisfy the single-destination requirement.

Do not change game progression to justify the accidental second cue. A replacement must keep the teddy, palette, drop and Royal arch at their starting non-cue brightness throughout, including reflections and camera changes. Only the bathroom's three pearls may be emphasized. Keep the corrected doorway order and architecture, and stage Roshan's attention toward the bathroom rather than a newly activated art-room doorway. No localized glow repaint or masking of existing frames: regenerate complete failed frames. A passing IMAGE_1 cannot establish that every later glow stays correct.

![Palette and pearls both illuminated at one second](frames/D1-C02-R02_QCFIX/sample_002.png)

## C13-S04: cup removed, but keep the short clean interval

The new shot genuinely addresses the named cup defect: sampled Rumi action sends water from her bare hand, with no white vessel. The giant remains intact and the tiny friend is absent; two ocean windows and the dusty arena landmarks remain. This is a meaningful improvement and is useful for the rough assembly.

There is still late prop drift: Roshan begins with a pink star-shaped sponge but holds a yellow rounded sponge by f72 / 3.000s and in later samples. A conservative two-second `[0,48)` insert avoids that observed later change while showing simultaneous team activity. It is not a replacement for the originally requested five seconds of stable-prop action. If a longer uninterrupted version is needed, its complete-frame regeneration must retain the same star sponge, Daddy's brush orientation, cup-free hand-water, intact giant and fixed arena.

![Cup-free team action and later sponge change](sheets/D1-C13-S04_QCFIX.jpg)

## C14-S05: a better rough endpoint, not continuous cleanup proof

Exact adjacent-frame inspection confirms the construction stated by the uploader:

- **f59 / 2.458333s:** water and dirt remain around the sponge, brush and runner edge; the floor is still visibly dirty.
- **f60 / 2.500000s:** a hard cut changes to a clean floor/runner, removed water stream, altered poses and dirt-colored bristles. This is the beginning of the clean endpoint plate.

Unlike the previous version, the new sampled endpoint does not finish in a pink puddle or brown floor smear. There are five actors and no additional bird in this shot. That makes it an improvement for a rough contact/result montage. It does **not** demonstrate continuous physical removal of all the debris; the edit omits that work.

If adopted editorially, treat it as two separate shots: contact `[0,60)` / 2.5s, then clean result `[60,96)` / 1.5s, totaling four seconds. Do not call the cut seamless, insert a dissolve or optical-flow bridge, or claim an intentional static hold—the endpoint footage itself moves. The separate full clean-endpoint file should not be appended again. A seamless single-shot completion would still need a new complete-frame cleanup span. The owner's C13 assembled-reveal lock does not automatically grant separate approval to this C14 construction.

![f59 before the clean cut](C14_cut_f57plus_003.png)

![f60 first clean endpoint frame](C14_cut_f57plus_004.png)

## Next action and acceptance limits

Do not regenerate all eleven. The mandatory next-shot priorities are **C14-S01 cast count** and **C02-R02 invitation exclusivity**. The six applied trims can be used in their stated rough roles. C13-S04 can contribute its short cup-free interval; C14-S05 offers a proposed rough editorial result cut. Longer continuous action and final identity fidelity remain separate work.

The source archive, earlier report and supplied handoff records are preserved. This addendum supplies QC evidence and editorial recommendations only; new decoded images are diagnostics, not cinematic art. No first-frame candidate, source clip, timeline, soundtrack or runtime asset was generated or edited; no game integration occurred. Per-frame full-generation provenance, exhaustive temporal/native-frame review, sound/listening review, exact first-frame approval for future reconstructions, current game-seam and owner/device acceptance remain outstanding. `DELIVERY_ACCEPTED: false`; no new `GENERATION_READY` job or committed-tree `ARCHIVE_COMPLETE` claim is made.
