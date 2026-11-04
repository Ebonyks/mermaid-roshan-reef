# DKC six track production and artistic decisions

This production pass develops the four existing studies, Simian Segue, DK Island Swing, Aquatic Ambiance and Fear Factory, and adds Life in the Mines and Funky’s Fugue. The six arrangements establish a practical method for the rest of the game’s score: preserve the source’s recognizable melody, instrument families and tonal relationships, then create character through touch, phrasing, independent timing and changes in instrumental responsibility.

The selected editions are private production candidates. The native renders, note and controller records, successive complete mixes and editable part sessions are retained. Source and arranging criteria support the choices below; complete subjective listening and owner musical acceptance remain open. In particular, automatic approval review rejected sending the new private candidates to the Gemini music listener because that transfer was not explicitly authorized. No candidate upload occurred.

The [production receipt](production_receipt_v1.json) identifies the actual selected audio, versions, hashes and measurements. The [performed call sheets](production_call_sheets_v3.json) bind the actual instruments to profile revisions and private native sessions. The [iteration register](production_iterations_v1.json) distinguishes source failures, performance development, alternatives and selected editions. These records supplement the [thirty cue production guide](SOUNDTRACK_REVISION_GUIDE_V2.md), rather than replacing its remaining soundtrack scope.

## Musical direction

Original in-game instrument identity takes priority over a convenient preset or the established cast. Fear Factory keeps a synthetic bass, electronic kit and electronic lead. Aquatic keeps its evolving synthetic field and rounded synthetic melody. A natural flute is an alternative to test, not the automatic destination for every breathy source. The roster contributes ways of phrasing and collaborating; it does not determine what the original instruments must become.

The aim is a more animated band interpretation with a clear foreground. Bass releases, the weight of repeated notes, breathing gaps, a percussion answer and a deliberate withdrawal can create life without rewriting the hook. New notes are exceptional and identified. No blanket random humanization or soundtrack-wide swing setting is used.

Bonobo remains the primary producer reference. The selected band ideas draw on Monty Alexander’s separation of melody and support, George Porter Jr.’s recognizable low figures, the Meters’ interlocking guitar and rhythm roles, and the percussion profiles’ distinction between a stable cycle and an answering gesture. These are principles for the fictional collective. The historical artists did not perform these recordings.

Cuban and African popular-music references remain specific optional influences. The exploratory son cell uses a consistent two–three orientation: beats two and three in its first bar, then one, the and of two, and four in the second. It appears in an alternate Island/Funky arrangement. It is not imposed on the ambient tracks or presented as proof of the original soundtrack’s historical rhythm. The [influence register](performance_references_v2.json) retains the Cuban piano, son, clave, Orchestra Baobab and AfroCubism study routes and their separate documentary limits.

## Source corrections that changed the music

### The selected MIDI notes required a second register check

The selected six MIDI scaffolds favor zero pitch-class transposition against the cached original references. Their notes remain at those source pitches. Chroma comparison does not identify an octave error, however. Native test notes showed that the initial original FM models sounded an octave below incoming MIDI, and the captured Cuba Bass also produced an octave-low result. The correction is inside the instruments, not a transposition of the score.

The corrected Cuba Bass was tested at the source’s low D and at three higher notes. The measured fundamentals follow D1, B1, E2 and C3 within approximately two cents in that test. Simian’s upright was separately tested in its actual MIDI 28–43 territory. A high test note outside that bass’s useful source range did not justify moving the whole bass line.

The first two full roughs are retained as rejected source diagnostics. They are not offered as approved reference backings. Their errors demonstrate why a finite, non-silent render is insufficient evidence of fidelity.

### Percussion labels and captured kit states were insufficient

The R78 state had its hat and cymbal components disabled. After enabling them, direct one-hit tests established which original MIDI triggers actually sounded. The ride-bell and splash variants that remained unavailable use the verified ride and cymbal strokes, with the substitution recorded.

Several other source percussion notes were initially being collapsed into unrelated sounds. Simian’s cabasa and frame-jingle rhythm now have separate native voices. Aquatic’s small-percussion pattern separates kick, frame jingles and claves. Island separates skin drums from wood sounds. Mines separates the muted and ringing metallic ticks and woodblocks from its congas and bongos. Funky separates small electronic clicks and cuica from its kit.

World Suite’s menu selector is part of instrument identity. The Latin menu’s saved selections are congas 7, bongos 3, cabasa 4, claves 6, cuica 9 and frame jingles 12. Selection 12 is the program’s Pandiero option, adopted as a frame-and-jingle proxy for the MIDI tambourine role. It is not a claim that pandeiro is the historical source instrument. The woodblock and metallic-tick models are likewise explicit reconstructions whose source likeness remains revisable.

### Controller movement is part of the phrase

Mines’ upper-string MIDI contains a sixteen-semitone bend range. A native test confirmed a corresponding wide excursion, approximately 259 Hz through 658 Hz to 103 Hz in the held-note probe. Flattening this to a default two-semitone gesture would change the musical identity of the backing.

Aquatic’s intro and smaller voices retain their bend lanes. Two background voices also contain varying modulation values. The final correction interprets those values as a restrained 5.2 Hz vibrato, added to the existing bend movement at an eighty-point-per-second control resolution. Its maximum added depth follows the original controller value and is roughly eleven cents for the source’s largest value. That is an adopted General MIDI-like interpretation, not a measured reconstruction of the game’s exact synthesis algorithm.

Held expression is applied as a continuous part-volume curve. Attack velocity, phrase length and note release remain separate decisions. The implementation does not claim that forwarding a controller automatically gives an instrument a pressure, breath or sample articulation that it lacks.

## Revision sequence

Each numbered pass is a complete song render. Native loading failures, silent probes and repeated exports are excluded from the musical revision count. The sequence retains eleven passes for each cue, followed by a targeted twelfth for Aquatic and Funky and a thirteenth Funky counterfactual. The actual register checks every file and hash before this report is published.

| Pass | Musical purpose | Disposition |
|---|---|---|
| 1 | Initial native source reconstruction | Rejected source diagnostic; percussion and register problems retained as evidence. |
| 2 | Reduce redundant layers and shape the register balance | Rejected source diagnostic; balance improvement did not repair the instrument faults. |
| 3 | Correct instrument registers, separate percussion families, restore critical bends and introduce the physical guitar candidate | Source-led construction baseline; exact sampled identity remains a listening question. |
| 4 | Restore continuous expression and add restrained shared early reflections | Source-expression comparison before the expressive take. |
| 5 | Shape velocities, releases, bass damping and selected subdivision timing | First complete performance treatment. |
| 6 | Establish cue-specific balances and separately balance Fear Factory’s kick, snare, hats and metal/tom voices | Stronger hierarchy without replacing the electronic engine. |
| 7 | Author independent piano/guitar placement, breath-shaped bottle phrases, hand-drum accents and rounded synth onset | Performance interpretation with original note contours retained. |
| 8 | Yield to the source’s reed, brass, flute or bass entrance and distinguish later sections | Handoffs follow source activity and named section boundaries. |
| 9 | Test stronger lilt, natural-flute replacements, son countercells, chromatic bass approaches and acoustic answers | Deliberately more adventurous alternative, retained rather than automatically selected. |
| 10 | Restore source-family leads and reduce unnecessary percussion/texture | Preferred restrained direction; Nordic upright enters Simian’s comparison. |
| 11 | Refine foreground width, percussion placement and bright synthetic edges for a stable center | Selected for Simian, Island, Fear and Mines. |
| 12 | Repair Aquatic’s small modulation lanes and refine Funky’s native pick, damping and simultaneous chord attacks | Selected for Aquatic and Funky after the targeted checks. |
| 13 | Substitute register-correct FM guitar voices into Funky’s same written performance | Retained keyboard-like alternative; the selected physical model remains the working guitar-family interpretation. |

The strongest-lilt version is an arrangement alternative, not a clean one-variable perceptual experiment: it also changes some instrumentation and supporting activity. The isolated native stems allow those choices to be compared separately.

## Simian Segue

### Source identity and tone

The source’s friendly travel refrain depends on short piano sentences, a buoyant upright-like bass, clipped string pulses and a reed-like response. Dry articulation and a clear reply matter more than a large room or a continuous new drum pattern. Echo channels are consolidated rather than cast as additional musicians.

The selected piano is World Suite Nordic Upright, with TDR Mellow Dark retained in the preceding source and performance prints. Both are upright-family candidates. Nordic is the working choice for a direct, animated piano character; the softer TDR remains useful for a gentler reprise. This is an artistic preference awaiting the complete A/B listening check, not a claim of proven superiority.

### Cast and performance

The keyboard chair owns the piano, with the bass chair on Jazzistic Double Bass. The producer retains the pizzicato and reed-like synthetic colors. Auxiliary percussion supplies the cabasa and frame-jingle parts; the small kit contribution follows the source rather than acquiring an invented snare groove.

The melody’s offbeats use a restrained 52 percent placement while the pizzicato and selected small percussion use 54 percent. Bass stays tied to the principal pulse, with shorter endings and a consistent small placement difference. The piano’s higher voice receives slightly more emphasis than support. No octave is changed to suit a library.

During the source reed’s active phrases, the secondary piano and pizzicato yield. The piano hook remains the reference for the return. Separate native tracks preserve the different piano source roles; they do not imply three pianists playing continuously.

### Alternative and next decision

The ninth take tests 56 percent accompaniment and sparse chromatic bass approaches into written arrivals. The destination note is retained and the preceding note is shortened where necessary. I prefer the simpler low contour for the working version: it leaves the familiar refrain and reed exchange easier to follow. The approach-note take has value for a later reprise or transition, where a small harmonic wink can be foreground material.

The most useful next comparison is Nordic against TDR at matched level, followed by 54 against 56 percent accompaniment with the melodic performance held constant. A piano that becomes electric-piano-like or loses the short source attack should be replaced regardless of the preferred performer reference.

## DK Island Swing

### Source identity and form

Percussion establishes the place before the main pipe-like hook arrives. The selected scaffold begins its bass around 27.43 seconds, develops the pitched backing, brings the main pipe theme around 59.71 seconds, changes to the slower passage around 84.57 seconds, features the natural-flute contrast around 91.13 seconds and gives the later low mallet a more important pulse role around 108.57 seconds. These are study/MIDI positions, not asserted timestamps of an identical YouTube edit.

The source comparison’s weak later-section fit is preserved as a limitation. Its global diagnostic time scale is not applied to the music. The study adopts the scaffold’s condensed unfolding and internal tempo change; an exact game-form transcription remains a separate comparison if a future runtime edit needs it.

### Cast and performance

The Afro-Caribbean chair supplies contrasting conga and bongo source roles, with explicit layering where simultaneous parts exceed a single setup. The auxiliary chair owns the wood and clave colors. Corrected Cuba Bass supplies the low anchor. The main pipe remains an original bottle-family synth; the existing contrasting flute uses the actual Djafe program. Keys, synthetic strings and brass retain their source functions.

The hand-drum accents distinguish a structural first beat from smaller offbeat movement. The pipe has grouped dynamic direction and small releases at phrase ends. The foundation stays largely straight. The later sustained passage reduces hand-drum density in the balance, and the low mallet gains responsibility when it becomes the source’s principal low/pulsed voice.

### Alternative and next decision

The alternate tests a natural-flute main hook and a two–three son wood cell. It offers a credible more openly Latin band direction, useful for an original jungle cue. My working preference keeps the bottle-like attack and the existing percussion conversation: they preserve the source’s unusual pipe identity and leave its contrasting flute with a reason to enter. The clave alternative should be retained as a specific rhythmic proposal, not turned into a universal jungle preset.

The first listening priorities are the main pipe’s attack, the clarity of the low hand drum against bass, and whether the slower passage feels like a deliberate opening of space.

## Aquatic Ambiance

### Source identity and tone

The evolving synthetic environment is essential to this track. The melody is a rounded electronic voice inside that environment, rather than a natural instrument waiting to be substituted. The source intro, held harmonic movement, low anchor, smaller plucked figures and answers form different depths.

### Cast and performance

The producer leads the synthetic field, melody and bass. Native Warmth derivatives and the original rounded lead are separately shaped. Harp-like and wood-like responses remain small, and the source kick, frame-jingle and clave events stay behind the long phrase. A human drummer or wind player is not forced to own the foreground because those chairs exist in the roster.

The seventh pass gives the principal synth a softer onset and more sustained body. The handoff pass reduces support during the melody’s actual activity. Small expression movements, the source bends and the final controller reconstruction supply animation without swinging the ambient line. Reflections are slightly more generous here than in the dry groove cues, while the bass and core remain centered.

### Alternative and next decision

The natural-flute alternate is valuable for a future lagoon, pastoral or more intimate original scene. I prefer the rounded synthetic lead for this DKC interpretation because it belongs to the same changing environment as the intro. The flute moves the cue toward an acoustic scene and can make the electronic field feel like accompaniment to a soloist.

The next listening check should compare the corrected small modulation against the preceding version, particularly behind the melody. It should add subtle movement without drawing attention as a new vibrato effect. The melody must remain recognizable in mono and at quiet playback level.

## Fear Factory

### Source identity and tone

The track’s identity depends on a firm electronic engine, a synthetic low line, a cutting electronic theme and sharply placed supporting figures. An acoustic bass, generic guitar lead or loose swing treatment would change the premise. Correct electronic instrument selection takes priority over making every roster member play.

### Cast and performance

The producer owns the R78 electronic kit, synth bass and principal synthetic voices. The kit’s kick, snare, hats and metal/tom material are printed separately for performance balance, with their original rhythm retained. Held strings, short figures, plucked responses and brass punctuation each have their own role.

The principal pulse remains firm. Smaller notes can be lighter and shorter, but there is no blanket swing. The brass arrival receives space from the short supporting figure; the machine theme yields slightly without losing the foreground. The brightest synthetic edges receive a restrained final rolloff, while the source’s electronic character remains intact.

### Alternative and next decision

The ninth take adds quiet acoustic rim/snare/tom answers around the electronic pattern. That is a useful hybrid route for an encounter or more celebratory arrangement. I prefer the electronic-led working take for this cue: the added answers consume space already occupied by the original short figures. The acoustic drummer’s meaningful rest is an arranging choice.

The next comparison should test whether the repaired hats propel the engine without becoming the focus, and whether bass and theme remain distinct on a small speaker. The R78 is a selected electronic-family candidate, not an assertion about the game’s historical drum machine.

## Life in the Mines

### Source identity and tone

The new Mines study is reflective and spacious. Its bottle-like melody, held strings, wide upper-string movement, later picked/plucked electric-bass function and finely divided small percussion create the environment. The metallic and wooden subdivisions must remain distinct from skin drums.

### Cast and performance

The producer plays the bottle-family reconstruction and synthetic strings. Wind phrasing informs the sentence and breath gaps, while the selected sound remains synthetic. The bass chair uses the corrected Cuba Bass in the source register. Low D requires an explicit drop-D conceptual setup; the native low-note test establishes the resulting pitch, not the original sample player’s physical fingering.

Congas and bongos retain separate source roles. The auxiliary wood and mounted metallic parts are declared layers where a single two-hand performance would be implausible. The bottle phrase has grouped dynamic direction and a small gap at its final note. Once bass enters around 56.67 seconds, the low string bed withdraws so the bass attack can define the floor.

### Alternative and next decision

The natural-flute duet offers a more pastoral and openly human color. I prefer the bottle-like working interpretation because its compact, slightly unusual core preserves the mine’s distance and mystery. The flute version has value for an original outdoor or discovery cue. It should remain a deliberate recasting rather than an assumed realism upgrade.

The most important listening questions are the metallic tick’s brightness, the separation of low strings and bass, and whether the wide string movement feels expressive rather than exposed as a technical glide. The explicit metallic and wood models are working timbre choices that can be replaced when a closer source match is heard.

## Funky’s Fugue

### Source identity and tone

The new Funky study preserves separate clean and muted guitar functions, a memorable electric-bass figure, compact drums and short accents. Its selected MIDI is titled Funky’s Flights; the alias is retained in the source record. The clean/muted contrast matters more than dressing the cue in an unrelated acoustic-guitar palette.

### Cast and performance

Strings A owns the cleaner melodic figure and strings B the muted interlock. Electric guitar is an explicit source-directed capability extension, realized here with original Falcon physical-string models. These are synthetic guitar-family candidates, not recordings of acoustic or electric guitarists. The bass and drum chairs anchor the pocket. Small electronic clicks and cuica retain their own identities.

The clean line uses a lighter 52 percent offbeat placement while the muted interlock uses 54 percent. The bass remains near the principal pulse. Higher muted notes have shorter endings. The twelfth pass spreads coincident written chord attacks by three milliseconds per note and revises the excitation, onset and active damping. This reduces the mismatch between a sharp attack and a weak body instead of treating loudness as the musical goal.

The source applause function is covered by an authored layered clap gesture at its source positions, using the native sampled-clap voice. It is not the original crowd sample. The gesture is quieter in the selected arrangement than in the exploratory take.

### Alternative and next decision

The more active ninth take combines stronger accompaniment lilt with a son countercell. It has value for a dance or credits arrangement, but I prefer the tighter original guitar/bass exchange for the working cue. The additional pattern competes with an already recognizable interlock.

The thirteenth take changes only the guitar model within the written performance to a register-correct FM interpretation. Its keyboard-like clarity is useful for an explicitly synthetic reprise. The physical model remains the working source-family choice. This distinction is provisional: guitar realism and the clean/muted contrast require the strongest ear-based review of the six studies.

## Performance and session organization

The selected versions have one principal low role at a time. Bass is centered, foreground width is restrained and support moves around that center. Expression and the shared early-reflection bus are preserved separately from the instrument prints. Shorter note releases are written into the performance before the final static level adjustment.

The owner review collection retains complete lossless mixes, listening copies, the source-corrected baseline, alternate full takes, printed stems and native editable part projects. The original MIDI scaffolds and event maps retain source indices, pitches and declared additions. Native preset state, proprietary sample libraries and original YouTube reference audio are not published with the public project metadata.

A guitar change or simultaneously active percussion setup is represented by separate players or declared studio takes. The files do not imply a one-take stage performance by an impossible number of hands. A quiet stick or brush sample is not described as a continuous brush sweep; no unsupported half-pedal, legato or round-robin mechanism is claimed.

## Listening priorities and remaining production

The next listening pass should first compare the source-corrected baseline with each selected performance at matched level, then inspect the contrasting section and return. Instrument family, source register, hook contour and rhythm identity come before attractiveness of the mix. The preferred arrangement can change when a closer source likeness or a clearer phrase is heard.

The highest-value open decisions are the physical guitar realism; Nordic versus TDR piano touch; frame jingles versus an exact tambourine source; metallic/wood percussion body; and bottle-model attack versus the game’s actual pipe sound. Each has an adopted working choice and a concrete alternative or replacement trigger. These are focused revision questions, not reasons to leave the arrangement unfinished.

After musical selection, original Roshan cues can apply the demonstrated method: a recognizable hook, an instrument-specific performance, a changing section role, a return and a purposeful ending. The remaining twenty-four DKC profile rows retain their individual source/cast briefs. They have not become completed arrangements through this six-track pass.

These full studies do not replace runtime music. Runtime loop edits, two-wrap listening, voice/ducking balance, music-off behavior, target-device playback, child and owner acceptance retain their existing gates. Machine signal, loudness and provenance checks do not close MA-AUDIO-001.

## Critical decisions for the next production cycle

The strongest general decision is to protect the source’s unusual voices. A synthetic bottle, a machine bass or a particular metallic tick can be more expressive than a generic acoustic replacement. The cast should expand its capabilities around that identity.

The second decision is to make timing relational. A steady bass can support a lightly delayed muted guitar; an ambient melody may need evolving sustain rather than swing. Assign the pulse, the subdivision and the answer before introducing irregularity.

The third is to use subtraction as a performed event. Lowering the low strings when the bass arrives, yielding beneath a reed answer and allowing the acoustic drummer to rest give the arrangement a clearer argument. Adding another competent musician is not automatically an improvement.

The fourth is to preserve counterfactuals. The flute, stronger son-oriented groove, chromatic approach and FM guitar takes suggest valuable future scenes even when source identity makes them lower-priority choices here. Their notes, timings and native sources remain available, so later decisions can be revised from actual music.

Finally, instrument verification must reach the sounding result. Correct note numbers did not prevent octave-low synths; enabled MIDI messages did not guarantee modulation; a saved kit name did not guarantee active hats; and a parameter labeled brightness did not guarantee that the selected damping mode used it. Future production should carry these short native register, articulation, controller and same-pitch dynamic checks into the first source pass.

## Measured delivery and editability

The six selected mixes decode as finite 48 kHz stereo audio with zero clipped samples. Their independently measured integrated loudness is DKC-02 -20.00 LUFS, DKC-03 -20.01 LUFS, DKC-07 -20.00 LUFS, DKC-19 -20.00 LUFS, DKC-11 -20.00 LUFS, DKC-15 -20.87 LUFS. All measured true peaks remain at or below −2.2 dBTP after rounding. The 80 individual MIDI parts and 80 instrumental prints retain the selected performance; six additional buses hold the shared reflections.

All six full-band projects reloaded and rendered in the isolated native REAPER profile. Their lengths match the selected masters exactly. The largest RMS difference is below −132 dBFS, with maximum sample differences around one millionth of full scale. This establishes native session recall at the printed-mix level, not subjective musical acceptance. The [native recall receipt](native_mix_recall_v1.json) records the exact results.

The comparison reels contain our corrected source reconstruction, the selected performance and the adventurous alternate, in that order for two sections. They use a common nominal whole-song loudness reference and contain no original game recording. The original YouTube references remain in the production receipt for direct source listening.

## Authority and evidence

Owner commission: [production direction](production_owner_direction_20261103.json). Scope and gates: [audit impact](../../audit_impacts/dkc-six-track-production-20261103.json). Current musical construction authority: [performer workflow](../performers/README.md), [profile registry](../performers/registry.json), and the thirty-cue guide linked above.

The native-control interpretations also use UVI’s primary [pitch-bend range guidance](https://support.uvi.net/hc/en-us/articles/360000044698-UVI-Soundware-Changing-the-Pitch-Bend-Range) and [Falcon oscillator documentation](https://manual.uvi.net/falcon/en/oscillators/). The private render measurements distinguish what the tested states actually did from what a manufacturer control can potentially do.
