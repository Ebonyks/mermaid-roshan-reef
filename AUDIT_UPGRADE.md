# Mermaid Roshan: Reef of Light — Audit / Upgrade

Date: 2026-07-15

Scope: comparative production-quality audit and intervention plan

Target: one non-reading four-year-old, one finger, short sessions, Android,
stable 30 fps minimum on the weakest supported device

## Executive verdict

There is no useful, publicly verified class of shipped **full-scale AAA 3D games
built entirely in Godot** against which this project can be compared directly.
Godot's own current showcase highlights successful commercial productions such
as *Slay the Spire 2*, *Until Then*, *Cassette Beasts*, *Dome Keeper*, and
*Brotato*, but these are different scopes, genres, team sizes, and hardware
targets. This audit therefore uses two standards:

1. the strongest publicly documented commercial Godot productions for engine
   workflow, content density, presentation, accessibility, and performance; and
2. AAA production disciplines—measured frame pacing, animation continuity,
   coherent direction, redundant feedback, reliable releases, and repeatable
   content tools—without importing AAA scope, photorealism, monetization, or
   online-service complexity.

The game is best described as a **content-rich, emotionally exceptional personal
game with a strong automated integration harness**, not an AAA production. Its
greatest competitive advantage is the irreplaceable book and family material.
Its greatest relative weaknesses are the absence of device evidence, a highly
procedural and centralized content pipeline, uneven animation/camera/audio
finish, and limited release observability.

The recommended intervention is **curated AAA polish**: make the first ten
minutes and one complete activity-return loop exemplary, turn those solutions
into reusable systems, then roll them across the existing game. Do not add plot
or another activity until the golden path meets its device, accessibility, and
presentation gates.

## Benchmark basis and the AAA caveat

- The [Godot showcase](https://godotengine.org/showcase/) demonstrates a growing
  catalogue of polished commercial games, but not a like-for-like AAA 3D mobile
  children's title. This absence is an inference from the public catalogue, not
  a claim that no private AAA studio uses Godot.
- Godot's own showcase criteria require a released/demo product, an active store
  page, public reception evidence, and a polished experience across gameplay,
  UI, or visuals. That is a practical commercial-quality floor, not an AAA
  certification: [showcase criteria](https://godotengine.org/showcase/submissions/).
- *Cassette Beasts* documents the strongest relevant production lessons: a
  two-person team delivered a dense 30+ hour game by investing in tools, patched
  engine performance hot spots, and used a specialist partner for console ports:
  [Godot's Cassette Beasts interview](https://godotengine.org/article/godot-showcase-cassette-beasts/).
- *Until Then* is the most relevant presentation reference because it blends
  hand-drawn characters, 3D spaces, lighting, reflections, and minigames into one
  cinematic visual language: [Godot showcase](https://godotengine.org/showcase/until-then/).
- *Brotato* is a useful accessibility/clarity reference: short runs, one-handed
  defaults, strong readability, and explicit difficulty tuning:
  [Godot showcase](https://godotengine.org/showcase/brotato/).
- *Slay the Spire 2* is a high-profile studio production and useful UI/content
  benchmark, but its 2D deckbuilder architecture is not evidence that Godot has
  shipped a comparable open 3D mobile title:
  [Godot showcase](https://godotengine.org/showcase/slay-the-spire-2/).

## Current repository evidence

This audit measured the repair branch rather than relying on the older v3_49
audit:

| Evidence | Current value | Meaning |
|---|---:|---|
| GDScript files | 77 | Broad system surface |
| GDScript lines | 28,001 | Substantial personal-project codebase |
| `main.gd` | 8,295 lines | Still the dominant state/content owner |
| `kart.gd` | 2,950 lines | One activity approaches subsystem scale |
| authored `.tscn` scenes | 1 | Nearly all content is constructed in code |
| asset files | 1,185 | Large and diverse presentation inventory |
| asset tree size | ~326.4 MB | Import, memory, and package discipline matter |
| `.new()` calls in `main.gd` | 498 | Heavy runtime construction and allocation |
| `_build*` functions in `main.gd` | 45 | Content authoring is code-centric |
| `_tick*` functions in `main.gd` | 35 | Broad per-frame responsibility |
| direct `g[...]` uses in `main.gd` | 141 | Significant string/dictionary state surface |
| probe files | 49 | Excellent diagnostic investment |
| trusted CI probes | 19 | Strong integration gate; incomplete visual/device gate |

Positive foundations already present:

- Godot 4.4 Mobile renderer on every platform, 1280×720 expandable canvas, and
  an explicit Speedy tier for the target Mali GPU.
- Analytic gameplay collision rather than uncontrolled physics-body scale.
- Versioned transactional save recovery and additive compatibility.
- A true passive negative test, full-game completion bot, activity-specific feel
  telemetry, exact-SHA release gating, and per-probe isolated user data.
- A coherent storybook art direction and recent removal of active 0–3/5 generic
  art routes, pending runtime visual approval.
- No advertising, monetization, account, network, or live-service burden.

## Comparative scorecard

Scores are relative to top commercial production practice, not to emotional
value. `5` means release-ready at that standard with evidence; `1` means an
important capability is mostly absent.

| Dimension | Score | Evidence and relative weakness |
|---|---:|---|
| Audience and emotional fit | 5.0 | Purpose-built for one child; book art and family voices are an advantage no generic AAA title can reproduce. |
| Progress safety / no-fail design | 4.5 | Repair pass removed passive rewards, lost-progress risks, and forced-result exits. Device usability still needs observation. |
| Gameplay breadth | 4.0 | Large variety: exploration, picture games, slide, kart, Galaxy, combat, puzzles, dance, craft, wardrobe. Breadth now exceeds the consistency of finish. |
| Core traversal and input feel | 3.0 | Strong analytic movement and multiple feel probes; camera, collision response, haptics, and touch latency lack device measurements. |
| Visual direction | 3.2 | Storybook target and rebuilt materials/landmarks are coherent on paper. Runtime shot continuity, composition, overdraw, and scale hierarchy are not yet certified. |
| Character animation / cinematics | 2.5 | Roshan has authored verbs and improved arms, but animation blending, contact, gaze, staging, and scene-specific acting remain below commercial character-game finish. |
| UI / non-reader accessibility | 3.5 | One-finger, forgiving, voiced/visual cues, neutral exits. Some text remains primary, touch target sizing is not automatically audited, and motor alternatives are incomplete. |
| Audio direction and mix | 2.7 | Irreplaceable voices and contextual music are strong; almost everything uses the Master bus, with no formal voice ducking, loudness targets, or mix test. |
| Performance engineering | 2.8 | Mobile renderer, quality tier, culling, and low-cost collision are good design choices. There is no committed frame-time, thermal, memory, or load-hitch evidence from the target device. |
| Architecture / authoring tools | 1.8 | Satellite extraction began, but one 8.2k-line owner, 497 runtime node constructors, one scene, and dictionary state make consistent iteration expensive. |
| Automated QA | 4.0 | Exceptional headless integration coverage for this project scale. Visual regression, performance regression, and real touch/device automation are missing. |
| Release / observability | 2.5 | Exact-SHA CI and save-compatible signing policy are strong. Signing setup is incomplete; there is no crash/ANR, device matrix, or local session health report. |

This is not a simple average. For the intended child, audience fit and progress
safety matter more than architecture elegance. For continued development,
however, architecture and device evidence are the constraints most likely to
turn every new feature into a regression.

## Relative weaknesses that should drive intervention

### 1. Quality is inferred headlessly instead of measured on the device

The hard requirement is 30 fps, yet CI proves logical completion rather than
frame pacing. Godot's guidance emphasizes measuring on target hardware, and its
mobile GPU guidance specifically warns about transparent overdraw, post effects,
shader cost, and differences between desktop and tiled mobile GPUs:
[Godot GPU optimization](https://docs.godotengine.org/en/latest/tutorials/performance/gpu_optimization.html).
Android treats stable pacing—not only average FPS—as a quality dimension and
tracks slow 20/30 fps sessions:
[Android frame-rate metrics](https://developer.android.com/games/optimize/framerate),
[slow sessions](https://developer.android.com/topic/performance/vitals/slow-session).

Current risk areas are transparent character/flora cards, particles, clustered
small geometry, many dynamic nodes, runtime material creation, scene rebuilds,
and activity transitions. The project has a pause-menu FPS label, but no repeatable
capture of P50/P95/P99 frame time, memory, thermal throttling, load duration, or
touch-to-response latency.

### 2. The content pipeline cannot cheaply enforce consistency

Godot presents scene composition and reusable nodes as its core production model:
[Godot features](https://godotengine.org/features/). This game instead builds
almost the entire world through one scene and hundreds of constructors. That is
not inherently invalid, but it removes editor previews, reusable authored scenes,
resource validation, and designer-safe tuning. The result is strong individual
systems with uneven cross-game conventions.

The correct intervention is not a rewrite. Continue the existing extract-only
rule, but introduce typed data and reusable presentation components around the
current behavior. New content must not increase `main.gd`.

### 3. Presentation systems are local effects, not a unified direction layer

The art inventory has improved faster than shot direction. Top commercial games
feel coherent because camera, animation, lighting, audio, UI, and effects agree
about the same beat. Here, celebrations, camera response, character contact,
pointer behavior, voice timing, and transition staging still vary by activity.

The next art pass should therefore be a **runtime direction pass**, not another
asset-generation pass: frame representative shots, validate silhouettes at phone
size, align camera grammar, reuse one interaction pulse, and define one reward
ceremony with scalable variants.

### 4. Accessibility is well-intentioned but not yet systematic

The child cannot be expected to read. Every required objective should therefore
have simultaneous voice, motion/shape, and optional haptic feedback. Microsoft’s
game-accessibility guidance recommends redundant sensory channels and alternatives
to timing-heavy or analog-only inputs:
[additional cue channels](https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/103),
[input guidance](https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/107).

The circular snowball gesture is now functional, but it still needs an assist
path if the child cannot sustain the gesture. Color-only puzzle information,
small pause controls, repeated tapping, and timed actions should receive the same
review. Difficulty selection should remain invisible and adaptive rather than a
reading-heavy settings screen.

### 5. Audio has high emotional value but low production control

Family voices are the highest-value assets in the game, yet music, voice, effects,
and ambience mostly share the Master bus and per-player `volume_db` constants.
Commercial mixing needs independent buses, speech priority, consistent loudness,
and protection from repetitive high-frequency effects. Accessibility guidance
also recommends separate control of music, effects, ambience, and dialogue:
[Xbox audio accessibility](https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/105).

### 6. Test breadth is stronger than test fidelity

Forty-nine probe scripts are a major strength, but only 19 are trusted. The main
gate has no screenshot comparison, render-budget assertion, audio routing check,
or physical-device input run. Several recent failures came from probes that
constructed impossible state or depended on render-frame cadence. Test policy
should specify whether each probe is trusted, diagnostic, visual, obsolete, or
quarantined, and time-based probes should use simulation time or explicit state.

### 7. Release safety is designed but not fully operational

The exact-SHA Android gate and stable-signing refusal are production-grade ideas.
The remaining gap is operational: the signing secret is not installed, the
N→N+1 in-place upgrade/save-retention test is not automated, and no device health
report accompanies a release. For a private child-focused game, external analytics
are unnecessary; an opt-in local session report is sufficient and safer.

## Recommended intervention: curated AAA polish

### Phase U0 — Establish a measurable baseline

Effort: 1–2 focused days. Risk: low. Do this before presentation changes.

- Add a repeatable on-device capture route for the target tablet and weakest
  phone: cold boot, reef traversal, each activity entry/exit, Sky Lagoon, castle,
  kart pack, Galaxy, dungeon, and 30-minute soak.
- Record frame-time percentiles, worst hitch, memory high-water mark, scene
  transition duration, thermal state, and node/draw-call counts.
- Add a visual capture matrix at 1280×720 Mobile rendering: first frame, active
  play, reward, pause, and return for every activity.
- Add a local JSON health report; keep it on-device unless the owner explicitly
  exports it.
- Classify all 49 probes as trusted, diagnostic, visual, obsolete, or quarantined.

Exit gate:

- no missing-resource or script-property errors;
- stable 30 fps target with P95 frame time at or below 33.3 ms and P99 at or
  below 50 ms in normal play;
- no post-load hitch over 100 ms on the golden path;
- no low-memory kill or thermal collapse in a 30-minute session;
- baseline report and screenshots committed as small text/selected PNG evidence,
  not a bulk capture dump.

### Phase U1 — Build one gold-standard vertical slice

Effort: 3–5 focused days. Risk: medium. Recommended slice:

`boot → intro/skip → reef swim → nearest friend → deliberate play → reward → reef return`

Polish this path until it establishes reusable rules:

- one camera grammar for traversal, interaction approach, play, reward, and
  return;
- animation transitions with no pose snap, deliberate gaze, contact, and settle;
- a shared interaction pulse and reward ceremony;
- voice-first objective, moving visual pointer, icon, and short haptic pattern;
- music ducking under voice and consistent transition fades;
- prewarmed assets/shaders so the first interaction does not hitch;
- two-frame maximum visible response to touch at the 30 fps target.

Exit gate: a five-minute observed child session completes without adult verbal
instruction, reading, trapped state, accidental reward, obvious camera snap, or
frame-time breach.

### Phase U2 — Convert the slice into reusable production systems

Effort: 5–8 focused days. Risk: medium.

- Create an `ActivityPresentation` component for enter, hint, reward, neutral
  exit, and return beats.
- Create one input-intent layer that exposes move, steer, act, cancel, and assist
  regardless of touch/gamepad/keyboard source.
- Add typed activity state or typed `Resource` definitions for all new work;
  migrate existing dictionaries one activity at a time without behavior rewrites.
- Add audio buses for Voice, Music, SFX, Ambience, and UI, with speech ducking
  and safe limiter settings.
- Move scene-size presentation families into reusable `.tscn` or typed builders
  that can be previewed and validated independently.
- Make `main.gd` a coordinator. First milestone: below 5,000 lines; long-term
  repository target remains below 2,500. Never extract multiple behaviors in one
  commit.

Exit gate: a second activity adopts the systems with materially less bespoke
code and without changing its gameplay outcome.

### Phase U3 — Game-wide presentation and accessibility rollout

Effort: 1–2 weeks. Risk: medium-high because of breadth.

- Apply the shared enter/hint/reward/exit grammar to every activity.
- Replace text-primary objectives with voice + motion + icon. Text remains a
  parent-facing backup.
- Add motor assists: alternate single-direction/tap route for circular motion,
  reduced repeated tapping, generous hold/timing windows, and adaptive hints.
- Never encode required information by color alone; pair color with position,
  shape, icon, or sound.
- Add restrained haptics for accepted action, collision, earned reward, and
  navigation error; haptics remain supplementary.
- Run a runtime shot-direction pass over the repaired art. Fix framing,
  silhouette, scale hierarchy, contrast, and overdraw before generating more art.

Exit gate: every objective passes a non-reader checklist and every activity has
the same recognizable interaction/return language.

### Phase U4 — Performance and package hardening

Effort: 3–5 focused days after U3. Risk: medium.

- Profile before optimizing; keep per-area CPU/GPU evidence.
- Reduce transparent overlap and clustered sub-pixel geometry first, then node
  count/material changes. Mobile GPUs often lose more to overdraw and fragment
  cost than to simple opaque triangles.
- Prebuild/reuse shared materials; pool burst effects; validate particle and
  light budgets on Speedy.
- Audit runtime-created nodes and per-frame allocations in `main.gd`, kart,
  Galaxy, Sky Lagoon, and castle.
- Establish asset inclusion rules so backups, source-review trees, and diagnostic
  captures never enter the APK.
- Measure APK size and cold import/load after every packaging change.

Exit gate: U0 metrics remain green in a 30-minute soak and all trusted probes
pass on the exact build candidate.

### Phase U5 — Release acceptance and maintenance loop

Effort: 1–2 focused days plus owner authorization. Risk: low if sequential.

- Install the persistent signing secret without committing it; record and back
  up the certificate fingerprint.
- Build N, create recognizable progress, install N+1 in place, and verify the
  complete save schema and unknown-field preservation.
- Attach a release manifest: commit, probe run, APK hash, device test result,
  performance summary, known visual exceptions, and rollback link.
- Keep the stable direct download URL; do not publish when device acceptance or
  exact-SHA probes are red.
- After release, prioritize observed friction and regressions over new content.

## Intervention choices evaluated

| Option | Value | Cost/risk | Decision |
|---|---|---|---|
| Chase AAA visual scope | Low for this child | Very high; harms mobile budget and book identity | Reject |
| Add more minigames now | Low–medium | High inconsistency and regression cost | Defer |
| Rewrite into scenes/components | Potential long-term value | Unacceptable behavior and save risk | Reject rewrite; extract mechanically |
| Curated AAA polish on a golden path | Very high | Controlled and measurable | Recommend first |
| Device evidence and accessibility system | Very high | Low–medium | Mandatory |
| Runtime direction pass using current assets | High | Medium | Recommend before new art |
| External analytics/crash SDK | Low for private use | Privacy/network complexity | Do not add by default |
| Local opt-in health report | High diagnostic value | Low | Recommend |

## What not to change in this upgrade

- Do not redesign the book plot or remove Roshan eating the snowman's nose.
- Do not replace or destructively process book art, family voices, or friend art.
- Do not add fail states, reading-dependent gates, dark threat, monetization,
  accounts, social features, or online dependencies.
- Do not chase Forward+-only rendering; Mobile remains the visual authority.
- Do not add more gameplay bodies, OmniLights, transparent cards, or texture
  families without a measured Speedy-tier budget.
- Do not patch probes to excuse intended behavior regressions. Fix synthetic or
  cadence-dependent probes only when production behavior is independently sound.

## Upgrade decision

Proceed with U0 and U1. They have the best information gain and the highest
visible payoff. Approve U2 only after the golden slice proves its conventions on
the actual child and target device. Defer new plot and content until U3 is
complete. This path can make the game feel commercially directed and unusually
safe without pretending that a one-child Android storybook game should imitate
the budget, scale, or technical architecture of an AAA console production.
