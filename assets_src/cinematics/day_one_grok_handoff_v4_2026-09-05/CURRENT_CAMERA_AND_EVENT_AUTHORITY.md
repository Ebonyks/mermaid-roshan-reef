# Current castle and suds-finale direction

This owner revision supersedes the old C11 closed-rainbow-door copy blocks and C13 clean-without-lather drafts. Copied `written_guide/C11_*` and older arena choreography documents are historical records, not executable direction. Use the active shot cards and this document.

## C11: correct the animation, keep the game layout

The implementation loads `HALL_REDRAW_ROOT = assets/flats/castle/main_hall_redraw_2026-08-03/`, with 8 by 2 tiles derived from the 7280 by 2048 panorama. The approved native screen drawings are [A](references/6e840715f1_accepted_screen_a_native_1672x941.png) and [B](references/7e77e4c29b_accepted_screen_b_native_1672x941.png), copied without alteration from `assets_src/imagegen/castle_main_hall_redraw_2026-08-03/`. They are 1672 by 941 originals, not native 2K; the runtime-sized derivatives do not prove native resolution acceptance.

The old `main_hall_2screen` family used by C11 is superseded here. Its windows, hanging chandeliers, navy banners, rainbow arch and closed shell door are not the implemented right-half hall. The current large arch has a shell crown, tied-open purple curtains, gold tassels, pale stairs with a red runner and an open blue-masonry corridor. No door leaf or handle exists. When the Royal Hall event is active, `_tick_royal_hall_mist` fades its mist out; do not turn the mist into a barrier the child must break.

| Landmark | Full-hall logical coordinates (3344 x 941) | Screen-B logical coordinates (1672 x 941) |
|---|---|---|
| Stuffie Playroom foot | (2015, 620) | (343, 620) |
| Craft Room foot | (2215, 620) | (543, 620) |
| Mermaid Pool foot | (2415, 620) | (743, 620) |
| Bubble Bath foot | (2615, 620) | (943, 620) |
| Royal Hall foot | (3045, 620) | (1373, 620) |

The Royal Hall interaction rectangle is `(2870,150,350,470)` in **logical hall coordinates**, not native panorama pixels. Its foot normalized to the full hall is `(0.910586,0.658874)`. Dividing 3045 by the 7280 native width is a unit error that wrongly moves the portal toward the center. These coordinates verify world relationships; they are not literal screen positions after a new camera projection.

C11-S01 shows the four correct doorway emblems (teddy, palette, blue droplet, three pearls) and the far-right arch from a low-left oblique view. C11-S02 is newly added to the reshoot queue: its retained footage also uses the obsolete door. The replacement uses a closer rear/child-height angle and stops Roshan at the stair foot. C11-S03 then cuts to the already-established empty dusty arena; do not invent an opening door or a new connecting corridor to simulate that cut.

Four floor trails are an owner-requested cinematic visualization of the four completed room states. They must not be described as literal footage of an implemented four-trail runtime effect. The current game saves and event logic remain unchanged by this handoff.

## C13: make the cleanup a complete causal action

| Shot | Camera and duration | Start | Action | End |
|---|---|---|---|---|
| C13-S04 | Low front-left; one <=4% push-in; 5s | Dusty intact Puff; first small sponge lather patch | All four friends build suds together | Generously sudsy Puff; full company |
| C13-S05 | Elevated front-right; fixed; 8s | Same foam coverage and physical cast blocking; two tall shell-topped blue/coral side windows, two ivory columns, centered chandelier, chests/shelves and stone octagon remain locked | Everyone removes the suds; the last wipe/rinse visibly clears the outer giant dust body as one tiny friend peeks and steps out | Exactly four helpers and one rainbow friend; giant dust body, face and ears completely absent |

This is a camera change around the same action, not a mirrored room or a shuffle of actors. Roshan and Daddy stay on Puff's left, Rumi on his right, Eagle in front. Use foreshortening and depth in the newly generated frames; do not fake a new perspective by moving or warping a flat plate.

S04 uses target frames `[0,24)`, `[24,72)`, `[72,102)`, `[102,120)`. S05 uses `[0,24)` sudsy opening, `[24,96)` coordinated foam removal, `[96,132)` continued final wipe/rinse contact while the outer giant dust body visibly thins, `[132,156)` curl-part/peek during active wipe/rinse, `[156,174)` one small step as the final wipe/rinse clears the giant body/face/ears completely and tools withdraw/water stops/wings fold, `[174,192)` four-helper/one-friend settle. All ranges are zero-based, half-open, at the authored target rate of 24 fps, not a claim of exact Grok frame control.

Foam is a surface coating through S04 and the sudsy S05 opening. For S05 only, the owner-directed event keeps the final wipe/rinse visibly active through 6.5 seconds as a causal authored full-frame change. Tools withdraw, water stops and wings fold only as the final giant dust body, face and ears clear in `[156,174)`. By the final hold, exactly one tiny rainbow friend remains with the four helpers. No cross-dissolve, compositing shortcut, snap, giant walk-off, body explosion, pain, duplicate friend, additional spawn or sudden pop-in is allowed. Keep the friend no taller than one sixth of the former giant body at the same depth, without growth during the reveal. This owner correction supersedes the older “giant remains intact/additional friend” S05 wording only; S04 remains the intact giant-lather shot.

The reference is the restored native dusty-attic master [dusty_attic_arena_native_1254.png](references/owner_restored_arena/dusty_attic_arena_native_1254.png), SHA-256 `9cb4b02dc4a56e1436ea0a6b21dccf4ef751716d213e3ff7624571f15a9e2cb6`, 1254×1254. It visibly contains two tall shell-topped blue/coral windows on the side walls, two ivory columns, a centered chandelier, chests/shelves and a stone octagon; these landmarks are locked for the S05 camera.

Daddy's hands stay behind the gold ferrule on the handle; the bristles point toward Puff and perform contact. No hand/handle striking, backward grip, human leg, shoe or boot. Roshan keeps her plain pink top, rainbow-streak hair and continuous tail. Room dust and cobwebs remain; the team cleans Puff, not the entire arena.

The lather storyboard implies Rumi's rinse through her hand aim and bubbles. That is sufficient to communicate narrative order, not proof of delivered action: motion review must see one thin stream reach Puff's upper-right body curls without crossing his face or ears. Reject a static pointing pose that contributes no cleaning.

## Review and delivery boundary

Every selected first frame is still presented for the owner's explicit approval. Storyboards communicate shot order only and never become IMAGE_1 through IMAGE_4. Sol recommendations are not human approval. The old no-suds frames and rejected attempts are retained as history, never enabled as jobs.

This is the revised rough-draft Grok handoff, not a newly rendered movie or an in-game update. The proposed full-team foam sequence and additional rainbow friend are not claimed to be implemented in the current game. The existing protected artwork is untouched. Archive publication, generator readiness and final delivery acceptance remain separate gates.
