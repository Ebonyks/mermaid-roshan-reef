extends RefCounted

## Visual and input tuning for the Sky Lagoon promenade.
const CLOUD_PATH := "res://assets/sprites/sky_lagoon/iteration_20261111/ivory_cloud.png"
const CLOUD_POSITION := Vector2(2720, 390)
const CLOUD_HEIGHT := 166.0
const CLOUD_NIGHT := Color(0.54, 0.62, 0.86)
const CLOUD_TRAVEL := 300.0
const FOOTINGS := [
	{"name": "SeesawFooting", "path": "res://assets/sprites/sky_lagoon/iteration_20261111/moss_footing.png", "position": Vector2(3826, 1500), "height": 37.0, "alpha": 0.66},
	{"name": "SwingFooting", "path": "res://assets/sprites/sky_lagoon/iteration_20261111/moss_footing.png", "position": Vector2(3200, 1365), "height": 68.0, "alpha": 0.52},
	{"name": "SlideLadderFooting", "path": "res://assets/sprites/sky_lagoon/iteration_20261111/moss_footing.png", "position": Vector2(2310, 1315), "height": 30.0, "alpha": 0.53},
	{"name": "SlideExitFooting", "path": "res://assets/sprites/sky_lagoon/iteration_20261111/moss_footing.png", "position": Vector2(2735, 1395), "height": 30.0, "alpha": 0.54},
]
const CUE_TEXTURE := preload("res://assets/sprites/sky_lagoon/iteration_20261111/pearl_focus.png")
const CAMERA_FOLLOW := 9.0
