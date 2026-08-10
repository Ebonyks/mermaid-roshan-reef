extends SceneTree
# Audio routing smoke test: important sound families must not collapse back to
# Master, where dialogue cannot be protected independently.

var bad := 0

const REQUIRED_AREA_MUSIC: Array[String] = [
	"castle_opera_hall", "castle_kitchen", "castle_library",
	"castle_playroom", "castle_craft_room", "castle_mermaid_pool",
	"castle_bubble_bath", "castle_dining_room", "castle_royal_bedroom",
	"castle_sleepover_bedroom", "castle_movie_lounge",
	"castle_family_gallery", "opera_lobby", "opera_chef",
	"opera_detective", "opera_ballerina", "opera_candymaker",
	"opera_doctor", "opera_farmer", "opera_boxer", "opera_magician",
	"opera_painter", "opera_astronaut", "opera_racer", "opera_popstar",
	"opera_nursery", "opera_boss_dragon", "opera_boss_phantom",
	"opera_boss_maestro", "northern", "galaxy", "ember",
	"dungeon_ice", "dungeon_ember", "combat_ice", "combat_fire",
	"stuffie_battle", "combat_tutorial", "picture_snowman",
	"picture_garden", "picture_trampoline", "picture_xmas",
]

func _init() -> void:
	var scene: PackedScene = load("res://scenes/main.tscn")
	var main: ReefMain = scene.instantiate()
	get_root().add_child(main)
	await process_frame
	await process_frame
	for bus_name: String in ["Music", "Voice", "SFX", "Ambience", "UI"]:
		_check("%s bus exists" % bus_name, AudioServer.get_bus_index(bus_name) >= 0)
	_check("music is routed", main.music != null and main.music.bus == "Music")
	_check("voice fallback is routed", main.voice != null and main.voice.bus == "Voice")
	_check("voice pool is routed", not main.voice_pool.is_empty() and (main.voice_pool[0] as AudioStreamPlayer).bus == "Voice")
	_check("effects are routed", main.chime != null and main.chime.bus == "SFX")
	_check("ambience is routed", main.ambience != null and main.ambience.bus == "Ambience")
	main._ui_tap()
	await process_frame
	_check("UI taps are routed", main._tap_player != null and main._tap_player.bus == "UI")
	var missing: Array[String] = []
	var not_import_looped: Array[String] = []
	for track: String in REQUIRED_AREA_MUSIC:
		var path := "res://assets/audio/music/%s.ogg" % track
		if not ResourceLoader.exists(path):
			missing.append(track)
			continue
		var stream: AudioStream = load(path)
		if not stream is AudioStreamOggVorbis \
				or not (stream as AudioStreamOggVorbis).loop:
			not_import_looped.append(track)
	_check("all authored area cues exist", missing.is_empty())
	_check("all authored area cues import looped", not_import_looped.is_empty())
	var opera_tracks: Dictionary = {}
	for config: Dictionary in OperaHouse.ACTS:
		var cue := String(config.get("music", ""))
		if cue != "":
			opera_tracks[cue] = true
	_check("every Opera act owns a unique cue",
		opera_tracks.size() == OperaHouse.ACTS.size())
	_check("every Castle room owns a cue",
		CastleRooms25D.ROOM_MUSIC.size() == CastleRooms25D.ROOMS.size())
	var before_missing := main.cur_track
	main._play_music("definitely_missing_audio_probe")
	_check("missing cue does not poison return track", main.cur_track == before_missing)
	main._play_music("castle_craft_room")
	await process_frame
	_check("area cue routes through Music", main.cur_track == "castle_craft_room"
		and main.music.stream != null and main.music.bus == "Music")
	_check("Castle area cue preserves room ambience",
		main.ambience != null and main.ambience.playing
		and main.ambience.stream.resource_path.ends_with("ambience_hall.ogg"))
	main._play_music("stuffie_battle")
	await process_frame
	_check("portable Stuffie cue preserves its source ambience",
		main.ambience.stream != null
		and main.ambience.stream.resource_path.ends_with("ambience_hall.ogg"))
	var pictures: PictureGames = main._pics_ref()
	pictures.open_generation = 10
	var stale_picture_generation := pictures.open_generation
	main.mg_kind = "garden"
	main.mg = {"music_return": "galaxy"}
	main._play_music("picture_garden")
	pictures.open_generation += 1   # model a new overlay opened before the timer
	pictures._mg2d_close(stale_picture_generation)
	_check("late picture close cannot overwrite a newer picture",
		main.cur_track == "picture_garden" and main.mg_kind == "garden")
	pictures._mg2d_close()
	_check("current picture close restores its source music",
		main.cur_track == "galaxy")
	_check("Galaxy cue keeps the Lagoon ambience bed",
		main.ambience.stream != null
		and main.ambience.stream.resource_path.ends_with("ambience_lagoon.ogg"))
	print("AUDIO|result: ", "ALL OK" if bad == 0 else "%d check(s) FAILED" % bad)
	quit()

func _check(label: String, ok: bool) -> void:
	print("AUDIO|%s: %s" % [label, "OK" if ok else "FAIL"])
	if not ok:
		bad += 1
