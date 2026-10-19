# Codex work order: learning sessions (2026-10-18)

**From:** Claude (written analysis and specification; no game change, no
image, no voice generation). **To:** Codex (every code change, image, voice
line, PDF and probe). **Owner:** chose the scope on 2026-10-18 and
2026-10-19 (section 1) and approves art, voice and wording.

**Status:** `PROPOSED / CANDIDATE`, revision 2 (the card now follows the
owner's 2026-10-19 book decision). Baseline: `dev`
`e1dc3e21f67afeacf48a3609ac520468d6fecc28`. Book sources: branch
`codex/mermaid-roshan-picture-book` at
`d75164b2c7e5f432a510c13a50b5feb5a3781784`. Encounter source: local branch
`codex/grand-puff-care-20261017` at
`e0abe9c9643e44a85c262683c75b6ac1fb04b5e3`, not on GitHub (see FP0). Review:
[Mermaid Roshan: Learning Value Beyond the Fantasy](https://claude.ai/artifact/JE6GvfXSBgBccHuwpDiLGc).
No finding is repaired or closed. This packet requests no generation:
`ARCHIVE_COMPLETE` only after remote verification, `GENERATION_READY` not
applicable, `DELIVERY_ACCEPTED` false.

| Read | For |
|---|---|
| [QUESTION_CARD.md](QUESTION_CARD.md) | Package QC: the printed card, its full text for all 17 openings of the book, binding and checks |
| [FEELINGS_WITH_PUFF.md](FEELINGS_WITH_PUFF.md) | Package FP: two feelings beats in the Grand Puff care encounter, 21 lines, pointers, the level that steps up and down, probes |
| [QUIET_MEDALS.md](QUIET_MEDALS.md) | Package QM: tiers hidden from her, a surprise keepsake on a game's first finish, 15 praise lines, probes |
| [PARENT_LOG.md](PARENT_LOG.md) | The two-week check sheet for the grown-up |
| [MANIFEST.json](MANIFEST.json) | SHA-256 of every packet file |

## 1. Owner decisions

The review recommended three ideas in order and named the medals as the
main motivation risk. Before anything was written, the owner was asked
three questions. The exact questions, options and answers are in
[owner_replies.json](../../../audit/cycles/learning-sessions-20261018/owner_replies.json),
and the decisions are in the
[decision register](../../../design/reference/OWNER_DECISIONS.md).

| # | Question | Owner's answer | Decision | Meaning for Codex |
|---|---|---|---|---|
| Q1 | Which learning ideas should the Codex work order cover? The doc ranks them 1, 2, 3; pick any. | "Book question card,Feelings with Puff" (2026-10-18) | `ODR-LEARNING-SCOPE-20261018` | Build QC and FP. "Count and Clean" was offered and not chosen, so it is not commissioned. |
| Q2 | Should the work order also soften the medals? That changes your 2026-07-18 medal decision, so it needs your explicit yes. | "Yes, all three" (2026-10-18) | `ODR-MEDALS-QUIET-20261018` | Build QM: surprise medals instead of a banner on every finish, tiers hidden from her, praise lines. Tiers are still computed and saved, upgrade-only. |
| Q3 | Which synthetic voice should speak the new Feelings with Puff lines and the new praise lines? | "Regenerate all lines in new voice, this is not preserved asset." (2026-10-19) | `ODR-GUIDE-VOICE-20261019` | Build VG (section 6): one new narrator voice; regenerate every existing Guide line in it together with the new lines. |

Q3 is read as: "all lines" means every line the Guide narrator speaks, that
is the two 2026-10-14 objective guides on `dev` and Grand Puff's five cold
lines on the care branch. Character voices and protected family recordings
are not included. The register entry records this reading so the owner can
correct it.

## 2. In short

Mermaid Roshan already exercises many preschool skills, almost all at one
fixed level. Nothing in it names feelings, and the medals grade speed with a
banner and chime on every finish. This order adds three small things:

- **QC:** a printed question card for the chapter-one picture book, so
  bedtime reading becomes talk, with no screen.
- **FP:** two short feelings beats in the Grand Puff care encounter, with a
  level that steps up and down with her.
- **QM:** quieter rewards: no tiers on her screen, a surprise keepsake the
  first time she finishes a game, and a narrator line praising what she did.

For two weeks a grown-up notes three things after each session: off-screen
use, whether she chooses it again, and frustration.

## 3. Evidence copied from the review

The review opened every source below and paraphrased its findings. It also
says plainly that nothing was checked by watching her play; every judgment
came from code and design documents.

- **Learning goals:** [Head Start Early Learning Outcomes Framework](https://headstart.gov/interactive-head-start-early-learning-outcomes-framework-ages-birth-five)
  (the review's lens: naming her feelings is a social and emotional goal
  at four to five), with its [preschool literacy](https://headstart.gov/school-readiness/article/literacy-preschool)
  and [preschool math](https://headstart.gov/school-readiness/article/math-preschool) pages.
- **Shared reading (QC):** [What Works Clearinghouse on dialogic reading](https://ies.ed.gov/ncee/WWC/EvidenceSnapshot/135),
  [Mol et al. 2008](https://eric.ed.gov/?id=EJ787378),
  [National Early Literacy Panel summary](https://nichd.nih.gov/publications/pubs/Documents/NELPSummary.pdf).
  Review: talk-based reading has the strongest evidence here and keeps
  bedtime screen-free; question-rich shared reading improves oral language,
  with smaller gains at ages 4 to 5.
- **Feelings and app quality (FP):** [AAP, Digital Ecosystems, Children, and Adolescents (2026)](https://publications.aap.org/pediatrics/article/157/2/e2025075320/206129/Digital-Ecosystems-Children-and-Adolescents-Policy)
  (social skills shown in content count toward app quality);
  [Hirsh-Pasek et al., Putting education in educational apps (2015)](https://www.psychologicalscience.org/publications/educational-apps.html)
  (active, engaged, meaningful and social learning around a clear goal).
- **Rewards (QM):** [Lepper, Greene and Nisbett 1973](https://psycnet.apa.org/doi/10.1037/h0035519)
  (an expected award lowered later free choice; a surprise award did not),
  [Deci, Koestner and Ryan 1999](https://pubmed.ncbi.nlm.nih.gov/10589297/)
  (128 studies: expected, task- and performance-based rewards lower later
  interest; positive feedback raises it),
  [Kamins and Dweck 1999](https://eric.ed.gov/?id=EJ586556) (praise what she
  did, not who she is),
  [Harvard on motivating children](https://developingchild.harvard.edu/resources/briefs/how-to-motivate-children-science-based-approaches-for-parents-caregivers-and-teachers/),
  [ICO Children's Code, standard 5](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/age-appropriate-design-a-code-of-practice-for-online-services/5-detrimental-use-of-data/)
  and [standard 13](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/age-appropriate-design-a-code-of-practice-for-online-services/13-nudge-techniques/),
  [Radesky et al. 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9206186/),
  [UNICEF RITEC](https://www.unicef.org/innocenti/projects/responsible-innovation-technology-children).
  The AAP 2026 statement also names frequent badges and trophies as
  behavioural lures.
- **Screens, people and bedtime:** [WHO guidelines for under-fives (2019)](https://www.who.int/news/item/24-04-2019-to-grow-up-healthy-children-need-to-sit-less-and-play-more),
  [AAP, Media and Young Minds (2016)](https://publications.aap.org/pediatrics/article/138/5/e20162591/60503/Media-and-Young-Minds),
  [Strouse and Samson 2021 meta-analysis](https://red.library.usd.edu/se-fp/3),
  [Education Week summary](https://www.edweek.org/leadership/how-can-video-conferenced-lessons-affect-learning-for-the-youngest-students/2020/10),
  [a mother's recorded voice and word learning](https://research-portal.uu.nl/en/publications/beneficial-effects-of-the-mothers-voice-on-infants-novel-word-lea/).
- **Self-control and retelling:** [Harvard Center on the Developing Child brief](https://developingchild.harvard.edu/resources/inbriefs/inbrief-executive-function/)
  and [activities for 3- to 5-year-olds](https://developingchild.harvard.edu/wp-content/uploads/2024/10/Executive-Function-Activities-for-3-to-5-year-olds.pdf).
- **Not used by this order** (they supported "Count and Clean", which was
  not chosen): [DREME](https://dreme.stanford.edu/publication/making-early-math-education-work-for-all-children),
  [WWC early math practice guide](https://ies.ed.gov/ncee/wwc/PracticeGuide/18),
  [IES subitizing progression](https://ies.ed.gov/ncee/rel/math-young-children/pdf/TMYC_Mod1_Subitizing_Developmental_Progression.pdf).

## 4. Rules and findings

Read at `dev` `e1dc3e21`: the master audit planning entry and task index,
`design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md`, the active findings and
`design/05_DOC_LEDGER.md`.

### Design rules that apply

| Rule | How it applies here |
|---|---|
| `DL-AUTH-05`, `DL-AUTH-06`, `DL-AUTH-07` | Every Codex change cites its rules and findings and carries an impact record; gates are blocking. |
| `DL-AGE-01` | Each new objective (the two feelings choices) has an exact spoken line and a moving pointer. The project's hard rule says the same: a new objective fires a voice line through `_say()` and a visual pointer. The care encounter speaks through `objective_guide()` in `audio_director.gd`; use that or `_say()`, never a caption alone. |
| `DL-AGE-02` | One finger: one tap on a card, no confirm button. |
| `DL-AGE-03` | No fail states: no buzzer, lost round or early end; other faces are named kindly. |
| `DL-AGE-04` | No passive wins: doing nothing never passes a feelings beat; help shows the answer but she taps it; the surprise and the praise come only from win paths. |
| `DL-AGE-05` | Random tapping is never faster than choosing; repeated taps on another face pay nothing. |
| `DL-AGE-06`, `DL-AGE-07`, `DL-AGE-08` | Short beats with clean leave and re-entry; a pressed state within two frames; the angry and scared faces stay mild. |
| `DL-READ-04` | No required words, letters or digits in world art: the face cards and the keepsake carry none. The printed card is adult reading material outside both the game and the book. |
| `DL-READ-05`, `DL-READ-06` | Cards never cover Roshan or Puff; the pointer points at a live card. |
| `DL-INT-01`, `DL-INT-02`, `DL-INT-05`, `DL-INT-06` | Only the cards take touches during a beat; choices are kind and repairable; help never taps for her or completes anything. |
| `DL-UI-03`, `DL-UI-04`, `DL-UI-05`, `DL-UI-06`, `DL-UI-07` | Large Storybook cards; one touch, one route; teardown cancels input; no standing medal tally on the play surface. |
| `DL-MOT-04`, `DL-MOT-05`, `DL-VIS-04` | Glow, sound and voice describe one event; rewards follow her own action; warm colour marks the chosen card and the keepsake. |
| `DL-SND-01`, `DL-SND-02`, `DL-SND-03`, `DL-SND-04`, `DL-SND-05` | Exact cues; captions for the adult; one voice per speaker; music ducks under speech; protected family recordings untouched. |
| `DL-SND-10`, `DL-SND-11`, `DL-SND-12`, `DL-SND-13`, `DL-SND-14`, `DL-SND-15`, `DL-SND-16`, `DL-SND-17` | An audio-ledger row per file; protected hashes unchanged; 48 kHz mono Ogg Vorbis at 64 kbps or more, −16 LUFS-I ±1 LU, peak −1.5 dBTP or lower; key plus pointer within 150 ms; mix levels; human review at 4/5 or better; device timing; the replacement bar (section 6). |
| `DL-SAVE-01`, `DL-SAVE-03`, `DL-SAVE-04`, `DL-CODE-03` | One additive save key; each activity owns and cancels its audio, timers and nodes; the full enter-to-re-enter path is tested. |
| `DL-CODE-05`, `DL-CODE-10`, `DL-QA-02` | One shared pointer and one shared ceremony helper; probe-first with zero-input coverage; probes use real input. |
| `DL-TYPE-07` | Reward meaning moves from emoji to an authored keepsake picture. |
| `DL-ASSET-01`, `DL-ASSET-02`, `DL-ASSET-03` | Reuse first; generate only for named gaps (the four faces and the keepsake); never alter the protected folders. |
| `DL-ASSET-08` | The card changes no book page, caption or art. |
| `DL-CIN-16` | The Grand Puff transformation clip is untouched; the beats come before it. |
| `DL-PLAN-04` | Reuse the Teacher's ladder; keep existing reward identities and regression coverage. |
| `DL-PLAN-05`, `DL-QA-05`, `DL-QA-06` | Authorization, implementation and acceptance stay separate; child observation and owner review are their own gates. |

### Related findings (none repaired, closed or changed)

| Finding | State | Relation |
|---|---|---|
| `MA-ACCESS-001` | P1 `BLOCKED_EXTERNAL` | New objectives need exact spoken cues: FP is incomplete until its recordings exist. |
| `MA-TYPE-004` | P1 `CONFIRMED_OPEN` | Emoji carry reward meaning; QM takes the medal emoji off her screen. The game-wide finding stays open. |
| `MA-TYPE-003` | P1 `CONFIRMED_OPEN` | The new cards and keepsake carry no text; captions remain adult support. |
| `MA-CI-005` | P1 `CONFIRMED_OPEN` | The zero-input snapshot must keep covering medals and add `feelings_learning_progress`. |
| `MA-CODE-003` | P2 `CONFIRMED_OPEN` | No shared pointer helper exists yet; build the card pointer as one reusable helper and add no new clone. |
| `MA-CODE-001` | P2 `CONFIRMED_OPEN` | New logic goes in satellites, not `scripts/main.gd`. |
| `MA-AUDIO-001` | P2 `FIXED_PENDING_VERIFICATION` | 43 new or regenerated voice files join the audio ledger and its human-review backlog. |
| `MA-PLAY-001` | P1 `CONFIRMED_OPEN` | Grand Puff is on the Day One route; FP does not change reachability. |
| `MA-CHILD-001` | P1 `BLOCKED_EXTERNAL` | The two-week log is private observation and does not close this finding. |
| `MA-OPERA-014` | P1 `CONFIRMED_OPEN` | The Pop Star, Ballerina and Racer rebuilds change those careers' verbs; update their praise categories (QM section 5) when they land. |

No new finding is opened. The gaps the review found break no current rule
(the design language has no learning-goal rules), and the design language
treats a gap without a rule as an observation or proposal. This order adds
the features under existing rules (`DL-AUTH-05`).

## 5. Current state and dependencies (checked 2026-10-19)

- **Book:** on 2026-10-19 the owner decided that the V34 audit-fix work
  order (`cc603da5`) governs the next revision, V36, built on Codex's V34
  (`4f65c502`): its 14 changed captions win, V34 wording stays elsewhere, and
  V33's story numbering returns for pages 6 to 32 (record
  `OWNER_DECISION_2026-10-19.md`, commit `d75164b2`). The card is written for
  that V36 manuscript. `PAGE_PLAN.md` on the branch still shows V34, so the
  card also carries a V34 map. V35's caption proposals (`137a1b28`) stay
  proposals; V35 also proposed "a separate grown-up card", which this card
  fulfils. Anchors are rebound whenever words move (QC4).
- **Grand Puff care recast:** only on a local branch in a Codex worktree,
  three commits ahead of `dev`, with no remote copy. Landing it is FP0.
- **Voice:** the Guide speaker is the local Kokoro `af_heart` voice: two
  lines on `dev` (the 2026-10-14 objective guides) and five more on the
  care branch. New lines normally use the Parler pipeline
  (`design/reference/recipes/voice_lines.md`); the owner chose a new voice
  for all of them (section 6).
- **Medals:** a ceremony on every ranked finish, a HUD tally, tier results
  in 15 Opera careers and tier words in Grand Puff's captions. Details in
  [QUIET_MEDALS.md](QUIET_MEDALS.md#2-what-she-sees-today-dev-e1dc3e21f67afeacf48a3609ac520468d6fecc28).
- **Teacher engine:** `scripts/teacher_lesson_plan.gd` steps up after three
  clean wins across levels 0 to 2 and never steps down. FP adds a step-down
  for feelings only; the Teacher does not change.

## 6. Package VG: the new narrator voice (shared by FP and QM)

Owner, 2026-10-19: "Regenerate all lines in new voice, this is not
preserved asset."

| Item | Work | Done when |
|---|---|---|
| VG1 | Pilot. Use the Parler candidate, selector and master pipeline in `assets/audio/voices/VOICE_MANIFEST.md` (`tools/make_parler_voice_trials.py`, `tools/select_filler_voices.py`, `tools/master_filler_voices.py`). Try at most two presets that no character uses today (the live map lists Joy, Lea, Jenna, Lauren, Gary, Jon, Tina, Rose, Mike, Emily, Laura and Will), described as a warm, calm, clear adult storyteller. Render three lines in each: "Grand Puff has a cold. Let's help!", "Achoo! Grand Puff has a cold. How does he feel?" and "You kept trying, and you did it!" Never condition on or imitate a family recording. | The owner listens and picks one voice (`DL-QA-06`). Rejected takes are kept as evidence. |
| VG2 | Regenerate the seven existing Guide lines in the chosen voice, same keys and texts: `guide_seek_tap_wiggly_tree` "Tap the wiggly tree!", `guide_dolls_catch_three` "Move left and right. Catch three sleepy dolls!", and the care branch's `guide_puff_cold_intro` "Grand Puff has a cold. Let's help!", `guide_puff_clean` "Tap his star to clean!", `guide_puff_relief` "Ahh! That feels better!", `guide_puff_almost` "Nearly clean! One more gentle wash!" and `guide_puff_healthy` "All clean! Feeling better!" Keep the old Kokoro sources and hashes under `assets_src/` as retired provenance. | One narrator voice for every Guide line. |
| VG3 | Generate the 21 FP lines ([FEELINGS_WITH_PUFF.md](FEELINGS_WITH_PUFF.md#4-voice-lines)) and the 15 QM lines ([QUIET_MEDALS.md](QUIET_MEDALS.md#4-voice-lines-new-narrator-voice-package-vg)) in the same voice. | 36 new files pass the selector's exact-word check. |
| VG4 | Records: update `assets/audio/objective_guides/OBJECTIVE_GUIDE_MANIFEST.json` (identity, status, provenance), add the narrator to the preset map in `VOICE_MANIFEST.md`, add an audio-ledger row per file (`DL-SND-10`) and `ASSET_LICENSES.md` lines, and extend `scripts/probe_audio.gd` to the new keys. | 43 files at 48 kHz mono Ogg Vorbis, 64 kbps or more, −16 LUFS-I ±1 LU, peak −1.5 dBTP or lower (`DL-SND-12`). |

Replacement bar (`DL-SND-17`): the change of speaker identity is
owner-directed (`ODR-GUIDE-VOICE-20261019`, `DL-QA-06`). Every other gate
still applies: complete provenance, routing, mono, device, child and
protected-asset checks, and a recorded human grade. If a regenerated line
grades worse than the line it replaces, hold that line and tell the owner.
The routing speaker name stays `guide`. `ODR-LUNA-OBJECTIVE-GUIDES-20261014`
keeps its line texts; only its voice choice is superseded.

## 7. Work packages

| ID | Work | Where | Details |
|---|---|---|---|
| QC1 to QC4 | Typeset, bind, publish and later rebind the question card and the parent log | `codex/mermaid-roshan-picture-book`, `books/chapter_one/companion/question_card/` | [QUESTION_CARD.md](QUESTION_CARD.md#4-what-codex-builds) |
| VG1 to VG4 | The new narrator voice, 7 regenerated and 36 new lines | `dev` work branch | Section 6 |
| FP0 | Land the Grand Puff care branch | Codex worktree, then `dev` | [FEELINGS_WITH_PUFF.md](FEELINGS_WITH_PUFF.md#2-before-you-start-fp0) |
| FP | Ladder, face cards and art, beats 1 and 3, routing, save key, probes | `dev` work branch | [FEELINGS_WITH_PUFF.md](FEELINGS_WITH_PUFF.md) sections 3 to 9 |
| QM1 to QM4 | Hide tiers, surprise keepsake and art, praise lines, `MEDALS.md` | `dev` work branch | [QUIET_MEDALS.md](QUIET_MEDALS.md) sections 3 to 7 |

## 8. Order, and what can run at the same time

1. **Now, in parallel:** QC on the book branch (it touches no game file);
   VG1, the voice pilot; and FP0, landing the care branch.
2. **Then:** QM's medal, HUD and Opera parts can start once the voice is
   chosen. Its Grand Puff caption and its audio routing wait for FP0, and
   must not run at the same time as FP in `scripts/games/dust_boss.gd`,
   `scripts/audio_director.gd` or the voice manifest.
3. **Then:** FP, after FP0 and VG2 to VG3.
4. Game packages (VG, FP, QM) merge into `dev` only with their own green
   branch CI; QC stays on the book branch. The two-week checks start when
   the card is printed, or when a game package reaches her phone through
   the normal `dev` to `master` promotion.

## 9. Acceptance and the two-week checks

Report three claims separately for each package: what was implemented, what
was machine-verified at the named commit, and what acceptance is still open
(visual, device, child, owner). Machine checks never establish learning or
child acceptance (`DL-PLAN-05`).

Each package ends with its own acceptance list. All three share the
grown-up's [two-week log](PARENT_LOG.md), which asks after each session:

1. Off-screen use: what did she say or do away from the screen or book that
   used it?
2. Choosing again: did she pick it again by herself?
3. Frustration: none, a little or a lot, and what happened?

The review's success signs: for the card, she answers more over rereads,
uses book words and retells three events in order; for Feelings with Puff,
she names a feeling unprompted ("I'm sad like Puff"); for quiet medals, she
still picks her favourite games without chasing medals.

## 10. Open owner questions (defaults apply until answered)

From [QUIET_MEDALS.md](QUIET_MEDALS.md#9-open-owner-questions-defaults-apply-until-answered):

- **OQ1:** Opera encore tokens and Grand Puff's two bonus pearls still pay
  more for faster or cleaner play. Default: unchanged.
- **OQ2:** surprises only on a game's first completion, which will be rare
  on her current save. Default: no other trigger.
- **OQ3:** a grown-up view of the hidden tiers. Default: none; the tiers stay
  in the save.

The VG1 voice pick and the card's wording also need the owner, but they are
approvals of built work, not open design questions.

## 11. Verification of this packet

- Impact record:
  [learning-sessions-handoff-20261018.json](../../../design/audit_impacts/learning-sessions-handoff-20261018.json).
- `MANIFEST.json` lists every packet file with its git-blob SHA-256.
- `REMOTE_VERIFICATION.json` is added after the push: an anonymous fetch of
  every manifest file from the exact commit, with hashes, access mode and
  time.

## 12. What this packet does not do

- No game code, scene, asset, voice, image, book page or release change.
- No merge to `dev` or `master`.
- No change to the Teacher, to tier maths, or to any protected recording.
- No "Count and Clean": the owner did not choose it.
- No claim about learning outcomes: the review's judgments are design
  readings, and only watching her can show what works.
