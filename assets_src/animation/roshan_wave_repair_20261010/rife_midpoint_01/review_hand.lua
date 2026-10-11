local root=app.params.root
local focus=Image(240,360,ColorMode.RGB);focus:clear(app.pixelColor.rgba(245,245,245,255))
for row,pair in ipairs({{6,3},{14,12},{10,12}}) do
 for i=0,2 do
  local src=Image{fromFile=root..string.format('/take_01/pair_%04d_%04d/%04d.png',pair[1],pair[2],i)}
  local crop=Image(80,120,ColorMode.RGB);crop:drawImage(src,Point(-65,-35))
  focus:drawImage(crop,Point(i*80,(row-1)*120))
 end
end
focus:saveAs(root..'/hand_comparison_native_crop.png')
