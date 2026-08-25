# Day One swimming dust bunny — prompt and provenance

Date: 2026-08-24

Method: OpenAI built-in `image_gen` tool, identity-preserving generation with
two approved project-original reference cutouts, followed by one targeted
built-in background-extraction edit. No protected original was modified.

## Approved references

- `assets/castle/dirty_cleanup_2d/critters/dust_bunnies/dust_bunny_curl_ears.png`
  - role: authoritative neutral identity and rendering reference
  - SHA-256: `D88F667724D2C06FC591B00EA91B018430BAD1A359E7527124A6E25B0CC6DA0F`
- `assets/castle/dirty_cleanup_2d/critters/dust_bunnies/dust_bunny_hop.png`
  - role: authoritative dynamic motion and side-curl reference
  - SHA-256: `677CDA8C5DE1D3AAF1D8960B089D48FAB27106429BC221B4C26C14775B382752`

## Accepted generation prompt

```text
Use case: identity-preserve
Asset type: production true-2D transparent swimming character cutout for Godot, reused in a mermaid pool and a filled bathtub
Input images: Image 1 is the authoritative approved dust-bunny identity and neutral front pose; Image 2 is the authoritative approved dynamic motion pose, side curls, and rendering-style reference.
Primary request: create exactly one new swimming pose of this same lavender dust bunny. The entire cloud body is clearly tilted into a buoyant diagonal swimming posture moving toward screen right, about 25 degrees above horizontal rather than sitting upright. The two pearl forepaws reach and paddle forward toward screen right; the rear cloud curls taper and trail toward screen left like a soft kick; both spiral ears stream slightly backward with motion while remaining recognizable. Keep the friendly face visible in a three-quarter view and looking toward the direction of travel.
Subject: exact same species identity—two lavender spiral ears with pearl beads, central forehead curl, rounded lavender cloud curls, exactly two visible pearl forepaws, warm brown-purple glossy eyes, coral blush, tiny cheerful mouth, fine navy-purple outline.
Style/medium: match the supplied polished pastel cel-painted children's storybook sprite style exactly; crisp phone-readable silhouette; soft lavender-to-lilac value bands and glossy highlights.
Composition/framing: exactly one complete diagonal swimmer centered on a square canvas with generous genuine transparent padding; full ears and trailing body visible; clear left-to-right motion silhouette.
Lighting/mood: cheerful, gentle, playful, safe for a four-year-old.
Constraints: preserve identity, palette, face language, spiral motifs, pearl-paw material, outline weight, lighting, and rendering from the references; exactly one bunny, exactly two ears, exactly two visible paws; genuinely transparent RGBA background with clean alpha; NO water ring, NO puddle, NO pool, NO bathtub, NO splash, NO bubbles, NO glow, NO floor, NO horizon, NO shadow, NO scenery, NO extra props, NO text, NO logo, NO watermark.
Avoid: upright seated pose, front-facing seated pose, standing, redesign, realistic fur, extra limbs, extra paws, cropped ears, separate motion tail, duplicate bunny, muddy colors, neon saturation, 3D rendering.
```

The generator returned a visually correct swimming pose with a baked preview
checkerboard. It was not used as delivery pixels. A targeted built-in edit made
only the background transparent.

## Accepted background-extraction prompt

```text
Use case: background-extraction
Asset type: corrected production true-2D transparent swimming character cutout for Godot
Input image: Image 1 is the exact diagonal swimming dust-bunny candidate and edit target.
Primary request: remove only the visible gray-and-white checkerboard background and replace it with genuine transparent alpha.
Invariants: preserve every subject pixel and detail in design and appearance—the exact diagonal swimming silhouette, two spiral ears and pearl beads, forehead curl, three-quarter face, eyes, blush, mouth, elongated trailing lavender cloud curls, exactly two pearl forepaws, outlines, colors, highlights, proportions, pose, composition, and scale.
Constraints: output genuinely transparent RGBA with clean alpha edges and generous transparent padding; no checkerboard, no white matte, no colored backdrop, no halo, no glow, no water, no bubbles, no floor, no shadow, no crop, no added or removed subject detail, no text, no watermark. Change only the background transparency.
```

## Accepted native and runtime derivative

- Built-in native output:
  - path at generation time: `C:/Users/Peter/.codex/generated_images/01a0373f-185f-7853-867e-4c911c2bfc21/exec-23af3d24-3e76-422c-8c50-a5a860218d5e.png`
  - dimensions/format: 1536×1024 RGBA
  - SHA-256: `8ABC138A24DBD2C10EFC6AAC04CBE67AE42F2A6EAB5DD1510EE893FC527206D8`
- Runtime derivative:
  - `assets/castle/dirty_cleanup_2d/critters/dust_bunnies/dust_bunny_swimming.png`
  - dimensions/format: 1024×683 RGBA
  - SHA-256: `D788366485DA7A19958C34278BD05A4A4977BE39582A9134D3E63A394D601143`
  - whole-canvas transform only: alpha-premultiply, Lanczos resize to
    1024×683, alpha-unpremultiply; no crop, mask, subject move, compositing, or
    isolated repair

## Review outcome

The first seated-in-ripple concept was rejected and is not a project asset.
The accepted candidate passed independent Luna review for curl-ear identity,
two-paw/two-ear anatomy, diagonal paddle/kick readability, transparent alpha,
and reuse in both the Mermaid Pool and filled bathtub. Runtime owns the small
ripple, tint, scale, depth, and bounded animation so the generated cutout stays
scene-neutral.
