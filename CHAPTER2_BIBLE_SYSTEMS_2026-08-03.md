# CHAPTER 2 STORY LAYER — EXACT BUILD PLAN

Read: `audio_director.gd`, `opera_act.gd` (7193 lines), `opera_career_world_2d.gd` (1700), `opera_house.gd`, `opera_lobby_2d.gd`, `save_state.gd`, `probe_opera_2d.gd`, `main.gd`, plus `opera_stage_paths.gd`, `opera_competition.gd`, `arena/castle_rooms_25d.gd`, `probe_castle_pearl_art.gd`. All paths below are under `C:/Users/Peter/Documents/mermaid-roshan-reef/.worktrees/codex-opera-art-regeneration/`.

---

## 0. FIVE FACTS THAT DECIDE THE DESIGN (verified in code, not assumed)

**0.1 — The caption is INVISIBLE for the whole opera.** `main.gd:2903-2904` (`_start_opera_now`) does `hud_layer.visible = false`; `main.gd:2916-2917` (`_end_opera`) restores it. `hud_msg` is a child of `hud_layer` (`main.gd:3034`, built into `cl` at `main.gd:3005-3007`). Nothing re-shows it inside the opera. So every `m.show_msg()` in the opera today is **voice-only** — the text is written to a hidden Label. Consequence: "caption contention" is really **voice-pool contention**, and any visible story text must be drawn by a node the opera itself owns. See §2.6 for the one-node fix.

**0.2 — The shipping path splits shows/bosses.** `opera_act.gd:530-536`: `use_career_world_2d = kind == "nursery" or (kind != "boss" and (DisplayServer.get_name() != "headless" or force_2d or OPERA_FORCE_2D))`. On a display build: **13 careers → 2D career world**, **3 floor bosses → the legacy 3D `OperaAct` theatre**. Both must carry story beats.

**0.3 — `say_sequence` REPLACES the queue.** `audio_director.gd:52` `m.dialogue_queue = lines.duplicate(true)`. A second call mid-sequence destroys the first. Every append must be done as `say_sequence(m.dialogue_queue + new_lines, m.dialogue_t)` — passing `m.dialogue_t` as `opening_hold` preserves the currently-speaking line's remaining time and does not re-speak it (the current line was already popped at `audio_director.gd:64`). This is the entire append mechanism; **AudioDirector needs no change**.

**0.4 — `steal_index == FINALE_START − 1` for every one of the 13 careers.** Verified across `PHASES` + `FINALE_START` (`opera_career_world_2d.gd:36-167`). Ten careers have 7 phases (`steal_index` 4, `_finale_start()` 5); three (boxer, racer, popstar) have 6 (`steal_index` 3, `_finale_start()` 4). Therefore the job phases are always `1 .. steal_index-1`, and **`STATION_n` maps to `phase_index` directly** (`STATION_1..3` for 7-phase careers, `STATION_1..2` for 6-phase).

**0.5 — `opera_pantry` is the save-safe flag home; no new key is needed.** It is already in `KNOWN_KEYS` (`save_state.gd:34`), normalised as a free-form Dictionary (`save_state.gd:465-466`), loaded at `save_state.gd:132-133`, written at `save_state.gd:207`, and round-trip-covered by `probe_load.gd:6`. Critically, **nothing iterates it** — `castle_rooms_25d.gd:3319/3346` do key-specific lookups against `KITCHEN_RECIPES` / `KITCHEN_FOOD_ICONS`, and `probe_castle_pearl_art.gd:1470/1492` assert only on `carrots`/`sugar`. Adding `ch2_open` / `ch2_party` keys is inert everywhere.

---

## 1. `scripts/opera_story.gd` — THE DATA SATELLITE

### 1.1 Shape

```gdscript
class_name OperaStory
extends RefCounted
## Chapter 2 story layer: PURE DATA + three speak helpers. No nodes, no
## _process, no signals, no gameplay state. Nothing in this file may read or
## write anything except m.dialogue_* (through say_sequence) and — in the two
## clearly marked chapter helpers — m.opera_pantry. Every runtime object stays
## where it already lives (satellite rule, audio_director.gd:46).

# ---- trigger names (STATION_n is built as "STATION_%d" % n) ----
const ACT_OPEN      := "ACT_OPEN"
const SCUFFLE       := "SCUFFLE"
const STEAL         := "STEAL"
const FINALE_OPEN   := "FINALE_OPEN"
const FINALE_MID    := "FINALE_MID"
const CURTAIN_CALL  := "CURTAIN_CALL"
const LOBBY_RETURN  := "LOBBY_RETURN"
const CHAPTER_OPEN  := "CHAPTER_OPEN"
const PARTY         := "PARTY"
const CRASH         := "CRASH"

# ---- save flags (existing opera_pantry key only — never a new save key) ----
const FLAG_CHAPTER_OPEN := "ch2_open"
const FLAG_PARTY        := "ch2_party"

# ---- the party table: the 13 SHOW acts in lobby display order ----
# (mirrors OperaLobby2D.SHOW_INDICES flattened; bosses are NOT party pieces)
const PARTY_ORDER := [0, 1, 2, 3, 5, 6, 7, 8, 10, 11, 12, 15, 13]

const PIECES := {
	"chef":       {"emoji": "🎂", "piece": "birthday cake"},
	"detective":  {"emoji": "👑", "piece": "pearl tiara"},
	"ballerina":  {"emoji": "🎶", "piece": "music box"},
	"candymaker": {"emoji": "🍬", "piece": "party candy"},
	"doctor":     {"emoji": "🧸", "piece": "starfish plushy"},
	"farmer":     {"emoji": "🐷", "piece": "party piggy"},
	"boxer":      {"emoji": "🥇", "piece": "champion belt"},
	"magician":   {"emoji": "🎩", "piece": "Lamba's big trick"},
	"painter":    {"emoji": "🖼", "piece": "sunrise painting"},
	"astronaut":  {"emoji": "🚀", "piece": "party rocket"},
	"racer":      {"emoji": "🏆", "piece": "shell trophy"},
	"nursery":    {"emoji": "🌙", "piece": "star mobile"},
	"popstar":    {"emoji": "🎤", "piece": "golden microphone"},
}
```

**Beat table — keyed by career slug + trigger.** One dictionary, thirteen career keys plus three boss keys. Missing trigger key ⇒ empty array ⇒ no beat. Nothing else in the codebase ever has to know a trigger exists.

```gdscript
const BEATS := {
	"chef": {
		ACT_OPEN: [
			{"who": "Roshan", "hold": 3.2, "vo": "st_chef_open_1",
			 "text": "It's my birthday! And the very best part is making my OWN cake."},
			{"who": "Princess Huluu", "hold": 3.2, "vo": "st_chef_open_2",
			 "text": "Then I shall be your kitchen helper, birthday girl. Hat on!"},
		],
		"STATION_1": [{"who": "Princess Huluu", "hold": 2.8, "vo": "st_chef_st1_1",
			"text": "Pour slowly — a birthday cake likes to be poured slowly."}],
		"STATION_2": [{"who": "Roshan", "hold": 2.8, "vo": "st_chef_st2_1",
			"text": "Round and round! This is going to be the tallest cake in the ocean."}],
		STEAL: [{"who": "Princess Huluu", "hold": 2.6, "vo": "st_chef_steal_1",
			"text": "He's taking your birthday cake to the STAGE! After him!"}],
		CURTAIN_CALL: [{"who": "Roshan", "hold": 2.8, "vo": "st_chef_bow_1",
			"text": "One birthday cake — on the party table it goes!"}],
	},
	# ... 12 more career keys, same five bespoke triggers ...
	"dragon":  { ACT_OPEN: [...], STEAL: [...], CURTAIN_CALL: [...] },
	"phantom": { ... },
	"maestro": { ... },
}

# Shared, deterministic pools (no RNG — matches the "never luck" rule at
# opera_career_world_2d.gd:798). Chosen by act_index % size.
const SCUFFLE_POOL := [ 4 lines ]        # the imps arrive
const FINALE_POOL  := [ 5 lines ]        # Imp Captain taunts from the boards
const TABLE_POOL   := [ 4 lines ]        # LOBBY_RETURN: the piece lands on the table

const CHAPTER := {
	CHAPTER_OPEN: [ 6 lines ],
	PARTY:        [ 8 lines ],
	CRASH:        [ 6 lines ],
}

# Replay friction (see §5)
const REPLAY_TRIGGERS := [ACT_OPEN, STEAL, CURTAIN_CALL]
const REPLAY_MAX_LINES := 1
```

### 1.2 How the runtime looks a beat up and fires it

```gdscript
static func key_for(config: Dictionary) -> String:
	# shows are keyed by costume; the three bosses have costume "" and are
	# keyed off their career name (opera_house.gd:45/74/103)
	var costume := String(config.get("costume", ""))
	if costume != "":
		return costume
	var career := String(config.get("career", "")).to_lower()
	if "dragon" in career: return "dragon"
	if "phantom" in career: return "phantom"
	if "maestro" in career: return "maestro"
	return ""


static func lines_for(trigger: String, config: Dictionary, replay: bool) -> Array:
	var key := key_for(config)
	var act_index := int(config.get("act_index", -1))
	var out: Array = []
	if trigger == SCUFFLE:
		out = [SCUFFLE_POOL[maxi(0, act_index) % SCUFFLE_POOL.size()]]
	elif trigger == FINALE_OPEN:
		out = [FINALE_POOL[maxi(0, act_index) % FINALE_POOL.size()]]
	elif trigger == LOBBY_RETURN:
		out = [TABLE_POOL[maxi(0, act_index) % TABLE_POOL.size()]]
	else:
		out = ((BEATS.get(key, {}) as Dictionary).get(trigger, []) as Array)
	if replay:
		if not (trigger in REPLAY_TRIGGERS):
			return []
		out = out.slice(0, REPLAY_MAX_LINES)
	return out.duplicate(true)


## THE ONE FIRE FUNCTION. Non-blocking, timer-advanced, touch-skippable,
## APPENDS instead of clobbering. Safe to call from any thread of the flow.
static func fire(m, trigger: String, config: Dictionary,
		opening_hold: float = 0.0, replay: bool = false) -> void:
	if m == null:
		return
	var lines := lines_for(trigger, config, replay)
	if lines.is_empty():
		return
	_speak(m, lines, opening_hold)


## THE ONE INSTRUCTION FUNCTION. An instruction NEVER interrupts a story
## beat — it is appended as the queue's tail so the child always hears
## "why" then "what to do", and it is the line left standing when the queue
## drains (show_msg sets msg_timer = 5.0, audio_director.gd:119).
static func instruct(m, who: String, text: String, vo: String,
		hold: float = 5.0) -> void:
	if m == null:
		return
	if not m.dialogue_active:
		m.show_msg(who, text, vo)
		return
	_speak(m, [{"who": who, "text": text, "vo": vo, "hold": hold}], 0.0)


static func _speak(m, lines: Array, opening_hold: float) -> void:
	if m.dialogue_active:
		# audio_director.gd:52 REPLACES the queue — rebuild it head-first and
		# hand back the current line's remaining time as the opening hold, so
		# the line being spoken right now is neither cut nor repeated.
		var queued: Array = (m.dialogue_queue as Array).duplicate(true)
		queued.append_array(lines)
		m.say_sequence(queued, maxf(opening_hold, m.dialogue_t))
		return
	m.say_sequence(lines.duplicate(true), opening_hold)


## Seconds of speech still owed — used to size OperaAct.win_t (§2.7).
static func queued_seconds(m) -> float:
	if m == null or not m.dialogue_active:
		return 0.0
	var total := m.dialogue_t
	for line: Dictionary in (m.dialogue_queue as Array):
		total += maxf(0.8, float(line.get("hold", 3.2)))
	return total
```

### 1.3 The only two functions that write

```gdscript
## Chapter open — the first time the child EVER enters the Pearl Opera.
## Uses only existing save keys (opera_stars + opera_pantry).
static func try_chapter_open(m) -> bool:
	if m == null:
		return false
	if m.opera_stars != 0:
		return false            # any prior star ⇒ not the first visit
	if int(m.opera_pantry.get(FLAG_CHAPTER_OPEN, 0)) != 0:
		return false            # already seen, even with zero stars
	m.opera_pantry[FLAG_CHAPTER_OPEN] = 1
	m._write_save()
	_speak(m, (CHAPTER[CHAPTER_OPEN] as Array).duplicate(true), 0.0)
	return true


## Party climax + crash. The CALLER decides "first time" (see §3.2) and has
## already folded the flag into its own _write_save, so this only speaks.
static func fire_party_and_crash(m) -> void:
	var lines: Array = (CHAPTER[PARTY] as Array).duplicate(true)
	lines.append_array(CHAPTER[CRASH] as Array)
	_speak(m, lines, 1.2)
```

### 1.4 How it stays a pure satellite

- `extends RefCounted`, every function `static`. It is **never instantiated, never added to the tree, never preloaded as a scene**. Call sites use the global class name `OperaStory.fire(...)` — same pattern as `StorybookUI` / `ImpAI`.
- It touches exactly four things on `m`: `say_sequence`, `show_msg`, `dialogue_active`/`dialogue_queue`/`dialogue_t` (read only, in `_speak`), and `opera_pantry` + `_write_save` (only inside `try_chapter_open`).
- It **never** touches `phase_index`, `phase_progress`, `active`, `rival_actor`, `competition`, `PHASES`, `FINALE_START`, or any node. That is what keeps every `probe_opera_2d` assertion intact (§7.1).
- **Hard rule to write into the file header: OperaStory may never add an entry to `OperaCareerWorld2D.PHASES`.** `probe_opera_2d.gd:96` asserts `modes[0] == "bop"` and `:102` asserts the captain scuffle sits strictly inside `[1, _finale_start())` with a bigger goal than phase 0. A story "phase" would break both.

---

## 2. EXACT CALL SITES PER TRIGGER

**The universal ordering rule:** *story first, instruction last.* Every phase instruction goes through `OperaStory.instruct()`, which appends behind whatever story is live. Every reactive one-off line (captain spawn, rally, telegraph, idle re-hint, lobby hints) gets a `not m.dialogue_active` guard so it never talks over a story beat.

### 2.1 `ACT_OPEN` — `opera_act.gd`, inside `start()`

This is also **the fix for the known defect** (§7.4). Replace lines **537-540**:

```gdscript
	# the Showtime announcement belongs to BOTH paths. Queued BEFORE the world
	# builds so [act open story ...] → [career voice] → [phase-1 instruction]
	# come out in narrative order instead of clobbering one another.
	OperaStory.fire(m, OperaStory.ACT_OPEN, config, 0.0, _story_replay())
	if use_career_world_2d:
		OperaStory.instruct(m, "Roshan",
			String(config.get("voice", "It's showtime! Follow the golden sparkle!")),
			"act_open", 3.6)
		_start_career_world_2d()
		if use_career_world_2d:
			return
```

and replace the 3D tail at lines **589-592** (the `_sparkle_burst` calls at 587-588 stay put):

```gdscript
	if stage_phase == "brawl":
		OperaStory.instruct(m, "Roshan", "Oh no — mischief imps snuck backstage! Pop them with SPARKLE so the show can start!", "talk")
	else:
		OperaStory.instruct(m, "Roshan", String(config.get("voice", "It's showtime! Follow the golden sparkle!")), "talk")
```

New helper on `OperaAct` (one line, used by every `fire` in this file):

```gdscript
func _story_replay() -> bool:
	var i := int(config.get("act_index", -1))
	return i >= 0 and (m.opera_stars & (1 << i)) != 0
```

Enabler — `opera_house.gd:625-626` in `_start_act()`:

```gdscript
	var cfg: Dictionary = (ACTS[i] as Dictionary).duplicate()
	cfg["act_tag"] = String(cfg["name"]) + "  "
	cfg["act_index"] = i          # ← ADD. story lookup + replay friction.
```

`probe_opera_2d.gd:59-60` builds `config` straight from `OperaHouse.ACTS` and never sets `act_index`, so it defaults to `-1` ⇒ `_story_replay()` false ⇒ **the probe always exercises the longest story path**, which is what you want for the guard budget.

### 2.2 `SCUFFLE`, `STATION_n`, `STEAL`, `FINALE_OPEN`, `FINALE_MID` — `opera_career_world_2d.gd`, inside `_show_phase()`

Replace the tail of `_show_phase()` (lines **724-727**):

```gdscript
	phase_label.text = "%s   %s" % [String(phase.get("icon", "★")), String(phase.get("name", "PLAY"))]
	phase_fill.value = 0.0
	if m != null:
		var trigger := _story_trigger()
		if trigger != "" and not story_fired.has(trigger):
			story_fired[trigger] = true          # guards the detective re-entry
			OperaStory.fire(m, trigger, config, 0.0, _story_replay())
		OperaStory.instruct(m,
			String(phase.get("speaker", "Roshan")),
			String(phase.get("voice", "Follow the golden sparkle!")),
			String(phase.get("vo", "hint")))
```

New members and helper on `OperaCareerWorld2D`:

```gdscript
var story_fired: Dictionary = {}

func _story_replay() -> bool:
	var i := int(config.get("act_index", -1))
	return i >= 0 and (m.opera_stars & (1 << i)) != 0

func _story_trigger() -> String:
	# fact 0.4: steal_index == _finale_start() - 1 for all thirteen careers,
	# so the job phases are exactly 1 .. steal_index-1 and STATION_n == n.
	if phase_index == 0:
		return OperaStory.SCUFFLE
	if phase_index == steal_index:
		return OperaStory.STEAL
	if phase_index == _finale_start():
		return OperaStory.FINALE_OPEN
	if phase_index == _finale_start() + 1:
		return OperaStory.FINALE_MID
	if phase_index > 0 and phase_index < steal_index:
		return "STATION_%d" % phase_index
	return ""
```

**Why the `story_fired` guard is mandatory:** `_process()` at **line 1687-1691** sets `phase_index = _finale_start()` and calls `_show_phase()` again after the detective's guided retry. Without the guard, `FINALE_OPEN` fires twice and `probe_opera_2d.gd:148-151` runs straight through it.

**Ordering against the existing instruction:** the story `fire` is unconditionally *before* the `instruct`, and `instruct` appends rather than overwrites. There is no window in which the two fight.

**Do NOT move the `_glide_roshan_to` / `_start_stage_combat` / prop-flee tween calls** — they already run above this block and must keep running on the same frame the phase changes (the theft tween at lines 713-720 is the visual the STEAL beat narrates).

### 2.3 `CURTAIN_CALL` — `opera_act.gd`, inside `_win()`

Replace the 2D branch (lines **7038-7049**):

```gdscript
	if use_career_world_2d:
		if competition != null:
			_competition_curtain_call()     # celebrate(): prop flies home, confetti
		var world_win_line := String(config.get("win_line", "What a show! Everybody is cheering!"))
		if not performance_result.is_empty():
			if competition != null and competition.is_cooperative():
				world_win_line += " %s for the nursery team!" % String(performance_result.get("cheer", "Big cheers"))
			else:
				world_win_line += " %s for Mermaid Roshan!" % String(performance_result.get("cheer", "Big cheers"))
		m.show_msg("Roshan", world_win_line, "win")            # existing payoff, immediate
		OperaStory.fire(m, OperaStory.CURTAIN_CALL, config, 3.0, _story_replay())
		win_t = clampf(3.2 + OperaStory.queued_seconds(m), 3.2, 12.0)
		return
```

`opening_hold = 3.0` lets the win line be heard before the story beat starts. `win_t` is grown to cover the queue so `_finish()` (`opera_act.gd:7088`, driven from `_process` line 6440-6442) can't cut the bow short. Apply the same `win_t = clampf(2.6 + queued, 2.6, 12.0)` at line **7052** for the three bosses.

**CURTAIN_CALL is the only trigger where story comes AFTER the existing line** — the win line *is* the beat's setup.

### 2.4 `LOBBY_RETURN` — `opera_house.gd`, inside `_return_to_lobby()`

Change the signature at line **669** to `func _return_to_lobby(finished: int, party: bool = false) -> void:` (only caller is `_act_won`), then replace lines **679-685**:

```gdscript
		var rcfg: Dictionary = (ACTS[finished] as Dictionary).duplicate()
		rcfg["act_index"] = finished
		if party:
			_begin_party_night()                                   # §3.2
		elif (finished == 4 or finished == 9) and m.opera_stars != ALL_STARS:
			m.show_msg("Roshan", "The next floor just lit up! Tap its bright number at the top!", "win")
		elif m.opera_stars == ALL_STARS:
			m.show_msg("Roshan", "Every show and every big finale! Take a bow, Opera Star Roshan!", "win")
		else:
			OperaStory.fire(m, OperaStory.LOBBY_RETURN, rcfg, 0.6,
				(m.opera_stars & (1 << finished)) != 0)
			OperaStory.instruct(m, "Roshan", "A gold star for that show! Tap the next sparkling picture!", "win")
		return
```

Mirror the same `party` branch in the 3D tail at lines **709-719**.

Note the replay argument here is *always* true (the star was just set at `opera_house.gd:658`), so `LOBBY_RETURN` always plays its single pooled line. That is intentional — the piece landing on the table is the one beat the child should hear every single time.

### 2.5 The `not m.dialogue_active` guards (the "never fight the slot" rule)

Add `if not m.dialogue_active:` in front of these seven existing `show_msg` calls. None of them is an instruction; all are reactive colour.

| File | Line | Call |
|---|---|---|
| `opera_career_world_2d.gd` | 864 | `_spawn_stage_captain` — "You'll have to bop ME twice!" |
| `opera_career_world_2d.gd` | 1170 | `begin_guided_retry` — "Watch the glowing answer…" |
| `opera_career_world_2d.gd` | 1432 | `_handle_brain_events` telegraph — "That imp is winding up" |
| `opera_career_world_2d.gd` | 1443 | `_handle_brain_events` rally — "Crew! Back to me!" |
| `opera_career_world_2d.gd` | 1663 | 9s idle re-hint |
| `opera_house.gd` | 195 / 198 | `_lobby_locked_hint` |
| `opera_lobby_2d.gd` | 285 | `_choose_floor` |

For the idle re-hint at **1656-1663** also freeze the clock, so a long story beat doesn't queue a re-hint the instant it ends:

```gdscript
		if m != null and m.dialogue_active:
			idle_t = 0.0
		else:
			idle_t += delta
			if idle_t >= 9.0:
				idle_t = 0.0
				surface.restart_demo()
				if m != null:
					m.show_msg("Roshan", String((phases[phase_index] as Dictionary).get("voice", "Follow the golden sparkle!")), "hint")
```

### 2.6 Touch-skip wiring (currently `skip_dialogue()` has ZERO callers)

`audio_director.gd:74` and `main.gd:3237` exist but nothing calls them. Three sites:

**a) `opera_career_world_2d.gd:867 _combat_input`** — first statement, before the `active`/`combat_imps` early-out so a story beat is skippable even between scuffles:

```gdscript
func _combat_input(event: InputEvent) -> void:
	var pressed := (event is InputEventScreenTouch and (event as InputEventScreenTouch).pressed) \
		or (event is InputEventMouseButton and (event as InputEventMouseButton).pressed)
	if pressed and m != null and m.skip_dialogue():
		return
	if not active or combat_imps.is_empty():
		return
	...
```

**b) `opera_career_world_2d.gd:1017 _on_gesture`** — first statement, using the file's own probe idiom (`amount < 5.0` = a real finger; the probe pumps `100.0`, see line 1061 for the precedent):

```gdscript
func _on_gesture(_kind: String, amount: float, quality: float) -> void:
	if amount < 5.0 and m != null and m.skip_dialogue():
		return
	if not active or reveal_t > 0.0 or phase_index >= phases.size():
		return
```

**This `amount < 5.0` gate is not optional.** `probe_opera_2d.gd:135-138` runs an **unguarded** `while world.phase_index < world._finale_start()` loop pumping `_on_gesture("probe", 100.0, 1.0)`. If a story beat could swallow those pumps, that loop hangs the probe forever.

**c) `opera_lobby_2d.gd`** — add to `_build()` and a new method. `_unhandled_input` never sees taps that Buttons consume, so this cannot steal a card press:

```gdscript
	root.set_process_unhandled_input(true)   # in _build()

func _unhandled_input(event: InputEvent) -> void:
	if not accepting_input or m == null:
		return
	var pressed := (event is InputEventScreenTouch and (event as InputEventScreenTouch).pressed) \
		or (event is InputEventMouseButton and (event as InputEventMouseButton).pressed)
	if pressed:
		m.skip_dialogue()
```

### 2.7 Queue teardown (mandatory — see §7.3)

`m.clear_dialogue()` as the **first** statement of:
- `opera_act.gd:7088 _finish()` — both branches
- `opera_act.gd:7119 cancel()` — both branches
- `opera_house.gd:903 _finish()`

Without this, `probe_opera_2d` accumulates thirteen acts of undrained queue and, on a display build, voices bleed from one show into the next and out into the reef.

### 2.8 Optional: make the story visible (one node)

`hud_msg` is hidden for the whole opera (fact 0.1). If the owner wants the words on screen — the child is a non-reader, so this is a *nice-to-have*, not a requirement — add to `OperaCareerWorld2D._build_world()` and to `OperaLobby2D._build()`:

```gdscript
	story_caption = _label("", 26, Color(1.0, 0.97, 0.88))
	story_caption.name = "OperaStoryCaption"
	story_caption.position = Vector2(180, 636)
	story_caption.size = Vector2(920, 74)
	story_caption.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	story_caption.mouse_filter = Control.MOUSE_FILTER_IGNORE
	root.add_child(story_caption)
```
and in `_process`: `story_caption.text = m.hud_msg.text if m.hud_msg != null else ""`. It mirrors the hidden slot, so nothing new can ever disagree with the voice. **It must be a `Label`, not a `Node3D`** — `probe_opera_2d.gd:32` asserts `house.find_children("*", "Node3D", true, false).is_empty()`.

---

## 3. CHAPTER OPEN AND PARTY CLIMAX + CRASH

### 3.1 CHAPTER_OPEN — once, on the first opera entry ever

**Site:** `opera_house.gd`, top of `start()` (line 147), so it covers the 2D lobby *and* the headless 3D lobby with one call:

```gdscript
func start(main: ReefMain, checkpoint: int, done_cb: Callable) -> void:
	m = main
	finish_cb = done_cb
	var chapter_opened := OperaStory.try_chapter_open(m)   # ← ADD
	use_lobby_2d = (...)
```

Then route the welcome line so the chapter open isn't clobbered — `opera_house.gd:191`:

```gdscript
	OperaStory.instruct(m, "Roshan", "Welcome to the Pearl Opera! Tap a picture to choose our next show!", "talk")
```
(same change at `opera_house.gd:169` for the 3D lobby).

**Save-safe "first time" condition, existing keys only:**
```gdscript
m.opera_stars == 0 and int(m.opera_pantry.get("ch2_open", 0)) == 0
```
- `opera_stars == 0` means a pre-existing save with progress can **never** retro-fire the chapter open on the build that ships this.
- `opera_pantry["ch2_open"] = 1` + `m._write_save()` makes it fire exactly once even if the child enters, hears it, leaves without winning anything, and comes back.
- No new save key. `opera_pantry` is already in `KNOWN_KEYS` (`save_state.gd:34`), already defaulted to `{}` in `_normalise_save` (`save_state.gd:465-466`), and is **not** in `CORE_KEYS`, so an old save missing the flag still loads clean (`save_state.gd:378-381`).

### 3.2 PARTY + CRASH — once, after the final star

**Which star is "final":** `ALL_STARS = (1 << 16) - 1` (`opera_house.gd:118`) is all sixteen ACTS. Floor 3's boss (index 14) is gated on all five Grand Gallery shows (`_floor_shows_starred`, `opera_house.gd:557-563` / `opera_lobby_2d.gd:323-327`), so **index 14, the Midnight Maestro, is always the last star.** The party therefore lands directly on top of "the Maestro just wanted to conduct the grand finale" — the house-law win line already there.

**Site A — `opera_house.gd:653-667 _act_won()`**, folding the flag into the existing single write:

```gdscript
func _act_won() -> void:
	var finished := act_index
	act = null
	act_index = -1
	var first_time: bool = (m.opera_stars & (1 << finished)) == 0
	m.opera_stars |= 1 << finished
	m.pearl_count += 3 if first_time else 1
	m.opera_progress = _star_count()
	if m.opera_stars == ALL_STARS and not m.opera_done:
		m.opera_done = true
		m.pearl_count += 50
		m.award_sticker("showtime")
	# CHAPTER 2 CLIMAX — the party happens, then it is ruined. Once, ever.
	var party := m.opera_stars == ALL_STARS \
		and int(m.opera_pantry.get(OperaStory.FLAG_PARTY, 0)) == 0
	if party:
		m.opera_pantry[OperaStory.FLAG_PARTY] = 1
	m._write_save()                # ← already here; now also lands the flag
	m._update_hud()
	_return_to_lobby(finished, party)
```

`award_sticker` at `main.gd:329-340` calls `_write_save()` itself, so the flag must be set **before** the `if m.opera_stars == ALL_STARS` block or after — either is fine because the block's write already happens first; setting it before line 661 is simplest and is what I wrote above (placed after, which still lands via the explicit `_write_save()` at line 665).

**Save-safe condition, existing keys only:** `m.opera_stars == ALL_STARS and int(m.opera_pantry.get("ch2_party", 0)) == 0`. Deliberately **not** `not m.opera_done` — an existing save could already carry `opera_done = true` from before this build, and that child must still get her party.

**Site B — the presentation, `opera_house.gd`, new method called from `_return_to_lobby`:**

```gdscript
func _begin_party_night() -> void:
	# the whole cast is present, the table is full, the imps are finally
	# invited — and then the true antagonist arrives. The overlay blocks the
	# lobby cards for exactly as long as the queue lasts, and every tap
	# advances a line so nothing is ever a wall.
	if lobby_2d != null and is_instance_valid(lobby_2d):
		lobby_2d.begin_party_night()      # dims the picker, lights the table
	for i in range(14):
		m._sparkle_burst(L + Vector3(randf_range(-30.0, 30.0), randf_range(3.0, 40.0), randf_range(-18.0, 18.0)), Color.from_hsv(randf(), 0.5, 1.0))
	OperaStory.fire_party_and_crash(m)
```

`OperaLobby2D.begin_party_night()` adds one `ColorRect` named `PartyNightOverlay` as the **last** child of `root` with `MOUSE_FILTER_STOP`, tweens `color` gold→warm across the eight PARTY lines then hard to `Color(0.20, 0.04, 0.06, 0.72)` for the CRASH, sets `accepting_input = false`, and in `_process` removes itself and restores `accepting_input = true` when `m.dialogue_active` goes false. Because it is `MOUSE_FILTER_STOP` and sits above the cards, `_unhandled_input` (§2.6c) still receives the tap and skips the line — the child can walk through the whole climax at her own pace but cannot accidentally launch a show mid-party.

**Cost:** 14 lines × ~3.0s ≈ 42s if never tapped, ~10s at a typical toddler tap rate. This is the one place in Chapter 2 where a long uninterrupted beat is correct.

---

## 4. PARTY TABLE IN THE LOBBY

**Which node:** a new `Panel` named `PartyTableShelf`, child of `OperaLobby2D.lower_stage`, created at the end of `_build()` (after the `boss_marks` loop, `opera_lobby_2d.gd:127-130`).

**Where:** `lower_stage` is `Rect2(22, 142, 1236, 556)` (`opera_lobby_2d.gd:86`). Cards occupy local `y 48..384`; `boss_button` occupies local `Rect2(326, 394, 584, 134)` (`:122-124`). That leaves two clean gutters at `y 394..528`. Use the left one:

```
PartyTableShelf   = Rect2(20, 392, 300, 140)   # local to lower_stage
  PartyTableTitle = Rect2(8, 6, 284, 30)       # font 20
  PartyPiece0..12 = 7 × 2 grid, cell 40 × 46,
                    origin (12, 42), step x = 41, step y = 48
                    row 0 → slots 0..6, row 1 → slots 7..12
```
`mouse_filter = Control.MOUSE_FILTER_IGNORE` on the Panel **and** every Label — it must add zero touch targets (`probe_touch_adversary` / `probe_ui_system` scan for interactable geometry). Style: `StorybookUI.panel_style(StorybookUI.GOLD, Color(0.98, 0.94, 0.86, 1.0), 28, 5)` — a gold banquet table that reads as furniture, not as a button.

**What it draws — derived purely from `opera_stars`:**

```gdscript
func _refresh_party_table() -> void:
	var made := 0
	for slot in range(OperaStory.PARTY_ORDER.size()):
		var act_index: int = int(OperaStory.PARTY_ORDER[slot])
		var cfg: Dictionary = acts[act_index]
		var piece: Dictionary = OperaStory.PIECES.get(String(cfg.get("costume", "")), {})
		var label := party_pieces[slot]
		label.text = String(piece.get("emoji", String(cfg.get("emoji", "★"))))
		var won: bool = (stars & (1 << act_index)) != 0
		label.modulate = Color(1, 1, 1, 1) if won else Color(0.62, 0.60, 0.72, 0.30)
		label.tooltip_text = String(piece.get("piece", ""))
		if won:
			made += 1
	party_title.text = "PARTY TABLE   %d / 13" % made
```

Call it as the last line of `refresh()` (`opera_lobby_2d.gd:241`, after `_update_guide()`). `refresh()` already runs on `setup()`, on every `_choose_floor`, and on every `show_lobby()` after an act (`opera_house.gd:678`), so the piece lights up on the exact frame the child returns from the show that made it — the causal link a four-year-old needs.

**Why this order:** `PARTY_ORDER` is `SHOW_INDICES` flattened (`opera_lobby_2d.gd:16`), which is the order she sees the cards in — floor 1 left-to-right, then floor 2, then floor 3 with Nursery at position 12. Bosses are deliberately absent: a floor boss is not a party piece, it is an escalation.

**Probe safety:** it is a `Panel` under a `CanvasLayer`, so `probe_opera_2d.gd:32` (`no Node3D children`) is unaffected; it is not named `RivalActor`, so `:37-40` is unaffected; it is not a `Button`, so `_visible_card_count` (`:35`, `:43`) is unaffected; `lobby.refresh(0, 0)` at `:48` must render thirteen dim cells without error, which the code above does.

**3D lobby:** `opera_house.gd:518-536 _build_hud()` already draws `★ n / 16`. Leave it — the 3D lobby is headless-regression-only (`opera_house.gd:3-4`).

---

## 5. REPLAY FRICTION

**Signal:** `(m.opera_stars & (1 << act_index)) != 0` at the moment the act starts — the star is only written in `_act_won` (`opera_house.gd:658`), so during the act the bit means "she has beaten this before". Requires `cfg["act_index"] = i` from §2.1.

**Policy, encoded as data in `opera_story.gd`:**

```gdscript
const REPLAY_TRIGGERS  := [ACT_OPEN, STEAL, CURTAIN_CALL]
const REPLAY_MAX_LINES := 1
```

Applied inside `lines_for()` (§1.2), so no call site has to know about it. Effect on a replay:

| Trigger | First play | Replay |
|---|---|---|
| ACT_OPEN | 2 lines + career voice | 1 line + career voice |
| SCUFFLE | 1 pooled | — |
| STATION_1 / 2 | 1 each | — |
| STEAL | 1 | 1 |
| FINALE_OPEN | 1 pooled | — |
| CURTAIN_CALL | 1 | 1 |
| LOBBY_RETURN | 1 pooled | 1 pooled (always) |

**≈31s of story on a first play → ≈11s on a replay.** The three kept beats are exactly the three the child replays *for*: "what am I making", "he took it!", "I got it back". The career `voice` line is never trimmed — it is the instruction that makes the job legible, and trimming it would make a replay *harder*, not shorter.

`_story_replay()` returns `false` whenever `act_index` is missing, so the probe and any direct `OperaAct.new()` caller always get the full path.

---

## 6. VO-KEY NAMING AND SPEAKER AUDIT

### 6.1 Naming

`show_msg(who, txt, vo)` → `_say(_speaker_key(who), vo, 0.5)` → the clip path is
`res://assets/audio/voices/<speaker_key>_<vo>.ogg`, with `res://assets/audio/voices/<speaker_key>.ogg` as the fallback (`audio_director.gd:22-27`).

**Scheme:** `vo = "st_" + <key> + "_" + <trigger_slug> + "_" + <n>`

| part | values |
|---|---|
| `<key>` | `chef detective ballerina candymaker doctor farmer boxer magician painter astronaut racer nursery popstar` · `dragon phantom maestro` · `ch2` (chapter) · `table` (shared) |
| `<trigger_slug>` | `open` `scuffle` `st1` `st2` `st3` `steal` `fin` `finmid` `bow` · chapter: `open` `party` `crash` |
| `<n>` | 1-based within that trigger |

Examples: `roshan_st_chef_open_1.ogg`, `evie_st_magician_steal_1.ogg`, `imp_st_table_3.ogg`, `ember_st_ch2_crash_2.ogg`.

The `st_` prefix guarantees zero collision with the existing `op_<career>_<phase>` phase keys (`opera_career_world_2d.gd:38-150`), the `op_captain` / `op_retry` reactive keys, and the generic `talk` / `hint` / `win` / `home` / `miss` events.

`_say`'s `min_gap` of 0.5s is keyed on `speaker + "_" + vo` (`audio_director.gd:14-19`), and every story key is unique, so **no story line can ever be silently swallowed by the cooldown**.

### 6.2 The 120-clip budget

| Group | Lines | Count |
|---|---|---|
| 13 careers × bespoke ACT_OPEN(2) + STATION_1(1) + STATION_2(1) + STEAL(1) + CURTAIN_CALL(1) | 6 each | **78** |
| Shared `SCUFFLE_POOL` | 4 | **4** |
| Shared `FINALE_POOL` (Imp Captain taunts) | 5 | **5** |
| Shared `TABLE_POOL` (LOBBY_RETURN) | 4 | **4** |
| 3 bosses × ACT_OPEN(1) + STEAL(1) + CURTAIN_CALL(1) | 3 each | **9** |
| `CHAPTER_OPEN` | 6 | **6** |
| `PARTY` | 8 | **8** |
| `CRASH` | 6 | **6** |
| | | **120** |

`STATION_3` and `FINALE_MID` are supported by the table and left empty — headroom for the ten 7-phase careers without re-plumbing anything.

The "clever character use" bar lives in the **78 bespoke lines**, and above all in the 13 `STEAL` lines, where the friend who *owns* the stolen thing reacts: Evie for Lamba, Faron for the plushy, Wacky (with Chuck) for the piggy, Sparkle for the rocket, Mewsha for the trophy, Huluu for the cake, Rosalina for the music box and the microphone, Harper for the belt, Kareem for the candy.

### 6.3 Speaker audit — `_speaker_key` (`audio_director.gd:95-113`) + `VOICE_PITCH` (`main.gd:3165`)

**The fall-through at `audio_director.gd:113` is `return "roshan"`.** An unrecognised speaker plays *in Roshan's voice*. For an antagonist that is the worst possible failure mode.

| Speaker string | `_speaker_key` branch | `VOICE_PITCH` | Verdict |
|---|---|---|---|
| Roshan | ✅ `roshan` | ✅ 1.18 | ok |
| Princess Huluu | ✅ `huluu` | ✅ 1.05 | ok |
| Evie | ✅ `evie` | ✅ 1.28 | ok |
| Harper / Fiona | ✅ `harper` | ✅ 1.12 | ok |
| Faron | ✅ `faron` | ✅ 1.00 | ok |
| Wacky | ✅ `wacky` | ✅ 0.70 | ok |
| Kareem / shop | ✅ `shop` (`:106` and `:111`) | ✅ 0.85 | ok |
| Rosalina | ✅ `rosalina` | ✅ 1.15 | ok |
| Sparkle | ✅ `sparkle` | ✅ 1.35 | ok |
| Mewsha | ✅ `mewsha` | ✅ 1.30 | ok |
| Everyone | ✅ `everyone` | ✅ 1.10 | ok |
| **Imp Captain / any "…imp…"** | ✅ `imp` (`:112`) | ❌ **missing** | **FLAG** — falls back to 1.0, indistinguishable from Faron/Chuck. Add `"imp": 1.42`. |
| **Midnight Maestro** | ✅ `maestro` (`:110`) | ❌ **missing** | **FLAG** — add `"maestro": 0.78`. |
| **Curtain Dragon** | ❌ **none** → `roshan` | — | **FLAG** — the floor-1 boss would speak in Roshan's voice. Add `if "dragon" in w: return "dragon"` + pitch `0.55`. |
| **Shadow Phantom** | ❌ **none** → `roshan` | — | **FLAG** — same. Add `if "phantom" in w or "shadow" in w: return "phantom"` + pitch `0.68`. |
| **TRUE ANTAGONIST (Chapter 2 cliffhanger)** | ❌ **none** → `roshan` | — | **FLAG, blocking.** Add a branch **before** the fall-through, e.g. `if "ember" in w or "lord" in w: return "ember"` + pitch `0.52`. Whatever name the owner picks, the branch must exist before the first CRASH line is written. |
| **Lamba** | ⚠️ `evie` (matches `"lamb"` at `:100`) | (Evie's 1.28) | **FLAG, by design or not?** Lamba currently speaks in Evie's voice. If Lamba should have its own timbre, the `lamba` branch must be inserted **before** line 100 — substring order decides. |
| **flower friend** | ❌ → `roshan` | — | **FLAG** — the silent muse. Give it zero lines; if it ever speaks it will be Roshan. |
| **Daddy Mermaid** | ✅ `daddy` | ✅ 0.90 | **CONSTRAINT** — real family recording. Give it **no new `st_*` vo key**. `_say` would fall back to `daddy.ogg` (`audio_director.gd:26`), i.e. a real clip under wrong words. Use `vo = "talk"` and write the caption to match a clip that exists. |
| **Chuck** | ✅ `chuck` | ✅ 1.00 | **CONSTRAINT** — same rule. Chuck appears beside Wacky; give Wacky the words. |

Portraits (`main.gd:3170-3182`) have no `imp`, `maestro`, `mewsha` entries, but `_flash_speaker_icon` (`main.gd:3200-3203`) falls back to Roshan's and — importantly — `show_msg` never calls it (`audio_director.gd:122`). **Portrait gaps are harmless today; pitch gaps are not.**

---

## 7. RISKS

### 7.1 Probe assertions at risk — `probe_opera_2d.gd`

| Line | Assertion | Risk | Mitigation |
|---|---|---|---|
| **135-138** | `while world.phase_index < world._finale_start(): world._on_gesture("probe", 100.0, 1.0)` — **no guard, no iteration cap** | **HIGHEST.** Any story gate on `_on_gesture` hangs the probe forever. | The `amount < 5.0` skip gate (§2.6b). `OperaStory` must never touch `phase_index`/`phase_progress`. |
| 156 | `while act.state == "play" and guard < 80` | Budget. Today ≈13 iterations (7 phases × 2, one for the `phase_gap` at `:1020-1023` + one to complete). Story adds **zero** because pumps carry `amount = 100`. | Verify with a run; headroom stays ~6×. |
| 91-92 | `is_equal_approx(world.progress(), 0.0)` after one frame | Story must not advance progress. | `OperaStory` writes nothing but `dialogue_*`. |
| 96-97 | `modes[0] == "bop"` | A story "phase" would break it. | **Never add to `PHASES`.** Header rule in `opera_story.gd`. |
| 102-105 | captain scuffle strictly inside `[1, _finale_start())`, bigger goal than phase 0 | Same. | Same. |
| 157-158, 167 | `rival_hid_through_scuffles` — `rival_actor.visible` false outside the finale | **A "friend on stage" story beat must not use `rival_actor`.** | If Faron/Evie/Huluu need to be seen during the job, add a *separate* `TextureRect`. Never call `_set_finale_visible(true)` from the story layer. |
| 148-151 | detective guided retry: `world.guided and world.active and phase_index == _finale_start() and phases.size() == original` | `_show_phase()` re-entry at `:1691` would re-fire `FINALE_OPEN`. | The `story_fired` dictionary (§2.2). |
| 32 | `house.find_children("*", "Node3D", …).is_empty()` | The party shelf / story caption / party overlay must be `Control`s. | All three are (`Panel`, `Label`, `ColorRect`). |
| 37-40 | cards have `RoshanActor` and **no** `RivalActor` | Don't reuse that node name. | Names are `PartyTableShelf`, `PartyPiece%d`, `PartyNightOverlay`, `OperaStoryCaption`. |
| 35, 43 | `_visible_card_count == 4` / `== 5` | Counts `card_buttons` only. | The shelf is not a `Button` and not in `card_buttons`. |
| 48 | `lobby.refresh(0, 0)` | `_refresh_party_table()` must render 13 dim cells at zero stars. | Handled. |
| 182-184 | `main.touch_ui.visible == touch_before` after `act.cancel()` | Unrelated, but a leaked queue across 13 acts is a real bug. | `m.clear_dialogue()` in `cancel()` / `_finish()` (§2.7). |

Also `probe_opera.gd` (legacy 3D) drives the boss/3D path through the same `OperaAct.start()`. It asserts mechanics, not captions — but the ACT_OPEN restructure at §2.1 touches its path, so re-run it.

### 7.2 Seconds added per act

Holds as specced (2.6–3.6s per line):

| Trigger | Lines | Seconds |
|---|---|---|
| ACT_OPEN (2 story + the restored career voice) | 3 | 10.0 |
| SCUFFLE | 1 | 2.6 |
| STATION_1 | 1 | 2.8 |
| STATION_2 | 1 | 2.8 |
| STEAL | 1 | 2.6 |
| FINALE_OPEN | 1 | 2.6 |
| CURTAIN_CALL (behind a 3.0s hold, absorbed by `win_t`) | 1 | 2.8 |
| LOBBY_RETURN | 1 | 2.8 |
| **Total queued** | **10** | **≈29.0s** |
| minus the career `voice` that *should* already have fired | | −3.6 |
| **Net worst case (child never taps)** | | **≈25.4s** |
| **Replay** | 3 | **≈11.0s** |
| **Realistic (taps advance every line)** | | **≈8–12s** |

Acts currently run ~90–150s, so worst case is **+17% to +28%**, realistic ~+8%. The two levers if that is too much: drop `ACT_OPEN` to one story line (−3.2s × 13) and drop `FINALE_OPEN` (−2.6s × 13).

The **party climax** adds ~42s worst case, once, ever.

### 7.3 Caption / voice contention

- **Voice, not caption.** The caption Label is invisible during the opera (fact 0.1); the real contention is the four-slot `voice_pool` (`audio_director.gd:28-33`), where a second `_say` in the same frame genuinely double-speaks.
- **Solved for instructions** by `OperaStory.instruct()` appending instead of overwriting (§1.2).
- **Solved for reactive lines** by the seven `not m.dialogue_active` guards (§2.5).
- **Residual:** `m._say("faron", "miss", 3.0)` at `opera_career_world_2d.gd:1136` (nursery miss) is a bare `_say`, not `show_msg`. It has a 3s cooldown and no caption, so it can gently overlap a story line. Acceptable — the ambience duck at `audio_director.gd:172-189` handles it — but guard it too if the owner hears mush.
- **`msg_timer` interaction:** `show_msg` sets `msg_timer = 5.0` (`audio_director.gd:119`) while `_advance_dialogue` sets `dialogue_t` to the line's `hold` (`:70`). Keeping every story `hold` ≤ 5.0 means the (hidden) caption never blanks mid-line. All specced holds are 2.6–3.6.
- **Skip is now real:** `skip_dialogue()` had **zero callers** before this plan. Without §2.6 the entire story layer is un-skippable for a child who is bored, which is the one thing that would make her hate it.

### 7.4 The `ACT_OPEN` defect — root cause and fix

**Defect.** `opera_act.gd:537-540`:

```gdscript
	if use_career_world_2d:
		_start_career_world_2d()
		if use_career_world_2d:
			return
```

On the shipping path `use_career_world_2d` is true for all thirteen careers (fact 0.2), `_start_career_world_2d()` succeeds, and `start()` **returns at line 540**. Lines 584-593 — the sparkle burst *and* `m.show_msg("Roshan", String(config.get("voice", …)), "talk")` at line **592** — are dead code on every shipping run. The result: the `ACTS` `"voice"` string, which is the only line that names the career and frames the whole show ("Chef hat on! You and the pastry imp each have a kitchen…", `opera_house.gd:24`), **has never been heard by the player for any of the thirteen careers.** The child hears only `PHASES[career][0]["voice"]` ("Mischief imps grabbed the spoons! Tap each imp!") — she is thrown into a scuffle with no idea what job she is doing.

**Fix:** §2.1. Move the announcement above the branch as an `OperaStory.instruct()` call so it is queued behind the ACT_OPEN story and ahead of phase 1's instruction. This is the single highest-value change in the whole plan and is worth landing on its own even if the story layer slips.

**Regression to watch:** the 3D boss path still fires its own `instruct` at 589-592. With ACT_OPEN queued above, the boss ordering becomes `[boss story…] → [boss voice/brawl line]`, which is correct. Do **not** leave both a `show_msg` at 592 and an `instruct` above it — the `show_msg` would overwrite the queue head.

### 7.5 Other

- **Double `_write_save()`:** `try_chapter_open` writes; `award_sticker` (`main.gd:333`) also writes. Both are milestone sites and the write is transactional (`save_state.gd:542-566`), so this is safe — but the PARTY flag is folded into the *existing* `_act_won` write (§3.2) rather than adding a second one.
- **`_return_to_lobby` signature change:** default-valued second parameter, single caller (`_act_won`). No other call site in the tree.
- **`cfg["act_index"]`:** `config` is `duplicate()`d at `opera_house.gd:625` and passed by reference into `OperaCareerWorld2D.setup` (`:612` → `:275`). Adding a key is inert everywhere else; nothing iterates `config`.
- **Nursery has no `PATHS` entry** (`opera_stage_paths.gd:20-153` stops at `popstar`), so it falls back to 4 stations while its `station_for_phase` assigns 5 — `mini(station_index, station_list.size() - 1)` at `:531` clamps the last two to the same marker. Unrelated to the story layer, but if `STATION_3` is ever populated for nursery, its beat will narrate a station the child is already standing on. Worth a separate fix.
