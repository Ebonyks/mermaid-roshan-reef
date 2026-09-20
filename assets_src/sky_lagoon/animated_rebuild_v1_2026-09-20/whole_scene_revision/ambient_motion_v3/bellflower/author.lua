local s=app.open(app.params.source)
local pc=app.pixelColor
local leaves=nil
for _,l in ipairs(s.layers) do if l.name=='leaves_fixed' then leaves=l end end
assert(leaves~=nil)
local source=Image(512,512,ColorMode.RGB);source:drawImage(leaves:cel(1).image,leaves:cel(1).position)
local phases={0,.55,1,.55,0,-.55,-1,-.55}
local function smooth(a,b,x) local t=math.max(0,math.min(1,(x-a)/(b-a)));return t*t*(3-2*t) end
local function sample(im,x,y)
 local x0,y0=math.floor(x),math.floor(y);local fx,fy=x-x0,y-y0
 local ra,ga,ba,aa=0,0,0,0
 for dy=0,1 do for dx=0,1 do
  local px,py=x0+dx,y0+dy
  if px>=0 and px<512 and py>=0 and py<512 then
   local w=(dx==0 and 1-fx or fx)*(dy==0 and 1-fy or fy)
   local c=im:getPixel(px,py);local a=pc.rgbaA(c)*w
   aa=aa+a;ra=ra+pc.rgbaR(c)*a;ga=ga+pc.rgbaG(c)*a;ba=ba+pc.rgbaB(c)*a
  end
 end end
 if aa<.5 then return 0 end
 return pc.rgba(math.floor(ra/aa+.5),math.floor(ga/aa+.5),math.floor(ba/aa+.5),math.floor(aa+.5))
end

for f=1,8 do
 local im=Image(512,512,ColorMode.RGB)
 for y=0,511 do for x=0,511 do
  local root=1-smooth(415,452,y)
  local stem=1-(1-smooth(8,28,math.abs(x-283)))*(1-smooth(365,405,y))
  local reach=math.max(0,math.min(1,(468-y)/210))
  local dx=phases[f]*4.5*root*stem*reach
  local dy=phases[f]*.7*root*stem*math.min(1,math.abs(x-308)/180)
  if dx==0 and dy==0 then im:drawPixel(x,y,source:getPixel(x,y)) else im:drawPixel(x,y,sample(source,x-dx,y-dy)) end
 end end
 leaves:cel(f).image=im;leaves:cel(f).position=Point(0,0)
 im:saveAs(app.params.out..string.format('/leaves-%02d.png',f-1))
end
leaves.name='leaves_rooted_breeze'
s:saveAs(app.params.out..'/bellflower-whole-leaf.aseprite')
for f=1,8 do local im=Image(s.spec);im:drawSprite(s,f);im:saveAs(app.params.out..string.format('/cel-%02d.png',f-1)) end
s:close()
local a=app.open(app.params.source);local b=app.open(app.params.out..'/bellflower-whole-leaf.aseprite');local untouched=0
for i,l in ipairs(a.layers) do
 for f=1,8 do
  local x,y=l:cel(f),b.layers[i]:cel(f)
  if l.name~='leaves_fixed' then assert(x.position==y.position and x.image.bytes==y.image.bytes);untouched=untouched+1 end
 end
end
assert(untouched==40)
for f=1,8 do assert(a.frames[f].duration==b.frames[f].duration);local im=Image(b.spec);im:drawSprite(b,f);im:saveAs(app.params.out..string.format('/reopen-%02d.png',f-1)) end
print('PASS eight frames,forty non-leaf cels exact,original timing preserved')
a:close();b:close()
