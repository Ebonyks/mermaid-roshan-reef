#!/usr/bin/env python3
"""make_voices.py — generate the game's character voice lines with Kokoro TTS.

Kokoro-82M is a free (Apache-2.0) neural TTS that runs on CPU — the same
class of model behind the "TikTok voice" style narration, and noticeably
better than it for clean speech. This script renders every scripted line
with a distinct per-character voice, pitch-shifts kids/creatures up,
trims silence, normalises to the project standard (-16 LUFS, -1.5 dBTP)
and writes game-ready .ogg files into assets/audio/voices/.

FAMILY RECORDINGS ARE SACRED: daddy*.ogg, chuck*.ogg and voice_yay.mp3
are real recordings and are never touched by this script.

Setup (once):
    pip install kokoro-onnx soundfile
    mkdir -p tools/kokoro && cd tools/kokoro
    # model + voices from the onnx-community mirror on Hugging Face:
    curl -L -o model.onnx  https://huggingface.co/onnx-community/Kokoro-82M-v1.0-ONNX/resolve/main/onnx/model.onnx
    for v in af_heart af_bella af_sarah af_sky af_nicole bf_emma bf_lily am_michael bm_george am_puck am_santa; do
        curl -L -o $v.bin https://huggingface.co/onnx-community/Kokoro-82M-v1.0-ONNX/resolve/main/voices/$v.bin
    done

Run:
    python3 tools/make_voices.py                 # all lines
    python3 tools/make_voices.py --only roshan   # one character
    python3 tools/make_voices.py --kokoro /path/to/model/dir
"""
import argparse, json, os, subprocess, sys, tempfile

# character -> (kokoro voice, pitch factor, speed). Pitch >1 = higher/younger.
CHARS = {
    "roshan":  ("af_heart",  1.24, 1.02),   # ONE consistent 4-6yo girl voice
    "huluu":   ("bf_emma",   1.10, 0.98),   # gentle British princess
    "evie":    ("af_bella",  1.30, 1.06),   # little kid + giggle energy
    "harper":  ("af_sarah",  1.18, 1.04),   # big-sister cheer
    "faron":   ("af_nicole", 1.05, 0.96),   # soft, hushed caregiver
    "wacky":   ("am_santa",  0.98, 0.97),   # grandpa chuckle
    "shop":    ("bm_george", 1.02, 1.00),   # friendly shopkeeper
    "sparkle": ("af_bella",  1.55, 1.12),   # tiny baby-eagle chirp
    "rosalina": ("bf_lily",  1.12, 0.97),   # dreamy keeper of the Butterfly World
}

# output name (without .ogg) -> (character, line text)
LINES = {
    # ---- Roshan (the player) ----
    "roshan_talk":   ("roshan", "This is so much fun!"),
    "roshan_intro1": ("roshan", "Wow! A princess in the sky!"),
    "roshan_intro2": ("roshan", "Oh no! A great big storm!"),
    "roshan_intro3": ("roshan", "Don't worry, Princess Huluu! I'll help you!"),
    "roshan_intro4": ("roshan", "Come on! Let's go!"),
    "roshan_whale":  ("roshan", "Woooow! A giant whale!"),
    "roshan_ship":   ("roshan", "Ooh! What's inside?"),
    "roshan_wreck":  ("roshan", "Treasure! Let's peek inside!"),
    "roshan_pearl":  ("roshan", "A rainbow pearl!"),
    "roshan_pearl2": ("roshan", "Ooh! Sparkly!"),
    "roshan_pearl3": ("roshan", "Got it!"),
    "roshan_win":    ("roshan", "Yay! I did it!"),
    "roshan_fail":   ("roshan", "Aww... let's try again!"),
    "roshan_idle1":  ("roshan", "La la la, dee dum."),
    "roshan_idle2":  ("roshan", "I love swimming!"),
    "roshan_idle3":  ("roshan", "It's so pretty down here!"),
    "roshan_beans":  ("roshan", "Beans, beans! Toot toot! Wheee!"),
    "roshan_hungry": ("roshan", "I sure am hungry... I bet I'd be faster after a good meal!"),
    "roshan_bump":   ("roshan", "Whoooaa! Bumper cars!"),
    "roshan_oops":   ("roshan", "Oopsie!"),
    # ---- Princess Huluu ----
    "huluu":        ("huluu", "Hello, Mermaid Roshan!"),
    "huluu_greet":  ("huluu", "Welcome to my castle, Mermaid Roshan!"),
    "huluu_intro":  ("huluu", "Please help me, brave little mermaid!"),
    "huluu_talk":   ("huluu", "You are my very best friend."),
    "huluu_thanks": ("huluu", "Thank you, Mermaid Roshan! You did a great job!"),
    "huluu_win":    ("huluu", "Hooray! You did it! This is now your castle!"),
    "huluu_hero":   ("huluu", "You saved Rosalina's butterflies? You're a HERO, Mermaid Roshan!"),
    # ---- reef friends ----
    "evie":       ("evie", "Tee hee! You found us! Let's play hide and seek!"),
    "evie_win":   ("evie", "You found Lamb-a' every time! Yay!"),
    "evie_fail":  ("evie", "Aww, Lamb-a' got away! Let's try again!"),
    "harper":     ("harper", "Come slide with us! Grab the fishies!"),
    "harper_win": ("harper", "Wheee! That was amazing!"),
    "faron":      ("faron", "Shhh... the babies are getting sleepy."),
    "faron_win":  ("faron", "All the babies are tucked in! Thank you!"),
    "faron_fail": ("faron", "Oh no, the babies! Let's try once more."),
    "faron_miss": ("faron", "Oh NO! The baby! Catch them, catch them!"),
    "wacky":      ("wacky", "Ho ho! Hello there, little mermaid!"),
    "wacky_win":  ("wacky", "Great throwing! Chuck says woof! Ho ho ho!"),
    "wacky_fail": ("wacky", "Ho ho! Chuck got all wet! Try again!"),
    "wacky_splash": ("wacky", "OH NO! Chuck is all WET! Shake shake shake, big fella!"),
    "shop":       ("shop", "Welcome, welcome! Have a look around!"),
    "sparkle":    ("sparkle", "Cheep cheep! Cheep!"),
    # ---- Mermaid Rosalina (Butterfly World) ----
    "rosalina":        ("rosalina", "Welcome to the Butterfly World, little star."),
    "rosalina_greet":  ("rosalina", "My baby butterflies all escaped! Bring all seven home, and I will open my castle for you!"),
    "rosalina_locked": ("rosalina", "Not yet, little star! Please find all seven of my butterflies first!"),
    "rosalina_open":   ("rosalina", "You found them ALL! My castle is open. Come in, come in!"),
    "rosalina_win":    ("rosalina", "You saved the Butterfly World! Fairy Roshan is yours now!"),
}

# "everyone" = three friends cheering together (mixed after generation)
EVERYONE = [("roshan", "Hooray!"), ("huluu", "Hooray!"), ("evie", "Hooray!!")]

SR = 24000
TARGET_LUFS = -16.0


def ff(*args):
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *args], check=True)


def measure_lufs(path):
    r = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", path, "-af",
         "loudnorm=I=-16:TP=-1.5:print_format=json", "-f", "null", "-"],
        capture_output=True, text=True)
    j = json.loads(r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1])
    return float(j["input_i"])


def polish(wav_in, ogg_out, pitch):
    """pitch-shift, trim edge silence, normalise to -16 LUFS / -1.5 dBTP, encode ogg"""
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as t:
        tmp = t.name
    chain = (
        f"asetrate={SR}*{pitch},aresample=48000,atempo={1.0/pitch:.6f},"
        "silenceremove=start_periods=1:start_threshold=-45dB,"
        "areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse"
    )
    ff("-i", wav_in, "-af", chain, tmp)
    gain = TARGET_LUFS - measure_lufs(tmp)
    ff("-i", tmp, "-af", f"volume={gain:.2f}dB,alimiter=limit=0.84:level=false",
       "-c:a", "libvorbis", "-q:a", "5", ogg_out)
    os.unlink(tmp)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kokoro", default=os.path.join(os.path.dirname(__file__), "kokoro"))
    ap.add_argument("--out", default=os.path.join(os.path.dirname(__file__), "..", "assets", "audio", "voices"))
    ap.add_argument("--only", default="")
    args = ap.parse_args()

    import numpy as np
    import onnxruntime as ort
    import soundfile as sf
    from kokoro_onnx.tokenizer import Tokenizer

    model = os.path.join(args.kokoro, "model.onnx")
    packed = os.path.join(args.kokoro, "voices.bin")
    if not os.path.exists(packed):
        import glob
        vs = {os.path.basename(f)[:-4]: np.fromfile(f, dtype=np.float32).reshape(510, 1, 256)
              for f in glob.glob(os.path.join(args.kokoro, "*.bin"))
              if not f.endswith("voices.bin")}
        np.savez(packed[:-4] + "_pack", **vs)
        os.rename(packed[:-4] + "_pack.npz", packed)
    sess = ort.InferenceSession(model)
    voices = np.load(packed)
    tok = Tokenizer()

    def tts(char, text, wav_path):
        vname, _pitch, speed = CHARS[char]
        ph = tok.phonemize(text, lang="en-us" if not vname.startswith("b") else "en-gb")
        # Her name is ro-SHAHN, not ROSH-in — fix at the phoneme layer so it
        # holds for every voice and any spelling in the display text
        ph = ph.replace("ɹˈɑːʃən", "ɹoʊʃˈɑːn").replace("ɹˈɒʃən", "ɹəʊʃˈɑːn")
        ids = tok.tokenize(ph)
        style = voices[vname][len(ids)]
        toks = np.array([[0, *ids, 0]], dtype=np.int64)
        audio = sess.run(None, {"input_ids": toks, "style": style,
                                "speed": np.full(1, speed, dtype=np.float32)})[0]
        sf.write(wav_path, audio.reshape(-1), SR)

    os.makedirs(args.out, exist_ok=True)
    done = 0
    for name, (char, text) in LINES.items():
        if args.only and not name.startswith(args.only):
            continue
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as t:
            raw = t.name
        tts(char, text, raw)
        polish(raw, os.path.join(args.out, name + ".ogg"), CHARS[char][1])
        os.unlink(raw)
        done += 1
        print(f"[ok] {name}.ogg  ({char}: \"{text}\")")

    if not args.only or args.only == "everyone":
        parts = []
        for i, (char, text) in enumerate(EVERYONE):
            with tempfile.NamedTemporaryFile(suffix=f"_{i}.wav", delete=False) as t:
                raw = t.name
            tts(char, text, raw)
            with tempfile.NamedTemporaryFile(suffix=f"_p{i}.wav", delete=False) as t2:
                shifted = t2.name
            p = CHARS[char][1]
            ff("-i", raw, "-af", f"asetrate={SR}*{p},aresample=48000,atempo={1.0/p:.6f}", shifted)
            parts.append(shifted)
            os.unlink(raw)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as t3:
            mixed = t3.name
        ff("-i", parts[0], "-i", parts[1], "-i", parts[2],
           "-filter_complex", "[0][1][2]amix=inputs=3:duration=longest:normalize=0,volume=2.4", mixed)
        polish(mixed, os.path.join(args.out, "everyone.ogg"), 1.0)
        for p2 in parts + [mixed]:
            os.unlink(p2)
        done += 1
        print("[ok] everyone.ogg  (3-voice \"Hooray!\")")
    print(f"done: {done} clips -> {os.path.abspath(args.out)}")


if __name__ == "__main__":
    main()
