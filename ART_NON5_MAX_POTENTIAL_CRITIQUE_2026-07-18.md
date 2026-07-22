# Non-5/5 Art Critique and Maximum-Potential Failure Analysis - 2026-07-18

## Scope and source note

This critique cross-references the complete non-5 audit history, the current
full-regeneration candidate pack, the book-derived style guide, owner feedback,
and the Claude GEN-2 audit corpus.

No file containing the literal name `Fable` exists in `assets/`, the active
checkout, the full-regeneration branch, or git history. The Claude asset review
that matches the request is the ten-part GEN-2 audit in
`gen2/audit/claude_0.json` through `claude_9.json`, aggregated in
`gen2/generated/ANALYSIS.md` and reconciled with owner calls in
`gen2/curation.json`. If a separate Fable export exists outside the repository,
it is not available to this audit.

Evidence reviewed:

- `ART_STYLE_GUIDE.md`
- `ART_RESIDUAL_LOW_SCORE_AUDIT.md`
- `ART_HUMAN_REVIEW_AUDIT_2026-07-16.md`
- `ART_GAME_WIDE_PASS35_AUDIT_2026-07-16.md`
- `ART_AUDIT_2026-07-18.md`
- `ART_SCORING_GOVERNANCE_2026-07-18.md`
- `FULL_TEXTURE_REGEN_FAILURE_ANALYSIS_2026-07-18.md`
- `FULL_TEXTURE_REGEN_POST_STRESS_ANALYSIS_2026-07-18.md`
- `audit/full_regen_2026-07-18/target_ledger.csv`
- `audit/full_regen_2026-07-18/candidate_role_review.csv`
- all full-regeneration model, texture, repetition, and phone-scale galleries
- the raw Claude GEN-2 verdicts, flaw codes, selected variants, and Round 2 picks

## Executive conclusion

The recurring problem is not insufficient asset volume. It is that the pipeline
repeatedly rewards **a valid, attractive isolated candidate** before proving an
**authored, functionally correct, book-aware result in the shipped scene**.

The art usually stops below 5/5 for five linked reasons:

1. A broad global style prompt replaces motif-specific observation.
2. Generators decorate or merge concepts instead of preserving one subject.
3. Procedural 3D removes obvious defects but converges on generic toy primitives.
4. Isolated renders hide repetition, scale, lighting, animation, and composition failures.
5. Audits score production stage or technical validity as though it were visual quality.

The result is a large library that is cleaner and more coherent than the legacy
art, but still reads as several competent automated pipelines rather than one
deliberately art-directed world. Maximum potential requires fewer simultaneous
assets, stronger motif references, stricter identity and function contracts,
and an independent runtime rejection loop before scores are assigned.

## What the Claude audit proves

The Claude GEN-2 review covers 123 roles and 492 generated variants. The
published aggregate records 83 KEEP, 23 POLISH, and 17 REGEN roles after the
owner override that moves `galaxy_fruit_apple` from POLISH to REGEN. The raw
review JSON, before that override, contains 83 KEEP, 24 POLISH, and 16 REGEN.

Across the 492 variants, Claude recorded 635 flaw incidents:

| Code | Failure | Incidents |
|---|---|---:|
| F2 | Face added to scenery or ordinary objects | 133 |
| F8 | Named subject enmeshed with another concept | 119 |
| F5 | Cluster or miniature scene instead of one reusable object | 104 |
| F3 | Confetti, decals, flowers, stars, or swirls added as filler | 91 |
| F10 | Subject hijacked by category/style context | 91 |
| F1 | Bubbles, droplets, or gems baked into the asset | 34 |
| F7 | Palette bleed or washed local color | 24 |
| F6 | Visible texture tessellation | 22 |
| F9 | Invented character | 11 |
| F4 | Baked sticker border | 6 |

The dominant failure is **semantic contamination**. F8, F5, and F10 account for
314 incidents: the generator understood the mood but did not preserve the
object boundary. Rocks became coral creatures, fruit grew butterfly wings,
playground equipment became castles, and a swing became an invented mermaid
hugging a tower. This is the clearest historical evidence that adding more
storybook context to a prompt can reduce accuracy.

Aquatic art contains 310 of the 635 flaw incidents. It is especially vulnerable
because "underwater," "magical," "coral," "bubbles," and "friendly" encourage the
model to graft habitat decoration and faces onto every subject. Terrain has a
different concentrated failure: all 22 F6 repetition incidents occur there.

The KEEP bucket was not a 5/5 bucket. Eighteen of 83 selected KEEP variants
either retain a recorded flaw or score below 8/10 for usability. Fourteen KEEP
picks retain an explicit flaw, including smiling scenery, mild tile repetition,
decorative butterfly remnants, clusters, and subject-context drift. Across all
107 selected KEEP/POLISH variants, 39 picks score only 5-7/10. "KEEP" meant best
available and salvageable, not maximum-potential art.

This distinction matters because later production work sometimes treated a
named Claude pick as design approval instead of as a curation starting point.

## What the runtime audits prove

The audit chronology shows that routing and file quality repeatedly masqueraded
as finished-art quality:

| Audit stage | Finding | What it actually measured |
|---|---|---|
| Residual audit, 2026-07-15 | No automatically replaceable 0-2 roles remained | File replacement and runtime routing |
| Human gameplay audit, 2026-07-16 | 71 of 88 roles were still 0-2 | Appearance in the Mobile renderer |
| Pass 3.5 audit | 52 roles became 4-candidates; 33 remained below 4 | Broad runtime capture matrix after rebuild |
| Four-day audit, 2026-07-18 | Median moved to 3.5; several major areas still 3-3.5 | Delivery and technical profile plus earlier captures |
| Full-regeneration review | All 85 generated roles assigned 4/5 candidate | Isolated Blender galleries and 112 px crops |

The jump from "none remain" to 71 low roles in one day is not an art regression.
It is an audit-method failure. The first audit scored whether a replacement
existed and was routed; the second scored what the child actually saw.

The full-regeneration review risks repeating that mistake. Its 85 candidate
roles all receive 4/5, while 71 rows use the identical evidence sentence:
"Reviewed in full-size and 112 px phone-scale galleries." The candidates are not
wired to runtime paths. The Godot probe proves importability and resource
budgets, but the CI world captures show the existing game, not the isolated
candidate pack. Under the project's own hard gate, an unwired candidate without
representative runtime screenshots cannot hold an official 4/5 role score.

The correct interpretation is:

- `structural_pass`: valid candidate file;
- `isolated_visual_pass`: worth staging in game;
- `runtime_pass`: eligible for 4/5;
- `owner_accepted`: eligible for 5/5.

The current `4/5 candidate` label combines the first two stages and should not
be read as a runtime art score.

## Repeating errors that block 5/5

### 1. Motif families collapse into one global "cute pastel" style

The book has distinct visual systems for butterflies, beetles, coral, garden
plants, toys, kitchen objects, snow, architecture, and handmade crafts. The
global prompt correctly asks for pastel cel art, indigo contours, and colored
shadows, but those traits do not define the subject.

When the motif reference is weak, butterflies become generic four-lobed icons,
plants become rounded tufts, coral becomes branching candy pipes, houses become
the same box with different roofs, and every material receives the same smooth
matte response. The library becomes consistent in palette but homogeneous in
design intelligence.

**Why this prevents 5:** style coherence is present, but observational truth and
family-specific character are missing.

**Required correction:** every role contract must name its canonical book pages,
growth habit/anatomy, functional silhouette, and forbidden neighboring motifs.
The global prompt comes last, not first.

### 2. Identity is decorated instead of designed

Claude's F2/F3/F8/F10 pattern is the central image-generation failure. Empty
space is filled with faces, butterflies, flowers, bubbles, stars, coral growth,
rainbows, and sticker rims. These additions feel superficially on-brand but make
ordinary objects less believable and reusable.

The same tendency appears more subtly in later art: stars and butterfly motifs
are used as universal decoration, coral dressing migrates into kart scenes, and
palette accents substitute for a role-specific construction detail.

**Why this prevents 5:** the object communicates "Mermaid Roshan themed" before
it communicates what it is or how the player uses it.

**Required correction:** use one subject, one attachment point, one dominant
hue, and at most two signature details. Effects and habitat dressing remain
separate scene layers.

### 3. Procedural geometry removes defects but stops at generic primitives

The full-regeneration baseline identified primitive or generic geometry in 38
roles, the largest current failure category. Procedural rebuilding eliminates
literal engine primitives and produces valid low-poly meshes, but many models
still read as arrangements of rounded boxes, spheres, cylinders, cones, rings,
and flat panels.

Examples in the candidate galleries include box-bodied trains and vehicles,
near-identical ring gates, simple slab stairs, cylindrical columns, disc doors,
box houses, smooth bell jellyfish, and coral families whose distinction comes
from primitive arrangement rather than observed growth logic.

**Why this prevents 5:** replacing a primitive node with beveled generated
primitives improves finish, not authorship. At phone size, silhouette is the
design; surface polish cannot compensate.

**Required correction:** require a black-silhouette review before materials.
Family members must differ in mass distribution, profile, negative space, and
attachment logic, not only color, count, or roof style.

### 4. Anatomy checks are too late and too literal

The game-wide ledger identifies 13 anatomy or identity failures. Owner review
has separately rejected incomplete butterflies and inaccurate shrimp, octopus,
and jellyfish. The current validators improved component counts, but a model can
contain six objects named `leg` and still have an implausible insect silhouette.

Claude's taxonomy has no dedicated anatomy code, which allowed visually pleasant
creatures to receive KEEP even when the review focused mainly on clutter and
concept fusion. The later pipeline added exact part counts, but not proportion,
joint placement, locomotion, overlap, or animation readability.

**Why this prevents 5:** technical completeness is mistaken for believable form.

**Required correction:** each creature needs a species-specific anatomy card,
silhouette overlay, side/dorsal views as appropriate, and motion-pose review.
Count checks remain a floor, never the verdict.

### 5. Functional roles are confused with visual variants

The Christmas tree issue exposed this clearly. Empty tree, five loose ornaments,
and completed tree are gameplay states, while decorated and undecorated scenery
trees are environmental roles. Similar risks exist for home versus inter-world
butterfly gates, dream/crown/chamber stars, fish body versus five fin pieces,
music bars, track signals, and protected paintings versus their frames.

The current pack documents these distinctions, but it did so after generation.

**Why this prevents 5:** art may be attractive yet redundant, unusable, or
incapable of representing the interaction sequence.

**Required correction:** write a state diagram and separation contract before
prompting or modeling. Audit the gameplay state, not just the filenames.

### 6. Repetition is treated as an edge problem instead of a composition problem

Claude found 22 terrain tessellation failures. The full-regeneration baseline
adds eight repetition/overdraw roles. The candidate pack fixed edge continuity,
but its own R044 rule warns that one Butterfly World meadow variant must never be
grid-repeated. Three seam-safe files still contain large recognizable blossom
motifs, so random selection reduces but does not remove pattern recognition.

The repetition galleries also show periodic seamount bands, caustic webs, stone
cells, floor blocks, and wood strips. Model families can repeat just as visibly:
identical palm rhythm, coral bases, house proportions, and barrier spacing expose
the generator even without texture seams.

**Why this prevents 5:** the asset passes alone and fails as a field, route, or
horizon.

**Required correction:** review 3x3 textures, 20-50 instance scatter fields, and
actual camera fly-throughs. Large landmark motifs wrap once; repeated surfaces
use low-frequency stochastic variation and independent dressing.

### 7. The 2D and 3D pipelines do not share one finish language

The new 3D corpus uses texture-free embedded flat materials. The 2D outputs use
strong painted contours, internal brush variation, and at times dense illustrative
detail. Fairy relief models form a third pipeline with baked imagery on white
geometry. The four-day audit already identifies those models as reading "from
another pipeline."

Specific candidate risks include the dense white web in R007 caustics, which the
style guide explicitly discourages; the painterly, high-frequency R044 meadow;
and picture-game sprites whose heavy outlined illustration is more detailed than
the smooth flat-material world around them.

**Why this prevents 5:** each asset may be appealing, but the game does not look
as though one art director chose the edge weight, cel-band shape, grain, and
material response.

**Required correction:** define a shared rendered finish board containing one
approved 2D sprite, one 3D prop, one creature, one architecture piece, and one
tile under the actual Mobile grade. Every pipeline must match that board at
gameplay size.

### 8. Palette consistency is substituting for material identity

Claude records 24 palette-bleed failures. Later procedural work solves the worst
recoloring but overuses the same coral, lavender, aqua, mint, cream, gold, and
indigo set across unrelated regions. Wood, stone, snow, glass, cloth, coral, and
metal can become differentiated mainly by color rather than edge treatment,
value grouping, or controlled roughness.

The latest technical audit praises 144 distinct base colors and a higher material
count. Those are implementation facts, not quality evidence. The bathroom sink's
18 materials are correctly identified as export debt; more slots are not more
art direction.

**Why this prevents 5:** local color survives, but tactile and regional identity
remain weak.

**Required correction:** build a material response chart by substance and biome.
Judge value bands and highlight shape in grayscale before approving hue.

### 9. Scene composition is deferred until after asset production

The full-regeneration baseline records 11 scale/occlusion failures, nine missing
runtime-validation failures, three exposure/bloom failures, and multiple broad
world-composition residuals. Reef hub, portals, Sky Lagoon, Butterfly World,
castle halls, kart presentation, and Northern approaches have all demonstrated
that good source assets can fail because of density, camera, scale, lighting, or
route framing.

Whole-world "composition kit" GLBs in an isolated gallery do not prove that the
state owner, procedural builders, camera, lights, and touch HUD can use them.

**Why this prevents 5:** the quality of the child's view is not the sum of the
asset files.

**Required correction:** stage focal assets in the real scene before producing
the rest of their family. Capture child-height approach, gameplay, reverse,
near, and transition views with HUD and player visible.

### 10. Batch scale suppresses art-direction feedback

The project moved from 30-50 samples to 100-item blocks and then to game-wide
regeneration. This is efficient only after a family has a 5/5 reference. Before
that point, batch generation replicates the same mistaken assumptions hundreds
of times: identical bevel language, the same palette, generic anatomy, and
similar decoration density.

**Why this prevents 5:** variation count increases faster than design learning.

**Required correction:** until one representative from a motif family is owner-
accepted at 5/5, cap that family at 6-12 candidates and spend the remaining time
on rejection analysis. Scale only after the reference asset and runtime setup
are locked.

### 11. The generator and auditor are insufficiently independent

The full-regeneration generator, stress scripts, galleries, and finalizer form a
strong technical QA system. They are not an independent art director. The same
system that produced the assets assigned every generated role 4/5 and supplied
the same review sentence to 71 roles.

**Why this prevents 5:** the audit confirms its own assumptions and has little
incentive to reject a coherent batch.

**Required correction:** separate maker and reviewer contexts. The reviewer sees
book references, runtime captures, role contracts, and anonymous candidate IDs,
but not generator intent or prior scores. Owner acceptance remains final.

### 12. Superseded and unused art obscures the real quality bar

The four-day audit finds 11 orphan GLBs and roughly 150 duplicate/byproduct
textures. Northern alone contains an obsolete six-piece pass-3.5 kit alongside
the stronger 17-piece authored kit. The full-regeneration pack adds another
17 Northern candidate models whose simple box-house language is not clearly an
improvement over the integrated timber, carving, stone, and rope kit.

**Why this prevents 5:** reviewers can inspect or promote the wrong generation,
and parallel "success" folders make quantity look like progress.

**Required correction:** maintain one role registry with `active`, `candidate`,
`rejected`, `superseded`, and `protected` states. A new candidate must identify
the active asset it intends to beat and demonstrate the improvement side by side.

## Current candidate-pack critique by area

These are not new official scores. They identify why the isolated candidates do
not yet demonstrate 5/5.

| Area | Positive movement | Remaining ceiling blocker |
|---|---|---|
| Reef | Complete creature parts, six coral profiles, modeled foliage | Hub/portal are schematic miniatures; coral and rocks remain generically procedural; mass placement and exposure unproven |
| Sky Lagoon | Cloud contrast improved; castle family is coherent | Cloud shelf can read as a platform; castles/trains remain box-and-cone toys; rainbow route and world composition untested in scene |
| Castle | Stars have distinct silhouettes; props are functionally separated | Halls, stairs, columns, doors, throne scaffold, and several furniture pieces remain simplified modular blockouts |
| Butterfly World | Complete wings/legs/antennae; gate roles documented | Gate profiles remain closely related; butterflies are generic decorative species; planet surface is high-frequency and conditionally repeatable |
| Dungeon | Every role exists and creature components are named | Enemies, arena, symbols, crystals, and shell props share a simple procedural grammar; no full candidate-room capture matrix |
| Kart | Separate pads, barriers, vehicles, boost, and finish roles | Vehicles are box-bodied toys, coral is reused rather than track-specific, and track-wide readability is unproven |
| Northern | Full 17-role coverage and readable winter palette | Candidate houses/landmarks are simpler than the already integrated authored kit; regeneration did not establish a side-by-side improvement |
| Undersea additions | Clear family separation | Jellyfish, fish, urchin, kelp, and coral remain simplified studies; anatomy and scatter behavior need in-game review |
| 2D materials | Correct dimensions, alpha, and edge matching | Several tiles remain visibly periodic or too painterly; R007 and R044 conflict with the guide's quiet broad-band surface language |
| Picture games | Strong isolated silhouettes and functional Christmas/fish separation | Contour weight and painterly detail do not yet prove unity with the 3D world; assembly and animation states need runtime captures |

## Audit-policy contradictions to resolve

1. `ART_SCORING_GOVERNANCE_2026-07-18.md` removes automatic 5/5 for provenance,
   while the full-regeneration ledger still assigns carrot and watering can 5/5
   solely because they are source-locked. Their **identity art** should remain
   protected and treated as authoritative; their **runtime presentation** should
   be scored separately.
2. The 2026-07-16 hard gate says unrouted candidates without runtime screenshots
   cap at 2/5. The current isolated pack labels all 85 candidates 4/5. Rename the
   label or stage the candidates before using a numeric score.
3. Northern is described both as 3/5 provisional, 4-ready, and the reference
   example for the accepted stress loop. One canonical role registry should own
   the current score and evidence links.
4. A family score may not hide a poor member, yet batch finalization assigns every
   file and role the same score. File-level visual review needs distinct notes or
   explicit "not individually reviewed" status.

## Revised path to 5/5

### Stage 1 - Role contract

Before generation, record:

- gameplay function and states;
- protected/source-derived status;
- canonical book pages and approved in-game comparison;
- silhouette and anatomy/growth-habit requirements;
- camera, scale, motion, attachment, and collision contract;
- forbidden motifs derived from Claude F1-F10;
- repetition density and biome placement.

### Stage 2 - Reference-quality design proof

Produce a small concept set for one representative family member. Review:

- black silhouette at actual phone size;
- front/side/back or dorsal/side views as appropriate;
- two or three color blocks in grayscale and color;
- complete functional parts without decoration;
- side-by-side comparison against the active asset and source pages.

Do not generate the family until this reference is accepted.

### Stage 3 - Family and material proof

Build three structurally different members and one material test. Reject the
family if silhouettes collapse when blacked out, if local materials read only by
hue, or if any member introduces a generic global motif.

### Stage 4 - Runtime stress

Integrate behind a reversible candidate switch and capture:

- near, mid, gameplay, reverse, and transition views;
- motion extremes for animated assets;
- 3x3 tiles and dense scatter fields;
- bright and shadowed Mobile-renderer conditions;
- player, HUD, touch controls, objective pointer, and route sightlines;
- target-device frame time and overdraw where relevant.

### Stage 5 - Independent review

Use six separate pass/fail axes:

1. source identity or motif truth;
2. silhouette and anatomy;
3. line, value, color, and material unity;
4. gameplay function and state separation;
5. runtime composition and repetition;
6. technical/mobile integrity.

The official score is limited by the weakest axis, not averaged. A 1 in anatomy
or function cannot be hidden by 5s in palette and file integrity.

### Stage 6 - Owner acceptance and registry update

Only an owner-accepted runtime evidence bundle becomes 5/5. Update one canonical
registry, archive the previous active version, and mark unsuccessful alternatives
as rejected or superseded rather than leaving them as ambiguous candidates.

## Highest-value next actions

1. Replace numeric `4/5 candidate` labels for unwired pack assets with staged
   evidence states, preserving numeric scores for runtime roles.
2. Build five motif-specific reference boards: coral/reef flora, butterflies and
   beetles, plants, architecture/vehicles, and picture-game craft art.
3. Select one difficult representative from each board and take it through the
   complete 5/5 loop before producing more family members.
4. Stage and re-audit R007, R008, R044, clouds, both butterfly gates, kart
   vehicles, and the Northern candidate kit first; they expose the dominant
   repetition, generic-geometry, role-differentiation, and improvement-proof risks.
5. Add anatomy proportion/pose checks beside component-count validators.
6. Quarantine orphaned, byproduct, rejected, and superseded art from the active
   registry and APK export while retaining source history.
7. Require every future audit to state exactly which evidence is new: file parse,
   isolated render, runtime capture, target-device capture, or owner acceptance.

## Final diagnosis

The project is no longer primarily suffering from broken files or raw placeholder
art. It is suffering from **premature convergence**: a competent shared palette,
rounded geometry, and successful import pipeline create the appearance of a
finished art system before motif truth, structural variety, runtime composition,
and owner-level specificity are complete.

Claude's audit already identified the generator's instinct to add theme instead
of preserve identity. The later human audit identified the engineering audit's
instinct to count routed replacements instead of judge the screen. The current
candidate pack solves many technical failures but repeats the same governance
mistake when isolated gallery success becomes a blanket 4/5.

The route to maximum potential is therefore not another larger generation batch.
It is a smaller, adversarial, motif-specific loop in which every candidate must
beat the active asset in the real game, survive family/repetition/anatomy stress,
and earn an independent owner acceptance before the pipeline scales it.
