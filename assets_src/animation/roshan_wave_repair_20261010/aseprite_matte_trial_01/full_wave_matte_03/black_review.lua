local root=app.params.root;local pc=app.pixelColor
app.fs.makeDirectory(root..'/native_on_black');app.fs.makeDirectory(root..'/sprite_on_black');app.fs.makeDirectory(root..'/reopen_check')
local board=Image(2048,1536,ColorMode.RGB);board:clear(pc.rgba(0,0,0,255))
local nativeTop=Image(3840,3600,ColorMode.RGB);nativeTop:clear(pc.rgba(0,0,0,255))
for n=0,40 do
 local im=Image{fromFile=root..string.format('/frames/%04d.png',n)}
 local bg=Image(im.width,im.height,ColorMode.RGB);bg:clear(pc.rgba(0,0,0,255));bg:drawImage(im)
 bg:saveAs(root..string.format('/sprite_on_black/%04d.png',n));board:drawImage(bg,Point((n%8)*256,math.floor(n/8)*256))
 local native=Image{fromFile=root..string.format('/native_rgba/%04d.png',n)}
 local nativeBg=Image(native.width,native.height,ColorMode.RGB);nativeBg:clear(pc.rgba(0,0,0,255));nativeBg:drawImage(native)
 nativeBg:saveAs(root..string.format('/native_on_black/%04d.png',n))
 for _,matte in ipairs({{'light',245,245,245},{'dark',20,26,34}}) do local composite=Image(native.width,native.height,ColorMode.RGB);composite:clear(pc.rgba(matte[2],matte[3],matte[4],255));composite:drawImage(native);composite:saveAs(root..'/native_on_'..matte[1]..string.format('/%04d.png',n)) end

 local crop=Image(nativeBg,Rectangle(0,95,768,400));nativeTop:drawImage(crop,Point((n%5)*768,math.floor(n/5)*400))
end
board:saveAs(root..'/contact_256_on_black.png');nativeTop:saveAs(root..'/contact_native_upperbody_on_black.png')
local master=app.open(root..'/wave.aseprite')
for _,n in ipairs({0,40}) do
 local image=Image(master.width,master.height,ColorMode.RGB);image:drawSprite(master,n+1);image:saveAs(root..string.format('/reopen_check/%04d.png',n))
end
master:close()

local nativeMaster=app.open(root..'/native_final_wave.aseprite')
for _,n in ipairs({0,40}) do local im=Image(nativeMaster.width,nativeMaster.height,ColorMode.RGB);im:drawSprite(nativeMaster,n+1);im:saveAs(root..string.format('/reopen_check/native_%04d.png',n)) end
nativeMaster:close()
