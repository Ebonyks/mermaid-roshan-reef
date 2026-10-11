local root=app.params.root;local f=io.open(root..'/source_and_seed_plan.json','r');local plan=json.decode(f:read('*a'));f:close()
local board=Image(128*8,112*6,ColorMode.RGB);board:clear(app.pixelColor.rgba(45,55,68,255))
for _,row in ipairs(plan.sources) do
 local n=row.index;local im=Image{fromFile=root..string.format('/sources/%04d.png',n)}
 local crop=Image(128,112,ColorMode.RGB);crop:drawImage(im,Point(-400,-170))
 local seed=row.hair_gap_component.seed;local sx,sy=seed[1]-400,seed[2]-170
 for d=-3,3 do crop:drawPixel(sx+d,sy,app.pixelColor.rgba(255,0,0,255));crop:drawPixel(sx,sy+d,app.pixelColor.rgba(255,0,0,255)) end
 board:drawImage(crop,Point((n%8)*128,math.floor(n/8)*112))
end
board:saveAs(root..'/hair_seed_review_board.png')
