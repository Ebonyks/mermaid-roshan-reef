# Master audit in everyday development

Status: `BINDING_OPERATIONAL` under `DL-AUTH-05`, `DL-AUTH-06`, and
`DL-AUTH-07`. Owner commission: 2026-09-06. Existing security, protected-content,
save, owner-decision, engine and release precedence remains unchanged.

## Read at the decision points

1. **Start:** use the [master task index](../audit/MASTER_AUDIT_2026-08-09.md#development-task-index).
   Read the planning entry, applicable design rules, related canonical findings,
   and current domain sources classified by the document ledger. State the
   relevant IDs and intended validation before implementation.
2. **Scope changes:** revisit affected rows and shared systems. Extend the
   impact record before dependent work. Continue independent authorized work;
   this process creates no routine owner approval checkpoint.
3. **Review:** compare the actual change with its rules and acceptance criteria.
   Check siblings, callers, save/input/lifecycle effects as applicable. Review
   the game in context when the acceptance rules require it.
4. **Completion:** update changed canonical facts, finding state/history and
   authority rows, run the required gates, and report outstanding evidence.
   A new feature can have no related finding; it still needs applicable rules.

The August 9 master is the canonical audit despite its dated filename. The
[design language](06_COMPREHENSIVE_DESIGN_LANGUAGE.md) owns durable `DL-*`
rules; the master and [finding register](../audit/findings/ACTIVE_FINDINGS_2026-08-13.md)
own compliance and closure; the [ledger](05_DOC_LEDGER.md) classifies other
documents. Later rounds retain their declared scope. Do not copy historical
counts into current instructions or choose authority by filename date.

## One compact impact record per development change

Create or update a JSON file in `design/audit_impacts/`. Link it from the chapter
brief, repair record, or PR description. The committed record is required even
when a PR description also summarizes it, so local and CI checks see the same
evidence. One record may cover a coherent task spanning several commits.

Use this shape, replacing all illustrative values with real evidence:

```json
{
  "id": "unique-task-id",
  "scope": "What changes and why it benefits the child or development process",
  "baseline": "full 40-character source commit SHA",
  "rules": ["DL-AUTH-05", "DL-AUTH-06"],
  "findings": [],
  "no_findings_reason": "Explain why no existing finding is being repaired",
  "files": ["exact/repository/path.ext"],
  "validation": [
    {
      "command": "Exact command or named review",
      "result": "PENDING",
      "evidence": "Build/commit and log, capture or review reference; state missing evidence"
    }
  ],
  "acceptance_gaps": "Name remaining visual/device/child/owner gates, or explain non-applicability"
}
```

- `rules` contains defined, individual `DL-*` IDs; `findings` contains defined
  individual `MA-*` IDs or an empty list with a nonempty reason. No invented
  finding is needed for a new feature. Review verifies applicability.
- `files` lists exact paths, including additions and deletions; directories and
  wildcards are rejected. The impact JSON itself is self-describing metadata
  and need not list itself. No other project files are exempt.
- `baseline` identifies the task's source commit and must exist in candidate
  ancestry. It records provenance; it does not select or narrow the CI diff.
- Each validation result is `PASS`, `FAIL`, `PENDING`, or `NOT_APPLICABLE`.
  Pending/failed evidence remains explicit. This structural gate does not waive
  any blocking test or independently verify a claimed result.
- Update a record when its scope or evidence changes. An unchanged old record
  cannot cover a new diff. Historical records retain their original baseline
  and evidence; do not delete, rename, or bulk-update them for unrelated work.
- New Markdown still needs a document-ledger row. JSON impact records use the
  structured change gate and do not create Markdown-ledger entries.

## Run the gates

```text
python -B tools/audit_document_authority.py
python -B tools/audit_development.py --base auto
python -B -m unittest tools.tests.test_audit_document_authority tools.tests.test_audit_development
```

The development check validates the identical top-level instruction contract,
required task routes, target headings, and coverage invocation in both CI entry
points. Every numbered master-audit and design-language section must be indexed;
adding or renaming a section requires refreshing the index in the same change.
`--base auto` also checks coverage of
the actual Git diff, including staged, unstaged and unignored new files.
Missing history fails closed. CI chooses the push's previous SHA or PR base;
new-branch/manual runs use the integration merge-base. Locally, a dirty checkout
at integration HEAD compares with HEAD; a clean checkout at integration HEAD
compares with its first parent so a committed integration cannot pass an empty diff.
Topic work compares with its integration merge-base. For a deliberate local
reconciliation using `git merge --no-commit origin/dev`, coverage compares with
the incoming integration parent, and ancestry may resolve through `MERGE_HEAD`;
unresolved conflicts always fail. This permits validation before the merge commit
without claiming already-integrated changes as new task work. For another local
range, use `--base <commit-or-ref>` and report that range; do not narrow CI's range.
Impact records must be added or updated inside the checked range to supply coverage.

The existing full local CI and GitHub probe workflow run the new checks along
with existing gates. `audit_document_authority.py` also validates the entry-point
and navigation contract. Its standalone run does not assess Git change coverage.
The root contract is mirrored in `tools/audit_development.py`; change all three
copies together when explicitly commissioned to revise project instructions.

## Report three separate claims

State what was **implemented**, what was **machine-verified** at the named
candidate, and what **acceptance remains outstanding**. Follow master audit
section 9 for repairs and section 12 for whole-game satisfaction. Structural
traceability and no-regression checks never establish full visual, device,
child, owner, or game-wide acceptance. Keep findings pending verification until
their actual closure evidence is complete.
