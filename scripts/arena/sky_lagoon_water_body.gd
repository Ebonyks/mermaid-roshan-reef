class_name SkyLagoonWaterBody
extends RigidBody3D
# A single constrained Jolt body for the Lagoon's water fauna. The promenade
# chooses a patrol target; Jolt integrates buoyancy, drag, wake impulses and
# the escape impulse. No delivered animation position is written directly.

var water_enabled: bool = false
var water_surface_y: float = 0.0
var water_surface_local_y: float = 0.0
var patrol_target_x: float = 0.0
var patrol_speed: float = 0.5
var drive_strength: float = 9.0
var buoyancy_strength: float = 28.0
var buoyancy_damping: float = 7.5
var wave_amplitude: float = 0.08
var wave_rate: float = 1.6
var water_clock: float = 0.0
var solver_steps: int = 0
var min_solver_y: float = INF
var max_solver_y: float = -INF
var received_escape_impulse: bool = false


func _ready() -> void:
	axis_lock_linear_z = true
	axis_lock_angular_x = true
	axis_lock_angular_y = true
	axis_lock_angular_z = true
	can_sleep = false
	continuous_cd = false
	collision_layer = 0
	collision_mask = 0
	set_meta("physics_engine", "Jolt Physics")
	set_meta("support_medium", "water")


func configure_water(start: Vector3, surface_y: float, speed: float,
		mass_value: float, wave: float) -> void:
	freeze = true
	position = start
	linear_velocity = Vector3.ZERO
	angular_velocity = Vector3.ZERO
	mass = mass_value
	gravity_scale = 1.0
	linear_damp = 1.15
	angular_damp = 3.0
	water_surface_local_y = surface_y
	water_surface_y = (get_parent_node_3d() as Node3D).to_global(
		Vector3(0.0, surface_y, 0.0)).y
	patrol_target_x = start.x
	patrol_speed = speed
	wave_amplitude = wave
	water_clock = 0.0
	solver_steps = 0
	min_solver_y = global_position.y
	max_solver_y = global_position.y
	received_escape_impulse = false
	water_enabled = true
	freeze = false
	sleeping = false


func disable_water() -> void:
	water_enabled = false
	freeze = true
	linear_velocity = Vector3.ZERO
	angular_velocity = Vector3.ZERO


func set_patrol_target(target_x: float, speed: float) -> void:
	patrol_target_x = target_x
	patrol_speed = speed
	if water_enabled:
		sleeping = false



func apply_escape_to(target_x: float, speed: float) -> void:
	# Activation still begins with a real Jolt impulse, but the solver drive is
	# bounded to the authored shoreline refuge instead of aiming off-screen.
	if not water_enabled:
		return
	var direction: float = signf(target_x - position.x)
	if is_zero_approx(direction):
		direction = 1.0
	patrol_target_x = target_x
	patrol_speed = speed
	received_escape_impulse = true
	apply_central_impulse(Vector3(direction * mass * speed * 0.30,
		mass * 1.8, 0.0))
	sleeping = false


func visual_waterline_y() -> float:
	return water_surface_local_y - 0.05


func _integrate_forces(state: PhysicsDirectBodyState3D) -> void:
	if not water_enabled:
		return
	var step: float = state.step
	water_clock += step
	var position_now: Vector3 = state.transform.origin
	var velocity_now: Vector3 = state.linear_velocity
	var wave_y: float = sin(water_clock * wave_rate) * wave_amplitude
	var desired_y: float = water_surface_y + wave_y
	var gravity: float = float(ProjectSettings.get_setting(
		"physics/3d/default_gravity", 9.8))
	var lift_acceleration: float = (desired_y - position_now.y) * buoyancy_strength \
		- velocity_now.y * buoyancy_damping + gravity
	var desired_velocity_x: float = clampf(
		(patrol_target_x - position_now.x) * 2.2,
		-patrol_speed, patrol_speed)
	# Work on Jolt's direct body state instead of accumulating a persistent
	# constant force. Jolt still integrates the body transform, damping and
	# impulses; this callback supplies the water-volume acceleration field.
	velocity_now.y += lift_acceleration * step
	velocity_now.x += (desired_velocity_x - velocity_now.x) \
		* minf(1.0, drive_strength * step)
	velocity_now.z = 0.0
	state.linear_velocity = velocity_now
	solver_steps += 1
	min_solver_y = minf(min_solver_y, position_now.y)
	max_solver_y = maxf(max_solver_y, position_now.y)
