# Pass-35 Generation Provenance

Generated 2026-07-16 for the game-wide 3.5-and-lower art pass. The generation
standard is `ART_STYLE_GUIDE.md` plus the book-motif analysis already recorded
in the repository. Book-source art was reference-only and was never edited.

## Shared 2D Prompt Contract

Each sprite used a separate built-in ChatGPT image-generation call with this
shared production direction:

> Single isolated children's storybook game sprite, complete object, generous
> padding, rounded cel-shaded forms, painted pastel face colors, dark
> navy-purple contour, aqua/lavender shadow accents, no photorealism, no text,
> no watermark, no cast shadow. Perfectly flat solid neon green or magenta
> chroma background, no gradient or texture, and no key color in the subject.

Role-specific additions:

| Runtime asset | Role direction |
|---|---|
| `assets/mg/sun.png` | Warm friendly radial sun; uneven hand-painted rays; no face. |
| `assets/mg/tree.png` | Complete deciduous tree with grouped leaf masses and visible trunk. |
| `assets/mg/coal.png` | One readable charcoal lump with broad graphic facets. |
| `assets/mg/star.png` | Five-point story star with painted inner highlight and thick contour. |
| `assets/mg/butterfly.png` | Complete dorsal anatomy: body, antennae, paired forewings and hindwings; symmetrical and animation-readable. |
| `assets/mg/fish_body.png` | Complete lateral fish body with eye, mouth, caudal peduncle and tail; no detached fins. |
| `assets/mg/fish_fins.png` | Matching transparent fin layer: dorsal, paired pectoral, pelvic and anal fins, spaced for animation. |
| `assets/mg/k_bush2.png` | Low garden bush with several authored leaf masses; no spherical topiary. |
| `assets/mg/xtree.png` | Bare functional Christmas tree with no decorations; ornaments remain separate interaction pieces. |
| `assets/mg/orn1.png` | Round coral-pink glass bulb with simple gold cap. |
| `assets/mg/orn2.png` | Long aqua drop ornament with simple gold cap. |
| `assets/mg/orn3.png` | Scallop-shell ornament with pastel ridges. |
| `assets/mg/orn4.png` | Five-point lavender star ornament. |
| `assets/mg/orn5.png` | Gold-and-aqua spiral ornament. |

Chroma sources are under
`assets_src/imagegen/pass35_2026-07-16/chroma/`. Active files were processed by
`tools/postprocess_pass35_sprites.py`: corner-sampled green/magenta removal,
soft matte/despill, tight alpha bounds, and normalization to at most 1024 px.

## 3D Generation Contract

All 96 Blender outputs are deterministic project-original geometry generated
by `tools/build_art_pass35.py`. Shared constraints:

- Mobile-friendly low-poly topology and embedded matte materials.
- Rounded toy geometry, broad color masses, navy-purple outline shells.
- No external meshes, textures, logos, or protected character/book assets.
- Correct anatomy for fish, octopus, shrimp, jellyfish, beetle, butterfly, and
  other creature roles.
- Complete silhouettes from the actual gameplay approach, not only the QA
  camera.
- Functional separation where play requires it: bare Christmas tree versus
  detachable ornaments, individual music bars, independent star bells, and
  open walk-through gates.

Editable source: `assets_src/blender/art_pass35.blend`.
Isolated QA renders: `assets_src/blender/qa_art_pass35/`.
