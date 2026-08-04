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
    "imp":     ("am_puck",   1.38, 1.08),   # giggly mischief imp (opera rivals)
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

    # ---- Pearl Opera career phases (OPERA_2D_REBUILD_2026-08-01) ----
    "roshan_op_chef_imps": ("roshan", "Mischief imps grabbed the spoons! Tap each imp to shoo them off!"),
    "roshan_op_chef_pour": ("roshan", "Hold to pour the sparkling batter!"),
    "roshan_op_chef_stir": ("roshan", "Draw big circles to stir!"),
    "roshan_op_chef_bake": ("roshan", "Tap when the oven marker is green!"),
    "roshan_op_chef_cake_chase": ("roshan", "The imp captain snatched the cake! Bop the crew to the stage door!"),
    "roshan_op_chef_pipe": ("roshan", "On stage! Swipe to pipe the frosting!"),
    "roshan_op_chef_top": ("roshan", "Tap the bright toppings and win the cake back!"),
    "roshan_op_detective_imps": ("roshan", "Imps scattered the clue boxes! Tap each imp!"),
    "roshan_op_detective_peek": ("roshan", "Hold the magnifier over the glowing clue!"),
    "roshan_op_detective_trail": ("roshan", "Swipe along the footprint trail!"),
    "roshan_op_detective_clues": ("roshan", "Tap every glowing clue you find!"),
    "roshan_op_detective_tiara_chase": ("roshan", "The imp captain ran off with the tiara case! Bop the lookouts!"),
    "roshan_op_detective_match": ("roshan", "Match each clue to the glowing place!"),
    "roshan_op_detective_name": ("roshan", "Tap when the spotlight shines on the answer!"),
    "roshan_op_ballerina_imps": ("roshan", "Imps are bouncing on the recital tiles! Tap them gently off!"),
    "roshan_op_ballerina_watch": ("roshan", "Hold still and watch the glowing dance!"),
    "roshan_op_ballerina_steps": ("roshan", "Tap the glowing dance step!"),
    "roshan_op_ballerina_ribbon": ("roshan", "Trace the ribbon across the floor!"),
    "roshan_op_ballerina_ribbon_chase": ("roshan", "The imp captain tangled the ribbons! Twirl-bop the crew!"),
    "roshan_op_ballerina_duet": ("roshan", "Step on the beat , tap in the green!"),
    "roshan_op_ballerina_twirl": ("roshan", "Draw circles for the grand twirl!"),
    "roshan_op_candymaker_imps": ("roshan", "Imps are juggling the gumdrops! Tap each imp!"),
    "roshan_op_candymaker_syrup": ("roshan", "Hold the sparkling syrup bottle!"),
    "roshan_op_candymaker_sort": ("roshan", "Tap the glowing candy chute!"),
    "roshan_op_candymaker_wrap": ("roshan", "Twist the wrappers in circles!"),
    "roshan_op_candymaker_candy_chase": ("roshan", "The imp captain rolled away the candy cart! Bop the crew!"),
    "roshan_op_candymaker_parade": ("roshan", "Tap when the parade cart is in the green!"),
    "roshan_op_candymaker_share": ("roshan", "Tap a candy for every friend in the crowd!"),
    "roshan_op_doctor_imps": ("roshan", "Imps are hiding the bandages! Tap each imp!"),
    "roshan_op_doctor_wash": ("roshan", "Hold to wash Doctor Roshan's hands!"),
    "roshan_op_doctor_find": ("roshan", "Find the plushy with the glowing ouch!"),
    "roshan_op_doctor_x_ray": ("roshan", "Tap the glowing cracked bone!"),
    "roshan_op_doctor_plushy_chase": ("roshan", "The imp captain borrowed the plushy patient! Bop the crew to the stage!"),
    "roshan_op_doctor_cast": ("roshan", "Draw circles to wrap the soft cast!"),
    "roshan_op_doctor_bandage": ("roshan", "Swipe the stretchy bandage around!"),
    "roshan_op_farmer_imps": ("roshan", "Imps are splashing in the mud! Tap each imp!"),
    "roshan_op_farmer_plant": ("roshan", "Tap the glowing garden row and plant the seed!"),
    "roshan_op_farmer_feed": ("roshan", "Tap when the veggie reaches a piggy!"),
    "roshan_op_farmer_mud_hop": ("roshan", "Hold to wind up... and make a big mud hop!"),
    "roshan_op_farmer_piggy_chase": ("roshan", "The imp captain opened the piggy gate! Bop the crew!"),
    "roshan_op_farmer_herd": ("roshan", "Sweep back and forth to guide the herd on stage!"),
    "roshan_op_farmer_picnic": ("roshan", "Tap a snack for every happy piggy!"),
    "roshan_op_boxer_spar": ("roshan", "Friendly sparring! Bop each padded imp!"),
    "roshan_op_boxer_jab": ("roshan", "Tap in the green to punch the padded gloves!"),
    "roshan_op_boxer_duck": ("roshan", "Swipe down to duck the friendly counter!"),
    "roshan_op_boxer_bell_chase": ("roshan", "The imp captain grabbed the championship belt and rang the big bell! Win it back in the title match!"),
    "roshan_op_boxer_round": ("roshan", "Punch the glowing pad , left, middle, right!"),
    "roshan_op_boxer_belt": ("roshan", "Tap the championship belt for the winner!"),
    "roshan_op_magician_imps": ("roshan", "Imps popped out of the magic hats! Tap each imp!"),
    "roshan_op_magician_vanish": ("roshan", "Hold the wand to vanish the bunny-fish!"),
    "roshan_op_magician_track": ("roshan", "Follow the glowing hat through the shuffle!"),
    "roshan_op_magician_rope": ("roshan", "Swipe the magic rope into one long ribbon!"),
    "roshan_op_magician_bunny_chase": ("roshan", "The imp captain hid the bunny-fish! Bop the crew to the stage!"),
    "roshan_op_magician_cabinet": ("roshan", "Tap on the star flashes to open the cabinet!"),
    "roshan_op_magician_portal": ("roshan", "Draw circles to open the giant star portal!"),
    "roshan_op_painter_imps": ("roshan", "Imps splashed the paint pots! Tap each imp!"),
    "roshan_op_painter_sketch": ("roshan", "Trace the sunrise sketch!"),
    "roshan_op_painter_fill": ("roshan", "Hold to fill the glowing shape!"),
    "roshan_op_painter_splat": ("roshan", "Tap five happy splatters!"),
    "roshan_op_painter_sunrise_chase": ("roshan", "The imp captain took the sunrise painting! Bop the crew!"),
    "roshan_op_painter_strokes": ("roshan", "Paint grand circles for the crowd!"),
    "roshan_op_painter_reveal": ("roshan", "Tap the glowing frame to hang the sunrise!"),
    "roshan_op_astronaut_imps": ("roshan", "Imps are floating around the rocket bay! Tap each imp!"),
    "roshan_op_astronaut_pipes": ("roshan", "Tap the glowing pipe to route the bubbles!"),
    "roshan_op_astronaut_patch": ("roshan", "Tap the sparkle leaks to patch them!"),
    "roshan_op_astronaut_valve": ("roshan", "Draw circles to turn the launch valve!"),
    "roshan_op_astronaut_rocket_chase": ("roshan", "The imp captain scooped up the little rocket and pressed the silly button! Bop the crew!"),
    "roshan_op_astronaut_boost": ("roshan", "Tap the boosters in the green!"),
    "roshan_op_astronaut_launch": ("roshan", "Hold through the countdown... and launch!"),
    "roshan_op_racer_imps": ("roshan", "Imps rolled tires onto the track! Tap each imp!"),
    "roshan_op_racer_steer": ("roshan", "Swipe to steer through the coral gates!"),
    "roshan_op_racer_turbo": ("roshan", "Tap TURBO when the marker hits green!"),
    "roshan_op_racer_trophy_chase": ("roshan", "The imp captain grabbed the shell trophy! Clear the track!"),
    "roshan_op_racer_lap_two": ("roshan", "Loop the loop! Draw big racing circles!"),
    "roshan_op_racer_finish": ("roshan", "Tap the zoom strips and cross the line!"),
    "roshan_op_popstar_imps": ("roshan", "Imps are drumming on the speakers! Tap each imp!"),
    "roshan_op_popstar_sound_check": ("roshan", "Hold the microphone for sound check!"),
    "roshan_op_popstar_dance": ("roshan", "Tap the glowing dance arrow!"),
    "roshan_op_popstar_mic_chase": ("roshan", "The imp captain unplugged the microphone! Bop the mischief band!"),
    "roshan_op_popstar_rhythm": ("roshan", "Tap each rainbow note in the green!"),
    "roshan_op_popstar_encore": ("roshan", "Draw a big encore spin for the crowd!"),
    "roshan_op_detective_lens": ("roshan", "Drag the magic magnifying glass over the stage to find the glowing clues!"),
    "roshan_op_detective_search": ("roshan", "Search the whole stage! Sweep your magnifying glass to find every hidden sparkle!"),

    # ---- Imp apprentice banter, per career (chapter 2) ----
    "imp_op_chef_arrive": ("imp", "I was sent to learn the CAKE. Don't mind me, I'm learning."),
    "imp_op_chef_copy": ("imp", "Flour goes in the bowl... or on my head. Either way!"),
    "imp_op_chef_steal": ("imp", "Mine now! A birthday needs a cake and I HAVE one!"),
    "imp_op_chef_bop": ("imp", "Ow! Fine! It needed more sugar anyway!"),
    "imp_op_candymaker_arrive": ("imp", "I was sent to learn the SWEETS. I am very good at sweets."),
    "imp_op_candymaker_copy": ("imp", "One for the bag, two for me. That's how it works!"),
    "imp_op_candymaker_steal": ("imp", "Candy! Every party needs candy and now WE have it!"),
    "imp_op_candymaker_bop": ("imp", "Oof! My tummy hurts anyway. Too many gumdrops."),
    "imp_op_detective_arrive": ("imp", "I was sent to learn the SEARCHING. Where is everything?"),
    "imp_op_detective_copy": ("imp", "I looked under here. And here. Nothing! Detecting is hard."),
    "imp_op_detective_steal": ("imp", "The sparkly crown! Now everyone will look at ME!"),
    "imp_op_detective_bop": ("imp", "Aww. It didn't even fit on my horns."),
    "imp_op_ballerina_arrive": ("imp", "I was sent to learn the DANCING. Watch my twirl!"),
    "imp_op_ballerina_copy": ("imp", "Spin, spin, spin, FALL. That's the hard part."),
    "imp_op_ballerina_steal": ("imp", "The music box! No music, no party, hee hee!"),
    "imp_op_ballerina_bop": ("imp", "Whoops! I'm dizzy. Dizzy is a kind of dancing."),
    "imp_op_doctor_arrive": ("imp", "I was sent to learn the MENDING. Something of mine is torn too."),
    "imp_op_doctor_copy": ("imp", "Bandage on... bandage off. Bandage on my nose?"),
    "imp_op_doctor_steal": ("imp", "I'm taking the patient! He likes me better!"),
    "imp_op_doctor_bop": ("imp", "Ouch! Can you fix ME after?"),
    "imp_op_farmer_arrive": ("imp", "I was sent to learn the FEEDING. What do piggies even eat?"),
    "imp_op_farmer_copy": ("imp", "I planted a rock. Nothing grew. Farming is tricky!"),
    "imp_op_farmer_steal": ("imp", "Snack time! This picnic is OUR picnic now!"),
    "imp_op_farmer_bop": ("imp", "Blegh! I got mud in my mouth."),
    "imp_op_boxer_arrive": ("imp", "I was sent to learn the BOUNCING. Put 'em up!"),
    "imp_op_boxer_copy": ("imp", "Left! Right! ...which one is left again?"),
    "imp_op_boxer_steal": ("imp", "The shiny belt! Champions get invited to things!"),
    "imp_op_boxer_bop": ("imp", "Good one! Best two out of three? No? Okay."),
    "imp_op_magician_arrive": ("imp", "I was sent to learn the MAGIC. Abraca-... something."),
    "imp_op_magician_copy": ("imp", "I made it disappear! ...where did it go? Uh oh."),
    "imp_op_magician_steal": ("imp", "Now you see the show, now you DON'T!"),
    "imp_op_magician_bop": ("imp", "Ta-daa! That was supposed to happen. Really."),
    "imp_op_painter_arrive": ("imp", "I was sent to learn the DECORATING. Ours is very grey."),
    "imp_op_painter_copy": ("imp", "I painted my hands. And the wall. And a bit of the floor."),
    "imp_op_painter_steal": ("imp", "Pretty colours! Our party needs pretty too!"),
    "imp_op_painter_bop": ("imp", "Bonk! Now I'm a different colour."),
    "imp_op_astronaut_arrive": ("imp", "I was sent to learn the SENDING. Nobody sends US anything."),
    "imp_op_astronaut_copy": ("imp", "My rocket went sideways. Into a wall. Twice."),
    "imp_op_astronaut_steal": ("imp", "No invitations, no guests! Hee hee hee!"),
    "imp_op_astronaut_bop": ("imp", "Wheee — oh. I landed. That's the hard bit."),
    "imp_op_racer_arrive": ("imp", "I was sent to learn the FAST. I am already fast!"),
    "imp_op_racer_copy": ("imp", "Whoa whoa WHOA — how do you stop this thing?"),
    "imp_op_racer_steal": ("imp", "Catch me! You won't! ...you might!"),
    "imp_op_racer_bop": ("imp", "Pit stop! Pit stop! I need a pit stop!"),
    "imp_op_popstar_arrive": ("imp", "I was sent to learn the SINGING. LA LAAAA!"),
    "imp_op_popstar_copy": ("imp", "Was that the right note? It felt like a note."),
    "imp_op_popstar_steal": ("imp", "No microphone, no singing! Our band is better anyway!"),
    "imp_op_popstar_bop": ("imp", "My ears! Okay okay, you sing it."),
    "imp_op_nursery_arrive": ("imp", "I was sent to learn the QUIET. I am bad at quiet."),
    "imp_op_nursery_copy": ("imp", "Shhh. Shhhh. SHHH— sorry. Sorry."),
    "imp_op_nursery_steal": ("imp", "The star mobile! Ours is just a sock on a string!"),
    "imp_op_nursery_bop": ("imp", "Sorry! Was that too loud? Was it?"),

    # ---- Roshan's in-theme working lines ----
    "roshan_op_chef_work": ("roshan", "Mixing, mixing! It's getting all smooth and creamy!"),
    "roshan_op_candymaker_work": ("roshan", "Sticky sweet! One bag for every single friend!"),
    "roshan_op_detective_work": ("roshan", "A clue! Right there, hiding where nobody looked!"),
    "roshan_op_ballerina_work": ("roshan", "Round and round — my ribbon is drawing circles!"),
    "roshan_op_doctor_work": ("roshan", "There, there. All better, all wrapped up soft!"),
    "roshan_op_farmer_work": ("roshan", "Munch munch! Look how happy they are!"),
    "roshan_op_boxer_work": ("roshan", "Bounce and duck! I'm getting good at this!"),
    "roshan_op_magician_work": ("roshan", "Watch closely... and TA-DAA!"),
    "roshan_op_painter_work": ("roshan", "Big swishy stripes! The whole hall is turning pretty!"),
    "roshan_op_astronaut_work": ("roshan", "Bubbles up! Off you go, find my friends!"),
    "roshan_op_racer_work": ("roshan", "Zoom! Round the corner and away!"),
    "roshan_op_popstar_work": ("roshan", "Testing, testing — everybody can hear me now!"),
    "roshan_op_nursery_work": ("roshan", "Shhh, little one. Snuggle down, it's sleepy time."),
    "imp_op_captain": ("imp", "Hee hee! You will have to bop ME twice!"),
    "roshan_op_nursery_imps": ("roshan", "Mischief imps are tickling the babies awake! Tap each imp!"),
    "roshan_op_nursery_wash": ("roshan", "Nursery Nurse Roshan! Hold the bubbly basin to wash your hands first!"),
    "faron_op_nursery_catch": ("faron", "Slide the soft cradle under five falling babies! Pillows keep every miss safe."),
    "faron_op_nursery_feed": ("faron", "Hold the warm bottle while Roshan and Faron feed every baby!"),
    "roshan_op_nursery_baby_chase": ("roshan", "The imp captain is playing peek-a-boo with the babies! Bop the crew to the stage!"),
    "roshan_op_nursery_burp": ("roshan", "Tap in the green for gentle burp-pats!"),
    "faron_op_nursery_bedtime": ("faron", "Swipe the blankets down and tuck every sleepy baby into bed!"),
    "faron_miss": ("faron", "Whoopsie! The pillow caught the baby. Try again!"),
    "imp_op_retry": ("imp", "I found it first! Watch the glowing answer, then solve the same mystery with your sparkle memory!"),
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
