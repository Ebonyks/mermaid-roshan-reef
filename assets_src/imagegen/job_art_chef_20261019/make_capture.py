from pathlib import Path
p=Path(__file__).resolve().parent
t=(p/'capture_chef_baseline.gd').read_text()
t=t.replace('review_baseline/','review_current_01/').replace('CHEF_BASELINE_CAPTURE','CHEF_CURRENT_CAPTURE')
t=t.replace('Current unchanged runtime baseline; configured phases, no acceptance','Current painted candidates; configured phases, no acceptance')
t=t.replace('if requested_mode == "tap":','''if requested_mode == "oven":
\t\t\t\tfor heat: float in [0.44,0.45,0.62,0.80,0.81]:
\t\t\t\t\tsurface.oven_t = heat
\t\t\t\t\tsurface.queue_redraw()
\t\t\t\t\tawait _shot("heat-"+str(heat))
\t\t\t\tsurface.oven_peek=0.5
\t\t\t\tsurface.queue_redraw()
\t\t\t\tawait _shot("door-open-fixture")
\t\t\tif requested_mode == "tap":''')
(p/'capture_chef_current_01.gd').write_text(t)

t=(p/'capture_chef_baseline.gd').read_text()
t=t.replace('review_baseline/','review_current_02/').replace('CHEF_BASELINE_CAPTURE','CHEF_CURRENT_CAPTURE')
t=t.replace('Current unchanged runtime baseline; configured phases, no acceptance',
    'Configured current painted phases, raw GUI earning and explicit diagnostic heat fixtures; physical device/owner acceptance separate')
t=t.replace('await _shot("ready")','''world.set_process(false)
\t\t\tsurface.set_process(false)
\t\t\tawait _shot("ready")
\t\t\tif requested_mode == "pourt":
\t\t\t\tvar at := surface._pour_pitcher_rect().get_center()
\t\t\t\tawait _touch(at,true)
\t\t\t\tfor tick in range(900):
\t\t\t\t\tsurface._process(1.0/30.0)
\t\t\t\t\tif tick == 80:
\t\t\t\t\t\tawait _shot("earned-mid-pour")
\t\t\t\t\tif surface.pour_level >= 0.999:
\t\t\t\t\t\tbreak
\t\t\t\tawait _touch(at,false)
\t\t\t\t_ck("pour earns filled bowl",surface.pour_level >= 0.999)
\t\t\t\tawait _shot("earned-full-pour")
\t\t\tif requested_mode == "circle":
\t\t\t\tvar pivot := surface._circle_pivot()
\t\t\t\tawait _touch(pivot+Vector2(42,0),true)
\t\t\t\tfor sample in range(1,121):
\t\t\t\t\tawait _drag(pivot+Vector2.from_angle(float(sample)*TAU/36.0)*42.0)
\t\t\t\t\tif sample in [9,18,27,36]:
\t\t\t\t\t\tawait _shot("whisk-angle-"+str(sample))
\t\t\t\tawait _touch(pivot+Vector2(42,0),false)
\t\t\t\t_ck("stir earns progress",world.phase_progress > 0.0)
\t\t\t\tawait _shot("earned-stir")
\t\t\tif requested_mode == "oven":
\t\t\t\tfor heat: float in [0.44,0.45,0.62,0.80,0.81]:
\t\t\t\t\tsurface.oven_t=heat
\t\t\t\t\tsurface.queue_redraw()
\t\t\t\t\tawait _shot("diagnostic-heat-"+str(heat))
\t\t\t\tsurface.oven_t=0.62
\t\t\t\tvar at := surface._oven_handle_rect().get_center()
\t\t\t\tawait _touch(at,true)
\t\t\t\tawait _touch(at,false)
\t\t\t\t_ck("handle tap earns baked result",world.phase_progress > 0.0)
\t\t\t\tawait _shot("earned-door-open")
\t\t\tif requested_mode == "swipe":
\t\t\t\tawait _touch(surface._trace_demo_point(0),true)
\t\t\t\tfor sample in range(1,65):
\t\t\t\t\tawait _drag(surface._trace_demo_point(float(sample)/64.0))
\t\t\t\t\tif sample in [16,32,48]:
\t\t\t\t\t\tawait _shot("earned-frost-"+str(sample))
\t\t\t\tawait _touch(surface._trace_demo_point(1),false)
\t\t\t\t_ck("source-aligned frosting earns completion",surface.trace_journey >= 0.99)
\t\t\t\tawait _shot("earned-frost-complete")''')
t=t.replace('for index: int in range(3):','for index: int in range(7):')
t=t.replace('await _shot("three-toppings")','''await _shot("seven-toppings")
\t\t\t\t_ck("seven toppings earn seven goals",world.phase_progress >= 6.99)''')
t=t.replace('world.task_open = false','world.set_process(true)\n\t\t\tworld.task_open = false')
t=t.replace('"scope":"Current painted', '"failures":failures,"scope":"Current painted')
t=t.replace('print("CHEF_CURRENT_CAPTURE|PASS|",records.size(),"frames")',
    'print("CHEF_CURRENT_CAPTURE|", "PASS" if failures.is_empty() else "FAIL", "|",records.size(),"frames")')
t=t.replace('\tquit()','\tquit(0 if failures.is_empty() else 1)')
(p/'capture_chef_current_02.gd').write_text(t)
# Keep the failed second pass unchanged. It continued stirring after the earned
# completion, which legitimately advanced the next phase and reset its progress.
t=t.replace('review_current_02/','review_current_03/')
t=t.replace('await _shot("whisk-angle-"+str(sample))',
    'await _shot("whisk-angle-"+str(sample))\n\t\t\t\t\tif world.phase_advance_pending:\n\t\t\t\t\t\tbreak')
t=t.replace('"baseline":"6fb96aeb441952c1053cc5ce18435fc57fc1d1ab"',
    '"baseline":"6fb96aeb441952c1053cc5ce18435fc57fc1d1ab","failures":failures')
(p/'capture_chef_current_03.gd').write_text(t)
