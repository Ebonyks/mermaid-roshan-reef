local s=app.open(app.params.source..'/meadow-berry-fan-eight-cels.aseprite')
local pc=app.pixelColor
local linear={}
for v=0,255 do local x=v/255;linear[v]=(x<=.04045) and x/12.92 or ((x+.055)/1.055)^2.4 end
local function encode(v) local x=(v<=.0031308) and 12.92*v or 1.055*v^(1/2.4)-.055;return math.max(0,math.min(255,math.floor(x*255+.5))) end
local cache={}
for _,cel in ipairs(s.cels) do
 local im=Image(cel.image)
 for it in im:pixels() do
  local c=it()
  if pc.rgbaA(c)>0 then
   local replacement=cache[c]
   if not replacement then
    local r,g,b=linear[pc.rgbaR(c)],linear[pc.rgbaG(c)],linear[pc.rgbaB(c)]
    local lum=.2126*r+.7152*g+.0722*b
    local t=math.max(0,math.min(1,(lum-.08)/.28));t=t*t*(3-2*t)
    local leafGain=.88-.36*t
    local rs,gs,bs=pc.rgbaR(c)/255,pc.rgbaG(c)/255,pc.rgbaB(c)/255
    local purple=math.max(0,math.min(1,(math.min(rs/math.max(gs,.001),bs/math.max(gs,.001))-1)/.18))
    local berryGain=.72-.20*math.min(1,lum/.25)
    local gain=leafGain*(1-purple)+berryGain*purple
    replacement=pc.rgba(encode(r*gain),encode(g*gain),encode(b*gain),pc.rgbaA(c));cache[c]=replacement
   end
   it(replacement)
  end
 end
 cel.image=im
end
s:saveAs(app.params.out..'/meadow-berry-fan-color-trial.aseprite')
for k=1,8 do
 local im=Image(s.width,s.height,ColorMode.RGB);im:drawSprite(s,k);im:saveAs(app.params.out..string.format('/cel-%02d.png',k-1))
 for _,l in ipairs(s.layers) do local c=l:cel(k);local layer=Image(s.width,s.height,ColorMode.RGB);layer:drawImage(c.image,c.position);layer:saveAs(app.params.out..'/'..l.name..string.format('-cel-%02d.png',k-1)) end
end
s:close()
