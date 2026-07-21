# Northern Kingdom — Asset Batch 02 (Codex request list)

Requested authored GLBs for the redesigned 3-act northern stage
(`scripts/arena/northern_kingdom.gd`). Batch 01 (pass arch, peaks, pines,
mushrooms, six houses, dock, wisp) is fully integrated via `_north_prop`.
Everything below currently renders as procedural blockwork or is missing
outright — each item lists the code site it replaces so integration is a
one-line swap.

**Style contract (same as batch 01):** matte pastel storybook palette,
baked flat colors (no PBR maps), single mesh per GLB, base at origin,
longest footprint edge ~1.0 so `_fit_authored_prop` can scale by target.
Poly budget: props ≤ 2k tris, buildings ≤ 6k, hero pieces ≤ 10k
(Mali-G52 phone target).

## P0 — Castle (the finale must not be boxes)

| Asset | Contents | Replaces |
|---|---|---|
| `northern_castle_gatehouse` | Arched gate, twin mini-turrets, balcony, crenellated parapet; ~30u wide | box gatehouse in `_build_castle` |
| `northern_castle_wall_seg` | Curtain-wall segment w/ walk + merlons, tileable, ~20u | `_castle_wall` boxes + merlon loop |
| `northern_castle_keep` | Keep EXTERIOR shell only: layered massing, buttresses, window reveals, gabled roof, OPEN 11u door gap front-center (interior is built procedurally inside it) | keep walls/roof/buttress/window boxes |
| `northern_spire_cluster` | 3 angled ice spires + cone caps, staggered heights ~40/30/28u | central + satellite spire cylinders |
| `northern_hall_staircase` | Curved quarter-sweep staircase w/ banister + newel orb, LEFT variant (mirror for right); rise 11u over 27u run | stepped-box flights in `_build_grand_hall` |
| `northern_hall_fountain` | Frozen fountain: 3 tiers + arrested splash jets, translucent tips; ~9u wide | tier cylinders + jet boxes |
| `northern_hall_chandelier` | 6-orb glow ring + crystal drops, hanging rod; ~8u across | torus + orb cluster |
| `northern_throne_duo` | Two small ice thrones w/ gold finials, kid-scaled | box thrones on mezzanine |

## P1 — Forest POIs & variety (the walk must keep surprising)

| Asset | Contents | Replaces / where |
|---|---|---|
| `northern_birch_a` / `_b` | Autumn broadleaf, magenta and gold canopy variants — the pines need deciduous partners at full quality | gen2 `tree_fall`/`tree_fall2` stand-ins in `_forest_tree` |
| `northern_waterfall` | Rock lip + falling-water sheet + splash foam, ~10u tall | white cards + foam spheres at POI 1 |
| `northern_hollow_log` | Mossy fallen log, genuinely hollow (walk-through bore ≥ 4u) | log-on-stumps gate at POI 3 |
| `northern_crystal_cluster` | 5-shard ice crystal cluster, cyan/magenta glow tips | `_l2_box` shards at POI 4 |
| `northern_standing_stone` | Runed monolith w/ carved glyph face (star/snow/mountain/orb variants) | plain boxes + Label3D glyphs in clearings |
| `northern_spirit_altar` | Stacked-stone altar, moss + glow seam | 3 stacked boxes at clearing hearts |
| `northern_bramble_berry` | Low berry bramble, red fruit dots | (new understory scatter) |
| `northern_fern_clump` | Broad soft fern, 2 sizes | (new understory scatter) |
| `northern_picnic_set` | Bench + basket + blanket one-piece | kit bench at POI 6 |
| `northern_ruin_pylon` | Cracked leaning gate pylon + fallen capstone | boxes at POI 7 |

## P1 — Northern critters (Critter Book expansion, 4 species)

New `habitat: "forest"` page in `collection_system.gd` DEFS — model per
species like the existing 18, `wing_*`-named flaps where sensible:

| Asset | Species | Where it will live |
|---|---|---|
| `critter_glow_fox` | Glowfox (teal-tipped tail) | crystal grotto (POI 4) |
| `critter_moss_bunny` | Moss Bunny | fairy ring (POI 2) |
| `critter_ember_newt` | Ember Newt (safe fire-spirit nod: green body, GOLD flame) | waterfall pond (POI 1) |
| `critter_star_finch` | Star Finch | castle forecourt lanterns |

## P2 — Town & misc polish

| Asset | Contents | Replaces |
|---|---|---|
| `northern_mill` | Island mill: house + wrap deck + water wheel (wheel a separate node `wheel_*` so code can spin it) + log ramp | whole `_build_mill` blockwork |
| `northern_forge_porch` | Open smithy porch: posts, roof, anvil, glowing hearth | forge boxes in `_build_town` |
| `northern_market_stall` | Striped-awning stall w/ crates | (new, town street dressing) |
| `northern_lantern_post` | Wood post + warm glass lantern | post+orb pairs (town & castle variants: wood / ice) |
| `northern_palisade_seg` | 4-stake pointed palisade run, tileable | stake boxes at town gates |
| `northern_log_bridge` | Log footbridge w/ rails, ~12u span | deck boxes at stream crossing 2 |
| `northern_bed_set` | Kid bed + quilt + pillow (3 quilt colors via tint) | box beds in bedrooms |
| `northern_toy_chest` | Toy chest w/ cracked-open lid | box chests in bedrooms |

## Future (blocked on design, listed for planning)

- **Spirit bosses** for the two clearings — safe stylized variants only:
  wind swirl (leaf vortex), river horse (translucent toon water), stone
  giant (mossy boulders), ember newt grown large. No Disney silhouettes,
  no blue-salamander-with-magenta-flame, no four-diamond glyphs.
- `northern_hall_interior_kit` (pillar, vault rib, arched window frame)
  if we later replace the procedural hall shell wholesale.

## Integration notes for whoever wires these in

- Register each GLB in `NORTH_ASSETS` (northern_kingdom.gd) and swap the
  named build site to `_north_prop(kind, pos, target, yrot)` — collision
  solids are already analytic and stay as-is.
- Keep `north_authored_asset_family_count` / instance probe expectations
  in `scripts/probe_northern.gd` in sync when adding families.
- Critters: add DEFS rows with `context: "north"`, then call
  `collection.spawn("north")` from `_enter_northern_kingdom` — the
  catch/HUD/book flow is context-driven and needs no other changes
  (HUD total updates automatically from DEFS size).
