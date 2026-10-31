local root=app.params.root;local packet=app.params.packet;local compare=app.params.compare
app.fs.makeDirectory(compare)
local old=root..'/assets_src/cinematics/ltx25_8gb_wave_20261004/results/scale_registered/refined_frames'
local s=Sprite(576,832,ColorMode.RGB);s.layers[1].name='Experimental two-step diffusion decode; entire figure unchanged latent'
for i=0,40 do
 if i>0 then s:newFrame() end
 local im=Image{fromFile=packet..string.format('/decoder_2_frames/%04d.png',i)}
 s.cels[i+1].image=im;s.frames[i+1].duration=(math.floor((i+1)*1000/24+.5)-math.floor(i*1000/24+.5))/1000
 local pair=Image(1152,832,ColorMode.RGB)
 pair:drawImage(Image{fromFile=old..string.format('/%04d.png',i)},Point(0,0))
 pair:drawImage(im,Point(576,0));pair:saveAs(compare..string.format('/%04d.png',i))
end
s:saveAs(packet..'/decoder_2_review.aseprite');s:close()
print('Complete41-frame two-step master and native1-vs2 comparison exported by Aseprite.')
