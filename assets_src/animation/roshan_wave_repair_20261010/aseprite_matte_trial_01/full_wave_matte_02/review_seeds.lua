local root=app.params.root;local pc=app.pixelColor
local f=io.open(root..'/source_and_seed_plan.json','r');local plan=json.decode(f:read('*a'));f:close()
local right=Image(1024,672,ColorMode.RGB);local left=Image(1024,1152,ColorMode.RGB)
for _,row in ipairs(plan.sources) do
 local n=row.index;local im=Image{fromFile=root..string.format('/sources/%04d.png',n)}
 local pad=im.width-640;local bx=405+pad;local by=170;local crop=Image(im,Rectangle(bx,by,128,112))
 local sx,sy=row.hair_gap_component.seed[1]-bx,row.hair_gap_component.seed[2]-by
 for d=-4,4 do if d~=0 then crop:drawPixel(sx+d,sy,pc.rgba(255,0,0,255));crop:drawPixel(sx,sy+d,pc.rgba(255,0,0,255)) end end
 right:drawImage(crop,Point((n%8)*128,math.floor(n/8)*112))
 local leftCrop=Image(im,Rectangle(135+pad,200,128,192))
 for _,c in ipairs(row.left_curl_gap_components) do local xx,yy=c.seed[1]-135-pad,c.seed[2]-200;for d=-4,4 do if d~=0 then leftCrop:drawPixel(xx+d,yy,pc.rgba(255,0,0,255));leftCrop:drawPixel(xx,yy+d,pc.rgba(255,0,0,255)) end end end
 left:drawImage(leftCrop,Point((n%8)*128,math.floor(n/8)*192))
end
right:saveAs(root..'/hair_seed_review_board.png');left:saveAs(root..'/left_curl_and_other_islands_review_board.png')
