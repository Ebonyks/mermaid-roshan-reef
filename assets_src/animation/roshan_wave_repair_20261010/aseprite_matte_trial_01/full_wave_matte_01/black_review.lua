local root=app.params.root;local pc=app.pixelColor
app.fs.makeDirectory(root..'/native_on_black');app.fs.makeDirectory(root..'/sprite_on_black');app.fs.makeDirectory(root..'/reopen_check')
local board=Image(2048,1536,ColorMode.RGB);board:clear(pc.rgba(0,0,0,255))
local nativeTop=Image(3200,3600,ColorMode.RGB);nativeTop:clear(pc.rgba(0,0,0,255))
for n=0,40 do
 local im=Image{fromFile=root..string.format('/frames/%04d.png',n)}
 local bg=Image(im.width,im.height,ColorMode.RGB);bg:clear(pc.rgba(0,0,0,255));bg:drawImage(im)
 bg:saveAs(root..string.format('/sprite_on_black/%04d.png',n));board:drawImage(bg,Point((n%8)*256,math.floor(n/8)*256))
 local native=Image{fromFile=root..string.format('/native_rgba/%04d.png',n)}
 local nativeBg=Image(native.width,native.height,ColorMode.RGB);nativeBg:clear(pc.rgba(0,0,0,255));nativeBg:drawImage(native)
 if n==14 or n==26 or n==40 then nativeBg:saveAs(root..string.format('/native_on_black/%04d.png',n)) end
 local crop=Image(nativeBg,Rectangle(0,95,640,400));nativeTop:drawImage(crop,Point((n%5)*640,math.floor(n/5)*400))
end
board:saveAs(root..'/contact_256_on_black.png');nativeTop:saveAs(root..'/contact_native_upperbody_on_black.png')
local master=app.open(root..'/wave.aseprite')
for _,n in ipairs({0,40}) do
 local image=Image(master.width,master.height,ColorMode.RGB);image:drawSprite(master,n+1);image:saveAs(root..string.format('/reopen_check/%04d.png',n))
end
master:close()
