from pathlib import Path
b=Path(r'C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
script=(Path(__file__).parent/'capture_pan_support_v118.py').read_text()
script=script.replace("previous=parent/'attempt_02';out=parent/'attempt_03'","previous=parent/'attempt_03';out=parent/'attempt_04'").replace('tmp/pan_details_v116/native_views','tmp/pan_support_v118/native_views').replace('tmp/pan_support_v118/native_views\',\'tmp/pan_support_v118/native_views','tmp/pan_support_v118/native_views\',\'tmp/pan_final_contact_v120/native_views')
old=".replace('invitation_support.z_index = -1','invitation_support.z_index = 0\\n\\t\\t\\t\\t\\tinvitation_support.show_behind_parent = true')"
new=".replace('active.object_size.y * 0.42)', 'active.object_size.y * 0.42 - 14.0)').replace('[\"original\", \"literal_raster\", \"painted_staging\"]', '[\"painted_staging\"]').replace('records.size() == 18','records.size() == 6').replace('18_NATIVE','6_NATIVE').replace('|18_CAPTURED','|6_CAPTURED')"
assert old in script;script=script.replace(old,new)
old=".replace('base + Vector2(0.0, -2.0), Vector2(24.0, 6.0), Color(0.22, 0.60, 0.65, 0.35), Color(0.57, 0.89, 0.88, 0.72)','base + Vector2(0.0, 4.0), Vector2(27.0, 8.0), Color(0.22, 0.60, 0.65, 0.50), Color(0.57, 0.89, 0.88, 0.85)')"
new=".replace('base + Vector2(0.0, 4.0), Vector2(27.0, 8.0)', 'base + Vector2(0.0, -2.0), Vector2(24.0, 6.0)')"
assert old in script;script=script.replace(old,new).replace('tmp/pan_support_v118/native_views\';native.mkdir','tmp/pan_final_contact_v120/native_views\';native.mkdir').replace('views=18','views=6').replace('and18-view','and6-view').replace('executed_capture_pan_support_v118.py','executed_capture_pan_final_contact_v120.py')
exec(compile(script,str(__file__),'exec'))
