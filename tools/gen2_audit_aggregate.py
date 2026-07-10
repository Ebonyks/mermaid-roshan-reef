#!/usr/bin/env python3
"""Aggregate the Claude-driven gen-2 audit (gen2/audit/claude_*.json)
into gen2/generated/ANALYSIS.md plus a machine-readable summary.

Owner manual calls in gen2/curation.json override agent verdicts.
"""
import glob
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIT = os.path.join(ROOT, "gen2", "audit")
OUT_MD = os.path.join(ROOT, "gen2", "generated", "ANALYSIS.md")
OUT_JSON = os.path.join(AUDIT, "summary.json")

FLAW_NAMES = {
	"F1": "baked bubbles", "F2": "face on scenery", "F3": "confetti decals",
	"F4": "sticker border", "F5": "cluster not single", "F6": "tile repetition",
	"F7": "palette bleed/washed", "F8": "concept enmeshing",
	"F9": "invented character", "F10": "subject hijack",
}


def main():
	roles = {}
	for p in sorted(glob.glob(os.path.join(AUDIT, "claude_*.json"))):
		roles.update(json.load(open(p)))

	cur = {}
	cpath = os.path.join(ROOT, "gen2", "curation.json")
	if os.path.exists(cpath):
		cur = json.load(open(cpath))
	approved = {}   # role -> [(variant, note)]
	for a in cur.get("approved_by_roshan", []):
		r, v = a["pick"].rsplit("/", 1)
		approved.setdefault(r, []).append((v, a.get("note", "")))
	rejected = {}   # role -> [variant] ("v1-v4" expands to all)
	for a in cur.get("rejected_examples", []):
		r, v = a["pick"].rsplit("/", 1)
		vs = ["v1", "v2", "v3", "v4"] if "-" in v else [v]
		rejected.setdefault(r, []).extend(vs)

	buckets = {"KEEP": [], "POLISH": [], "REGEN": [], "MISSING": []}
	flaw_count = {}
	owner_overrides = []
	for role in sorted(roles):
		e = roles[role]
		verdict = e.get("verdict", "REGEN")
		kind = verdict.split(":")[0]
		# Owner approval pins the variant; his note decides KEEP vs POLISH
		if role in approved:
			v, note = approved[role][0]
			pin_kind = "POLISH" if "polish" in note.lower() else "KEEP"
			if verdict != f"{pin_kind}:{v}":
				owner_overrides.append(f"{role}: agent said {verdict}, owner pinned {pin_kind}:{v}")
			kind, verdict = pin_kind, f"{pin_kind}:{v}"
			e["verdict"] = verdict
			e["note"] = ("owner: " + note) if note else e.get("note", "")
		# Owner rejection of the agent's pick forces demotion
		elif ":" in verdict and verdict.split(":")[1] in rejected.get(role, []):
			kind, verdict = "REGEN", "REGEN"
			e["verdict"] = verdict
			owner_overrides.append(f"{role}: agent pick was owner-rejected -> REGEN")
		buckets.setdefault(kind, []).append(role)
		for v in e.get("variants", {}).values():
			for f in v.get("flaws", []):
				flaw_count[f] = flaw_count.get(f, 0) + 1

	n = len(roles)
	lines = ["# GEN-2 Batch 1 — Claude Audit", ""]
	lines.append(f"Roles audited: **{n}** (492 variants). Verdicts merge 10 parallel "
	             "Claude reviewers with the owner's manual calls (curation.json).")
	lines.append("")
	lines.append("| Verdict | Roles | % |")
	lines.append("|---|---|---|")
	for k in ("KEEP", "POLISH", "REGEN", "MISSING"):
		c = len(buckets.get(k, []))
		lines.append(f"| {k} | {c} | {100*c//max(n,1)}% |")
	lines.append("")
	lines.append("## Flaw frequency (per variant)")
	lines.append("")
	lines.append("| Code | Flaw | Hits |")
	lines.append("|---|---|---|")
	for f, c in sorted(flaw_count.items(), key=lambda x: -x[1]):
		lines.append(f"| {f} | {FLAW_NAMES.get(f, '?')} | {c} |")
	if owner_overrides:
		lines.append("")
		lines.append("## Owner overrides applied")
		lines.append("")
		for o in owner_overrides:
			lines.append(f"- {o}")
	for k, title in (("KEEP", "KEEP — ship the named variant"),
	                 ("POLISH", "POLISH — usable after photo-edit pass"),
	                 ("REGEN", "REGEN — no usable variant, round-2 scope"),
	                 ("MISSING", "MISSING — no files found")):
		rs = buckets.get(k, [])
		if not rs:
			continue
		lines.append("")
		lines.append(f"## {title} ({len(rs)})")
		lines.append("")
		for r in rs:
			e = roles[r]
			pick = e["verdict"].split(":")[1] if ":" in e["verdict"] else "-"
			lines.append(f"- `{r}` [{pick}] — {e.get('note', '')}")
	open(OUT_MD, "w").write("\n".join(lines) + "\n")

	json.dump({"roles": roles, "buckets": {k: v for k, v in buckets.items()},
	           "flaw_count": flaw_count}, open(OUT_JSON, "w"), indent=1)
	print(f"aggregated {n} roles -> {OUT_MD}")
	for k in ("KEEP", "POLISH", "REGEN", "MISSING"):
		print(f"  {k}: {len(buckets.get(k, []))}")


if __name__ == "__main__":
	main()
