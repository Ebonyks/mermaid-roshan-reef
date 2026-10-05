local root=app.params.packet
local take=app.params.take or 'figure_wide_root'
local count=take=='figure_wide_slow' and 81 or 41
local factor=count==81 and 2 or 1
local s=Sprite(896,512,ColorMode.RGB);s.layers[1].name='Complete native LTX figure frames; visible, unmasked'
local native=s.layers[1]
local reference=s:newLayer();reference.name='Approved full-figure source poses (hidden reference only)';reference.isVisible=false
for i=0,count-1 do
 if i>0 then s:newFrame() end
 local raw=Image{fromFile=root..string.format('/results/'..take..'/native_frames/%04d.png',i)}
 s:newCel(native,i+1,raw,Point(0,0));s.frames[i+1].duration=(math.floor((i+1)*1000/24+0.5)-math.floor(i*1000/24+0.5))/1000
end
for _,pair in ipairs({{1,0},{8,1},{18,2},{28,3},{37,0},{41,0}}) do
 local im=Image{fromFile=root..string.format('/inputs/figure_key_%02d.png',pair[2])};s:newCel(reference,(pair[1]-1)*factor+1,im,Point(0,0))
end
for _,x in ipairs({{1,8,'whole_figure_raise_to_shoulder'},{9,18,'whole_figure_greeting'},{19,28,'whole_figure_lower'},{29,41,'whole_figure_settle'}}) do local tag=s:newTag((x[1]-1)*factor+1,math.min(count,x[2]*factor));tag.name=x[3] end
local slice=s:newSlice(Rectangle(0,0,896,512));slice.name='STUDY_waist_root_landmark_not_pixel_freeze';slice.pivot=Point(461,280)
s:saveAs(root..'/results/'..take..'/wave_full_figure.aseprite');s:close()
