# Day One audit reshoots — editorial QC, 2026-09-09

Four shots can be kept with short trims, two offer conditional salvage, and the owner-locked C13 assembled reveal remains the rough-cut choice. Four shots need targeted corrections. Do not regenerate all eleven.

[Source release and original audit packet](https://github.com/Ebonyks/mermaid-roshan-reef/releases/tag/day1-world-animation-audit-2026-09-09). Source names containing `APPROVED` are uploader filenames, not this review's verdict.

## Scope and evidence

Intake verified 23 newly supplied assets against GitHub's SHA-256 and byte counts: 13 MP4s (11 queue primaries and two C13 alternatives), five supplied first-frame images, three handoff documents, and two completion manifests. `INTAKE.json` binds their exact bytes, asset IDs and stable download URLs. Normal clips are 1280×720, 24 fps, 145 frames / 6.041667 seconds. The C13 assembled primary is 240 frames / 10 seconds.

The review compares decoded native video samples against the September 6 audit's shot briefs, source room plates, character locks and supplied IMAGE_1s. The original audit names game source `6d7c5e85b6c53b6fbd4a304759ec97f7a6935b5d`; this is not a fresh capture or acceptance of today's integration build. Luna reviewed bathroom/art-room shots; Sol reviewed Hall B and the workbench contact boundary; the root reviewer examined the C13/C14 issues and adjudicated the recommendations.

The evidence ZIP includes 107 regularly sampled native frames, 13 diagnostic contact sheets, and an additional exact C10 sequence from f24 through f48. Extra frames examined by reviewers are not all archived. This is sampled visual/editorial QC, not exhaustive frame-by-frame motion acceptance. All MP4s have audio streams; sound content, dialogue, listening quality and mix continuity were not reviewed here. No source clip, edit, game asset, runtime trigger or voice was modified.

All indices are source-video, zero-based at 24 fps. Trim intervals are **end-exclusive**: `[0,48)` keeps f0–47, exactly 2 seconds. They are editing recommendations, not edits already applied. They are not indices in an assembled film.

## All eleven queue shots

| Shot | Decision | Suggested usable range | What is now right / remaining limitation |
|---|---|---|---|
| D1-C02-R01 | KEEP_MAP_ONLY; dirty-state pickup conditional | `[72,144)` / 3.000s | Hall B portal order and open Royal arch are corrected. Floor/runner read substantially clean; left-side settling/action brief is not achieved. Use only as neutral geography, not proof of a dirty hall. |
| D1-C02-R02 | REGENERATE destination-cue shot | No complete invitation retained | Both blue-drop pool and three-pearl bathroom illuminate. Bathroom alone must invite the player. Geometry is worth preserving. |
| D1-C03-S03 | TRIM; no regeneration | `[0,72)` / 3.000s | Ocean window restored; mirror/shell sink, toilet, dirty bath and purple swimmer agree with references. Roshan remains viewer-right. |
| D1-C04-R01 | TRIM; no regeneration | `[0,48)` / 2.000s | Clean bath, two ocean windows, mirror/sink, left tub, right toilet and swimmer are present; no cleaning tool. Minor later decorative fish additions do not justify remaking it. |
| D1-C09-R01 | TRIM; no regeneration | `[0,48)` / 2.000s | Low central shelved workbench, supply groups and plain pink top are correct. Head turn finishes about f36; trim the redundant tail. |
| D1-C10-R01 | TRIM_BEFORE_CONTACT; longer endpoint conditional | `[0,33)` / 1.375s | Correct workbench and blank mat. f32 is the last unambiguous hand-clearance frame; f33 begins border overlap/ambiguous contact. This short approach does not supply the requested 3-second pre-contact settle. |
| D1-C12-R01 | KEEP with trim; no regeneration | `[0,48)` / 2.000s | Correct clean Hall B and far-right open Royal arch; no invented Hall B window. Daddy's glasses and separate tails survive the sampled hug. Already embracing at f0, but a readable affectionate hold. |
| D1-C13-S04 | REGENERATE cup-free team shot | Earlier establishing fragment only | Giant stays intact, no tiny friend, team together, correct two-window arena. Rumi still uses a white cup during the shot. |
| D1-C13-S05 | KEEP_LOCKED_ROUGH_CUT | `FIX_ASSEMBLED_10s` only | Giant absent after f132 / 5.5s; exactly four helpers and one tiny friend. Hard-cut reveal works as the locked rough placeholder, not continuous removal. |
| C14-S01 | REGENERATE five-character setup | No complete three-second setup retained | Tiny friend is already in f0; a second much larger rainbow rabbit joins by f24. Six characters instead of the required five. |
| C14-S05 | REGENERATE cleaning-result shot | Early contact insert only | Team contact is visible, but the action adds/redeposits pink spill and mud instead of leaving a clean patch. Dirty endpoint persists. |

## Priority corrections — specific evidence and reconstruction

These are QC instructions, **not new generation-ready jobs**. Preserve useful geography and acting as reference continuity, never as a localized pixel patch. Corrections require newly generated complete frames; no masking away an actor, repainting a glow in existing frames, optical flow, compositing or other forbidden delivery shortcuts. Any changed first-frame staging must be shown to the owner as an exact filename and hash before another job. Prepare the actual small bound-image shot card separately; never feed these annotated sheets or gameplay captures as generation pixels.

### 1. C14-S01 — one friend, not an additional large rabbit

**Observed:** f0 contains Roshan, Daddy, Rumi, Eagle and a tiny rainbow cloud friend. By f24 / 1.000s another very large, furry rainbow rabbit has entered beside that existing friend. Both persist in sampled f48, f72, f96, f120 and f144. This is not just perspective scaling: two separate friends are simultaneously visible. The large rabbit also changes the approved low-cloud silhouette and facial treatment.

**World/story disagreement:** this follows the one-giant-to-one-tiny-friend reveal. It must introduce no sixth actor or restored large bunny. The extra rabbit breaks both C13 continuity and the five-person cleaning team.

**Reconstruction:** retain the corrected hall landmarks and the four helpers. Use exactly one low, broad rainbow cloud body with spiral ears, an orange forehead curl, pearl-like front feet and simple eyes. At shared depth its height is no more than one quarter Roshan's. The identity reference describes that already-present actor, never an actor entering from off-screen. Begin with all five accounted for; a brief shared look toward the first mess is sufficient action. Do not add growth, a second bunny, an eyelash-heavy furry rabbit or a new magical entrance. End with the same five in readable positions for the next cleaning cut.

**Review points:** f0 cast ledger; f12, f24 and every subsequent actor entrance/occlusion; final 12 frames. Count characters across occlusion, not merely in the last frame.

![C14-S01 contact sheet](sheets/C14-S01_APPROVED.jpg)

### 2. C14-S05 — remove the mess; do not pour it back

**Observed:** f24 / 1.000s introduces a cloth for Rumi; f48 / 2.000s shows tools carrying dirt. A conspicuous pink spill is present by f72 / 3.000s; at f96 / 4.000s Roshan's handling reads as releasing captured dirty material back onto the floor. f120 and the final f144 / 6.000s retain a pink puddle, brown debris and brush smear. There is no convincing clean runner-foot patch at the endpoint.

**World/story disagreement:** the shot is the coordinated *completion* of a small mess, followed by a separate clean-wide shot. It currently demonstrates new mess creation/redeposit, so cutting straight to a sparkling castle would conceal a contradictory action rather than complete it.

**Reconstruction:** keep the existing messy patch and all five characters. In a four-second single shot: 0–1s establish tool contact at that patch; 1–2.5s Roshan wipes with her bound sponge, Daddy collects dirt on the bristles of his hand brush, Rumi sends a thin clear hand-water stream to wet the sponge, Eagle gives a restrained wingbeat, and the tiny friend nudges one inert scrap toward collection. At 2.5–3.5s a clean patch is visible directly behind the passing tools. At 3.5–4s the dirty tools withdraw and retain the removed material. Keep the walls, portals, stairs and runner fixed. No new pink liquid, poured-out captured mud, rag replacing the assigned action, broom replacing the brush, magical smear fade, whole-room wipe or sweeping of living puff creatures. Keep final wide S06 separate.

**Review points:** before/after each contact; f24, f48, f60, f72 and f84–95 for a 96-frame replacement. Track where every lump/spill goes. The area must become cleaner only after physical contact, and remain clean at the final cut.

![C14-S05 contact sheet](sheets/C14-S05_APPROVED.jpg)

### 3. D1-C02-R02 — only the bathroom invitation lights

**Observed:** f24 / 1.000s and subsequent one-second samples through f144 show the blue-drop pool emblem and three-pearl bathroom emblem illuminated together. The revised portal symbols and their order are otherwise much better.

**World/gameplay disagreement:** the next activity is the bathroom. Two luminous destinations give a non-reader competing objective cues. Do not change game progression to make this mistaken double invitation true.

**Reconstruction:** preserve the spatial sequence teddy → palette → single blue drop → three pearls → far-right open Royal arch. Keep the pool drop plainly visible but at constant unlit brightness. Only the three pearls receive the invitation glow; Roshan's eye-line/gesture resolves to that doorway. Preserve intentional dirty hall dressing and the open arch, without adding Hall B windows, doors or obsolete symbols. Use one modest camera move at most. End with the bathroom target unmistakable and all other emblems unchanged. A neutral pre-glow fragment cannot replace this required invitation.

**Review points:** inspect every glow onset and the last 12 frames; compare pool emblem luminance to its own first-frame state. Check that camera movement or reflections do not accidentally promote a second destination.

![D1-C02-R02 contact sheet](sheets/D1-C02-R02_APPROVED.jpg)

### 4. D1-C13-S04 — cup-free team action; giant remains intact

**Observed:** the intact giant, four helpers and arena topology are retained. At f72 / 3.000s Rumi clearly pours from a white cup; the cup also remains in samples f96, f120 and f144, with the late action reading as a sip. This repeats the specific prop/action defect the reshoot was meant to remove.

**World/character disagreement:** the assigned action is Rumi's thin hand-water stream, not a conjured drinking vessel. The problem is the prop and action, not the collaborative staging or the still-intact giant.

**Reconstruction:** preserve the two-window attic arena, pillars, chandelier and octagonal floor/rug. Keep all four helpers actively participating around one intact giant. Rumi's open hand emits a thin controlled stream directly onto the local cleaning contact; no cup, bottle, pail or drinking gesture. Daddy's brush bristles contact the giant with the handle seated correctly in his hands; Roshan's sponge acts at a separate readable contact; Eagle helps with a small directed wingbeat. Suds build at those contacts. Keep the giant present through the last frame, with no tiny rainbow friend yet. S05 owns the disappearance/reveal.

**Review points:** Rumi's hand silhouette at f0 and each direction change, all water origins, brush/hand connection, final intact-giant state. A tool appearing halfway through is a failure even if the start frame passed.

![D1-C13-S04 contact sheet](sheets/D1-C13-S04_APPROVED.jpg)

## Conditional pickups and exact salvage

### D1-C02-R01 — corrected geography, weak dirty state

The portal map is valuable and should not be redesigned. However, the runner and broad floor read largely clean; limited far-left wall grime does not establish the messes later cleaned. Roshan traverses from the left under successive portals (f0, f24, f48, f72), rather than staying near the left and settling toward the bathroom. `[72,144)` can be used as a neutral geography insert if the surrounding edit already establishes dirt and the movement matches. If this must carry the opening *dirty hall* beat, commission a bounded dirty-state/staging pickup preserving this exact topology and matching the mess locations used in the cleanup. Do not claim the neutral insert fulfills that role.

### D1-C10-R01 — use the approach only

The room and mat are corrected. Native adjacent-frame review of f24–48 places the last defensible visible fingertip gap at **f32 / 1.333333s**; f33 / 1.375s begins silhouette overlap with the mat border and thereafter reads as contact or ambiguous contact. Use `[0,33)` only if a 1.375-second approach can cut directly into gameplay. Contact is unequivocal in the later two-second samples. If the edit needs a complete three-second pre-touch settle, request a short endpoint pickup: hand stops clearly above the blank mat and remains visibly separated, with no mark, rune, chest, object activation or touch. Do not duplicate a still to manufacture that missing action/settle.

The ZIP includes `manual_frames/C10_f24plus_001.png` through `_025.png`, mapping exactly to f24–48. `_009.png` is f32; `_010.png` is f33.

## C13 continuity lock — preserve it

Use **`D1-C13-S05_FIX_ASSEMBLED_10s.mp4` only** as the S05 primary. The owner explicitly selected it. Keep `D1-C13-S05_SINGLE_SHOT_DRAFT.mp4` out of the assembly; the standalone `ENDPOINT_HOLD` is an alternate/reference segment, not an additional story shot.

At f131 / 5.458333s the giant and suds remain. At **f132 / 5.500s** the assembled cut presents four helpers and one tiny friend with the giant gone. The two ocean windows and arena landmarks are retained. This satisfies the rough-cut endpoint's no-coexistence requirement. It does not prove a continuous suds-removal transformation: the giant, foam and poses change at a hard cut. Record that honestly, without rejecting the owner-selected rough solution or replacing it with the single-shot draft. The last 4.5 seconds are an endpoint *segment*; its filename does not prove it is a static hold.

Later editing may shorten the endpoint if pacing warrants, but this QC makes no edit. S04 must end with the intact giant; do not move S05's tiny-friend state backward into S04.

![C13 assembled cut and endpoint samples](sheets/D1-C13-S05_FIX_ASSEMBLED_10s.jpg)

## References and next handoff clarity

The evidence ZIP copies seven reference files (six images and one JSON) byte-for-byte from the already published audit: Hall B, craft room, clean/dirty bathroom, the dusty attic arena, the tiny rainbow cloud identity, and the C14 character locks. Their inherited provenance and original packet hashes are recorded in `QC_EVIDENCE_MANIFEST.json`. The original full archive remains authoritative for all additional character, fixture, style and seam context.

There is a source-document clarity defect: an eight-second reveal frame paragraph is repeated in several unrelated shot READMEs, including S04 and C14 shots. That paragraph belongs to the S05 reveal only. It must not override S04's intact-giant endpoint or the C14 shot-specific timelines. The published original archive remains unchanged; this QC flags the discrepancy rather than silently rewriting its evidence.

Prioritize the four corrections above. Retain the four strong trims. Resolve the two conditional pickups only if their short inserts cannot serve the intended edit. Preserve the locked C13 rough solution. Do not batch-regenerate corrected rooms or change game geometry to rationalize stray props, an extra character, a wrong destination cue or an inverted cleaning result.

## Claims kept separate

- **Implemented:** intake, sampled QC, source comparison, exact trim recommendations and GitHub QC evidence attachments. No film assembly, game integration, new IMAGE_1 generation or sound edit in this pass.
- **Machine evidence:** incoming asset hashes/size and media metadata; diagnostic extraction and evidence ZIP round-trip checks. These do not prove acting, per-frame identity, licensing clearance or runtime correctness.
- **Acceptance outstanding:** exhaustive native-frame temporal review, sound/listening review, first-frame approval for any reconstructed staging, final full-frame provenance, owner/device/game-seam acceptance. `DELIVERY_ACCEPTED` remains false. No new `GENERATION_READY` jobs are asserted; this is a QC supplement, not a new self-contained executable generator packet. The original archive's uncommitted-tree limitation is unchanged.
