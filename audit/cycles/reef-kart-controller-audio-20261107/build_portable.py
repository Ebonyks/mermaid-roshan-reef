"""Build and smoke-test an isolated Windows x64 Reef Grand Prix playtest."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import zipfile

CYCLE = Path(__file__).resolve().parent
ROOT = CYCLE.parents[2]
APP = "Reef Grand Prix"
COURSES = ("playroom", "kitchen", "mermaid_pool", "opera_hall")
PROJECT = """
config_version=5

[application]
config/name="Reef Grand Prix"
run/main_scene="res://portable.tscn"
config/features=PackedStringArray("4.7", "Mobile")

[display]
window/size/viewport_width=1280
window/size/viewport_height=720
window/stretch/mode="canvas_items"
window/stretch/aspect="expand"

[rendering]
renderer/rendering_method="mobile"
"""
PRESET = """
[preset.0]
name="Windows Playtest"
platform="Windows Desktop"
runnable=true
advanced_options=false
dedicated_server=false
custom_features=""
export_filter="all_resources"
include_filter=""
exclude_filter=""
export_path=""
script_export_mode=2

[preset.0.options]
binary_format/architecture="x86_64"
binary_format/embed_pck=false
texture_format/s3tc_bptc=true
texture_format/etc2_astc=false
application/modify_resources=false
application/export_angle=0
application/export_d3d12=0
codesign/enable=false
"""
SCENE = """[gd_scene load_steps=2 format=3]

[ext_resource type="Script" path="res://portable_entry.gd" id="1"]

[node name="ReefGrandPrix" type="Node"]
script = ExtResource("1")
"""
EXIT_SCENE = """[gd_scene load_steps=2 format=3]

[ext_resource type="Script" path="res://exit_portable.gd" id="1"]

[node name="Exit" type="Node"]
script = ExtResource("1")
"""
README = """Reef Grand Prix — Windows x64 split-screen playtest

Extract the entire ZIP into a writable folder. Keep the EXE and PCK together.
Open Reef Grand Prix.exe. Godot installation is unnecessary.

For a logged session, open "Start Controller Test.cmd" instead. The game writes
controller-trace.jsonl beside the EXE. The trace records gamepad events and game
steps. Physical button-to-screen delay includes hardware and display timing.

Plug in the USB pad and pair the Bluetooth pad in Windows before starting.
Use the wired pad to choose Split-screen and enter the garage. Join with A on
the Bluetooth pad, then mark both players ready. P1 chooses and starts a track.

A / RT gas     Left stick or D-pad steer     B / LT brake and reverse
RB drift      X / LB use item                Start pause or resume

Run all four courses. Alternate, overlap and release both gas inputs. Collect
items on both sides. The item voice is panned left for P1 and right for P2
through the PC stereo output. The active item badge lights up on its owner's
side. Both players hear the centered opening guide.

Record controller models, which one is wired, any drops or delay, and which
seat heard each item cue. Retain controller-trace.jsonl with your notes.
"""


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.lstrip("\n"), encoding="utf-8", newline="\n")


def add_source(relative, stage):
    source = ROOT / relative
    destination = stage / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    if source.suffix in {".gd", ".gdshader", ".tscn", ".tres", ".uid"}:
        shutil.copyfile(source, destination)
    else:
        os.link(source, destination)
    importer = source.with_name(source.name + ".import")
    if importer.is_file():
        shutil.copyfile(importer, destination.with_name(destination.name + ".import"))


def resources(cast):
    racer_dir = ROOT / "scripts/racer"
    scripts = sorted(racer_dir.glob("*.gd"))
    text = cast + "\n".join(p.read_text(encoding="utf-8-sig") for p in scripts)
    paths = set(re.findall(r'res://(assets/[^"\s%]+?\.(?:png|webp|jpg|ogg))"', text))
    for pattern in (
        "assets/kart/**/*.png",
        "assets/racer/**/*.png",
        "assets/audio/objective_guides/guide_kart_*.ogg",
        "assets/flats/castle/rooms/room_playroom_item_*.png",
        "assets/flats/castle/rooms/room_kitchen_item_*.png",
        "assets/flats/castle/rooms/room_opera_hall_item_*.png",
    ):
        paths.update(p.relative_to(ROOT).as_posix() for p in ROOT.glob(pattern)
                     if "/rider_poses_v2/" not in p.as_posix())
    paths.update(f"assets/flats/castle/rooms/room_{room}_background.png" for room in COURSES)
    paths.update(p.relative_to(ROOT).as_posix() for p in racer_dir.iterdir()
                 if p.is_file() and p.suffix in {".gd", ".gdshader", ".uid"})
    paths.update(("scenes/racer/reef_grand_prix_pc.tscn", "default_bus_layout.tres",
                  "scripts/storybook_ui.gd", "scripts/shell_ornament.gd",
                  "assets/fashion/skin_engine_v2/ui/wardrobe_card.png"))
    return sorted(paths)


def run(args, log, env, timeout=360):
    with log.open("wb") as output:
        result = subprocess.run([str(x) for x in args], cwd=log.parent, env=env,
                                stdout=output, stderr=subprocess.STDOUT, timeout=timeout)
    log_text = log.read_text(encoding="utf-8", errors="replace")
    if result.returncode or re.search(r"SCRIPT ERROR|^ERROR:|^USER ERROR:", log_text, re.M):
        raise RuntimeError(f"{log.name}: exit {result.returncode}\n{log_text[-5000:]}")
    return log_text


def sha(path):
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def build(output, godot, template):
    if template.name != "windows_release_x86_64.exe" or template.parent.name != "4.7.2.stable":
        raise ValueError("Select the official Godot 4.7.2-stable Windows x64 release template.")
    output.mkdir(parents=True, exist_ok=False)
    stage = output / "isolated-project"
    game = output / "game"
    profile = output / "export-profile"
    game.mkdir()
    profile.mkdir()
    legacy = (ROOT / "scripts/racer_game_2d.gd").read_text(encoding="utf-8-sig")
    table = re.search(r"^const RACERS := \[\n.*?^\]", legacy, re.M | re.S).group()
    paths = resources(table)
    for path in paths:
        if (ROOT / path).is_file():
            add_source(path, stage)
    write(stage / "scripts/racer_game_2d.gd", "extends RefCounted\nclass_name RacerGame2D\n\n" + table + "\n")
    write(stage / "project.godot", PROJECT)
    write(stage / "portable.tscn", SCENE)
    write(stage / "scenes/main.tscn", EXIT_SCENE)
    write(stage / "exit_portable.gd", "extends Node\n\nfunc _ready() -> void:\n\tget_tree().quit()\n")
    write(stage / "export_presets.cfg", PRESET)
    shutil.copyfile(CYCLE / "physical_playtest.gd", stage / "controller_trace.gd")
    shutil.copyfile(CYCLE / "portable_entry.gd", stage / "portable_entry.gd")
    diagnostics = stage / "diagnostics"
    write(diagnostics / ".gdignore", "")
    write(diagnostics / "licenses.gd", """extends SceneTree
func _initialize() -> void:
	print(Engine.get_license_text())
	var licenses := Engine.get_license_info()
	for name: String in licenses:
		print("\n" + name + "\n" + String(licenses[name]))
	quit()
""".replace('print("\n" + name + "\n"', 'print("\\n" + name + "\\n"'))
    env = dict(os.environ, APPDATA=str(profile), LOCALAPPDATA=str(profile))
    version = run([godot, "--version"], output / "engine-version.log", env).strip()
    if not version.startswith("4.7.2.stable.official.ed1daf0bf"):
        raise ValueError(f"Unexpected engine {version}")
    run([godot, "--headless", "--path", stage, "--import"], output / "portable-import.log", env)
    pack = game / f"{APP}.pck"
    # Export the standalone resource pack and use the byte-exact official
    # template executable beside it. The project has no installer.
    run([godot, "--headless", "--path", stage, "--export-pack", "Windows Playtest", pack],
        output / "portable-export.log", env)
    exe = game / f"{APP}.exe"
    os.link(template, exe)
    binary_version = run([exe, "--version"], output / "template-version.log", env).strip()
    if binary_version != version:
        raise RuntimeError(f"Template reports {binary_version}, expected {version}")
    smoke = run([exe, "--rendering-method", "mobile", "--", "--verify-portable"], output / "portable-smoke.log", env, timeout=100)
    if "PORTABLE|DONE|0" not in smoke or sum("|two_seats=true|assets=true" in line for line in smoke.splitlines()) != 4:
        raise RuntimeError(f"Incomplete exported executable verification\n{smoke[-5000:]}")
    run([exe, "--headless", "--quit-after", "3", "--", "--controller-trace"], output / "portable-trace.log", env, timeout=30)
    trace = game / "controller-trace.jsonl"
    if not trace.is_file() or json.loads(trace.read_text(encoding="utf-8").splitlines()[0])["event"] != "ready":
        raise RuntimeError("Exported trace did not start")
    write(game / "Read me.txt", README)
    write(game / "Start Controller Test.cmd", '@echo off\nstart "" "%~dp0Reef Grand Prix.exe" -- --controller-trace\n')
    shutil.copyfile(ROOT / "ASSET_LICENSES.md", game / "Asset credits.md")
    notices = run([godot, "--headless", "--path", stage, "-s", "res://diagnostics/licenses.gd"],
                  output / "license-output.log", env)
    write(game / "Godot notices.txt", notices)
    contents = [exe, pack, game / "Read me.txt", game / "Start Controller Test.cmd",
                game / "Asset credits.md", game / "Godot notices.txt"]
    provenance = {"engine": version, "portable_runtime_files": len(paths), "source_head": subprocess.check_output(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip(),
        "staged_source_sha256": {path: sha(stage / path) for path in paths if (stage / path).is_file()},
        "generated_entry_and_metadata": {p: sha(stage / p) for p in (
            "project.godot", "portable.tscn", "portable_entry.gd", "controller_trace.gd", "export_presets.cfg",
            "scripts/racer_game_2d.gd", "scenes/main.tscn", "exit_portable.gd")},
        "package_members": {path.name: sha(path) for path in contents}}
    info = game / "Build info.json"
    write(info, json.dumps(provenance, indent=2) + "\n")
    contents.append(info)
    archive = output / "Reef-Grand-Prix-Windows-x64.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as bundle:
        for path in contents:
            bundle.write(path, f"{APP}/{path.name}")
    with zipfile.ZipFile(archive) as bundle:
        if bundle.testzip() is not None:
            raise RuntimeError("ZIP checksum verification failed")
    receipt = {"zip_sha256": sha(archive), "zip_bytes": archive.stat().st_size,
               "pck_sha256": sha(pack), "template_sha256": sha(template),
               "smoke_log_sha256": sha(output / "portable-smoke.log"),
               "build_info_sha256": sha(info), "trace_log_sha256": sha(trace),
               "standalone_course_count": 4, "godot": version}
    write(output / "receipt.json", json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--godot", type=Path, required=True)
    parser.add_argument("--template", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    build(args.output.resolve(), args.godot.resolve(), args.template.resolve())
