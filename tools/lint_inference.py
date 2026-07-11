#!/usr/bin/env python3
"""Catch GDScript ':=' inferences that Godot's analyzer rejects but a
parse-only check (gdtoolkit) cannot see.

Godot fails 'var x := <expr>' when <expr> is statically Variant. Both
2026-07-11 incidents (sky_lagoon 'tnode', main.gd 'sm2') had one shape: the
WHOLE right-hand side is a member-call/subscript chain on a receiver with
no static type (untyped 'var m', untyped 'for' loop variable, untyped
parameter). This lint flags exactly that shape. Arithmetic around the
access (e.g. 'c.x + cos(a) * r') is deliberately NOT flagged - the live
tree contains such lines and Godot accepts them, so whole-RHS chains are
the only shape with an actual incident record.

Usage: python3 tools/lint_inference.py <file.gd> [...]  (exits 1 on findings)
"""
import re
import sys

FUNC_RE = re.compile(r"^(\s*)func\s+\w+\s*\(([^)]*)\)")
FOR_RE = re.compile(r"^\s*for\s+(\w+)\s+in\s")
FOR_TYPED_RE = re.compile(r"^\s*for\s+\w+\s*:\s*\w+\s+in\s")
VAR_UNTYPED_RE = re.compile(r"^(\s*)var\s+(\w+)\s*(?:=(?!=)|$)")
ASSIGN_RE = re.compile(r":=\s*(.+)$")
RECV_RE = re.compile(r"^(\w+)\s*([.\[])")


def strip_comment(s: str) -> str:
    out, q = [], None
    for ch in s:
        if q:
            out.append(ch)
            if ch == q:
                q = None
        elif ch in "\"'":
            q = ch
            out.append(ch)
        elif ch == "#":
            break
        else:
            out.append(ch)
    return "".join(out)


def whole_rhs_is_chain(rhs: str) -> str:
    """Return the receiver name if the entire RHS is a .member/(...)/[...]
    chain rooted at a bare identifier, else ''."""
    rhs = strip_comment(rhs).strip()
    m = RECV_RE.match(rhs)
    if not m:
        return ""
    recv = m.group(1)
    i = len(recv)
    n = len(rhs)
    while i < n:
        ch = rhs[i]
        if ch == ".":
            j = i + 1
            while j < n and (rhs[j].isalnum() or rhs[j] == "_"):
                j += 1
            if j == i + 1:
                return ""
            i = j
        elif ch in "([":
            depth, close = 0, {"(": ")", "[": "]"}[ch]
            while i < n:
                if rhs[i] == ch:
                    depth += 1
                elif rhs[i] == close:
                    depth -= 1
                    if depth == 0:
                        break
                i += 1
            if depth != 0:
                return ""
            i += 1
        elif ch.isspace():
            i += 1
        else:
            return ""   # arithmetic / operators: type may resolve, skip
    return recv


def lint(path: str) -> list:
    findings = []
    class_untyped: set = set()
    func_untyped: set = set()
    with open(path, encoding="utf-8") as f:
        for ln, line in enumerate(f, 1):
            fm = FUNC_RE.match(line)
            if fm:
                func_untyped = set()
                for p in fm.group(2).split(","):
                    p = p.strip()
                    if p and ":" not in p:
                        func_untyped.add(p.split("=")[0].strip())
                continue
            m = FOR_RE.match(line)
            if m and not FOR_TYPED_RE.match(line):
                func_untyped.add(m.group(1))
            m = VAR_UNTYPED_RE.match(line)
            if m and ":=" not in line:
                (class_untyped if m.group(1) == "" else func_untyped).add(m.group(2))
            m = ASSIGN_RE.search(strip_comment(line))
            if m:
                recv = whole_rhs_is_chain(m.group(1))
                if recv and recv in (func_untyped | class_untyped):
                    findings.append((path, ln, recv, line.strip()))
    return findings


def main() -> int:
    bad = []
    for path in sys.argv[1:]:
        bad.extend(lint(path))
    for path, ln, var, src in bad:
        print(f"{path}:{ln}: ':=' infers from untyped '{var}' (Variant) - "
              f"Godot will reject this. Add an explicit type.\n    {src}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
