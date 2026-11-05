local root=assert(app.params.root);local out=root..'/evidence/editable_props';local rows={}
local function save(name,files)
 local first=Image{fromFile=root..'/demo/art/'..files[1]..'.png'};local s=Sprite(first.width,first.height,ColorMode.RGB)
 for i,n in ipairs(files) do local l=i==1 and s.layers[1] or s:newLayer();l.name=n;local im=Image{fromFile=root..'/demo/art/'..n..'.png'};s:newCel(l,1,im,Point(0,0)) end
 s:saveAs(out..'/'..name..'.aseprite');s:close()
 local reopened=app.open(out..'/'..name..'.aseprite');for _,l in ipairs(reopened.layers) do local im=Image(first.width,first.height,ColorMode.RGB);local c=l:cel(1);im:drawImage(c.image,c.position);local p=root..'/evidence/verification_v3/roundtrip_raw/prop__'..l.name..'.png';im:saveAs(p);table.insert(rows,{master='evidence/editable_props/'..name..'.aseprite',layer=l.name,source='demo/art/'..l.name..'.png',output='evidence/verification_v3/roundtrip_raw/prop__'..l.name..'.png'}) end;reopened:close()
end
save('glove_surface_keys',{'glove_guard','glove_jab','glove_palm'});save('complete_wheel',{'wheel'});save('painted_grips',{'racer_grip_left','racer_grip_right','popstar_grip'});save('supported_microphone',{'mic_lower','mic_upper'});save('focus_mitt',{'focus_mitt'})
local f=io.open(out..'/mapping.json','w');f:write(json.encode({scope='Archival lossless pixel packaging only, no new painting, animation or frozen input edits. View layers are separate static keys, not action timings.',rows=rows}));f:close();print('ARCHIVE_PROP_MASTERS_COMPLETE '..#rows)
