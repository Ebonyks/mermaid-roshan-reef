local root=app.params.take
for _,kind in ipairs({'stage1','refined_native','requested_canvas'}) do
 local dims=({stage1={352,544},refined_native={704,1088},requested_canvas={576,832}})[kind]
 local s=Sprite(dims[1],dims[2],ColorMode.RGB);s.layers[1].name='Unchanged complete model frames'
 for i=0,40 do if i>0 then s:newFrame() end;s.cels[i+1].image=Image{fromFile=root..'/'..kind..'_frames/'..string.format('%04d.png',i)};s.frames[i+1].duration=(math.floor((i+1)*1000/24+.5)-math.floor(i*1000/24+.5))/1000 end
 local tag=s:newTag(20,27);tag.name='REVIEW_lowering_19_26';local tag2=s:newTag(23,23);tag2.name='CHECK_mid_key22_actual_pose';s:saveAs(root..'/'..kind..'.aseprite');s:close()
end
local contact=Sprite(704*3,1088,ColorMode.RGB);contact.layers[1].name='Native1to1 frames19,22,25; no resize'
for n,idx in ipairs({19,22,25}) do contact.cels[1].image:drawImage(Image{fromFile=root..'/refined_native_frames/'..string.format('%04d.png',idx)},Point((n-1)*704,0)) end
contact.cels[1].image:saveAs(root..'/lowering_native_contact.png');contact:close()
