"""Apply Resolve's standard video transition at a named edit point."""

from __future__ import annotations

import argparse
import ctypes
import time

from resolve_bridge_client import ResolveBridgeClient


VK_CONTROL = 0x11
VK_T = 0x54
VK_V = 0x56
KEYEVENTF_KEYUP = 0x0002


def tap(user32: ctypes.WinDLL, key: int) -> None:
	user32.keybd_event(key, 0, 0, 0)
	time.sleep(0.05)
	user32.keybd_event(key, 0, KEYEVENTF_KEYUP, 0)


def main() -> None:
	parser = argparse.ArgumentParser()
	parser.add_argument("timecode")
	args = parser.parse_args()
	client = ResolveBridgeClient()
	if not client.call("OpenPage", "edit"):
		raise RuntimeError("Resolve could not open the Edit page")
	if not client.call("SetCurrentTimecode", args.timecode, target="current_timeline"):
		raise RuntimeError(f"Resolve rejected timecode {args.timecode}")
	user32 = ctypes.windll.user32
	hwnd = user32.FindWindowW(None, "DaVinci Resolve - Mermaid Roshan - Luna Editorial Recut 2026-08-23 v5")
	if not hwnd:
		# Resolve's project title can include additional timeline text; use the
		# bridge-started process window when an exact caption is unavailable.
		import psutil

		for process in psutil.process_iter(["name"]):
			if (process.info["name"] or "").lower() == "resolve.exe":
				hwnd = user32.FindWindowW("Qt673QWindowIcon", None)
				break
	if not hwnd:
		raise RuntimeError("Resolve main window not found")
	user32.ShowWindow(hwnd, 9)
	user32.SetForegroundWindow(hwnd)
	time.sleep(0.6)
	# V selects the edit nearest the playhead; Ctrl+T applies the standard
	# video transition to that selected edit.
	tap(user32, VK_V)
	time.sleep(0.25)
	user32.keybd_event(VK_CONTROL, 0, 0, 0)
	tap(user32, VK_T)
	user32.keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, 0)
	time.sleep(1.0)
	client.call("SaveProject", target="project_manager")
	print(args.timecode)


if __name__ == "__main__":
	main()
