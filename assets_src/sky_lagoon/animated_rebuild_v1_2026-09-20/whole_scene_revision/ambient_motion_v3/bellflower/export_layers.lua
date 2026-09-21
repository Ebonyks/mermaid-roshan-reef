local s=app.open(app.params.base..'/bellflower-whole-leaf.aseprite')
for i,l in ipairs(s.layers) do
 for f=1,8 do local im=Image(s.spec);local c=l:cel(f);im:drawImage(c.image,c.position);im:saveAs(app.params.base..string.format('/layer-%02d-pose-%02d.png',i-1,f-1)) end
 print(l.name)
end
s:close()
