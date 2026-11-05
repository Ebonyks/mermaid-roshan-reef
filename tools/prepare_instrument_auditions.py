"""Prepare private native UVI comparisons from captured presets and existing music.

No samples/presets are committed. REAPER's Lua worker performs the audio synthesis.
"""
from pathlib import Path
import base64
import hashlib
import json
import xml.etree.ElementTree as ET
import zlib

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / 'build/dkc_instrument_auditions_20261101'
WARM = ROOT / 'build/warm_ensemble_20261101'
SCORES = ROOT / 'assets_src/audio/music/warm_ensemble_20261101'


def lua(value):
    if isinstance(value, dict):
        return '{' + ','.join('[' + lua(k) + ']=' + lua(v) for k, v in value.items()) + '}'
    if isinstance(value, list):
        return '{' + ','.join(map(lua, value)) + '}'
    if value is None:
        return 'nil'
    if isinstance(value, bool):
        return 'true' if value else 'false'
    return json.dumps(value, ensure_ascii=False)


def note(qn, pitch, velocity, duration=.10):
    return dict(qn=round(qn, 5), pitch=pitch, velocity=velocity, duration_qn=duration)


def kit_pattern(mapping):
    """Identical original four-bar cell, translated to each actual kit mapping."""
    notes = []
    for bar in range(4):
        q = 2 + bar * 4
        for pos, velocity in [(0, 85), (1.75, 63), (2.5, 76)]:
            notes.append(note(q + pos, mapping['kick'], velocity))
        for pos in [1.025, 3.025]:
            notes.append(note(q + pos, mapping['snare'], 72 if bar % 2 else 81))
        for i in range(8):
            notes.append(note(q + i / 2 + (.025 if i % 2 else 0), mapping['hat'], 43 if i % 2 else 57))
        notes.append(note(q + 3.75, mapping['rim'], 37))
    return notes


def world_pattern(keys, switch):
    notes = [note(.1, switch, 100, .05)]
    for bar in range(4):
        q = 2 + 4 * bar
        for pos, idx, vel in [(0, 0, 81), (.75, 1, 52), (1.5, 2, 69), (2.25, 1, 44), (2.75, 0, 74), (3.5, 3, 61)]:
            notes.append(note(q + pos, keys[idx], vel, .14))
        if bar == 3:
            for i in range(4):
                notes.append(note(q + 3.5 + i * .125, keys[i % len(keys)], 42 + i * 7, .08))
    return notes


def main():
    BUILD.mkdir(parents=True, exist_ok=True)
    tests = []

    def add(ident, state, notes, bpm=100, eq=None, purpose=''):
        path = state.resolve()
        assert path.is_relative_to(BUILD) or path.is_relative_to(WARM)
        raw = base64.b64decode(path.read_bytes())
        # REAPER's current Falcon VST3 state wrapper; fail explicitly if changed.
        assert raw[196:198] in (b'x\x9c', b'x\xda', b'x\x01')
        xml = ET.fromstring(zlib.decompress(raw[196:]))
        program = xml.find('.//Program')
        assert program is not None and program.get('ProgramPath', '').startswith('$')
        tests.append(dict(id=ident, state=path.relative_to(ROOT).as_posix(),
                          state_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                          program=program.get('DisplayName'), program_path=program.get('ProgramPath'),
                          bpm=bpm, notes=sorted(notes, key=lambda n: n['qn']),
                          end_qn=18, tail_seconds=2.5,
                          eq=eq or [['hp', 30, 0, 1], ['lp', 14000, 0, .8]], purpose=purpose))

    for ident, mapping in [
        ('lofi_dreams_lofi_kit', dict(kick=48, snare=51, rim=53, hat=54)),
        ('lofi_dreams_jazz_kit', dict(kick=36, snare=38, rim=37, hat=42)),
        ('lofi_dreams_foley_kit', dict(kick=35, snare=38, rim=40, hat=41)),
        ('bba2_ace_t1', dict(kick=36, snare=38, rim=37, hat=42)),
        ('bba2_classic_r78', dict(kick=36, snare=38, rim=37, hat=42)),
    ]:
        add(ident, BUILD / (ident + '.chunk.b64'), kit_pattern(mapping), 110,
            purpose='Same original diagnostic beat; actual kit-specific MIDI notes; no sequencer trigger')
    for ident, keys, switch in [
        ('world_african_large_drums', [48, 53, 49, 71], 45),
        ('world_celtic_percussion_menu', [55, 60, 64, 67], 43),
        ('world_bodhran_hits', [48, 49, 50, 51], 36),
        ('world_antic_tabla', [48, 49, 50, 51], 40),
        ('world_modern_tabla', [48, 49, 60, 55], 38),
    ]:
        add(ident, BUILD / (ident + '.chunk.b64'), world_pattern(keys, switch),
            purpose='Original body/mute/response diagnostic; program keyswitch before first playing note; not a traditional-performance transcription')
    scores = {cue: json.loads((SCORES / cue / 'score.json').read_text(encoding='utf-8'))
              for cue in ['opera_house', 'sky_lagoon', 'castle']}
    selections = dict(opera_house=['pan', 'congas', 'maracas', 'timbales', 'cowbell'],
                      sky_lagoon=['flute', 'valiha', 'udu', 'bongos', 'guiro', 'bass'],
                      castle=['sunbird', 'guitar_comp', 'bass', 'ep', 'kit'])
    castle_hook = None
    for cue, ids in selections.items():
        score = scores[cue]
        for track in score['tracks']:
            if track['id'] not in ids:
                continue
            # Prefer a refrain so quiet introductory percussion is not mistaken for failure.
            start = next(sec['start_qn'] for sec in score['sections'] if sec['kind'] == 'C1')
            notes = [dict(n, qn=round(n['qn'] - start + 2, 5)) for n in track['notes']
                     if start <= n['qn'] < start + 16]
            if not notes:
                start = track['notes'][0]['qn']
                notes = [dict(n, qn=round(n['qn'] - start + 2, 5)) for n in track['notes']
                         if start <= n['qn'] < start + 16]
            for n in notes:
                n['duration_qn'] = min(n['duration_qn'], 18 - n['qn'])
            if cue == 'castle' and track['id'] == 'sunbird':
                castle_hook = notes
            add(cue + '_' + track['id'], WARM / (cue + '__' + track['id'] + '_rendered.chunk.b64'),
                notes, score['bpm'], track['eq'], 'Unchanged four-bar excerpt from current warm-ensemble study; isolated instrument')
    assert castle_hook
    add('world_nordic_upright_1_full', BUILD / 'world_nordic_upright_1_full.chunk.b64', castle_hook, 92,
        [['hp', 65, 0, 1], ['bell', 300, -1.5, 1.4], ['lp', 11000, 0, .8]],
        'Same Castle lead excerpt as Sunbird, to compare a new keyboard voice')
    add('world_kora_1', WARM / 'kora_1.chunk.b64', castle_hook, 92,
        [['hp', 90, 0, 1], ['lp', 11000, 0, .8]],
        'Same Castle lead excerpt as Sunbird; candidate guest, not a committed song substitution')
    (BUILD / 'auditions.json').write_text(json.dumps(tests, indent=2) + '\n', encoding='utf-8')
    (BUILD / 'auditions.lua').write_text('return ' + lua(tests) + '\n', encoding='utf-8')
    print(f'Prepared {len(tests)} short tests; no full compositions or factory samples written.')


if __name__ == '__main__':
    main()
