local p=app.params.packet
local s=Sprite(1728,832,ColorMode.RGB);s.layers[1].name='Native1to1: original base, registered-input take, Aseprite filtered review'
app.fs.makeDirectory(p..'/scale_continuity/comparison_frames')
for i=0,40 do
 if i>0 then s:newFrame() end
 local frame=Image(1728,832,ColorMode.RGB)
 frame:drawImage(Image{fromFile=p..string.format('/results/base_two_pass/refined_frames/%04d.png',i)},Point(0,0))
 frame:drawImage(Image{fromFile=p..string.format('/results/scale_registered/refined_frames/%04d.png',i)},Point(576,0))
 frame:drawImage(Image{fromFile=p..string.format('/scale_continuity/decoded_filtered/%04d.png',i)},Point(1152,0))
 s.cels[i+1].image=frame;s.frames[i+1].duration=(math.floor((i+1)*1000/24+.5)-math.floor(i*1000/24+.5))/1000
 frame:saveAs(p..string.format('/scale_continuity/comparison_frames/%04d.png',i))
end
s:saveAs(p..'/scale_continuity/scale_comparison.aseprite');s:close()
