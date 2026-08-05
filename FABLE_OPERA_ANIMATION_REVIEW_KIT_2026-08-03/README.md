# Fable Opera Animation Review Kit — 2026-08-03

## Start here

This tracked folder is the portable, discoverable companion to
[`CODEX_OPERA_ANIMATION_HANDOFF_2026-08-03.md`](../CODEX_OPERA_ANIMATION_HANDOFF_2026-08-03.md).
It packages the five Mobile-renderer review masters that previously existed
only beneath the ignored `.godot/opera_animation_review_20260803/` build tree.

The PNGs are byte-for-byte copies of live Godot 4.7.1-stable review captures.
They are **visual QA evidence only**. They are not runtime art, sprite sheets,
source masters, cinematic frames, or delivery pixels. Do not crop, trace,
composite, edit, or reimport their pixels into the game. The folder's
`.gdignore` deliberately keeps all of it outside Godot's importer and exports.

## What is included

| Review master | Coverage | Use it to inspect |
|---|---|---|
| [`opera_imp_family_master_contact.png`](review_masters/opera_imp_family_master_contact.png) | 14 families; 56 live full-viewport frames; 14 family sheets | Identity lock, authored pose readability, foot registration, same-family fallbacks |
| [`opera_selected_scuffles_master_contact.png`](review_masters/opera_selected_scuffles_master_contact.png) | Opening and captain sequences for Chef, Detective, Ballerina, Candymaker, and Nursery; 77 frames; 10 sheets | Wind-up/charge/slash/recover order, FX anchors, contact clarity, bopped behavior |
| [`opera_12_rival_master_contact.png`](review_masters/opera_12_rival_master_contact.png) | 12 finale rivals at taunt and bow; 24 frames; 12 sheets | Costume continuity, final-stage acting, restored idle registration |
| [`opera_60_widget_master_contact.png`](review_masters/opera_60_widget_master_contact.png) | 60 widgets at idle/demo, active, near-complete, and accepted-complete; 240 frames; 60 sheets | Registration, gesture causality, child-readable motion, completion feedback |
| [`opera_stress_master_contact.png`](review_masters/opera_stress_master_contact.png) | One 20-tap rest frame plus five early exit/re-entry frames | Transform drift, lifecycle cleanup, repeat-input stability |

Exact byte counts, dimensions, source locations, and SHA-256 hashes are in
[`manifest.json`](manifest.json).

## Fable review workflow

1. Inspect the masters in this order: family, scuffle, rival, widget, stress.
2. Record each issue by master, family/career, state, and visible defect.
3. Inspect the corresponding runtime PNG and its live animation owner; do not
   use a contact-sheet crop as a replacement asset.
4. Fix runtime selection, registration, transform ownership, or gesture
   binding first. Generate art only after a capture documents an exact gap
   that the accepted art cannot fill.
5. Rerun the focused probe and make new windowed Mobile captures in an ignored
   `.godot/` review directory. Keep any replacement evidence out of runtime
   `assets/`.

Owner identity/topology/style review and a real Android Speedy-tier frame-time
capture remain pending. This kit is not final art acceptance.

## Runtime source map

Use the real source assets in place:

| Path | Contents |
|---|---|
| `assets/opera/worlds/actors/` | Mermaid Roshan, Faron, base imps, and rival-family states |
| `assets/opera/worlds/props/` | Goal props and combat FX |
| `assets/opera/worlds/widgets/` | 60 widget backdrops, movers, marks, fills, and shared layers |
| `assets/opera/worlds/ui/` | Task frame, station marker, and magnifier |
| `assets/opera/worlds/nursery/` | Nursery interaction art |
| `assets/opera/worlds/backdrops/` | Accepted static world plates |
| `assets/opera/worlds/stage/` | Accepted static finale plates |

Primary runtime owners:

- `scripts/opera_career_world_2d.gd` — actors, state resolution, scuffles,
  effects, rest transforms, rival finale acting.
- `scripts/opera_gesture_surface.gd` — gesture-driven widget layers and demos.
- `scripts/opera_imp_clips.gd` — shared imp clip names and timing helpers.

Focused gates:

- `scripts/probe_imp_animation_art.gd`
- `scripts/probe_imp_ai.gd`
- `scripts/probe_opera.gd`
- `scripts/probe_opera_2d.gd`
- `scripts/probe_opera_nursery.gd`
- `scripts/probe_passive.gd`

Known intentional fallbacks are neutral prowl to same-family idle, rally to
same-family taunt, and no `hop_a`/`hop_b` for the two base families. Never
cross from one character family to another to fill a missing state.

## Recapture on the repository workstation

Captures must be windowed. `probe_imp_animation_art.gd` verifies files but
intentionally skips screenshots under `--headless`.

```powershell
$GODOT = 'C:\Users\Peter\AppData\Local\Programs\MermaidReefTools\Godot\4.7.1\godot.exe'
$reviewRoot = Join-Path (Resolve-Path '.godot').Path 'opera_animation_review_YYYYMMDD'

$env:IMP_ANIM_SHOT_OUT = Join-Path $reviewRoot 'families'
$families = @(
  'imp_mischief', 'imp_captain', 'rival_chef', 'rival_detective',
  'rival_ballerina', 'rival_candymaker', 'rival_doctor', 'rival_farmer',
  'rival_boxer', 'rival_magician', 'rival_painter', 'rival_astronaut',
  'rival_racer', 'rival_popstar'
)
foreach ($family in $families) {
  $env:IMP_ANIM_CAPTURE_FAMILY = $family
  & $GODOT --path . --rendering-method mobile -s scripts/probe_imp_animation_art.gd
  if ($LASTEXITCODE -ne 0) { throw "Imp capture failed: $family" }
}

$env:OPERA_WIDGET_SHOT_OUT = Join-Path $reviewRoot 'widgets'
$env:OPERA_RIVAL_SHOT_OUT = Join-Path $reviewRoot 'rivals'
$env:OPERA_SCUFFLE_SHOT_OUT = Join-Path $reviewRoot 'scuffles'
$env:OPERA_STRESS_SHOT_OUT = Join-Path $reviewRoot 'stress'
Remove-Item Env:OPERA_SCUFFLE_CAPTURE_CAREER -ErrorAction SilentlyContinue
& $GODOT --path . --rendering-method mobile -s scripts/probe_opera_2d.gd
if ($LASTEXITCODE -ne 0) { throw 'Opera capture failed' }
```

Setting `OPERA_SCUFFLE_CAPTURE_CAREER` to one career (for example, `chef`)
captures only that scuffle and exits. With the selector unset, the harness
captures the selected review set. See the main handoff's verification and
acceptance sections before changing capture scope.

## Non-negotiable boundaries

- Do not modify, recompress, replace, or derive anything in `assets/book/`,
  `assets/audio/voices/`, or `assets/characters/friends/`.
- Gameplay whole-sprite animation is allowed here; authored cinematic frames
  remain subject to the repository's mandatory full-frame regeneration rule.
- Keep accepted world and stage paintings static. Do not fake motion by
  panning, warping, or moving the whole plate.
- Preserve the one-finger, no-fail contract and Mobile renderer limits.
