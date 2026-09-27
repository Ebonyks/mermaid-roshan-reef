# Battle of the Bands — prototype and refinement handoff

Status: `CANDIDATE`; owner commission 2026-09-20. The candle contest is a battle
of the bands using the recorded Iko Iko, with Roshan drumming in her Pop Star
costume and recorded King/Prince grindcore outbursts. Daddy Mermaid plays
ukulele and Baby Eagle plays bass; the Ember Prince plays metal drums and
the Ember King leads with electric guitar. The Prince has a comically complex
kit with one kick drum and the trial crowned-flame Ember family emblem. Baby
Eagle's corrected bass has four strings, four posts and four tuning keys. This supersedes the
stomp/dodge **story direction** in the earlier lawn draft, not its still-live
runtime implementation. The King cheats after Roshan succeeds; the child never
has to fail to advance the story. The Prince remains conflicted and leaves with
his father. Preparation, cake, friends and earned rewards remain intact.

## Play the candidate

Open `scenes/battle_of_bands_prototype.tscn` in Godot **4.7.2-stable** and run
the current scene (F6), or run the engine with
`--path . scenes/battle_of_bands_prototype.tscn`.
Tap the glowing drum or cymbal through twelve forgiving hits; there is no
timing deadline. Three lights mark completed phrases. After success, touch the
arrow through cheating theft, Prince reaction, and the hopeful ending. Back
closes this standalone review scene. It is not yet linked from the shipped
Opera Hall or the chapter's lawn route.

Progress uses `user://battle_of_bands_prototype.cfg`, separate from
`reef_save.json`. The exported `recording` AudioStream and `king_outburst_cues` / `prince_outburst_cues`
start/end pairs provide a binding seam. No recording was located by the Iko Iko
name or metadata search at task start; no guessed musical timecodes or
replacement singing are presented as the owner's track. The exact spoken
objective is also missing. This is an adult-assisted prototype until those
audio/comprehension gates pass.

## Existing work and reuse

Pop Star currently has sound-check hold, dance choice, rhythm echo, and encore
circle phases, with a practice/stage plan in ordinary freeplay. Chapter 2
already pairs Roshan with Rumi and carries musical props onto the birthday
lawn. `chapter_two_lawn_finale_2d.gd` still implements the old protection
contest; its save/story semantics are the integration starting point.

Reuse the Pop Star stage tiles/costume, approved King V4 and thin Prince,
rainbow candle and lawn sources. No suitable approved 2D drum kit or drummer
pose was found. The existing portrait carries a microphone; the bounded new
drummer asset fills that pose/prop gap. New pose/art is a review candidate,
not accepted cinematic art. Protected originals remain untouched.

## Handoffs and evidence

The self-contained [Grok review packet](../assets_src/cinematics/battle_of_bands_2026-09-20/START_HERE.txt)
includes actual references, an inspectable thirteen-shot board, one V1 card and
prompt per shot, an empty explicitly blocked recording cue sheet, and the
[Codex refinement work order](../assets_src/cinematics/battle_of_bands_2026-09-20/CODEX_REFINEMENT.txt).
Six seconds per draft card is provisional coverage, not measured song timing.
Split/reorder coverage around the supplied recording after listening.

The [impact record](audit_impacts/battle-of-bands-20260920.json) owns exact
baseline, changed files and machine evidence. The focused probe exercises
passive/wrong input, focus loss, success-before-theft and preserved completion.
No existing master finding is claimed repaired. `ARCHIVE_COMPLETE`,
`GENERATION_READY`, and `DELIVERY_ACCEPTED` remain separate; missing recording,
accepted clean first frames, final bindings and human review block generation.
Gameplay composition is not cinematic delivery. Full integration, voice,
sound synchronization, device performance, child comprehension and owner
acceptance remain open.
