# Evie and Lamb-a' animated Seek actors

Generation date: 2026-08-09
Tool: built-in OpenAI image generation
Use: new project-owned 2D animation sources for the true-Canvas Seek activity

The owner rejected the interim vinyl-sticker pair and low-grade generic bush
presentation. Repository and full-history review found no animated Evie or
Lamb-a' atlas. The retired `assets/characters/lamb.glb` is also static: it has
no armature, action, or shape key. These two sheets therefore fill a specific
missing-art gap; they do not replace or modify a protected original.

Identity references, read only:

- `assets/characters/friends/pearl_friend.png` — protected Evie and Lamb-a'
  source identity; unchanged.
- `assets/sprites/stuffie_studio/lamma.png` — current project-owned Lamb-a'
  companion derivative; unchanged.
- Historical project art `assets/minigames/seek/lamb.png` at commit
  `f8e83bcf` — clean-body secondary Lamb-a' identity reference; unchanged and
  not copied into runtime.

## Lamb-a' source atlas

Generated source: `lamma_atlas_chroma.png`
SHA-256: `7f38bb41209073f38aaec2cd4a99ed609154da71b02a383e89bfa58548a051fa`

Initial prompt:

> Use case: stylized-concept. Asset type: polished 2D game character
> animation sprite atlas for a preschool hide-and-seek game. Image 1 is the
> binding Lamma identity reference; Image 2 is a secondary clean-body
> reference with the egg removed. Create exactly eight authored chronological
> full-body animation frames of the same Lamb-a' character, arranged as a
> precise 4-column by 2-row sprite atlas with equal square cells and consistent
> scale, anchor, outline, lighting, anatomy, and identity. Preserve the same
> round fluffy white lamb, very wide ears with pale-blue inner ears, navy oval
> eyes with eyelashes, peach cheek blush, tiny salmon-pink nose, small woolly
> hooves, pale blue-gray storybook contour, and gentle delighted personality.
> Remove the decorative egg and all handheld objects. Top row frames 1-4 form
> a seamless gentle idle-breathe and ear-wiggle loop. Bottom row frames 1-4
> form one clear reveal celebration: crouched/peeking, springing upward, happy
> airborne hop with ears lifted, then a soft cheerful landing that can return
> to idle. Use polished 2D children's storybook cel illustration with genuine
> authored pose changes. Every cell contains one complete uncropped Lamb-a'.
> Use one perfectly flat solid `#ff00ff` chroma background. No labels,
> dividers, text, logos, watermark, contact shadow, cast shadow, ground, glow,
> vinyl border, 3D render, plush fabric, extra limbs, or identity drift.

The first candidate contained decorative motion marks. One precise edit
removed only those marks and restored the same flat chroma field; the eight
character drawings and pose order were otherwise preserved. The edited source
above is the accepted build input.

## Evie source atlas

Generated source: `evie_atlas_chroma.png`
SHA-256: `2b1cd2703388f14525603146545d7b9299e53d68e0d0ead449b3a5d85fe40597`

Prompt:

> Use case: stylized-concept. Asset type: polished 2D game character
> animation sprite atlas for a preschool hide-and-seek game. Image 1 is the
> binding protected Evie identity reference; preserve it unchanged and use it
> only as an identity/style reference. Create exactly eight authored
> chronological full-body frames of standalone Evie, arranged as a precise
> 4-column by 2-row atlas with equal square cells and consistent scale, anchor,
> outline, lighting, anatomy, and identity. Preserve the same young friendly
> brunette mermaid, long flowing chestnut hair, coral/pearl/star hair ornament,
> warm child-friendly face, iridescent shell cap sleeves over a navy-and-cream
> striped top, and luminous pink-coral-gold scaled mermaid tail with a broad
> two-lobed fin. Lamb-a' must not appear. Top row frames 1-4 form a seamless
> underwater hover/swim-idle loop. Bottom row frames 1-4 form one helper cue:
> notice the hiding places, extend an open hand to point, delighted
> giggle/clap, then welcoming cheer. Use polished 2D children's storybook cel
> illustration with genuine authored pose changes. Every cell contains one
> complete uncropped Evie. Use one perfectly flat solid `#00ff00` chroma
> background. No labels, dividers, text, logos, watermark, contact shadow,
> cast shadow, ground, glow, vinyl border, 3D render, extra limbs, costume
> drift, identity drift, or sexualized proportions.

## Deterministic processing

`tools/build_seek_animation_assets.py` removes border-connected chroma,
preserves same-colored interior costume pixels, normalizes the two action rows
into 256x256 cells, and decontaminates residual chroma hue only within a narrow
transparent-edge shell after atlas resampling. It produces:

- `assets/minigames/seek/evie_animation.png` — 4x2, 1024x512 RGBA.
- `assets/minigames/seek/lamma_animation.png` — 4x2, 1024x512 RGBA.
- `assets/minigames/seek/evie_portrait.png` — first Evie idle frame for the
  speaker portrait, avoiding the unrelated Faron portrait and any sticker.

The generated sources are never loaded by the game. Runtime uses only the
normalized outputs, current approved Sky Lagoon meadow art, and existing
Roshan atlases.
