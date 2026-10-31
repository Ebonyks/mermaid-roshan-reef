local root=app.params.root
local f=io.open(root..'/SAMPLES.json','r');local list=json.decode(f:read('*a'));f:close()
for _,s in ipairs(list) do
 local path=root..'/objects/'..s.id..'/'..s.id..'.aseprite'
 local sprite=app.open(path)
 for n,frame in ipairs(sprite.frames) do frame.duration=(s.durations[n] or 2)/12 end
 sprite:saveAs(path);sprite:close()
end
print('Native pose-key timing updated. Gate return is explicitly in the gallery timeline.')
