-- Reversible material grade: only the existing leaf layer, every cel.
local s=app.open(app.params.source)
local pc=app.pixelColor
local linear={}
for v=0,255 do local x=v/255; linear[v]=x<=.04045 and x/12.92 or ((x+.055)/1.055)^2.4 end
local function encode(v)
 local x=v<=.0031308 and 12.92*v or 1.055*v^(1/2.4)-.055
 return math.max(0,math.min(255,math.floor(x*255+.5)))
end
local changed=0
for _,c in ipairs(s.cels) do
 if c.layer.name=='leaves_fixed' then
  local im=Image(c.image)
  for it in im:pixels() do
   local p=it()
   if pc.rgbaA(p)>0 then
    local r,g,b=linear[pc.rgbaR(p)],linear[pc.rgbaG(p)],linear[pc.rgbaB(p)]
    local l=.2126*r+.7152*g+.0722*b
    local t=math.max(0,math.min(1,(l-.035)/.20));t=t*t*(3-2*t)
    local gain=.88-.20*t
    it(pc.rgba(encode(r*gain*.90),encode(g*gain),encode(b*gain*1.10),pc.rgbaA(p)))
   end
  end
  c.image=im;changed=changed+1
 end
end
assert(changed==8,'Expected eight leaf cels')
s:saveAs(app.params.out..'/bellflower-leaf-grade.aseprite')
for _,l in ipairs(s.layers) do
 local c=l:cel(1);local im=Image(s.width,s.height,ColorMode.RGB)
 im:drawImage(c.image,c.position);im:saveAs(app.params.out..'/'..l.name..'.png')
end
for k=1,8 do
 local im=Image(s.width,s.height,ColorMode.RGB);im:drawSprite(s,k)
 im:saveAs(app.params.out..string.format('/cel-%02d.png',k-1))
end
s:close()
local original=app.open(app.params.source)
local candidate=app.open(app.params.out..'/bellflower-leaf-grade.aseprite')
assert(#original.frames==8 and #candidate.frames==8)
local untouched=0
for i,l in ipairs(original.layers) do
 assert(candidate.layers[i].name==l.name)
 for k=1,8 do
  local a,b=l:cel(k),candidate.layers[i]:cel(k)
  assert(a.position==b.position and a.image.width==b.image.width and a.image.height==b.image.height)
  if l.name~='leaves_fixed' then assert(a.image.bytes==b.image.bytes);untouched=untouched+1 end
 end
end
assert(untouched==40)
for k=1,8 do assert(original.frames[k].duration==candidate.frames[k].duration) end
print('LEAF_GRADE|8 frames; 40 non-leaf cels byte-exact; positions and timing preserved|PASS')
candidate:close();original:close()
