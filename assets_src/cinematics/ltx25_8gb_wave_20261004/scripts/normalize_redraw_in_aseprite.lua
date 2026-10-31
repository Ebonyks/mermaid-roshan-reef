local root=app.params.packet
local image=Image{fromFile=root..'/scale_continuity/key22_redraw_attempt01_native.png'}
local h=math.floor(image.height*576/image.width+0.5)
image:resize{width=576,height=h,method='bilinear'}
local canvas=Image(576,832,ColorMode.RGB);canvas:clear(Color{r=238,g=238,b=238,a=255});canvas:drawImage(image,Point(0,0));canvas:saveAs(root..'/scale_continuity/key22_redraw_attempt01_canvas.png')
