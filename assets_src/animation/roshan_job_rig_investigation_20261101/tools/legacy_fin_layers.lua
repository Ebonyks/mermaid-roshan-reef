local root=assert(app.params.root)
local source=Image{fromFile=root.."/demo/art/anatomy.png"}
local without=Image(source)
local new_with_fin=Image{fromFile=root.."/demo/art/investigation_anatomy.png"}
for y=590,1023 do for x=0,1023 do
 without:drawPixel(x,y,0)
 new_with_fin:drawPixel(x,y,source:getPixel(x,y))
end end
without:saveAs(root.."/demo/art/seed_anatomy_no_fin.png")
new_with_fin:saveAs(root.."/demo/art/new_anatomy_legacy_fin.png")
print("CONDITIONAL_LEGACY_FIN_LAYERS_COMPLETE")
