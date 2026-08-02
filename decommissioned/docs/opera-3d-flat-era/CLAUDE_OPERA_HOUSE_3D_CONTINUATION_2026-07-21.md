# Claude handoff — Pearl Opera House 3D continuation

## Source of truth

Use the flat prototypes in `assets_src/concepts/opera_house_flat/` as the
visual source of truth. Start with
`opera_house_master_scene_key_2026-07-21.png` and
`opera_house_upper_floor_access_kit_2026-07-21.png`. The lobby is the primary
playable stage; the auditorium/backstage sheets are secondary.

Do not use the earlier realistic or mesh-first experiments as style targets.
Do not modify protected book art, family voices, or friend cutouts.

## Required lobby state

- Exactly twelve career portals, four per floor.
- Ground portals active at first entry.
- Middle and top portal curtains closed/dim until their floor unlocks.
- Both stair entrances use closed shell-clasp gates with three dark pearl
  sockets at first entry.
- Both bubble lifts are dormant while their destination floor is locked.
- Keep every central, portal, stair, lift, and ramp lane clear.
- Service and lounge props live in side zones and under-stair bays.

The flat pack provides 108 lobby-first cards and 64 stage/act cards. The exact
mapping is `audit/opera_house_flat_prototype_ledger_2026-07-21.csv`.

## Code integration map

Keep state on `ReefMain` and extract/build mechanically around the existing
logic.

| Runtime builder | Replacement responsibility |
|---|---|
| `scripts/opera_house.gd::_build_lobby` | Modular floor, wall/cove, balcony, stair/ramp, balustrade, chandelier, furniture, service, and decor kit. |
| `scripts/opera_house.gd::_build_doors` | One instanced portal frame with per-act curtain/crest/material parameters and active/locked/completed states. |
| `scripts/opera_house.gd::_build_boss_spots` | Pearl-rosette inlay and dark/lit crest states. |
| `scripts/opera_house.gd::_build_lifts` | One cheap tube, shell locking ring, landing trim, and capped bubble emitter per lift. |
| `scripts/opera_act.gd::_build_theatre` | Proscenium, house curtain, apron/footlights, pit, boxes, seating, and scenic-flat modules. |
| `scripts/opera_act.gd::_build_backstage` | Boards, crates, fly/counterweight, costume/work, practical-light, and curtain-gate modules. |

## Upper-floor unlock logic

The current runtime lifts cycle through all floors regardless of progress.
That behavior does not match the accepted concept and must be changed during
integration, not hidden with decorative gates.

Use the existing `m.opera_stars` bitmask; no save key is needed:

- Story 1 / ground is always unlocked.
- Story 2 / middle unlocks when the floor-1 boss bit (act index 4) is earned.
- Story 3 / top unlocks when the floor-2 boss bit (act index 9) is earned.

Suggested helper contract:

```gdscript
func _floor_unlocked(story: int) -> bool:
	if story <= 1:
		return true
	var prior_boss := 4 if story == 2 else 9
	return (m.opera_stars & (1 << prior_boss)) != 0
```

Gate, portal, selector, and lift visuals should all consume that same helper.
When the child approaches a locked gate/lift, do not fail or push them away
harshly: play the existing hint voice path, pulse the three pearl sockets, and
move the golden pointer toward an unfinished reachable show. When a floor
unlocks, open both relevant gate leaves fully, enable the lift destination,
light the floor-color shell, and play the short bubble/pearl/ribbon burst.

## Modeling order

1. Architecture modules and the 12-portal instance system.
2. Closed/open gate, clasp, three-pearl progress, and lift states.
3. Floor zoning materials, chandeliers/sconces, and wall-bound decor.
4. Ticket/coat/program and flower/sweets service bays.
5. Four compact lounge islands.
6. Supporting auditorium/backstage kit.
7. Act props only after the lobby passes its Mobile-render audit.

Each step should be reviewed in the same fixed camera set from
`scripts/probe_opera_art.gd`. Reject any 3D interpretation that loses the
prototype silhouette, replaces broad cel planes with realistic materials, or
scores below 4.5/5.

## Mobile constraints

- Godot Mobile renderer only; Speedy is the default.
- No new OmniLights. Use the existing directional light plus baked/emissive
  fixture materials.
- Instance repeated portal, rail, column, chair, plant, and sconce meshes.
- Use shared palette/material atlases and textures no larger than 1024 px.
- Keep lift transparency to one layer per visible tube; cull the far lift when
  practical.
- Use simple static collision, especially on stairs and gates. Open gate leaves
  must fold outside the navigation volume.
- Cap unlock particles aggressively; bubbles and pearl glints can be sprites.
- Preserve the current friend cutouts exactly until their approved gen2 GLBs
  land.

## Validation

Before pushing any 3D implementation:

1. Run the GDScript parser and inference lint on changed scripts.
2. Capture the 30-view opera set under Mobile rendering.
3. Verify the initial shot visibly blocks both upper routes.
4. Verify each unlock state opens the correct floor and does not expose the
   next floor early.
5. Run `scripts/ci.sh` and require all trusted probes to pass.
