from pathlib import Path
p=Path(__file__).resolve().parent
def guard(name):
    return '''\tvar expected := ProjectSettings.globalize_path("res://tmp/chef_capture_appdata_%s").replace("\\\\", "/")
\tif not OS.get_user_data_dir().replace("\\\\", "/").begins_with(expected + "/"):
\t\tpush_error("USERDATA_ISOLATION_FAILED_BEFORE_GAME_INITIALIZATION")
\t\tquit(2)
\t\treturn
\tprint("USERDATA_ISOLATION|PASS|", OS.get_user_data_dir())
'''%name
t=(p/'capture_chef_current_03.gd').read_text()
t=t.replace('review_current_03/','review_current_04/')
t=t.replace('func _run() -> void:\n','func _run() -> void:\n'+guard('current_04'),1)
(p/'capture_chef_current_04.gd').write_text(t)
(p/'capture_chef_current_05.gd').write_text(t.replace('current_04','current_05'))
t6=t.replace('current_04','current_06')
t6=t6.replace('if sample in [16,32,48]:\n\t\t\t\t\t\tawait _shot("earned-frost-"+str(sample))',
    'if sample in [16,32,48]:\n\t\t\t\t\t\t_ck("partial frost does not complete",not world.phase_advance_pending)\n\t\t\t\t\t\tawait _shot("earned-frost-"+str(sample))')
t6=t6.replace('_ck("source-aligned frosting earns completion",surface.trace_journey >= 0.99)',
    '_ck("source-aligned frosting earns completed cake and exact goal",world.phase_advance_pending and surface.completion_accepted and is_equal_approx(world.phase_progress,6.0))')
(p/'capture_chef_current_06.gd').write_text(t6)
prefix=t[:t.index('func _run() -> void:')].replace('review_current_04/','review_chapter2_01/')
boot=t[t.index('\tDirAccess.make_dir_recursive_absolute(OUT)'):t.index('\tvar act_index := -1')]
body='''func _run() -> void:
'''+guard('chapter2_01')+boot+'''
\tm.chapter2_active=true
\tm.chapter2_active_objective=ChapterTwoDirector.OBJECTIVE_PARTY_PREP
\tm.chapter2_strawberry_mask=0x1F
\tfor aspect: int in [1280,1600]:
\t\twidth_now=aspect
\t\troot.size=Vector2i(aspect,720)
\t\tDisplayServer.window_set_size(root.size)
\t\tfor phase in range(5):
\t\t\tm.chapter2_cake_piece_mask=[0,1,3,7,15][phase]
\t\t\tvar competition := OperaCompetition.new()
\t\t\tcompetition.configure("chef")
\t\t\tworld=OperaCareerWorld2D.new()
\t\t\tm.add_child(world)
\t\t\tworld.setup(m,{"costume":"chef","chapter":"chapter2",
\t\t\t\t"phase_overrides":ChapterTwoCareerSceneAdapter.phase_set("chef").get("phases",[]),
\t\t\t\t"finale_start":5,"chapter2_resume_phase_index":phase},competition,Callable(),[],
\t\t\t\tChapterTwoCareerSceneAdapter.adapter_config("chef"),{"chapter":"chapter2"})
\t\t\tawait process_frame
\t\t\tworld.phase_gap=0.0
\t\t\tworld.reveal_t=0.0
\t\t\tworld._open_task()
\t\t\tawait create_timer(0.36).timeout
\t\t\tworld.reveal_t=0.0
\t\t\tworld.set_process(false)
\t\t\tsurface=world.surface as OperaGestureSurface
\t\t\t_ck("Chapter Two uses room-coordinate Chef surface",surface is OperaChefSurface)
\t\t\tsurface.set_process(false)
\t\t\tphase_id="chapter2-"+str(phase)+"-"+surface.mode
\t\t\tawait _shot("ready")
\t\t\tmatch phase:
\t\t\t\t0:
\t\t\t\t\tvar at:=surface._pour_pitcher_rect().get_center()
\t\t\t\t\tawait _touch(at,true)
\t\t\t\t\tfor tick in range(180):
\t\t\t\t\t\tsurface._process(1.0/30.0)
\t\t\t\t\t\tif tick==45:
\t\t\t\t\t\t\tawait _shot("earned-mid-pour")
\t\t\t\t\t\tif surface.pour_level>=0.999:
\t\t\t\t\t\t\tbreak
\t\t\t\t\tawait _touch(at,false)
\t\t\t\t\t_ck("Child pour earns full bowl",surface.pour_level>=0.999)
\t\t\t\t1:
\t\t\t\t\tvar pivot:=surface._circle_pivot()
\t\t\t\t\tawait _touch(pivot+Vector2(42,0),true)
\t\t\t\t\tfor sample in range(1,121):
\t\t\t\t\t\tawait _drag(pivot+Vector2.from_angle(float(sample)*TAU/36.0)*42.0)
\t\t\t\t\t\tif sample in [9,18,27,36]:
\t\t\t\t\t\t\tawait _shot("whisk-angle-"+str(sample))
\t\t\t\t\t\tif world.phase_advance_pending:
\t\t\t\t\t\t\tbreak
\t\t\t\t\tawait _touch(pivot+Vector2(42,0),false)
\t\t\t\t\t_ck("Child stir earns completion",world.phase_advance_pending)
\t\t\t\t2:
\t\t\t\t\tsurface.oven_t=0.62
\t\t\t\t\tvar at:=surface._oven_handle_rect().get_center()
\t\t\t\t\tawait _touch(at,true)
\t\t\t\t\tawait _touch(at,false)
\t\t\t\t\t_ck("Child hearth tap earns bake",world.phase_progress>0)
\t\t\t\t3:
\t\t\t\t\tfor index in range(3):
\t\t\t\t\t\tvar at:=surface._target_anchor_point(index)-Vector2(0,17)
\t\t\t\t\t\tawait _touch(at,true)
\t\t\t\t\t\tawait _touch(at,false)
\t\t\t\t\t\t_ck("One earned pair per tray",is_equal_approx(world.phase_progress,float(index+1)))
\t\t\t\t\t\tawait _shot("earned-stack-"+str(index+1))
\t\t\t\t4:
\t\t\t\t\tawait _touch(surface._trace_demo_point(0),true)
\t\t\t\t\tfor sample in range(1,65):
\t\t\t\t\t\tawait _drag(surface._trace_demo_point(float(sample)/64.0))
\t\t\t\t\t\tif sample in [16,32,48]:
\t\t\t\t\t\t\tawait _shot("earned-frost-"+str(sample))
\t\t\t\t\tawait _touch(surface._trace_demo_point(1),false)
\t\t\t\t\t_ck("Child frosting earns completion",surface.trace_journey>=0.99)
\t\t\tawait _shot("earned-endpoint")
\t\t\tworld.queue_free()
\t\t\tawait process_frame
\t\t\tawait process_frame
\tvar file:=FileAccess.open(OUT+"capture.json",FileAccess.WRITE)
\tfile.store_string(JSON.stringify({"captures":records,"failures":failures,
\t\t"scope":"Configured Chapter Two actual GUI input and current Mobile/HUD; no physical-device/owner acceptance"},"\\t"))
\tfile.close()
\tprint("CHEF_CHAPTER2_CAPTURE|", "PASS" if failures.is_empty() else "FAIL", "|",records.size(),"frames")
\tquit(0 if failures.is_empty() else 1)
'''
(p/'capture_chef_chapter2_01.gd').write_text(prefix+body)
# Preserve01: its standalone world was behind the still-mounted Castle UI.
# Suspend that UI exactly as the real Opera route does, retaining this fixture's
# explicit configured-world scope rather than pretending it traversed the route.
t=prefix+body
t=t.replace('chapter2_01','chapter2_02')
t=t.replace('\tm.chapter2_active=true','''\tm._castle_rooms_ref().suspend()
\tm.game="opera"
\tm.set_process(false)
\tm.hud_layer.layer=12
\tm.hud_game.visible=false
\tm.obj_card.visible=false
\tm.hud_msg.visible=false
\tm.player.visible=false
\tm.chapter2_active=true''',1)
t=t.replace('\t\t\tawait _shot("ready")','''\t\t\tm.clear_dialogue()
\t\t\tm.hud_msg.visible=false
\t\t\tm.obj_card.visible=false
\t\t\tawait _shot("ready")''',1)
(p/'capture_chef_chapter2_02.gd').write_text(t)
t=t.replace('chapter2_02','chapter2_03')
t=t.replace('\t\t\tm.clear_dialogue()', '\t\t\tm._sync_castle_voice_caption()\n\t\t\tm.clear_dialogue()')
(p/'capture_chef_chapter2_03.gd').write_text(t)
(p/'capture_chef_chapter2_04.gd').write_text(t.replace('chapter2_03','chapter2_04'))
t5=t.replace('chapter2_03','chapter2_05')
t5=t5.replace('_ck("Child frosting earns completion",surface.trace_journey>=0.99)',
    '_ck("Child frosting earns completed cake",world.phase_advance_pending and surface.completion_accepted)')
(p/'capture_chef_chapter2_05.gd').write_text(t5)
