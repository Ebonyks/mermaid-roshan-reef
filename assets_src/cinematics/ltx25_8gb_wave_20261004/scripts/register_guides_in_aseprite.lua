local packet=app.params.packet
local function read(path) local f=assert(io.open(path,'rb'));local v=json.decode(f:read('*a'));f:close();return v end
local plan=read(packet..'/scale_continuity/registration_plan.json')
local replacement=read(packet..'/scale_continuity/redraw_registration_diagnostic.json')
assert(replacement.pass,'New whole-figure key fails multi-anchor fit; no export')
local sprite=Sprite(576,832,ColorMode.RGB)
sprite.layers[1].name='Registered complete figure; all body parts preserved'
app.fs.makeDirectory(packet..'/scale_continuity/registered_guides')
for k,row in ipairs(plan.guides) do
 local source,fit
 if row.index==22 then source=packet..'/scale_continuity/key22_redraw_attempt01_canvas.png';fit=replacement
 else assert(row.pass,'Original pose failed preflight');source=app.params.repo..'/'..row.source;fit=row end
 if k>1 then sprite:newFrame() end
 local im=Image{fromFile=source}
 assert(fit.scaled_canvas[1]*832==fit.scaled_canvas[2]*576,'Nonuniform scaling rejected')
 if fit.scaled_canvas[1]~=576 then im:resize{width=fit.scaled_canvas[1],height=fit.scaled_canvas[2],method='bilinear'} end
 local canvas=Image(576,832,ColorMode.RGB);canvas:clear(Color{r=238,g=238,b=238,a=255})
 local placement=fit.raster_corrected_placement or fit.placement
 canvas:drawImage(im,Point(placement[1],placement[2]))
 sprite.cels[k].image=canvas
 sprite.frames[k].duration=((plan.guides[k+1] and plan.guides[k+1].index or 41)-row.index)/24
 canvas:saveAs(packet..string.format('/scale_continuity/registered_guides/guide_%04d.png',row.index))
 for _,name in ipairs(plan.anchor_names) do
  local xy=row.target_landmarks[name];local slice=sprite:newSlice(Rectangle(math.floor(xy[1]+.5)-3,math.floor(xy[2]+.5)-3,7,7))
  slice.name=string.format('f%04d/%s',row.index,name);slice.pivot=Point(3,3)
  slice.data=json.encode{timeline_index=row.index,anchor_name=name,target=xy,whole_figure_scale=fit.raster_uniform_scale,translation=placement,review_status='SOURCE_ONLY'}
 end
 local tag=sprite:newTag(k,k);tag.name=string.format('REGISTERED_KEY_%04d',row.index)
end
sprite:saveAs(packet..'/scale_continuity/registered_guides.aseprite')
sprite:close()
print('Eight whole-figure guides registered in Aseprite; five anchors per pose, exact aspect ratio.')
