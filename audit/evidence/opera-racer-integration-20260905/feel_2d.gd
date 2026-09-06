extends SceneTree

func _init() -> void:
	call_deferred("run")

func run() -> void:
	for policy in ["center", "inside", "drift"]:
		var surface := OperaRacerSurface.new()
		get_root().add_child(surface)
		surface.size = Vector2(1280,720)
		surface.configure("kart_race", Color.CORAL)
		surface.set_process(false)
		surface._press(surface.STEERING_RECT.get_center())
		var seconds := 0.0
		var max_tier := 0
		for frame in range(6000):
			var steer := 0.0
			var curvature := surface.road_curvature(float(surface.kart.s))
			if policy == "drift" and absf(curvature) > 0.006:
				steer = -signf(curvature)
			elif policy == "inside":
				steer = clampf((-signf(curvature) * 3.0 - float(surface.kart.lat)) * 0.3, -0.55, 0.55)
			surface._drag(surface.STEERING_RECT.get_center() + Vector2(steer * 290,0))
			surface._process(1.0/60.0)
			seconds += 1.0/60.0
			max_tier = maxi(max_tier, KartDriving.drift_tier(float(surface.kart.get("drift_t",0.0))))
			if surface.race_finished:
				break
		print("RACER2DFEEL|",policy," seconds=",seconds," tier=",max_tier,
			" pearls=",surface.race_pearls," turbos=",surface.race_turbo_fires," walls=",surface.race_wall_bumps)
		surface.free()
	quit()
