# Reef Grand Prix roadside art

The 2026-11-07 owner review asked for a complete upgrade beyond the now-clear road edges. The desktop work starts from `c97a4cc6f8b60522c5de782842325ed9984d54c6`. At that revision, the route and props were easy to recognize, but bare ground separated most individual fixtures from each other and from the room walls. The new roadside uses the same canvas and chase projection as the karts.

## Reference observations

- In the original Super Mario Kart image, the edge blocks and sandy shoulders set a steady rhythm. Big green slopes sit behind a clean horizon, and the bend reads instantly in split-screen. Sparse scenery leaves room for driving, but stretched simple ground and interchangeable distant props offer few cues about which part of a lap a player is in. [Nintendo game overview](https://www.nintendo.com/en-gb/Games/Super-Nintendo/Super-Mario-Kart-279580.html) · [Original gameplay image](https://images.nintendolife.com/191dc4028a526/super-mario-kart2.large.jpg)
- Ribbon Road makes the course feel toy-sized by showing oversized objects at different distances, with low repeating elements at the racing edge. Donut Plains 3 uses shoreline, timber and rock to connect the bridge to a place. Sweet Sweet Canyon groups similarly shaped sweets into a skyline and lets a few tall silhouettes rise above it. Electrodrome uses a recognizable run of stage frames. Dense, high-contrast details in an inside turn would compete with the curb and item silhouettes, especially in a half-width view. Reef applies the depth, material changes and pacing with lower foreground shapes and gaps between the large landmarks. [Nintendo course gallery](https://www.nintendo.com/sg/switch/aabp/sp/course/index.html)
- Nintendo's designers describe gradual transitions and landmarks that orient players between areas. Reef keeps distinct groups within a room and uses its own painted floor and repeated low shapes to link them. Reference images were used for study only. [Nintendo developer interview](https://www.nintendo.com/au/news-and-articles/ask-the-developer-vol-18-mario-kart-world-chapter-2/)

## Room construction

| Course | Foreground and midground |
|---|---|
| Playroom | Low toy chests and display decks bring blocks, stacking toys, the tent and the music box down to furniture level. Small matching toys sit on the opposite benches. |
| Kitchen | Four cabinet banks stage tea, cooking, cold storage and washing. Existing teapot, oven, fridge and sink become the silhouettes, with separate pot and pan details across the road. |
| Mermaid Pool | A dry towel alcove gives way to low tiled fountain, float and waterfall basins. Existing pool water fills the latter three. Low coping and coral indicate the pool before the large fixtures arrive. |
| Opera Hall | A lobby display, instrument platform, stage and backstage bay have different deck heights. Gold molding, low footlights and small stars connect the groups without competing with the curtain or fixtures. |

Each of the sixteen scenes has one main bay, one low trim and one opposing bench. World placement checks each box against the track rail samples and other structures. Props and their shadows rest at the deck height. Turn signs close to furniture mount on its road-facing side. Each camera clips and sorts the same shared scene independently. Canvas polygons use perspective-correct UVs, and the four imported painted materials share a single mipmapped atlas. Road footprint, markings and driving layout follow the previous version. The moving review exposed a finish-arch strip that collapsed at a nearly edge-on angle in Opera split-screen. Subpixel arch strips are skipped before triangulation.

The new atlas supplies flat frontal material unavailable in the room inventory. Existing cast, fixtures and room art supply the rest, including the new shoulder finish. [Atlas provenance and exact prompt](../../../assets_src/imagegen/reef_kart_roadside_20261107/generation_job.json)

## Runtime evidence

[Audit impact](../../../design/audit_impacts/reef-kart-roadside-20261107.json) · [Desktop evidence](../../../audit/cycles/reef-kart-roadside-20261107/RUNTIME_EVIDENCE.json)

[Playroom](../../../audit/cycles/reef-kart-roadside-20261107/playroom.jpg) · [Kitchen](../../../audit/cycles/reef-kart-roadside-20261107/kitchen.jpg) · [Mermaid Pool](../../../audit/cycles/reef-kart-roadside-20261107/mermaid_pool.jpg) · [Opera Hall](../../../audit/cycles/reef-kart-roadside-20261107/opera_hall.jpg)

The posed views can be reproduced from the project root with the approved Godot build:

```text
godot --path . -s res://audit/cycles/reef-kart-roadside-20261107/capture.gd
godot --path . -s res://audit/cycles/reef-kart-roadside-20261107/drive.gd -- res://tmp/roadside/drive
```

Godot 4.7.2 Mobile screenshots and controller-driven laps provide desktop evidence. Tablet, physical controller, child and owner acceptance remain open.
