# Chapter development guide

Status: `BINDING_DOMAIN` for chapter planning and delegated creative work,
under `DL-PLAN-01` through `DL-PLAN-06`. Owner direction: 2026-09-05.
Subordinate to direct owner decisions and the existing operational, security,
protected-content, save, medium, cinematic, and release requirements.

## 1. Start here

Read the [master audit planning entry](../audit/MASTER_AUDIT_2026-08-09.md#0-planning-entry),
the [current design rules](06_COMPREHENSIVE_DESIGN_LANGUAGE.md), and the
applicable current chapter authorities in the
[reference library](10_CHAPTER_REFERENCE_LIBRARY.md). Use the
[chapter brief](templates/CHAPTER_BRIEF_V1.md) for each new chapter.
Consult the [document ledger](05_DOC_LEDGER.md) before treating an older bible
or work order as current. A source's self-declared authority is insufficient.

This guide applies after a chapter is commissioned; it does not commission an
unspecified next chapter or reopen deferred features. Existing Chapter 2/3
plans retain their scoped authority. This planning update accepts no runtime,
art, voice, device, child, or release result.

The owner's additional 2026-09-05 direction makes strategic evaluation of the
large unused-asset library part of future chapter development. The agent may
discover and select suitable existing assets within the approved chapter scope;
it should actively look for assets that improve play or story, not merely fill
an already-written shopping list. Section 6 defines the evaluation contract.
The same day's follow-up explicitly permits free reuse, modification, and
combination of mechanics. The [Northern/Ice World planning branch](chapters/NORTHERN_ICE_WORLD.md)
records the owner's example: a second chef game in an existing building,
combining cooking with customer orders and new contextual artwork.

## 2. Creative authority — owner decision, 2026-09-05

The owner selected these two policies during this guide's commissioning:

> Agent develops the chapter within agreed boundaries; owner reviews the playable result.

> Allow minor additions that preserve established canon; major characters and plot changes need approval.

Once the owner approves the premise and boundaries, the agent chooses the
detailed plan and develops the chapter through a reviewable playable result.
Routine planning, implementation, iteration, and expansion within that brief
need no additional approval. Record choices in the brief instead of repeatedly
asking the owner to reconfirm the same scope. Build and evaluate a representative
activity early; this is a development checkpoint, not an extra owner gate.

| Decision | Agent action |
|---|---|
| Existing or remixed mechanics, approved art reuse, staging, optional discoveries, kind feedback, and activity variations within the brief | Freely reuse, modify, combine, implement, verify, and record the rationale. Preserve applicable quality and asset constraints; similarity to an earlier game is not a defect. |
| New minor character or optional story thread | May invent within the approved premise. Record identity, role, source distinction, and continuity effects; use the limits below. |
| New major character, change to an established character, major plot development, or changed chapter premise or ending | Prepare the concrete proposal and ask before dependent implementation. Continue independent authorized work. Required controls remain within the existing child/one-finger rules. |
| Protected original/voice changes, policy exceptions, architecture decisions explicitly reserved for the owner, or new spending outside the recorded budget | Follow the existing authority requirement; chapter delegation alone grants none of these permissions. |
| Integration and release | Follow existing branch/probe/promotion rules. Creative authority does not grant missing acceptance evidence or an unsolicited release. |

A **minor addition** has a local supporting role, preserves established
identities and motives, and does not create a new mandatory cross-chapter
dependency. An optional thread cannot gate the main path or alter the approved
ending. A recurring companion, principal antagonist, new family relationship,
retcon, or change to a future chapter's central conflict is a major change even
if introduced briefly. Record invented content as agent-authored within the
delegated scope; do not attribute it to the book or to an owner decision.

Resolve ordinary uncertainty from current authorities and the approved brief.
Ask only when alternatives materially change story, player experience, cost,
scope, or a reserved decision. Name the choice, consequence, and recommended
answer. Silence is not approval for a reserved decision. A later explicit owner
instruction may expand or narrow this scope; record its date and exact scope.

## 3. What makes a Mermaid Roshan chapter

Start with a concrete wish the child can understand through a short voice cue
and a visible situation. Let intentional touch change a recognizable object
or relationship. Preserve that result when the child leaves. The chapter's
payoff should visibly follow from those actions and motivate what comes next.

Use familiar motor verbs in meaningful new situations. Freely modify their
sequencing, objectives, combinations, assistance, and contextual presentation
within the approved brief. For example, cooking a party cake and cooking a
customer's pictured order can share gesture implementations while offering
different decisions and outcomes. No new mechanic needs an owner question merely
because it changes an earlier mechanic; ask when it crosses a reserved scope.

Feature work may intentionally change the new activity's behavior and its tests.
Keep the existing activity's save/reward meaning and sibling behavior stable;
use configuration or a bounded variant where practical. Mechanical extraction
remains behavior-preserving under the separate refactor rules. Never patch an
unrelated failing probe to accept a regression or add special probe-only play.

Novelty can come from
purpose, sequence, collaboration, or discovery; it need not require a new
engine, control scheme, character redesign, or more generated art. Chapter 2's
construction arc is one example, not a required eight-job formula.

Follow existing short-session and assistance standards in game design section
4 and `DL-AGE-*`. Plan natural stopping points, a quiet beat after demanding
play, and a clear payoff. Optional depth may offer replay and precision while
the required path remains one-finger, non-reading, forgiving, and completable
without adult verbal instruction. More repetition is not more content.

Each activity has one sentence describing the causal result: "By doing X,
Roshan changes Y, so Z becomes possible." If only a counter changes, explain
why that is sufficient for this activity's purpose or redesign its visible
result. Transitions may establish geography rather than award a new prize.

## 4. Keep three related plans inspectable

| Plan | Record | Verify |
|---|---|---|
| Story causality | Prerequisite event, motivation, action, persistent consequence, next beat | The next beat is justified by what the child has seen and done; no reward or completed construction is threatened or erased. |
| Navigation | Visible entrance, destination, unlock/reveal, exit, exact return context | Fresh, partial, complete, replay, Back, and legacy access have coherent routes. No menu or shortcut silently bypasses the story geography. |
| Save progression | Owning fields, defaults, milestone writes, reconstruction, compatibility, malformed-state handling | Each meaningful boundary survives interruption and re-entry; passive/wrong/repeated input cannot earn completion or duplicate rewards. |

Use the current chapter sources for facts. Identify intentionally different
story and freeplay routes explicitly; a chapter-specific room/order does not
silently replace global freeplay. Use symbols and links for shared global
constants instead of copying their values into every chapter brief.

## 5. Production workflow

1. **Establish scope.** Record premise, entry/ending, creative boundaries,
   budget, dependencies, and the dated owner authorization in the brief.
   For a not-yet-commissioned chapter, prepare a proposal only.
2. **Inventory reuse.** Identify existing code, art masters, cutouts, voice
   cues, music, and routes. Cite approved source/provenance and acceptance
   limits. Name any gap before generation; follow the separate cinematic
   regime for every authored delivery frame.
   Absence from the current checkout is not evidence that art does not exist.
   When the owner identifies an existing family, trace relevant Git history,
   staged/untracked files in related worktrees, and original generation records
   before proposing replacement landmarks. Read other tasks' sources without
   changing their worktrees. Distinguish not-yet-located, recovered, rejected,
   and genuinely missing assets; preserve exact source bytes and hashes when
   building the review packet. Continue independent interaction planning while
   source-dependent visual decisions remain unresolved.
3. **Plan the whole chapter.** Complete the causal, navigation, save, pacing,
   and acceptance tables. Record proposed minor additions and novelty costs.
   Trace navigation against the actual painted surfaces: bridge decks, both
   banks, door thresholds, stairs and occluding rails. Specify Roshan's ground
   anchor and whole silhouette through each transition, in both directions and
   at supported camera/aspect states. A horizontal lane or a route diagram
   alone does not prove that she follows the artwork's walkable geometry.
4. **Build a representative activity.** Exercise enter → understand → act →
   visible result → save → leave → return. Include assistance, wrong/passive
   input, focus loss, and re-entry. Use the actual production implementation.
5. **Evaluate and revise.** Check composition, input, identity, causality,
   lifecycle, and measured performance where equipment exists. A machine
   pass does not establish comprehension or enjoyment. Fix the pattern before
   repeating it across the chapter; routine revisions remain delegated.
6. **Expand and connect.** Build bounded, independently testable activities,
   then verify chapter-wide state, navigation, audio, and story continuity.
   Preserve existing behavior during separately required mechanical refactors.
7. **Prepare the playable review.** Supply the exact build/source, chapter
   route, checkpoint scenarios, captures, change summary, and outstanding
   device/child/owner evidence. Follow existing full-suite and integration
   gates. Do not label incomplete product acceptance as complete.
8. **Learn from review.** Record observations, owner corrections, and reuse
   limitations. Promote a pattern into the reference library only for the
   claims actually demonstrated. Carry unresolved evidence forward explicitly.

## 6. Strategic use of unused assets

Search the existing inventories and relevant source/runtime families linked in
the reference library. Evaluate assets while shaping the detailed chapter plan,
and again before requesting new art. An overlooked location, prop, animation,
music cue, or interaction kit may suggest a better activity or optional beat.
Within delegated scope, the agent may adapt the plan to realize that benefit.
If the opportunity changes the approved premise, major cast, or ending, present
the opportunity for owner decision before developing the dependent story.

Create a bounded shortlist for this chapter rather than exhaustively consuming
the library. Assess complementary sets as well as individual assets: a complete
prop-state family may support meaningful construction where a single attractive
image cannot. Compare the best reusable option with a no-addition option and,
only for a documented gap, a new-asset option. No chapter has an asset-use quota.

For each shortlisted asset or coherent family, record:

- Exact paths, source/provenance/license, protection status, preview/contact
  sheet, and revision/hash for selected source bytes.
- Usage evidence: where it is referenced, dynamically loaded, exported, or
  reachable. A text-search miss is only an unused **candidate**, not proof of
  no consumers; generated paths, resource IDs, atlases, and manifests matter.
- Authority: approved/reusable, candidate needing review, superseded for a
  named scope, prohibited, or unknown. Unused and approved are separate facts.
- Proposed role and causal benefit: the specific activity, discovery, scene
  change, character interaction, or audio beat it would improve.
- Fit with story/canon, authored identity/style, phone readability, one-finger
  play, and neighboring assets; list missing states, voice cues, or connectors.
- Readiness and cost: true-2D suitability, native per-screen coverage, import
  limits, decoded memory/overdraw, integration work, and required acceptance.
- Decision: use now, reserve for a named later opportunity, reject for this
  chapter, or blocked pending evidence; include a short reason and next action.

First exclude violations of canon, protection, licensing, medium, and child
rules. Among viable choices, rank concrete player benefit and thematic fit,
then completeness and integration cost. A beautiful asset with weak gameplay
purpose should lose to a coherent useful family. Do not invent numeric quality
or acceptance scores to make a selection appear verified.

Reserve promising unused assets with a suggested theme/verb and known gaps in
the chapter's shortlist; this is an opportunity record, not authorization for
another chapter. Preserve originals and use new paths for permitted derivatives.
Do not delete unused work as part of selecting it. Retired 3D resources remain
archive evidence, not a resource pool or fallback; prohibited characters and
rejected designs remain excluded. Scoped non-boss reuse of inactive 2D art is
possible only where its current authority permits it, without restoring a cut
character, route, boss, or save identity. Cinematic reference use never makes
those pixels accepted full-frame delivery.

## 7. Readiness, dependencies, and budget

Maintain separate columns for authorization, implementation, and acceptance.
An activity can be authorized and implemented while device review is pending.
Missing external evidence blocks the corresponding acceptance claim; it does
not automatically block unrelated authorized development. Shared integration
gates and game-wide strict-zero 2D satisfaction still apply at their own scopes.

| Dependency type | Planning consequence |
|---|---|
| Approved source or protected recording unavailable | Identify affected objectives and prepare the recording/reference request. Do independent logic and other activities; do not present a generic fallback as accepted guidance. |
| Required engine/service absent or only proposed | Use a verified compatible extension path, or name the prerequisite implementation and its existing authorization. Never pretend the Mode Platform target already exists. |
| Device/child/owner review pending | Prepare a reproducible review packet and continue independent authorized work. Do not invent observations or close those gates. |
| Unresolved canon or reserved scope decision | Ask the concrete question and pause only dependent creative work. |
| Failing shared regression gate | Repair within authority or record the blocker; do not integrate red work. |

Every brief records scope limits: required activities, optional additions,
new mechanics, new art gaps, cinematic workload, and any paid-service budget.
Use existing project asset rules when no numeric generation budget was agreed;
do not invent an unlimited allowance. New purchases or third-party commissioning
require existing explicit authorization. Stop expansion at the approved chapter
boundary instead of appending another chapter or speculative framework.

Prioritize next work by child impact and dependencies, not by the oldest open
finding alone. Keep a short queue: actionable deliverable, prerequisites,
blocked portion, next verification, and who can supply missing evidence.

## 8. Chapter acceptance and guide evaluation

Use separate evidence entries for static checks, runtime probes, captures,
target-device measurements, child observation, and owner review. Link relevant
`DL-*` rules and existing audit findings; a planning checklist is not a second
finding ledger. Each entry states build, scope, result, and remaining limits.

The human review asks whether the purpose was understood, intentional action
caused a visible result, familiar verbs gained meaningful context, effort and
rest were balanced, and completion left something worth revisiting. Record
observations such as missed cues, unprompted successful actions, requested
replays, adult help, and comfortable stopping points. Do not convert an AI
score, a suggested target, or lack of observation into child acceptance.

The first commissioned chapter using this guide is a bounded autonomy trial.
Record where the agent guessed, needed material clarification, contradicted
canon, duplicated a system, exceeded scope, or required owner correction.
Record successes as well. The goal is fewer avoidable corrections with equal
or better player quality, not fewer questions at any cost. Update the reusable
guidance from evidence; do not silently expand creative authority from a pass.

## 9. Maintenance

At chapter completion or a relevant owner decision, update the brief, current
source links, reference library, and audit planning entry together. Preserve
historical evidence and stable rule/finding IDs. Check the document ledger and
run `python -B tools/audit_document_authority.py`; its selected fact checks are
structural safeguards, not a complete semantic or creative review.
