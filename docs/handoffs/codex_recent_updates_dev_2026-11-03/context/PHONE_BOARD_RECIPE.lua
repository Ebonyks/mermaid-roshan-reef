local root="C:/Users/Peter/.codex/worktrees/recent-updates-dev-20261103/mermaid-roshan-reef/docs/handoffs/codex_recent_updates_dev_2026-11-03/context"
local names_snowfield={"01_small","02_wrong_passive","03_growing_lower","04_lower_settled","05_growing_middle","06_two_settled","07_growing_head","08_three_stack_face","09_partial_face","10_chase_full","11_lower_bite_squash","12_remaining_two","13_middle_bite_squash","14_remaining_head","15_head_bite_squash","16_carrot_only","17_original_win","18_fresh_reentry"}
local names_melody={"01_left_08","02_approach_30","03_mid_55","04_window_75","05_right_93","06_note_1_green","07_note_2_green","08_note_3_green","09_note_4_green","10_note_5_green","11_note_6_green"}
local aspects={"1280x720","1600x720","1280x800"}
for _,lane in ipairs({"source","candidate"}) do
 for _,activity in ipairs({"snowfield","melody"}) do
  local names=(activity=="snowfield") and names_snowfield or names_melody
  for _,aspect in ipairs(aspects) do
   local dir=root.."/"..lane.."_native/"..activity.."/"..aspect
   app.fs.makeDirectory(dir.."/phone")
   for _,name in ipairs(names) do
    local s=app.open(dir.."/"..name..".png")
    app.command.SpriteSize{ui=false,scale=0.3,method="bilinear"}
    s:saveCopyAs(dir.."/phone/"..name..".png")
    s:close()
   end
  end
 end
end
for _,activity in ipairs({"snowfield","melody"}) do
 local names=(activity=="snowfield") and names_snowfield or names_melody
 app.fs.makeDirectory(root.."/phone_comparisons/"..activity)
 for _,name in ipairs(names) do
  local board=Sprite(968,704,ColorMode.RGB)
  for row,aspect in ipairs(aspects) do
   local before=Image{fromFile=root.."/source_native/"..activity.."/"..aspect.."/phone/"..name..".png"}
   local after=Image{fromFile=root.."/candidate_native/"..activity.."/"..aspect.."/phone/"..name..".png"}
   board.cels[1].image:drawImage(before,Point(0,(row-1)*232))
   board.cels[1].image:drawImage(after,Point(488,(row-1)*232))
  end
  board:saveCopyAs(root.."/phone_comparisons/"..activity.."/"..name..".png")
  board:close()
 end
end
