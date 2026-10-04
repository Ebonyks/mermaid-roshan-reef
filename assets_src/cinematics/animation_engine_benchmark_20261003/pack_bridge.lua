local directory=app.params.directory
local output=app.params.output
local count=tonumber(app.params.count)
local width=tonumber(app.params.width) or 896
local height=tonumber(app.params.height) or 512
local canvasWidth=tonumber(app.params.canvas_width) or 2048
local canvasHeight=tonumber(app.params.canvas_height) or 2048
for page=0,math.floor((count-1)/8) do
 local sheet=Image(canvasWidth,canvasHeight,ColorMode.RGB)
 sheet:clear(app.pixelColor.rgba(0,0,0,0))
 for cell=0,7 do
  local index=page*8+cell+1
  if index<=count then
   local image=Image{fromFile=directory..string.format('/clean_%04d.png',index)}
   sheet:drawImage(image,Point((cell%2)*width,math.floor(cell/2)*height))
  end
 end
 sheet:saveAs(output..string.format('/atlas_%02d.png',page))
end
