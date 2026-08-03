class_name DaySystem
extends RefCounted
# The days system.
#
# OWNER 2026-08-03, DEV-PROCESS DECISION: days are selected from the pause
# menu, and **the player is on NO DAY by default**. Free Play is the shipped
# state; a day is something you deliberately step into while the day content is
# being built. This will be replaced by real story progression later — until
# then nothing may auto-enter a day, and nothing may auto-leave one.
#
# Everything day-gated asks this one class what day it is, so when the selector
# is replaced by story progression there is a single call site to change.
#
# Satellite rules (CLAUDE.md): logic only, `main` by reference, state on main.

const NO_DAY := ""

# The roster the pause selector cycles through, in order, starting at Free
# Play. Adding a day is one row here plus its own content — the selector, the
# save round-trip and the probe all read this table.
const DAYS: Array[Dictionary] = [
	{"id": NO_DAY, "name": "Free Play", "label": "✦   FREE PLAY"},
	{"id": "day_one", "name": "Day One", "label": "①   DAY ONE"},
]

var m: ReefMain

func _init(main: ReefMain) -> void:
	m = main

static func day_record(day_id: String) -> Dictionary:
	for day: Dictionary in DAYS:
		if String(day["id"]) == day_id:
			return day
	return DAYS[0]

# The one question every piece of day-gated content asks.
static func is_day(main: ReefMain, day_id: String) -> bool:
	return main.current_day == day_id

func current() -> String:
	return m.current_day

func label() -> String:
	return String(day_record(m.current_day)["label"])

func day_name() -> String:
	return String(day_record(m.current_day)["name"])

func next_id() -> String:
	# Free Play is index 0, so cycling always passes back through it: there is
	# never a day you cannot leave.
	for i in range(DAYS.size()):
		if String(DAYS[i]["id"]) == m.current_day:
			return String(DAYS[(i + 1) % DAYS.size()]["id"])
	return NO_DAY

func set_day(day_id: String) -> void:
	var resolved: String = String(day_record(day_id)["id"])
	if resolved == m.current_day:
		return
	m.current_day = resolved
	m.save_data["current_day"] = resolved
	m._write_save()
	# Re-enter the current area so the new day's content builds. Day-gated
	# pieces are decided at build time, not polled per frame, so a plain state
	# flip would leave the world showing the previous day until the next
	# transition.
	if m.game == "level2" and String(m.g.get("phase", "")) == "promenade":
		m._enter_level2_now(false, false, bool(m.g.get("ocean_gate_hub", true)))

func cycle() -> void:
	set_day(next_id())
