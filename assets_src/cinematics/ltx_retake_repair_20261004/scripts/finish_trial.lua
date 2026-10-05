local root=app.params.packet
local take=app.params.take
local first=Image{fromFile=root..'/results/'..take..'/native_frames/0000.png'}
local width=first.width;local height=first.height
local function reference(file)
 local temp=Sprite{fromFile=file};app.activeSprite=temp
 if temp.width~=width or temp.height~=height then app.command.SpriteSize{ui=false,width=width,height=height,method='bilinear'} end
 local image=Image(temp.cels[1].image);temp:close();return image
end
local s=Sprite(width,height,ColorMode.RGB)
local visible=s.layers[1];visible.name='Complete native generated repair window; unmasked'
local original=s:newLayer();original.name='Original full-frame comparison; whole-canvas scaled if needed (hidden)';original.isVisible=false
local guides=s:newLayer();guides.name='Whole-figure guides; whole-canvas scaled if needed (hidden)';guides.isVisible=false
for i=0,24 do
 app.activeSprite=s
 if i>0 then s:newFrame() end
 s:newCel(visible,i+1,Image{fromFile=root..'/results/'..take..string.format('/native_frames/%04d.png',i)},Point(0,0))
 s:newCel(original,i+1,reference(root..string.format('/inputs/source_frames/%04d.png',i+40)),Point(0,0))
 s.frames[i+1].duration=(math.floor((i+1)*1000/24+0.5)-math.floor(i*1000/24+0.5))/1000
end
for _,pair in ipairs({{1,'original_0040.png'},{9,'corrected_0048.png'},{25,'original_0064.png'}}) do
 s:newCel(guides,pair[1],reference(root..'/inputs/'..pair[2]),Point(0,0))
end
local tag=s:newTag(5,13);tag.name='Original defect span 44-52; whole-figure regeneration'
local mark=s:newSlice(Rectangle(0,0,width,height));mark.name='Registration root permits figure motion';mark.pivot=Point(math.floor(461*width/896+0.5),math.floor(280*height/512+0.5))
app.activeSprite=s;s:saveAs(root..'/results/'..take..'/repair_window.aseprite');s:close()
