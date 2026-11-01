"""Retain failed export; add one measured codec-loudness correction, no new take."""
from pathlib import Path

HERE = Path(__file__).resolve().parent
text = (HERE / 'generate_care_guides_resume.py').read_text(encoding='utf-8')
old = 'OUT = Path(__file__).resolve().parent / "generated_resume"'
assert text.count(old) == 1
text = text.replace(old, 'OUT = Path(__file__).resolve().parent / "generated_final"', 1)
old = '        post, post_command = measure(export)'
assert text.count(old) == 1
text = text.replace(old, '''        post, post_command = measure(export)
        record["initial_encode"] = {"path": export.relative_to(OUT).as_posix(),
            "sha256": digest(export), "measurement": post}
        correction = -16.0 - float(post["input_i"])
        if abs(correction) > 0.25:
            calibrated = OUT / "review" / (key + "_calibrated.ogg")
            calibrated_command = list(encode)
            calibrated_command[calibrated_command.index("-af") + 1] = (
                filt + ",volume=" + format(correction, ".6f") + "dB")
            calibrated_command[-1] = str(calibrated)
            run(calibrated_command)
            record["codec_loudness_calibration"] = {
                "gain_db": correction, "command": calibrated_command,
                "source": "same conditioned native WAV; no additional inference or retiming"}
            export = calibrated
            encode = calibrated_command
            post, post_command = measure(export)''', 1)
target = HERE / 'generate_care_guides_final.py'
if target.exists():
    raise RuntimeError('Final producer already exists')
target.write_text(text, encoding='utf-8')
print(target)
