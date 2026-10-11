-- A complete source image is transformed once, then installed as one cel.
-- No region selection, part layer, crossfade or synthetic in-between.
local f=io.open(app.params.plan,'r');local plan=json.decode(f:read('*a'));f:close()
local out=plan.output;app.fs.makeDirectory(out);app.fs.makeDirectory(out..'/frames')
local sprite=Sprite(plan.canvas[1],plan.canvas[2],ColorMode.RGB)
sprite.layers[1].name='Whole Roshan drawing'
local cache={}
for i,row in ipairs(plan.frames) do
 if i>1 then sprite:newFrame() end
 local key=row.path..'|'..tostring(row.width)..'|'..tostring(row.x)..'|'..tostring(row.y)
 if not cache[key] then
  local image=Image{fromFile=row.path}
  if not row.exact then
   for it in image:pixels() do if app.pixelColor.rgbaA(it())<=plan.alpha_floor then it(0) end end
   image:resize{width=row.width,height=row.width,method='bilinear'}
  end
  local canvas=Image(plan.canvas[1],plan.canvas[2],ColorMode.RGB)
  canvas:drawImage(image,Point(row.x,row.y));cache[key]=canvas
 end
 sprite.cels[i].image=Image(cache[key])
 sprite.frames[i].duration=row.duration_ms/1000
 sprite.cels[i].image:saveAs(out..string.format('/frames/%04d.png',i-1))
end
local tag=sprite:newTag(1,#plan.frames);tag.name='wave';tag.aniDir=AniDir.FORWARD
sprite:saveAs(out..'/wave.aseprite');sprite:saveAs(out..'/wave.gif')
local board=Image(plan.canvas[1]*8,plan.canvas[2]*math.ceil(#plan.frames/8),ColorMode.RGB)
board:clear(app.pixelColor.rgba(245,245,245,255))
for i,cel in ipairs(sprite.cels) do board:drawImage(cel.image,Point(((i-1)%8)*plan.canvas[1],math.floor((i-1)/8)*plan.canvas[2])) end
board:saveAs(out..'/contact_sheet.png');sprite:close()
print('WHOLE_CEL_ASSEMBLY '..#plan.frames..' frames')
