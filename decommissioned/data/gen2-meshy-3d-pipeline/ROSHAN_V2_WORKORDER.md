# ROSHAN V2 — the hero overhaul (owner directive 2026-07-11)

She is the most important character in the game. Goal: a true 3D Roshan —
abandon the stuffed-animal sculpt — with a comprehensive movement set.
Design spec = the owner's turnaround sheets (gold tiara with aqua gem, pink
ruffle top, NO backpack, rainbow-streak brown hair, iridescent pastel tail).
Repo copies live in gen2/turnarounds/roshan_v2/ (front is a deliberate open
A-pose: clean geometry for photogrammetry AND clean weight transfer).

## The one architectural rule

Roshan is ALREADY a rigged 26-bone character (assets/characters/roshan.glb).
player.gd drives her by bone NAME every frame — procedural tail sine, fin
flutter, hair sway (see tools/build_roshan_rig.py header). Therefore:

**The V2 mesh replaces the SCULPT, never the SKELETON.** Meshy's auto-rig is
not used (wrong bone names, and it rejects mermaid silhouettes anyway). The
new body is weighted onto the EXISTING armature with the exact 26 names
(tools/glb_check.py ROSHAN_BONES). Every existing behavior — swim, skins,
cosmetic sockets — keeps working the moment the mesh lands.

## Stages

**R2-A: mesh (BLOCKED on Meshy key — task staged in gen2/meshy/tasks.json).**
Multi-image image-to-3D from the three turnaround views, highest quality
target; then the standard shrink+posterize toon-bake pass. Gate: silhouette
readable, face clean, tail fluke intact.

**R2-B: weight transfer (automatable headless in Blender — it IS available
in the work container now, unlike when build_roshan_rig.py was written).**
Import roshan.glb (keep armature), delete old mesh, align+scale V2 mesh to
the rest pose, parent with automatic weights, then fix the known trouble
zones (hair↔chest bleed, fin tips) with scripted vertex-group cleanup.
Export as assets/characters/roshan_v2.glb. Ship behind skin id "classic_v2"
first so the owner can A/B on device before it becomes the default. Gate:
probe suite + the skin-audit probe (every mode moves effectively).

**R2-C: the movement set.** Two layers, additive:
1. The procedural layer (already alive): swim wave, fin flutter, hair sway,
   idle bob — driven by player.gd on the shared bone names, tuned per-verb
   (fast swim = bigger amplitude, sleep = slow breathing curve).
2. Authored clips, scripted as keyframes in Blender on the same armature and
   baked into roshan_v2.glb: wave_hello, clap_celebrate, spin_twirl,
   sleep_curl, look_around, giggle_bounce. Wired through an AnimationPlayer
   with a small verb API in player.gd (play_verb("wave")) triggered from
   game events: friend greet → wave_hello, trophy → clap + spin, bedtime
   flip → sleep_curl, idle >20s → look_around. NO fail/hurt clips — the
   game has no fail states.

## Sequencing note
R2-A fires the moment the Meshy key is re-supplied (17 other staged tasks
launch in the same batch). R2-B/C scripts can be written and dry-run against
the CURRENT roshan.glb mesh meanwhile — the armature is identical, so the
clip work is not blocked on Meshy.
