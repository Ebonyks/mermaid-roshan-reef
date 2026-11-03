extends Node2D
## Tiny world-local effects on the original lift shafts and chandelier light.

var phase := 0.0
var enabled := true
var materials: Array[ShaderMaterial] = []
var tea_burst := 0.0
var bell_burst := 0.0
var lift_burst := 0.0
var celebration := 0.0
var celebration_position := Vector2.ZERO
var curtains: Array[Node2D] = []

func _process(delta: float) -> void:
	if not enabled or not is_visible_in_tree():
		return
	phase += minf(delta, 0.05)
	tea_burst = maxf(tea_burst-delta,0.0)
	bell_burst = maxf(bell_burst-delta,0.0)
	lift_burst = maxf(lift_burst-delta,0.0)
	celebration = maxf(celebration-delta,0.0)
	for material: ShaderMaterial in materials:
		material.set_shader_parameter("phase", phase)
		material.set_shader_parameter("tea_reaction",minf(tea_burst,1.0))
		material.set_shader_parameter("bell_reaction",minf(bell_burst,1.0))
	for curtain: Node2D in curtains:
		curtain.pose(phase)
	queue_redraw()

func _draw() -> void:
	for side: int in range(2):
		var x: float = 438.0 if side == 0 else 2120.0
		for index: int in range(7):
			var y: float = 970.0 - fposmod(phase * 38.0 + float(index) * 113.0, 810.0)
			var center := Vector2(x + sin(float(index)*4.2+phase*0.35)*24.0, y)
			draw_arc(center, 3.5 + float(index % 3), 0, TAU, 18,
				Color(0.76, 0.94, 1.0, 0.28+minf(lift_burst,1.0)*0.25), 1.5, true)
	for index: int in range(12):
		var x: float = 550.0 + fposmod(float(index)*149.2+phase*4.0, 1450.0)
		var y: float = 160.0 + fposmod(float(index)*131.7-phase*5.0, 700.0)
		draw_circle(Vector2(x,y), 1.5, Color(1,0.9,0.62,0.18+0.08*sin(phase+float(index))))
	# Steam belongs to the original refreshment cart; a touch makes a short puff.
	for index: int in range(3):
		var progress: float = fposmod(phase*0.24+float(index)/3.0,1.0)
		var points := PackedVector2Array()
		for step_index: int in range(9):
			var t: float = float(step_index)/8.0
			points.append(Vector2(2360.0+float(index)*16.0+sin(t*TAU+phase)*6.0,
				1160.0-progress*48.0-t*(22.0+minf(tea_burst,1.0)*28.0)))
		draw_polyline(points,Color(1,0.97,0.91,(1.0-progress)*(0.20+minf(tea_burst,1.0)*0.35)),1.8,true)
	if bell_burst>0.0:
		var progress: float = 1.0-bell_burst/2.0
		draw_arc(Vector2(630,938),12.0+progress*35.0,-2.7,-0.4,24,Color(1,0.88,0.46,(1.0-progress)*0.75),2.0,true)
	if celebration>0.0:
		for index: int in range(9):
			var angle: float = float(index)*TAU/9.0+phase*0.3
			var radius: float = 35.0+(2.5-celebration)*12.0
			var position: Vector2 = celebration_position+Vector2.from_angle(angle)*radius
			draw_circle(position,2.6,Color(1,0.88,0.40,celebration/2.5))
