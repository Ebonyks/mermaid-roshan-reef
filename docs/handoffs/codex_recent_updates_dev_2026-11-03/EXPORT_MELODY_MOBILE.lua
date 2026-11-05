local root="C:/Users/Peter/.codex/worktrees/recent-updates-dev-20261103/mermaid-roshan-reef"
local rows={
{source="assets/characters/stickers/daddy.png",target="assets/melody/mobile/daddy.png",w=281,h=384,crop=false,x=0,y=0},
{source="assets/melody/curtain_left_painted.png",target="assets/melody/mobile/curtain_left_painted.png",w=302,h=751,crop=true,x=0,y=8},
{source="assets/melody/curtain_right_painted.png",target="assets/melody/mobile/curtain_right_painted.png",w=213,h=744,crop=true,x=88,y=13},
{source="assets/melody/footlight_green.png",target="assets/melody/mobile/footlight_green.png",w=64,h=64,crop=false,x=0,y=0},
{source="assets/melody/footlight_orange.png",target="assets/melody/mobile/footlight_orange.png",w=64,h=64,crop=false,x=0,y=0},
{source="assets/melody/footlight_periwinkle.png",target="assets/melody/mobile/footlight_periwinkle.png",w=64,h=64,crop=false,x=0,y=0},
{source="assets/melody/footlight_purple.png",target="assets/melody/mobile/footlight_purple.png",w=64,h=64,crop=false,x=0,y=0},
{source="assets/melody/footlight_red.png",target="assets/melody/mobile/footlight_red.png",w=64,h=64,crop=false,x=0,y=0},
{source="assets/melody/footlight_sky_blue.png",target="assets/melody/mobile/footlight_sky_blue.png",w=64,h=64,crop=false,x=0,y=0},
{source="assets/melody/footlight_yellow.png",target="assets/melody/mobile/footlight_yellow.png",w=64,h=64,crop=false,x=0,y=0},
{source="assets/melody/progress_pip_current_blue_painted.png",target="assets/melody/mobile/progress_pip_current_blue_painted.png",w=64,h=64,crop=false,x=0,y=0},
{source="assets/melody/progress_pip_current_green_painted.png",target="assets/melody/mobile/progress_pip_current_green_painted.png",w=64,h=64,crop=false,x=0,y=0},
{source="assets/melody/progress_pip_current_indigo_painted.png",target="assets/melody/mobile/progress_pip_current_indigo_painted.png",w=64,h=64,crop=false,x=0,y=0},
{source="assets/melody/progress_pip_current_orange_painted.png",target="assets/melody/mobile/progress_pip_current_orange_painted.png",w=64,h=64,crop=false,x=0,y=0},
{source="assets/melody/progress_pip_current_red_painted.png",target="assets/melody/mobile/progress_pip_current_red_painted.png",w=64,h=64,crop=false,x=0,y=0},
{source="assets/melody/progress_pip_current_violet_painted.png",target="assets/melody/mobile/progress_pip_current_violet_painted.png",w=64,h=64,crop=false,x=0,y=0},
{source="assets/melody/progress_pip_current_yellow_painted.png",target="assets/melody/mobile/progress_pip_current_yellow_painted.png",w=64,h=64,crop=false,x=0,y=0},
{source="assets/melody/progress_pip_filled_blue_painted.png",target="assets/melody/mobile/progress_pip_filled_blue_painted.png",w=64,h=64,crop=false,x=0,y=0},
{source="assets/melody/progress_pip_filled_green_painted.png",target="assets/melody/mobile/progress_pip_filled_green_painted.png",w=64,h=64,crop=false,x=0,y=0},
{source="assets/melody/progress_pip_filled_indigo_painted.png",target="assets/melody/mobile/progress_pip_filled_indigo_painted.png",w=64,h=64,crop=false,x=0,y=0},
{source="assets/melody/progress_pip_filled_orange_painted.png",target="assets/melody/mobile/progress_pip_filled_orange_painted.png",w=64,h=64,crop=false,x=0,y=0},
{source="assets/melody/progress_pip_filled_red_painted.png",target="assets/melody/mobile/progress_pip_filled_red_painted.png",w=64,h=64,crop=false,x=0,y=0},
{source="assets/melody/progress_pip_filled_violet_painted.png",target="assets/melody/mobile/progress_pip_filled_violet_painted.png",w=64,h=64,crop=false,x=0,y=0},
{source="assets/melody/progress_pip_filled_yellow_painted.png",target="assets/melody/mobile/progress_pip_filled_yellow_painted.png",w=64,h=64,crop=false,x=0,y=0},
{source="assets/melody/progress_pip_idle_blue_painted.png",target="assets/melody/mobile/progress_pip_idle_blue_painted.png",w=64,h=64,crop=false,x=0,y=0},
{source="assets/melody/progress_pip_idle_green_painted.png",target="assets/melody/mobile/progress_pip_idle_green_painted.png",w=64,h=64,crop=false,x=0,y=0},
{source="assets/melody/progress_pip_idle_indigo_painted.png",target="assets/melody/mobile/progress_pip_idle_indigo_painted.png",w=64,h=64,crop=false,x=0,y=0},
{source="assets/melody/progress_pip_idle_orange_painted.png",target="assets/melody/mobile/progress_pip_idle_orange_painted.png",w=64,h=64,crop=false,x=0,y=0},
{source="assets/melody/progress_pip_idle_red_painted.png",target="assets/melody/mobile/progress_pip_idle_red_painted.png",w=64,h=64,crop=false,x=0,y=0},
{source="assets/melody/progress_pip_idle_violet_painted.png",target="assets/melody/mobile/progress_pip_idle_violet_painted.png",w=64,h=64,crop=false,x=0,y=0},
{source="assets/melody/progress_pip_idle_yellow_painted.png",target="assets/melody/mobile/progress_pip_idle_yellow_painted.png",w=64,h=64,crop=false,x=0,y=0},
{source="assets/melody/rainbow_note_blue_painted.png",target="assets/melody/mobile/rainbow_note_blue_painted.png",w=128,h=128,crop=false,x=0,y=0},
{source="assets/melody/rainbow_note_green_painted.png",target="assets/melody/mobile/rainbow_note_green_painted.png",w=128,h=128,crop=false,x=0,y=0},
{source="assets/melody/rainbow_note_indigo_painted.png",target="assets/melody/mobile/rainbow_note_indigo_painted.png",w=128,h=128,crop=false,x=0,y=0},
{source="assets/melody/rainbow_note_orange_painted.png",target="assets/melody/mobile/rainbow_note_orange_painted.png",w=128,h=128,crop=false,x=0,y=0},
{source="assets/melody/rainbow_note_red_painted.png",target="assets/melody/mobile/rainbow_note_red_painted.png",w=128,h=128,crop=false,x=0,y=0},
{source="assets/melody/rainbow_note_violet_painted.png",target="assets/melody/mobile/rainbow_note_violet_painted.png",w=128,h=128,crop=false,x=0,y=0},
{source="assets/melody/rainbow_note_yellow_painted.png",target="assets/melody/mobile/rainbow_note_yellow_painted.png",w=128,h=128,crop=false,x=0,y=0},
{source="assets/melody/star_painted.png",target="assets/melody/mobile/star_painted.png",w=128,h=128,crop=false,x=0,y=0},
{source="assets/opera/worlds/actors/roshan_popstar.png",target="assets/melody/mobile/roshan_popstar.png",w=256,h=256,crop=false,x=0,y=0},
}
for _,r in ipairs(rows) do
 local s=app.open(root.."/"..r.source)
 if r.crop then
  local o=Sprite(r.w,r.h,ColorMode.RGB)
  local cel=s.cels[1]
  o.cels[1].image:drawImage(cel.image,Point(cel.position.x-r.x,cel.position.y-r.y))
  o:saveCopyAs(root.."/"..r.target)
  o:close()
 else
  app.command.SpriteSize{ui=false,width=r.w,height=r.h,method="bilinear"}
  s:saveCopyAs(root.."/"..r.target)
 end
 s:close()
end
