class_name OperaAct
extends Node
## One Canvas career performance.
##
## OperaAct is intentionally a small lifecycle wrapper. The career world owns
## all play, art and touch input; this node owns validation, competition time,
## music restoration, the curtain-call delay and safe cancellation.

const CompetitionDirector := preload("res://scripts/opera_competition.gd")
const CareerWorld2D := preload("res://scripts/opera_career_world_2d.gd")

var m: ReefMain
var config: Dictionary = {}
var kind := ""
var finish_cb: Callable
var state := "play"
var stage_phase := "puzzle"
var elapsed := 0.0
var win_t := 0.0
var competition: OperaCompetition = null
var performance_result: Dictionary = {}
var use_career_world_2d := false
var career_world_2d: OperaCareerWorld2D = null
var touch_was_visible := true
var player_was_visible := true
var prior_music := ""
var owns_music := false
var failure_reason := ""


static func supports_config(act_config: Dictionary) -> bool:
	if act_config.is_empty() \
			or bool(act_config.get("retired", false)) \
			or String(act_config.get("type", "show")) != "show" \
			or String(act_config.get("kind", "")) == "boss":
		return false
	var costume := String(act_config.get("costume", ""))
	return costume != "" \
		and CompetitionDirector.CAREERS.has(costume) \
		and CareerWorld2D.PHASES.has(costume)


func start(main: ReefMain, act_config: Dictionary, done_cb: Callable) -> bool:
	m = main
	config = act_config.duplicate(true)
	finish_cb = done_cb
	kind = String(config.get("kind", ""))
	stage_phase = "puzzle"
	if not supports_config(config):
		state = "invalid"
		failure_reason = "unsupported or retired career configuration"
		push_error("OperaAct: %s" % failure_reason)
		set_process(false)
		return false
	prior_music = m.cur_track
	var cue := String(config.get("music", ""))
	if cue != "" and cue != prior_music:
		m._play_music(cue)
		owns_music = m.cur_track == cue
	competition = CompetitionDirector.new() as OperaCompetition
	competition.configure(String(config.get("costume", "")))
	if not competition.is_valid():
		state = "invalid"
		failure_reason = "career competition mapping is unavailable"
		push_error("OperaAct: %s" % failure_reason)
		_restore_act_music()
		set_process(false)
		return false
	if m.touch_ui != null:
		touch_was_visible = m.touch_ui.visible
		m.touch_ui.visible = false
	if m.player != null:
		player_was_visible = m.player.visible
		m.player.visible = false
	career_world_2d = CareerWorld2D.new() as OperaCareerWorld2D
	add_child(career_world_2d)
	career_world_2d.setup(m, config, competition, Callable(self, "_win"))
	use_career_world_2d = true
	return true


func _process(delta: float) -> void:
	if m == null or state == "done" or state == "invalid":
		return
	elapsed += delta
	if state == "won":
		win_t -= delta
		if win_t <= 0.0:
			_finish()
		return
	_tick_competition(delta)
	if career_world_2d != null and is_instance_valid(career_world_2d):
		career_world_2d.update_competition()


func _notification(what: int) -> void:
	if (what == NOTIFICATION_APPLICATION_PAUSED \
			or what == NOTIFICATION_WM_CLOSE_REQUEST) and state == "won":
		# The child earned the result before the curtain-call delay. Commit it
		# synchronously before Android can suspend or terminate the process.
		_finish()


func _tick_competition(delta: float) -> void:
	if competition == null or competition.completed \
			or career_world_2d == null or not is_instance_valid(career_world_2d):
		return
	for event: String in competition.tick(delta, career_world_2d.competition_progress()):
		if event == "rival_step":
			career_world_2d.rival_step()
		elif event == "rival_solved":
			career_world_2d.begin_guided_retry()


func _win() -> void:
	if state != "play":
		return
	state = "won"
	win_t = 3.2
	if competition != null:
		performance_result = competition.complete()
	if career_world_2d != null and is_instance_valid(career_world_2d):
		career_world_2d.celebrate(performance_result)
	var win_line := String(config.get("win_line", "What a show! Everybody is cheering!"))
	if not performance_result.is_empty():
		if competition != null and competition.is_cooperative():
			win_line += " %s for the nursery team!" % String(performance_result.get("cheer", "Big cheers"))
		else:
			win_line += " %s for Mermaid Roshan!" % String(performance_result.get("cheer", "Big cheers"))
	# Chapter 2 rewrites the curtain line around its persistent story prop. The
	# legacy generic win recording is celebratory but does not speak that line,
	# so keep the truthful reading-aid caption instead of hiding it behind audio.
	var win_voice := "" if String(config.get("reward_policy", "")) \
		== "chapter2_story" else "win"
	m.show_msg("Roshan", win_line, win_voice)


func _finish() -> void:
	if state == "done" or state == "invalid":
		return
	state = "done"
	_cleanup_world()
	_restore_act_music()
	var completed_cb := finish_cb
	finish_cb = Callable()
	if completed_cb.is_valid():
		completed_cb.call()
	queue_free()


func cancel() -> void:
	if state == "done":
		return
	if state == "invalid":
		# Validation failed before this act acquired player, touch or music
		# ownership. Never restore default visibility over the caller's state.
		state = "done"
		finish_cb = Callable()
		queue_free()
		return
	if state == "won":
		_finish()
		return
	state = "done"
	_cleanup_world()
	_restore_act_music()
	finish_cb = Callable()
	queue_free()


func _cleanup_world() -> void:
	if career_world_2d != null and is_instance_valid(career_world_2d):
		career_world_2d.close()
	career_world_2d = null
	if m == null:
		return
	if m.touch_ui != null:
		m.touch_ui.visible = touch_was_visible
	if m.player != null:
		m.player.visible = player_was_visible


func _restore_act_music() -> void:
	if not owns_music or m == null:
		return
	owns_music = false
	var restore_track := prior_music
	prior_music = ""
	if restore_track != "":
		m._play_music(restore_track)


func action_label() -> String:
	return "PLAY"
