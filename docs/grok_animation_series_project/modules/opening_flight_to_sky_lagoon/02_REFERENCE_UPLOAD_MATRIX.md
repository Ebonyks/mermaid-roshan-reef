# Reference upload matrix

Reference names come from the shared `characters/` and `locations/sky_lagoon/` libraries. The airplane alone lives under this module's `references/` folder. Order matters: the first image is the strongest authority for the requested composition. This avoids storing duplicate copies of the same canonical art in Git.

Path map:

- `01_SKY_LAGOON_FINAL_GEOGRAPHY` → `../../locations/sky_lagoon/01_SKY_LAGOON_FINAL_GEOGRAPHY.jpg`
- `02_CASTLE_EXACT_FOUR_TOWER` → `../../locations/sky_lagoon/02_CASTLE_EXACT_FOUR_TOWER.png`
- `03_ROSHAN_FRONT_IDENTITY` → `../../characters/roshan/ROSHAN_FRONT_IDENTITY.png`
- `04_ROSHAN_REAR_POSE_SHEET` → `../../characters/roshan/ROSHAN_REAR_POSE_SHEET.png`
- `05_DADDY_FRONT_IDENTITY` → `../../characters/daddy_mermaid/DADDY_FRONT_IDENTITY.png`
- `06_AIRPLANE_EXACT` → `references/06_AIRPLANE_EXACT.png`
- `07_SKY_LAGOON_FULL_PANORAMA` → `../../locations/sky_lagoon/07_SKY_LAGOON_FULL_PANORAMA.png`

| Shot | Attach in this order | Why |
|---:|---|---|
| Character anchor: Daddy rear | `05_DADDY_FRONT_IDENTITY` | One identity authority; neutral study only. |
| Character anchor: handhold | `03_ROSHAN_FRONT_IDENTITY`, `05_DADDY_FRONT_IDENTITY` | Establish exact inner hand ownership. |
| 1 | `06_AIRPLANE_EXACT`, `07_SKY_LAGOON_FULL_PANORAMA` | Plane identity first; sky palette second. |
| 2 | approved cabin still, `03_ROSHAN_FRONT_IDENTITY`, `05_DADDY_FRONT_IDENTITY`, `06_AIRPLANE_EXACT` | Layout first, then character identities. |
| 3 | accepted shot-2 ending frame, `03_ROSHAN_FRONT_IDENTITY` | Continue Roshan and cabin lighting. |
| 4 | accepted cabin anchor, `05_DADDY_FRONT_IDENTITY` | Daddy close-up identity. |
| 5–10 | accepted previous ending frame, `03_ROSHAN_FRONT_IDENTITY`, `05_DADDY_FRONT_IDENTITY` | Sequential acting and hand/belt continuity. |
| 11 | accepted shot-10 ending frame, `04_ROSHAN_REAR_POSE_SHEET`, `APPROVED_DADDY_REAR`, `06_AIRPLANE_EXACT` | Rear movement and plane identity. |
| 12 | accepted shot-11 ending frame, `06_AIRPLANE_EXACT`, `07_SKY_LAGOON_FULL_PANORAMA` | Door direction and sky-only threshold. |
| 13 | approved route still, `06_AIRPLANE_EXACT`, `07_SKY_LAGOON_FULL_PANORAMA` | Countable route composition. |
| 14 | accepted shot-13 ending frame, `04_ROSHAN_REAR_POSE_SHEET`, `APPROVED_DADDY_REAR` | Step contact and rear identity. |
| 15 | accepted shot-14 ending frame, `03_ROSHAN_FRONT_IDENTITY`, `05_DADDY_FRONT_IDENTITY` | Side two-shot before reveal. |
| 16 | approved kingdom-side close-up still, `03_ROSHAN_FRONT_IDENTITY`, `05_DADDY_FRONT_IDENTITY` | Reaction faces; kingdom remains offscreen. |
| 17 still | `01_SKY_LAGOON_FINAL_GEOGRAPHY`, `02_CASTLE_EXACT_FOUR_TOWER`, `04_ROSHAN_REAR_POSE_SHEET`, `APPROVED_DADDY_REAR` | Placement first, castle design second, characters last. |
| 17 video | approved shot-17 still as starting image | Do not dilute the locked composition unless the interface allows explicit secondary references. |
| 18 | accepted shot-17 ending frame as starting image | Exact composition continuation; minimal motion. |

## Reference budget

- Use two to four references normally.
- Seven is a ceiling, not a target.
- If two images disagree, the prompt must name which controls composition and which controls appearance.
- Never mix rejected or obsolete castle variants with the accepted four-tower authority.
- Never attach the full panorama as the primary reference for shots 17–18; it does not contain the accepted castle placement.
