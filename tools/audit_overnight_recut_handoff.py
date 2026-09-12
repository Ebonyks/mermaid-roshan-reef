"""Validate the overnight repair archive, frame mappings and blocked draft cards."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

if __package__:
    from .audit_grok_handoff_2 import check_card
else:
    from audit_grok_handoff_2 import check_card


def digest(path: Path) -> str:
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def audit(root: Path, require_ready: bool = False) -> list[str]:
    errors: list[str] = []
    def load(name: str):
        return json.loads((root / name).read_text(encoding='utf-8'))
    manifest = load('HANDOFF_PACKET.json')
    rows = manifest['files']
    declared = [r['path'] for r in rows]
    actual = {p.relative_to(root).as_posix() for p in root.rglob('*')
              if p.is_file() and p.name not in ('HANDOFF_PACKET.json', 'REMOTE_VERIFICATION.json')}
    if len(set(declared)) != len(declared) or set(declared) != actual:
        errors.append('manifest must cover each payload file exactly once')
    for row in rows:
        path = (root / row['path']).resolve()
        if not path.is_relative_to(root.resolve()):
            errors.append('unsafe payload path'); continue
        if not path.is_file() or digest(path) != row['sha256']:
            errors.append('payload hash mismatch: ' + row['path'])
        if any(not row.get(k) for k in ('source_path', 'role', 'license_provenance', 'modifications')):
            errors.append('missing provenance: ' + row['path'])
        if path.suffix.lower() in ('.jpg', '.png') and not row.get('dimensions'):
            errors.append('missing image dimensions: ' + row['path'])
    joined = ''.join(f"{r['path']}|{r['sha256']}\n" for r in sorted(rows, key=lambda r: r['path']))
    if hashlib.sha256(joined.encode()).hexdigest() != manifest['payload_sha256']:
        errors.append('payload digest mismatch')
    source = load('SOURCE_CUT.json')
    if (source['frames'], source['fps'], source['sha256']) != (3150, 24, '97471d822dd4d2fc05bbfa59f820e7db33451983876dc0a109da084f40e4b0e7'):
        errors.append('wrong overnight cut')
    plan = load('evidence/PICTURE_EDIT_PLAN.json')
    if digest(root / 'evidence/PICTURE_EDIT_PLAN.json') != source['plan_sha256']:
        errors.append('edit plan mismatch')
    queue = load('SHOT_REPAIR_QUEUE.json')['shots']
    ids = {j['shot_id'] for j in queue}
    if len(ids) != len(queue): errors.append('duplicate job id')
    cards = {}
    for job in queue:
        card = load(job['card']); sid = card['shot_id']; cards[sid] = card
        if sid != job['shot_id']: errors.append('queue/card mismatch')
        errors.extend(check_card(root, card, ids, ready=require_ready))
        covered = set()
        for a,b in card['master_ranges']:
            if not 0 <= a < b <= 3150: errors.append(sid + ': invalid master range')
            covered.update(range(a,b))
        mapped = set()
        for event in card['source_events']:
            a,b = event['master_range']; c,d = event['source_range']
            if b-a != d-c: errors.append(sid + ': unequal source duration')
            src = plan['sources'][event['source_id']]
            if src['sha256'] != event['source_sha256']: errors.append(sid + ': source identity changed')
            expected = [s for s in plan['timelines'][-1]['shots'] if s['source_id'] == event['source_id'] and s['record_frame'] <= a and b <= s['record_frame']+s['out_frame_exclusive']-s['in_frame'] and c == s['in_frame']+a-s['record_frame']]
            if not expected: errors.append(sid + ': source frame map does not match edit')
            if mapped.intersection(range(a,b)): errors.append(sid + ': overlapping map')
            mapped.update(range(a,b))
        if covered != mapped: errors.append(sid + ': incomplete source map')
        if not (root / f'boards/{sid}.jpg').is_file(): errors.append(sid + ': missing board')
    def visit(sid, chain):
        if sid in chain: errors.append('cyclic dependency'); return
        for dependency in cards[sid]['depends_on']:
            if dependency in cards: visit(dependency, chain | {sid})
    for sid in cards: visit(sid,set())
    rainbow_covered = set()
    for sid in ('R11','R12','R15','R16'):
        c = cards[sid]
        if not any(b.get('path','') == 'references/rainbow_dust_bunny_concept.png' for b in c['bindings']):
            errors.append(sid + ': concept identity unbound')
        for a,b in c['master_ranges']:rainbow_covered.update(range(a,b))
    if rainbow_covered != set(range(2504,2678)) | set(range(2846,3014)):
        errors.append('incomplete visible rainbow-bunny coverage')
    if cards['R10']['depends_on'] != ['R09'] or cards['R11']['depends_on'] != ['R10']:
        errors.append('broken scrub/jump/settle chain')
    for sid, card in cards.items():
        for binding in card['bindings']:
            if 'BABY_EAGLE_STANDING_IDENTITY' in (binding.get('path') or '') or 'BABY_EAGLE_PINNED_STATE' in (binding.get('path') or ''):
                errors.append(sid + ': rejected Eagle redraw is bound')
        if 'Baby Eagle' in card['exact_cast']:
            authority = card.get('eagle_identity_authority', {})
            if authority.get('path') != 'references/baby_eagle_original_book.png' or authority.get('sha256') != digest(root / 'references/baby_eagle_original_book.png'):
                errors.append(sid + ': missing original book Eagle authority')
        if 'Daddy' in card['exact_cast'] and not any(b.get('path') == 'references/daddy_generation_preview.jpg' for b in card['bindings']):
            errors.append(sid + ': exact Daddy identity is not bound')
    for sid in ('R09', 'R10'):
        if not cards[sid].get('little_bunny_hidden_until_jump'):
            errors.append(sid + ': hidden little-bunny start is not locked')
    if not cards['R09'].get('big_bunny_form_at_start') or not cards['R09'].get('cleaning_suds_required'):
        errors.append('R09: recognizable big bunny and visible soapy cleaning required')
    if cards['R17']['master_ranges'] != [[1717,1805]] or cards['R18']['master_ranges'] != [[1805,1919]]:
        errors.append('incomplete Eagle rescue/recovery coverage')
    if (root/'references/ba0048fc93_DUSTY_ATTIC_OCTAGON_ARENA_MASTER.png').exists():
        errors.append('obsolete wooden arena reintroduced')
    return errors


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('packet', type=Path)
    parser.add_argument('--require-ready', action='store_true')
    args = parser.parse_args()
    findings = audit(args.packet, args.require_ready)
    for finding in findings: print('RECUT|FAIL|' + finding)
    print('RECUT|' + ('FAIL' if findings else 'ALL OK: archive integrity, exact frame maps, draft cards, dependencies and rainbow coverage'))
    raise SystemExit(bool(findings))
