-- One complete-source-frame transformation inside Aseprite. No anatomy-based bypass.
local packet=app.params.packet;local root=app.params.root
local f=assert(io.open(packet..'/registration_plan.json','rb'))
local plan=json.decode(f:read('*a'));f:close()
local out=packet..'/frames';app.fs.makeDirectory(out)
local s=Sprite(576,832,ColorMode.RGB)
s.layers[1].name='Continuous whole-frame registration; anatomy review separate'
local function affine(im,scale,tx,ty)
 assert(im.bytesPerPixel==4 and im.rowStride==576*4,'Expected native RGBA bytes')
 local bytes=im.bytes
 local function sample(x,y)
  if x<0 or y<0 or x>=576 or y>=832 then return 238,238,238,255 end
  return string.byte(bytes,y*im.rowStride+x*4+1,y*im.rowStride+x*4+4)
 end
 local rows={}
 for y=0,831 do
  local row={}
  for x=0,575 do
   local sx=(x-tx)/scale;local sy=(y-ty)/scale
   local ix=math.floor(sx);local iy=math.floor(sy);local fx=sx-ix;local fy=sy-iy
   local r1,g1,b1,a1=sample(ix,iy);local r2,g2,b2,a2=sample(ix+1,iy)
   local r3,g3,b3,a3=sample(ix,iy+1);local r4,g4,b4,a4=sample(ix+1,iy+1)
   local function lerp(p1,p2,p3,p4)
    return math.floor(((p1*(1-fx)+p2*fx)*(1-fy)+(p3*(1-fx)+p4*fx)*fy)+.5)
   end
   row[#row+1]=string.char(lerp(r1,r2,r3,r4),lerp(g1,g2,g3,g4),lerp(b1,b2,b3,b4),lerp(a1,a2,a3,a4))
  end
  rows[#rows+1]=table.concat(row)
 end
 local frame=Image(576,832,ColorMode.RGB);frame.bytes=table.concat(rows);return frame
end
for k,row in ipairs(plan.frames) do
 assert(row.apply_registration==true and row.no_new_clipping==true,'All reliable frames must be processed')
 if k>1 then s:newFrame() end
 local frame
 if app.params.feedback_only=='true' and not row.raster_feedback then
  frame=Image{fromFile=out..string.format('/%04d.png',row.index)}
 else
  local im=Image{fromFile=root..'/'..row.source}
  frame=affine(im,row.uniform_scale,row.translation[1],row.translation[2])
 end
 s.cels[k].image=frame
 s.frames[k].duration=(math.floor(k*1000/24+.5)-math.floor((k-1)*1000/24+.5))/1000
 frame:saveAs(out..string.format('/%04d.png',row.index))
 local tag=s:newTag(k,k);tag.name=string.format('%s_%04d',row.anatomy_geometry_pass and 'REGISTERED_REVIEW' or 'REGISTERED_ANATOMY_FAIL',row.index)
 for name,xy in pairs(row.target_landmarks) do
  local slice=s:newSlice(Rectangle(math.floor(xy[1]+.5)-3,math.floor(xy[2]+.5)-3,7,7))
  slice.name=string.format('f%04d/%s',row.index,name);slice.pivot=Point(3,3)
  slice.data=json.encode{timeline_index=row.index,target=xy,registered=true,anatomy_geometry_pass=row.anatomy_geometry_pass,review_only=true}
 end
 print(string.format('REGISTERED %04d scale=%.9f anatomy=%s',row.index,row.uniform_scale,tostring(row.anatomy_geometry_pass)))
end
s:saveAs(packet..'/registered_review.aseprite');s:close()
print('All41 continuous-scale frames exported. Artwork acceptance remains separate.')
