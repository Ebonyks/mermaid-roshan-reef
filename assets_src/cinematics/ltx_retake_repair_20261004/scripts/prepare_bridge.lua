local root=app.params.packet
local corrected=Sprite{fromFile=root..'/inputs/corrected_0048_native.png'}
app.activeSprite=corrected
app.command.SpriteSize{ui=false,width=896,height=512,method='bilinear'}
corrected:saveAs(root..'/inputs/corrected_0048.png');corrected:close()
local s=Sprite(896,512,ColorMode.RGB)
local original=s.layers[1];original.name='Original full-frame entry, defect and exit (hidden reference)';original.isVisible=false
local clean=s:newLayer();clean.name='Complete-figure clean guides; no fixed-body composite'
for i,item in ipairs({{40,'original_0040.png'},{48,'corrected_0048.png'},{64,'original_0064.png'}}) do
 if i>1 then s:newFrame() end
 local raw=Image{fromFile=root..string.format('/inputs/original_%04d.png',item[1])}
 s:newCel(original,i,raw,Point(0,0))
 local key=Image{fromFile=root..'/inputs/'..item[2]};s:newCel(clean,i,key,Point(0,0))
 s.frames[i].duration=({8/24,16/24,1/24})[i]
end
for i,global in ipairs({40,48,64}) do local tag=s:newTag(i,i);tag.name='native_frame_'..global..(i==2 and '_whole_figure_redraw' or '_boundary_reference') end
local rootmark=s:newSlice(Rectangle(0,0,896,512));rootmark.name='Waist registration landmark; permits body motion';rootmark.pivot=Point(461,280)
s:saveAs(root..'/inputs/repair_keys.aseprite');s:close()
