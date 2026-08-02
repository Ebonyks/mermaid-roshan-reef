#!/usr/bin/env python3
"""audit_audio_usage.py — map every audio file to the code that plays it.

Audio in this game is never referenced by filename. `AudioDirector._say()`
composes voice paths at runtime from a (speaker, event) pair, and
`_play_music()` composes music paths from a track name:

    voices/<speaker>_<event>.ogg   preferred
    voices/<speaker>.ogg           fallback when the exact line is missing
    music/<track>.ogg              (+ world -> world_night at night)

So `grep daddy1.ogg` finds nothing, and a naive reference scan reports ~94%
of the audio library as dead. This script resolves the real vocabulary
instead: it parses every `_say()`, `show_msg()` and `_play_music()` call in
scripts/, applies `_speaker_key()`, expands array-literal event picks, and
labels each file on disk.

Reached at runtime
  USED-EXACT     a call site resolves to this exact file
  USED-FALLBACK  no exact line exists, so `_say` falls back to this
                 speaker's base clip
  USED-DIRECT    loaded by an explicit res:// path (sfx, ambience, UI)
  DYNAMIC-ONLY   only reachable through a call site whose speaker or event
                 is a runtime variable (needs eyes, never auto-delete)
  PROBE-ONLY     loaded by a probe but never by the running game

Not reached — each cause needs a different fix, so they are labelled apart
rather than lumped into one "unused" bucket:
  UNREACHABLE-NAMING   the clip exists but its filename cannot be built by
                       `<speaker>` or `<speaker>_<event>`. A rename makes it
                       audible; deleting it throws away a working recording.
  UNREACHABLE-SPEAKER  no call site can produce that speaker key at all —
                       `_speaker_key` shadowing, or a character missing from
                       the roster. A code fix makes the whole set audible.
  UNUSED-LINE          a recorded line no call site asks for.
  UNUSED-FALLBACK      base clip never needed, because every requested line
                       for that speaker has its own exact recording. Still
                       worth keeping as the safety net for future lines.
  UNUSED-TRACK         music with no `_play_music()` caller.
  UNUSED-SFX           an sfx path nothing loads.

It also reports MISSING keys: lines the game asks for that have no
recording, which today fall back to a pitched "yay". Those are the
recording opportunities, not deletion candidates.

Nothing here is a delete list. Voice recordings are irreplaceable family
audio (CLAUDE.md); "not currently reachable" is far more often a naming or
routing bug than a dead asset — see the two live examples in AUDIO_AUDIT.md.

Usage:  python3 tools/audit_audio_usage.py [--json out.json]
Exit code is always 0 — this is a report, not a gate.
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "scripts")
AUDIO = os.path.join(ROOT, "assets", "audio")
VOICES = os.path.join(AUDIO, "voices")
MUSIC = os.path.join(AUDIO, "music")

# Mirrors AudioDirector._speaker_key(). Order matters — first hit wins.
SPEAKER_RULES = [
    ("rosalina", "rosalina"), ("roshan", "roshan"), ("huluu", "huluu"),
    ("evie", "evie"), ("lamb", "evie"),
    ("harper", "harper"), ("fiona", "harper"),
    ("faron", "faron"), ("daddy", "daddy"), ("chuck", "chuck"),
    ("wacky", "wacky"), ("shop", "shop"),
    ("sparkle", "sparkle"), ("eagle", "sparkle"),
    ("mewsha", "mewsha"), ("kitty", "mewsha"),
    ("everyone", "everyone"), ("imp", "imp"),
]
SPEAKER_DEFAULT = "roshan"


def speaker_key(who: str) -> str:
    w = who.lower()
    for needle, key in SPEAKER_RULES:
        if needle in w:
            return key
    return SPEAKER_DEFAULT


def split_args(text: str):
    """Split a call's argument list on top-level commas.

    GDScript arguments here contain nested calls, array literals, dictionary
    lookups, format operators and quoted commas, so a naive split(',') is
    wrong. Returns None if the parens never balance (truncated line).
    """
    args, depth, buf, quote, esc = [], 0, [], None, False
    for ch in text:
        if esc:
            buf.append(ch)
            esc = False
            continue
        if quote:
            buf.append(ch)
            if ch == "\\":
                esc = True
            elif ch == quote:
                quote = None
            continue
        if ch in "\"'":
            quote = ch
            buf.append(ch)
            continue
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            if depth == 0:
                args.append("".join(buf).strip())
                return args
            depth -= 1
        if ch == "," and depth == 0:
            args.append("".join(buf).strip())
            buf = []
            continue
        buf.append(ch)
    return None


STR_RE = re.compile(r'^"([^"\\]*)"$')
ARRAY_RE = re.compile(r'^\[(.*)\]', re.S)


def literal_values(arg: str):
    """Resolve an argument to the set of literal strings it can be.

    Returns (values, is_dynamic). A bare string literal yields one value; an
    array literal of string literals yields all of them (call sites index
    these randomly, so every element is reachable); anything else is dynamic.
    """
    if arg is None:
        return set(), True
    arg = arg.strip()
    m = STR_RE.match(arg)
    if m:
        return {m.group(1)}, False
    m = ARRAY_RE.match(arg)
    if m:
        inner = split_args(m.group(1) + ")")
        if inner is not None:
            vals, dyn = set(), False
            for piece in inner:
                sm = STR_RE.match(piece.strip())
                if sm:
                    vals.add(sm.group(1))
                elif piece.strip():
                    dyn = True
            if vals:
                return vals, dyn
    # String(x.get("label", "Roshan")) — the default is a usable hint
    if arg.startswith("String(") or ".get(" in arg:
        hints = re.findall(r'"([^"\\]*)"', arg)
        if hints:
            return {hints[-1]}, True
    return set(), True


KNOWN_SPEAKERS = {k for _n, k in SPEAKER_RULES} | {SPEAKER_DEFAULT}
_NUMBERED = re.compile(r"^([a-z]+)(\d+)$")


def _why_unreachable(stem, reachable, known):
    """Split ORPHAN into the four cases that need different fixes.

    UNREACHABLE-NAMING    the clip exists but its filename cannot be built by
                          `<speaker>` or `<speaker>_<event>` — e.g. daddy1.ogg,
                          where the speaker key is `daddy` and no call site
                          ever asks for event "1". A rename makes it audible.
    UNREACHABLE-SPEAKER   no call site can ever produce this speaker key, so
                          nothing under it can play. Usually `_speaker_key`
                          shadowing or a character absent from the roster.
    UNUSED-FALLBACK       base clip that is never needed because every line
                          the code asks for has its own exact recording.
    UNUSED-LINE           a recorded line no call site requests.
    """
    m = _NUMBERED.match(stem)
    if m and m.group(1) in known:
        return ("UNREACHABLE-NAMING",
                [f"speaker '{m.group(1)}' is reachable; '{stem}' is not a "
                 f"<speaker> or <speaker>_<event> name"])
    sp = stem.split("_")[0]
    if sp not in reachable:
        return ("UNREACHABLE-SPEAKER",
                [f"no call site resolves to speaker '{sp}'"])
    if "_" not in stem:
        return ("UNUSED-FALLBACK",
                ["every requested line for this speaker has its own clip"])
    return ("UNUSED-LINE", [f"no call site asks for '{stem}'"])


def _direct_label(sites):
    """A file only a probe loads is not reached by the running game."""
    if all("(probe only)" in s for s in sites):
        return ("PROBE-ONLY", sites[:4])
    return ("USED-DIRECT", [s for s in sites if "(probe only)" not in s][:4])


def find_calls(name: str):
    """Yield (file, lineno, [args]) for every call to `name` in scripts/."""
    pat = re.compile(r'\b' + re.escape(name) + r'\(')
    for dirpath, _dirs, files in os.walk(SCRIPTS):
        for fn in sorted(files):
            if not fn.endswith(".gd"):
                continue
            path = os.path.join(dirpath, fn)
            with open(path, encoding="utf-8", errors="replace") as fh:
                text = fh.read()
            lines = text.splitlines()
            for m in pat.finditer(text):
                lineno = text.count("\n", 0, m.start()) + 1
                # allow a call to span a few lines (array literals wrap)
                chunk = "\n".join(lines[lineno - 1:lineno + 4])
                off = chunk.find(name + "(") + len(name) + 1
                args = split_args(chunk[off:])
                if args is None:
                    continue
                rel = os.path.relpath(path, ROOT)
                yield rel, lineno, args


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", help="also write the full report as JSON")
    args_ns = ap.parse_args()

    # key -> list of "file:line" ; also track which speakers appear at all
    wanted = defaultdict(list)          # "<speaker>_<event>" or "<speaker>"
    dynamic_speakers = defaultdict(list)
    tracks = defaultdict(list)
    notes = []
    deferred_who = []   # show_msg sites whose speaker resolves from the roster

    # ---- _say(speaker, event, min_gap) -------------------------------------
    for rel, line, a in find_calls("_say"):
        if not a or rel.endswith("audio_director.gd") and line < 40:
            continue
        speakers, sp_dyn = literal_values(a[0])
        events, ev_dyn = literal_values(a[1] if len(a) > 1 else '""')
        if len(a) == 1:
            events, ev_dyn = {""}, False
        site = f"{rel}:{line}"
        if sp_dyn and not speakers:
            notes.append((site, "dynamic speaker", a[0][:60]))
            continue
        for sp in speakers:
            if ev_dyn and not events:
                dynamic_speakers[sp].append(site)
                continue
            for ev in events:
                wanted[f"{sp}_{ev}" if ev else sp].append(site)
            if ev_dyn:
                dynamic_speakers[sp].append(site)

    # ---- show_msg(who, txt, vo="talk") -> _say(_speaker_key(who), vo) -------
    for rel, line, a in find_calls("show_msg"):
        if not a or "audio_director.gd" in rel:
            continue
        whos, who_dyn = literal_values(a[0])
        vos, vo_dyn = literal_values(a[2] if len(a) > 2 else '"talk"')
        if len(a) <= 2:
            vos, vo_dyn = {"talk"}, False
        site = f"{rel}:{line}"
        keys = {speaker_key(w) for w in whos}
        if who_dyn:
            # `fr["fname"]` and friends: the speaker comes from the roster at
            # runtime, so every roster name is reachable here. Deferred until
            # the roster has been harvested below.
            deferred_who.append((site, vos, vo_dyn, a[0][:60]))
            if not keys:
                continue
        if not keys:
            keys = {SPEAKER_DEFAULT}
            notes.append((site, "dynamic who -> defaults to roshan", a[0][:60]))
        for sp in keys:
            if vo_dyn and not vos:
                dynamic_speakers[sp].append(site)
                continue
            for vo in vos:
                wanted[f"{sp}_{vo}" if vo else sp].append(site)
            if vo_dyn:
                dynamic_speakers[sp].append(site)

    # ---- friend roster: show_msg(fr["fname"], ...) -------------------------
    # Most character dialogue names its speaker indirectly, out of the friends
    # roster. Harvest the roster's display names so a dynamic `who` resolves to
    # the real set of speakers instead of silently defaulting to Roshan.
    roster = {}
    fname_re = re.compile(r'"fname"\s*:\s*"([^"\\]+)"')
    for dirpath, _d, files in os.walk(SCRIPTS):
        for fn in sorted(files):
            if not fn.endswith(".gd") or fn.startswith("probe"):
                continue
            path = os.path.join(dirpath, fn)
            with open(path, encoding="utf-8", errors="replace") as fh:
                for i, ln in enumerate(fh, 1):
                    for m in fname_re.finditer(ln):
                        roster.setdefault(m.group(1),
                                          f"{os.path.relpath(path, ROOT)}:{i}")
    roster_keys = {}
    for name, site in roster.items():
        roster_keys.setdefault(speaker_key(name), []).append(name)

    for site, vos, vo_dyn, snippet in deferred_who:
        if not roster_keys:
            notes.append((site, "dynamic who, empty roster", snippet))
            continue
        for sp in roster_keys:
            if vo_dyn and not vos:
                dynamic_speakers[sp].append(site)
                continue
            for vo in vos:
                wanted[f"{sp}_{vo}" if vo else sp].append(site)
            if vo_dyn:
                dynamic_speakers[sp].append(site)

    # ---- data-table rows: {"speaker": "Faron", "vo": "op_nursery_catch"} ---
    # The opera career tables and the intro panels carry the voice key as data,
    # not as a call argument. A row's sibling "speaker" names who says it and
    # defaults to the consumer's default (Roshan in both current consumers):
    #   m.show_msg(String(phase.get("speaker", "Roshan")), ..., phase["vo"])
    vo_re = re.compile(r'"vo"\s*:\s*"([^"\\]+)"')
    spk_re = re.compile(r'"speaker"\s*:\s*"([^"\\]+)"')
    dflt_re = re.compile(r'get\(\s*"speaker"\s*,\s*"([^"\\]+)"\s*\)')
    for dirpath, _d, files in os.walk(SCRIPTS):
        for fn in sorted(files):
            if not fn.endswith(".gd"):
                continue
            path = os.path.join(dirpath, fn)
            rel = os.path.relpath(path, ROOT)
            with open(path, encoding="utf-8", errors="replace") as fh:
                lines = fh.readlines()
            body = "".join(lines)
            if '"vo"' not in body:
                continue
            dm = dflt_re.search(body)
            file_default = dm.group(1) if dm else "Roshan"
            for i, ln in enumerate(lines, 1):
                for vm in vo_re.finditer(ln):
                    sm = spk_re.search(ln)
                    who = sm.group(1) if sm else file_default
                    sp = speaker_key(who)
                    ev = vm.group(1)
                    wanted[f"{sp}_{ev}" if ev else sp].append(f"{rel}:{i}")

    # ---- _play_music(track) ------------------------------------------------
    for rel, line, a in find_calls("_play_music"):
        if not a or "audio_director.gd" in rel:
            continue
        vals, dyn = literal_values(a[0])
        site = f"{rel}:{line}"
        for v in vals:
            tracks[v].append(site)
        if dyn and not vals:
            notes.append((site, "dynamic music track", a[0][:60]))

    # night variant is derived inside _play_music
    if "world" in tracks:
        tracks["world_night"] = tracks["world"] + ["(derived: is_night)"]

    # ---- explicit res:// audio loads --------------------------------------
    # Two shapes in use: a full res:// path, and a path relative to
    # assets/audio/ carried in an interaction row ("sound": "castle/x.ogg").
    direct = defaultdict(list)
    dpat = re.compile(r'res://assets/audio/([A-Za-z0-9_./-]+\.(?:ogg|wav|mp3))')
    rpat = re.compile(r'"((?:castle|music|voices)/[A-Za-z0-9_.-]+\.(?:ogg|wav|mp3))"')
    for dirpath, _d, files in os.walk(SCRIPTS):
        for fn in sorted(files):
            if not fn.endswith(".gd"):
                continue
            path = os.path.join(dirpath, fn)
            rel = os.path.relpath(path, ROOT)
            is_probe = os.path.basename(path).startswith("probe")
            with open(path, encoding="utf-8", errors="replace") as fh:
                for i, ln in enumerate(fh, 1):
                    for m in list(dpat.finditer(ln)) + list(rpat.finditer(ln)):
                        tag = f"{rel}:{i}" + ("  (probe only)" if is_probe else "")
                        direct[m.group(1)].append(tag)

    # ---- disk inventory ----------------------------------------------------
    on_disk = []
    for dirpath, _d, files in os.walk(AUDIO):
        for fn in sorted(files):
            if os.path.splitext(fn)[1].lower() not in (".ogg", ".wav", ".mp3"):
                continue
            on_disk.append(os.path.relpath(os.path.join(dirpath, fn), AUDIO))
    on_disk.sort()

    voice_files = {os.path.splitext(os.path.basename(p))[0]
                   for p in on_disk if p.startswith("voices/")}

    # speakers that have a base clip usable as a fallback
    base_clips = {v for v in voice_files if "_" not in v}
    wanted_speakers = {k.split("_")[0] for k in wanted}
    known_speakers = KNOWN_SPEAKERS

    reachable = set(wanted_speakers) | set(dynamic_speakers)

    report = {}
    for rel in on_disk:
        stem = os.path.splitext(os.path.basename(rel))[0]
        if rel.startswith("voices/"):
            if stem in wanted:
                report[rel] = ("USED-EXACT", wanted[stem][:4])
            elif stem in base_clips:
                # base clip: reached whenever any line for this speaker
                # is requested but has no exact recording
                fb = [k for k in wanted if k.split("_")[0] == stem
                      and k not in voice_files]
                if fb:
                    report[rel] = ("USED-FALLBACK",
                                   [f"fallback for {len(fb)} line(s), e.g. "
                                    + ", ".join(sorted(fb)[:3])])
                elif stem in dynamic_speakers:
                    report[rel] = ("DYNAMIC-ONLY", dynamic_speakers[stem][:4])
                else:
                    report[rel] = _why_unreachable(stem, reachable,
                                                   known_speakers)
            elif stem.split("_")[0] in dynamic_speakers:
                report[rel] = ("DYNAMIC-ONLY",
                               dynamic_speakers[stem.split("_")[0]][:4])
            else:
                report[rel] = _why_unreachable(stem, reachable, known_speakers)
        elif rel.startswith("music/"):
            if stem in tracks:
                report[rel] = ("USED-EXACT", tracks[stem][:4])
            elif rel in direct:
                # e.g. banjo.ogg lives under music/ but is loaded as a sound
                # effect by an explicit path, never via _play_music
                report[rel] = _direct_label(direct[rel])
            else:
                report[rel] = ("UNUSED-TRACK",
                               ["no _play_music() call names this track"])
        else:
            if rel in direct:
                report[rel] = _direct_label(direct[rel])
            else:
                report[rel] = ("UNUSED-SFX", ["no code loads this path"])

    # ---- missing: asked for, never recorded -------------------------------
    missing = {}
    for key, sites in sorted(wanted.items()):
        if key in voice_files:
            continue
        sp = key.split("_")[0]
        missing[key] = {
            "sites": sites[:4],
            "count": len(sites),
            "falls_back_to": f"voices/{sp}.ogg" if sp in base_clips
                             else "pitched voice_yay",
        }
    missing_tracks = {t: s[:4] for t, s in sorted(tracks.items())
                      if not os.path.exists(os.path.join(MUSIC, t + ".ogg"))}

    # ---- print -------------------------------------------------------------
    counts = defaultdict(int)
    for label, _ in report.values():
        counts[label] += 1
    print("=" * 72)
    print("AUDIO USAGE AUDIT")
    print("=" * 72)
    print(f"files on disk : {len(on_disk)}")
    for label in ("USED-EXACT", "USED-FALLBACK", "USED-DIRECT",
                  "DYNAMIC-ONLY", "PROBE-ONLY", "UNUSED-FALLBACK",
                  "UNUSED-LINE", "UNREACHABLE-NAMING", "UNREACHABLE-SPEAKER",
                  "UNUSED-TRACK", "UNUSED-SFX", "ORPHAN"):
        print(f"  {label:<14} {counts[label]}")
    print(f"\nvoice keys requested by code : {len(wanted)}")
    print(f"  of those with no recording : {len(missing)}")
    print(f"music tracks requested       : {len(tracks)}"
          f"  (missing: {len(missing_tracks)})")

    for label in ("UNREACHABLE-NAMING", "UNREACHABLE-SPEAKER",
                  "UNUSED-LINE", "UNUSED-FALLBACK", "UNUSED-TRACK",
                  "UNUSED-SFX", "ORPHAN",
                  "PROBE-ONLY", "DYNAMIC-ONLY"):
        rows = sorted(r for r, (l, _) in report.items() if l == label)
        if not rows:
            continue
        print(f"\n--- {label} ({len(rows)}) ---")
        for r in rows:
            why = report[r][1]
            print(f"  {r}" + (f"   <- {why[0]}" if why else ""))

    if missing:
        print(f"\n--- MISSING RECORDINGS ({len(missing)}) ---")
        by_speaker = defaultdict(list)
        for k, v in missing.items():
            by_speaker[k.split("_")[0]].append((k, v))
        for sp in sorted(by_speaker, key=lambda s: -len(by_speaker[s])):
            rows = by_speaker[sp]
            fb = rows[0][1]["falls_back_to"]
            print(f"  {sp}  ({len(rows)} line(s), falls back to {fb})")
            for k, v in sorted(rows):
                print(f"      {k}.ogg   x{v['count']}  {v['sites'][0]}")

    if missing_tracks:
        print(f"\n--- MISSING MUSIC ({len(missing_tracks)}) ---")
        for t, s in missing_tracks.items():
            print(f"  music/{t}.ogg   <- {s[0]}")

    if notes:
        print(f"\n--- UNRESOLVED CALL SITES ({len(notes)}) ---")
        for site, why, snippet in notes[:20]:
            print(f"  {site}  {why}: {snippet}")

    if args_ns.json:
        out = {
            "files": {r: {"label": l, "evidence": e}
                      for r, (l, e) in sorted(report.items())},
            "missing_voice_lines": missing,
            "missing_music": missing_tracks,
            "requested_voice_keys": {k: v for k, v in sorted(wanted.items())},
            "requested_music_tracks": {k: v for k, v in sorted(tracks.items())},
        }
        with open(args_ns.json, "w", encoding="utf-8") as fh:
            json.dump(out, fh, indent=2, sort_keys=True)
        print(f"\nwrote {args_ns.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
