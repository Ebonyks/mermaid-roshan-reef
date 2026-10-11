local root=app.params.root;local pc=app.pixelColor
local paths={root..'/approved_K0.png',root..'/tinted_inside_edge_pilot_01/frames/0014.png',root..'/dim_closed_edge_pilot_01/frames/0014.png'}
for _,m in ipairs({{'black',0,0,0},{'light',245,245,245}}) do
 local board=Image(1536,512,ColorMode.RGB);board:clear(pc.rgba(m[2],m[3],m[4],255))
 for n,path in ipairs(paths) do local im=Image{fromFile=path};im:resize{width=512,height=512,method='bilinear'};board:drawImage(im,Point((n-1)*512,0)) end
 board:saveAs(root..'/k0_inside_dim_comparison_512_on_'..m[1]..'.png')
end
