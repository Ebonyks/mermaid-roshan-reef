local root=app.params.root
local board=Image(768,768,ColorMode.RGB);board:clear(app.pixelColor.rgba(245,245,245,255))
for row,pair in ipairs({{6,3},{14,12},{10,12}}) do
 for i=0,2 do
  local src=Image{fromFile=root..string.format('/take_01/pair_%04d_%04d/%04d.png',pair[1],pair[2],i)}
  assert(src.width==256 and src.height==256)
  board:drawImage(src,Point(i*256,(row-1)*256))
 end
end
board:saveAs(root..'/contact_sheet.png')
