# Mermaid Roshan v4 rig and wireframe audit

Date: 2026-07-15

Source: `assets/characters/roshan_v4.glb`

Method: non-destructive source-GLB linear-blend skinning, rendered in Blender 4.4.3

## Conclusion

Roshan v4 has a valid, loadable skeleton and valid skin data, but it is not a
clean or bilaterally consistent deformation rig. The most serious defect is the
anatomical left (`+X`) arm/hand: it exists, but it is underbound and heavily
cross-weighted to the torso. T-pose, overhead, and clap tests visibly pull long
triangles and sheets out of that side of the torso, sleeve, and arm.

Roshan does **not** literally lack a left hand, but the missing-looking diagnosis
is functionally fair. The GLB contains the `hand` joint and 174 rendered vertices
bound to it. Their bind envelope is only `0.034 x 0.057 x 0.040` units. The right
`hand2` joint has 705 bound vertices (586 above the audit's 0.12 hand-probe
threshold) spanning `0.150 x 0.209 x 0.202`. The left hand is therefore present
as a very small, substantially incomplete or underbound region. Neither hand has
finger or palm articulation.

No source character asset was written, exported, recompressed, or replaced by
this audit. The source GLB's SHA-256, byte size, and modification time were
unchanged before and after every final run.

## What was tested

The audit imports the shipping GLB and uses its own nodes, rest transforms,
inverse bind matrices, joint indices, and weights. It computes linear blend
skinning directly, rather than trusting Blender's slightly different armature
evaluation. Every rendered pose is rejected unless its measured hand centroids
match the direct source-GLB result within `0.000005` model units.

Five diagnostic states were rendered from front, three-quarter, and side views:

- imported rest pose;
- a mathematically lateral T-pose (the user's “t-frame”), with both
  shoulder-to-wrist chains at `0.00°` from outward model X;
- the current `cheer` overhead hold from `scripts/player.gd`;
- the current `clap` open/rebound key;
- the current `clap` contact key at `t = 0.50`.

The generated contact sheet is at
`audit/roshan_wireframe_final/roshan_rig_contact_sheet.png`; exact measurements
are in `audit/roshan_wireframe_final/audit_report.json`. Recreate both with:

```powershell
blender --background --factory-startup `
  --python tools/audit_roshan_wireframe.py -- `
  --glb assets/characters/roshan_v4.glb `
  --out audit/roshan_wireframe_final --resolution 720
```

## Structural health

The parts required for Godot runtime compatibility are sound:

- one mesh primitive, one skin, 57 joints, 40,795 triangles;
- all required procedural arm, body, tail, hair, and socket names are present;
- no baked clips and no morph targets, consistent with procedural animation in
  `scripts/player.gd`;
- inverse-bind identity residual: `3.3415e-6` maximum;
- rest-quaternion norm error: `8.17e-8` maximum;
- source weight-sum error: `4.47e-8` maximum;
- all positions, weights, bind matrices, and joint indices are finite/in range;
- every imported deform vertex is weighted, with no more than four influences.

An exhaustive numeric sample of the existing swim and seven verb cages passed
the existing 45/45 acceptance checks. That confirms runtime compatibility, but
the rendered stress poses show that those gates do not presently reject the
left-side shard/stretch defects.

## Pose findings

### T-pose

The joint solver reaches a true lateral T-pose: both upper arms and forearms
measure `0.00°` from their intended horizontal directions. This exposes rather
than creates the underlying asymmetry.

- The right shoulder-to-wrist chain is `0.4613` units; the left is `0.3312`.
  The right chain is `39.3%` longer.
- Shoulder planes differ by `0.0501` vertically and `0.2237` in depth.
- The left arm pulls visible sheets/spikes from the torso and sleeve.
- Maximum arm-connected edge-length change is `0.0847` units; 158 arm
  triangles grow beyond 3x their rest area.

A generic mirrored retargeter cannot correct the different shoulder planes and
chain lengths. Each side currently needs its own authored angles.

### Arms overhead (`cheer`)

The current per-side `cheer` keys do put both hands overhead. Their weighted
centroids differ by only `0.0342` in height, but by `0.0956` in depth, and their
overall separation is `0.4816`.

The silhouette is not deformation-safe: the left sleeve/arm visibly tears into
long shards near the shoulder. Maximum arm-connected edge-length change is
`0.1054` units; 216 arm triangles exceed 3x rest area and 26 collapse below
0.2x.

### Clap

The authored motion moves the weighted hand-centroid gap from `0.4234` at the
open key to `0.2775` at the supposed contact key. The remaining gap is `14.6%`
of Roshan's model height, or about `1.03` world units at the player's `3.7`
model scale. It is a near-clap, not hand contact.

At the contact key, maximum arm-connected edge-length change is `0.1132` units;
238 arm triangles exceed 3x rest area and 27 collapse below 0.2x. The left
torso/sleeve shards are visible in the front and three-quarter wireframes.

Because each hand is a single rigid joint, the rig cannot independently orient
palms or fingers to sell a clap. Real palm contact must come from better hand
geometry/binding plus upper-arm, forearm, and rigid-hand keys, or from adding a
small hand articulation chain.

## Confirmed rig problems

1. **Left hand is present but nearly absent as a usable hand region.** The
   anatomical-left `hand` group has 174 vertices, total weight 158.1, and a
   `0.034 x 0.057 x 0.040` bind envelope; anatomical-right `hand2` has 705
   vertices, total weight 309.6, and a `0.150 x 0.209 x 0.202` envelope. This
   supports the visual impression that the left hand is missing or incomplete.
2. **Severe one-sided torso contamination.** Of 977 rendered vertices influenced
   by the left arm, 863 also carry more than 5% combined `root`/`spine1`/`chest`
   weight; median contamination is 30.2%. The left forearm reaches 66.2%. The
   right arm's median and maximum torso contamination are both 0%.
3. **Mismatched arm skeletons.** The right shoulder-to-wrist chain is 39.3%
   longer, with materially different shoulder height/depth and elbow geometry.
4. **Visible deformation spikes.** Direct source-GLB skinning confirms long
   torso/sleeve triangles in T, overhead, and clap poses; these are not a Blender
   conversion artifact.
5. **Unclean topology.** After a practical `1e-4` positional weld, the mesh still
   has 620 one-face boundary edges, 59 edges used by more than two faces, and
   four geometric shells (20,242, 288, 51, and 4 welded vertices). Some open
   hair/clothing boundaries may be intentional, but the small detached arm/hand
   fragments and four-vertex chip are not clean production topology.
6. **No clavicles, palms, or fingers.** Shoulder shaping and clapping must be
   faked entirely through upper arm, forearm, and one rigid hand joint per side.
7. **Some animation targets are inert.** Legacy `hair1`/`hair2`/`hair3` and
   `hairL1`/`hairL2` have zero weighted vertices. The active strand rig carries
   most hair motion, but any verb keys aimed only at those legacy groups have no
   visible effect.

## Recommended repair order

1. Restore/verify a complete anatomical-left hand mesh and bind it comparably to
   the right hand, preserving Roshan's existing illustrated design.
2. Remove `root`/`spine1`/`chest` influence from the distal left arm and hand;
   retain only a narrow, deliberate shoulder blend.
3. Rebuild matched bilateral shoulder planes and shoulder-to-wrist proportions,
   then rebind both arms consistently.
4. Weld/close the arm and torso boundaries; remove the detached 51-vertex and
   four-vertex fragments after confirming they are not intentional art layers.
5. Retune separate left/right T, overhead, and clap keys. Make the clap reach
   actual palm contact and verify palm facing from the gameplay camera.
6. Re-run this direct-GLB audit, the 45 motion-cage checks, Godot probes, and a
   Mobile-renderer gameplay-camera inspection before replacing the shipping GLB.

The first two items should be treated as one repair: fixing only the bones will
not restore a deficient hand, and fixing only the hand mesh will leave the
torso-cross-weighting that causes the visible shards.
