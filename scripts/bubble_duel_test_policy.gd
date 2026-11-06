class_name BubbleDuelTestPolicy
extends RefCounted
## Test-only observer. Never writes to the fighter being played.
var memory := BubbleDuelFighter.new()
var last_press: int = -30
var release_top: bool = false
var period: int = 6
var strong: bool = true


func _init(seed_number: int = 1, tap_period: int = 6, skilled: bool = true) -> void:
	memory.rng.seed = seed_number
	memory.cpu_skill = 65
	memory.cpu_reflex = 75
	period = tap_period
	strong = skilled


func observe(player: BubbleDuelFighter, world: BubbleDuelArena, tick: int) -> Dictionary:
	memory.position = player.position
	memory.velocity = player.velocity
	memory.bubbles = player.bubbles
	memory.team = player.team
	memory.max_vx = player.max_vx
	memory.max_vy = player.max_vy
	memory.gear = player.gear
	memory.charge = player.charge
	memory.lost = player.lost
	memory.swallowed = player.swallowed
	memory.kick_edge = false
	if not strong:
		BubbleDuelBrain.decide(memory, world.fighters)
	else:
		var foe: BubbleDuelFighter = BubbleDuelBrain.opponent(memory, world.fighters)
		if foe != null:
			var dx: float = BubbleDuelMotion.wrapped_dx(foe.position.x + foe.velocity.x * 4 - memory.position.x)
			var vx: float = clampf(dx * 0.15, -4, 4)
			var vy: float = clampf((clampf(foe.position.y - 50, 32, 240) - memory.position.y) * 0.12, -4, 4)
			var error: float = vx - memory.velocity.x
			memory.direction = signf(error) if absf(error) > 0.8 else 0.0
			if memory.position.y < 30: release_top = true
			if memory.position.y > 95: release_top = false
			memory.kick_edge = not release_top and (memory.velocity.y > vy + 0.6 or (absf(error) > 1.8 and memory.position.y > 55 and memory.velocity.y > -2))
	var press: bool = memory.kick_edge and tick - last_press >= period
	if press: last_press = tick
	return {"axis": memory.direction, "flap": press,
		"power": player.charge >= 85 and tick % 90 < period and player.gear not in ["classic", "tidewing"]}
