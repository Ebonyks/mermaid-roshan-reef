local lanes={"source","candidate"}
local aspects={"1280x720","1600x720","1280x800"}
local names={"01_small", "02_wrong_passive", "03_growing_lower", "04_lower_settled", "05_growing_middle", "06_two_settled", "07_growing_head", "08_three_stack_face", "09_partial_face", "10_chase_full", "11_lower_bite_squash", "12_remaining_two", "13_middle_bite_squash", "14_remaining_head", "15_head_bite_squash", "16_carrot_only", "17_original_win", "18_fresh_reentry"}
local root="C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/docs/handoffs/codex_flat_vector_art_2026-10-07/r131_snowball_runtime"
for _,lane in ipairs(lanes) do
 for _,aspect in ipairs(aspects) do
  local dir=root.."/"..lane.."_native/"..aspect
  app.fs.makeDirectory(dir.."/phone")
  for _,name in ipairs(names) do
   local s=app.open(dir.."/"..name..".png")
   app.command.SpriteSize{ui=false,scale=0.3,method="bilinear"}
   s:saveCopyAs(dir.."/phone/"..name..".png")
   s:close()
  end
 end
end
app.fs.makeDirectory(root.."/phone_comparisons")
for _,name in ipairs(names) do
 local board=Sprite(968,704,ColorMode.RGB)
 for row,aspect in ipairs(aspects) do
  for col,lane in ipairs(lanes) do
   local img=Image{fromFile=root.."/"..lane.."_native/"..aspect.."/phone/"..name..".png"}
   board.cels[1].image:drawImage(img,Point((col-1)*488,(row-1)*232))
  end
 end
 board:saveCopyAs(root.."/phone_comparisons/"..name..".png")
 board:close()
end
