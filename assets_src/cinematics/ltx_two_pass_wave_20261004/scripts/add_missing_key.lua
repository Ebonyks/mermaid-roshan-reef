local root=app.params.packet
local src=app.open(root..'/inputs/missing_lowering_native.png');app.activeSprite=src
app.command.SpriteSize{ui=false,width=576,height=864,method='bilinear'}
local img=Image(576,832,ColorMode.RGB);img:clear(app.pixelColor.rgba(0,0,0,0));img:drawImage(src.cels[1].image,Point(-32,8));src:close()
img:saveAs(root..'/inputs/portrait_rgba_mid.png')
local gray=Image(576,832,ColorMode.RGB);gray:clear(Color{r=238,g=238,b=238,a=255});gray:drawImage(img,Point(0,0));gray:saveAs(root..'/inputs/portrait_key_mid.png')
local indices={0,3,7,17,22,27,36,40};local poses={'00','00','01','02','mid','03','00','00'}
local s=Sprite(576,832,ColorMode.RGB);s.layers[1].name='Complete figure guide; editable native exports'
for k,idx in ipairs(indices) do
 if k>1 then s:newFrame() end
 s.cels[k].image=Image{fromFile=root..'/inputs/portrait_key_'..poses[k]..'.png'}
 s.frames[k].duration=((indices[k+1] or 41)-idx)/24
end
for k,idx in ipairs(indices) do local tag=s:newTag(k,k);tag.name=string.format('guide_frame_%04d',idx) end
local slice=s:newSlice(Rectangle(0,0,576,832));slice.name='Study waist registration; all body parts may act';slice.pivot=Point(183,453)
s:saveAs(root..'/inputs/wave_guides.aseprite')
for k,idx in ipairs(indices) do s.cels[k].image:saveAs(root..string.format('/inputs/guide_%04d.png',idx)) end
s:close()
