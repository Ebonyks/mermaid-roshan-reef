local root=app.params["packet"]
local total=0
for _,name in ipairs({"fir_crown","meadow_flowers","lakeside_lupines","lake_ripples"}) do
 local s=app.open(root.."/"..name..".aseprite")
 assert(#s.layers==1 and #s.frames==32 and #s.cels==32,name.." structure")
 for i=0,31 do
  assert(math.abs(s.frames[i+1].duration-0.125)<0.001,name.." duration")
  local expected=Image{fromFile=root.."/demo_project/"..name.."/"..string.format("%02d.png",i)}
  assert(s.cels[i+1].image:isEqual(expected),name.." frame "..i.." differs")
  total=total+1
 end
 s:close()
end
local receipt=assert(io.open(root.."/evidence/aseprite-verification.json","w"))
receipt:write('{"result":"PASS","masters":4,"layers_per_master":1,"frames_per_master":32,"rgba_cels_verified":'..total..',"frame_duration_ms":125,"aseprite_version":"'..tostring(app.version)..'","check_time_utc":"'..os.date('!%Y-%m-%dT%H:%M:%SZ')..'"}\n')
receipt:close()
