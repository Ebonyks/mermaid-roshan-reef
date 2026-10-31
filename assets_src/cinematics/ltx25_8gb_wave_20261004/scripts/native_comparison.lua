local root=app.params.root
local paths={'base_two_pass','temporal_retake','anti_blur_nag','temporal_48fps'}
local sprite=Sprite(2304,832,ColorMode.RGB)
sprite.layers[1].name='Native1to1 base | retake | NAG |48fps at matched action times'
app.fs.makeDirectory(root..'/comparison/frames')
for i=0,40 do
 if i>0 then sprite:newFrame() end
 local canvas=Image(2304,832,ColorMode.RGB)
 for column,take in ipairs(paths) do
  local index=take=='temporal_48fps' and i*2 or i
  canvas:drawImage(Image{fromFile=root..'/results/'..take..'/refined_frames/'..string.format('%04d.png',index)},Point((column-1)*576,0))
 end
 sprite.cels[i+1].image=canvas
 sprite.frames[i+1].duration=(math.floor((i+1)*1000/24+.5)-math.floor(i*1000/24+.5))/1000
 canvas:saveAs(root..'/comparison/frames/'..string.format('%04d.png',i))
end
sprite:saveAs(root..'/comparison/native_four_takes.aseprite')
sprite:close()
