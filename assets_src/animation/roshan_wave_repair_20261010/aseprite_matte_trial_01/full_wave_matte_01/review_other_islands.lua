local root=app.params.root;local f=io.open(root..'/source_and_seed_plan.json','r');local plan=json.decode(f:read('*a'));f:close()
local board=Image(128*8,192*6,ColorMode.RGB);board:clear(app.pixelColor.rgba(45,55,68,255))
for _,row in ipairs(plan.sources) do
 local n=row.index;local im=Image{fromFile=root..string.format('/sources/%04d.png',n)}
 local crop=Image(128,192,ColorMode.RGB);crop:drawImage(im,Point(-140,-190))
 for _,item in ipairs(row.left_curl_gap_components) do local sx,sy=item.seed[1]-140,item.seed[2]-190;for d=-2,2 do crop:drawPixel(sx+d,sy,app.pixelColor.rgba(255,0,0,255));crop:drawPixel(sx,sy+d,app.pixelColor.rgba(255,0,0,255)) end end
 for _,item in ipairs(row.other_unclassified_closed_neutral_components) do local sx,sy=math.floor(item.bbox[1]+item.bbox[3]/2)-140,math.floor(item.bbox[2]+item.bbox[4]/2)-190;for d=-2,2 do crop:drawPixel(sx+d,sy,app.pixelColor.rgba(0,0,255,255));crop:drawPixel(sx,sy+d,app.pixelColor.rgba(0,0,255,255)) end end
 board:drawImage(crop,Point((n%8)*128,math.floor(n/8)*192))
end
board:saveAs(root..'/left_curl_and_other_islands_review_board.png')
