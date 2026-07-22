# NPC 3D WORKORDER — full cast sprite → Meshy migration (owner directive 2026-07-19)

Owner: "start making Meshy models of all of the game characters and abandon
the old sprite style… focus on daddy mermaid next." Gabby is removed entirely
(IP hold — see attic/gabby/), not migrated.

## Key status — READ FIRST

**The Meshy key is NOT in this repo or any fresh session container.** It lived
in `.secrets/meshy_key` (gitignored, never committed) or `$MESHY_API_KEY`;
remote-session containers start clean, so it must be re-supplied every time.
The moment it exists again, one command submits the whole staged batch:

    echo "<key>" > .secrets/meshy_key
    python3 tools/meshy_pipeline.py launch     # submits every stage=="ready" task
    python3 tools/meshy_pipeline.py status     # poll
    python3 tools/meshy_pipeline.py harvest    # download GLBs (+ auto rigging try)

## Staged batch (gen2/meshy/tasks.json)

| task | src | pri | state |
|---|---|---|---|
| npc_daddy | gen2/npc_src/daddy.png | **1** (15k tris) | **ready — Daddy Mermaid first** |
| npc_huluu | gen2/npc_src/huluu.png | 2 | ready |
| npc_kareem | gen2/npc_src/kareem.png | 2 | ready |
| npc_flower_friend | gen2/npc_src/flower_friend.png | 3 | ready |
| npc_wacky | — | 2 | needs_src (crop Wacky; Chuck already 3D) |
| npc_evie | — | 2 | needs_src (crop Evie; Lamb-a' already 3D) |
| npc_harper_fiona | — | 3 | needs_src (split the sisters sheet) |
| npc_faron | — | 3 | needs_src (crop Faron from mama_baby) |

Already 3D, no task: Roshan (v4 shipping), fairy (fairy_v2), Chuck
(chuck_poodle_rigged), Lamb-a' (lamb.glb), craft kitty/birdie.
Sources were white-carded by `tools/prep_npc_sources.py` (transparent PNG →
black-flatten poisons Meshy). Pair sheets need per-figure sources first —
ideally proper Gemini turnarounds (gen2 lane, like roshan_v2) rather than
crops, then flip their tasks to "ready" with the src path (add "src_views"
for turnarounds).

## Per-character pipeline (after harvest)

1. `gen2/meshy/<task>/static.glb` (+ `rigged.glb` if Meshy's auto-rig took —
   expect 422 on mermaid tails: daddy, huluu).
2. Toon bake: shrink/decimate + posterize pass (tools/shrink_glb.py) —
   textures ≤1024 POT, speculars stripped, WW flat-fill look.
3. Rig: Meshy rig if accepted, else weight-transfer in Blender —
   merfolk via the roshan_v2 retarget lane (tools/roshan_v2_retarget.py
   pattern), land kids via the shared 18-bone rig (tools/build_npc_rig.py);
   author/reuse the one looping `idle` clip.
4. Drop at the task's `target` path (assets/characters/friends/<tex>.glb).
   **The loaders are already live** (2026-07-19): `_build_friends` in main.gd
   and the melody StarPerformer prefer `<tex>.glb` over the sprite, play the
   first clip looped, and fall back to the cutout when no model exists — the
   cast converts one file at a time with zero breakage.
5. `python3 tools/glb_check.py <target>`, add the ASSET_LICENSES.md line,
   probes green on CI, then eyeball scale on device (loader assumes
   scale ×4.0, base y +4.0 — tune per model if the silhouette lands wrong).

## Excluded

**Gabby** — removed 2026-07-19, IP hold. Assets preserved in attic/gabby/.
Do NOT stage, generate, or reintroduce her without an owner-approved
original redesign.
