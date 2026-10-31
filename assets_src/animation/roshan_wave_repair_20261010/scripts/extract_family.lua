local root=app.params.root
local source=Image{fromFile=root..'/native.png'}
local out=root..'/cells';app.fs.makeDirectory(out)
local count=4;local cell=math.ceil(source.width/count)
local sheet=Sprite(cell,cell,ColorMode.RGB);sheet.layers[1].name='Complete painted cel'
for i=0,15 do
 if i>0 then sheet:newFrame() end
 local image=Image(cell,cell,ColorMode.RGB)
 image:drawImage(source,Point(-math.floor((i%4)*source.width/count),-math.floor(math.floor(i/4)*source.height/count)))
 sheet.cels[i+1].image=image
 image:saveAs(out..string.format('/%04d.png',i))
end
sheet:saveAs(root..'/native_cells.aseprite');sheet:close()
local preview=Sprite(cell,cell,ColorMode.RGB);preview.layers[1].name='Single whole cel with alpha cleanup candidate'
local image=Image{fromFile=out..'/0009.png'}
for it in image:pixels() do
 local v=it(); local a=app.pixelColor.rgbaA(v)
 if a<=16 then it(app.pixelColor.rgba(0,0,0,0)) end
end
preview.cels[1].image=image
local bg=Image(cell,cell,ColorMode.RGB);bg:clear(app.pixelColor.rgba(245,245,245,255));bg:drawImage(image)
bg:saveAs(root..'/clean_alpha_test_on_gray.png');image:saveAs(root..'/clean_alpha_test.png')
preview:close()
print('Whole cells extracted through Aseprite; native untouched')
