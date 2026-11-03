local root=assert(app.params.root);local out=root..'/evidence/verification_v3/roundtrip_raw';app.fs.makeAllDirectories(out)
local rows={};local function check(master,layer,file,ox,oy,w,h)
 local s=app.open(root..'/masters/'..master..'.aseprite');local found=nil;for _,l in ipairs(s.layers) do if l.name==layer then found=l end end;assert(found,'missing '..master..'/'..layer)
 local target=Image{fromFile=root..'/demo/art/'..file..'.png'};local im=Image(w or target.width,h or target.height,ColorMode.RGB);local c=found:cel(1);if c then im:drawImage(c.image,Point(c.position.x-(ox or 0),c.position.y-(oy or 0))) end
 local p=out..'/'..master..'__'..layer..'.png';im:saveAs(p);table.insert(rows,{master=master,layer=layer,source='demo/art/'..file..'.png',output='evidence/verification_v3/roundtrip_raw/'..master..'__'..layer..'.png'});s:close()
end
for _,theme in ipairs({'boxer','racer','popstar'}) do
 local m=theme=='boxer' and 'boxer_skin_v1' or theme..'_skin_bound_v3'
 for _,e in ipairs({{'body','body'},{'tail','tail'},{'headwear','head'}}) do check(m,e[1],theme..'_'..e[2]) end
end
for _,theme in ipairs({'original','ballet','magician','boxer','racer','popstar'}) do for _,layer in ipairs({'ActionBody','LeftUpper','LeftFore','LeftHand','RightUpper','RightFore','RightHand'}) do check(theme..'_action_parts_v1',layer,theme..'_'..layer) end end
for _,layer in ipairs({'LeftElbowCap','RightElbowCap'}) do check('shared_joint_caps',layer,layer) end
check('racer_hip_panel','racer_jacket_panel_Torso','racer_hip_panel')
check('popstar_grip','approved_hand_and_contact_sliver','popstar_grip')
local f=io.open(root..'/evidence/verification_v3/roundtrip_mapping.json','w');f:write(json.encode(rows));f:close();print('ROUNDTRIP_EXPORTS '..#rows)
