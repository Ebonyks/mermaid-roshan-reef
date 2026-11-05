#!/usr/bin/env python3
"""Validate/render chapter canon and map. No reference pass grants game acceptance."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path

CANON = 'design/reference/canon.json'
MAP = 'design/chapters/chapter_map.json'
CANON_VIEW = 'design/reference/CANON.md'
MAP_VIEW = 'design/chapters/CHAPTER_MAP.md'
MASTER = 'audit/MASTER_AUDIT_2026-08-09.md'
START = '<!-- CHAPTER_BOARD_START -->'
END = '<!-- CHAPTER_BOARD_END -->'
RUNGS = ['PLANNED', 'COMMISSIONED', 'PLAYABLE_REVIEW', 'ON_PHONE', 'ACCEPTED']

def load(root: Path, name: str):
    return json.loads((root / name).read_text(encoding='utf-8'))

def path_issues(root: Path, name: str) -> list[str]:
    if not isinstance(name, str) or not name: return ['empty source path']
    relative = name.split('#', 1)[0]
    path = (root / relative).resolve()
    if ':' in relative or not path.is_relative_to(root.resolve()) or any(p in {'.git', '.secrets', '.aws'} for p in Path(relative).parts):
        return ['unsafe source path: ' + name]
    return [] if path.is_file() else ['missing source: ' + name]

def validate(root: Path, canon: dict, chapters: dict) -> list[str]:
    issues = []
    if canon.get('schema') != 'design_reference_canon/1': issues.append('wrong canon schema')
    if chapters.get('schema') != 'chapter_map/1': issues.append('wrong chapter-map schema')
    rows = canon.get('entities', [])
    ids = [row.get('id') for row in rows]
    if not rows or len(ids) != len(set(ids)): issues.append('missing/duplicate canon entities')
    conflicts = canon.get('conflicts', [])
    conflict_ids = {row.get('id') for row in conflicts}
    decisions = {row['id'] for row in load(root, 'design/reference/owner_decisions.json')['decisions']}
    for row in rows:
        identity = row.get('id', '?')
        for field in ('id', 'names', 'status', 'role', 'identity', 'voice', 'movement', 'appears_in', 'sources', 'chapter_latitude', 'voice_availability'):
            if not row.get(field): issues.append(identity + ': missing ' + field)
        if not re.fullmatch(r'(CHR|PLC|OBJ|STY|CUT)-[A-Z0-9-]+', identity): issues.append('invalid canon ID: ' + identity)
        if row.get('status') not in {'ACTIVE','PLANNED','RETIRED','REMOVED_IP_HOLD','CUT'}: issues.append(identity + ': invalid status')
        latitude = row.get('chapter_latitude', {})
        if latitude.get('value') not in {'NONE','MINOR','RESERVED'} or not latitude.get('scope'): issues.append(identity + ': missing latitude scope')
        for source in row.get('sources', []):
            if not isinstance(source, dict) or not source.get('authority'): issues.append(identity + ': source authority missing'); continue
            issues.extend(path_issues(root, source.get('path')))
        for field in ('chapter_latitude', 'voice_availability'):
            issues.extend(path_issues(root, row.get(field, {}).get('source')))
        movement = row.get('movement')
        if movement and movement != 'GAP': issues.extend(path_issues(root, movement))
        for art in row.get('identity', {}).get('art', []):
            errors = path_issues(root, art.get('path'))
            issues.extend(errors)
            if not errors and hashlib.sha256((root / art['path']).read_bytes()).hexdigest() != art.get('sha256'): issues.append(identity + ': identity source hash drift: ' + art['path'])
            if not art.get('scope'): issues.append(identity + ': art acceptance scope missing')
        for reference in row.get('conflicts', []):
            if reference not in conflict_ids: issues.append(identity + ': unknown conflict ' + reference)
        for reference in row.get('decisions', []):
            if reference not in decisions: issues.append(identity + ': unknown owner decision ' + reference)
    question_ids = {row.get('id') for row in canon.get('open_questions', [])}
    for question in canon.get('open_questions', []):
        if not all(question.get(field) for field in ('id','question','default','blocks','source')): issues.append('incomplete open question')
        issues.extend(path_issues(root, question.get('source')))
    for conflict in conflicts:
        if len(conflict.get('sources', [])) < 2 or not conflict.get('default'): issues.append('conflict lacks both sources/default: ' + conflict.get('id','?'))
        if conflict.get('status') == 'OPEN' and conflict.get('question_id') not in question_ids: issues.append('open conflict lacks registered question ID')
        for source in conflict.get('sources', []): issues.extend(path_issues(root, source.get('path')))
    precedence = canon.get('book_precedence', {})
    if precedence.get('decision') != 'ODR-BOOK-FIRST-20261031': issues.append('book-first owner correction is missing')
    issues.extend(path_issues(root, precedence.get('book_script')))
    manifest = load(root, 'design/reference/book_sources/SOURCES.json')
    for row in manifest.get('sources', []):
        errors = path_issues(root, row.get('path')); issues.extend(errors)
        if not errors and hashlib.sha256((root / row['path']).read_bytes()).hexdigest() != row.get('sha256'): issues.append('book source hash drift: ' + row['path'])
    for chapter in chapters.get('chapters', []):
        rung = chapter.get('rung')
        if rung not in RUNGS: issues.append('invalid chapter rung'); continue
        for field in ('name','authorization','implementation','entry_condition','end_state','ending_obligation','sources','evidence'):
            if not chapter.get(field): issues.append(chapter['id'] + ': missing ' + field)
        for source in chapter.get('sources', []): issues.extend(path_issues(root, source))
        for source in chapter.get('trusted_probes', []) + chapter.get('untrusted_probes', []): issues.extend(path_issues(root, source))
        evidence = chapter.get('acceptance_evidence', {})
        for threshold, fields in [('PLAYABLE_REVIEW', ['fresh_save_route','static_bindings','reward_clip_seam','exact_head_probes','captures']), ('ON_PHONE',['device_session']), ('ACCEPTED',['owner_review'])]:
            if RUNGS.index(rung) >= RUNGS.index(threshold):
                for field in fields:
                    if not evidence.get(field): issues.append(chapter['id'] + ': ' + rung + ' lacks ' + field)
        for evidence_path in evidence.values(): issues.extend(path_issues(root, evidence_path))
    for row in chapters.get('carried_state', []):
        if not row.get('chapter_must_decide') or not row.get('sources'): issues.append('carried state lacks decision/source')
        for source in row.get('sources', []): issues.extend(path_issues(root, source))
    for row in chapters.get('open_threads', []):
        if not row.get('owner_mark') or not row.get('mark_authority'): issues.append('thread owner mark missing')
        for source in row.get('sources', []): issues.extend(path_issues(root, source.split(' (',1)[0]))
    return sorted(set(issues))

def cell(value) -> str:
    return str(value).replace('|', '&#124;').replace('\n', ' ')

def link(path: str, prefix: str = '../../') -> str:
    return '[' + cell(path) + '](' + prefix + path + ')'

def render_canon(data: dict) -> str:
    lines = ['# Chapter canon register', '', 'Status: SUPPORTING_CURRENT. Generated from canon.json by tools/design_reference.py. Narrative authority comes from the cited book and owner decisions; source-code entries describe implementation. No generated table accepts art, voice, runtime, device or child evidence.', '', 'Use the [book source register](BOOK_SOURCES.md) and [chapter map](../chapters/CHAPTER_MAP.md). Major plot/character changes remain reserved. Conflicts marked OPEN retain a question rather than an invented answer.', '']
    for row in data['entities']:
        lines += ['## ' + row['id'], '', '**' + ', '.join(row['names']) + '** — ' + row['status'], '', row['role'], '', '| Field | Source-bound value |', '|---|---|', '| Chapter latitude | ' + cell(row['chapter_latitude']['value'] + ': ' + row['chapter_latitude']['scope']) + ' |', '| Voice availability | ' + cell(row['voice_availability']['type']) + ' |', '| Voice restrictions | ' + cell(row['voice'].get('note', row['voice']['type'])) + ' |', '| Chapters | ' + ', '.join(row['appears_in']) + ' |', '| Movement | ' + ('GAP' if row['movement'] == 'GAP' else link(row['movement'])) + ' |', '| Sources | ' + '; '.join(link(source['path']) + ' (' + cell(source['authority'] + ': ' + source.get('location','')) + ')' for source in row['sources']) + ' |', '| Conflicts | ' + ', '.join(row['conflicts']) + ' |', '| Owner decisions | ' + ', '.join(row['decisions']) + ' |', '']
        for art in row['identity']['art']: lines += ['- Identity: ' + link(art['path']) + '; SHA-256 ' + art['sha256'] + '. ' + art['scope']]
        lines += ['- Preserve: ' + cell('; '.join(row['identity']['must']) or 'Preserve the source-bound identity and narrative above; no new traits inferred.'), '- Never: ' + cell('; '.join(row['identity']['never'])), '']
    lines += ['## Conflicts and open questions', '']
    for row in data['conflicts']:
        lines += ['### ' + row['id'] + ' — ' + row['topic'], '', row['status'] + (': ' + row['question_id'] if row.get('question_id') else '') + '. ' + row['default'], '', 'Sources: ' + '; '.join(link(source['path']) for source in row['sources']) + '.', '']
    lines += ['## Open questions', '', '| ID | Question | Default, not an owner answer | Blocks | Source |', '|---|---|---|---|---|']
    for row in data.get('open_questions', []):
        lines.append('| ' + row['id'] + ' | ' + cell(row['question']) + ' | ' + cell(row['default']) + ' | ' + cell(row['blocks']) + ' | ' + link(row['source']) + ' |')
    return '\n'.join(lines) + '\n'

def render_map(data: dict) -> str:
    lines = ['# Chapter map', '', 'Status: SUPPORTING_CURRENT. Generated from chapter_map.json by tools/design_reference.py. This is the single home for chapter aliases, carried state and open threads. Numbers/names and owner marks retain provisional handoff defaults; code and save keys keep their names. A scoped commission does not commission a whole ending.', '', 'Read the [canon](../reference/CANON.md), [book source](../reference/BOOK_SOURCES.md), [guide](../09_CHAPTER_DEVELOPMENT_GUIDE.md) and [chapter board](../../audit/MASTER_AUDIT_2026-08-09.md#chapter-board).', '']
    for row in data['chapters']:
        lines += ['## ' + row['id'], '', '**' + row['name'] + '**', '', '| Field | Value |', '|---|---|']
        fields = [('Aliases', ', '.join(row['aliases'])), ('Premise',row['premise']), ('Authorization',row['authorization']), ('Implementation',row['implementation']), ('Evidence rung',row['rung']), ('Entry save condition',row['entry_condition']), ('End state',row['end_state']), ('Next-chapter obligation',row['ending_obligation'])]
        lines += ['| ' + label + ' | ' + cell(value) + ' |' for label,value in fields]
        lines += ['| Code entry points | ' + cell('; '.join(key + ': ' + value for key,value in row['code'].items())) + ' |', '| Trusted probes | ' + '; '.join(link(p) for p in row['trusted_probes']) + ' |', '| Diagnostic/unrostered probes | ' + '; '.join(link(p) for p in row['untrusted_probes']) + ' |', '| Sources | ' + '; '.join(link(p) for p in row['sources']) + ' |', '']
    lines += ['## Carried state', '', '| Item | Existing state | Chapter must decide | Sources |', '|---|---|---|---|']
    for row in data['carried_state']: lines.append('| ' + row['id'] + ' | ' + cell(row['what']) + ' | ' + cell(row['chapter_must_decide']) + ' | ' + '; '.join(link(p) for p in row['sources']) + ' |')
    lines += ['', '## Open threads', '', '| Thread | Continuity obligation | Owner mark and authority | Sources |', '|---|---|---|---|']
    for row in data['open_threads']: lines.append('| ' + row['id'] + ' | ' + cell(row['thread']) + ' | ' + cell(row['owner_mark'] + '; ' + row['mark_authority']) + ' | ' + '; '.join(link(p.split(' (',1)[0]) for p in row['sources']) + ' |')
    lines += ['', '## Blocked sources', '', '| Source | Limit | Evidence |', '|---|---|---|']
    for row in data['blocked_sources']: lines.append('| ' + row['id'] + ' | ' + cell(row['what']) + ' | ' + cell(row['source']) + ' |')
    return '\n'.join(lines) + '\n'

def render_board(data: dict) -> str:
    lines = [START, '| Chapter | Rung | Authorization / implementation | Evidence and blockers |', '|---|---|---|---|']
    for row in data['chapters']:
        evidence = link(row['evidence'], '../')
        blockers = ', '.join(row['findings']) or 'Whole-chapter runtime/acceptance missing; see map.'
        if row['id'] == 'CH-3': blockers += ' Chapter 3 probes are absent from both trusted rosters; workflow edits need a separately explicit task.'
        lines.append('| [' + cell(row['name']) + '](../design/chapters/CHAPTER_MAP.md#' + row['id'].lower() + ') | ' + row['rung'] + ' | ' + cell(row['authorization'] + ' / ' + row['implementation']) + ' | ' + evidence + '; ' + cell(blockers) + ' |')
    return '\n'.join(lines + [END])

def check(root: Path, render: bool = False) -> list[str]:
    try:
        canon, chapters = load(root, CANON), load(root, MAP)
        issues = validate(root, canon, chapters)
        if issues: return issues
        products = {CANON_VIEW: render_canon(canon), MAP_VIEW: render_map(chapters)}
        master = (root / MASTER).read_text(encoding='utf-8')
        if master.count(START) != 1 or master.count(END) != 1: return ['chapter-board markers missing/duplicated']
        expected = master[:master.index(START)] + render_board(chapters) + master[master.index(END) + len(END):]
        products[MASTER] = expected
        for name, content in products.items():
            path = root / name
            if render: path.write_text(content, encoding='utf-8')
            elif not path.is_file() or path.read_text(encoding='utf-8') != content: issues.append('stale generated chapter reference: ' + name)
        return issues
    except (OSError, ValueError, TypeError, KeyError) as exc:
        return ['chapter reference unreadable: ' + str(exc)]

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument('--check',action='store_true')
    parser.add_argument('--render',action='store_true')
    args=parser.parse_args()
    if args.check and args.render: parser.error('choose --check or --render')
    issues=check(args.root.resolve(),args.render)
    for issue in issues: print('REFERENCE|FAIL|' + issue)
    print('REFERENCE|RESULT|' + ('FAIL' if issues else 'ALL OK'))
    return int(bool(issues))

if __name__ == '__main__': raise SystemExit(main())
