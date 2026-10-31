-- Local whole-cel wide-boundary edge unmatting pilot. No part segmentation, warping or pasted anatomy.
local root=app.params.root
local source=app.params.source or (root..'/sources')
local f=io.open(root..'/source_and_seed_plan.json','r');local plan=json.decode(f:read('*a'));f:close()
local selected={};local seedRows={};for _,row in ipairs(plan.sources) do selected[#selected+1]=row.index;seedRows[row.index]=row end
local approvedK0=Image{fromFile=root..'/approved_K0.png'}
local columns=8;local rows=math.ceil(#selected/columns)
local function tick(i) return math.floor((i*1000+12)/24) end
local nativeMaster=nil
local pc=app.pixelColor
for _,dir in ipairs({'native_rgba','upstream_endpoint_matte','baseline_native_rgba','frames','baseline_sprite_rgba','native_on_light','native_on_dark','sprite_on_light','sprite_on_dark'}) do app.fs.makeDirectory(root..'/'..dir) end
local results={}
local sprite=Sprite(256,256,ColorMode.RGB);sprite.layers[1].name='One complete cel with boundary-only alpha recovery'
local lightBoard=Image(256*columns,256*rows,ColorMode.RGB);lightBoard:clear(pc.rgba(245,245,245,255))
local darkBoard=Image(256*columns,256*rows,ColorMode.RGB);darkBoard:clear(pc.rgba(20,26,34,255))
local baseDarkBoard=Image(256*columns,256*rows,ColorMode.RGB);baseDarkBoard:clear(pc.rgba(20,26,34,255))
local function median(a) table.sort(a);return a[math.floor((#a+1)/2)] end
local function composite(im,r,g,b) local out=Image(im.width,im.height,ColorMode.RGB);out:clear(pc.rgba(r,g,b,255));out:drawImage(im);return out end
for frame,n in ipairs(selected) do
 local original=Image{fromFile=source..string.format('/%04d.png',n)};local w,h=original.width,original.height
 local rs,gs,bs,eligible,visited,queue={},{},{},{},{},{}
 for y=0,h-1 do for x=0,w-1 do
  local k=y*w+x+1;local c=original:getPixel(x,y);local r,g,b=pc.rgbaR(c),pc.rgbaG(c),pc.rgbaB(c)
  rs[k],gs[k],bs[k]=r,g,b
  if math.max(r,g,b)-math.min(r,g,b)<=22 and math.min(r,g,b)>=170 then eligible[k]=true end
 end end
 local function push(k) if eligible[k] and not visited[k] then visited[k]=true;queue[#queue+1]=k end end
 for x=0,w-1 do push(x+1);push((h-1)*w+x+1) end
 for y=0,h-1 do push(y*w+1);push(y*w+w) end
 -- Bound source-specific hair background components only, all previously model-reviewed.
 assert(seedRows[n].hair_gap_component.review_status=='MODEL_REVIEWED_TRUE_BACKGROUND','Review every actual background-hole crop before applying');local manualSeeds={seedRows[n].hair_gap_component.seed}
 for _,item in ipairs(seedRows[n].left_curl_gap_components) do manualSeeds[#manualSeeds+1]=item.seed end
 for _,manualSeed in ipairs(manualSeeds) do local seed=manualSeed[2]*w+manualSeed[1]+1;assert(eligible[seed],'Reviewed background seed changed');push(seed) end
 local q=1
 while q<=#queue do
  local k=queue[q];q=q+1;local x=(k-1)%w;local y=math.floor((k-1)/w)
  if x>0 then push(k-1) end;if x<w-1 then push(k+1) end;if y>0 then push(k-w) end;if y<h-1 then push(k+w) end
 end
 -- Keep the original strict closed pale cells as an additional pilot protection mask.
 local strictEligible,strictVisited,strictQueue={},{},{}
 for k=1,w*h do if math.max(rs[k],gs[k],bs[k])-math.min(rs[k],gs[k],bs[k])<=10 and math.min(rs[k],gs[k],bs[k])>=205 then strictEligible[k]=true end end
 local function strictPush(k) if strictEligible[k] and not strictVisited[k] then strictVisited[k]=true;strictQueue[#strictQueue+1]=k end end
 for x=0,w-1 do strictPush(x+1);strictPush((h-1)*w+x+1) end
 for y=0,h-1 do strictPush(y*w+1);strictPush(y*w+w) end
 for _,seed in ipairs(manualSeeds) do strictPush(seed[2]*w+seed[1]+1) end
 local sq=1;while sq<=#strictQueue do local k=strictQueue[sq];sq=sq+1;local x=(k-1)%w;local y=math.floor((k-1)/w);if x>0 then strictPush(k-1) end;if x<w-1 then strictPush(k+1) end;if y>0 then strictPush(k-w) end;if y<h-1 then strictPush(k+w) end end
 local originalClosed={};for k in pairs(strictEligible) do if not strictVisited[k] then originalClosed[k]=true end end
 -- Broader field classification must not consume any original closed paint cell.
 local filteredQueue={};for _,k in ipairs(queue) do if originalClosed[k] then visited[k]=nil else filteredQueue[#filteredQueue+1]=k end end;queue=filteredQueue
 -- Distance from connected background and from retained figure; cap both at4px for modification.
 local depth,nearForeground={},{},{}
 for y=0,h-1 do for x=0,w-1 do
  local k=y*w+x+1
  if not visited[k] then
   for dy=-4,4 do for dx=-4,4 do
    local xx,yy=x+dx,y+dy
    if xx>=0 and xx<w and yy>=0 and yy<h and visited[yy*w+xx+1] then
     local d=math.max(math.abs(dx),math.abs(dy));if not depth[k] or d<depth[k] then depth[k]=d end
    end
   end end
  else
   for dy=-4,4 do for dx=-4,4 do
    local xx,yy=x+dx,y+dy
    if xx>=0 and xx<w and yy>=0 and yy<h and not visited[yy*w+xx+1] then
     local d=math.max(math.abs(dx),math.abs(dy));if not nearForeground[k] or d<nearForeground[k] then nearForeground[k]=d end
    end
   end end
  end
 end end
 local baseline=Image(original);local cleaned=Image(original)
 for _,k in ipairs(queue) do local x,y=(k-1)%w,math.floor((k-1)/w);baseline:drawPixel(x,y,0);cleaned:drawPixel(x,y,0) end
 local stats={reviewed_background_seeds=manualSeeds,frame_index=n,native_width=w,native_height=h,connected_outer_pixels_removed=#queue,retained_closed_neutral_pixels=0,recovered_removed_edge_pixels=0,adjusted_retained_edge_pixels=0,fit_rejected_or_unchanged_edge_pixels=0,alpha_min=255,alpha_max=0,boundary_radius_px=4,foreground_candidate_radius_px=6}
 for k in pairs(eligible) do if not visited[k] then stats.retained_closed_neutral_pixels=stats.retained_closed_neutral_pixels+1 end end
 for y=1,h-2 do for x=1,w-2 do
  local k=y*w+x+1
  if depth[k] and not visited[k] and not originalClosed[k] then
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
   if not eligible[k] or (rs[k]<=br-4 and gs[k]<=bg-4 and bs[k]<=bb-4) then
   local cr,cg,cb=rs[k]-br,gs[k]-bg,bs[k]-bb;local cden=cr*cr+cg*cg+cb*cb
   local best=nil;local bestScore=1e9
   for dy=-6,6 do for dx=-6,6 do
    local ds=dx*dx+dy*dy;local xx,yy=x+dx,y+dy
    if ds>0 and ds<=36 and xx>=0 and xx<w and yy>=0 and yy<h then
     local z=yy*w+xx+1
     if not visited[z] and (not depth[z] or depth[z]>=2) and (math.max(rs[z],gs[z],bs[z])-math.min(rs[z],gs[z],bs[z])>=20 or math.min(rs[z],gs[z],bs[z])<=140) then
      local fr,fg,fb=rs[z]-br,gs[z]-bg,bs[z]-bb;local den=fr*fr+fg*fg+fb*fb
      -- F is an actual stronger-painted native neighbor, never a guessed palette or external patch.
      if den>=45*45 and den>cden+15*15 then
       local a=(cr*fr+cg*fg+cb*fb)/den
       if a>=0.04 and a<=0.985 then
        local er,eg,eb=cr-a*fr,cg-a*fg,cb-a*fb;local error=math.sqrt(er*er+eg*eg+eb*eb)
        if error<=(eligible[k] and 10 or ((math.max(rs[k],gs[k],bs[k])-math.min(rs[k],gs[k],bs[k])<=15) and 25 or 10)) then
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
   end -- dim-only closed edge fit guard
  end
 end end
 if n==0 or n==40 then
  cleaned:saveAs(root..string.format('/upstream_endpoint_matte/%04d.png',n))
  local endpoint=Image(approvedK0);endpoint:resize{width=819,height=819,method='bilinear'}
  local nativeEndpoint=Image(w,h,ColorMode.RGB);nativeEndpoint:drawImage(endpoint,Point(-48,32));cleaned=nativeEndpoint
  stats.final_native_endpoint_replacement={source='approved_K0.png',source_dimensions={256,256},whole_resized_dimensions={819,819},uniform_raster_scale=819/256,translation={-48,32},ideal_inverse_mapping_scale=3.2,ideal_inverse_mapping_translation={-48,32},upstream_matte_preserved=true}
 end
 cleaned:saveAs(root..string.format('/native_rgba/%04d.png',n))
 if not nativeMaster then nativeMaster=Sprite(w,h,ColorMode.RGB);nativeMaster.layers[1].name='Complete native RGBA cel with local boundary cleanup' else nativeMaster:newFrame() end
 nativeMaster.cels[frame].image=Image(cleaned);nativeMaster.frames[frame].duration=(tick(n+1)-tick(n))/1000
 if n==14 or n==26 or n==40 then composite(cleaned,245,245,245):saveAs(root..string.format('/native_on_light/%04d.png',n));composite(cleaned,20,26,34):saveAs(root..string.format('/native_on_dark/%04d.png',n)) end
 -- One uniform whole-frame resample and translation matches the root's established source-study layout.
 local small=Image(cleaned);small:resize{width=math.floor(w*0.3125+0.5),height=math.floor(h*0.3125+0.5),method='bilinear'}
 local canvas=Image(256,256,ColorMode.RGB);local offsetX=55-(w-640)*0.3125;canvas:drawImage(small,Point(offsetX,-10));if n==0 or n==40 then canvas=Image(approvedK0) end;canvas:saveAs(root..string.format('/frames/%04d.png',n))
 local baseSmall=Image(baseline);baseSmall:resize{width=math.floor(w*0.3125+0.5),height=math.floor(h*0.3125+0.5),method='bilinear'}
 local baseCanvas=Image(256,256,ColorMode.RGB);baseCanvas:drawImage(baseSmall,Point(offsetX,-10))
 local light=composite(canvas,245,245,245);local dark=composite(canvas,20,26,34)
 light:saveAs(root..string.format('/sprite_on_light/%04d.png',n));dark:saveAs(root..string.format('/sprite_on_dark/%04d.png',n))
 lightBoard:drawImage(light,Point(((frame-1)%columns)*256,math.floor((frame-1)/columns)*256));darkBoard:drawImage(dark,Point(((frame-1)%columns)*256,math.floor((frame-1)/columns)*256));baseDarkBoard:drawImage(composite(baseCanvas,20,26,34),Point(((frame-1)%columns)*256,math.floor((frame-1)/columns)*256))
 if frame>1 then sprite:newFrame() end;sprite.cels[frame].image=canvas;sprite.frames[frame].duration=(tick(n+1)-tick(n))/1000
 results[#results+1]=stats
end
local tag=sprite:newTag(1,#selected);tag.name='wave';tag.aniDir=AniDir.FORWARD;sprite:saveAs(root..'/wave.aseprite');sprite:close();nativeMaster:saveAs(root..'/native_final_wave.aseprite');nativeMaster:close()
lightBoard:saveAs(root..'/contact_256_on_light.png');darkBoard:saveAs(root..'/contact_256_on_dark.png');baseDarkBoard:saveAs(root..'/baseline_contact_256_on_dark.png')
local f=io.open(root..'/pixel_processing_stats.json','w');f:write(json.encode({schema='reef.aseprite-boundary-alpha-pilot.v1',frames=results,parameters={connected_background_min_channel=170,connected_background_max_chroma=22,boundary_radius=4,foreground_radius=6,max_rgb_fit_error_l2=10,neutral_boundary_max_chroma=15,neutral_boundary_max_rgb_fit_error_l2=25,alpha_min=0.04,alpha_max=0.985,foreground_bg_separation_min_l2=45,bg_local_median_radius=4,foreground_seed_depth_min=2,foreground_seed_chroma_min=20,foreground_seed_dark_min_channel_max=140,protect_original_strict_closed_neutral_highlights=true,recover_visited_background_pixels=false,fit_new_closed_neutral_edge_each_rgb_le_local_background_minus=4,closed_neutral_rgb_fit_error_l2=10},acceptance='UNACCEPTED_MATTE_CANDIDATE_REVIEW_REQUIRED'}));f:close()






