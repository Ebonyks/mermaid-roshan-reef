local root=app.params.packet
local shifts={{0,0},{17,-3},{58,2},{81,-7}}
local s=Sprite(896,512,ColorMode.RGB);local figure=s.layers[1];figure.name='Complete approved source figure; whole-canvas integer root registration'
local bg=s:newLayer();bg.name='Neutral conditioning field';bg.stackIndex=1
for k=0,3 do
 if k>0 then s:newFrame() end
 local src=Image{fromFile=root..string.format('/inputs/source_rgba_%02d.png',k)}
 local registered=Image(896,512,ColorMode.RGB);registered:drawImage(src,Point(shifts[k+1][1],shifts[k+1][2]))
 local gray=Image(896,512,ColorMode.RGB);gray:clear(Color{r=238,g=238,b=238,a=255})
 s:newCel(bg,k+1,gray,Point(0,0));s:newCel(figure,k+1,registered,Point(0,0));s.frames[k+1].duration=({0.3,0.4,0.4,0.608})[k+1]
 registered:saveAs(root..string.format('/inputs/figure_rgba_%02d.png',k));gray:drawImage(registered,Point(0,0));gray:saveAs(root..string.format('/inputs/figure_key_%02d.png',k))
end
local slice=s:newSlice(Rectangle(0,0,896,512));slice.name='STUDY_root_anchor_not_pixel_freeze';slice.pivot=Point(461,280)
s:saveAs(root..'/inputs/figure_keys.aseprite');s:close()
