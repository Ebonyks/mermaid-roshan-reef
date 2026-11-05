local root="C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/snowfield_20261103"
local runtime="C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets/mg"
local source=Image{fromFile=root.."/snowfield_master_native.png"}
local names={"snowfield_painted_00.png","snowfield_painted_01.png","snowfield_painted_10.png","snowfield_painted_11.png"}
for i,name in ipairs(names) do
 local x=((i-1)%2)*1024
 local y=math.floor((i-1)/2)*1024
 local s=Sprite(1024,1024,ColorMode.RGB)
 s.cels[1].image:drawImage(source,Point(-x,-y))
 s:saveCopyAs(runtime.."/"..name)
 s:close()
end
local s=app.open(root.."/masters/snowfield_native_2048.aseprite")
s:saveCopyAs("C:/Users/Peter/AppData/Local/Temp/reef-flat-vector-snowfield-native-20261103/master_roundtrip.png")
s:close()
