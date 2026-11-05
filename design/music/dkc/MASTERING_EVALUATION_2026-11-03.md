# DKC six track mastering and evaluation

The six constructed DKC performances now have a separate production and mastering revision. The work follows the owner’s request for properly layered production, clarity, soundstage and polish, with five to ten comprehensive evaluation audits before approval. Eight rounds were chosen. The construction mixes, their performances and their earlier alternatives remain preserved.

The technical portions of the eight rounds are recorded separately from listening. No new-candidate audio was sent to Gemini: the earlier transfer-permission question remains unanswered after automatic approval review rejected that upload. These files are mastering candidates for listening review. No subjective sound-quality grade or owner approval is claimed.

## Inputs and boundaries

The input is the six-track construction revision at commit d2d7d4f79d3057c1def36fd07cd8ed92f183248b. It contains Simian Segue, DK Island Swing, Aquatic Ambiance, Fear Factory, Life in the Mines and Funky’s Fugue. The [construction report](SIX_TRACK_PRODUCTION_2026-11-03.md) and [performed call sheets](production_call_sheets_v3.json) retain the instruments, exact profiles, note/controller provenance and native sessions. All six construction-master hashes and all eighty instrumental input-stem hashes were checked before mastering.

Mastering preserves the original note and tempo performances. It changes balance, selected frequency regions, player position, shared depth and bounded dynamics. Original in-game instrument identity still has priority. The bottle, frame-jingle, wood/metal and physically modelled guitar choices remain working source interpretations; mastering does not settle their fidelity by itself. A source mismatch returns to instrument selection and performance.

The [audit plan](mastering_audit_plan_v1.json) defines the same criteria for every round: source integrity; layer hierarchy; clarity and tone; soundstage and mono; dynamics and headroom; form and tails; translation; delivery; and listening/approval status. A round can complete its technical tests while its listening criteria remain pending. Eight rounds do not mean eight independent listeners or eight completed ear-based judgments.

## Eight evaluation rounds

| Round | Primary investigation | Production action and evaluation |
|---|---|---|
| 1 | Source lock and baseline | Validate the six masters and eighty stems. Measure full-song loudness, true peak, range, crest, DC, stereo correlation, mono retention and low-side energy. Inspect sampled spectral balance and coactive stem powers. |
| 2 | Layer hierarchy | Make small cue-specific balance changes. Preserve foreground identity and purposeful rests; reduce selected support or bass weight by fractions of a decibel. Recheck all shared criteria. |
| 3 | Conditional clarity | Apply modest cuts only to named support voices, often while the source foreground or bass is active. Preserve instrument body and the source register. Recheck level, peak, stereo and duration. |
| 4 | Position and depth | Give the principal players coherent positions, center the low field and rebuild the short shared reflections with different front/back sends. Recheck mono and section contrast. |
| 5 | Bounded dynamics | Apply slow, gentle musical control around the stronger active passages, with a cue-specific cap. Preserve the large source contrasts in Island and Aquatic. Measure the actual gain reduction. |
| 6 | Coherence and true peak | Set a common quiet review-level target and use oversampled, look-ahead gain control where peaks require it. Preserve dynamics rather than pursuing maximum loudness. Recheck complete files. |
| 7 | Translation and codecs | Produce mono, quiet and band-limited diagnostic copies; decode MP3 and Ogg listening versions. Supply level-controlled construction/master comparisons for two sections of each song. Revisit all criteria and retain listening gaps. |
| 8 | Native recall and delivery | Reload and render all six editable mastering mixes in native REAPER. Compare their output with the selected masters, check lengths and payload hashes, and verify private archive integrity. Keep final listening and approval open. |

Rounds two through six produce thirty complete processing-stage prints. A print may be unchanged when the next audit finds no need for additional processing; it is then not counted as a new musical revision. Rounds seven and eight evaluate the selected result and its delivery.

## What the baseline established

The construction mixes already retained their center well in mono. Their measured mono power losses ranged from approximately 0.005 to 0.28 dB. There was no numerical basis for a broad stereo repair across the score. The stage work therefore concentrates on coherent player positions, low-field stability and the relationship between direct sound and the short shared reflections.

Island and Mines had more low-frequency side energy than the other cues. Their initial low-side-to-mid ratios were approximately minus 15.6 and minus 16.6 dB below 120 Hz. Centering the lower field improved those ratios by roughly nine and eleven decibels in the spatial pass. Their upper instrumental width remains available.

Funky was the main headroom exception. Its construction version measured minus 20.87 LUFS with a minus 2.20 dBTP maximum. Constraining peaks through static gain alone made the early mastering pass substantially quieter. This justifies a bounded peak-control comparison, while retaining the guitar/bass interlock and the stronger attacks.

The sampled spectral profiles differ substantially between cues. Aquatic and Funky carry considerable low-frequency energy; Fear’s electronic voices concentrate more energy in the low mids; Mines’ bottle and strings occupy much of the middle register. Those differences follow orchestration and are not instructions to make every spectrum flat.

The initial layering diagnostic also required correction. Comparing foreground with a backing part during that backing’s intentional rests produced misleadingly large ratios. The revised diagnostic compares only windows where both are active and records how much coactive material exists. In Funky, sustained harmony is rare; its two guitar figures are both foreground roles. A numerical foreground/support ratio cannot replace listening to their interlock.

## Production decisions by track

### Simian Segue

The piano, upright bass and reed-like response remain the center. Small balance changes reduce secondary piano weight and leave the clipped pulses legible. The support-piano adjustment around 300 Hz is only half a decibel. It aims to preserve the original piano sentence and the bass’s independent contour.

The piano’s written left and right roles receive a coherent, relatively narrow image, while the reed answer has a modest separate position. The principal hook remains stable. Short reflections are reduced on the foreground relative to the backing. The dynamics cap is three quarters of a decibel; the piano’s attack and the bass’s releases remain important listening checks.

Listen for whether the reed exchange remains effortless, whether the bass still bounces, and whether the piano’s short high notes retain their acoustic character. The Nordic/TDR instrument comparison belongs to the preserved construction alternatives.

### DK Island Swing

The hand-percussion introduction, staged instrumental arrivals and slower contrasting passage retain their source timeline. The production moves are small: slightly less bass and string weight, a restrained adjustment to the low drum, and continued responsibility for the later low mallet.

The low mallet is treated as a center anchor when it takes over that role. Conga and bongo positions are distinct. Supporting strings yield slightly around the pipe/flute foreground. The lower stereo field is stabilized, while upper atmosphere remains. Its large loudness range is preserved as an arranging feature.

Listen through the percussion opening, full hook and later passage consecutively. The transition should feel intentional, and the hand drums should remain individual voices. The tonal identity of the bottle-like main pipe remains a source-listening question.

### Aquatic Ambiance

The synthetic field, rounded melody and moving background voices stay intact. A small reduction in bass weight and a conditional dip in selected low support create space without changing the electronic palette. The modulation repair from construction remains part of the source performance.

The foreground has a firmer center and a lower short-reflection send than the background. The wider field still supplies depth. Dynamic control is limited to four tenths of a decibel; long phrases and the large intro-to-theme contrast are preserved.

Listen for whether bass supports the depth without obscuring the melodic core, and whether the moving field stays gentle. Neither a darker spectrum nor a larger image automatically establishes a better aquatic atmosphere.

### Fear Factory

The electronic engine remains firm. Small reductions in the short ostinato, held strings and running support clarify their hierarchy. The supporting low-mid cut is conditional on the foreground; the main bass and machine theme retain their identity.

The bass and kit occupy the center. Supporting replies receive defined positions and a modest depth relationship. The dynamics cap is six tenths of a decibel. No swing or additional acoustic drum overlay enters this mastering revision.

Listen for distinct bass, theme and hat pulse, then inspect the brass arrivals. The objective is a readable machine-like arrangement with controlled edges, not a generic warm acoustic mix.

### Life in the Mines

The bottle-like lead, wide string motion and later electric-bass entry remain. Low strings and upper support receive small balance adjustments. A restrained conditional cut around 170 Hz gives bass more room; an upper-support cut around 700 Hz follows foreground activity.

The low field is centered more firmly while the sustained upper space remains. The dynamic cap is six tenths of a decibel. Metallic and wooden subdivisions remain separate from the skin drums; they are not replaced with a single percussion texture.

Listen for a stable floor beneath the drifting strings, a complete bottle sentence and a metallic tick that supplies detail without becoming tiring. The working wood/metal timbres still need source-based ear review.

### Funky’s Fugue

The cleaner guitar figure and muted interlock retain separate roles. A small reduction in muted-guitar and bass weight is paired with a conditional adjustment around 240 Hz in the muted figure. The guitar parts receive different positions while the bass and compact kit remain centered.

This cue receives the largest dynamics allowance, capped at one and a half decibels for the musical-control stage. The later peak controller addresses the remaining transient/headroom problem. Actual reduction amount and duration are recorded; no extra compression is justified solely by a desire to match a louder file.

Listen for unchanged rhythmic character, distinct clean/muted attacks and enough body after each pick. Guitar realism is still the strongest upstream listening question. The construction’s register-correct FM version remains an available counterfactual.

## Processing limits and reproducibility

Balance changes are small and named. The clarity cuts range from half a decibel to about 1.1 dB and are applied to specific support voices. The spatial stage uses a high-pass on side information at 140 Hz, retains a centered principal bass, and uses source-derived short reflection timings with different sends by role.

The musical dynamics stage works around stronger active passages with a soft knee, a twelve-millisecond attack and a 160-millisecond release. Its caps vary by cue. The final peak controller analyzes four-times-oversampled audio and uses four milliseconds of look-ahead with a slower recovery. Its actual behavior is measured on the exported files.

The review target is about minus 20 LUFS with a conservative ceiling below minus 3 dBTP. These are full-song private review masters. They do not satisfy the separate integer-bar runtime loop contract merely by meeting a level target. Ogg previews are listening/translation copies, not runtime replacements.

The selected mastering stems include the shared gain behavior, so the native printed-mix projects can reproduce the mastering result while keeping the instruments separate. The construction MIDI and original native instrument projects remain the performance-editing source. The private recipe archive records the exact processing and input references.

## Listening and approval

The complete listening evaluation must compare construction and mastering at a common level, then hear each entire song through its opening, contrasts and ending. Check timbre, melodic priority, bass weight, transient quality, stereo depth, mono character, fatigue and the return. A quieter or louder file is not an improvement grade.

Mono, quiet and band-limited files are useful review aids. They do not prove phone, Lenovo Tab M11, headphone, speaker, child or voice-over acceptance. Protected family recordings were not used or altered. The runtime voice, ducking, music-off, loop and device gates remain separate.

The technical audit records preserve every listening criterion as pending. Automatic approval review rejected the prior new-audio transfer to Gemini because explicit transfer authorization was missing, and that permission question remains unanswered. No upload or invented model-listening score is included here. Owner musical approval remains open.

## Measured results

| Track | Integrated LUFS | True peak dBTP | Loudness range LU |
|---|---:|---:|---:|
| Simian Segue | -20.00 | -4.01 | 4.0 |
| DK Island Swing | -20.00 | -3.43 | 17.8 |
| Aquatic Ambiance | -20.00 | -3.94 | 15.4 |
| Fear Factory | -20.00 | -6.17 | 3.5 |
| Life in the Mines | -20.00 | -4.92 | 12.3 |
| Funky's Fugue | -20.04 | -3.15 | 3.2 |

The thirty processing-stage prints contain twenty-five distinct audio hashes. The five unchanged round-six prints retain the round-five result because further peak reduction was unnecessary. Funky’s final peak controller reaches a maximum 1.75 dB reduction, exceeding 1 dB for about 0.19 percent of its duration. The other five receive no extra peak reduction.

All twelve MP3/Ogg listening copies were measured after encoding. Funky’s Ogg needed an additional 0.18 dB level trim to retain the listening-copy peak ceiling; the earlier encoding is preserved as a trial. Every final listening copy decodes finitely and measures no higher than minus 3 dBTP.

All six native mastering projects reload and reproduce the selected lossless masters with exact sample lengths. Their RMS differences are below minus 138 dBFS. The original six construction masters and eighty input stems retain their exact hashes. These results establish recall and signal integrity, while the listening and approval criteria remain pending.

## Authority and records

The owner’s [mastering direction](mastering_owner_direction_20261103.json), [eight-round plan](mastering_audit_plan_v1.json), [audit results](mastering_audits_v1.json), [delivery receipt](mastering_receipt_v1.json) and [impact record](../../audit_impacts/dkc-six-track-mastering-20261103.json) identify the scope and evidence. Original in-game instrumentation retains priority; DL-AUTH-05 through DL-AUTH-07 and the existing sound-delivery, performer and listening rules continue to apply. MA-AUDIO-001 remains unchanged.
