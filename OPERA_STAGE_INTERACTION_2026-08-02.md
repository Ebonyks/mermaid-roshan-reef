# Opera stage interaction system — 2026-08-02

Phase-2 rebuild of the career worlds per the owner direction: the painted
worlds ARE the stages, not backdrops. Sits on OPERA_2D_REBUILD_2026-08-01.md.

## What changed

1. **Stage geography** (`scripts/opera_stage_paths.gd`): every painted world
   carries a walkable route (normalized waypoints tracing the PAINTED
   walkways), 4-5 task stations anchored to real painted landmarks, and 8
   magnifier clue spots. Derived visually per painting; helpers give
   arc-length interpolation, nearest-point, and screen conversion. Careers
   without data (nursery, until its painting lands) use a safe fallback arc.
2. **Roaming stage combat**: scuffle imps now wander the painted route
   (depth-scaled, direction-flipped, hop-bobbing) instead of bouncing in a
   panel. TAP an imp or SWEEP A SWIPE through it to bop (segment-vs-reach
   hit test, one hit per imp per stroke); stray taps fizzle-trickle. The
   captain still arrives when the crew thins and reserves his two bops.
   State sprites: idle -> bopped (spin/fade); costumed crews use the rival
   slices, co-op careers the dedicated imps.
3. **Point-and-click task flow**: non-combat phases belong to painted
   stations visited left-to-right; Roshan glides along the route to each
   station (flip-facing, depth-scaled), the station pulses until done, and
   the task opens in a compact card DOCKED BESIDE the station.
4. **The magic magnifying glass** (detective LENS/SEARCH): a full-stage
   draggable lens; sparkles hide at painted details and glow only under
   the glass (dwell 0.45 s to collect, ghost-lens demo until first touch).
   The generic hold/tap phases it replaces are gone.
5. **Storybook task cards**: the giant navy overlays are gone. Task cards
   use the exact menu language (StorybookUI): paper fill #E6F5FF, 5 px
   PURPLE->PURPLE_DEEP contour, radius 44, violet drop shadow, gold ribbon
   title, corner pearls; the gesture window is a light paper inset.

## Walkability notes per painting (from the visual derivation)

- **astronaut**: The route runs along the pale paved ledge (y~0.72) then steps down onto the right-hand pier (y~0.63); the small teal dome huts and pipe pedestals sit slightly in front of the path and can occlude feet, and no character should stand below the cliff face (y>0.78), beyond the pier's right edge, or in the water/sky gaps between floating rocks.
- **ballerina**: Everything below the raised causeway is dense non-walkable flower garden (with a sheer drop under the bridge gap around x 0.50-0.62), the upper-left terrace garden with its fountain circle is unreachable background scenery, and the tall filigree lantern near (0.72, 0.65) is a foreground occluder a character should never stand behind.
- **boxer**: The bottom band of blue rope-wrapped cushions and coral (below y~0.78 across most of the frame, ~0.72 at far left) is a foreground occluder where no one should stand, the water gap beneath the rope bridge (x 0.66-0.83) is swim-space only, and the punching-bag platform top is a raised tier (~y 0.60) reached by small steps, so the route stays on the lower mat level in front of it.
- **candymaker**: The strip below the gold balustrade (y > ~0.82) is a sunken foreground terrace of giant jars and berry planters where characters must never stand, and the candy-character conveyor belt (y ~0.30-0.40) plus the taffy-press pedestal (x 0.33-0.48, above y ~0.77) are elevated non-walkable scenery the route skirts in front of.
- **chef**: The teal water pool inset under the footbridge (roughly x 0.53-0.63, y 0.55-0.64) is unwalkable and must be crossed via the bridge arc; the bottom foreground strip below y~0.72 is a separate lower ledge crowded with rope stanchions and oversized dessert props that would occlude a character, so gameplay should stay on the mid-level candy-edged promenade.
- **detective**: The glowing paw-print-to-bow clue trail marks the walkable mid-level walkway (y~0.54-0.56); the row of dark alcoves and the fenced bottom terrace below y~0.62 are a separate lower floor off the route, so characters should never stand inside alcove interiors, below the walkway railing curve (x 0.66-0.87, y>0.58), or in the dark foliage occluders in the extreme corners.
- **doctor**: The sunken teal canal, waterfall, fountain bowls, pool basins and teal-tiled retaining walls are non-walkable; the route leaves the booth promenade down the bandage-decorated ramp at x~0.63 (the last three booths at x&gt;0.7 sit on the upper walk beside, not on, the descending route), and characters should not stand on the purple exam cushions or inside building doorways.
- **farmer**: The white picket fence and dense flower border across the bottom (below y ~0.72) is foreground occluder where a character should never stand, and the hills/sky above y ~0.40 are unwalkable except the barn-door spur and the picnic blanket at upper-right; the hay-bale stack itself should be treated as scenery, with the character standing at its base.
- **magician**: The bottom band (y > 0.82) is a foreground occluder of rope stanchions and coral where a character should never stand; all water (canals under the two bridges, the small left basin, and the big right pool) is non-walkable, so the route must cross on the long bridge deck (waypoints 4-6) and follow the glowing star-tile trail, which bends sharply upward at the door gallery — cutting the corner between waypoints 7-9 would clip the pool's left edge.
- **painter**: The turquoise channel between bridge and right bank (x 0.63-0.78, y 0.60-0.80) is water (only the arced bridge or the stepping stones cross it), and the bottom ~20% of the frame is an oversized-prop occluder band (giant paintbrushes, brush cup, coral) where a character should never stand; the splat-topiary bed itself is decorative — stand on its front rim only.
- **popstar**: The rainbow road is the only crossing over the open-water gap between the plaza and the encore balcony (roughly x 0.55-0.85 below y 0.80 is water and sunken facades - never stand there); everything above y~0.50 is distant skyline backdrop, the coral beds along the bottom edge are foreground-only, and the mic stands and pearl lamp posts sit at the path edge as occluders characters should pass behind.
- **racer**: The bottom foreground (y > ~0.78) is an off-track seabed of coral, shells, and tire stacks that occludes the track wall, and the teal water pool inside the hairpin loop (x 0.64-0.74, y 0.51-0.58) plus the glass pearl-tube bridge across the top are decoration a character should never stand on.

## Validation

- probe_opera_2d (287 checks, 13 careers) and probe_opera_nursery still
  green: probes drive phases through the same `_on_gesture` pump contract.
- probe_opera_2d_balance simulates the new flow honestly: swipe strikes on
  roaming imps, drag-speed lens sweeps, cradle steering.

## Codex handoffs

- P6 in OPERA_CODEX_REGENERATION_REQUESTS_2026-08-01.md: the imp/rival
  animation-state program (fix list + 60-file state manifest + gate).
- P7 ibid.: task-card nine-patch frame, station marker, magnifier prop.
- P3-04/P3-05 stage scenes and the nursery painting remain open.
