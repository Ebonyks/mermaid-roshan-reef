local root=app.params['root']
local out=app.params['out']
local function centered(src, dest, scale)
 local s=app.open(src)
 app.command.SpriteSize{width=math.floor(s.width*scale+0.5),height=math.floor(s.height*scale+0.5),method='bilinear'}
 local img=s.cels[1].image
 local master=Sprite(896,512,ColorMode.RGB)
 master.layers[1].name='Source on shared neutral field'
 local bg=Image(896,512,ColorMode.RGB);bg:clear(Color{r=238,g=238,b=238,a=255})
 bg:drawImage(img,Point(math.floor((896-img.width)/2),math.floor((512-img.height)/2)))
 master.cels[1].image=bg
 master:saveAs(dest..'.aseprite')
 bg:saveAs(dest..'.png')
 master:close();s:close()
end
centered(root..'/assets_src/cinematics/sky_lagoon_local_motion_v1_2026-09-30/objects/03_hydrangea/source.png',out..'/plant',1.65)
centered(root..'/assets_src/sky_lagoon/playground_revision_2026-07-29/swing_single_mermaid_gripfit_alpha_master.png',out..'/swing',0.38)
local atlas=app.open(root..'/assets/characters/roshan_25d/roshan_gesture_a.png')
local wave=Sprite(896,512,ColorMode.RGB)
wave.layers[1].name='Approved wave keys on shared neutral field'
for i=0,3 do
 local cell=Image(atlas.cels[1].image,Rectangle(i*256,0,256,256))
 local key=Sprite(256,256,ColorMode.RGB); key.cels[1].image=cell
 app.command.SpriteSize{width=460,height=460,method='bilinear'}
 local bg=Image(896,512,ColorMode.RGB); bg:clear(Color{r=238,g=238,b=238,a=255})
 bg:drawImage(key.cels[1].image,Point(218,26))
 if i>0 then wave:newFrame() end
 wave:newCel(wave.layers[1],i+1,bg,Point(0,0))
 wave.frames[i+1].duration=({0.3,0.4,0.4,0.4})[i+1]
 if i==0 then bg:saveAs(out..'/wave.png') end
 key:close()
end
wave:newFrame()
wave:newCel(wave.layers[1],5,Image(wave.cels[1].image),Point(0,0))
wave.frames[5].duration=0.5
wave:saveAs(out..'/wave_driver.aseprite')
wave:saveAs(out..'/wave_driver.gif')
wave:close();atlas:close()
