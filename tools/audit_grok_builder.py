"""Validate the shared builder database; derive a browsable library and SQLite mirror."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import sqlite3
from contextlib import closing
from pathlib import Path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(root, data):
    errors = []
    tables = {}
    for table in ("entities", "events", "shots", "references", "storyboards", "clips"):
        rows = data.get(table, [])
        tables[table] = {r["id"]: r for r in rows}
        if len(rows) != len(tables[table]):
            errors.append(f"Duplicate ID in {table}")
    def link(table, key, owner):
        if key not in tables[table]:
            errors.append(f"{owner}: unresolved {table} ID {key}")
    for r in data["references"]:
        p = (root / r["path"]).resolve()
        if not p.is_relative_to(root.resolve()) or not p.is_file():
            errors.append(f"{r['id']}: missing or escaping media path")
        elif digest(p) != r["sha256"]:
            errors.append(f"{r['id']}: media hash mismatch")
    for e in data["entities"]:
        for rid in e["reference_ids"]:
            link("references", rid, e["id"])
            ref = tables['references'].get(rid, {})
            if any(ref.get('sha256', '').startswith(h) for h in data.get('superseded_reference_hashes', [])):
                errors.append(f"{e['id']}: superseded identity reference")
        for rid in e.get('boundary_reference_ids', []):
            link('references', rid, e['id'])
    for edge in data.get('entity_relationships', []):
        link('entities', edge['from_id'], 'relationship')
        link('entities', edge['to_id'], 'relationship')
    for clip in data.get('clips', []):
        if clip.get('delivery_accepted') or clip.get('appearance_authority'):
            errors.append(f"{clip['id']}: historical clip inventory cannot grant delivery or appearance acceptance")
    for e in data["events"]:
        if e.get("location_id"):
            link("entities", e["location_id"], e["id"])
        if e.get('destination_location_id'):
            link('entities', e['destination_location_id'], e['id'])
        for key in e.get("character_ids", []) + e.get("prop_ids", []):
            link("entities", key, e["id"])
        for dep in e.get("depends_on", []):
            link("events", dep, e["id"])
    for s in data["shots"]:
        link("events", s["event_id"], s["id"])
        link("entities", s["location_id"], s["id"])
        for key in s.get("character_ids", []):
            link("entities", key, s["id"])
        for rid in s.get("reference_pool_ids", []):
            link("references", rid, s["id"])
        for dep in s.get("depends_on", []):
            link("shots", dep, s["id"])
        if s.get("generation_ready") or s.get("delivery_accepted"):
            errors.append(f"{s['id']}: this builder schema cannot grant execution or delivery acceptance; use independent gates")
        if s.get("opening_reference_id"):
            link("references", s["opening_reference_id"], s["id"])
            r = tables["references"].get(s["opening_reference_id"], {})
            if not r.get("appearance_authority") or any(w in r.get("role", "").lower() for w in ("board", "runtime", "evidence")):
                errors.append(f"{s['id']}: prohibited opening reference")
        if s.get("board") and not (root / s["board"]).is_file():
            errors.append(f"{s['id']}: missing beat board")
    for b in data["storyboards"]:
        link("references", b["reference_id"], b["id"])
        for eid in b.get("event_ids", []):
            link("events", eid, b["id"])
    for table in ("events", "shots"):
        visited, active = set(), set()
        def walk(key):
            if key in active:
                errors.append(f"{table}: dependency cycle at {key}")
                return
            if key in visited or key not in tables[table]:
                return
            active.add(key)
            for dep in tables[table][key].get("depends_on", []):
                walk(dep)
            active.remove(key)
            visited.add(key)
        for key in tables[table]:
            walk(key)
    return errors


def rebuild(root, data):
    path = root / "DATABASE.sqlite"
    if path.exists():
        path.unlink()
    with closing(sqlite3.connect(path)) as db, db:
        db.execute("PRAGMA foreign_keys=ON")
        db.executescript('''
        CREATE TABLE entities(id TEXT PRIMARY KEY, type TEXT, name TEXT, record_json TEXT NOT NULL);
        CREATE TABLE clips(id TEXT PRIMARY KEY, sha256 TEXT, source_url TEXT, record_json TEXT NOT NULL);
        CREATE TABLE refs(id TEXT PRIMARY KEY, path TEXT, sha256 TEXT, record_json TEXT NOT NULL);
        CREATE TABLE entity_refs(entity_id TEXT REFERENCES entities(id), reference_id TEXT REFERENCES refs(id), PRIMARY KEY(entity_id, reference_id));
        CREATE TABLE events(id TEXT PRIMARY KEY, name TEXT, location_id TEXT REFERENCES entities(id), record_json TEXT NOT NULL);
        CREATE TABLE event_dependencies(event_id TEXT REFERENCES events(id), requires_id TEXT REFERENCES events(id), PRIMARY KEY(event_id, requires_id));
        CREATE TABLE shots(id TEXT PRIMARY KEY, event_id TEXT REFERENCES events(id), status TEXT, record_json TEXT NOT NULL);
        CREATE TABLE shot_dependencies(shot_id TEXT REFERENCES shots(id), requires_id TEXT REFERENCES shots(id), PRIMARY KEY(shot_id, requires_id));
        CREATE TABLE storyboards(id TEXT PRIMARY KEY, reference_id TEXT REFERENCES refs(id), status TEXT, record_json TEXT NOT NULL);
        CREATE TABLE participants(event_id TEXT REFERENCES events(id), entity_id TEXT REFERENCES entities(id), PRIMARY KEY(event_id,entity_id));
        CREATE TABLE entity_relationships(from_id TEXT REFERENCES entities(id), relation TEXT, to_id TEXT REFERENCES entities(id), PRIMARY KEY(from_id,relation,to_id));
        ''')
        for e in data["entities"]:
            db.execute("INSERT INTO entities VALUES(?,?,?,?)", (e["id"], e["type"], e["name"], json.dumps(e)))
        for c in data.get('clips', []):
            db.execute('INSERT INTO clips VALUES(?,?,?,?)', (c['id'], c['sha256'], c['source_url'], json.dumps(c)))
        for edge in data.get('entity_relationships', []):
            db.execute('INSERT INTO entity_relationships VALUES(?,?,?)', (edge['from_id'], edge['relation'], edge['to_id']))
        for r in data["references"]:
            db.execute("INSERT INTO refs VALUES(?,?,?,?)", (r["id"], r["path"], r["sha256"], json.dumps(r)))
        for e in data["entities"]:
            db.executemany("INSERT INTO entity_refs VALUES(?,?)", [(e["id"], r) for r in e["reference_ids"]])
        for e in data["events"]:
            db.execute("INSERT INTO events VALUES(?,?,?,?)", (e["id"], e["name"], e.get("location_id"), json.dumps(e)))
        for e in data["events"]:
            db.executemany("INSERT INTO event_dependencies VALUES(?,?)", [(e["id"], dep) for dep in e.get("depends_on", [])])
            db.executemany("INSERT INTO participants VALUES(?,?)", [(e["id"], c) for c in e.get("character_ids", [])])
        for s in data["shots"]:
            db.execute("INSERT INTO shots VALUES(?,?,?,?)", (s["id"], s["event_id"], s["status"], json.dumps(s)))
        for s in data["shots"]:
            db.executemany("INSERT INTO shot_dependencies VALUES(?,?)", [(s["id"], dep) for dep in s.get("depends_on", [])])
        for b in data["storyboards"]:
            db.execute("INSERT INTO storyboards VALUES(?,?,?,?)", (b["id"], b["reference_id"], b["status"], json.dumps(b)))
        assert db.execute("PRAGMA foreign_key_check").fetchall() == []
        assert db.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
    refs = {r["id"]: r for r in data["references"]}
    cards = []
    for table in ("entities", "events", "shots", "storyboards", "clips"):
        for row in data.get(table, []):
            title = row.get("name", row["id"])
            category = row.get("type", table)
            pictures = row.get("reference_ids", []) or ([row["reference_id"]] if row.get("reference_id") else [])
            if row.get("board_reference_id"):
                pictures = [row["board_reference_id"]]
            imgs = ''.join(f'<a href="{html.escape(refs[r]["path"])}"><img loading="lazy" src="{html.escape(refs[r]["path"])}" alt="{html.escape(title)}"></a>' for r in pictures)
            if row.get("board"):
                imgs += f'<a href="{html.escape(row["board"])}"><img loading="lazy" src="{html.escape(row["board"])}" alt="Draft reference beat board"></a>'
            details = html.escape(json.dumps(row, indent=2, ensure_ascii=False))
            cards.append(f'<article data-kind="{category}"><small>{category} · {row["id"]}</small><h2>{html.escape(title)}</h2>{imgs}<p>{html.escape(row.get("status", "SOURCE_RECORD"))}</p><details><summary>Identity, state, sources and relationships</summary><pre>{details}</pre></details></article>')
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Mermaid Roshan — builder library</title><style>
    *{box-sizing:border-box}body{margin:0;background:#101e30;color:#eef5ff;font:16px system-ui}header{padding:34px max(24px,5vw);background:#203653}h1{margin:0 0 12px;font-size:34px}a{color:#9ee0eb}nav{position:sticky;top:0;background:#14283e;padding:18px 5vw;display:flex;gap:14px;z-index:2}input,select{font:inherit;padding:10px;border:1px solid #53718b;border-radius:8px;background:#fff;color:#16283c}input{flex:1;min-width:100px}main{padding:25px 5vw;display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:22px}article{padding:22px;background:#20334c;border-radius:14px;min-width:0}article img{max-width:100%;max-height:340px;object-fit:contain;background:#dce5ec;border-radius:7px}h2{font-size:22px}small{color:#abd7df}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:13px ui-monospace}details{margin-top:14px}footer{padding:28px 5vw}.note{color:#ffd897}#count{margin-left:auto}</style>
    <header><h1>Mermaid Roshan · Project library</h1><p>One shared world. Stable characters, fixed locations, causal events and a visible replacement queue.</p><p><a href="START_GROK.txt">Start Grok builder</a> · <a href="DATABASE.json">Editable JSON</a> · <a href="DATABASE.sqlite">SQLite mirror</a> · <a href="CONFLICT_RESOLUTIONS.json">Conflict resolutions</a> · <a href="HANDOFF_PACKET.json">Manifest</a></p><p class="note">Planning/reference library. Missing-shot boards are reference art plus text beats, not generated action frames. Generation and delivery acceptance remain open.</p></header>
    <nav><input id="search" aria-label="Search library" placeholder="Search names, events, rules, missing shots…"><select id="kind" aria-label="Record type"><option value="">All records</option><option>character</option><option>location</option><option>prop</option><option>events</option><option>shots</option><option>storyboards</option><option>clips</option></select><span id="count"></span></nav><main>'''+''.join(cards)+'''</main><footer><a href="evidence/ALL_STORYBOARD_INVENTORY.json">Complete historical storyboard inventory</a> · <a href="AUDIT.txt">Audit and limits</a><p>Read-only browser. Edit the canonical JSON and rebuild; Grok builder import/export requirements are in START_GROK.txt.</p></footer><script>
    const search=document.querySelector('#search'),kind=document.querySelector('#kind'),cards=[...document.querySelectorAll('article')];function filter(){let count=0;for(const c of cards){const show=(!kind.value||c.dataset.kind===kind.value)&&c.textContent.toLowerCase().includes(search.value.toLowerCase());c.hidden=!show;if(show)count++;}document.querySelector('#count').textContent=count+' records';}search.addEventListener('input',filter);kind.addEventListener('change',filter);filter();</script></html>'''
    (root / "index.html").write_text(page, encoding="utf-8")


def manifest(root):
    prov = json.loads((root / "PROVENANCE_INPUTS.json").read_text(encoding="utf-8"))
    files = []
    for p in sorted(root.rglob("*"), key=lambda p: p.relative_to(root).as_posix()):
        if not p.is_file() or p.name in ("HANDOFF_PACKET.json", "REMOTE_VERIFICATION.json"):
            continue
        path = p.relative_to(root).as_posix()
        item = dict(prov.get(path, {}))
        item.update(path=path, sha256=digest(p), bytes=p.stat().st_size, used_as_delivery_pixels=False)
        item.setdefault("source_paths", ["New project-authored builder database/derived artifact, 2026-09-14"])
        item.setdefault("role", "project knowledge, review or derived database")
        item.setdefault("license_provenance", "Project-owned original; inherited art provenance retained in source manifests and ASSET_LICENSES.txt")
        item.setdefault("modifications", "new authored or deterministic derived file")
        item.setdefault("dimensions", None)
        files.append(item)
    payload = ''.join(f"{x['path']}|{x['sha256']}\n" for x in files)
    result = dict(schema="grok-builder-archive-v1", files=files, payload_sha256=hashlib.sha256(payload.encode()).hexdigest(), payload_formula="SHA256 sorted relative_path|sha256 LF; excludes manifest and subsequent remote receipt", ARCHIVE_COMPLETE=False, publication="See separate REMOTE_VERIFICATION.json", GENERATION_READY=False, DELIVERY_ACCEPTED=False)
    (root / "HANDOFF_PACKET.json").write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("packet",type=Path)
    parser.add_argument("--rebuild",action="store_true")
    args=parser.parse_args()
    data=json.loads((args.packet/"DATABASE.json").read_text(encoding="utf-8"))
    errors=validate(args.packet,data)
    if errors:
        print('\n'.join('FAIL '+e for e in errors))
        return 1
    if args.rebuild:
        rebuild(args.packet,data)
        manifest(args.packet)
    else:
        saved=json.loads((args.packet/"HANDOFF_PACKET.json").read_text(encoding="utf-8"))
        actual={p.relative_to(args.packet).as_posix() for p in args.packet.rglob('*') if p.is_file() and p.name not in ('HANDOFF_PACKET.json','REMOTE_VERIFICATION.json')}
        assert actual=={f['path'] for f in saved['files']},'Unmanifested or missing payload'
        for f in saved['files']:
            assert digest(args.packet/f['path'])==f['sha256'],f['path']
        payload=''.join(f"{x['path']}|{x['sha256']}\n" for x in saved['files'])
        assert hashlib.sha256(payload.encode()).hexdigest()==saved['payload_sha256']
    print('PASS builder IDs, relationships, acyclic dependencies, media hashes, draft-only acceptance; '+str(len(data['shots']))+' shots')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
