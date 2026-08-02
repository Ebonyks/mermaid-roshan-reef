# Mermaid Roshan Score-3 Rebuild Audit

_Audit and implementation date: 2026-07-15_

This is the game-wide follow-up to `ART_STYLE_AUDIT.md` and
`ART_FULL_INVENTORY.md`. It rechecks every family previously rated 3/5 against
current runtime references, then records the live replacement, material pass,
retirement, or protected exception. A raw source file is not promoted merely
because a stronger runtime route exists; the live route and retained source
inventory are scored separately.

## Result summary

- All unprotected, actively visible 3/5 families now have a rebuilt 4/5
  candidate route.
- Five terrain canvases were replaced in place, with byte-for-byte previous
  files under `backups/art_pre_score3_2026-07-15/`.
- Fourteen transparent story cards cover tropical foliage, flowers, mushrooms,
  fruit, and anatomically checked beetles.
- Crystal, ship, kit, arena, creature, and vehicle silhouettes were retained
  where their geometry or animation already worked; their visible material
  language was rebuilt instead.
- The garden seed and incomplete butterfly placeholder were replaced in place.
- Protected, family-specific, and child-toy character work remains deliberately
  outside automatic generation.

## Complete disposition of prior 3/5 families

| Previous family | Runtime finding | New live score | Disposition |
|---|---|---:|---|
| Roshan V2/V3 | Fallback only; source-associated character history | 3, dormant | Preserve. V4 remains the preferred route; no automatic redesign. |
| Lamb and rigged Chuck | Family/story subjects, not generic world props | 3, protected exception | Preserve pending explicitly approved source-faithful character work. |
| Craft kitty and birdie | Child-toy/source-derived customization subjects | 3, protected exception | Hard no for automatic generation. Existing models remain temporary fallbacks. |
| GEN2 dolphin, whale, penguin | Active anatomy and animation are sound; surfaces were washed out | 4 candidate | Stronger local-color contrast, dolphin/whale body-fin separation, existing navy outline, and retained penguin beak/rig. |
| Dirt, grass, sand, snow | Active surfaces contained baked props or read repetitively | 4 candidate | Replaced with blank low-frequency painted canvases; normals and gameplay geometry retained. |
| Soft snow | Active but under-described | 4 candidate | Uses the new powder-snow canvas while retaining the separate snow role and normal map. |
| Rainbow road | Old audit referred to a missing file | 4, already live | Stale finding. The painted road tile was promoted in the earlier pass. |
| `polyp.png`, `star_detail.png` | Polyp is fallback detail only; star detail has no runtime consumer | 3, dormant/functional | Do not turn functional masks into focal art. No active 3/5 presentation remains. |
| Castle kit | Active shapes are readable but used one material everywhere | 4 candidate | Role-specific painted masonry, roof, and flag/fabric wraps. Raw kit files remain 3/5 source inventory. |
| Furniture kit | Active, generic surfaces | 4 candidate | Painted wood for table/bookcase and illustrated fabric for chairs. |
| Park kit | Active, separate pack look | 4 candidate | Painted wood, marble, and blank-grass wraps by role. |
| Raw GEN2-routed trees | Old audit mixed raw source and live path | 4 live / 3 raw | Existing tree redirects retained; pine now also redirects to the painted GEN2 pine. |
| Bushes and large leaves | Active models wore lawn textures | 4 candidate | Replaced in live calls by broad-leaf, spear-leaf, fern, and palm-fan crossed cards. |
| Flowers and mushrooms | Active raw pack colors and forms | 4 candidate | Replaced by complete illustrated cards with independent flower and mushroom roles. |
| Nature rocks | No direct current `_nature()` consumer | 3, dormant | Retained as licensed source inventory; active rock roles already use GEN2. |
| Ship, barrel, chest | Active silhouettes work, surfaces were generic | 4 candidate | Shared coral/peach/lavender painted plank overlay with aqua trim; horror cues remain excluded. |
| Galaxy crystals and castle | Active silhouettes work, glass tint was generic | 4 candidate | New matte amethyst/aqua painted-facet triplanar wrap. |
| Galaxy fruit | Active tray props used raw pack skins | 4 candidate | Four complete painted fruit cards, with internal colors preserved during alpha extraction. |
| Galaxy beetle and ladybug | Active glossy miniatures lacked source linework | 4 candidate | Complete top-view cards with six legs, two antennae, and role-correct body structure. |
| Galaxy tropical plants | Active pack geometry reused lawn/wood sheets | 4 candidate | Low-overdraw story cards and simple painted palm trunks; raw GLBs are no longer referenced by gameplay scripts. |
| Motorcycle and go-kart | Active handling and proportions work; stock material did not | 4 candidate | All vehicle routes now pass through matte pastel toon treatment; stock paint no longer restores glossy originals. |
| Garden seed | Active icon looked like a ring/prop | 4 candidate | Replaced by one readable bean seed with a clear hilum and no character face. |
| Garden butterfly | Active image contained only disconnected wing blobs | 4 | Replaced by the approved complete butterfly family; no half-drawn animation component remains in this minigame. |
| Box/cylinder arena architecture | Active masses were flat and generic | 4 candidate | Course pieces use painted fabric; Level 2 masses use painted castle surfaces while collision stays unchanged. |
| HUD, touch, panels, sticker cells | Active but inconsistent ink and panel radii | 4 candidate | Shared navy/plum outline language, reduced heavy black outlines, bordered focal panels, and 8px card/panel radii. Circular touch and icon controls remain circular. |

## Generated-art second-pass gate

| New family | Anatomy or role gate | Repetition and mobile gate | Result |
|---|---|---|---:|
| Terrain canvases | No baked props; snow reads as powder, not water | 1024 square, broad low-frequency shapes | 4/5 |
| Tropical leaves | Complete silhouettes; distinct broad/spear/fern/fan roles | 130-569px source crops; two crossed cards per clump | 4/5 |
| Mushrooms | One red single and one tan cluster; no faces | Separate transparent cards; no mixed biome sheet at runtime | 4/5 |
| Fruit | Apple, banana, orange, and melon remain independently identifiable | Border-connected key removal preserves the melon's internal green | 4/5 |
| Beetles | Six legs, two antennae, head/thorax/wing cases, and a coherent ladybug spot pattern | 1024px maximum; one horizontal card per crawler | 4/5 |
| Crystal and ship surfaces | Material texture, not a standalone object impostor | 1024 square; broad forms and restrained seams | 4/5 |
| Seed | Reads as seed at 72px, not donut/stone/character | 512px alpha card | 4/5 |

The original flowing snow candidate was rejected because it read as water. Raw
chroma sheets remain in `assets_src/style_review_score3/` for provenance and are
not loaded by the game.

## Rollback and QA

Run `backups/art_pre_score3_2026-07-15/restore.ps1` to restore every raster
overwritten in place. New story cards and code routes are ordinary Git changes,
so any family can be reverted independently. Promotion is provisional until the
Mobile renderer screenshots and full probe suite pass; a generated image by
itself is never treated as a finished 3D replacement.
