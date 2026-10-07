local p=app.params.packet;local root=app.params.root;local take=app.params.take;local out=app.params.output
app.fs.makeDirectory(out)
local native=p..'/'..take..'/refined_frames';local old=root..'/assets_src/cinematics/ltx25_scale_filter_v2_20261004/frames'
local s=Sprite(640,896,ColorMode.RGB);s.layers[1].name='Native Union LTX2.5 entire generated frame; no pixel repair'
for i=0,40 do
 if i>0 then s:newFrame() end
 local image=Image{fromFile=native..string.format('/%04d.png',i)};assert(image.width==640 and image.height==896)
 s.cels[i+1].image=image;s.frames[i+1].duration=(math.floor((i+1)*1000/24+.5)-math.floor(i*1000/24+.5))/1000
 local triple=Image(1920,896,ColorMode.RGB);triple:clear(Color{r=238,g=238,b=238,a=255})
 triple:drawImage(Image{fromFile=old..string.format('/%04d.png',i)},Point(8,32))
 triple:drawImage(Image{fromFile=p..string.format('/guide_full/%04d.png',i)},Point(640,0))
 triple:drawImage(image,Point(1280,0));triple:saveAs(out..string.format('/%04d.png',i))
end
s:saveAs(p..'/'..take..'/native_review.aseprite');s:close()
print('Native41-frame master +1920x896 prior-v2/structural-guide/Union comparison')
