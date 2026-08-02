# Royal Kitchen v3 kettle correction - 2026-07-29

Status: **accepted production source on `codex/kitchen-audit-fridge`**

## Defect and scope

The accepted Kitchen v2 frame painted the small golden stove kettle with two
spouts. Kitchen v3 changes only that defective object. The refrigerator,
single opaque shell light inset, architecture, appliances, furniture, floor,
lighting, palette, and composition remain inherited from the accepted v2
source.

## Accepted files and hashes

- Parent full frame:
  `room_kitchen_fullframe_v2_1672x941.png`
  - SHA-256:
    `8faa4e15e60503cb0303434b77461fa559a81c3d021eb6c3165e9ed176bfbf3e`
- Native ImageGen chroma source:
  `room_kitchen_kettle_single_spout_chroma.png`
  - SHA-256:
    `183d86ab56f36aee01ad5f6276a7bef9723f1dacb67a257fe2244d4d20fbdfc6`
- Locally alpha-extracted kettle:
  `room_kitchen_kettle_single_spout.png`
  - SHA-256:
    `7ace2fda18c48ad7e9da6dc5c233fdab3607d3736506b49689615dc3801ce5a2`
- Corrected complete frame:
  `room_kitchen_fullframe_v3_1672x941.png`
  - SHA-256:
    `7824977df5c875246054bc480eb3b5bdaa00b41ca1b7da1e532216e2844b33f0`

## Production method

1. OpenAI built-in ImageGen produced one isolated, single-spout kettle on a
   flat green field, using the v2 kettle crop only as the identity/style
   reference.
2. The installed ImageGen chroma helper removed the flat field with a
   24-point hard-key tolerance, despill, and one-pixel edge contraction.
3. `tools/repair_kitchen_kettle.py` restores the old kettle footprint from
   surrounding pixels and alpha-composites the complete replacement kettle at
   the same stove location.
4. The complete flattened v3 frame is normalized and layered by
   `tools/build_castle_room_layers.py`; no runtime kettle overlay is used.

Rejected full-frame and crop edits were not promoted because they changed
unrelated room pixels or reframed the source.

## Final accepted ImageGen prompt

```text
Use case: precise-object-edit
Asset type: isolated replacement object for a 2D storybook game background
Input image: identity, shape, material, lighting, outline, and viewing-angle reference for the small golden kettle on the stove.
Primary request: Recreate only that same compact polished golden kettle, but with exactly one spout: retain the longer upturned spout on the kettle's right side and remove the erroneous left spout entirely. Keep its rounded squat body, small lid knob, arched top handle, warm copper-gold highlights, dark plum/brown storybook outline, and straight-on slightly elevated kitchen view.
Scene/backdrop: perfectly flat solid #00ff00 chroma-key background for background removal.
Composition: one complete kettle centered, generous even padding, no cropping.
Constraints: one kettle, exactly one right-side spout, one arched handle, one lid; crisp complete outer silhouette. The background must be one uniform #00ff00 with no shadows, gradients, texture, reflections, floor plane, or lighting variation. Do not use #00ff00 in the kettle. No cast shadow, contact shadow, reflection, stove, wall, pans, utensils, text, watermark, or additional objects.
```
