local ok,err=pcall(function()
local out=app.params.out
local s=app.open(out..'/wave_driver.aseprite')
for _,cel in ipairs(s.cels) do
 local raw=cel.image
 local mask=Image(raw.width,raw.height,ColorMode.RGB)
 mask:clear(Color{r=0,g=0,b=0,a=255})
 for y=0,raw.height-1 do for x=0,raw.width-1 do
  local p=raw:getPixel(x,y)
  local r=app.pixelColor.rgbaR(p);local g=app.pixelColor.rgbaG(p);local b=app.pixelColor.rgbaB(p)
  if math.max(math.abs(r-238),math.abs(g-238),math.abs(b-238))>24 then
   mask:drawPixel(x,y,app.pixelColor.rgba(0,0,255,255))
  end
 end end
 cel.image=mask
end
s.layers[1].name='Owned driver colored subject mask; threshold against neutral backdrop'
s:saveAs(out..'/wave_mask.aseprite');s:saveAs(out..'/wave_mask.gif');s:close()

end)
if not ok then print(tostring(err)) else print('MASK_PASS') end
