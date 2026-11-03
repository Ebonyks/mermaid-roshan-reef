"""Check performer provenance and cue-plan coverage before soundtrack construction."""
from pathlib import Path
import argparse
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]


def check(plan_path: Path, for_construction: bool = False, test_tracks: bool = False) -> list[str]:
    registry = json.loads((ROOT / 'design/music/performers/registry.json').read_text(encoding='utf-8'))
    roster = json.loads((ROOT / 'design/music/ENSEMBLE_ROSTER_2026-11-01.json').read_text(encoding='utf-8'))
    auditions = json.loads((ROOT / 'design/music/INSTRUMENT_AUDITIONS_2026-11-01.json').read_text(encoding='utf-8'))
    plans = json.loads(plan_path.read_text(encoding='utf-8'))
    issues = []
    profiles = {p['id']: p for p in registry['profiles']}
    expected = {p['id'] for p in roster['core'] + roster['guests']}
    if len(profiles) != 15 or set(profiles) != expected:
        issues.append('Registry must cover all ten core and five guest profiles exactly once')
    for p in profiles.values():
        path = (ROOT / p['path']).resolve()
        if not path.is_relative_to(ROOT) or not path.is_file():
            issues.append(f"{p['id']}: missing or unsafe profile path")
        elif hashlib.sha256(path.read_bytes().replace(b'\r\n', b'\n')).hexdigest() != p['sha256']:
            issues.append(f"{p['id']}: stale profile hash")
    if 'Bonobo' not in profiles['producer']['artist']:
        issues.append('Producer primary identity must retain the owner-selected Bonobo reference')
    available = {a['id'] for a in auditions['tests']}
    roles = {'lead', 'harmony', 'bass', 'groove', 'response', 'texture', 'rest'}
    for cue in plans['cues']:
        ident = cue['id']
        selected = {p['profile_id']: p for p in cue['performers']}
        if len(selected) != len(cue['performers']):
            issues.append(f'{ident}: duplicate performer ID')
        for p in cue['performers']:
            original = profiles.get(p['profile_id'])
            if not original or any(p[k] != original[k] for k in ['revision', 'sha256']):
                issues.append(f"{ident}/{p['profile_id']}: unknown or stale profile reference")
            for field in ['purpose', 'reference_principle', 'performance', 'physical_model', 'tone_review']:
                if not isinstance(p.get(field), str) or not p[field].strip():
                    issues.append(f"{ident}/{p['profile_id']}: missing {field}")
            if not p.get('audition_ids') or not set(p['audition_ids']) <= available:
                issues.append(f"{ident}/{p['profile_id']}: missing native source evidence")
        bar = 1
        for section in cue['sections']:
            if section['start_bar'] != bar or section['bars'] <= 0:
                issues.append(f'{ident}: non-contiguous section bounds')
            bar += section['bars']
            if set(section['roles']) != set(selected) or not set(section['roles'].values()) <= roles:
                issues.append(f"{ident}/{section['name']}: incomplete or invalid performer roles")
            if section['foreground'] not in selected or section['roles'].get(section['foreground']) != 'lead':
                issues.append(f"{ident}/{section['name']}: foreground must name the lead performer")
            if section['groove_leader'] not in selected:
                issues.append(f"{ident}/{section['name']}: missing groove leader")
            if not section.get('development') or not section.get('handoff'):
                issues.append(f"{ident}/{section['name']}: missing development or handoff")
        if bar - 1 != cue['bars']:
            issues.append(f'{ident}: section lengths do not fill the song')
        duration = cue['bars'] * cue['meter'][0] * 4 / cue['meter'][1] * 60 / cue['bpm'] + cue['tail_seconds']
        if abs(duration - cue['duration_seconds']) > .02:
            issues.append(f'{ident}: incorrect planned duration')
        if not cue['hook'].get('source') or not (ROOT / cue['hook']['source']).is_file():
            issues.append(f'{ident}: missing melody source')
        if ident == 'opera_house' and cue.get('steel_pan_parts') != 1:
            issues.append('Opera requires exactly one principal steel-pan part')
        if ident in {'sky_lagoon', 'castle'} and cue.get('steel_pan_parts') != 0:
            issues.append(f'{ident}: unintended steel pan')
        if for_construction and cue.get('review_before_construction_required', False):
            review = cue.get('owner_review', {})
            test_auth = cue.get('test_construction_authorization', {})
            test_evidence = (ROOT / test_auth.get('evidence', '')).resolve()
            private_test = (test_tracks and test_auth.get('status') == 'AUTHORIZED_PRIVATE_REVIEW_TESTS'
                            and test_auth.get('scope') == 'private_test_tracks_only'
                            and test_evidence.is_relative_to(ROOT) and test_evidence.is_file())
            if private_test:
                continue
            if review.get('status') != 'APPROVED' or not review.get('evidence'):
                issues.append(f'{ident}: owner review pending; do not construct the new full arrangement')
            elif not (ROOT / review['evidence']).is_file():
                issues.append(f'{ident}: owner-review evidence does not resolve')
    return issues


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan', type=Path, default=ROOT / 'design/music/CUE_PLANS_2026-11-01.json')
    parser.add_argument('--for-construction', action='store_true')
    parser.add_argument('--test-tracks', action='store_true', help='Apply the separately evidenced owner authorization for private review tests only')
    args = parser.parse_args()
    if args.test_tracks and not args.for_construction:
        parser.error('--test-tracks requires --for-construction')
    issues = check(args.plan, args.for_construction, args.test_tracks)
    for issue in issues:
        print('MUSIC_PROFILES|FAIL|' + issue)
    print('MUSIC_PROFILES|RESULT|' + ('FAIL' if issues else 'ALL OK'))
    raise SystemExit(bool(issues))


if __name__ == '__main__':
    main()
