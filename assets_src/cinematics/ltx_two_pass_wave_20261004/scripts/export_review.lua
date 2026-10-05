local root=app.params.take
local folder=app.params.folder or 'native_frames'
local source=Image{fromFile=root..'/'..folder..'/0000.png'}
local s=Sprite(source.width,source.height,ColorMode.RGB)
s.layers[1].name='Unmodified complete model frames'
for i=0,40 do
 if i>0 then s:newFrame() end
 s.cels[i+1].image=Image{fromFile=root..'/'..folder..'/'..string.format('%04d.png',i)}
 s.frames[i+1].duration=(math.floor((i+1)*1000/24+.5)-math.floor(i*1000/24+.5))/1000
end
local t=s:newTag(20,27);t.name='CHECK_lowering_19_26'
s:saveAs(root..'/native_review.aseprite');s:close()
local twos=Sprite(source.width,source.height,ColorMode.RGB);twos.layers[1].name='Declared whole-frame cadence on twos; anatomy failures retained'
for n=0,20 do
 if n>0 then twos:newFrame() end
 local i=n*2;twos.cels[n+1].image=Image{fromFile=root..'/'..folder..'/'..string.format('%04d.png',i)}
 local finish=math.min(i+2,41)
 twos.frames[n+1].duration=(math.floor(finish*1000/24+.5)-math.floor(i*1000/24+.5))/1000
end
twos:saveAs(root..'/on_twos.aseprite');twos:close()
local c=Sprite(source.width*3,source.height,ColorMode.RGB);c.layers[1].name='Native1to1 frames19,22,25; no resize'
for n,i in ipairs({19,22,25}) do c.cels[1].image:drawImage(Image{fromFile=root..'/'..folder..'/'..string.format('%04d.png',i)},Point((n-1)*source.width,0)) end
c.cels[1].image:saveAs(root..'/lowering_native_contact.png');c:close()
