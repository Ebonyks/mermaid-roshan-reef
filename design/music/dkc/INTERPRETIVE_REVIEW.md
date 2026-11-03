# DKC working interpretations and MIDI stress review

The working direction is now explicit for every soundtrack entry. These are adopted, revisable musical opinions: use the original’s audible role and behavior, choose a practical instrument family, and change that choice when a better comparison explains the sound. Missing historical patch names or downloadable MIDI files do not hold up interpretation.

## What was compared

The pass checked 106 indexed MIDI URLs: 105 parsed, representing 75 distinct byte hashes. A further 33-file archive supplied no new hashes. The [expanded search receipt](evidence/expanded_search_receipt.json) records the additional catalogs, targeted searches and inaccessible leads. One malformed alternate MIDI remains rejected.

Thirty original-version YouTube references were acquired for analysis, capped at the first 180 seconds. Two initial version mistakes—an arranged Forest Frenzy and a beta fanfare—were rejected and replaced before the final evidence. The [reference manifest](evidence/original_reference_manifest.json) records URLs, analysis hashes and exact excerpt spans.

Automated listening covered 52 excerpts across all 30 entries. Its broad musical descriptions inform the choices below, alongside MIDI notes and controllers. Generic frequency diagnoses, mood scores and stereo claims from mono analysis are not adopted as facts. [Listening observations](evidence/listening_summary.json).

The note comparison tests pitch-class movement and timing, not preset similarity. Each candidate’s first 65 seconds was fitted within bounded tempo/offset limits, then its 65–100-second region was checked with that fit frozen where enough audio existed. Wrong-original, shuffled-order and transposed controls expose accidental agreement; synthetic known-sequence controls pass. Mirrors were deduplicated by hash for selection. [Results](evidence/midi_audio_comparisons.json).

Twenty-four entries have a usable parsed MIDI candidate. The other six now have explicit ear-led roles and a construction route rather than an empty design row. No replacement audio was rendered or claimed to match native patches in this pass.

## Decisions changed by the evidence

- **Simian Segue:** use the King Meteor transcription as the working scaffold. It retains 390 paired notes in a low bass channel spanning MIDI 28–43. Its named echo tracks should become controlled spatial treatment, not additional full-volume piano/reed players. Lead with dry worn acoustic-piano articulation and keep the pizzicato/reed replies; a sampled-key hybrid is the alternate.

- **Aquatic Ambience:** preserve synthetic movement. The preferred MIDI has extensive volume, modulation and pitch-bend activity; a note-only decode loses meaningful expressive information. Its opening and later-section tonal agreement support the scaffold, while the pad/lead interpretation is guided by the original and composer interviews.

- **DK Island Swing:** the opening-only winner loses agreement later. Choose a balanced scaffold and check the changing sections against audio before reusing it wholesale. Hand percussion, breathy lead, bass and sustained backing each keep their own job.

- **Voices of the Temple:** the highest opening score also fits a wrong recording. Prefer the simpler explicitly named version for initial construction, with the denser Temple Tempest version as an alternate. This is an arranging choice, not a claim that the six-channel file is historically exact.

- **Forest Frenzy and Ice Cave Chant:** later-section evidence changes the balance among transcriptions. Forest’s nature-like track labels are useful role metaphors; they do not prove zoological sample origins. Ice Cave’s fan MIDI composer label conflicts with Rare’s attribution and is not used for credit.

- **Misty Menace:** adopt wind, drone, filtered noise and sparse event timing. Its weak tonal score fits this soundscape reading; do not fill it with an invented melody to satisfy a conventional band template.

- **Short cues:** shuffled-note controls can score well and some comparisons have no valid alignment. Use contour, attack, pitch motion and the final stop directly. Null measurements are unavailable evidence, not negative fidelity grades.

## Current working call sheet

The full [interpretation register](working_interpretations.json) includes roles, available starting routes, selected MIDI URL/hash, reasons, excerpt spans and a specific revision trigger for every entry. “Available starting route” can include a new synth patch or guest capability; it never forces an unsuitable installed instrument.

| Track | Working direction | MIDI starting point |
|---|---|---|
| Theme | Keep the contrast between the small retro opening and the full sampled groove. | [Theme](https://themushroomkingdom.net/sounds/mid/dkcountry_theme.mid) |
| Simian Segue | Lead with a dry, slightly worn acoustic-piano attack and a bouncing low bass; keep the clipped string/reed replies. | [Simian Segue (2)](https://www.vgmusic.com/music/console/nintendo/snes/DKC_Map-KM.mid) |
| DK Island Swing | Let hand percussion establish the place, then open into a breathy pipe/bottle-like hook over low bass and sustained backing. | [DK Island Swing (3)](https://www.vgmusic.com/music/console/nintendo/snes/DKC_-_DK_Island_Swing-1.mid) |
| Cranky's Theme | Use a playful wooden-mallet foreground, clipped bass and bright high replies. | [Cranky's Cabin](https://themushroomkingdom.net/sounds/mid/dkcountry_cranky_cabin.mid) |
| Cave Dweller Concert | Treat tuned percussion, echoes and dark sustained space as the arrangement’s core. | [Cave Dweller Concert](https://www.vgmusic.com/music/console/nintendo/snes/DKC_-_Cave_Dweller_Concert.mid) |
| Bonus Room Blitz | Make a dry mallet/kalimba-like hook bounce against pizzicato bass and compact percussion. | [Bonus Stage (2)](https://www.vgmusic.com/music/console/nintendo/snes/DKC1-BonusRoomBlitz.mid) |
| Aquatic Ambiance | Build a moving synth environment; the melody floats over a real low synth foundation and small bright figures. | [Aquatic Ambiance [2]](https://themushroomkingdom.net/sounds/mid/dkcountry_aquatic_ambiance[2].mid) |
| Candy's Love Song | Use clipped brassy/workstation chord colors and a plucky, syncopated bass rather than assuming a soft piano ballad. | Ear-led phrase/event sketch |
| Bad Boss Boogie | Keep the sharp electric/synthetic edge and pulsing accompaniment. | [Bad Boss Boogie](https://www.vgmusic.com/music/console/nintendo/snes/DKC_-_Bad_Boss_Boogie.mid) |
| Mine Cart Madness | Keep a driving low pulse and bright lead/answer layers with sustained harmonic backing. | [Mine Cart Madness](https://www.vgmusic.com/music/console/nintendo/snes/Mine_Cart_Madness.mid) |
| Life in the Mines | Use a breathy bottle/flute-like foreground against sustained synth strings, rounded picked bass and small rhythmic accents. | [Life in the Mines (4)](https://www.vgmusic.com/music/console/nintendo/snes/DKC_Mines-KM.mid) |
| Voices of the Temple | Choose a choir-like atmospheric center with low resonance, sparse melodic gestures and a defined percussive pulse. | [Voices of the Temple](https://www.vgmusic.com/music/console/nintendo/snes/DKC_-_Voices_of_the_Temple.mid) |
| Forest Frenzy | Orchestrate the pulse as playful natural-sounding gestures: rattles, feet, birds and ripples translated into distinct musical voices. | [Forest Frenzy](https://themushroomkingdom.net/sounds/mid/dkcountry_forest_frenzy.mid) |
| Treetop Rock | Use a bright mallet/pipe/pluck exchange over short bass rather than assigning one guitar as the whole identity. | [Tree Top Town](https://themushroomkingdom.net/sounds/mid/dkcountry_tree_top_town.mid) |
| Funky's Fugue | Center the funk bass and short clean/muted guitar-like chops, with orchestral/vocal-like hits as punctuation. | [Funky's Flights (2)](https://www.vgmusic.com/music/console/nintendo/snes/DKC_Funkys_Flights-KM.mid) |
| Misty Menace | Treat this as an authored soundscape with a loose pulse, not a melody waiting for a fuller band. | [Misty Menace (GS)](https://www.vgmusic.com/music/console/nintendo/snes/DKC_Mist-KM.mid) |
| Northern Hemispheres | Keep the dark wind/drone opening and the later bright repeated keys or arpeggio as a deliberate change of scale. | [Northern Hemispheres](https://themushroomkingdom.net/sounds/mid/dkcountry_northern_hemispheres.mid) |
| Ice Cave Chant | Use a glassy mallet/harp weave with warm plucked bass and soft breathy sustained color. | [Ice Cave Chant [2]](https://themushroomkingdom.net/sounds/mid/dkcountry_ice_cave_chant[2].mid) |
| Fear Factory | Keep a mechanical electronic rhythm section with distinct bass, ostinato and lead functions. | [Fear Factory (3)](https://www.vgmusic.com/music/console/nintendo/snes/DKC1_FearFactory.mid) |
| Gang-Plank Galleon | Use a reed/accordion-like opening, then let the harder sustained lead and rhythm section take over. | [Gang-Plank Galleon (3)](https://www.vgmusic.com/music/console/nintendo/snes/DKC_-_Gang-Plank_Galleon.mid) |
| K. Rool's Cacophony | Use a sparse, subdued synthetic phrase with gentle plucked accents, low support and a lingering tail. | Ear-led phrase/event sketch |
| The Credits Concerto | Use buoyant keys and pipe-like lead exchanges over a firm plucked bass and concise kit. | [End Credits](https://themushroomkingdom.net/sounds/mid/dkcountry_end_credits.mid) |
| Fanfare | Make a short coordinated brass-like statement with low reinforcement and a clean release. | Ear-led phrase/event sketch |
| Level Goal | Use a compact bright fanfare: lead/harmony and bass land together, followed by a small tail. | [Level Clear XG](https://themushroomkingdom.net/sounds/mid/dkcountry_level_clear(XG).mid) |
| Bonus Win | Use an expanded version of the success vocabulary with a distinct concluding phrase. | [Bonus and Boss Victory XG](https://themushroomkingdom.net/sounds/mid/dkcountry_bonus_boss_victory(XG).mid) |
| Bonus Lose | Keep a short descending/comic mallet phrase, bass punctuation and airy high reply. | [Bonus Lose](https://themushroomkingdom.net/sounds/mid/dkcountry_bonus_lose.mid) |
| Lost Life | Use the short fall/turn as a complete gesture, including its bent low voice and stop. | [Death](https://www.vgmusic.com/music/console/nintendo/snes/DKC_Death-KM.mid) |
| Bonus Room Opened! | Treat this as a tiny reveal gesture whose attack and tail carry the meaning. | Ear-led phrase/event sketch |
| Extra Life Balloon | Use a light, compact upward reward gesture with a crisp finish. | Ear-led phrase/event sketch |
| Game Over | Preserve a slow, sparse final-state gesture and its silence/tail; do not assume it is identical to K. Rool’s cue. | Ear-led phrase/event sketch |

## How to use the findings

Begin construction from the selected note scaffold and the adopted roles. Keep bass register and rhythmic placement. Translate meaningful controllers into the chosen instrument’s articulation/envelope behavior. Merge echo-only copies into deliberate delay/reverb where they represent the same gesture; retain separate notes when they actually form an answer or counterline.

When the exact source identity remains ambiguous, choose the best supported timbre now, keep one alternative, and use the register’s revision trigger during the next audition. Change the interpretation when the alternative explains the original more convincingly. Do not wait for a factory-preset name, and do not invent one.

The highest-value resource gaps are now concrete: short clean/muted electric-guitar colors, brass/reed/accordion voices, wooden and glassy mallets, nonverbal choir, and evolving workstation-like synth patches. Existing UVI banks and custom Falcon work should be searched for those roles before buying or adding anything. Soul Bass and Soul Drums remain resources rather than mandatory choices; Fear Factory’s electronic rhythm section should remain electronic.

Next construction tests should audition the adopted roles in source-matched phrases, starting with Simian Segue and Aquatic Ambience, then the contrasting sections of DK Island Swing and the electronic core of Fear Factory. Complete-song, native timbre and owner acceptance remain separate from this working design.

## Evidence and audit scope

The [event summaries](evidence/midi_event_summaries.json) retain tracks, channels, programs, note ranges, controllers, bends, tempo changes and note-pairing checks without publishing a full score. Program names and fan credits are evidence about each transcription, not original-game authority.

The [impact](../../audit_impacts/dkc-interpretive-midi-stress-20261102.json) records the original-instrument priority, owner correction, exact baseline, executed checks and limitations. No game audio or runtime behavior changed; MA-AUDIO-001 remains FIXED_PENDING_VERIFICATION. Private reference media remains outside the repository; the durable study contains links, hashes, summaries and decisions.
