# Soundtrack performer profiles and construction workflow

The collective has ten core creative members and five guest families. Each has a detailed profile of musical knowledge, techniques, stylistic references, phrasing, collaboration, physical limits and instrument realization. The [master audit logs every performer individually](../../../audit/MASTER_AUDIT_2026-08-09.md#soundtrack-performer-logs); the [registry](registry.json) records profile revisions and hashes. Profile text hashes normalize CRLF to LF for portable UTF-8 identity; audio and native-state hashes remain byte-exact.

**Bonobo is the owner-selected single primary producer identity.** The other producer references support particular pop, dance, lo-fi or chip techniques. They do not constitute competing primary identities. Original DKC1 remains the reference for the score's variety, atmosphere, location identity and memorable returns.

The profiles describe a fictional creative collective. The historical artists are reference points, not participants. Documented artist practices, proposed performer abilities, catalogue possibilities, native test coverage and human musical acceptance remain distinct.

## Performer index

| Performer | Historical starting point | Profile |
|---|---|---|
| Fretted-strings collaborator A | Ernest Ranglin | [strings_a, revision 1](strings_a.md) |
| Fretted-strings collaborator B | Leo Nocentelli with The Meters | [strings_b, revision 1](strings_b.md) |
| Keyboard collaborator | Monty Alexander | [keys, revision 1](keys.md) |
| Low-strings collaborator | George Porter Jr. | [bass, revision 1](bass.md) |
| Acoustic-drum and groove collaborator | Joseph Zigaboo Modeliste | [acoustic_drums, revision 1](acoustic_drums.md) |
| Afro-Caribbean percussion collaborator | Mongo Santamaria | [afro_caribbean_percussion, revision 1](afro_caribbean_percussion.md) |
| Traditional/world percussion collaborator | Zakir Hussain | [traditional_percussion, revision 1](traditional_percussion.md) |
| Wind collaborator | Herbie Mann | [winds, revision 1](winds.md) |
| Pitched-percussion collaborator | Andy Narell | [pitched_percussion, revision 1](pitched_percussion.md) |
| Electronic-production collaborator | Bonobo / Simon Green | [producer, revision 2](producer.md) |
| Harp-lute and plucked-string guest | Toumani Diabate | [kora, revision 1](kora.md) |
| Harp-family guest | Alan Stivell | [harp, revision 1](harp.md) |
| Bowed-string guest | Stephane Grappelli | [fiddle, revision 1](fiddle.md) |
| Reed-family guest | Djivan Gasparyan | [duduk, revision 1](duduk.md) |
| Additional Latin-percussion guest | Willie Bobo | [aux_percussion, revision 1](aux_percussion.md) |

## Use a profile to make a musical decision

Begin with the scene and approved hook. Select the people who can develop that idea; a ten-person core does not require ten simultaneous parts. Consult each selected profile's technique, range, knowledge and physical limits. Invite melodic, harmonic and arranging contributions from every chair, then give each section a clear foreground and groove leader.

Use an instrument because of the musical role it can fulfill. A catalogue name does not establish the installed program's range or articulation behavior. Record the actual preset, selected layer, MIDI map, relevant controls and audition evidence. A program can have a legacy display name: the Sky Valiha test uses **Valiha D1, selector 3**, inside a program named Kora 1. Preserve both facts.

Reference studies answer specific questions. A guitar study may guide chord placement; a tabla study may guide stroke conversation; a Bonobo study may guide an entrance, subtraction or bass relationship. State the adapted principle without copying a recording's melody or samples. Preserve approved themes and declare proposed changes before construction.

## Song call sheet

The [revised cue plans](../CUE_PLANS_2026-11-01.json) implement this format. Each selected performer needs:

| Field | Construction decision |
|---|---|
| Identity | Profile ID, revision and SHA-256; cue/plan revision and review state. |
| Source | Exact UVI bank/program and active articulation, or the scoped RetroPlug/LSDJ lane; native audition ID and its limited coverage. |
| Musical purpose | Hook, harmony, bass, groove, response or texture; why this person/instrument serves the scene. |
| Reference | Named recording or primary technique source and the specific principle being adapted. |
| Performance | Range/register, strokes/articulations, phrase boundaries, dynamics, releases, breathing or sticking and instrument-specific limits. |
| Form | For every section: lead and groove leader, each player's role, entrance, exit, handoff and meaningful rest. |
| Physical model | Single performance, feasible simultaneous gestures, instrument-change time, separate player or declared studio overdub. |
| Tone | Source/touch first, then EQ and balance purpose, stereo/mono behavior, shared space and foreground protection. |
| Review | Exact recall/render evidence and questions for dry sound, musical phrasing, full-mix clarity and acceptance. |

Short diagnostic or unchanged study excerpts can investigate a source without constructing a new full song. They do not supply a completed performance or a completed arrangement. Further expressive tests are needed where an audition used one velocity, a narrow range or only two kit notes.

## Construct and review a song

1. Read the mission, relevant profiles, current audit/rules and accepted melody version. Name the emotional purpose and recognizable hook.
2. Plan a complete form with distinct verse/refrain or other purposeful sections. Allocate harmonic movement, rhythmic development and foreground handoffs before adding notes.
3. Fill the performer call sheets and section roles. Choose one groove leader; other percussionists can answer, simplify or rest. Write physical constraints and overdubs honestly.
4. Validate the plan with `python -B tools/audit_music_performer_plans.py`. Before full construction, its `--for-construction` mode honors any explicit owner-review requirement. All three current plans require that review and remain drafts.
5. Construct editable parts through the established REAPER/Falcon/Lua workflow, retaining exact source programs, articulation events, MIDI and automation. Keep dry, edited and processed band material identifiable.
6. Check the hook without decorative tracks. Review each entrance, withdrawal and return, then shape phrasing and dynamics. A random humanize control does not author a performance.
7. Balance and EQ the actual arrangement. Preserve useful instrument body and headroom, control pan transients, and check mono and speech space before mastering. Source comparisons are not final masters.
8. Review complete songs and any separately authored runtime edits. Preserve provenance and distinguish machine checks, AI advice, human listening, device/child acceptance and release authority.

## Current evidence and pending decisions

The [audition receipt](../INSTRUMENT_AUDITIONS_2026-11-01.json) covers 28 native Falcon/REAPER instrument/configuration tests, including five lo-fi/electronic kits and five world-percussion choices. These are short diagnostics and existing-material excerpts. The five reels and individual audio files remain in the private owner-review workspace; factory sample/preset states are not redistributed.

Percussion Factory is owner-reported added. Its documented legacy engine supports separate sound and sequence triggers and part-level editing, but the exact installed edition and chosen programs still require native audition. The current plans use sources already rendered in this pass; Percussion Factory can replace a named role after that comparison, rather than add an automatic eight-part layer.

General instruments remain UVI soundkits and explicitly requested UVI-powered Sunbird. Sunbird is a steel-string Hummingbird library, despite an older source label calling it nylon. RetroPlug/LSDJ remains the explicit Game Boy/chiptune exception for Ember King.

`DL-SND-18` makes profile use part of new authoring. `DL-AUTH-05`–`07` govern traceability; `DL-SND-04`, `07`, `09`, `12` and `17` retain routing, delivery and acceptance boundaries. Full-song source masters do not silently replace the existing runtime loop contract. `MA-AUDIO-001` remains `FIXED_PENDING_VERIFICATION`; this profile work does not close it.


The subsequent [expanded-palette test commission](../expanded_palette_test_tracks_owner_direction_20261101.json) authorizes private Opera House, Sky Lagoon and Castle test constructions. Use the separately evidenced `--for-construction --test-tracks` check. Final artistic review remains pending; this does not mark unseen arrangements approved or authorize runtime replacement.
