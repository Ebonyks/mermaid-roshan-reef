# Opera House — faithful four-screen operative v1

Status: REVIEW_PROTOTYPE, 2026-10-31; local topic checkpoint with82passing
source-bound probes and20focused Opera checks. Production integration and
external acceptance remain pending. Original layout translated into one
2560 × 1440 Canvas world with four 1280 × 720 views. The owner approved the
intended vision and requested higher detail, visible life and interaction;
the current output still needs exact visual, motion and device acceptance.

## Design lock and implementation

Preserve the original three galleries, twelve arches, both dark bubble lifts,
curved stairs, chandeliers, lounges, carts, plants, central seating island,
runner and terrazzo at their normalized source positions. The five thematic
generations are rejected, preserved outside runtime and have no runtime references.
The subsequent two built-in edits restore detail and heal only embedded
medallions so separate signs can sit above each arch.

Roshan uses the approved authored swim atlas and follows the original galleries,
curved stair paths and two working lifts. Foyer routes pass around the central
island. A press previews the destination; one-finger drag/release commits it.
The camera follows smoothly across quadrant boundaries. Atlas motion samples
logical travel independently of camera translation.

Twelve independent source-pixel curtain pairs ripple with fixed tops. Resident
activity curtains part after arrival. Original sconces breathe warmth, lower
chandelier crystals glint, island leaves flex, and bubbles rise in both shafts.
The ticket counter and refreshment cart respond after approach with local
motion, a chime and a short ring/steam response. Whole architecture stays fixed.
The shader uses shared original coordinates at joins; island leaf deformation
uses Y sampling so the central X split cannot sample transparent padding.

Ballerina (2), Pop Star (13) and Magician (8) remain the three physical resident
activities. Existing career crests sit above arches and display completion
stars. The isolated review invokes shipping activities with dev_playtest:
cancel returns to the exact entry position/camera, success changes only the
review-session crest, and saved stars/pearls/story data stay unchanged.
A stale callback cannot award again. The nine other complete historical career crests remain
decorative; the review does not silently turn Opera into the all-career hub.
Pause/focus interrupts cancel pending travel and freeze ambient time.

## Resolution and provenance

The original whole-house master is1024×576. Existing3640×2048 cards were
resampled derivatives; the earlier built-in restoration returned1672×941.
Those source generations and their evidence are preserved as history.

The owner authorized tiled merging or account credits. The built-in workflow
produced24 overlapping background detail panels, six whole-fixture regional
detail crops and two pilot/backing outputs:32calls in this bounded phase,
39including the seven earlier calls. No direct paid API calls were made.
Billing, hosted model revision, request IDs and seeds were not exposed.

The assembled detail plate is7360×4140, or3680×2070per playable quadrant.
Every generated background panel meets the measured target density without
enlargement. A low-frequency source lock preserves the historical composition
and palette; native generated high-frequency surface information adds detail.
This is a declared composite, not a claim that the old master was native4K.
Forty non-overlapping POT-padded cards reproduce the assembled background
byte-exactly. Forty-three source-owned fixture groups use51cards; no object is
independently regenerated across a background join. Six whole regional crops
add confidence-masked microdetail; fixtures crossing those groups retain their
original source resolution. Healed interiors avoid duplicate painted fittings;
a two-source-pixel original boundary prevents unrelated clean-plane bleed.
Twelve fabric cards preserve the same world-space motion at the new density.
Every exported runtime texture isPOT and at most1024pixels on either side.

Native output sizes, hashes, exact prompts, ownership masks, crop rectangles,
source locks and lossless slice-roundtrip evidence are in the
[tiled generation record](../assets_src/review/opera_exploration_v1/tiled_detail/generation_log.json),
[assembly report](../assets_src/review/opera_exploration_v1/tiled_detail/assembly_report.json)
and [translation manifest](../assets_src/review/opera_exploration_v1/translation_manifest.json).
Originals, protected art and family voices are unchanged. Measured coverage
does not establish exact restored-art, motion or device/child/owner acceptance.

## Review launch and evidence

The review scene is a pure Control prefab. It needs the existing ReefMain state
owner; it is not a standalone main scene or a new 3D root. In the isolated
MermaidReef-OperaRemovalReview-20261017 profile, run scenes/main.tscn explicitly,
then attach scripts/review/opera_review_boot.gd as a Node to the current scene.
The bootstrap enters Castle/Opera and instantiates the review Control. Startup
settings and autoload writes were refused by Godot AI; none were changed.

The dedicated Godot AI runtime uses exactly 4.7.2-stable with Mobile rendering.
The final native run passed 20 focused checks, including routed input,
pause/focus, passive no-award, both lift routes, cross-screen travel, authored
swim progression, prop arrival, activity cancellation, exact return, callback
presentation and save invariance. The successful completion check is an explicit
synthetic callback fixture, not a played end-to-end win; its temporary crest bit
is cleared after capture. Baseline/final save hash is 541225771 and stars remain64.
Route sampling excludes the central island. See
[focused evidence](../assets_src/review/opera_exploration_v1/verification/focused_runtime.json).
The first failed pass and second repaired pass remain historical evidence;
later final-host evidence does not erase them.

## Remaining acceptance and integration plan

1. Review the tiled native-resolution candidate under the same layout lock: every
   original object, all joins, curtain seams and fixture motion at full speed
   and frame-step. The restoration candidate is not final accepted artwork.
2. Refine silhouette/rail occlusion and semantic travel voice/pointer coverage
   for the child-facing production route.
3. Complete full local and exact-topic CI before commit/integration; replace
   the venue through its existing lifecycle without changing sparse save bits,
   story/party/global completion authority, normal job ownership or return routes.
4. Measure Mobile/Speedy on Lenovo Tab M11 and wide phones:30fps, overdraw,
   memory, load, pause/focus/re-entry/save restore, then child and owner review.

Per-action animation derivation records preserve editable source/script hashes.
No new character animation was invented. Aseprite was unnecessary for these
engine fixture effects; preproduction per-action wall/cleanup caps were not
recorded and remain an explicit DL-MOT-16 evidence gap.

Baseline:218ae766f8e60afb3f6338b8fafce28ec9fab7f2.
Applicable rules and exact changed paths are recorded in the
[audit impact](audit_impacts/opera-four-screen-v1-20261031.json).
MA-OPERA-012 keeps its existing lifecycle; MA-2D-002 is not closed.
This isolated review adds no 3D resources or production 3D scene roots.

Native stationary-frame comparison confirms changed pixels in the ground curtain,
lamp and island leaves; see idle_pixel_change.json. The optional
operative_native_demo.mp4 is a sparse framebuffer recording with actual VFR
capture intervals, including readback/write overhead. It demonstrates fixture
changes and exploration, not runtime framerate or final cinematic acceptance.
Parser/inference and three exact-engine analyzer checks passed. Document
authority, development coverage and54 contract tests passed. Full game CI and
production integration remained pending at that earlier uncommitted snapshot.

## Owner correction: crest construction and palette

Owner feedback2026-10-31 identifies ballet as the correct sign construction and
rejects the darker/redder color balance. All twelve signs now reuse complete
256-square painted alpha crests from the existing family at scale0.31, preserving
their full rims and silhouettes. No sign uses a46px mural crop, square wall
corners or a circular clipping shader. The historical four-per-floor career
pictures fill decorative positions; only Ballerina2, Pop Star13 and Magician8
retain resident launch targets and completion stars. No retired boss crest is used.

The background shader previously multiplied its explicit texture sample by
fragment COLOR, which already includes the texture. This squared the painting's
colors. Vertex tint now travels separately, so paint is sampled once. Both
background and fabric are unshaded and share one small palette include:
94% chroma and RGB gains0.965/0.955/0.970, compared against the original source.
This restores softer coral/ivory with clearer teal/navy. Original raster hashes
and all fixture/navigation geometry remain unchanged. Source-average comparison
is diagnostic, not artistic acceptance.

The live-refresh inspection hit a debugger error when reading a newly added
constant from a cached script. The preview was stopped and relaunched from the
existing main scene to load the corrected sources cleanly. That failed refresh
does not count as visual or gameplay verification. New evidence is isolated in
verification/door_color; earlier focused passes/captures remain historical.
Exact color/sign review, device/child/owner acceptance and the broader exact-art/production-integration gaps remain separate.

Door/color verification: all12complete alpha crests are visible at scale0.31,
with exactly3resident crests. A native texture-once comparison matches the
unshaded source exactly (RGB error0); the deliberately squared-texture control
differs by43.40286 mean channel levels. The new focused run passes20/20,
including unchanged save hash541225771. Exact4.7.2 analyzer/parser/inference
checks pass. See verification/door_color/pixel_comparison.json,
focused_runtime.json and static_checks.json. This does not supply owner/device
art acceptance or the pending full game CI/integration evidence.

## Tiled candidate runtime follow-up

The final new-resolution runtime passes20focused checks again after the control
and completion-badge refinements. Native inspection confirms40background cards,
51fixture cards with43owners,12full painted crests,12curtains and legal texture
sizes. World-space curtain excursion remains1.9138756pixels at every density.
Unmodified stationary1600×900frames show leaf, lamp and fabric changes. The
registered art's mean RGB channels stay within0.47levels of the1672reference;
this diagnostic does not establish exact art or colour acceptance.

The first1.5second fabric comparison sampled nearly matching points in the
oscillation. A separate natural-loop capture waits for opposite extrema without
assigning phase or retiming: wave values+0.995and-0.996, identical camera/player
positions and18,780changed fabric pixels. See natural_curtain_motion.json and
the two unmodified curtain_peak images. The earlier ROI/capture data remains
preserved; these diagnostics do not replace owner normal-speed/seam review.

A separate touch-handler bot completes all six shipping ballet phases without
assigning progress or forcing a win. In52.15seconds and248gesture events, the
actual success callback returns to the hall, marks bit2 and shows the physical
crest badge. Normal saved stars64, pearls9 and hash541225771 remain unchanged.
This is programmatic hotspot/touch-handler play, not manual child acceptance.
The first capture accidentally retained the previous result frame; the repaired
capture waits two frames and reveals an oversized174px star. The final code
sizes the painted star to36px beside its79px crest and uses a110×110pause target.
The final callback image and runtime size check verify that presentation change.

Godot AI's short attach health probe intermittently reports PORT_OCCUPIED even
though its existing local backend is healthy. A normal MCP SDK connection to
that same server with a longer transport timeout verifies the same runtime@ee96
session. No shared server, other editor, startup settings or autoload was changed.
The final demo is left unpaused in the main foyer with test award bits cleared.
See verification/tiled_detail/final_review, played_ballet.json, pixel_checks.json,
final_demo_state.json, static_checks.json and final_source_overlay.json.

The full_ci_v3 run stopped at audio-ledger drift before the chime reference
refresh finished. That refresh changes only the chime count12to13 and inventory
digest; all857audio SHA256values and quality fields stay unchanged. The exact
failed audio command and every remaining original CI command are replayed in
ci_continuation.log, with the source recipe and unchanged classifiers/timeouts
preserved. The independent857-file audio rerun passes. Earlier failed full
runs remain explicit; no fresh single-invocation green claim is made.
Exact-topic remote CI, integration and device/child/owner
acceptance remain separate. Runtime source was refined before the full suite's
import/probe phase; changed-source parser, inference and exact-engine analyzers
were rerun after that refinement. No frozen-at-start whole-suite claim is made.

## Final regression follow-up

The unchanged CI suffix completed every82ordered probes:81passed and the
Geologist partner-placement assertion failed once. A clean baseline control at
218ae766 and an unchanged candidate rerun both pass with fresh isolated data,
the exact original touch/classic flags and byte-identical ALL OK logs. All
production Opera sources match baseline. The first control preparation omitted
import sidecars and is explicitly invalid; its resource errors are retained.
No production gameplay or assertion was changed to obtain a pass. This is an
intermittent failure, not evidence of a repaired Geologist defect. A final full
original CI invocation is recorded separately. No earlier failed run is erased.

All82trusted probes now have passing source-bound evidence:81from the original
ordered continuation and the unchanged Opera rerun. The121authored changed
runtime input hashes still match final checks; production runtime sources and
all assertions remain baseline bytes. source_bound_regression_summary.json
reapplies the original failure/runtime classifiers and records the earlier
intermittent failure. This is probe-by-probe completion; a redundant whole-suite
repeat was interrupted, and no new single-invocation green result is claimed.
The temporary clean-baseline control checkout was removed after preserving its
exact sources, command, hashes and logs. The private demo remains running.
