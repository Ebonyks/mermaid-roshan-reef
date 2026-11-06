local root=app.params['packet']
local names={'lake_foxtails','meadow_spikes','arrival_bells'}
local receipt=io.open(root..'/evidence/aseprite-build.txt','w')
receipt:write('Aseprite '..tostring(app.version)..'\n')
for _,name in ipairs(names) do
  local s=Sprite(512,512,ColorMode.RGB)
  s.layers[1].name='Complete original context - gentle breeze'
  for i=0,59 do
    if i>0 then s:newEmptyFrame() end
    local im=Image{fromFile=root..'/frames/'..name..'/'..string.format('%03d',i)..'.png'}
    s:newCel(s.layers[1],i+1,im,Point(0,0))
    s.frames[i+1].duration=(i%3==2) and 0.034 or 0.033
  end
  local tag=s:newTag(1,60);tag.name='rooted_breeze_2s'
  s:saveAs(root..'/'..name..'.aseprite')
  s:close()
  local check=app.open(root..'/'..name..'.aseprite')
  app.fs.makeDirectory(root..'/roundtrip/'..name)
  local total=0
  for i=1,60 do
    local im=Image(check.spec)
    im:drawSprite(check,i)
    im:saveAs(root..'/roundtrip/'..name..'/'..string.format('%03d',i-1)..'.png')
    total=total+check.frames[i].duration
  end
  receipt:write(name..' reopened/exported 60 frames duration='..total..'s\n')
  check:close()
end
receipt:close()
