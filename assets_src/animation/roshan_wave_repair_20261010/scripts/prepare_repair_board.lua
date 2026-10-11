local root=app.params.root;local native=root..'/native640_01/take_01/native_frames/'
local indices={0,8,12,16,22,26,29,32,36}
local board=Image(1344,1344,ColorMode.RGB)
board:clear(app.pixelColor.rgba(245,245,245,255))
for i,n in ipairs(indices) do
 local image=Image{fromFile=native..string.format('%04d.png',n)}
 image:resize{width=320,height=448,method='bilinear'}
 board:drawImage(image,Point(((i-1)%3)*448+64,math.floor((i-1)/3)*448))
end
app.fs.makeDirectory(root..'/whole_key_repair_01')
board:saveAs(root..'/whole_key_repair_01/edit_target.png')
