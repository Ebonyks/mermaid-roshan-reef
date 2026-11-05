-- Apply measured album gain and a transparent native peak guard to saved sessions.
local path=debug.getinfo(1,'S').source:sub(2):gsub('\\','/')
local root=assert(path:match('^(.*)/tools/reaper/[^/]+$'))
local build=root..'/build/full_arrangements_20261101/'
local package=root..'/assets_src/audio/music/arranged_main_themes_20261101/'
assert(reaper.GetResourcePath():gsub('\\','/'):find('/build/reaper-profile-full',1,true))
reaper.Audio_Init();local ok,mode=reaper.GetAudioDeviceInfo('MODE');assert(ok and mode=='Dummy Audio')
local gains=dofile(build..'master_gains.lua');local scores=dofile(package..'performance.lua')
local function file(n,s)local f=assert(io.open(build..n,'w'));f:write(s);f:close()end
local receipt=assert(io.open(build..'native_mastering.tsv','w'))
receipt:write('cue\tproject\talbum_gain_db\tlimiter_threshold\tlimiter_ceiling\tlimiter_release_db_per_sec\n')
local function set_display(tr,fx,p,target,tolerance)
 local lo,hi=0,1
 for i=1,36 do
  local x=(lo+hi)/2;reaper.TrackFX_SetParamNormalized(tr,fx,p,x)
  local _,text=reaper.TrackFX_GetFormattedParamValue(tr,fx,p,'');local n=tonumber(text:match('[-+]?%d+%.?%d*'));assert(n)
  if math.abs(n-target)<(tolerance or .005) then return text end
  if n<target then lo=x else hi=x end
 end
 local _,text=reaper.TrackFX_GetFormattedParamValue(tr,fx,p,'');return text
end
for _,s in ipairs(scores)do
 for _,kind in ipairs({'composition','mix'})do
  file('current.txt','Mastering '..s.id..' '..kind)
  reaper.Main_OnCommand(40859,0);reaper.Main_openProject(build..s.id..'_'..kind..'.rpp')
  local master=reaper.GetMasterTrack(0);assert(reaper.TrackFX_GetCount(master)==4)
  reaper.SetMediaTrackInfo_Value(master,'D_VOL',1)
  local global=nil
  for p=0,reaper.TrackFX_GetNumParams(master,2)-1 do local _,name=reaper.TrackFX_GetParamName(master,2,p,'');if name=='Global Gain' then global=p end end
  assert(global,'Master EQ Global Gain not found')
  local gain_display=set_display(master,2,global,gains[s.id],.051)
  reaper.TrackFX_SetNamedConfigParm(master,2,'renamed_name',string.format('Album gain %+0.2f dB',gains[s.id]))
  reaper.TrackFX_SetEnabled(master,1,true)
  local threshold=set_display(master,3,0,-3.8);local ceiling=set_display(master,3,1,-3.8);reaper.TrackFX_SetParamNormalized(master,3,2,.3548134)
  local _,release=reaper.TrackFX_GetFormattedParamValue(master,3,2,'') -- 15 dB/sec, not milliseconds
  reaper.TrackFX_SetEnabled(master,3,true)
  reaper.GetSetProjectInfo(0,'RENDER_NORMALIZE',0,true)
  reaper.GetSetProjectInfo_String(0,'RENDER_PATTERN',s.id..'_master',true)
  receipt:write(s.id..'\t'..kind..'\t'..gain_display..'\t'..threshold..'\t'..ceiling..'\t'..release..'\n');receipt:flush()
  reaper.Main_SaveProjectEx(0,build..s.id..'_'..kind..'.rpp',8)
  if kind=='mix' then
   reaper.GetSetProjectInfo_String(0,'RENDER_PATTERN',s.id..'_master_native_verified',true)
   reaper.Main_OnCommand(42230,0)
   reaper.GetSetProjectInfo_String(0,'RENDER_PATTERN',s.id..'_master',true)
   reaper.Main_SaveProjectEx(0,build..s.id..'_mix.rpp',8)
  end
 end
end
receipt:close();file('current.txt','NATIVE MASTERS COMPLETE: final encode and independent quality checks next')
