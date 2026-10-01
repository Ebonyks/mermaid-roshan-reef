"""Read a constrained GDScript literal subset without executing project code."""
from __future__ import annotations

import ast
import json
import re
from pathlib import Path

CONSTRUCTORS = {"Color", "Vector2", "Vector2i", "Rect2", "PackedStringArray",
                "PackedInt32Array", "PackedFloat32Array"}
TAG_KEYS = {"__call__", "__dict__", "__stringname__"}


def mask_source(text: str, mask_strings: bool = True) -> str:
    """Preserve source offsets/newlines while hiding comments and string tokens."""
    out = list(text)
    index = 0
    def hide(start: int, end: int) -> None:
        for position in range(start, end):
            if out[position] not in "\r\n":
                out[position] = " "
    while index < len(text):
        if text[index] == "#":
            end = text.find("\n", index)
            end = end if end >= 0 else len(text)
            hide(index, end)
            index = end
        elif text[index] in ('"', "'"):
            start = index
            delimiter = text[index] * (3 if text.startswith(text[index] * 3, index) else 1)
            index += len(delimiter)
            while index < len(text):
                if text[index] == "\\":
                    index += 2
                elif text.startswith(delimiter, index):
                    index += len(delimiter)
                    break
                else:
                    index += 1
            else:
                raise ValueError("unterminated string in GDScript source")
            if mask_strings:
                hide(start, index)
        else:
            index += 1
    return "".join(out)


class GDParser:
    def __init__(self, text: str, start: int = 0):
        self.s, self.i = text, start

    def ws(self):
        while self.i < len(self.s):
            if self.s[self.i] in " \t\r\n\\":
                self.i += 1
            elif self.s[self.i] == "#":
                self.i = self.s.find("\n", self.i)
                if self.i < 0:
                    self.i = len(self.s)
            else:
                break

    def peek(self):
        self.ws()
        return self.s[self.i:self.i + 1]

    def value(self):
        c = self.peek()
        if c == "{":
            return self.mapping()
        if c == "[":
            return self.sequence("]")
        if c == "&":
            self.i += 1
            return {"__stringname__": self.string()}
        if c in ("'", '"'):
            return self.string()
        if c.isdigit() or c in ("-", "."):
            m = re.match(r"-?(?:0x[0-9A-Fa-f_]+|\d[\d_]*(?:\.\d+)?(?:[eE][-+]?\d+)?|\.\d+)", self.s[self.i:])
            if not m:
                raise ValueError("invalid number at " + str(self.i))
            raw = m.group().replace("_", "")
            self.i += len(m.group())
            return int(raw, 16) if "0x" in raw else (float(raw) if any(x in raw for x in ".eE") else int(raw))
        m = re.match(r"[A-Za-z_][A-Za-z0-9_]*", self.s[self.i:])
        if m:
            name = m.group()
            self.i += len(name)
            if name in ("true", "false", "null"):
                return {"true": True, "false": False, "null": None}[name]
            if self.peek() == "(":
                if name not in CONSTRUCTORS:
                    raise ValueError("forbidden constructor " + name)
                return {"__call__": name, "args": self.sequence(")")}
            raise ValueError("unsupported identifier " + name)
        raise ValueError("unsupported literal at " + str(self.i))

    def string(self):
        quote, start = self.s[self.i], self.i
        self.i += 1
        while self.i < len(self.s):
            if self.s[self.i] == "\\":
                self.i += 2
            elif self.s[self.i] == quote:
                self.i += 1
                raw = self.s[start:self.i]
                # JSON handles Unicode exactly; single quoted Godot literals are
                # read by Python's literal reader, never eval.
                return json.loads(raw) if quote == '"' else ast.literal_eval(raw)
            else:
                self.i += 1
        raise ValueError("unterminated string")

    def sequence(self, end):
        self.i += 1
        result = []
        while self.peek() != end:
            if not self.peek():
                raise ValueError("unterminated sequence")
            result.append(self.value())
            if self.peek() == ",":
                self.i += 1
            elif self.peek() != end:
                raise ValueError("missing sequence separator")
        self.i += 1
        return result

    def mapping(self):
        self.i += 1
        pairs = []
        while self.peek() != "}":
            key = self.value()
            if self.peek() not in (":", "="):
                raise ValueError("missing dictionary separator")
            self.i += 1
            pairs.append([key, self.value()])
            if self.peek() == ",":
                self.i += 1
            elif self.peek() != "}":
                raise ValueError("missing dictionary comma")
        self.i += 1
        if all(isinstance(k, str) for k, _ in pairs):
            if len(set(k for k, _ in pairs)) != len(pairs):
                raise ValueError("duplicate dictionary key")
            return dict(pairs)
        return {"__dict__": pairs}


def read_const(path: Path, name: str):
    text = path.read_text(encoding="utf-8")
    matches = list(re.finditer(r"(?m)^const\s+" + re.escape(name) + r"\b[^=\n]*=(?:\s*\\)?", mask_source(text)))
    if len(matches) != 1:
        raise ValueError(f"{path}: expected exactly one real constant {name}")
    parser = GDParser(text, matches[0].end())
    value = parser.value()
    tail = text[parser.i:text.find("\n", parser.i) if text.find("\n", parser.i) >= 0 else len(text)].strip()
    if tail and not tail.startswith("#"):
        raise ValueError(f"{path}: trailing expression after {name}")
    return value


def read_python_list(path: Path, name: str):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            if any(isinstance(t, ast.Name) and t.id == name for t in targets):
                return ast.literal_eval(node.value)
    raise ValueError(f"{path}: missing literal {name}")


def opera_rows(root: Path):
    text = (root / "scripts/living_world_catalog.gd").read_text(encoding="utf-8")
    code = mask_source(text)
    functions = list(re.finditer(r"(?m)^static func _add_opera_acts\(", code))
    if len(functions) != 1:
        raise ValueError("expected one real Opera living-world function")
    function = functions[0]
    following = re.search(r"(?m)^(?:static\s+)?func\b", code[function.end():])
    end = function.end() + following.start() if following else len(text)
    calls = list(re.finditer(r"_add_rows\(", code[function.end():end]))
    if len(calls) != 1:
        raise ValueError("expected one real Opera living-world row call")
    start = function.end() + calls[0].start()
    match = re.match(r'_add_rows\(specs,\s*"opera_act",\s*11,\s*', text[start:end])
    if not match:
        raise ValueError("Opera living-world row call differs")
    parser = GDParser(text, start + match.end())
    value = parser.value()
    if parser.peek() != ")":
        raise ValueError("trailing expression after Opera living-world rows")
    parser.i += 1
    newline = text.find("\n", parser.i)
    tail = text[parser.i:newline if newline >= 0 else len(text)].strip()
    if tail and not tail.startswith("#"):
        raise ValueError("trailing expression after Opera living-world call")
    return value


def integer_mapping(value):
    if isinstance(value, dict) and set(value) == {"__dict__"}:
        return dict(value["__dict__"])
    return value

