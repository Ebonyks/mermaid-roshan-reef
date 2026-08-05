# Pearl Castle native interactions V4 audit — 2026-08-04

Finalized 2026-08-05 after native-alpha, duplicate-ownership, runtime-route,
forced-fallback, and exact Godot 4.7.1 Forward Mobile visual validation.

## Outcome

V4 keeps the approved room compositions intact and makes **13 objects that were
already painted into the rooms** interactive. Eight are newly isolated ownership
cards and five reuse previously source-owned cards: four Pool fixtures plus the
Kitchen refrigerator. Every accepted object
has eight authored states (within the required 4–12 frame range), and state 0
uses the exact source-owned resting pixels. No newly invented freestanding
fixture is placed into a room.

The pass deliberately does not force an equal quota into every room. A
four-year-old benefits more from a few large, obvious, cause-and-effect actions
than from small overlapping hit targets or objects that do not belong. Existing
V2 interactions remain available; V4 adds only candidates that pass placement,
ownership, and normalized-use review.

Separately, the already-isolated Dream House role-play cards were audited for
the same question: “How can this room become more interesting for a four-year-
old without adding another object?” Their rejected generic whole-card bounce is
removed and replaced with the item-specific responses documented below. These
existing role-play cards are not counted among the 13 V4 authored atlases.

The same pass also corrected the older static depth cards that could hide
Roshan behind opaque floor- or wall-shaped alpha. Sixteen retained foreground
cards now keep only reviewed physical subjects, and the Pool's full water-oval
mid card is retired because water belongs in the room background rather than in
front of the character.

Delivery methods:

- Eight ImageGen sources initially passed source-level style/cutout review. The
  tent source then failed final ownership scope because it retained outer-canopy
  and knob pixels, the Kitchen lid failed because every source mask retained a
  pot-body band and right handle, and the generated seahorse failed the final
  in-room frame review because its body color and silhouette drifted from the
  approved fixture. Five final atlases therefore use fixed-pivot normalized
  generated states: the Kitchen refrigerator, Playroom sailboat, Craft Room
  cupboard, and Pool flower and star floats.
  The refrigerator source's baked pale checker field is removed by a fully
  recorded deterministic segmentation rather than being misreported as alpha.
- Seven fixtures use deterministic local state derivation from exact source-owned
  rest cards: both Opera sconces, both Library light fixtures, the Playroom tent
  flaps, the Pool seahorse fountain, and the Bath mirror. These are derived
  assets, not generations. The seahorse keeps the exact approved body in all
  states and varies only its already-present nozzle stream.
- The Pool waterfall uses deterministic exact-source states with a bounded
  low-alpha fixture-water shader handoff. Its drifting generated attempt is
  rejected. Exact-engine capture verifies that flow begins at the existing shell
  lip, reaches its painted splash, and introduces no rectangular overlay.

The authoritative per-file paths, hashes, frame counts, ownership evidence, and
method labels are in
`assets/flats/castle/interactions_v4/castle_interactions_v4.json`. Built-in
generation attempts, including rejected attempts, are in
`assets_src/imagegen/castle_object_animations_v4/PROVENANCE.json`.

## Acceptance rules

An item passes only when all of the following are true:

1. It is visibly pre-existing in the approved room and belongs in that room.
2. Its movable ownership unit can be isolated without wall, shelf, counter,
   holder, neighboring-object, or architectural pixels.
3. Owned rest pixels are removed from the background exactly once, leaving no
   painted duplicate under the interactive card.
4. The action is specific to normal or imaginative use of that item; a generic
   bounce, whole-card spin, or detached overlay is not accepted as the action.
5. The action has a large, readable cause-and-effect payoff for a non-reader
   using one finger.
6. The sequence contains 4–12 authored states, begins from an exact resting
   state, keeps a stable pivot, and returns coherently.

## Rooms receiving no new V4 ownership extraction

These rooms were audited rather than skipped. They either already provide a
coherent normalized-use response/navigation role or reuse a previously owned
card, so another extraction would add visual clutter or create two owners for
the same pixels.

| Room | Existing child-readable interest | V4 verdict |
|---|---|---|
| Main Hall | Room navigation, the retained throne interaction, and dust-bunny play already provide large one-finger targets and immediate responses. | Add no new card. Retire the obsolete overlay sconces/tapestry instead of preserving decorative sticker motion. |
| Dining Room | Serving and eating visibly change the six actual plates already set in the room. | Keep the coherent meal sequence; do not layer novelty food or furniture cutouts over the table. |
| Kitchen | The actual refrigerator, oven, and sink/faucet already provide familiar cooking and water cause-and-effect. | Reuse and clean the already source-owned teal refrigerator card, override its poor beige V2 animation with the accepted V4 door/interior states, and add no second ownership extraction. Reject the lid and teapot candidates rather than duplicating the pot or cup. |
| Royal Bedroom | Sleeping changes the room from day to night and changes Roshan's pose; wardrobe/light state also responds as part of the room. | Keep the whole-room bedtime cause and effect. Extra bedside stickers would compete with the sleep interaction. |
| Sleepover Bedroom | Each of the three beds runs the existing day/night sleep-and-wake sequence. | Keep the normalized bedtime use; leave the decorative chandelier static instead of inventing unrelated motion. |
| Movie Lounge | The actual screen image cycles and the seating is used as seating, so the room already behaves like a movie room. | Keep screen/seating state changes; do not paste additional movie props over the composition. |
| Family Gallery | The physical doors provide the room's clear navigation action. | Keep the doors as the meaningful targets; decorative portrait or frame motion would be an overlay rather than useful object interaction. |

## Dream House normalized-use behavior audit

The Dream House furniture was already delivered as transparent, independently
cropped cards from the accepted furnishing-family sheet, while its 2K room
shells were built separately. The existing
`audit/castle_dream_house/dream_house_room_art_manifest.json` remains the source,
crop, alpha, placement, and hash authority. This pass changes behavior only:
no new furniture art is generated, no room placement moves, and no painted copy
is introduced beneath a card.

| Room / existing item | Normalized four-year-old response | Placement and animation verdict |
|---|---|---|
| Dining Room — Royal buffet and family table | Serving reveals the six real plate cards one at a time in a six-step cadence. Eating fades only the consumed plate through four steps and removes it. Tapping an empty table delegates serving to the real buffet instead of pretending the table makes food. | Buffet and table transforms remain exact and fixed. The visible result objects—the plates—change; neither furniture card bounces, rotates, or scales. |
| Royal Bedroom — shell wardrobe | The existing wardrobe card gives a four-state pearl glint, then opens the project's real visual wardrobe picker. Choosing a look immediately rebuilds the separate in-room Roshan standee/animation loop and the existing picker saves that choice. | The wardrobe remains in its approved position and never deforms. This does not falsely claim drawn door/interior frames: the honest payoff is the existing dress-up interface and Roshan's changed appearance. |
| Royal Bedroom — bedside pearl light | The actual combined bedside card changes brightness through four on/off transition states with the existing switch sound. | The same card remains fixed; there is no separate glow sticker, alpha aura, new light node, or furniture bounce. |
| Royal Bedroom — reading cushion | Roshan walks to the cushion's authored foot position and receives story-cushion-specific feedback. | The cushion correctly stays still under a seated child; no fake four-frame count or whole-card deformation is claimed. |
| Royal and Sleepover bedrooms — existing beds | The retained sleep interaction moves Roshan to the chosen bed, changes the room between day and night, and wakes safely with no fail state. | These already-coherent bedtime interactions remain at their authored placements; no decorative prop is layered over them. |
| Movie Lounge — screen and family picture | Tapping the real screen runs a four-state fade/swap on the actual picture card, directly cycling the five protected family images. | The screen frame stays fixed. Protected book images are displayed directly and unchanged; the picture, not a detached overlay or bouncing frame, carries the response. |
| Movie Lounge — left/right cloud settees and center pouf | Tapping a seat moves Roshan to that seat's authored foot position; couch and pouf messages match the chosen item. | Furniture transforms remain fixed. Normal use is the child settling onto the seat, so no false furniture animation/state count is added. |

### Intentionally indirect or noninteractive Dream House art

| Item | Audit decision |
|---|---|
| Six meal plates | No individual hotspots. They are subordinate visual states owned by serving/eating, preventing six tiny competing touch targets. |
| Dining seats and dining chandelier | Keep as composition/supporting furniture. Adding bounce or arbitrary light motion would not improve the already-clear table action. |
| Sleepover chandelier | Keep static; the room's three large bed targets already provide the coherent bedtime response. |
| Movie picture | No direct hotspot. It is the actual four-state visual target controlled by the surrounding screen. |
| Movie-night popcorn bowl | Intentionally `proximity_only`, with no hotspot and no role-play action. The approved art has no honest empty-bowl state, so it remains set dressing instead of inexplicably changing the movie or pretending to be eaten through an overlay. |
| Family Gallery decoration | Keep portraits and frames static. The four physical room doors remain navigation targets rather than receiving unrelated novelty motion. |

The generic `_roleplay_prop_bounce` helper is removed entirely. The trusted
interaction probe asserts its absence, each fixed furniture transform, the
plate cadences, movie-picture target, popcorn's missing hotspot/action, seat
destination, wardrobe picker and in-room skin refresh, and bedside-light state.
The three temporary role-play values—plate count, movie index, and bedside-light
state—remain session-only and are cleared when the castle closes; the wardrobe
choice continues through the existing save path.

## Accepted objects

| Room / accepted item | Placement and environmental blend | Eight-state action and four-year-old interest | Ownership and duplication verdict |
|---|---|---|---|
| Opera Hall — left pearl sconce | Existing symmetrical wall light; its scale, lavender wall recess, and stage-side location are unchanged. | The real pearl brightens through a color chase, giving a simple “I turned on the theater light” response. | Clean lamp-only card; wall remains background; healed once; no overlap. |
| Opera Hall — right pearl sconce | Existing matching wall light on the opposite side of the stage; no new fixture or visual weight is added. | The real pearl answers the left light in a readable theater-light chase. | Clean lamp-only card; wall remains background; healed once; no overlap. |
| Kitchen — teal refrigerator | Existing refrigerator remains in the approved Kitchen crop at `[636,86,133,256]`; mint/teal body, peach shell badge, gold hardware, scale, and cabinet base are preserved. | The latch releases, the attached real door opens to a coherent food interior, and it closes again. Eight fixed-base states replace the unrelated beige V2 design. | Reuses the prior source-owned card rather than adding another appliance. Alpha cleanup removes 240 visible wall/neighbor fragments without repainting refrigerator RGB; frame 0 is the cleaned exact rest card; one V4 heal removes the painted duplicate only under the live frame union. |
| Library — right pearl lamp | Existing large pearl lamp at the right edge; its architectural base and room silhouette remain unchanged. | The real lamp wakes from dim to warm glow, an immediate touch-to-light payoff. | Clean fixture-only card; adjacent wall and trim excluded; healed once; no overlap. |
| Library — ceiling chandelier | Existing chandelier centered over the room, already aligned to the ceiling. | Its attached pearls illuminate in sequence like a tiny library celebration. | Chandelier silhouette isolated without ceiling; healed once; no overlap. |
| Playroom — right tent flaps | Existing cloth inside the right play-tent opening; the shell arch remains exactly where the background artist placed it. | Exact-source deterministic fold states open and close the actual fabric for peekaboo, one of the clearest anticipation/reveal actions for this age. | Flaps only; the generated retry still carried outer-canopy/knob pixels and was superseded, avoiding an arch pasted over itself. |
| Playroom — shelf sailboat | Existing toy boat on the right cubby shelf; shelf position and supporting edge remain untouched. | The real sail unfurls and the hull rocks gently, turning a static toy into a miniature voyage. | Boat-only cutout; shelf and neighboring toys excluded; healed once; no overlap. |
| Craft Room — left supply cupboard | Existing built-in cupboard at child-eye level on the left; it remains part of the room cabinetry. | Its real bins/drawers slide out to reveal art supplies and reseat, creating a readable surprise-and-discovery loop. | Cupboard carcass and moving bins/drawers only; jars and surrounding cabinetry remain background; healed once; no overlap. |
| Mermaid Pool — waterfall | Existing source-owned waterfall in its original rock opening; no second water feature is added. | The real painted rainbow stream pulses while the bounded fixture-water shader supplies moving flow from the existing lip into the pool. | Reuses the approved card; every state keeps the complete painted-stream alpha, so no dry frame can expose the rejected rectangular heal; no generated gate or overlap. |
| Mermaid Pool — flower float | Existing source-owned flower float already resting naturally on the water. | Its actual petals open into a bloom and close again, with a small contact-local ripple, turning the familiar float into a large, readable surprise. | Reuses the approved card; no new flower or platform; no overlap. |
| Mermaid Pool — seahorse fountain | Existing source-owned fountain in its architectural niche, with its nozzle already aimed into the pool. | The exact real fixture remains stable while its already-painted nozzle stream shimmers through eight restrained states, so the response reads as water flow rather than a replacement seahorse. | Reuses the approved card; the generated moving-body attempt is rejected for color/silhouette drift, and the accepted flow remains nozzle-local rather than a detached screen overlay; no duplicate fixture. |
| Mermaid Pool — star float | Existing source-owned star float already placed on the pool surface. | One real point flexes in a friendly wave and makes a small contact-local ripple; extreme generated poses are culled so the star remains recognizable. | Reuses the approved card; prior heal was corrected in V4; no overlap remains. |
| Bubble Bath — vanity mirror | Existing mirror centered over the vanity and sink; no new bathroom furnishing is introduced. | The real mirror surface fogs, then a wipe clears it, inviting a familiar reveal game. | Mirror-only card; wall and vanity stay background; healed once; no overlap. |

## Retained and rejected candidates

| Room / candidate or attempt | Verdict | Placement, blending, or animation flaw |
|---|---|---|
| Main Hall — Huluu throne | Retain the already approved existing interaction; do not create a V4 duplicate. | It was previously extracted from its approved high-resolution source with separate ownership provenance. Re-extraction would establish two owners for one throne. |
| Opera Hall — side portals | Reject. | These are architectural recesses partly occluded by auditorium rails, not movable doors. Any card would carry rail or wall fragments and sit visibly over the architecture. |
| Kitchen — full stove-pot generation | Reject. | The generation animates the entire pot. Shipping it would put a second pot body over the painted one. |
| Kitchen — lid-only generation and extraction | Reject at final delivery. | The generated states passed source-level alpha/style review, but repeated rest-card masks visibly retained a pot-body strip and right handle. The candidate is removed rather than shipping a dirty partial cutout. |
| Kitchen — teapot / tea-service attempt 1 | Reject. | The spout moves away from the cup, so the pouring action no longer represents normal teapot use. |
| Kitchen — teapot / tea-service attempt 2 | Reject. | The generated sheet bakes in another cup, which would duplicate the room's cup and disrupt the counter composition. |
| Kitchen — teapot attempt 3 | Reject despite cleaner animation art. | The source teapot still touches the cup, coral, and counter shadow. A clean generated sequence cannot repair an unownable source object. |
| Playroom — tent generations | Reject the full-arch attempt; supersede the cleaner flap retry at final delivery; exact-source flap states accepted. | The first attempt owns obvious architecture. The retry passed alpha/style review but still carries outer-canopy and knob pixels. Runtime derives folds from the exact owned flap card so neither generation can cover the original tent. |
| Craft Room — right ribbon rack | Reject. | Lowest ribbons cross the wall shelf and cup. Extraction leaves shelf/cup fragments, so the card fails blend and ownership review. |
| Mermaid Pool — giant clam | Reject. | It is integrated into the stairs and overlaps the foreground bubble-fountain composition. Separation would split or duplicate shared pixels. |
| Mermaid Pool — bubble fountain generation | Reject. | The generated fixture drifts into a new jar-like object and does not blend with the approved shell-and-stair composition. |
| Bubble Bath — toilet roll | Reject. | The paper is painted through its gold holder and overlaps the purple plant/wall shadow. Either the roll has a hole or the card carries non-owned pixels. |
| Mermaid Pool — flower-float attempt 1 | Reject attempt; accepted replacement retained. | The first chroma-to-alpha result failed edge/matte quality. It remains only as rejected provenance evidence. |
| Craft Room — cupboard attempt 1 | Reject attempt; accepted replacement retained. | The generated composition merged the frame layout, so eight independent, fixed-pivot states could not be packed reliably. |
| Mermaid Pool — generated waterfall attempt | Reject; exact-source deterministic replacement accepted. | It invents a clam-door/gate that is absent from the approved room. This is precisely the “new asset over old art” failure V4 is meant to remove. |

Rejected PNG evidence lives only under
`assets_src/imagegen/castle_object_animations_v4/**/rejected/`; no rejected
attempt is referenced by the runtime manifest or room registry. The prior V3
novel-object expansion and its V3-only source/license entries are removed rather
than left as dormant alternate room furnishings.

## Cutout, healing, and animation QA

- All eight new ownership cards were reviewed against white as well as against
  their healed room plates. The accepted silhouettes contain the intended
  object only; no rectangular room-color fringe or neighboring fixture is
  accepted.
- Five items reuse established source-owned cards. V4 re-audits the four Pool
  masks, corrects the star float's old heal, and tightens the refrigerator's
  legacy alpha to remove purple wall and neighboring-cabinet fragments without
  repainting its retained RGB.
- Seven V4 runtime rooms receive one non-destructive derived heal. The native
  baseline for all seven tiled rooms is also rebuilt from approved whole-room
  pixels outside the exact union of active V2/V4 frame alpha and static depth
  cards at alpha 128, retaining prior hidden fill only underneath that union.
  Approved parent room art is unchanged. Both the baseline and final V4 routes
  report zero changed native pixels outside their live unions and zero
  rest-state duplicate ownership.
- The static-depth repair removes 70,013 alpha-scissor pixels that belonged to
  empty floor/wall spill while preserving visible source RGB byte-for-byte,
  clears 563,980 latent RGB pixels beneath alpha zero, and removes the Pool
  water oval's 214,981 opaque pixels from runtime. Main Hall and Opera keep their
  already-clean physical silhouettes; their hidden RGB is cleared only.
- Retiring the Pool water-oval card exposed a pre-existing scanline-fill defect
  in the legacy logical clean plate. The native repair now excludes that retired
  card from its protected union and restores the approved crisp Pool water before
  applying the four localized V4 ownership masks. The broad horizontal blur is
  absent in exact-engine full-room capture.
- The six non-Kitchen healed backgrounds use 3640 × 2048 native masters split
  into four-by-two grids of 910 × 1024 lossless tiles. Kitchen retains its
  4096 × 2304 four-by-three grid of 1024 × 768 tiles. Every playable screen now
  has at least 2048 native background pixels on each axis before runtime slicing.
- Every runtime atlas is RGBA with eight authored states and a stable pivot.
  Twelve are 1024 × 512 in a 4 × 2 grid; the refrigerator is 960 × 816 in a
  3 × 3 grid with one unused cell. State 0 is the exact approved/cleaned rest
  card; no generic transform fallback is allowed.
- The refrigerator's 1536 × 1024 RGB source is segmented by edge-connected
  neutral-matte components, one-pixel core erosion, 0.8-pixel feathering, fixed
  base registration, and nearest-solid-core RGB decontamination. Each runtime
  frame has one connected visible alpha component, and the pale/cyan/green
  matte-leak audit reports zero retained leakage.
- Generated state sources are accepted only when the generated object's identity
  and action remain coherent with its approved room object. Deterministic light,
  mirror, and waterfall states are explicitly labeled as derived, with no false
  ImageGen attribution.
- Pool streams and ripples use the established fixture-water shader inside
  source-rect-normalized outlet/contact masks. The manifest explicitly records
  `uses_jolt_for_fluid: false`; Jolt is limited to bounded secondary solid-body
  settling where allowed and is not misrepresented as the fluid renderer. The
  waterfall layer uses restrained alpha and a tapered outlet-to-splash polygon;
  exact Forward Mobile capture shows no hard rectangle or detached flow.
- The repository frame-review gate reconstructs the exact runtime tile underlay,
  applies the runtime alpha-128 scissor and active static-card z ordering, and
  emits both untinted composites and diagnostic sheets. All 104 authored states
  were visually inspected. Their exact hashes and the six intentional tent/front-
  card occlusion relations are locked in
  `assets_src/castle/interactions_v4/castle_interaction_frame_approval_ledger.json`;
  the gate reports zero blocking duplicates, ownership leaks, or coplanar cards.
- The source/hash/provenance validators are blocking for missing files, stale
  hashes, ownership overlap, rejected runtime references, and out-of-range frame
  counts. Exact Codex frame-by-frame visual review is recorded; this document
  does not claim separate owner review.
- The delivery gate binds the ownership extractor, V4 specification, and Fable
  layer manifest by path and SHA-256 instead of trusting metadata copied from a
  prior delivery run. Audit contact labels use Pillow's pinned bundled font so
  Windows and Ubuntu reconstruct identical evidence pixels.
- Every native-room rejection path is also forced in the interaction probe. A
  failed decode now shows the intact fallback room tiles while suppressing all
  13 source-owned replacement cards, so the refrigerator and four Pool fixtures
  cannot be pasted over their still-painted originals. Dream House retains its
  independent legacy 2-by-2 grid.

## Full change ledger

- Added eight clean ownership cards from approved Opera, Library, Playroom,
  Craft Room, and Bubble Bath art.
- Reused and re-audited five approved ownership cards: four Pool fixtures plus
  the Kitchen refrigerator; repaired the star-float heal and cleaned the
  refrigerator's contaminated legacy alpha without repainting retained RGB.
- Added one healed V4 background route for each of seven runtime rooms, and
  repaired all seven native background baselines so approved pixels are restored
  outside the exact live Sprite3D alpha union. Approved parent room images remain
  untouched.
- Rebuilt the Pool native baseline from approved crisp water after proving the
  retired broad mid-water card had caused the old logical plate's scanline blur;
  verified the repaired full room and waterfall maximum-flow state in Godot
  4.7.1 Forward Mobile runtime captures.
- Tightened sixteen existing foreground-card alpha masks to the physical
  furniture/coral/architectural subjects, cleared all fully transparent RGB,
  and retired the Pool's broad mid-water card. Together this removes 284,994
  opaque runtime depth pixels that could cover Roshan without a physical object.
- Added thirteen eight-state runtime atlases: five from accepted generated state
  sources and eight deterministic exact-source derivatives, including the
  source-faithful replacement for the rejected generated seahorse body.
- Rejected the waterfall's intermediate dry/blurred handoff during untinted
  frame review; rebuilt it so the original painted fall remains complete in all
  eight states beneath the bounded animated-water shader.
- Limited animation to actual object behavior: lamp/chandelier illumination,
  tent-flap peekaboo, sail unfurl/rock, supply-bin/drawer pullout/reveal,
  mirror fog/wipe, refrigerator latch/door/interior use, flower-petal bloom,
  star-point wave, and nozzle-local Pool fixture actions.
- Removed the Dream House generic whole-card bounce route. Serving now reveals
  six real plates in sequence; eating consumes one real plate through four
  states; an empty table delegates back to the buffet.
- Changed the Movie Lounge so the actual protected picture performs the
  four-state fade/swap while the screen frame stays fixed, and made the popcorn
  bowl intentionally proximity-only because no honest empty-bowl art exists.
- Changed seating to move Roshan to each existing cushion/settee/pouf while the
  furniture stays fixed; corrected item-specific cushion/pouf feedback without
  inventing animation-frame claims.
- Changed the Royal Bedroom wardrobe to give four states of card feedback then
  open the existing wardrobe picker, and refresh the in-room Roshan standee when
  a saved look is selected. Changed the bedside card to a four-state brightness
  transition with no detached glow layer or new light node.
- Kept alpha-scissor depth protection on solid room cutouts while routing only
  intentional soft visuals (Roshan's contact shadow, meal-plate consumption,
  the real movie picture crossfade, sparkles, and tutorial pointer) through
  alpha blending without the opaque depth pass. Their soft states no longer
  collapse into hard pops and transparent texels do not hide Roshan.
- Kept Dream House plates/pictures indirectly controlled and left the dining
  seats/chandelier, Sleepover chandelier, popcorn, and gallery decoration
  intentionally without hotspots or novelty motion where a truthful state was
  unavailable.
- Rejected every candidate that was architectural, overlapped another painted
  object, required non-owned pixels, duplicated a room fixture, used a broken
  frame layout, or drifted into a new design.
- Quarantined twelve rejected built-in generation attempts as non-runtime
  provenance evidence; retained two source-review passes that were superseded
  by the stricter delivery ownership gate; and recorded all nineteen built-in
  attempts with native paths/IDs and verified hashes.
- Removed the rejected V3 novel-object expansion and its obsolete V3-only
  license/provenance references.
- Added a blocking 104-frame approval gate with exact decoded-pixel duplicate
  detection, non-blocking tolerance diagnostics, untinted visual composites,
  and explicit static-depth occlusion evidence.
- Added cross-platform upstream-provenance and contact-render self-tests so a
  stale source-layer hash or OS-specific audit font cannot pass locally and fail
  silently on the Ubuntu release runner.
- Extended the trusted Godot 4.7.1 interaction probe to reject the removed
  bounce helper and verify the Dream House target nodes, fixed transforms,
  state cadences, indirect controls, wardrobe avatar refresh, and intentional
  noninteraction; `INTERACTION|ALL OK`, bathroom integration, and castle-art
  noninteraction, all seven forced native-route failures, suppression of all 13
  overlapping fallback cards, and the untouched Dream House legacy grid;
  `INTERACTION|ALL OK`, bathroom integration, and castle-art mobile-render probes
  are green.
