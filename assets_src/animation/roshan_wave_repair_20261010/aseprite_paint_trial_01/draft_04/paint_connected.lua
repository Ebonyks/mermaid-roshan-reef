-- Aseprite 1.3.18.4: newly authored connected contour directly into complete
-- native images. No cropped body parts, hand/arm templates, or part-image draws.
-- Original native PNGs remain unchanged; each output cel is one flattened image.
-- API: https://aseprite.org/api/graphicscontext and /api/image
local root = assert(app.params.root, "root is required")
local output = assert(app.params.output, "output is required")
assert(not app.fs.isFile(app.fs.joinPath(output, "trial.aseprite")), "preserve earlier trials; use a new output folder")
app.fs.makeAllDirectories(output)
local sourceDir = app.fs.joinPath(root, "assets_src/animation/roshan_wave_repair_20261010/native640_01/take_01/native_frames")
local U, F, H = 81.664, 78.461, 65.651
local poses = {
  {index=8, shoulder={213,345}, upper=125, fore=155, hand=175},
  {index=26, shoulder={213,345}, upper=174.25, fore=220, hand=225},
  {index=32, shoulder={213,345}, upper=124.875, fore=132.5, hand=145},
}
local function v(x,y) return {x,y} end
local function add(a,b) return v(a[1]+b[1],a[2]+b[2]) end
local function mul(a,k) return v(a[1]*k,a[2]*k) end
local function sub(a,b) return add(a,mul(b,-1)) end
local function direction(deg) local r=math.rad(deg);return v(math.cos(r),math.sin(r)) end
local function normal(d) return v(-d[2],d[1]) end
local function unit(a) local z=math.sqrt(a[1]^2+a[2]^2);return mul(a,1/z) end
local function color(r,g,b,a) return Color{r=r,g=g,b=b,a=a or 255} end
local palette = {base=color(255,223,192),shadow=color(248,188,141),highlight=color(255,240,217),outline=color(88,82,64),crease=color(168,111,72)}
local function pm(gc,p) gc:moveTo(p[1],p[2]) end
local function pc(gc,a,b,c) gc:cubicTo(a[1],a[2],b[1],b[2],c[1],c[2]) end
local function armContour(gc,p)
  local S,E,W,du,df,dh,nu,nf,nh,ne = p.S,p.E,p.W,p.du,p.df,p.dh,p.nu,p.nf,p.nh,p.ne
  local function hp(u,z) return add(W,add(mul(nh,u),mul(dh,z))) end
  local bend=13
  local outerBefore=sub(sub(E,mul(du,bend)),mul(nu,10.5))
  local outerAfter=sub(add(E,mul(df,bend)),mul(nf,9.5))
  local innerBefore=add(sub(E,mul(du,bend)),mul(nu,10.5))
  local innerAfter=add(add(E,mul(df,bend)),mul(nf,9.5))
  gc:beginPath();pm(gc,sub(S,mul(nu,12)))
  pc(gc,sub(add(S,mul(du,U*.35)),mul(nu,15)),sub(outerBefore,mul(du,14)),outerBefore)
  pc(gc,add(outerBefore,mul(du,bend*.8)),sub(outerAfter,mul(df,bend*.8)),outerAfter)
  pc(gc,sub(add(outerAfter,mul(df,18)),mul(nf,1.1)),sub(sub(W,mul(df,F*.26)),mul(nf,8.5)),hp(-7,0))
  -- Palm, four unequal fingers, and an opposed thumb share one closed path.
  pc(gc,hp(-12,4),hp(-16,16),hp(-19,28))
  pc(gc,hp(-22,36),hp(-25,44),hp(-23,48))
  pc(gc,hp(-21,51),hp(-17.5,50),hp(-17,46))
  pc(gc,hp(-16.5,40),hp(-15,35),hp(-13.6,32))
  pc(gc,hp(-13.7,39),hp(-15,49),hp(-13,55))
  pc(gc,hp(-12,59),hp(-8,60),hp(-6.7,55))
  pc(gc,hp(-5.8,48),hp(-6,39),hp(-4.2,34))
  pc(gc,hp(-3.8,43),hp(-4.8,58),hp(-2.4,63.1))
  pc(gc,hp(-1.2,H+.9),hp(2,H+.9),hp(3.8,63.1))
  pc(gc,hp(5.3,54),hp(4.1,42),hp(6.5,34))
  pc(gc,hp(8.3,40),hp(9.2,50),hp(12,55.4))
  pc(gc,hp(14.3,60),hp(18.7,59.2),hp(18.1,53.6))
  pc(gc,hp(17.4,44),hp(16.1,36),hp(16.8,29))
  pc(gc,hp(17.2,23),hp(19.5,21),hp(22.3,25.5))
  pc(gc,hp(25,30),hp(27.1,35.9),hp(31,33.8))
  pc(gc,hp(34.5,31.7),hp(32.6,27.1),hp(29.6,22.6))
  pc(gc,hp(24.4,14),hp(15,6),hp(7,0))
  pc(gc,add(sub(W,mul(df,F*.25)),mul(nf,7.2)),add(innerAfter,mul(df,18)),innerAfter)
  pc(gc,sub(innerAfter,mul(df,bend*.8)),add(innerBefore,mul(du,bend*.8)),innerBefore)
  pc(gc,sub(innerBefore,mul(du,14)),add(add(S,mul(du,U*.35)),mul(nu,11.5)),add(S,mul(nu,12)))
  pc(gc,add(S,mul(du,-5)),add(S,mul(du,-5)),sub(S,mul(nu,12)));gc:closePath()
end
local borders={{130,150},{315,150},{320,176},{335,188},{345,238},{470,238},{480,190},{590,190}}
local function bodyBoundary(y)
  for i=2,#borders do if y<=borders[i][1] then local a,b=borders[i-1],borders[i];return a[2]+(b[2]-a[2])*(y-a[1])/(b[1]-a[1]) end end
  return 190
end
local function makeRepairDomain(source)
  -- Preserve native hair/sleeve contours with a color-derived mask. A sleeve
  -- seed expands 5 px to retain its brown outline and existing antialiasing.
  -- This is a mask, not copied appearance pixels. Erasure/paint share the domain.
  local sleeve,rgba={},app.pixelColor
  for y=318,590 do for x=176,242 do
    local z=source:getPixel(x,y);local r,g,b=rgba.rgbaR(z),rgba.rgbaG(z),rgba.rgbaB(z)
    if b>g+8 and b>r-70 and r>80 then sleeve[y*640+x]=true end
  end end
  local protected={}
  for key,_ in pairs(sleeve) do local x,y=key%640,math.floor(key/640)
    for oy=-5,5 do for ox=-5,5 do if ox*ox+oy*oy<=26 then protected[(y+oy)*640+x+ox]=true end end end
  end
  local allowed={}
  for y=130,590 do allowed[y]={};local boundary=math.floor(bodyBoundary(y))
    for x=0,boundary do local keepHair=(y<=337 and x>=165 and y>=318)
      if not keepHair and not protected[y*640+x] then allowed[y][x]=true end
    end
  end
  return allowed
end
local function clipDomain(gc,domain)
  gc:beginPath()
  for y=130,590 do local run=nil
    for x=0,238 do local yes=domain[y][x]
      if yes and not run then run=x end
      if run and (not yes or x==238) then local stop=yes and x+1 or x;gc:rect(Rectangle(run,y,stop-run,1));run=nil end
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
  for y=130,590 do for x=0,238 do if domain[y][x] then
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
local native=Sprite(640,896,ColorMode.RGB)
native.layers[1].name="Complete native cel with newly painted connected contour"
local observations={schema="reef.aseprite-connected-paint-trial.v1",purpose="Three representative complete native cels for model style review",revision="round elbow, complete fixture preservation, charcoal contour and native painted volume",authoring="Aseprite GraphicsContext cubicTo/fill/stroke and locally authored skin color field directly into each flattened native image",human_acceptance=false,cell_scale=3.2025,contract_lengths_native={upper=U,fore=F,open_hand=H},angles_convention="degrees clockwise in image coordinates: 0 right, 90 down",sources={},frames={},body_preservation_boundary=borders,paint_half_widths={upper=12,fore=8.5,wrist=7},palette={base="#ffdfc0",shadow="#f8bc8d",highlight="#fff0d9",outline="#585240"},api_sources={"https://aseprite.org/api/graphicscontext","https://aseprite.org/api/image"}}
for i,pose in ipairs(poses) do
  local src=app.fs.joinPath(sourceDir,string.format("%04d.png",pose.index));local before=Image{fromFile=src}
  assert(before.width==640 and before.height==896,"unexpected native canvas")
  local whole=Image(before);local domain=makeRepairDomain(before)
  -- Neutral native field from one outside-gray pixel per row; no part pixels.
  for y=130,590 do local gray=before:getPixel(4,y)
    for x=0,238 do if domain[y][x] then whole:drawPixel(x,y,gray) end end
  end
  local p={S=pose.shoulder,du=direction(pose.upper),df=direction(pose.fore),dh=direction(pose.hand)}
  p.nu,p.nf,p.nh=normal(p.du),normal(p.df),normal(p.dh)
  p.ne=unit(add(p.nu,p.nf));p.E=add(p.S,mul(p.du,U));p.W=add(p.E,mul(p.df,F));p.T=add(p.W,mul(p.dh,H))
  local gc=whole.context;gc.antialias=true;gc:save();clipDomain(gc,domain)
  armContour(gc,p);gc.color=palette.base;gc.opacity=255;gc:fill()
  gc:save();armContour(gc,p);gc:clip()
  -- Feathered curved accents give the new contour painted volume.
  for _,w in ipairs({18,13,8}) do shadedCurve(gc,p,7,w,palette.shadow,32) end
  for _,w in ipairs({15,10,6}) do shadedCurve(gc,p,-4,w,palette.highlight,46) end
  paintedVolume(whole,p,domain,pose.index)
  local function hp(u,z) return add(p.W,add(mul(p.nh,u),mul(p.dh,z))) end
  gc.color=palette.highlight;gc.opacity=58;gc.strokeWidth=3.1;gc:beginPath();pm(gc,hp(-1,28));pc(gc,hp(-1,41),hp(-1.5,54),hp(.3,61));gc:stroke()
  gc.color=palette.crease;gc.opacity=108;gc.strokeWidth=1.05;gc:beginPath();pm(gc,hp(-10,22));pc(gc,hp(-5,16),hp(7,19),hp(12,28));gc:stroke()
  gc:beginPath();pm(gc,hp(11,13));pc(gc,hp(6,20),hp(9,27),hp(13,31));gc:stroke();gc:restore()
  armContour(gc,p);gc.color=palette.outline;gc.opacity=92;gc.strokeWidth=4.8;gc:stroke()
  armContour(gc,p);gc.color=palette.outline;gc.opacity=244;gc.strokeWidth=2.8;gc:stroke();gc:restore()
  if i>1 then native:newEmptyFrame(i) end
  native:newCel(native.layers[1],i,whole,Point(0,0));native.frames[i].duration=.25
  local dest=app.fs.joinPath(output,string.format("%04d.png",pose.index));whole:saveAs(dest)
  observations.sources[i]=src
  observations.frames[i]={source_index=pose.index,master_frame=i,output=dest,shoulder=p.S,elbow=p.E,wrist=p.W,longest_fingertip=p.T,angles={upper=pose.upper,fore=pose.fore,hand=pose.hand},hand_open=true,analytic_lengths={upper=U,fore=F,open_hand=H},geometry_evidence="authored joint center distances; silhouette and attachment still require native/model visual review"}
end
assert(#native.layers==1 and #native.frames==3 and #native.cels==3,"whole-cel master structure failed")
native:saveAs(app.fs.joinPath(output,"trial.aseprite"))
local file=assert(io.open(app.fs.joinPath(output,"joint_geometry.json"),"wb"));file:write(json.encode(observations),"\n");file:close();native:close()
print("Preserved native sources; saved 3 whole-cel PNGs and one-layer 3-frame master: "..output)
