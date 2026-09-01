# Roshan synthetic preset audition — 2026-08-31

Status: **NON-RUNTIME / OPEN HUMAN LISTENING REVIEW**. None of these files is
referenced by the game. Faron and the protected family recordings were not read,
modified, conditioned into the model, or replaced.

## Purpose and rights boundary

This is a named-preset Parler-TTS Mini v1.1 audition for temporary synthetic
Roshan dialogue. It uses no reference audio, voice cloning, impersonation, or
talent identity. The model is Apache-2.0 and pinned to revision
`fbb2dd281092c5b414ef29cf9d8895f386f1feef`; the Parler code is pinned to
`d108732cd57788ec86bc857d99a6cabd66663d68`. Exact prompts, seeds, raw/review
hashes, tool versions, model/tokenizer artifact hashes, and normalization
commands are in `manifest.json`, `attempt_2/manifest.json`, and the adjacent
`run_provenance.json` files.

Primary sources:

- https://huggingface.co/parler-tts/parler-tts-mini-v1.1
- https://github.com/huggingface/parler-tts

## First discriminating pass

All five named presets rendered the same contextual line: “This castle is so
dusty!” The current shipped Laura `roshan_talk.ogg` measured 204.8 Hz median F0.

| Candidate | Median F0 | 75th-percentile F0 | Mean spectral centroid | Result |
|---|---:|---:|---:|---|
| Joy child spark | 257.2 Hz | 290.0 Hz | 2779.7 Hz | **Best natural child register; advance** |
| Lea child light | 237.2 Hz | 271.0 Hz | 3174.8 Hz | Bright backup |
| Jenna child bright | 231.8 Hz | 252.8 Hz | 2533.7 Hz | Backup only |
| Laura high baseline | 219.4 Hz | 267.8 Hz | 2881.1 Hz | Reject: still close to shipped adult register |
| Tina child tiny | 217.6 Hz | 231.8 Hz | 2569.7 Hz | Reject: prompt did not produce a high register |

These measurements screen for the reported “far too deep” problem; they do not
prove perceived age, naturalness, pronunciation, or acting quality. Human
listening remains blocking.

## Joy five-mood audition

Joy was then rendered without post-generation pitch shifting across happy,
calm, urgent, wonder, and castle-context delivery. The raw set is 44.1-kHz mono
WAV; review copies are 48-kHz mono 96-kbps Vorbis normalized toward -16 LUFS and
-1.5 dBTP.

| Line | Duration | Median F0 | 25th–75th percentile F0 | Review |
|---|---:|---:|---:|---|
| calm | 2.380 s | 263.2 Hz | 200.4–283.8 Hz | Open |
| castle context | 1.834 s | 257.2 Hz | 235.9–290.0 Hz | Open |
| happy | 2.264 s | 255.0 Hz | 208.0–280.1 Hz | Open |
| urgent, attempt 1 | 2.322 s | 207.7 Hz | 186.1–246.0 Hz | **Reject: register dropped** |
| urgent, attempt 2 | 2.426 s | 229.2 Hz | 200.7–285.4 Hz | Better, but still open |
| wonder | 2.496 s | 251.4 Hz | 198.3–288.7 Hz | Open |

Recommendation: use `joy_child_spark` as Roshan’s leading preset and Lea as the
fallback. Do not promote the urgent attempt-1 take. Before a full runtime batch,
listen to every Joy mood file for perceived age, exact transcript, artifacts,
and emotional fit; select or regenerate low-register outliers rather than
assuming the named preset and prose prompt guarantee identity.

## Reproduction

The generator is `tools/make_roshan_voice_auditions.py`. The disposable
environment used Python 3.10, Parler-TTS 0.2.2, Transformers 4.46.1, and CUDA
PyTorch/Torchaudio 2.6.0+cu124 on an RTX 3060 Ti. The key commands were:

```powershell
python -m venv --system-site-packages tmp/roshan_parler_env
tmp/roshan_parler_env/Scripts/python.exe -m pip install "git+https://github.com/huggingface/parler-tts.git@d108732cd57788ec86bc857d99a6cabd66663d68" soundfile==0.13.1
tmp/roshan_parler_env/Scripts/python.exe -m pip install --index-url https://download.pytorch.org/whl/cu124 torch==2.6.0+cu124 torchaudio==2.6.0+cu124 torchvision==0.21.0+cu124
tmp/roshan_parler_env/Scripts/python.exe tools/make_roshan_voice_auditions.py --line castle_context
tmp/roshan_parler_env/Scripts/python.exe tools/make_roshan_voice_auditions.py --preset joy_child_spark
tmp/roshan_parler_env/Scripts/python.exe tools/make_roshan_voice_auditions.py --preset joy_child_spark --line urgent --attempt 2 --out assets_src/audio/roshan_voice_auditions_2026-08-31/attempt_2
```
