local root=app.params.root;local columns=tonumber(app.params.columns);local rows=tonumber(app.params.rows)
local source=Image{fromFile=root..'/native.png'};local cw=math.ceil(source.width/columns);local ch=math.ceil(source.height/rows)
app.fs.makeDirectory(root..'/cells');local sprite=Sprite(cw,ch,ColorMode.RGB)
sprite.layers[1].name='Complete native drawings'
for i=0,columns*rows-1 do
 if i>0 then sprite:newFrame() end
 local image=Image(cw,ch,ColorMode.RGB)
 image:drawImage(source,Point(-math.floor(i%columns*source.width/columns),-math.floor(math.floor(i/columns)*source.height/rows)))
 sprite.cels[i+1].image=image;image:saveAs(root..string.format('/cells/%04d.png',i))
end
sprite:saveAs(root..'/native_cells.aseprite');sprite:close()
