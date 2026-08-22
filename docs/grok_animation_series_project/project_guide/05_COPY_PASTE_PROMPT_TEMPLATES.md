# Reusable copy/paste prompts

Append `SERIES_LOCK` from the Project Constitution to every production prompt.

## Sequence kickoff — no generation

```text
Open a new sequence continuity ledger for [EPISODE_ID / SEQUENCE_ID / TITLE]. Do not generate yet. Cast: [CHARACTER IDs and authority versions]. Location: [LOCATION ID/version]. Props and current owners: [list]. Wardrobe/state: [list]. Starting emotional beat: [beat]. Ending emotional beat: [beat]. Read the attached script and return: shot list, continuity risks, required anchor stills, per-shot reference pack, and any missing authority that requires human input. Enforce the 15-second maximum.
```

## Shot-generation template

```text
SHOT: [ID], [authored duration], 16:9, audio off.
START: [exact opening pose/state].
ACTION: [one clear action with timing].
END: [exact ending pose/state].
CAMERA: [locked/pan/push/reframe; specify timing].
REFERENCE DOMAINS: Image 1 = [start frame/composition]; Image 2 = [character identity]; Image 3 = [other character identity]; Image 4 = [location geography]; Image 5 = [base-video style]. Apply each only in its domain; do not blend designs.
CONTINUITY: [screen sides, hand/prop ownership, wardrobe, geography, light].
NEGATIVES: [shot-specific drift risks].
```

## Character onboarding — first pass

```text
CHARACTER ONBOARDING, not production animation. Image 1 is the sole canonical identity authority for [CHARACTER]. Create a neutral 16:9 presentation containing one front, one three-quarter and one rear full-body study of the exact same character at consistent scale. Preserve [immutable traits]. Plain neutral background, no props, no text, no extra character, no costume variation, no photorealism or 3D. Do not invent details hidden in Image 1; keep uncertain areas simple and flag them for human approval.
```

## Reference conflict check — no generation

```text
Do not generate. Compare the attached references only within their declared domains: style, character identity, location geography and shot pose. List every apparent conflict. For each conflict, say which authority should control and what must remain unchanged. If authority is ambiguous, stop and request a human decision rather than averaging the designs.
```

## Continuity review — no regeneration

```text
Act as continuity reviewer. Compare this candidate to the attached accepted authorities and previous ending frame. Score 0–2 for identity, age/anatomy, wardrobe/color placement, topology, screen direction, hand/prop ownership, geography, camera/light continuity, style match and motion coherence. Cite the visible failure precisely. Return APPROVE only if every identity/topology/geography category scores 2; otherwise return REJECT with the smallest next prompt correction. Do not generate a replacement.
```

## Style extraction from the base video

```text
Analyze the attached owner-approved Mermaid Roshan base video as STYLE authority only. Do not infer canonical character details from it. Produce a compact style specification covering line weight/color, value grouping, highlight/shadow treatment, background paint, atmosphere, facial rendering, motion cadence, camera behavior, effects density and common failure modes. Then identify twelve representative timestamps matching the STYLE_SET checklist. Do not generate new art.
```
