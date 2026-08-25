"""Apply Resolve's standard transition at a v2 edit point."""

from __future__ import annotations

import argparse
import ctypes
import sys
import time
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
sys.path.insert(0, str(PACKAGE.parent))

from resolve_bridge_client import ResolveBridgeClient  # noqa: E402
from otter_recut_v2_plan import PROJECT_NAME  # noqa: E402


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
	if client.request("health")["current_project"] != PROJECT_NAME:
		raise RuntimeError("Wrong active project")
	if not client.call("OpenPage", "edit"):
		raise RuntimeError("Resolve could not open Edit page")
	if not client.call("SetCurrentTimecode", args.timecode, target="current_timeline"):
		raise RuntimeError(f"Resolve rejected {args.timecode}")
	user32 = ctypes.windll.user32
	title = f"DaVinci Resolve - {PROJECT_NAME}"
	hwnd = user32.FindWindowW(None, title)
	if not hwnd:
		raise RuntimeError(f"Resolve window not found: {title}")
	user32.ShowWindow(hwnd, 9)
	user32.SetForegroundWindow(hwnd)
	time.sleep(0.6)
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
