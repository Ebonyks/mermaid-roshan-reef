"""Preserve failed producer/native evidence; resume with robust FFmpeg JSON parsing."""
from pathlib import Path

HERE = Path(__file__).resolve().parent
text = (HERE / 'generate_care_guides.py').read_text(encoding='utf-8')


def replace_once(old: str, new: str) -> None:
    global text
    if text.count(old) != 1:
        raise RuntimeError('Producer anchor changed: ' + old[:80])
    text = text.replace(old, new, 1)


replace_once('OUT = Path(__file__).resolve().parent / "generated"',
             'OUT = Path(__file__).resolve().parent / "generated_resume"')
replace_once('return json.loads(output[start:]), command',
             'return json.JSONDecoder().raw_decode(output[start:])[0], command')
replace_once('manifest_path = OUT / "generation_manifest.json"', '''prior_path = OUT.parent / "generated/generation_manifest.json"
prior = json.loads(prior_path.read_text(encoding="utf-8"))
known_native = {row["key"]: row["native"] for row in prior["attempts"] if "native" in row}
manifest["previous_run"] = {"path": "generated/generation_manifest.json",
    "sha256": digest(prior_path), "synthesis_calls": prior["synthesis_calls"],
    "failure": prior.get("failure", "")}
manifest_path = OUT / "generation_manifest.json"''')
replace_once('''        audio = session.run(None, {
            "input_ids": np.array([[0, *ids, 0]], dtype=np.int64),
            "style": voices["af_heart"][len(ids)],
            "speed": np.full(1, 1.0, dtype=np.float32),
        })[0].reshape(-1)''', '''        if key in known_native:
            original = OUT.parent / "generated" / known_native[key]["path"]
            if digest(original) != known_native[key]["sha256"]:
                raise RuntimeError("Preserved native hash mismatch")
            audio, rate = sf.read(original, dtype="float32")
            if rate != SR:
                raise RuntimeError("Preserved native rate mismatch")
            record["native_reused_from"] = str(original.relative_to(OUT.parent))
            record["native_reused_sha256"] = digest(original)
            manifest["synthesis_calls"] -= 1
        else:
            audio = session.run(None, {
                "input_ids": np.array([[0, *ids, 0]], dtype=np.int64),
                "style": voices["af_heart"][len(ids)],
                "speed": np.full(1, 1.0, dtype=np.float32),
            })[0].reshape(-1)''')
target = HERE / 'generate_care_guides_resume.py'
if target.exists():
    raise RuntimeError('Resume producer already exists')
target.write_text(text, encoding='utf-8')
print(target)
