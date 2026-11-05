local root=assert(app.params.root);local out=root..'/review/frozen_v3';local pc=app.pixelColor
local function board(name,items,w,h)
 local s=Sprite(w,h,ColorMode.RGB);local back=Image(w,h,ColorMode.RGB);back:clear(pc.rgba(20,41,56,255));s.layers[1].name='neutral_review_canvas';s:newCel(s.layers[1],1,back,Point(0,0))
 for i,item in ipairs(items) do local im=Image{fromFile=out..'/'..item[1]..'.png'};local l=s:newLayer();l.name=item[1];s:newCel(l,1,im,Point(item[2],item[3])) end
 s:saveAs(out..'/'..name..'.aseprite');s:saveCopyAs(out..'/'..name..'.png');s:close()
end
board('outfits_and_glove_perspective',{{'boxer_0096',0,0},{'racer_0096',1024,0},{'popstar_0096',0,1024},{'boxer_0120',1024,1024}},2048,2048)
for _,theme in ipairs({'boxer','racer','popstar'}) do local items={};for i,frame in ipairs({0,45,96,120,156,210,240}) do table.insert(items,{theme..'_'..string.format('%04d',frame),((i-1)%2)*1024,math.floor((i-1)/2)*1024}) end;board(theme..'_beat_board',items,2048,4096) end
print('REVIEW_BOARDS_COMPLETE; exact native key pixels on a neutral canvas only; no drawing, retouch or anatomy changes')
