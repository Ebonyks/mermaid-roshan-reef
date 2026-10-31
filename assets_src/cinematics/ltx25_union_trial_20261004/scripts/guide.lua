-- Authored complete-figure structural drawing, not delivery pixels or appearance authority.
local p=app.params.packet;local root=app.params.root
for _,n in ipairs({'guide_full','guide_half','guide_quarter'}) do app.fs.makeDirectory(p..'/'..n) end
local keys={{0,80,500,116,408,0},{3,82,500,118,407,0},{7,100,236,92,321,.65},{17,80,104,117,226,1},{22,96,180,65,289,.85},{27,82,339,99,382,.45},{36,80,500,116,408,0},{40,80,500,116,408,0}}
local function pose(i)
 for j=1,#keys-1 do if i>=keys[j][1] and i<=keys[j+1][1] then
  local t=(i-keys[j][1])/(keys[j+1][1]-keys[j][1]);t=t*t*(3-2*t)
  local a={};for k=2,6 do a[k-1]=keys[j][k]+(keys[j+1][k]-keys[j][k])*t end;return a
 end end
end
local function draw(i,scale)
 local im=Image(640/scale,896/scale,ColorMode.RGB);im:clear(Color{r=0,g=0,b=0,a=255})
 local v=pose(i);local phase=v[5];local ang=.012*phase
 local c,s=math.cos(ang),math.sin(ang)
 local function tr(x,y,part)
  if part=='shoulder' then y=y-6*phase*(1-math.min(1,math.abs(x-140)/120))*math.max(0,math.min(1,(453-y)/140)) end
  if part=='hair' then x=x+4*math.sin(i*math.pi/20)*math.max(0,(x-260)/155) end
  if part=='tail' then x=x+4*math.sin(i*math.pi/20)*math.max(0,(y-453)/330) end
  local dx,dy=x-184.5,y-453
  return {(184.5+dx*c-dy*s+32)/scale,(453+dx*s+dy*c+32)/scale}
 end
 local white=Color{r=255,g=255,b=255,a=255}
 local function line(a,b)
  local n=math.max(1,math.ceil(math.max(math.abs(b[1]-a[1]),math.abs(b[2]-a[2]))))
  for j=0,n do local x=math.floor(a[1]+(b[1]-a[1])*j/n+.5);local y=math.floor(a[2]+(b[2]-a[2])*j/n+.5)
   if x>=0 and y>=0 and x<im.width and y<im.height then im:drawPixel(x,y,white) end
  end
 end
 local function path(points,part,closed,smooth)
  local pts={};for _,a in ipairs(points) do pts[#pts+1]=tr(a[1],a[2],part) end
  if smooth then
   local count=#pts;local total=closed and count or count-1
   for j=1,total do
    local function at(k) if closed then return pts[(k-1)%count+1] else return pts[math.max(1,math.min(count,k))] end end
    local a,b,c1,d=at(j-1),at(j),at(j+1),at(j+2);local last=b
    for q=1,12 do local t=q/12;local t2,t3=t*t,t*t*t
     local now={};for axis=1,2 do now[axis]=.5*((2*b[axis])+(-a[axis]+c1[axis])*t+(2*a[axis]-5*b[axis]+4*c1[axis]-d[axis])*t2+(-a[axis]+3*b[axis]-3*c1[axis]+d[axis])*t3) end
     line(last,now);last=now
    end
   end
  else for j=1,#pts-1 do line(pts[j],pts[j+1]) end;if closed then line(pts[#pts],pts[1]) end end
 end
 -- Hair, face, crown and stable facial landmarks: fixed shape, pose-dependent rigid lean.
 path({{113,280},{96,253},{104,230},{95,206},{104,156},{124,115},{161,87},{202,79},{254,98},{304,108},{332,147},{384,163},{414,199},{410,247},{385,283},{381,312},{339,334},{308,316},{276,300},{276,278}},'hair',true,true)
 path({{142,172},{163,143},{192,129},{220,140},{250,161},{273,182},{276,221},{262,251},{232,274},{201,279},{172,264},{147,241},{138,205}},'head',true,true)
 path({{148,166},{166,153},{193,149},{216,170},{243,179},{253,172}},'head',false,true)
 for _,x in ipairs({174,242}) do
  path({{x-13,201},{x-10,188},{x,182},{x+12,189},{x+14,207},{x+7,220},{x-5,221},{x-13,211}},'head',true,true)
 end
 path({{185,247},{202,251},{219,245}},'head',false,true)
 path({{166,100},{178,83},{195,91},{213,54},{230,92},{249,83},{266,107},{238,105},{213,87},{189,105}},'head',true,false)
 -- Complete bodice, sleeves, waist and tail, all re-authored on every guide frame.
 path({{160,283},{164,299},{190,307},{217,299},{230,283}},'shoulder',false,true)
 path({{144,296},{126,321},{137,346},{149,334},{154,394},{150,434},{184.5,453},{247,438},{263,392},{265,335},{282,343},{296,319},{279,297},{241,294},{217,307},{190,315},{162,309}},'shoulder',true,true)
 path({{150,434},{137,421},{133,439},{152,449},{184.5,453},{220,442},{247,426},{262,412},{274,428},{247,448}},'shoulder',false,true)
 path({{150,446},{126,491},{124,578},{132,652},{149,709},{190,744},{237,759},{284,756},{312,744},{336,762},{379,778},{423,770},{467,739},{523,702},{493,685},{448,678},{416,687},{385,706},{423,670},{428,628},{460,579},{486,543},{450,548},{416,566},{381,609},{345,675},{330,704},{303,718},{271,715},{254,691},{248,650},{263,598},{277,547},{279,494},{266,451}},'tail',true,true)
 path({{312,744},{350,715},{400,654},{450,582}},'tail',false,true)
 path({{336,753},{391,749},{450,716},{496,696}},'tail',false,true)
 -- Left waving arm: one connected contour through shoulder/elbow/wrist/palm/fingers.
 local hx,hy,ex,ey=v[1],v[2],v[3],v[4];local ha=math.pi*(1-phase)
 local hc,hs=math.cos(ha),math.sin(ha)
 local function hand(x,y) return {hx+x*hc-y*hs,hy+x*hs+y*hc} end
 local wrist=hand(0,18)
 local arm={{140,319},{ex-10,ey},{wrist[1]-9,wrist[2]}}
 local hp={{-9,18},{-18,5},{-21,-9},{-18,-17},{-12,-4},{-13,-26},{-9,-32},{-5,-8},{-4,-33},{1,-35},{4,-8},{7,-30},{12,-32},{10,-5},{18,-21},{22,-20},{16,2},{21,-6},{27,-6},{27,0},{13,15},{9,18}}
 for _,a in ipairs(hp) do arm[#arm+1]=hand(a[1],a[2]) end
 arm[#arm+1]={ex+10,ey};arm[#arm+1]={151,323};path(arm,'arm',true,false)
 path({{275,326},{285,391},{321,480},{341,500},{346,517},{342,531},{336,513},{335,535},{329,531},{327,513},{321,531},{317,526},{318,503},{311,499},{282,438},{262,359}},'shoulder',true,true)
 local anchors={};for name,a in pairs({crown={213,54},left_eye={174,202},right_eye={242,202},neck={195,301},waist={184.5,453},left_shoulder={140,319},right_shoulder={275,326},tail_junction={271,715}}) do
  local part='head';if name=='tail_junction' then part='tail' elseif name=='neck' or name=='left_shoulder' or name=='right_shoulder' then part='shoulder' end
  anchors[name]=tr(a[1],a[2],part)
 end
 return im,anchors
end
local master=Sprite(640,896,ColorMode.RGB);master.layers[1].name='Whole-figure control outlines; no delivery pixels'
local records={}
for i=0,40 do
 if i>0 then master:newFrame() end
 local full,anchors=draw(i,1);master.cels[i+1].image=full
 master.frames[i+1].duration=(math.floor((i+1)*1000/24+.5)-math.floor(i*1000/24+.5))/1000
 full:saveAs(p..string.format('/guide_full/%04d.png',i))
 local half=draw(i,2);half:saveAs(p..string.format('/guide_half/%04d.png',i))
 local quarter=draw(i,4);quarter:saveAs(p..string.format('/guide_quarter/%04d.png',i))
 records[#records+1]={index=i,anchors=anchors,uniform_body_lean_radians=.012*pose(i)[5],world_scale=1,role='structural_motion_control_only',used_as_delivery_pixels=false}
end
master:saveAs(p..'/structural_guide.aseprite');master:close()
local first=Image{fromFile=root..'/assets_src/cinematics/ltx25_8gb_wave_20261004/scale_continuity/registered_guides/guide_0000.png'}
local plate=Image(640,896,ColorMode.RGB);plate:clear(Color{r=238,g=238,b=238,a=255});plate:drawImage(first,Point(32,32));plate:saveAs(p..'/identity_first_frame.png')
local f=io.open(p..'/guide_plan.json','w');f:write(json.encode({status='AUTHORING_PLAN_NOT_PIXEL_ACCEPTANCE',frames=records,source='Existing complete Roshan pose guides0,3,7,17,22,27,36,40; outline manually re-authored with continuous pose trajectories',method='Whole-figure Catmull-Rom contour drawing and smoothstep pose in-betweens through Aseprite; controls only',appearance_authority='Approved source atlas through registered opening; outlines carry no appearance authority',delivery_pixels=false}));f:close()
print('ASEPRITE_GUIDE_COMPLETE41 frames full640x896/half320x448/quarter160x224')
