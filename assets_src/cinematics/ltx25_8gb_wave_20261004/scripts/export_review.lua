local root=app.params.take
local folder=app.params.folder or 'refined_frames'
local count=tonumber(app.params.count or '41')
local fps=tonumber(app.params.fps or '24')
local source=Image{fromFile=root..'/'..folder..'/0000.png'}
local s=Sprite(source.width,source.height,ColorMode.RGB)
s.layers[1].name='Unmodified complete LTX2.5 model frames'
for i=0,count-1 do
 if i>0 then s:newFrame() end
 s.cels[i+1].image=Image{fromFile=root..'/'..folder..'/'..string.format('%04d.png',i)}
 s.frames[i+1].duration=(math.floor((i+1)*1000/fps+.5)-math.floor(i*1000/fps+.5))/1000
end
local multiplier=fps/24
local t=s:newTag(math.floor(17*multiplier)+1,math.floor(32*multiplier)+1);t.name='CHECK_whole_figure_lowering'
local t2=s:newTag(math.floor(19*multiplier)+1,math.floor(26*multiplier)+1);t2.name='CHECK_finger_continuity'
s:saveAs(root..'/native_review.aseprite');s:close()
local c=Sprite(source.width*3,source.height,ColorMode.RGB);c.layers[1].name='Native1to1 frames19,22,25 at24fps-equivalent times'
for n,i in ipairs({19,22,25}) do c.cels[1].image:drawImage(Image{fromFile=root..'/'..folder..'/'..string.format('%04d.png',math.floor(i*multiplier))},Point((n-1)*source.width,0)) end
c.cels[1].image:saveAs(root..'/lowering_native_contact.png');c:close()
