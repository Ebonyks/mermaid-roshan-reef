-- Aseprite 1.3.18.4: newly authored connected contour directly into complete
-- native images. No cropped body parts, hand/arm templates, or part-image draws.
-- Original native PNGs remain unchanged; each output cel is one flattened image.
-- API: https://aseprite.org/api/graphicscontext and /api/image
local root = assert(app.params.root, "root is required")
local output = assert(app.params.output, "output is required")
local cfg={}
if app.params.config then local f=assert(io.open(app.params.config,"rb"));cfg=json.decode(f:read("*a"));f:close() end
local masterName=cfg.master_name or "trial.aseprite"
assert(not app.fs.isFile(app.fs.joinPath(output,masterName)), "preserve earlier trials; use a new output folder")
app.fs.makeAllDirectories(output)
local started=os.time();local startedUTC=os.date("!%Y-%m-%dT%H:%M:%SZ",started)
local sourceDir = app.fs.joinPath(root,cfg.source_dir or "assets_src/animation/roshan_wave_repair_20261010/native640_01/take_01/native_frames")
local SOURCE_W,SOURCE_H=640,896
if cfg.native_canvas then SOURCE_W,SOURCE_H=cfg.native_canvas[1],cfg.native_canvas[2] end
local PAD=cfg.workspace_padding_left or 0
local CANVAS_W=SOURCE_W+PAD
local repairY=cfg.repair_y_range or {130,590}
local repairRight=cfg.repair_right_max or 238
local headMasks=nil
if cfg.head_boundary_masks then local f=assert(io.open(app.fs.joinPath(root,cfg.head_boundary_masks),"rb"));headMasks=json.decode(f:read("*a"));f:close() end
local lens=cfg.lengths_native or {upper=81.664,fore=78.461,open_hand=65.651}
local U,F,H=lens.upper,lens.fore,lens.open_hand
local poses = {
  {index=8, shoulder={213,345}, upper=125, fore=155, hand=175},
  {index=26, shoulder={213,345}, upper=174.25, fore=220, hand=225},
  {index=32, shoulder={213,345}, upper=124.875, fore=132.5, hand=145},
}
local function boundedHermite(keys,n,name)
  local function secant(i) return (keys[i+1][name]-keys[i][name])/(keys[i+1].frame-keys[i].frame) end
  local function tangent(i)
    if i==1 then return secant(1) end
    if i==#keys then return secant(#keys-1) end
    local a,b=secant(i-1),secant(i)
    if a*b<=0 then return 0 end
    local ha,hb=keys[i].frame-keys[i-1].frame,keys[i+1].frame-keys[i].frame
    local w1,w2=2*hb+ha,hb+2*ha
    return (w1+w2)/(w1/a+w2/b)
  end
  if n<=keys[1].frame then return keys[1][name] end
  if n>=keys[#keys].frame then return keys[#keys][name] end
  for i=1,#keys-1 do if n>=keys[i].frame and n<=keys[i+1].frame then
    local a,b=keys[i],keys[i+1];local span=b.frame-a.frame;local t=(n-a.frame)/span
    local z=(2*t^3-3*t^2+1)*a[name]+(t^3-2*t^2+t)*span*tangent(i)+(-2*t^3+3*t^2)*b[name]+(t^3-t^2)*span*tangent(i+1)
    return math.max(math.min(a[name],b[name]),math.min(math.max(a[name],b[name]),z))
  end end
end
if cfg.frame_count then
  assert(cfg.frame_count==41 and cfg.fps==24,"this recipe is scoped to the authorized 41-frame wave")
  poses={}
  for n=0,cfg.frame_count-1 do
    local doPaint=n>=cfg.paint_range[1] and n<=cfg.paint_range[2]
    local p={index=n,paint=doPaint,shoulder=cfg.shoulder_native,openness=1}
    if doPaint then
      for _,name in ipairs({"upper","fore","hand"}) do p[name]=boundedHermite(cfg.angle_keys,n,name) end
      if cfg.angle_keys[1].shoulder_x then p.shoulder={boundedHermite(cfg.angle_keys,n,"shoulder_x"),boundedHermite(cfg.angle_keys,n,"shoulder_y")} end
      local function ease(t) return t*t*(3-2*t) end
      if n<8 then p.openness=ease(math.max(0,(n-4)/4)) elseif n>30 then p.openness=ease(math.max(0,(34-n)/4)) end
    end
    poses[#poses+1]=p
  end
end
if cfg.sample_frames then
  local wanted,selected={},{}
  for _,n in ipairs(cfg.sample_frames) do wanted[n]=true end
  for _,p in ipairs(poses) do if wanted[p.index] then selected[#selected+1]=p end end
  assert(#selected==#cfg.sample_frames,"sample frame not in recipe")
  poses=selected
end
local function v(x,y) return {x,y} end
local function add(a,b) return v(a[1]+b[1],a[2]+b[2]) end
local function mul(a,k) return v(a[1]*k,a[2]*k) end
local function sub(a,b) return add(a,mul(b,-1)) end
local function direction(deg) local r=math.rad(deg);return v(math.cos(r),math.sin(r)) end
local function normal(d) return v(-d[2],d[1]) end
local function unit(a) local z=math.sqrt(a[1]^2+a[2]^2);return mul(a,1/z) end
local function color(r,g,b,a) return Color{r=r,g=g,b=b,a=a or 255} end
local palette = {base=color(255,223,192),shadow=color(248,188,141),highlight=color(255,240,217),outline=color(88,82,64),crease=color(168,111,72)}
if cfg.palette then for name,c in pairs(cfg.palette) do palette[name]=color(c[1],c[2],c[3]) end end
local function pm(gc,p) gc:moveTo(p[1],p[2]) end
local function pc(gc,a,b,c) gc:cubicTo(a[1],a[2],b[1],b[2],c[1],c[2]) end
local function armContour(gc,p)
  local S,E,W,du,df,dh,nu,nf,nh,ne = p.S,p.E,p.W,p.du,p.df,p.dh,p.nu,p.nf,p.nh,p.ne
  local function hp(u,z)
    return add(W,add(mul(nh,u),mul(dh,z)))
  end
  local bend=13
  local outerBefore=sub(sub(E,mul(du,bend)),mul(nu,10.5))
  local outerAfter=sub(add(E,mul(df,bend)),mul(nf,9.5))
  local innerBefore=add(sub(E,mul(du,bend)),mul(nu,10.5))
  local innerAfter=add(add(E,mul(df,bend)),mul(nf,9.5))
  gc:beginPath();pm(gc,sub(S,mul(nu,12)))
  pc(gc,sub(add(S,mul(du,U*.35)),mul(nu,15)),sub(outerBefore,mul(du,14)),outerBefore)
  pc(gc,add(outerBefore,mul(du,bend*.8)),sub(outerAfter,mul(df,bend*.8)),outerAfter)
  pc(gc,sub(add(outerAfter,mul(df,18)),mul(nf,1.1)),sub(sub(W,mul(df,F*.26)),mul(nf,8.5)),hp(-7,0))
  local fringeCompensation=cfg.visible_tip_fringe_compensation or 0
  -- Two authored anatomical states, with curved relaxed fingertips and an
  -- opposed thumb; blend control coordinates, never image pixels or part cels.
  local open={
    {-12,4,-16,16,-19,28},{-22,36,-25,44,-23,48},{-21,51,-17.5,50,-17,46},
    {-16.5,40,-15,35,-13.6,32},{-13.7,39,-15,49,-13,55},{-12,59,-8,60,-6.7,55},
    {-5.8,48,-6,39,-4.2,34},{-3.8,43,-4.8,58-fringeCompensation,-2.4,63.1-fringeCompensation},
    {-1.2,H+.9-fringeCompensation,2,H+.9-fringeCompensation,3.8,63.1-fringeCompensation},
    {5.3,54,4.1,42,6.5,34},{8.3,40,9.2,50,12,55.4},{14.3,60,18.7,59.2,18.1,53.6},
    {17.4,44,16.1,36,16.8,29},{17.2,23,19.5,21,22.3,25.5},
    {25,30,27.1,35.9,31,33.8},{34.5,31.7,32.6,27.1,29.6,22.6},{24.4,14,15,6,7,0}}
  local peak=(cfg.relaxed_hand_native or 51.728)-1.5
  local relaxed={
    {-11,4,-12,16,-13,28},{-15,34,-17,38,-16,40},{-13,42,-11,40,-11,37},
    {-10,33,-9,29,-8,28},{-9,34,-11,43,-9,46},{-8,49,-5,49,-4,46},
    {-3,42,-3,33,-2,30},{-2,36,-3,peak-5,-1,peak-2},
    {0,peak+1,1,peak+1,2,peak-2},{3,45,2,34,4,30},{5,34,6,42,8,45},
    {10,48,13,46,12,42},{11,35,10,31,12,25},{13,21,14,19,15,24},
    {17,29,19,32,21,30},{23,28,22,24,20,20},{17,13,12,6,7,0}}
  local o=p.openness or 1
  for i,a in ipairs(open) do local b=relaxed[i];local c={}
    for j=1,6 do c[j]=b[j]+(a[j]-b[j])*o end
    pc(gc,hp(c[1],c[2]),hp(c[3],c[4]),hp(c[5],c[6]))
  end
  pc(gc,add(sub(W,mul(df,F*.25)),mul(nf,7.2)),add(innerAfter,mul(df,18)),innerAfter)
  pc(gc,sub(innerAfter,mul(df,bend*.8)),add(innerBefore,mul(du,bend*.8)),innerBefore)
  pc(gc,sub(innerBefore,mul(du,14)),add(add(S,mul(du,U*.35)),mul(nu,11.5)),add(S,mul(nu,12)))
  pc(gc,add(S,mul(du,-5)),add(S,mul(du,-5)),sub(S,mul(nu,12)));gc:closePath()
end
local borders={{130,238},{470,238},{480,190},{590,190}}
if cfg.fixture_domain then borders=cfg.fixture_domain.boundary end
local function bodyBoundary(y)
  for i=2,#borders do if y<=borders[i][1] then local a,b=borders[i-1],borders[i];return a[2]+(b[2]-a[2])*(y-a[1])/(b[1]-a[1]) end end
  return 190
end
local function makeRepairDomain(source,index)
  -- Preserve native hair/sleeve contours with a color-derived mask. A sleeve
  -- seed expands 5 px to retain its brown outline and existing antialiasing.
  -- This is a mask, not copied appearance pixels. Erasure/paint share the domain.
  local sleeve,hair,rgba={},{},app.pixelColor
  local headBoundary={}
  if headMasks then for _,r in ipairs(headMasks.frames[index+1].rows) do headBoundary[r[1]]=r[2] end end
  for y=318,590 do for x=176,242 do
    local z=source:getPixel(x,y);local r,g,b=rgba.rgbaR(z),rgba.rgbaG(z),rgba.rgbaB(z)
    if b>g+8 and b>r-70 and r>80 then sleeve[y*SOURCE_W+x]=true end
  end end
  -- Preserve brown/gold hair through its actual color contour, rather than a
  -- rectangular guard that retained skin patches and cut the bottom curl.
  for y=130,326 do for x=150,242 do
    local z=source:getPixel(x,y);local r,g,b=rgba.rgbaR(z),rgba.rgbaG(z),rgba.rgbaB(z)
    local coordinateScope=not headMasks or (headBoundary[y] and x>=headBoundary[y]-3)
    local likelySkin=r>215 and g>140 and b>100
    if coordinateScope and math.max(r,g,b)<235 and b<160 and not likelySkin then hair[y*SOURCE_W+x]=true end
  end end
  local protected={}
  local sleeveRadius=(cfg.fixture_domain and cfg.fixture_domain.fixture_color_dilation_native_px) or 5
  for key,_ in pairs(sleeve) do local x,y=key%SOURCE_W,math.floor(key/SOURCE_W)
    local radius=y<375 and sleeveRadius or 5
    for oy=-radius,radius do for ox=-radius,radius do if ox*ox+oy*oy<=radius*radius+1 then protected[(y+oy)*SOURCE_W+x+ox]=true end end end
  end
  for key,_ in pairs(hair) do local x,y=key%SOURCE_W,math.floor(key/SOURCE_W)
    for oy=-2,2 do for ox=-2,2 do if ox*ox+oy*oy<=5 then protected[(y+oy)*SOURCE_W+x+ox]=true end end end
  end
  local allowed={}
  for y=repairY[1],repairY[2] do allowed[y]={};local boundary=math.floor(bodyBoundary(y))
    for x=-PAD,boundary do
      local keepHead=(headMasks and y<280 and headBoundary[y] and x>=headBoundary[y]-3) or (y<=313 and x>=205)
      if not keepHead and not protected[y*SOURCE_W+x] then allowed[y][x+PAD]=true end
    end
  end
  return allowed
end
local function clipDomain(gc,domain)
  gc:beginPath()
  for y=repairY[1],repairY[2] do local run=nil
    for x=0,repairRight+PAD do local yes=domain[y][x]
      if yes and not run then run=x end
      if run and (not yes or x==repairRight+PAD) then local stop=yes and x+1 or x;gc:rect(Rectangle(run,y,stop-run,1));run=nil end
    end
  end
  gc:clip()
end
local function shadedCurve(gc,p,offset,width,col,opacity)
  gc.color=col;gc.opacity=opacity;gc.strokeWidth=width;gc:beginPath();pm(gc,add(p.S,mul(p.nu,offset)))
  pc(gc,add(add(p.S,mul(p.du,U*.45)),mul(p.nu,offset)),add(sub(p.E,mul(p.du,U*.1)),mul(p.ne,offset)),add(p.E,mul(p.ne,offset)))
  pc(gc,add(add(p.E,mul(p.df,F*.36)),mul(p.nf,offset*.7)),add(sub(p.W,mul(p.df,F*.14)),mul(p.nf,offset*.45)),add(p.W,mul(p.nh,offset*.35)))
  pc(gc,add(p.W,mul(p.dh,10)),add(add(p.W,mul(p.dh,25)),mul(p.nh,offset*.6)),add(add(p.W,mul(p.dh,31)),mul(p.nh,offset*.6)));gc:stroke()
end
local function paintedVolume(image,p,domain,index)
  -- A smooth, softly mottled painted color field, authored natively in Aseprite.
  -- Only fresh skin fill inside the repair domain is touched. No appearance
  -- pixels are sampled from another limb or from another source frame.
  local rgba=app.pixelColor
  local function dot(a,b) return a[1]*b[1]+a[2]*b[2] end
  local function nearby(q,a,d,len)
    local z=sub(q,a);local t=math.max(0,math.min(len,dot(z,d)))
    local delta=sub(z,mul(d,t));return dot(delta,delta),dot(delta,normal(d)),t/len
  end
  local function mix(a,b,t) return a+(b-a)*t end
  for y=repairY[1],repairY[2] do for x=0,repairRight+PAD do if domain[y][x] then
    local c=image:getPixel(x,y);local r,g,b=rgba.rgbaR(c),rgba.rgbaG(c),rgba.rgbaB(c)
    if r>245 and g<235 and b<220 and g>b+13 then
      local q=v(x+.5,y+.5);local d1,z1,t1=nearby(q,p.S,p.du,U)
      local d2,z2,t2=nearby(q,p.E,p.df,F);local z,width
      if d1<d2 then z=z1;width=12.5-2*t1 else z=z2;width=9.8-2.8*t2 end
      local hw=sub(q,p.W);local distal=dot(hw,p.dh)
      if distal>3 then z=dot(hw,p.nh);width=19 end
      local side=math.max(-1,math.min(1,z/width))
      local shadow=.52*math.exp(-((side-.88)/.75)^2)
      local highlight=.53*math.exp(-((side+.22)/.51)^2)
      local nr=mix(255,248,shadow);local ng=mix(223,188,shadow);local nb=mix(192,141,shadow)
      nr=mix(nr,255,highlight);ng=mix(ng,240,highlight);nb=mix(nb,217,highlight)
      local soft=1.2*math.sin(x*.17+y*.13+index*.17)+.65*math.sin(x*.41-y*.29)
      local grain=(((x*73+y*37+index*11)%17)-8)*.11
      local function byte(a) return math.floor(math.max(0,math.min(255,a+soft+grain))+.5) end
      image:drawPixel(x,y,rgba.rgba(byte(nr),byte(ng),byte(nb),255))
    end
  end end end
end
local native=Sprite(CANVAS_W,SOURCE_H,ColorMode.RGB)
native.layers[1].name="Complete native cel with newly painted connected contour"
local observations={schema="reef.aseprite-connected-paint-trial.v1",purpose=cfg.purpose or "Three representative complete native cels for model style review",revision="round elbow, complete fixture preservation, charcoal contour and native painted volume",authoring="Aseprite GraphicsContext cubicTo/fill/stroke and locally authored skin color field directly into each flattened native image",human_acceptance=false,cell_scale=3.2025,contract_lengths_native={upper=U,fore=F,open_hand=H},angles_convention="degrees clockwise in image coordinates: 0 right, 90 down",sources={},frames={},body_preservation_boundary=borders,paint_half_widths={upper=12,fore=8.5,wrist=7},palette={base="#ffdfc0",shadow="#f8bc8d",highlight="#fff0d9",outline="#585240"},api_sources={"https://aseprite.org/api/graphicscontext","https://aseprite.org/api/image"},profile=cfg,actual_method="whole-native-cel local direct paint",acceptance_status="DRAFT_UNREVIEWED_FULL_MOTION",run_started_utc=startedUTC}
for i,pose in ipairs(poses) do
  local src=app.fs.joinPath(sourceDir,string.format("%04d.png",pose.index));local before=Image{fromFile=src}
  assert(before.width==SOURCE_W and before.height==SOURCE_H,"unexpected native canvas")
  local whole=Image(CANVAS_W,SOURCE_H,ColorMode.RGB)
  if PAD>0 then for y=0,SOURCE_H-1 do local gray=before:getPixel(4,y);for x=0,PAD-1 do whole:drawPixel(x,y,gray) end end end
  whole:drawImage(before,Point(PAD,0))
  if pose.paint~=false then
  local domain=makeRepairDomain(before,pose.index)
  -- Neutral native field from one outside-gray pixel per row; no part pixels.
  for y=repairY[1],repairY[2] do local gray=before:getPixel(4,y)
    for x=0,repairRight+PAD do if domain[y][x] then whole:drawPixel(x,y,gray) end end
  end
  local p={S={pose.shoulder[1]+PAD,pose.shoulder[2]},du=direction(pose.upper),df=direction(pose.fore),dh=direction(pose.hand),openness=pose.openness or 1}
  p.nu,p.nf,p.nh=normal(p.du),normal(p.df),normal(p.dh)
  local handTarget=(cfg.relaxed_hand_native or 51.728)+(H-(cfg.relaxed_hand_native or 51.728))*p.openness
  p.ne=unit(add(p.nu,p.nf));p.E=add(p.S,mul(p.du,U));p.W=add(p.E,mul(p.df,F));p.T=add(p.W,mul(p.dh,handTarget))
  local gc=whole.context;gc.antialias=true;gc:save();clipDomain(gc,domain)
  armContour(gc,p);gc.color=palette.base;gc.opacity=255;gc:fill()
  gc:save();armContour(gc,p);gc:clip()
  -- Feathered curved accents give the new contour painted volume.
  for _,w in ipairs({18,13,8}) do shadedCurve(gc,p,7,w,palette.shadow,32) end
  for _,w in ipairs({15,10,6}) do shadedCurve(gc,p,-4,w,palette.highlight,46) end
  paintedVolume(whole,p,domain,pose.index)
  local function hp(u,z) return add(p.W,add(mul(p.nh,u),mul(p.dh,z))) end
  gc.color=palette.highlight;gc.opacity=58;gc.strokeWidth=3.1;gc:beginPath();pm(gc,hp(-1,28));pc(gc,hp(-1,35+6*p.openness),hp(-1.5,44+10*p.openness),hp(.3,48+13*p.openness));gc:stroke()
  gc.color=palette.crease;gc.opacity=108;gc.strokeWidth=1.05;gc:beginPath();pm(gc,hp(-10,22));pc(gc,hp(-5,16),hp(7,19),hp(12,28));gc:stroke()
  gc:beginPath();pm(gc,hp(11,13));pc(gc,hp(6,20),hp(9,27),hp(13,31));gc:stroke();gc:restore()
  armContour(gc,p);gc.color=palette.outline;gc.opacity=92;gc.strokeWidth=4.8;gc:stroke()
  armContour(gc,p);gc.color=palette.outline;gc.opacity=244;gc.strokeWidth=2.8;gc:stroke();gc:restore()
  observations.frames[i]={source_index=pose.index,master_frame=i,painted=true,shoulder={p.S[1],p.S[2]},elbow={p.E[1],p.E[2]},wrist={p.W[1],p.W[2]},longest_fingertip_target={p.T[1],p.T[2]},angles={upper=pose.upper,fore=pose.fore,hand=pose.hand},hand_open=p.openness>=.999,hand_openness=p.openness,analytic_lengths={upper=U,fore=F,open_hand=H,hand_target=handTarget},geometry_evidence="authored joint center distances and hand center target, padded canvas; not measured visible landmarks; silhouette and attachment still require native/model visual review"}
  else observations.frames[i]={source_index=pose.index,master_frame=i,painted=false,geometry_evidence="PENDING_NATIVE_LANDMARKS; unchanged source cel, no measured joints fabricated"} end
  if i>1 then native:newEmptyFrame(i) end
  native:newCel(native.layers[1],i,whole,Point(0,0))
  local duration=.25
  if cfg.fps then local tick=function(n) return math.floor((n*1000+cfg.fps/2)/cfg.fps) end;duration=(tick(i)-tick(i-1))/1000 end
  native.frames[i].duration=duration
  local dest=app.fs.joinPath(output,string.format("%04d.png",pose.index))
  if pose.paint==false and PAD==0 then local f=assert(io.open(src,"rb"));local bytes=f:read("*a");f:close();f=assert(io.open(dest,"wb"));f:write(bytes);f:close() else whole:saveAs(dest) end
  observations.sources[i]=src;observations.frames[i].output=dest;observations.frames[i].duration_ms=duration*1000
end
assert(#native.layers==1 and #native.frames==#poses and #native.cels==#poses,"whole-cel master structure failed")
native:saveAs(app.fs.joinPath(output,masterName))
observations.profile=nil;observations.profile_file=app.params.config;observations.profile_file_preserved_separately=true
observations.run_finished_utc=os.date("!%Y-%m-%dT%H:%M:%SZ");observations.run_wall_seconds=os.time()-started
observations.generated_api_calls=0;observations.gpu_jobs=0;observations.external_monetary_cost=0
local file=assert(io.open(app.fs.joinPath(output,"joint_geometry.json"),"wb"));file:write(json.encode(observations),"\n");file:close();native:close()
print("Preserved native sources; saved "..#poses.." whole-cel PNGs and one-layer master: "..output)
