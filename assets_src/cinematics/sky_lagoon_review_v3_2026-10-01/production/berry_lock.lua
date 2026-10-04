local root=app.params.root
local dir=root..'/objects/02_huckleberry'
local f=io.open(dir..'/BERRY_LOCK.json','r');local cfg=json.decode(f:read('*a'));f:close()
local sprite=app.open(dir..'/02_huckleberry.aseprite')
local source=Image{fromFile=dir..'/frames/frame_00.png'}
for n,frame in ipairs(sprite.frames) do
 local out=Image{fromFile=dir..string.format('/frames/frame_%02d.png',n-1)}
 for _,run in ipairs(cfg.runs) do for x=run[2],run[3] do out:drawPixel(x,run[1],source:getPixel(x,run[1])) end end
 local cel=sprite.layers[1]:cel(frame.frameNumber);assert(cel,'Missing berry cel');cel.image=out
 out:saveAs(dir..string.format('/frames/frame_%02d.png',n-1))
end
sprite:saveAs(dir..'/02_huckleberry.aseprite')
sprite:close()
print('Two fixed berry clusters: Aseprite junction cleanup applied.')
