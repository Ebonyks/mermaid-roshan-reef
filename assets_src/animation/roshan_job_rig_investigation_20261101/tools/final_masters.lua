local root=assert(app.params.root)
for _,job in ipairs({"detective","geologist"}) do
 local s=Sprite(1024,1024,ColorMode.RGB);s:newEmptyFrame(2)
 local entries={
  {"Clean anatomy / old clothing absent","investigation_anatomy.png"},
  {"Complete tail / own silhouette",job.."_tail.png"},
  {"Body and cape / torso ownership",job.."_body.png"},
  {"New sleeve / LeftUpper pivot474.74,379.76",job.."_sleeve.png"},
  {"UpperArm / original identity","upper_clean.png"},
  {"Forearm / original versus work wrist","forearm.png","fore_work.png"},
  {"Clean scalp / source-derived","ballet_scalp.png"},
  {"Headwear / Head rest",job.."_head.png"},
  {"Closed grasp / LeftHand socket24,0",nil,"grip_front.png"}
 }
 for i,e in ipairs(entries) do
  local l=i==1 and s.layers[1] or s:newLayer();l.name=e[1]
  for frame=1,2 do
   local f=(frame==2 and e[3]) or e[2]
   if f then s:newCel(l,frame,Image{fromFile=root.."/demo/art/"..f},Point(0,0)) end
  end
 end
 s.frames[1].duration=0.5;s.frames[2].duration=0.5
 local t=s:newTag(1,1);t.name="open_hand_source_parts"
 local u=s:newTag(2,2);u.name="closed_grasp_source_parts"
 s:saveAs(root.."/masters/"..job.."_binding.aseprite");s:close()
 local reopened=Sprite{fromFile=root.."/masters/"..job.."_binding.aseprite"}
 for i,l in ipairs(reopened.layers) do
  for _,cel in ipairs(l.cels) do
   local out=Image(1024,1024,ColorMode.RGB);out:drawImage(cel.image,cel.position)
   out:saveAs(root.."/evidence/master_roundtrip/"..job.."_"..i.."_"..cel.frameNumber..".png")
  end
 end
 reopened:close()
end
print("FINAL_MASTERS_REOPENED")
