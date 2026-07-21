# Fable Kit Runtime Audit — 2026-07-19 (constructor self-audit, E3)

Auditor: Fable 5 constructor session, same day as the build (03c33e6).
Ruleset: `assets/OBJECT_GENERATION_AUDIT_LOG.md` v6 (R-GOV, R-GEO, R-MAT,
R-REP, R-QA), evidence classes E0-E4. Target bar per owner: **4/5 or greater
on aesthetics and performance; anything lower goes back to Codex for
revision.**

## Evidence base

- R-GOV1 export measurements: `tools/measure_fable_kit.py` output (below),
  parsed from the GLBs, not from the generator manifest.
- E3 runtime captures: `audit/fable_kit_mobile/` — Godot 4.7-dev2,
  `--rendering-method mobile` (confirmed in-run:
  `RenderingServer.get_current_rendering_method() == "mobile"`), 1280x720,
  child-height near/mid/far, station approach, boarding side, ride POV,
  castle-return context, low grazing track pan. Probe:
  `scripts/probe_fable_audit.gd`.
- Functional evidence: `probe_train.gd` full-lap clip sweep at 55 spd, zero
  guard hides; station dwell; phase hide/rebuild — all OK (the "glued"
  FAIL reproduces on the pre-kit base commit and is not kit-related).
- Two captures are INVALID under R-QA8 and were not scored from:
  `kelp_field_oblique` (camera clipped below terrain) and `boarding_view`
  (camera on the ring-inner side; platform is outboard). Re-capture is part
  of the revision order.

### Measured exports (R-GOV1)

| File | Tris | Mesh objs | Islands | Mats | Size (Blender xyz) |
|---|---:|---:|---:|---:|---|
| coral_bare_0.glb | 3040 | 1 | 1460 | 3 | 1.73 x 2.07 x 3.01 |
| kelp_vol_0.glb | 1248 | 1 | 15 | 3 | 1.65 x 1.82 x 3.58 |
| loco_body.glb | 2588 | 23 | 712 | 7 | 5.00 x 11.00 x 7.19 |
| track_straight.glb | 1512 | 1 | 756 | 3 | 4.60 x 5.01 x 0.75 |
| track_curve.glb | 8640 | 1 | 3888 | 3 | 14.29 x 14.29 x 0.75 |
| station_platform.glb | 1404 | 13 | 702 | 5 | 5.93 x 12.02 x 1.33 |
| station_shelter.glb | 1548 | 17 | 653 | 4 | 4.84 x 4.70 x 6.83 |

## Scores

| Item | Score | Verdict |
|---|---|---|
| r021A locomotive body | **4/5** | PASS — hold for owner review |
| r003 bare coral | 3/5 | REVISE |
| r004 volumetric kelp | 3/5 | REVISE |
| r021B straight track | 3/5 | REVISE (perf + value wash) |
| r021C quarter-curve track | 2/5 | QUARANTINED (no runtime role yet) |
| r021D station platform | 3/5 | REVISE (value wash) |
| r021E station shelter | 3/5 | REVISE (value wash + roof form) |

One of seven reaches the bar. Findings and revision orders below; the
cross-cutting cause first.

### Cross-cutting: pale-arena value clip (affects track, platform, shelter)

The Sky Lagoon's bright exposure pushes mid-value pastels past readable
saturation (known issue; see the arena exposure work: pale albedos clip near
ACES white on Mobile). Measured against the captures: tie lavender
(0.66,0.58,0.82), deck teal (0.45,0.78,0.76), skirt lavender and roof purple
(0.48,0.44,0.72) all render close to white at gameplay distance; only navy
and gold survive. **Rule: lagoon-placed kit albedos need a ~0.72-0.80
multiplier on value, keeping hue.** The reef flora does NOT need this (the
underwater tint darkens instead — see coral finding).

## Per-item findings

### r021A locomotive body — 4/5 (PASS)

- Identity unmistakable at near/mid/far and in silhouette against sky:
  stack, boiler + bands, dome, enclosed cab, warm window, finned
  cowcatcher, couplers (R-GEO1, R-GEO5 pass).
- Integrates with scripted wheels/rods/smoke; full-lap clip sweep clean;
  2588 tris one-off is negligible.
- Nits (do NOT block 4/5, fold into any future pass): cowcatcher fins read
  slightly detached at extreme near; funnel navy washes toward blue-grey in
  full sun.
- 5/5 requires owner acceptance of shipped views (R-GOV4) — out of scope
  for any agent.

### r003 bare coral — 3/5 (REVISE)

- PASS side: bare growth, direct seabed embedding, no pedestal, asymmetric
  crown, cream tips read at near (family directive #1 satisfied in form).
- F1 (aesthetics): underwater teal tint mutes the salmon pink to
  grey-lavender at mid distance; identity as "coral" weakens vs the sheet.
  Revision: warm and darken the body pink (target ~0.88,0.42,0.44) and
  brighten tip cream so the value step survives the tint.
- F2 (family, R-REP2): only one growth form shipped. The approved direction
  requires three genuinely different silhouettes (antler + plate/fan +
  compact bush) before mass placement is called covered.
- F3 (performance): flat-shaded export splits the mesh into 1460 islands →
  ~9.1k effective vertices; at 46 instances this is tolerable but wasteful.
  Revision: rebuild with smooth shading + explicit low-poly facet geometry
  (or autosmooth angle) targeting ≤1.8k tris and connected shells.
- F4 (evidence): no dense-field stress capture yet (R-REP1).

### r004 volumetric kelp — 3/5 (REVISE)

- PASS side: volumetric ribbons with purple backs, visible stems, open
  lower third, direct burial; integrates alongside legacy blades (family
  directive #2 satisfied in form).
- F1 (evidence, R-QA8): the near capture did not clearly frame a new-kelp
  instance and the dense-field oblique was invalid (camera under terrain).
  A valid sparse + dense field pair is REQUIRED before any 4/5 claim.
- F2 (family, R-REP2): one clump only; the direction requires sparse and
  dense structural variants.
- F3 (aesthetics): blade solidify is 0.05 — at far distance the ribbon edge
  can alias to a line; consider 0.07-0.08 on the widest two blades.

### r021B straight track — 3/5 (REVISE)

- PASS side: gauge/section per interface sheet; 240 segments tile the ring
  with no visible seams (verified in castle-context and side pans); rhythm
  of ties + gold plates reads as toy railway at side/three-quarter views.
- F1 (PERFORMANCE, blocking): 1512 tris x 240 instances = ~363k triangles
  for the ring vs ~4.3k for the old procedural rails+ties. This is the
  wrong budget for Speedy-tier Mobile (R-QA5: promotion must not regress
  frame time). Revision: target ≤400 tris/segment (≤96k ring): remove
  bevels from ties and plates (plain boxes), rail bevel one chamfer
  segment, drop hidden bottom/end faces where safe.
- F2 (aesthetics): at grazing/low angles the pale ties merge with the sand
  deck into a solid white causeway; the two-rail read disappears (R-MAT1
  value separation). Revision: ties to ~0.50,0.42,0.66 (keep hue), and/or
  narrow the tie top face; keep rails navy.
- F3 (minor): gold plates read as floating chips at grazing angle — merge
  them visually with the railhead (inset, not proud) or halve their height.

### r021C quarter-curve track — 2/5 (QUARANTINED)

- Geometry and gauge continuity are sound (E2), but the piece has NO
  runtime placement: the live ring is tiled by straights (chord sag 0.016)
  and no spur exists. Per R-QA6 it stays labeled reference-only and per
  R-GOV4 it cannot exceed structural evidence class.
- Path to 4/5 (Codex + constructor choice): give it a real role — e.g. a
  short decorative siding at the station or a child-scale toy loop
  elsewhere — then capture it in that role. Otherwise leave quarantined and
  exclude from APK export (currently it ships in assets/; move or mark).
- Also decimate (8640 tris is heavy for any single kit piece).

### r021D station platform — 3/5 (REVISE)

- PASS side: correct placement beside the dwell point, clear of the train
  envelope (clip sweep clean), non-solid, low boarding read, steps face
  away from rails.
- F1 (aesthetics): deck teal and skirt lavender clip to near-white at
  gameplay distance — the platform reads as an unpainted slab from the
  approach (R-MAT2). Revision: apply the 0.72-0.80 value multiplier; add a
  thin navy edge line under the cream rim (same trick the rails use) so the
  silhouette holds on the pale meadow.
- F2 (evidence): no valid boarding-side capture with the coach aligned at
  the platform (the one taken was from the wrong side). Required for 4/5.

### r021E station shelter — 3/5 (REVISE)

- PASS side: open sightlines on all approaches, posts clear of the
  boarding envelope, train and platform visible under it; framing the
  stone bench reads charmingly.
- F1 (aesthetics): roof purple clips to white; only the navy edge trim
  reads, so the roof looks like bare metal sheet. Same value-multiplier
  revision as the platform.
- F2 (form, R-GEO2): the capsule-arc roof is still primitive-convergent;
  the approved sheet shows a shallower, wider roof with a visible eave
  shadow line. Revision: flatten the arc (height ~0.35 of current), extend
  overhang ~0.3 per side, deepen the eave trim.
- F3 (placement intent): the shelter currently lands over the depot bench
  (unplanned but pleasant). Codex/constructor must either declare
  bench-under-shelter as the intended composition (and center it) or
  offset the shelter to the platform's far third.

## Adjacent finding (not a kit item)

Ride POV from the coach bench: the coach's solid end wall fills the forward
view while riding — the engine is invisible from the seat. Pre-existing
scripted coach art, not part of this kit, but it caps the experienced quality
of the whole train role; recorded here for the next coach pass (suggest a
half-height front wall or a wide front window).

## Handoff

All REVISE items return to Codex for image/spec-side revision where the
change is identity or color (coral color, tie/deck/roof values, roof form,
kelp variants, coral variants), and to the next constructor pass where the
change is geometry/perf (track decimation, coral shell rebuild, curve-piece
role decision). Branch: `claude/fable-constructed-models`; this audit and
the invalid-capture list define the acceptance tests for the next round:

1. Valid R-QA8 captures: kelp sparse+dense field, platform boarding side.
2. Track ring ≤100k tris total, ties readable as ties at grazing angle.
3. Flora color revisions verified under the underwater tint, station kit
   verified under lagoon exposure, both on Mobile renderer.
4. Coral x3 and kelp x2 structural variants before density increases.
5. Curve piece: role assigned + captured, or moved out of APK export.
