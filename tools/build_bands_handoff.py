"""Build the bounded music-video review packet; never claim generation approval."""
from pathlib import Path
import hashlib
import html
import json
import shutil
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "assets_src/cinematics/battle_of_bands_2026-09-20"
OLD = "assets_src/cinematics/chapter2_lawn_scale_v2_2026-09-06"
REFERENCES = {
    "roshan_popstar.png": "assets/opera/worlds/actors/roshan_popstar.png",
    "roshan_costume_poses.png": "assets/opera/worlds/actors/animation/roshan_popstar_sheet_a.png",
    "popstar_stage.png": "assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_stage_master_popstar.png",
    "lawn.png": OLD + "/references/lawn.png",
    "king.png": OLD + "/characters/ember_king_v4.png",
    "prince.png": OLD + "/characters/ember_prince_identity.png",
    "candle.png": OLD + "/references/candle_lit.png",
    "cake.png": OLD + "/references/cake.png",
    "rumi.png": OLD + "/references/rumi_atlas.png",
    "daddy.webp": "assets/characters/friends/daddy.webp",
    "baby_eagle.png": "assets/book/baby_eagle.png",
    "roshan_drums.png": "assets/prototypes/bands/roshan_drums.png",
    "king_guitar.png": "assets/prototypes/bands/king_guitar.png",
    "prince_drums.png": "assets/prototypes/bands/prince_drums.png",
    "daddy_ukulele.png": "assets/prototypes/bands/daddy_ukulele.png",
    "eagle_bass.png": "assets/prototypes/bands/eagle_bass.png",
}
SHOTS = [
    ("The birthday becomes a bandstand", "song introduction", "roshan_popstar.png", "candle.png", "Roshan raises both sticks above her kit on the birthday lawn", "the friends are ready and the single lit candle remains on the cake"),
    ("Roshan finds the groove", "first percussion entrance", "roshan_popstar.png", "candle.png", "Roshan alternates two clear stick contacts on the two toms", "both sticks rebound naturally above the drumheads"),
    ("Daddy on ukulele", "first light string phrase", "daddy.webp", "roshan_popstar.png", "Daddy Mermaid strums his four-string ukulele beside Roshan on drums", "Daddy smiles toward Roshan with his ukulele still held naturally"),
    ("Baby Eagle on bass", "first bass phrase", "baby_eagle.png", "daddy.webp", "Baby Eagle plucks a four-string bass with one wing while the other steadies the neck", "Baby Eagle holds the bass securely, with no human hands or extra wings"),
    ("The King demands a turn", "first King grindcore onset — locate in recording", "king.png", "candle.png", "the King strums his electric lead guitar during one theatrical musical outburst", "the King settles with his guitar and the candle still on the cake"),
    ("A delighted drum reply", "Roshan return after first outburst", "roshan_popstar.png", "candle.png", "Roshan answers with a short tom fill ending on one cymbal contact", "the cymbal gently settles and Roshan smiles"),
    ("The Prince joins in", "Prince grindcore onset — speaker attribution pending recording", "prince.png", "king.png", "the Prince plays a short fill around his absurdly elaborate metal drum kit with exactly two sticks then glances toward Roshan with a shy smile", "the Prince faces Roshan without threatening her"),
    ("The groove belongs to everyone", "next recorded chorus or repeated phrase", "roshan_popstar.png", "daddy.webp", "Roshan keeps time while Daddy strums once in response", "Roshan and Daddy face the same audience"),
    ("The King's last blast", "last King grindcore interruption — locate in recording", "king.png", "candle.png", "the King delivers one final overblown lead-guitar flourish while eyeing the candle", "the King settles his strapped guitar and looks at the candle"),
    ("Roshan finishes successfully", "last Roshan cadence", "roshan_popstar.png", "candle.png", "Roshan lands her final drum hit and raises the sticks in happy relief", "Roshan has visibly finished and the candle is still hers"),
    ("Cheating after the contest", "post-cadence story beat; not a missed player note", "king.png", "candle.png", "the King lifts the single lit rainbow candle from the cake using his royal magic", "the candle is in the King's hand and the intact cake has an empty candle place"),
    ("The Prince objects", "quiet reaction after theft", "prince.png", "king.png", "the Prince reaches one open hand toward his father then lets it fall in disappointment", "the Prince remains beside his father, visibly unhappy with the cheating"),
    ("Together after the music", "closing tail or separate story coda", "roshan_popstar.png", "daddy.webp", "Daddy moves beside Roshan with his ukulele as Roshan lowers her sticks", "Roshan has support; Baby Eagle stays with her and King and Prince have left together with the candle"),
]

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((json.dumps(data, indent=2) + "\n").encode("utf-8"))

def build():
    (PACKET / "references").mkdir(parents=True, exist_ok=True)
    (PACKET / ".gdignore").write_text("", encoding="utf-8")
    sources = {}
    for name, source in {"ART_PROVENANCE.json": "assets_src/imagegen/bands_20260920/PROVENANCE.json", "SOURCE_ASSET_LICENSES.txt": "ASSET_LICENSES.md", "runtime/prototype.png": "build/bands/prototype.png"}.items():
        if (ROOT / source).exists():
            (PACKET / name).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / source, PACKET / name)
            sources[name] = source
    for name, source in REFERENCES.items():
        relative = "references/" + name
        shutil.copyfile(ROOT / source, PACKET / relative)
        sources[relative] = source
    cards = []
    board = []
    contact = Image.new("RGB", (1500, 1750), "#21192e")
    draw = ImageDraw.Draw(contact)
    font_path = next((str(p) for p in [Path("C:/Windows/Fonts/arial.ttf"), Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")] if p.exists()), None)
    font = ImageFont.truetype(font_path, 22) if font_path else ImageFont.load_default()
    small = ImageFont.truetype(font_path, 17) if font_path else ImageFont.load_default()
    musician = {"roshan_popstar.png": "roshan_drums.png", "king.png": "king_guitar.png", "prince.png": "prince_drums.png", "daddy.webp": "daddy_ukulele.png", "baby_eagle.png": "eagle_bass.png"}
    for index, (title, cue, subject, prop, action, end) in enumerate(SHOTS, 1):
        shot = f"BAND-{index:02}"
        folder = PACKET / "shots" / shot
        folder.mkdir(parents=True, exist_ok=True)
        prompt = (f"locked camera on the approved birthday-lawn bandstand from IMAGE_1.\n\n"
                  f"0.0–1.0s: settle in the opening pose.\n1.0–4.0s: {action.lower()}.\n"
                  f"4.0–6.0s: {end}.\n\n"
                  "keep lawn geometry, cake and all unaffected props fixed. preserve the exact subject identity from IMAGE_2, supporting identity from IMAGE_3, and reviewed instrument design from IMAGE_4. "
                  "no hud, no text, no extra limbs or sticks, no duplicate candle, no costume drift, no cuts, no injury.\n"
                  f"end: {end}.\nSound: light instrument/contact foley only; use the owner's existing recording in edit, no generated singing or family voices.\n")
        (folder / "PROMPT.txt").write_bytes(prompt.encode("utf-8"))
        refs = [{"id": "IMAGE_1", "role": "approved_clean_first_frame", "path": None,
                 "human_decision": "pending", "blocking_gap": "Generate and approve this shot's clean full frame; do not bind board or runtime capture."}]
        for number, name in enumerate([subject, prop], 2):
            relative = "references/" + name
            refs.append({"id": f"IMAGE_{number}", "role": "subject_identity" if number == 2 else "object_or_material_identity",
                         "path": relative, "sha256": digest(PACKET / relative), "hud_present": False,
                         "human_decision": "existing source identity; new shot binding pending"})
        instrument = "references/" + musician[subject]
        refs.append({"id": "IMAGE_4", "role": "object_or_material_identity", "path": instrument, "sha256": digest(PACKET / instrument), "hud_present": False, "human_decision": "prototype instrument design; shot binding approval pending"})
        card = {"schema": "imagine-shot-packet-v1", "movie_id": "battle_of_bands", "shot_id": shot,
                "title": title, "status": "DRAFT", "duration_seconds": 6, "aspect_ratio": "16:9",
                "delivery_size": [1280, 720], "mode": "image_to_video", "output_disposition": "motion_reference_only",
                "bound_references": refs, "camera": {"verb": "locked", "move_count": 0},
                "must_move": [action], "must_not_move": ["lawn geometry", "unaffected props"], "end_state": end,
                "negative_constraints": ["no HUD", "no text", "no extra limbs", "no duplicate candle"],
                "prompt_path": f"shots/{shot}/PROMPT.txt", "prompt_sha256": digest(folder / "PROMPT.txt"),
                "editorial_cue": cue, "recording_start_seconds": None, "recording_end_seconds": None,
                "timing_note": "Six seconds is a provisional generation length, NOT a measured song timecode. Split or repeat coverage after listening; do not stretch motion to fill a whole song.",
                "ARCHIVE_COMPLETE": False, "GENERATION_READY": False, "DELIVERY_ACCEPTED": False,
                "blocking_findings": ["recording and cue map missing", "approved clean first frame missing", "per-shot identity/binding review pending"]}
        write_json(folder / "SHOT_PACKET.json", card)
        cards.append(f"shots/{shot}/SHOT_PACKET.json")
        x, y = ((index - 1) % 3) * 500, ((index - 1) // 3) * 350
        draw.rounded_rectangle((x+8,y+8,x+492,y+342),radius=15,fill="#483754")
        draw.text((x+20,y+20), shot + "  " + title, font=font, fill="#fff1cc")
        for offset, name in enumerate([subject, prop]):
            with Image.open(PACKET / "references" / musician.get(name,name)) as im:
                im = im.convert("RGBA")
                im.thumbnail((220,230))
                contact.paste(im,(x+20+offset*240+(220-im.width)//2,y+60+(230-im.height)//2),im)
        draw.text((x+20,y+306),"REFERENCE BOARD / staging + timecodes pending",font=small,fill="#f1dcf2")
        board.append(f'<section><h2>{shot} · {html.escape(title)}</h2><div class="refs"><img src="references/{subject}"><img src="references/{prop}"></div><p>{html.escape(action)}</p><p><b>End:</b> {html.escape(end)}</p><small>{html.escape(cue)}</small></section>')
    (PACKET / "SHOT_BOARD.html").write_text('<!doctype html><meta charset="utf-8"><title>Battle of the Bands — reference shot board</title><style>body{background:#21192e;color:#fff5e8;font:18px system-ui;margin:32px}main{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}section{background:#423452;padding:18px;border-radius:16px}h2{font-size:20px}.refs{display:flex;height:210px;background:#eadfeb;border-radius:12px}.refs img{width:50%;object-fit:contain}small{color:#f3cf86}</style><h1>Battle of the Bands</h1><p>13-shot editorial reference board. Images identify subjects and props; they are not generated staging, bound first frames or delivery pixels. Musical timecodes await the recorded Iko Iko track.</p><main>' + ''.join(board) + '</main>', encoding="utf-8")
    contact.save(PACKET / "SHOT_BOARD.png")
    write_json(PACKET / "IMAGINE_HANDOFF.json", {"schema": "imagine-handoff-v1", "movie_id": "battle_of_bands", "archive_status": "incomplete", "generation_status": "blocked", "delivery_status": "not_accepted", "shot_packets": [], "draft_shot_packets": cards, "shot_board": "SHOT_BOARD.png", "archive_payload_manifest": "ARCHIVE_MANIFEST.json", "blocking_findings": ["Recorded Iko Iko source/cue timing missing", "13 approved clean first frames missing", "Drummer pose and kit acceptance pending", "Remote receipt required"]})
    write_json(PACKET / "AUDIO_CUE_SHEET.json", {"recording_path": None, "recording_sha256": None, "duration_seconds": None, "status": "AWAITING_OWNER_RECORDING_LOCATION", "outburst_cues": [], "cue_contract": "Each measured entry: start_seconds, end_seconds, speaker (king/prince), shot_id, listened_by. Never infer grindcore timing from amplitude alone or invent speaker attribution.", "song_edit": "Keep the exact recorded musical sequence. Reorder/split draft shots to fit it; no invented lyrics or synthesized replacement voices."})
    (PACKET / "START_HERE.txt").write_text("BATTLE OF THE BANDS — GROK REVIEW HANDOFF\nOwner commission 2026-09-20. Roshan is the drummer in her established pop-star costume. Iko Iko is the existing recorded soundtrack. King/Prince grindcore moments follow that recording, not invented timing. Ember King leads with electric guitar; Ember Prince plays the metal drum kit. Daddy Mermaid plays ukulele; Baby Eagle plays bass. Roshan remains the drummer in her own band. The King cheats and takes the rainbow candle after Roshan succeeds. The Prince remains conflicted, not malicious.\n\nOpen SHOT_BOARD.html locally after downloading the packet (GitHub HTML source itself is not a rendered preview). Then open shots/BAND-01 through BAND-13. Each has one draft SHOT_PACKET.json and paste-ready PROMPT.txt. The six-second cards are coverage plans, not a measured 78-second song edit.\n\nREVIEW REQUEST: approve clean first frames showing the existing identities, Roshan with two sticks and no microphone, a coherent kit, the single candle, and the birthday lawn. Never swap instrumental roles: Roshan drums, Daddy ukulele, Baby Eagle bass, Prince comically complicated metal drums with exactly ONE kick drum and the trial Ember-family crowned-flame crest, King lead guitar. Baby Eagle bass must have exactly four strings and four visible tuning pegs. Existing Pop Star stage art is rehearsal/style context only; the story contest remains on the lawn. Never mix its architecture into a lawn shot. Prince visible standing height is 80% of King's.\n\nBLOCKED FOR GENERATION: recording and timecodes, clean first frames, kit/drummer art approval, final bindings. Boards and gameplay captures are non-pixel references. Grok clips are motion/editorial references only; full-frame cinematic delivery evidence is still required. ARCHIVE_COMPLETE, GENERATION_READY and DELIVERY_ACCEPTED are separate claims; consult REMOTE_VERIFICATION.json when present for published-byte evidence.\n\nCODEx: see CODEX_REFINEMENT.txt. Do not substitute the isolated prototype for the production chapter finale without the listed integration work.\n", encoding="utf-8")
    (PACKET / "CODEX_REFINEMENT.txt").write_text("CODEX SCENE REFINEMENT COMMISSION\n\nRead AGENTS.md, master planning/task index, current design rules/ledger, and design/BATTLE_OF_BANDS_2026-09-20.md. Owner's battle-of-bands premise supersedes the earlier stomp/dodge contest direction; theft remains a scripted cheating act AFTER the child's success.\n\nSTART: scenes/battle_of_bands_prototype.tscn; scripts/battle_of_bands_prototype.gd; scripts/probe_battle_of_bands.gd. Launch directly with exact Godot 4.7.2. Existing production mechanics are in opera_career_world_2d.gd (Pop Star) and chapter_two_lawn_finale_2d.gd / chapter_two_ember_encounter.gd (old contest). This prototype deliberately uses a separate save and does not grant career stars.\n\n1. Locate/listen to the exact recorded Iko Iko master; preserve bytes and hash. Fill AUDIO_CUE_SHEET.json with measured King/Prince intervals. Bind an approved non-destructive runtime derivative to recording, set king_outburst_cues and prince_outburst_cues, and review speech/music levels. Never synthesize replacement singing.\n2. Preserve the owner-defined lineup: Roshan drums, Daddy Mermaid ukulele, Baby Eagle bass; Ember Prince metal drums and Ember King lead guitar. Retain the Prince's comically complicated kit with exactly one kick drum and the trial crowned-flame Ember crest. Baby Eagle bass must retain exactly four strings, four string posts and four tuning pegs. All five new cutouts remain review candidates. Refine approved Pop Star costume into readable drummer hand/contact poses, remove the microphone from those poses, preserve face/tail/costume. Separate approved kit cards with target regions exactly over heads/cymbal; no duplicated baked kit plus procedural overlay. Review hit/contact/rebound at 30 fps and phone size.\n3. Turn the Pop Star rehearsal and lawn finale into a bounded shared drumming component. Reuse large one-finger echo/choice grammar; permit unlimited listening and retries, no compulsory beat-perfect timing. Wrong/passive input cannot finish; performance cues alone cannot take the candle.\n4. Migrate production state through ReefMain/SaveState additively. Preserve prior preparation/candle/completed-round saves; map existing successful challenge to already-completed music, not replay debt. Keep earned cake/friends/career rewards. Persist intentional milestones and restore correct candle owner.\n5. Add exact _say objective lines and diegetic pointers; missing cue is an acceptance blocker. Implement Back, pause, second-finger ownership, touch/mouse deduplication, lifecycle cleanup and music resume. Route from Opera Hall and the chapter's existing lawn entry, with return to the original room.\n6. Replace old stomp dialogue/telegraphs only within the commissioned contest; King cheats, Prince objects and leaves with him, friends support Roshan. No new boss, health bar, lost rewards or chapter-three retcon.\n7. Verify passive, wrong, held, rapid duplicate and second-finger input, save/load each beat, already-completed legacy saves, pause/background/Back/reentry, sibling Pop Star career rewards and full CI. Capture rehearsal, drumming/contact, each recorded outburst, earned success, theft and hopeful return in Mobile on exact candidate. Then target device/child/owner review.\n\nCINEMATIC LIMIT: gameplay sprites and captures are not cinematic frames. Follow shot cards, full-frame provenance and human gates separately. Missing recording/first-frame approval blocks dependent work only. Publish every handoff revision and verify anonymous recipient access and bytes.\n", encoding="utf-8")
    (PACKET / "README.md").write_text("# Battle of the Bands — review handoff\n\nOwner lineup: **Roshan — drums; Daddy Mermaid — ukulele; Baby Eagle — bass; Ember Prince — enormous metal kit with one kick; Ember King — lead guitar.** The crowned-flame Ember emblem is a trial design.\n\n[Start here](START_HERE.txt) · [Codex refinement handoff](CODEX_REFINEMENT.txt) · [Audio cue sheet](AUDIO_CUE_SHEET.json) · [Archive manifest](ARCHIVE_MANIFEST.json)\n\n![Thirteen-shot reference board](SHOT_BOARD.png)\n\nThese are reference thumbnails, not cinematic staging or generation first frames. Read the [detailed board](SHOT_BOARD.html) after downloading the packet.\n\n" + "\n".join(f"- [{Path(c).parent.name} — {SHOTS[i][0]}]({c}) · [Prompt](shots/{Path(c).parent.name}/PROMPT.txt)" for i,c in enumerate(cards)) + "\n\n![Mobile prototype diagnostic](runtime/prototype.png)\n\n**Generation blocked:** exact recording/timecodes, approved clean first frames, final bindings and review. The six-second shots are provisional coverage, not the song duration. Grok clips remain motion/editorial references. Runtime capture is a seam reference and must never be bound as generation pixels. Archive completeness, generation readiness and cinematic delivery acceptance remain separate. The production finale is not replaced by this isolated prototype.\n", encoding="utf-8")
    # Git transports text as LF; hash the same canonical bytes recipients fetch.
    for text_path in PACKET.rglob("*"):
        if text_path.is_file() and text_path.suffix in {".json", ".txt", ".md", ".html"}:
            text_path.write_bytes(text_path.read_bytes().replace(b"\r\n", b"\n"))
    files = []
    for path in sorted(PACKET.rglob('*'), key=lambda item: item.relative_to(PACKET).as_posix()):
        if not path.is_file() or path.name in {"ARCHIVE_MANIFEST.json", "REMOTE_VERIFICATION.json"}:
            continue
        relative = path.relative_to(PACKET).as_posix()
        entry = {"path": relative, "sha256": digest(path), "source_path": sources.get(relative, "project-authored:" + path.relative_to(ROOT).as_posix()), "role": "runtime_seam_reference_never_generation_pixels" if relative.startswith("runtime/") else ("identity_or_location_reference" if relative in sources else "review_planning_not_delivery"), "license_provenance": "Project-owned source; existing source license retained; see packet SOURCE_ASSET_LICENSES.txt", "modification_status": ("UTF-8 LF-normalized reference copy" if path.suffix in {".json", ".txt"} else "byte-identical copy") if relative in sources else "new planning artifact", "dimensions": None}
        if path.suffix.lower() in {'.png', '.jpg', '.webp'}:
            with Image.open(path) as im:
                entry['dimensions'] = list(im.size)
        files.append(entry)
    payload = ''.join(f"{e['sha256']}  {e['path']}\n" for e in files).encode()
    write_json(PACKET / "ARCHIVE_MANIFEST.json", {"schema": "bands-review-archive-v1", "payload_algorithm": "sha256 of sorted sha256 + two spaces + path + LF, excluding manifest and remote receipt", "packet_payload_sha256": hashlib.sha256(payload).hexdigest(), "ARCHIVE_COMPLETE": False, "GENERATION_READY": False, "DELIVERY_ACCEPTED": False, "files": files})

if __name__ == '__main__':
    build()
