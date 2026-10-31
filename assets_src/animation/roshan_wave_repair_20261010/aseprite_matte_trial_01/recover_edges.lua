-- Local whole-cel edge unmatting pilot. No part segmentation, warping or pasted anatomy.
local root=app.params.root
local pc=app.pixelColor
for _,dir in ipairs({'native_rgba','baseline_native_rgba','sprite_rgba','baseline_sprite_rgba','native_on_light','native_on_dark','sprite_on_light','sprite_on_dark'}) do app.fs.makeDirectory(root..'/'..dir) end
local results={}
local sprite=Sprite(256,256,ColorMode.RGB);sprite.layers[1].name='One complete cel with boundary-only alpha recovery'
local lightBoard=Image(768,256,ColorMode.RGB);lightBoard:clear(pc.rgba(245,245,245,255))
local darkBoard=Image(768,256,ColorMode.RGB);darkBoard:clear(pc.rgba(20,26,34,255))
local baseDarkBoard=Image(768,256,ColorMode.RGB);baseDarkBoard:clear(pc.rgba(20,26,34,255))
local function median(a) table.sort(a);return a[math.floor((#a+1)/2)] end
local function composite(im,r,g,b) local out=Image(im.width,im.height,ColorMode.RGB);out:clear(pc.rgba(r,g,b,255));out:drawImage(im);return out end
for frame,n in ipairs({14,26,40}) do
 local original=Image{fromFile=root..string.format('/sources/%04d.png',n)};local w,h=original.width,original.height
 local rs,gs,bs,eligible,visited,queue={},{},{},{},{},{}
 for y=0,h-1 do for x=0,w-1 do
  local k=y*w+x+1;local c=original:getPixel(x,y);local r,g,b=pc.rgbaR(c),pc.rgbaG(c),pc.rgbaB(c)
  rs[k],gs[k],bs[k]=r,g,b
  if math.max(r,g,b)-math.min(r,g,b)<=10 and math.min(r,g,b)>=205 then eligible[k]=true end
 end end
 local function push(k) if eligible[k] and not visited[k] then visited[k]=true;queue[#queue+1]=k end end
 for x=0,w-1 do push(x+1);push((h-1)*w+x+1) end
 for y=0,h-1 do push(y*w+1);push(y*w+w) end
 local q=1
 while q<=#queue do
  local k=queue[q];q=q+1;local x=(k-1)%w;local y=math.floor((k-1)/w)
  if x>0 then push(k-1) end;if x<w-1 then push(k+1) end;if y>0 then push(k-w) end;if y<h-1 then push(k+w) end
 end
 -- Distance from connected background and from retained figure; cap both at2px for modification.
 local depth,nearForeground={},{},{}
 for y=0,h-1 do for x=0,w-1 do
  local k=y*w+x+1
  if not visited[k] then
   for dy=-2,2 do for dx=-2,2 do
    local xx,yy=x+dx,y+dy
    if xx>=0 and xx<w and yy>=0 and yy<h and visited[yy*w+xx+1] then
     local d=math.max(math.abs(dx),math.abs(dy));if not depth[k] or d<depth[k] then depth[k]=d end
    end
   end end
  else
   for dy=-2,2 do for dx=-2,2 do
    local xx,yy=x+dx,y+dy
    if xx>=0 and xx<w and yy>=0 and yy<h and not visited[yy*w+xx+1] then
     local d=math.max(math.abs(dx),math.abs(dy));if not nearForeground[k] or d<nearForeground[k] then nearForeground[k]=d end
    end
   end end
  end
 end end
 local baseline=Image(original);local cleaned=Image(original)
 for _,k in ipairs(queue) do local x,y=(k-1)%w,math.floor((k-1)/w);baseline:drawPixel(x,y,0);cleaned:drawPixel(x,y,0) end
 local stats={frame_index=n,native_width=w,native_height=h,connected_outer_pixels_removed=#queue,retained_closed_neutral_pixels=0,recovered_removed_edge_pixels=0,adjusted_retained_edge_pixels=0,fit_rejected_or_unchanged_edge_pixels=0,alpha_min=255,alpha_max=0,boundary_radius_px=2,foreground_candidate_radius_px=3}
 for k in pairs(eligible) do if not visited[k] then stats.retained_closed_neutral_pixels=stats.retained_closed_neutral_pixels+1 end end
 for y=1,h-2 do for x=1,w-2 do
  local k=y*w+x+1
  if depth[k] or nearForeground[k] then
   -- A local high-confidence neutral-field median handles the measured236..238 background gradient.
   local brs,bgs,bbs={},{},{}
   for dy=-4,4 do for dx=-4,4 do
    local xx,yy=x+dx,y+dy
    if xx>=0 and xx<w and yy>=0 and yy<h then
     local z=yy*w+xx+1
     if visited[z] and math.min(rs[z],gs[z],bs[z])>=232 and math.max(rs[z],gs[z],bs[z])-math.min(rs[z],gs[z],bs[z])<=4 then
      brs[#brs+1]=rs[z];bgs[#bgs+1]=gs[z];bbs[#bbs+1]=bs[z]
     end
    end
   end end
   local br,bg,bb=237,237,237
   if #brs>=3 then br,bg,bb=median(brs),median(bgs),median(bbs) end
   local cr,cg,cb=rs[k]-br,gs[k]-bg,bs[k]-bb;local cden=cr*cr+cg*cg+cb*cb
   local best=nil;local bestScore=1e9
   for dy=-3,3 do for dx=-3,3 do
    local ds=dx*dx+dy*dy;local xx,yy=x+dx,y+dy
    if ds>0 and ds<=9 and xx>=0 and xx<w and yy>=0 and yy<h then
     local z=yy*w+xx+1
     if not visited[z] then
      local fr,fg,fb=rs[z]-br,gs[z]-bg,bs[z]-bb;local den=fr*fr+fg*fg+fb*fb
      -- F is an actual stronger-painted native neighbor, never a guessed palette or external patch.
      if den>=45*45 and den>cden+15*15 then
       local a=(cr*fr+cg*fg+cb*fb)/den
       if a>=0.025 and a<=0.985 then
        local er,eg,eb=cr-a*fr,cg-a*fg,cb-a*fb;local error=math.sqrt(er*er+eg*eg+eb*eb)
        if error<=5 then
         local score=error+math.sqrt(ds)*0.7+(depth[z] and 0.4 or 0)
         if score<bestScore then bestScore=score;best={alpha=a,r=rs[z],g=gs[z],b=bs[z],error=error,distance=math.sqrt(ds)} end
        end
       end
      end
     end
    end
   end end
   if best then
    local alpha=math.floor(best.alpha*255+0.5)
    cleaned:drawPixel(x,y,pc.rgba(best.r,best.g,best.b,alpha))
    if visited[k] then stats.recovered_removed_edge_pixels=stats.recovered_removed_edge_pixels+1 else stats.adjusted_retained_edge_pixels=stats.adjusted_retained_edge_pixels+1 end
    stats.alpha_min=math.min(stats.alpha_min,alpha);stats.alpha_max=math.max(stats.alpha_max,alpha)
   else stats.fit_rejected_or_unchanged_edge_pixels=stats.fit_rejected_or_unchanged_edge_pixels+1 end
  end
 end end
 baseline:saveAs(root..string.format('/baseline_native_rgba/%04d.png',n));cleaned:saveAs(root..string.format('/native_rgba/%04d.png',n))
 composite(cleaned,245,245,245):saveAs(root..string.format('/native_on_light/%04d.png',n));composite(cleaned,20,26,34):saveAs(root..string.format('/native_on_dark/%04d.png',n))
 -- One uniform whole-frame resample and translation matches the root's established source-study layout.
 local small=Image(cleaned);small:resize{width=200,height=280,method='bilinear'}
 local canvas=Image(256,256,ColorMode.RGB);canvas:drawImage(small,Point(55,-10));canvas:saveAs(root..string.format('/sprite_rgba/%04d.png',n))
 local baseSmall=Image(baseline);baseSmall:resize{width=200,height=280,method='bilinear'}
 local baseCanvas=Image(256,256,ColorMode.RGB);baseCanvas:drawImage(baseSmall,Point(55,-10));baseCanvas:saveAs(root..string.format('/baseline_sprite_rgba/%04d.png',n))
 local light=composite(canvas,245,245,245);local dark=composite(canvas,20,26,34)
 light:saveAs(root..string.format('/sprite_on_light/%04d.png',n));dark:saveAs(root..string.format('/sprite_on_dark/%04d.png',n))
 lightBoard:drawImage(light,Point((frame-1)*256,0));darkBoard:drawImage(dark,Point((frame-1)*256,0));baseDarkBoard:drawImage(composite(baseCanvas,20,26,34),Point((frame-1)*256,0))
 if frame>1 then sprite:newFrame() end;sprite.cels[frame].image=canvas;sprite.frames[frame].duration=1/24
 results[#results+1]=stats
end
sprite:saveAs(root..'/matte_trial.aseprite');sprite:close()
lightBoard:saveAs(root..'/contact_256_on_light.png');darkBoard:saveAs(root..'/contact_256_on_dark.png');baseDarkBoard:saveAs(root..'/baseline_contact_256_on_dark.png')
local f=io.open(root..'/pixel_processing_stats.json','w');f:write(json.encode({schema='reef.aseprite-boundary-alpha-pilot.v1',frames=results,parameters={boundary_radius=2,foreground_radius=3,max_rgb_fit_error_l2=5,alpha_min=0.025,alpha_max=0.985,foreground_bg_separation_min_l2=45,bg_local_median_radius=4},acceptance='UNREVIEWED_SOURCE_STUDY_ONLY'}));f:close()

