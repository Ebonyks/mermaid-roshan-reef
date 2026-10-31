local root=app.params.root
for _,i in ipairs({3,6,10,12,14}) do
 local image=Image{fromFile=root..string.format('/inputs/native_rgba/%04d.png',i)}
 assert(image.width==256 and image.height==256,'Complete-cell dimensions changed')
 local bg=Image(256,256,ColorMode.RGB)
 bg:clear(app.pixelColor.rgba(245,245,245,255))
 bg:drawImage(image)
 bg:saveAs(root..string.format('/inputs/neutral_gray/%04d.png',i))
end
print('Five complete 256px input cels flattened once over RGB245 gray by Aseprite; no resized or isolated parts')
