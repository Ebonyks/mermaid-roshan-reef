"""Measure the pacing of a comic book script. Numbers only; reads JSON, writes JSON.

Supports three script shapes used by the Rumi under-pool book editions:

* ``story_script.json`` - pages[].panels[].entries[] with ``speaker`` and ``text``
* ``comic_script.json`` - pages[].panels[].text[] with ``speaker`` and ``line``
* ``book_plan.json`` - spreads[] with ``left`` and ``right`` prose

Optional per-panel fields that the revised script should carry are counted
when present: ``size`` (splash, large, medium, small, inset), ``silent``
(true when the picture carries the beat alone), ``location``, ``plot``
(A, B, C or D) and ``game_link``. Optional per-page fields: ``turn``
("hook" on an odd page's last panel, "reveal" on an even page's first panel)
and ``chapter``.

Usage::

    python -B measure_book_pacing.py SCRIPT.json [--spreads] [--out OUT.json]

``--spreads`` reports page-turn hooks for a book whose page 1 is a lone
right-hand page, so turns happen after pages 3, 5, 7 and so on.

Word counts split on whitespace after removing music-note glyphs. A page is
"story" unless its ``kind`` is ``cover`` or ``back``. Hook detection is a
text proxy only: a page-ending entry that ends in ``?``, ``...`` or an em dash,
or a panel the script marks ``turn: hook``. It does not judge pictures.
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

NOTE_GLYPHS = re.compile("[♪♫♬♩]")
TRAILING = ("?", "...", "…", "—", "-")


def words(text: str) -> int:
    cleaned = NOTE_GLYPHS.sub(" ", text or "")
    return len([w for w in cleaned.split() if any(ch.isalnum() for ch in w)])


def load_pages(data: dict) -> list[dict]:
    """Normalise every supported shape to pages[{number, kind, panels[{entries}]}]."""
    if "pages" in data:
        pages = []
        for page in data["pages"]:
            panels = []
            for panel in page.get("panels", []):
                if "entries" in panel:
                    entries = [
                        {"speaker": e.get("speaker", ""), "text": e.get("text", "")}
                        for e in panel.get("entries", [])
                    ]
                else:
                    entries = [
                        {"speaker": e.get("speaker", ""), "text": e.get("line", e.get("text", ""))}
                        for e in panel.get("text", [])
                    ]
                panels.append({**panel, "entries": entries})
            pages.append(
                {
                    "number": page.get("number"),
                    "kind": page.get("kind", "story"),
                    "turn": page.get("turn"),
                    "chapter": page.get("chapter"),
                    "panels": panels,
                }
            )
        return pages
    if "spreads" in data:
        pages = []
        for index, spread in enumerate(data["spreads"]):
            for side in ("left", "right"):
                text = spread.get(side, "")
                pages.append(
                    {
                        "number": 3 + index * 2 + (side == "right"),
                        "kind": "story",
                        "turn": None,
                        "chapter": None,
                        "panels": [{"entries": [{"speaker": "Prose", "text": text}]}],
                    }
                )
        return pages
    raise SystemExit("Unsupported script shape: expected 'pages' or 'spreads'.")


def summary(values: list[float]) -> dict:
    if not values:
        return {"n": 0}
    return {
        "n": len(values),
        "min": min(values),
        "median": statistics.median(values),
        "mean": round(statistics.mean(values), 2),
        "max": max(values),
        "stdev": round(statistics.pstdev(values), 2),
    }


def longest_run(values: list[int]) -> int:
    best = run = 0
    previous = None
    for value in values:
        run = run + 1 if value == previous else 1
        best = max(best, run)
        previous = value
    return best


def is_hook_text(text: str) -> bool:
    stripped = NOTE_GLYPHS.sub("", text or "").strip()
    return stripped.endswith(TRAILING)


def measure(data: dict, spreads: bool) -> dict:
    pages = load_pages(data)
    story = [p for p in pages if p["kind"] not in ("cover", "back")]
    panel_counts, word_counts = [], []
    speaker_lines, speaker_words = Counter(), Counter()
    silent = sound = 0
    sizes, locations, plots, game_links = Counter(), Counter(), Counter(), Counter()
    per_page = []
    for page in story:
        page_words = 0
        page_speakers = set()
        for panel in page["panels"]:
            if not panel["entries"] or panel.get("silent") is True:
                silent += 1
            for entry in panel["entries"]:
                count = words(entry["text"])
                page_words += count
                speaker = (entry["speaker"] or "").split(",")[0].strip()
                speaker_lines[speaker] += 1
                speaker_words[speaker] += count
                page_speakers.add(speaker)
                if speaker.lower().startswith("sound"):
                    sound += 1
            if panel.get("size"):
                sizes[panel["size"]] += 1
            if panel.get("location"):
                locations[panel["location"]] += 1
            for plot in panel.get("plot", []) if isinstance(panel.get("plot"), list) else [panel.get("plot")]:
                if plot:
                    plots[plot] += 1
            if panel.get("game_link"):
                game_links[panel["game_link"]] += 1
        last_text = ""
        for panel in reversed(page["panels"]):
            if panel["entries"]:
                last_text = panel["entries"][-1]["text"]
                break
        marked_hook = page.get("turn") == "hook" or any(
            panel.get("turn") == "hook" for panel in page["panels"][-1:]
        )
        per_page.append(
            {
                "page": page["number"],
                "panels": len(page["panels"]),
                "words": page_words,
                "speakers": len(page_speakers),
                "ends_open": bool(marked_hook or is_hook_text(last_text)),
            }
        )
        panel_counts.append(len(page["panels"]))
        word_counts.append(page_words)
    total_panels = sum(panel_counts)
    total_words = sum(word_counts)
    result = {
        "pages_total": len(pages),
        "story_pages": len(story),
        "panels_total": total_panels,
        "words_total": total_words,
        "panels_per_page": summary(panel_counts),
        "words_per_page": summary(word_counts),
        "words_per_panel_mean": round(total_words / total_panels, 2) if total_panels else 0,
        "one_panel_pages": sum(1 for c in panel_counts if c == 1),
        "pages_with_5_plus_panels": sum(1 for c in panel_counts if c >= 5),
        "longest_run_same_panel_count": longest_run(panel_counts),
        "silent_panels": silent,
        "silent_panel_share": round(silent / total_panels, 3) if total_panels else 0,
        "sound_effect_entries": sound,
        "speaker_lines": dict(speaker_lines.most_common()),
        "speaker_words": dict(speaker_words.most_common()),
        "narrator_word_share": round(speaker_words.get("Narrator", 0) / total_words, 3) if total_words else 0,
        "per_page": per_page,
    }
    if sizes:
        result["panel_sizes"] = dict(sizes)
    if locations:
        result["panels_per_location"] = dict(locations.most_common())
    if plots:
        result["panels_per_plot_thread"] = dict(plots)
    if game_links:
        result["panels_per_game_link"] = dict(game_links)
    if spreads:
        turn_pages = [row for row in per_page if isinstance(row["page"], int) and row["page"] % 2 == 1 and row["page"] >= 3]
        result["page_turns"] = len(turn_pages)
        result["page_turns_ending_open"] = sum(1 for row in turn_pages if row["ends_open"])
        result["page_turn_pages_ending_open"] = [row["page"] for row in turn_pages if row["ends_open"]]
    return result


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("script", type=Path)
    parser.add_argument("--spreads", action="store_true")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args(argv)
    data = json.loads(args.script.read_text(encoding="utf-8"))
    result = {"script": args.script.name, **measure(data, args.spreads)}
    text = json.dumps(result, indent=2, ensure_ascii=False)
    if args.out:
        args.out.write_text(text + "\n", encoding="utf-8")
    else:
        sys.stdout.write(text + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
