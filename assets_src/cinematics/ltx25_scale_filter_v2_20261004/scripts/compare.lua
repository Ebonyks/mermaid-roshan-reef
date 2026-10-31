local root=app.params.root;local packet=app.params.packet
local old=root..'/assets_src/cinematics/ltx25_8gb_wave_20261004'
local output=app.params.output;app.fs.makeDirectory(output)
for i=0,40 do
 local result=Image(1728,832,ColorMode.RGB)
 result:drawImage(Image{fromFile=old..string.format('/results/scale_registered/refined_frames/%04d.png',i)},Point(0,0))
 result:drawImage(Image{fromFile=old..string.format('/scale_continuity/decoded_filtered/%04d.png',i)},Point(576,0))
 result:drawImage(Image{fromFile=packet..string.format('/frames/%04d.png',i)},Point(1152,0))
 result:saveAs(output..string.format('/%04d.png',i))
end
print('41 native comparisons: raw | v1 | continuous v2. No temporal substitutions.')
