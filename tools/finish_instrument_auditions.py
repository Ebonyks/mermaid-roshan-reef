"""Verify and level-match private native auditions without limiting their transients."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
import json
import subprocess

import numpy as np
import soundfile as sf
import balance_main_arrangements as audio

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / 'build/dkc_instrument_auditions_20261101'
audio.BUILD = BUILD


def one(test):
    ident = test['id']
    source = BUILD / (ident + '.wav')
    pcm, rate = sf.read(source, dtype='float32', always_2d=True)
    assert rate == 48000 and pcm.shape[1] == 2 and np.isfinite(pcm).all()
    expected = test['end_qn'] * 60 / test['bpm'] + test['tail_seconds']
    assert abs(len(pcm) / rate - expected) < .035, ident
    assert 1e-6 < np.max(np.abs(pcm)) < .99999, (ident, 'silence or clipping')
    native = audio.native_state(BUILD / (ident + '_recalled.chunk.b64'))
    program = native.find('.//Program')
    assert program.get('ProgramPath') == test['program_path'], ident
    expected_selector = {'world_african_large_drums': '10', 'world_celtic_percussion_menu': '8',
                         'world_bodhran_hits': '1', 'world_antic_tabla': '5', 'world_modern_tabla': '3'}
    selectors = [s.get('KeyswitchSelection') for s in native.iter('ScriptProcessor')]
    if ident in expected_selector:
        assert expected_selector[ident] in selectors, (ident, selectors)
    if ident.startswith('bba2_'):
        samples = [s.get('SamplePath', '') for s in native.iter('SamplePlayer')]
        assert any(('cR78-BD' if ident.endswith('r78') else 'AceT1-BD') in p for p in samples)
    measured = audio.measure(source)
    raw_i, raw_tp = float(measured['input_i']), float(measured['input_tp'])
    assert raw_i > -65, (ident, 'missing instrument')
    gain = min(-22 - raw_i, -6 - raw_tp)
    output = BUILD / 'review' / (ident + '.wav')
    sf.write(output, pcm * 10 ** (gain / 20), rate, subtype='PCM_24')
    matched = audio.measure(output)
    assert float(matched['input_tp']) <= -5.95
    mono = pcm.mean(axis=1).astype('float64')
    mono_delta = 20 * np.log10(max(np.sqrt(np.mean(mono ** 2)), 1e-12) /
                              max(np.sqrt(np.mean(pcm.astype('float64') ** 2)), 1e-12))
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(output),
                    '-c:a', 'libvorbis', '-q:a', '6', str(output.with_suffix('.ogg'))], check=True)
    return dict(id=ident, program=test['program'], program_path=test['program_path'],
                notes=len(test['notes']), keyswitch_selectors=selectors,
                duration_seconds=round(len(pcm) / rate, 5), eq=test['eq'],
                raw_lufs=raw_i, raw_true_peak_dbtp=raw_tp, gain_db=round(gain, 4),
                review_lufs=float(matched['input_i']), review_true_peak_dbtp=float(matched['input_tp']),
                mono_rms_change_db=round(float(mono_delta), 3), source_sha256=audio.sha(source),
                native_recall_sha256=audio.sha(BUILD / (ident + '_recalled.chunk.b64')),
                review_wav_sha256=audio.sha(output), review_ogg_sha256=audio.sha(output.with_suffix('.ogg')),
                purpose=test['purpose'])


def main():
    assert (BUILD / 'render_status.txt').read_text().startswith('COMPLETE 28')
    (BUILD / 'review').mkdir(exist_ok=True)
    tests = json.loads((BUILD / 'auditions.json').read_text())
    with ThreadPoolExecutor(max_workers=3) as pool:
        rows = list(pool.map(one, tests))
    groups = {
        '01_lofi_electronic_kits': [t['id'] for t in tests[:5]],
        '02_world_percussion': [t['id'] for t in tests[5:10]],
        '03_leads_piano_kora': ['opera_house_pan', 'sky_lagoon_flute', 'castle_sunbird',
                               'world_nordic_upright_1_full', 'world_kora_1'],
        '04_chords_keys_plucks': ['castle_guitar_comp', 'castle_ep', 'sky_lagoon_valiha', 'castle_kit'],
        '05_bass_hand_percussion': ['sky_lagoon_bass', 'castle_bass', 'opera_house_congas',
                                    'opera_house_maracas', 'opera_house_timbales', 'opera_house_cowbell',
                                    'sky_lagoon_udu', 'sky_lagoon_bongos', 'sky_lagoon_guiro'],
    }
    reels = []
    for name, ids in groups.items():
        segments, markers, elapsed = [], [], 0.
        common_lufs = min(r['review_lufs'] for r in rows if r['id'] in ids)
        for ident in ids:
            test = next(t for t in tests if t['id'] == ident)
            pcm, rate = sf.read(BUILD / 'review' / (ident + '.wav'), always_2d=True)
            start = max(0, 2 * 60 / test['bpm'] - .15)
            end = test['end_qn'] * 60 / test['bpm'] + .85
            pcm = pcm[int(start * rate):int(end * rate)].copy()
            row = next(r for r in rows if r['id'] == ident)
            pcm *= 10 ** ((common_lufs - row['review_lufs']) / 20)
            fade = min(2400, len(pcm))
            pcm[-fade:] *= np.linspace(1, 0, fade)[:, None]
            markers.append(dict(start_seconds=round(elapsed, 4), id=ident))
            segments.append(pcm);elapsed += len(pcm) / rate
        out = BUILD / 'review' / (name + '.wav')
        sf.write(out, np.concatenate(segments), 48000, subtype='PCM_24')
        subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(out),
                        '-c:a', 'libvorbis', '-q:a', '6', str(out.with_suffix('.ogg'))], check=True)
        reels.append(dict(file=out.with_suffix('.ogg').name, common_lufs=round(common_lufs, 2), duration_seconds=round(elapsed, 4),
                          sha256=audio.sha(out.with_suffix('.ogg')), markers=markers))
    receipt = dict(status='PASS_NATIVE_AND_MEASUREMENTS', checked_utc=datetime.now(timezone.utc).isoformat(),
                   method='Falcon in isolated REAPER; actual preset-specific MIDI; native ReaEQ; static gain toward -22 LUFS with -6 dBTP ceiling. No limiter, forced saturation or reference-recording upload.',
                   private_audio=True, subjective_listening='PENDING', tests=rows, reels=reels)
    (BUILD / 'measurement_receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps([dict(id=r['id'], lufs=r['review_lufs'], peak=r['review_true_peak_dbtp']) for r in rows], indent=2))


if __name__ == '__main__':
    main()
