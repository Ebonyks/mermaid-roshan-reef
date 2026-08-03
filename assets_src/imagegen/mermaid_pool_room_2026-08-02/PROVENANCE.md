# Mermaid Pool full-frame regeneration - 2026-08-02

Status: v3 accepted production source on `codex/mermaid-pool-expanded`.

## Defect and scope

The prior v2 interaction pass explicitly removed the painted rainbow water
from the room's iconic waterfall and replaced the resting visual with a dry
shell gate/control fixture plus procedural flow. The small right-side bubble
fixture also read as unexplained plumbing. The owner requested a complete room
regeneration and corrected touch interactions.

This regeneration preserves the approved room architecture, centered pool,
ocean window, left steps, open foreground walkway, palette, camera, flower
float, and star float. It restores a continuously visible rainbow waterfall
as the hero feature and replaces the pipe-like bubble fixture with one
pool-specific seahorse fountain. No protected book, voice, or character asset
was modified.

## Existing-art inventory and references

- Primary composition/style reference: `assets/flats/castle/rooms/room_mermaid_pool.png` as it existed before this regeneration; SHA-256 `4ed0f6ce0fb79c35cb55f9c18c56518252df1a8e478de1ef8c06d3cf4a9e0e0`.
- Supporting room-purpose reference: `assets_src/imagegen/castle_room_buttons_2026-08-01/castle_button_mermaid_pool_master.png`; SHA-256 `0e90d41d68fe208d47567dfa6511afd417b2b803aef09a880c3255a2323fd25f`.
- Reuse decision: the approved architecture, layout, waterfall identity, and two sensible floats were retained. New generation was limited to the complete coherent room frame required to remove the dry shell-gate regression and ambiguous pipe.

## Accepted generation (v2)

- Method: OpenAI built-in Codex ImageGen, reference-guided precise-object edit.
- Attempt: 1.
- Native output copy: `room_mermaid_pool_fullframe_v2_native.png`.
- Native dimensions: 1672x941.
- Native SHA-256: `a9c8ea63173fda88c2b674c9f3fc1ddbe2d85c9031bba778b86ec590b1e7a119`.
- Original tool output: `C:\Users\Peter\.codex\generated_images\019fc4ee-fba3-7dc3-876c-f751c715c915\exec-545ccc9f-f975-4319-b8f7-06e8f240b217.png`.

## Final prompt

> Use case: precise-object-edit
> Asset type: complete flattened production room master for a 16:9 mobile children's storybook game
> Input images: Of the supplied recent images, the complete wide Mermaid Pool room is the authoritative edit target and composition/style reference. The other images are supporting closeups of its separated background and existing interaction art; they must not replace the full-room framing.
> Primary request: Regenerate the complete Mermaid Pool room as one coherent full-frame illustration. Preserve the room architecture, centered oval swimming pool, broad empty peach walkway in the foreground, ocean-view center window, left pool steps, lavender pearl arches, coral framing, symmetrical composition, camera, and established pastel palette. Restore the iconic RAINBOW WATERFALL at the left-rear pool edge as the dominant hero feature: a broad, continuously visible cascade of distinct luminous pastel rainbow bands flowing naturally from the existing coral-and-pearl wall opening into the pool, with visible foam and splash. It must read first as a magical rainbow waterfall, never as a dry shell machine, gate, control panel, or mechanical device.
> Interaction layout: keep the waterfall in the same left-rear zone as the complete room reference; keep one pink flower float near the left-center of the water and one golden star float near the middle of the water; replace every narrow pipe, nozzle, vase-like sprayer, plumbing fixture, or ambiguous bubble device in the right half of the pool with ONE clearly readable friendly pastel seahorse fountain sculpture rooted naturally at the right-rear pool rim, spraying a small playful arc of water and bubbles into the pool. The seahorse fountain must occupy approximately the same combined right-side area as the removed pipe-like fountains, leaving the central swim water open.
> Style/medium: polished 2D children's storybook illustration matching the complete room reference, softly painted cel shading, crisp navy-purple edge accents, pearly lavender shells, aqua water, warm peach floor, bright magical but gentle.
> Composition/framing: exact 16:9 wide room, straight-on slightly elevated view, full room from back arches to foreground coral, no crop; preserve the large open foreground walkway and the current object zones so existing touch interaction positions remain valid.
> Constraints: complete flattened full-frame image; no characters; no text; no labels; no UI; no watermark. Exactly four intended interaction subjects are visible and separated: rainbow waterfall, pink flower float, golden star float, seahorse fountain. Keep these subjects visually distinct, toddler-readable, and not overlapping. The rainbow flow must remain visible in the resting scene.
> Avoid: dry waterfall fixture; retracting shell gate; pearl control; shell device; control panel; exposed outlet mouth; pipe; plumbing; faucet; narrow bottle-shaped fountain; duplicated fountains; extra floats; extra interaction props; technical machinery; empty waterfall opening; scene redesign; changed room camera; foreground clutter.

## Accepted geometry revision (v3)

The owner accepted the v2 interaction repair but found its pool too small and
too kidney-bean-shaped. The requested follow-up was limited to enlarging the
pool beyond half of the visible room floor, rounding its footprint, and
extending it into the foreground. Existing approved art was inventoried before
generation; the accepted v2 full frame remained the authoritative edit target,
and the existing Mermaid Pool room-button master was used only as a supporting
pool-proportion reference.

- Method: OpenAI built-in Codex ImageGen, reference-guided precise-object edit.
- Attempt: 1.
- Native output copy: `room_mermaid_pool_fullframe_v3_native.png`.
- Native dimensions: 1672x941.
- Native SHA-256: `2a4bd923c26d5f7980fc8a723576ecb573097e30bc94090f75437833fc3d55a5`.
- Original tool output: `C:\Users\Peter\.codex\generated_images\019fc4ee-fba3-7dc3-876c-f751c715c915\exec-9694b851-d751-4c35-9e94-0f865351c43a.png`.
- Authoritative edit target: `room_mermaid_pool_fullframe_v2_native.png`;
  SHA-256 `a9c8ea63173fda88c2b674c9f3fc1ddbe2d85c9031bba778b86ec590b1e7a119`.
- Supporting proportion reference:
  `assets_src/imagegen/castle_room_buttons_2026-08-01/castle_button_mermaid_pool_master.png`;
  SHA-256 `0e90d41d68fe208d47567dfa6511afd417b2b803aef09a880c3255a2323fd25f`.
- Exact prompt: `room_mermaid_pool_fullframe_v3_prompt.txt`;
  SHA-256 `d592d192699a36fcf7b90063795042660467c86db7d3d91884cf01bed03e6560`.

Visual review accepted the broad continuous convex front rim, balanced oval
silhouette, foreground expansion, slim remaining promenade, and preservation
of the waterfall, flower float, star float, and seahorse fountain. The routing
polygon for the pool occupies 69.44% of the visible floor plane below its back
edge. No pipe, shell gate, control device, extra float, text, character, or
additional interaction prop is present.

## Production derivatives and review

`tools/build_castle_room_layers.py` performs the only whole-canvas normalization
of the accepted v3 master to 1024x576, records the native source hash, extracts outline-refined depth
cards for the four interaction subjects, and heals the non-overlapping clean
plate. `tools/build_castle_room_2k_tiles.py` creates the 2048x1152 clean
background master and four non-overlapping 1024x576 runtime tiles.

`tools/build_castle_interaction_atlases.py` derives fixed-pivot eight-frame
atlases from the accepted room cards. Mermaid Pool runtime deliberately bypasses
the rejected v2 dry-fixture sheets. Human identity review is not applicable;
visual review accepted the room architecture, waterfall identity, prop logic,
subject separation, absence of pipes/devices, and toddler-readable composition.
