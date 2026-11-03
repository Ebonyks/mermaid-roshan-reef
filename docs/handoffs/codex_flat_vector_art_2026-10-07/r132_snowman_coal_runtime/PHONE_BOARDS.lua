local root="C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/docs/handoffs/codex_flat_vector_art_2026-10-07/r132_snowman_coal_runtime"
local source="C:/Users/Peter/AppData/Local/Temp/reef-flat-vector-snowman-coal-20261103/source_reused_phone"
local aspects={"1280x720","1600x720","1280x800"}
local names={"01_small","02_wrong_passive","03_growing_lower","04_lower_settled","05_growing_middle","06_two_settled","07_growing_head","08_three_stack_face","09_partial_face","10_chase_full","11_lower_bite_squash","12_remaining_two","13_middle_bite_squash","14_remaining_head","15_head_bite_squash","16_carrot_only","17_original_win","18_fresh_reentry"}
for _,aspect in ipairs(aspects) do
 local dir=root.."/candidate_native/"..aspect
 app.fs.makeDirectory(dir.."/phone")
 for _,name in ipairs(names) do
  local s=app.open(dir.."/"..name..".png")
  app.command.SpriteSize{ui=false,scale=0.3,method="bilinear"}
  s:saveCopyAs(dir.."/phone/"..name..".png")
  s:close()
 end
end
app.fs.makeDirectory(root.."/phone_comparisons")
for _,name in ipairs(names) do
 local board=Sprite(968,704,ColorMode.RGB)
 for row,aspect in ipairs(aspects) do
  local before=Image{fromFile=source.."/"..aspect.."/"..name..".png"}
  local after=Image{fromFile=root.."/candidate_native/"..aspect.."/phone/"..name..".png"}
  board.cels[1].image:drawImage(before,Point(0,(row-1)*232))
  board.cels[1].image:drawImage(after,Point(488,(row-1)*232))
 end
 board:saveCopyAs(root.."/phone_comparisons/"..name..".png")
 board:close()
end
