# Day One Grok location-geometry authority audit

Date: 2026-09-02  
Scope: D1-C00 through D1-C12 external-animation handoffs  
Review method: Luna repository inventory, followed by Sol topology review  

## Blocking rule

A first frame may show only geometry established by one named approved location
authority. Generated storyboards and environment-perspective sheets are
non-pixel narrative aids. They cannot authorize an unseen wall, reverse view,
door, stair, balcony, fixture position, or merged room. A first-frame candidate
fails immediately when it changes landmark count/order, closes a floor-open
portal, combines two screen masters into a third space, or adds geometry absent
from its named authority.

Every promotable first frame must have a `LOCATION_GEOMETRY_LOCK.json` record,
an exact source hash, ordered landmarks, forbidden additions, a Sol topology
decision, and a separate human decision. `eligible_as_image_1` remains false
until both decisions pass and the immutable GitHub URL resolves.

## Scene findings

| Scene | Available location authority | Geometry state | Blocking gap |
|---|---|---|---|
| D1-C00 | Sky Lagoon 6144×2048 panorama | Partial exterior geography | No cabin interior; no integrated dock-to-castle route; castle absent from panorama plate. |
| D1-C01 | Same panorama plus detached airplane, castle, and door references | Partial exterior geography | No approved landing/dock/approach perspective integrating those detached elements. |
| D1-C02 | Main Hall screen A and B, each 2048×1153 | Two authoritative side elevations | Dirty A/B derivatives are Sol topology-pass candidates, but human approval is pending. Never merge A+B. |
| D1-C03 | Dirty Bubble Bathroom 1024×576 front plate | Front plate only | Entrance/door and reverse/threshold view are unseen; cleanup basket placement is not fixed. |
| D1-C04 | Clean Bubble Bathroom 1024×576 front plate | Front plate only | Entrance/reverse view unseen; generated clean endpoint still needs approval. |
| D1-C05 | Mermaid Pool 1024×576 front plate plus detached fixtures | Layout incomplete | Waterfall and seahorse positions are not established; doorway/cardinal views absent. |
| D1-C06 | Same pool authority family | Layout incomplete | Clean fixture positions and cardinal topology remain unapproved. |
| D1-C07 | Playroom 1024×576 front plate | Layout incomplete | Door, basket zones, dirty geography, and Baby Eagle floor location are absent. |
| D1-C08 | Same playroom authority family | Layout incomplete | Clean endpoint geography and the same missing placements remain unapproved. |
| D1-C09 | Art Room 1024×576 front plate | Front plate only | Door/reverse wall absent; required human-approved clean/dirty six-view packet absent. |
| D1-C10 | Same Art Room authority family | Front plate only | Required human-approved six-view packet and clean endpoint absent. |
| D1-C11 | Main Hall screen B only; no arena plate | Wrong location authority for arena | Approved boss-arena topology card is absent. Main Hall cannot stand in for the arena. |
| D1-C12 | Main Hall A/B only within a six-location montage packet | Packet not self-contained | Bathroom, Pool, Playroom, Art Room, and arena plates/endpoints are absent from this packet. |

## Main Hall lock

Screen A, left to right: partial exterior arch; vertical entrance-carpet
segment; tall aqua window; pearl fountain; large purple-curtained central
portal; book-emblem portal; aqua bubble-emblem portal. All portals open to the
floor. Screen A has no stair, balcony, or throne.

Screen B, left to right: bear, palette/flower, blue shell/drop, and white
pearl/flower route portals; short red stair; right throne alcove. Screen B has
one short stair and no balcony.

The detailed machine record and candidate decisions live in
`assets_src/cinematics/d1_c02_first_dirty_castle_discovery_visual_v1/LOCATION_GEOMETRY_LOCK.json`.

## Consequences for generation

- C02 may continue only in the screen-A or screen-B camera families until new
  human-approved perspectives exist.
- S02 is now a screen-A interior orientation, not an unsupported reverse view
  toward an unseen opposite wall.
- S03 uses the real central-portal → column → book-portal bay; both doorways
  remain open to the floor.
- The other listed scenes stay `GENERATION_READY=false` for any angle that
  depends on missing geometry. Additional views must be generated as complete
  location candidates, audited against observable seams, and human-approved
  before they can become authority.

