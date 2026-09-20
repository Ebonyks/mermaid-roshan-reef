local s=app.open(app.params.source)
local pc=app.pixelColor
local linear={}
for v=0,255 do local x=v/255;linear[v]=x<=.04045 and x/12.92 or ((x+.055)/1.055)^2.4 end
local function encode(v) local x=v<=.0031308 and 12.92*v or 1.055*v^(1/2.4)-.055;return math.max(0,math.min(255,math.floor(x*255+.5))) end
local function smooth(a,b,x) local t=math.max(0,math.min(1,(x-a)/(b-a)));return t*t*(3-2*t) end
local changed=0
for _,c in ipairs(s.cels) do
 local im=Image(c.image)
 for it in im:pixels() do
  local p=it();local R,G,B=pc.rgbaR(p),pc.rgbaG(p),pc.rgbaB(p)
  local color=Color{r=R,g=G,b=B,a=pc.rgbaA(p)}
  local h=color.hsvHue;local sat=color.hsvSaturation
  local weight=smooth(45,65,h)*(1-smooth(165,190,h))*smooth(.10,.32,sat)
  if pc.rgbaA(p)>0 and weight>0 then
   local r,g,b=linear[R],linear[G],linear[B];local l=.2126*r+.7152*g+.0722*b
   local t=smooth(.04,.30,l);local gain=.96-.23*t
   it(pc.rgba(encode(r*(1-weight+weight*gain*.80)),encode(g*(1-weight+weight*gain)),encode(b*(1-weight+weight*gain*1.16)),pc.rgbaA(p)));changed=changed+1
  end
 end
 c.image=im
end
s:saveAs(app.params.out..'/huckleberry-leaf-grade.aseprite')
for k=1,#s.frames do local im=Image(s.width,s.height,ColorMode.RGB);im:drawSprite(s,k);im:saveAs(app.params.out..string.format('/cel-%02d.png',k-1)) end
for _,l in ipairs(s.layers) do local c=l:cel(1);local im=Image(s.width,s.height,ColorMode.RGB);im:drawImage(c.image,c.position);im:saveAs(app.params.out..'/'..l.name..'.png') end
print('GRADED_PIXELS '..changed..' FRAMES '..#s.frames..' LAYERS '..#s.layers)
s:close()
local a=app.open(app.params.source);local b=app.open(app.params.out..'/huckleberry-leaf-grade.aseprite')
assert(#a.frames==8 and #b.frames==8)
for i,l in ipairs(a.layers) do
 assert(b.layers[i].name==l.name)
 for k=1,8 do
  local x,y=l:cel(k),b.layers[i]:cel(k);assert(x.position==y.position and x.image.width==y.image.width and x.image.height==y.image.height)
 end
end
for k=1,8 do
 assert(a.frames[k].duration==b.frames[k].duration)
 local im=Image(a.width,a.height,ColorMode.RGB);im:drawSprite(a,k);im:saveAs(app.params.out..string.format('/original-%02d.png',k-1))
 local im2=Image(b.width,b.height,ColorMode.RGB);im2:drawSprite(b,k);im2:saveAs(app.params.out..string.format('/reopen-%02d.png',k-1))
end
print('REOPEN_TIMING_GEOMETRY PASS')
