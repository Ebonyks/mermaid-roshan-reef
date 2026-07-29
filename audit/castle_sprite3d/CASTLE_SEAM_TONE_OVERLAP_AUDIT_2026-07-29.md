# Pearl Castle seam, tone, and overlap audit — 2026-07-29

## Verdict

The accepted 3344 x 941 Main Hall reconstruction contains two different
classes of joins:

- The four horizontal splits and the vertical splits at x=836 and x=2508 are
  correct lossless tile boundaries.
- The x=1672 boundary between the independently authored Screen A and Screen B
  masters is an art-direction discontinuity, not a slicing error. Wall
  material, floor value, and the architectural baseline all change there.

The accepted masters and eight lossless runtime tiles remain unchanged.
Runtime now turns the source discontinuity into an intentional architectural
transition using an approved open-corridor extraction as a shaded Sprite3D card
at real depth. The same card supplies the missing physical Playroom entrance.
The final junction capture has no rectangular floor patch or framed-picture
treatment.

Final verdicts from `tools/audit_castle_tile_tone.py`:

| Gate | Verdict |
| --- | --- |
| Internal tile splits | PASS |
| Source A/B join | FAIL — retained and documented in immutable masters |
| Runtime A/B join | PASS — architectural Sprite3D bridge |
| Runtime castle-room tone | PASS |
| Fixed-elevator prop clearance | PASS |
| Speedy card/light budget | PASS |

## Programmatic seam evidence

The metric is the mean absolute RGB change at the boundary divided by the
average one-pixel gradient immediately beside it.

| Boundary | Mean abs RGB | Relative to local gradient | Result |
| ---: | ---: | ---: | --- |
| x=836 | 6.5427 | 1.0246 | normal lossless split |
| x=1672 | 69.3280 | 8.2103 | source art-direction discontinuity |
| x=2508 | 6.2738 | 0.9889 | normal lossless split |

At x=1672 the architecture band is 72.4362, runner band is 81.9479, and
foreground-floor band is 51.1746. These measurements reject the idea that the
problem came from tile scaling, crop drift, padding, or import loss.

Machine-readable evidence:
`audit/castle_sprite3d/castle_tile_tone_audit_2026-07-29.json`.

Annotated source reconstruction:
`audit/castle_sprite3d/castle_tile_seam_audit_2026-07-29.png`,
1672 x 470, SHA-256
`5c5e587a3db769dc4a380f53ae51ce217808970af4a5205c3bf8ceae453e2c9f`.

## Runtime repair and overlap correction

`castle_playroom_portal_reuse.png` is a 250 x 412 exact-pixel extraction from
an accepted open Main Hall corridor. Only its arch, corridor, and jamb
silhouette own alpha. It is not a rescaled background patch and contains no
new painted pixels.

- asset SHA-256:
  `2b7e52e0c91778967c88475dfb2eaf045be8c12b7986169323f7619cfb356f2c`
- runtime junction capture:
  `main_hall_seam_bridge.png`, 2560 x 1369, SHA-256
  `84518f00468d67b17b639748f78efeb94902e73dad6fc76e01f1acbc720bb1eb`
- marker: unchanged project dust-bunny family Sprite3D
- Playroom hotspot: 244 x 414 logical-art pixels, routed to the new entrance

The obsolete left tapestry was removed from the same socket. Lower-lane shell
and family bunnies were moved outside the fixed Storybook elevator footprint.
The focused probe verifies all four interaction sprites remain clear.

## Lighting tone and fixture discretion

The earlier 1024 x 1024 navy mounted sconce assembly was rejected in play
review because it read as a UI button. It remains only as a preserved audit
source and is not loaded by the game.

Each of the six runtime fixtures now uses
`castle_sconce_glow_reuse.png`, a 176 x 176 circular exact crop of the accepted
sconce's pearl core, SHA-256
`13480cad46b3b9a5ab87bd0ce0e75550bdf56779df834314d231bd9ad8a8628f`.
The glint sits over the existing architectural lamp housing. The touch target
remains at least 112 x 112, but the visible animation is only a 3.5-percent
pulse. The former star burst was removed. Tap still changes the real
SpotLight3D energy and plays the existing chime.

Background-weighted CIE Lab means were measured from current 2560 x 1369
Mobile-renderer captures. The seven destination rooms are the primary style
reference, as directed by the owner.

| Capture | Mean Lab | Delta-E76 to destination-room mean |
| --- | --- | ---: |
| Main Hall Screen A | 57.472, 17.701, -9.316 | 11.309 |
| Main Hall Screen B | 63.718, 12.310, -5.445 | 3.578 |
| Seven-room reference mean | 63.829, 12.027, -1.881 | — |

Both hall halves pass the audit threshold of Delta-E76 <= 12. Screen B is a
close match; darker Screen A remains within the accepted castle-room range and
retains the Opera/throne-wing mood.

Fresh live Sky Lagoon and Northern World captures were also made from this
checkout. They confirm the broader game uses a wider day/night and warm/cool
range than the castle rooms. They are retained as context, not substituted for
the owner's primary room reference. The Northern capture was made during its
entry overlay and the Sky Lagoon capture is its night state, so neither is
treated as a strict hue target.

## Final runtime node inventory

Main Hall maximum visible world inventory:

| Node/type | Count | Notes |
| --- | ---: | --- |
| shaded background Sprite3D | 8 | accepted 2 x 4 tile grid |
| shaded architectural Sprite3D | 1 | Playroom/junction bridge |
| unshaded structure marker Sprite3D | 1 | existing dust-bunny family |
| unshaded touch-item Sprite3D | 11 | six glints, one tapestry, four bunnies |
| player and contact-shadow Sprite3D | 2 | depth-sorted stage actors |
| visible Light3D | <=3 | one fill plus two visible-half clusters |
| Speedy shadow maps | 1 | pooled cap |
| modeled world art / CanvasItem world art | 0 | HUD remains Control-only |

Maximum visible Sprite3D cards: 23, below the probe cap of 26.

## Validation

Clean focused Mobile-renderer probe result:

```text
all_eight_rooms_sprite3d_only OK
all_rooms_use_multiple_real_depths OK
speedy_visible_card_budget OK maximum visible cards=23
main_hall_native_2x4_sprite3d_grid OK
main_hall_screen_join_architectural_bridge OK
main_hall_mobile_light_pool OK visible=3 shadowed=1
main_hall_fixture_and_tapestry_continuity OK
main_hall_touch_lighting_engine OK
main_hall_all_lights_off_affects_engine OK
main_hall_physical_portal_inventory OK
main_hall_lower_lane_interactions OK
main_hall_interactions_clear_fixed_elevator OK
main_hall_two_screen_camera_travel OK
RESULT=OK checks_failed=0
```

Primary runtime captures:

- Screen A:
  `main_hall.png`, SHA-256
  `f1fc72500dfffb4cd77153ee85f5126245f5cc321c234f00daf8e23382753c2a`
- junction:
  `main_hall_seam_bridge.png`, SHA-256
  `84518f00468d67b17b639748f78efeb94902e73dad6fc76e01f1acbc720bb1eb`
- Screen B:
  `main_hall_screen_b.png`, SHA-256
  `f925e1be1974d40f0bac55d368184bd98a0064f7ef9b6fd423a52591913499c1`
- Screen A all touch lights off:
  `main_hall_lights_off.png`, SHA-256
  `315c7d3a31b35945b445d6ad1943904c19ef27577017e2322352355a9a4c4a95`

No ImageGen call was used in this correction pass. The earlier castle ceiling
remains 25/25.

## Subjective re-audit

| Goal | Score | Result |
| --- | ---: | --- |
| Fixture integration/discretion | 4.7 / 5 | pass |
| Tile reconstruction correctness | 4.9 / 5 | pass |
| Runtime junction continuity | 4.5 / 5 | pass |
| Castle-room lighting tone | 4.6 / 5 | pass |
| Child interaction clearance | 4.7 / 5 | pass |
| Overall | 4.68 / 5 | accepted |
