local p=app.params.base
local s=Sprite(400,1152,ColorMode.RGB)
local names={'crown','upper_boughs','middle_boughs','lower_boughs','trunk_and_roots'}
local layers={}
for j,n in ipairs(names) do local l=j==1 and s.layers[1] or s:newLayer();l.name=n;layers[j]=l end
for k=0,11 do
 if k>0 then s:newEmptyFrame() end
 s.frames[k+1].duration=.2
 for j,n in ipairs(names) do local t=app.open(p..'/'..n..string.format('-%02d.png',k));local im=Image(400,1152,ColorMode.RGB);local c=t.cels[1];im:drawImage(c.image,c.position);t:close();s:newCel(layers[j],k+1,im,Point(0,0)) end
end
app.activeSprite=s;s:newTag(1,12).name='whole_tree_breeze_trial';s:saveAs(p..'/whole-tree-12-cels.aseprite');s:close()
