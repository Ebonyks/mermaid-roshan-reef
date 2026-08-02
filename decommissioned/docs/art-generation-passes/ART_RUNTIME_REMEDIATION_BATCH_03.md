# Runtime Art Remediation Batch 03

_Built: 2026-07-14 from approved style-review masters_

This pass promotes the remaining approved 2D candidates only where they satisfy
their actual gameplay role. Protected book art, character art, friend cutouts,
and child-owned toys were not opened or modified.

| Runtime role | Implementation | Provisional score |
|---|---|---:|
| Swaying foliage | `assets/terrain/leaf.png` is a single broad illustrated leaf cropped from the approved plant family and normalized to 512x1024 RGBA. | 4/5 |
| Craft rainbow control | `assets/mg/rainbow_swatch.png` is the approved fin-shaped swatch, normalized to 512px and displayed without aspect distortion. | 4/5 |
| Craft fish color zones | The registered body, fins, and line form a replaceable three-layer craft family. The current composite is 4/5, but no individual drawing is protected. | 4/5 |
| Fetch ball | The old glossy RGB texture is no longer consumed. A Mobile-safe shader draws six matte pastel panels with restrained navy seams. | 4/5 |
| Lagoon sky | The visible photoreal HDR path is retired. Day and dusk now use seamless illustrated color bands under the Mobile renderer. | 4/5 |
| Kart finish | `finish_banner.png` provides a shell-tied navy-and-cream checker cue; the ground checker and posts now share its matte palette. | 4/5 |
| Kart ramps | `boost_ribbon.png` replaces the text arrow with a large aqua/coral/lavender motion cue. | 4/5 |
| Ambient mantas and turtles | Normal play now uses the established 5/5 GEN2 stingray and turtle models; procedural ribbon silhouettes are missing-file fallbacks only. | 5/5 |

## Functional audit decision

The three decorated rock clusters in Batch 04 candidate 021 were not promoted
as hazards. They contain starfish and shells, while those silhouettes already
mean rewards and pickups in the kart mode. Reusing them as obstacles would make
the art prettier but the one-finger, non-reader interaction less legible.

The continuation audit also corrects the craft cat to 1/5. Its body/accent
files duplicate a plush-style render and its line layer is blank. It remains an
active documented exception: the owner has placed stuffed animals in a hard-no
zone for automatic generation, so replacement waits for the child's real toy
source. This batch does not modify or disguise it.

The alpha audit found that `bird_line.png` is also blank. Its body/accent are
readable but are grayscale transformations of protected Baby Eagle art, so the
preview is corrected to 2/5. It is likewise excluded from automatic redesign
and waits for an owner-approved source-art layer separation.

## Technical contract

- Runtime textures are RGBA and power-of-two, with a 1024px maximum side.
- `tools/promote_style_review_batch_04.py` reproduces every promoted crop and
  normalization from the review masters.
- Existing craft layer names and ordering are unchanged. Future fish passes may
  replace all three images together while retaining independent color zones.
- The HDR and old beach-ball files remain in inventory for provenance but no
  longer have runtime references.
- Final acceptance still requires Mobile-render screenshots. A live Godot
  editor currently owns the project lock, so this batch cannot refresh imports
  or run the headless probes until that lock is released.
