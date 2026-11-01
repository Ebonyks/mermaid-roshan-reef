"""Seal existing studio test/capture evidence against exact source bytes."""
import hashlib
import json
import argparse
import re
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'tmp/studio-stress-20261015'
DEST = ROOT / 'audit/evidence/studio-dirty-furniture-20261015'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def seal(full_ci_exit=None):
    DEST.mkdir(parents=True, exist_ok=True)
    entries = []
    cases = [('final3.log', 'mobile-final3', '1280'),
             ('wide-final.log', 'mobile-wide-final', '1560')]
    for log_name, capture_dir, label in cases:
        log = SOURCE / log_name
        transcript = log.read_text(encoding='utf-8')
        assert 'ART_STRESS|RESULT: PASS failures=0' in transcript
        assert 'ART_STRESS|FAIL|' not in transcript
        assert 'SCRIPT ERROR' not in transcript
        paths = [log]
        paths += [SOURCE / capture_dir / (name + '.png') for name in
                  ['00_dirty_room_with_floor_supplies', '02_partial_scrub',
                   '05_all_furniture_clean']]
        for path in paths:
            target = DEST / (label + '_' + path.name)
            shutil.copy2(path, target)
            entries.append({'path': target.relative_to(ROOT).as_posix(),
                            'sha256': digest(target),
                            'role': 'diagnostic Mobile gameplay evidence'})
    for name in ['live.log', 'live-v2.log', 'full-ci.log', 'verbs-retry.log']:
        target = DEST / ('prior_' + name)
        shutil.copy2(SOURCE / name, target)
        entries.append({'path': target.relative_to(ROOT).as_posix(),
                        'sha256': digest(target),
                        'role': 'Prior diagnostic/reproduction; not final full-suite or visual acceptance'})
    names = ['scripts/day_one_art_studio.gd', 'scripts/day_one_art_furniture_2d.gd',
             'scripts/day_one_contact_action_2d.gd', 'scripts/attack_customizer.gd',
             'scripts/roshan_sprite_loop.gd', 'scripts/sprite_transition_2d.gd',
             'scripts/probe_day_one_art_attack_state.gd',
             'scripts/probe_day_one_art_studio_shots.gd',
             'tools/build_studio_furniture_states.py']
    names += [p.relative_to(ROOT).as_posix() for p in
              sorted((ROOT/'assets/castle/day_one_art_studio/furniture').glob('*.png'))]
    sources = {name: {'sha256': digest(ROOT/name),
               'utf8_lf_sha256': hashlib.sha256((ROOT/name).read_bytes().replace(b'\r\n', b'\n')).hexdigest()
               if name.endswith(('.gd', '.py')) else None} for name in names}
    receipt = {
        'baseline': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        'engine': '4.7.2-stable official.ed1daf0bf', 'renderer': 'Forward Mobile Vulkan RTX3060Ti',
        'save_isolation': 'Each process requires DAY_ONE_ART_USERDATA_ROOT and validates user:// is beneath it before instantiating main.',
        'sources': sources, 'evidence': entries,
        'review': 'The root orchestrator inspected dirty/partial/clean runtime PNGs at both aspects. Luna independently reviewed earlier state ownership and found the fringe and wipe/contact issues repaired by the final candidate.',
        'scope': 'Staged unfinished Craft Room checkpoint. Not a fresh-save whole-game run, target-device result, accepted visual-adapter PASS, owner acceptance or child comprehension evidence.',
        'prior_failures': 'live.log: opening clip hid the room plus pause cancellation failure. live-v2.log: state tests passed but pixel review rejected dirty texture multiplied into clean shader; wide capture dynamically resized an already-built stage and was rejected. final3/wide-final use correct clips-seen checkpoint, fixed shader and cold viewport construction.'
    }
    if full_ci_exit is not None:
        assert full_ci_exit == 0
        transcript = (SOURCE/'full-ci-retry.log').read_text(encoding='utf-8')
        suite = (ROOT/'scripts/ci.sh').read_text(encoding='utf-8')
        expected = re.search(r'for p in (.*?); do', suite).group(1).split()
        completed = re.findall(r'^PROBE (\S+) process exit: (\d+)$', transcript, re.M)
        assert [name for name, _code in completed] == expected
        assert all(code == '0' for _name, code in completed)
        assert not re.search(r'^PROBE .* (reported a failure|reported a resource|hit a script compile)',
                             transcript, re.M)
        target = DEST/'full_ci.log'
        shutil.copy2(SOURCE/'full-ci-retry.log', target)
        entries.append({'path': target.relative_to(ROOT).as_posix(),
                        'sha256': digest(target), 'role': 'Unmodified full local CI transcript'})
        receipt['full_suite'] = {'command': 'scripts/ci.sh',
                                  'process_exit': full_ci_exit,
                                  'trusted_probes': len(expected),
                                  'note': 'Exit status supplied only after the owning process finished. The first full run had an unexplained verbs process exit127; its isolated retry completed with exit0 and both transcripts are retained. The final complete rerun is separate. Existing advisory UNSATISFIED reports and headless visual skips are not acceptance.'}
    path = DEST/'RECEIPT.json'
    path.write_text(json.dumps(receipt, indent=2)+'\n', encoding='utf-8')
    print('STUDIOSEAL|OK|sources=%d evidence=%d' % (len(sources), len(entries)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--full-ci-exit', type=int, choices=[0])
    seal(parser.parse_args().full_ci_exit)
