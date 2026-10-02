from pathlib import Path
import hashlib,json,shutil
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
source=r/'tmp/capture_doctor_sink_contact_v58.gd'
s=source.read_text(encoding='utf-8')
s=s.replace('doctor_sink_contact_v58','doctor_sink_water_contact_v68')
s=s.replace('"res://assets_src/imagegen/day2_doctor_wash_reach_v1_20261001/attempt01_native.png",','"res://assets_src/imagegen/day2_doctor_wash_reach_v1_20261001/attempt01_native.png",\n\t"res://assets_src/imagegen/day2_doctor_wash_reach_clean_v1_20261001/attempt01_native.png",')
s=s.replace('var sink_offset := 0.0','var sink_offset := 0.0\n\tvar sink_offset_y := 0.0\n\tvar water_on := false\n\tvar water_spout := Vector2.ZERO\n\tvar soap_contact := Vector2.ZERO\n\tvar basin_centre := Vector2.ZERO')
s=s.replace('Vector2(733.0,739.0)','Vector2(690.0,739.0)')
s=s.replace('hand + Vector2(sink_offset,0.0)','hand + Vector2(sink_offset,sink_offset_y)')
s=s.replace('\t\tqueue_redraw()','\t\twater_spout = sink_rect.position + Vector2(128.0,69.0)*scale_factor\n\t\tsoap_contact = character_rect.position + Vector2(684.0,680.0)*(character_rect.size.y/1402.0)\n\t\tbasin_centre = sink_rect.position + Vector2(128.0,111.0)*scale_factor\n\t\tqueue_redraw()',1)
s=s.replace('\t\tdraw_texture_rect(character,character_rect,false)','\t\tif water_on:\n\t\t\tdraw_line(water_spout,soap_contact,Color("448fa9"),3.5,true)\n\t\t\tdraw_line(water_spout,soap_contact,Color("caf9ff"),1.6,true)\n\t\tdraw_texture_rect(character,character_rect,false)\n\t\tif water_on:\n\t\t\tvar runoff := PackedVector2Array([soap_contact+Vector2(9.0,6.0),basin_centre+Vector2(8.0,-1.0)])\n\t\t\tdraw_polyline(runoff,Color("77c7dc"),2.0,true)\n\t\t\tdraw_circle(basin_centre+Vector2(7.0,-1.0),2.0,Color("caf9ff"))',1)
start=s.index('\t\tcanvas.character=ImageTexture.create_from_image')
end=s.index('\t\tassert(main.opera_stars==stars',start)
s=s[:start]+'''\t\tfor source_index: int in range(SOURCES.size()):
\t\t\tcanvas.character=ImageTexture.create_from_image(Image.load_from_file(SOURCES[source_index]))
\t\t\tcanvas.character_rect=Rect2(25.0,0.0,300.0*1122.0/1402.0,300.0)
\t\t\tcanvas.sink_extent=140.0
\t\t\tfor shift: float in [0.0,-10.0]:
\t\t\t\tcanvas.sink_offset_y=shift
\t\t\t\tfor flow: bool in [false,true]:
\t\t\t\t\tcanvas.water_on=flow
\t\t\t\t\tcanvas.refresh_geometry()
\t\t\t\t\tawait _wait(2)
\t\t\t\t\tvar ident := "doctor_%d_source%d_sinky%d_water%d"%[width,source_index,int(shift),int(flow)]
\t\t\t\t\tawait _capture(ident,{"variant":"static_outward_sink_water_contact","source":SOURCES[source_index],"source_sha256":FileAccess.get_sha256(SOURCES[source_index]),"sink_source":"res://assets/flats/castle/interactions_v2/bubble_bath_sink_sheet.png","sink_source_sha256":FileAccess.get_sha256("res://assets/flats/castle/interactions_v2/bubble_bath_sink_sheet.png"),"sink_region":[0,0,256,256],"sink_extent":canvas.sink_extent,"sink_offset_y":shift,"front_region":[0,116,256,140],"draw_order":"whole_sink_then_water_behind_whole_character_then_short_runoff_then_same_sink_front","actor_position":[canvas.position.x,canvas.position.y],"character_rect":[canvas.character_rect.position.x,canvas.character_rect.position.y,canvas.character_rect.size.x,canvas.character_rect.size.y],"hand_source_landmark":[canvas.hand_source.x,canvas.hand_source.y],"hand_local":[canvas.hand.x,canvas.hand.y],"sink_rect":[canvas.sink_rect.position.x,canvas.sink_rect.position.y,canvas.sink_rect.size.x,canvas.sink_rect.size.y],"water_on":flow,"water_spout_local":[canvas.water_spout.x,canvas.water_spout.y],"soap_contact_local":[canvas.soap_contact.x,canvas.soap_contact.y],"basin_centre_local":[canvas.basin_centre.x,canvas.basin_centre.y],"water_presentation":"Static test-only sparse 2D line from literal spout to upper hand and short runoff into basin; no causal/timed/action acceptance."})
''' +s[end:]
s=s.replace('STATIC_CONTACT_PLACEMENTS_CAPTURED','STATIC_WATER_CONTACT_PLACEMENTS_CAPTURED').replace('DOCTOR_SINK_CONTACT|','DOCTOR_SINK_WATER_CONTACT|')
script=r/'tmp/capture_doctor_sink_water_contact_v68.gd';script.write_text(s,encoding='utf-8',newline='\n')
runner=(r/'tmp/run_reach_sink_contact_v58.py').read_text(encoding='utf-8').replace('doctor_sink_contact_v58','doctor_sink_water_contact_v68').replace('capture_doctor_sink_contact_v58.gd','capture_doctor_sink_water_contact_v68.gd')
runner=runner.replace("'assets_src/imagegen/day2_doctor_wash_reach_v1_20261001/attempt01_native.png']","'assets_src/imagegen/day2_doctor_wash_reach_v1_20261001/attempt01_native.png','assets_src/imagegen/day2_doctor_wash_reach_clean_v1_20261001/attempt01_native.png']")
old="'variants':'One complete outward-reaching doctor key, uniform figure fits250/300px, reused sink extents140/160px, offsets0/20px,1280/1600 desktop widths;18 static views including2 current originals. Original first sink cell behind character, identical original front-rim/cabinet region0,116,256,140 in front. No source-pixel editing or new sink generation.'"
new="'variants':'Two complete outward-reaching soapy/clean sources, uniform figure fit300px, reused sink extent140px, lower-hand anchor690,739, sink vertical shifts0/-10px, water off/on at1280/1600 desktop widths;18 static views including2 current originals. Water is a sparse 2D graphic anchored to literal sink spout128,69, unchanged upper-hand684,680 and literal basin128,111. Original sink front-rim/cabinet region0,116,256,140 stays in front. Static gameplay study only, no cinematic pixels or source-pixel edits.'"
assert old in runner;runner=runner.replace(old,new)
runner_path=r/'tmp/run_reach_sink_water_contact_v68.py';runner_path.write_text(runner,encoding='utf-8',newline='\n')
packet=r/'audit/day_two_wash_contact_study_v1_20261001/attempt_05';assert not packet.exists();packet.mkdir()
(packet/'.gdignore').write_text('')
shutil.copyfile(script,packet/'capture.gd');shutil.copyfile(runner_path,packet/'executed_capture_runner.py');shutil.copyfile(Path(__file__),packet/'executed_prepare_reach_water_contact_study_v68.py')
record=json.loads((r/'design/audit_impacts/job-doctor-reach-local-rub-study-20261001.json').read_text(encoding='utf-8'))
record.update(id='job-doctor-reach-water-contact-study-20261001',scope='Reversible static gameplay-only contact study after actual doctor station arrival. Reuse the unchanged painted sink and complete soapy/clean reaching originals. Compare exact upper-hand/spout/basin anchors, quiet sparse graphic water, layered sink rim, two vertical placements and two viewport widths. No production, save, award, timed action or cinematic changes.',files=sorted(p.relative_to(r).as_posix() for p in packet.rglob('*') if p.is_file()),validation=[dict(command='Parser, inference, official4.7.2 analyzer/native static capture; literal source hashes/no-award assertions',result='PENDING',evidence=packet.relative_to(r).as_posix()+'/PROFILE.json; prepared contract, capture not run yet.')],acceptance_gaps='All 18 planned native views require direct contact/composition review. Static water does not prove a wet/rub/rinse/clean sequence, input causality, matching transitions, runtime or device/child/owner/cinematic acceptance.')
(r/'design/audit_impacts/job-doctor-reach-water-contact-study-20261001.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
profile=dict(status='PREPARED_STATIC_WATER_CONTACT_STUDY',baseline=record['baseline'],intention=record['scope'],rules=record['rules'],findings=record['findings'],capture_sha256=hashlib.sha256(script.read_bytes()).hexdigest(),expected_native_views=18,whole_action_acceptance=False,production_integration=False)
(packet/'PREPARED_PROFILE.json').write_text(json.dumps(profile,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(dict(prepared_script=str(script),prepared_runner=str(runner_path),planned_views=18,production_integration=False)))
