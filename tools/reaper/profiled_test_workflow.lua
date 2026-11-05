-- One isolated worker, with no user project or hardware-audio access.
local src=debug.getinfo(1,'S').source:sub(2):gsub('\\','/')
local root=assert(src:match('^(.*)/tools/reaper/[^/]+$'))
local build=root..'/build/profiled_test_tracks_20261101/'
assert(reaper.GetResourcePath():gsub('\\','/'):find('/build/reaper-profile-audition',1,true))
assert(reaper.CountTracks(0)==0,'Protect nonempty projects')
reaper.Audio_Init();local ok,mode=reaper.GetAudioDeviceInfo('MODE');assert(ok and mode=='Dummy Audio')
local function write(p,s)local f=assert(io.open(p,'wb'));f:write(s);f:close()end
local function read(p)local f=io.open(p,'rb');if not f then return ''end;local s=f:read('*a');f:close();return s end
_G.ROSHAN_AUTHORING_BUILD=build
_G.ROSHAN_AUTHORING_PACKAGE=root..'/assets_src/audio/music/profiled_test_tracks_20261101/'
_G.ROSHAN_RESOURCE_GUARD='/build/reaper-profile-audition'
_G.ROSHAN_AUDITION_BUILD=root..'/build/expanded_palette_auditions_20261101/'
_G.ROSHAN_KEEP_WORKER=true;_G.ROSHAN_MASTER_CEILING=-2.0
_G.ROSHAN_SKIP_LEGACY_GUARDS=true;_G.ROSHAN_BUS_TIMING=true
local scripts={auditions='render_instrument_auditions.lua',build='build_warm_ensemble.lua',mix='mix_warm_ensemble.lua',master='master_warm_ensemble.lua'}
local alive=true
local function owned_project(filename)
 filename=(filename or ''):gsub('\\','/'):lower()
 return filename=='' or filename:sub(1,#build)==build:lower() or filename:sub(1,#_G.ROSHAN_AUDITION_BUILD)==_G.ROSHAN_AUDITION_BUILD:lower()
end
local function clear_private_tabs(stage)
 local idx=0
 while true do
  idx=idx+1;assert(idx<=20,'Unexpected private project-tab count')
  local _,filename=reaper.EnumProjects(-1,'');assert(owned_project(filename),'Preserve unexpected project')
  for i=reaper.CountTracks(0)-1,0,-1 do reaper.DeleteTrack(reaper.GetTrack(0,i))end
  reaper.Main_SaveProjectEx(0,build..'_worker_empty_'..stage..'_'..idx..'.rpp',8)
  if not reaper.EnumProjects(1,'')then break end
  local action=reaper.kbd_getTextFromCmd(40860,0):lower()
  assert(action:find('close') and action:find('tab'),'Unexpected close-tab action')
  reaper.Main_OnCommand(40860,0)
 end
end
local function cycle()
 local command=read(build..'command.txt'):match('^%s*(.-)%s*$')
 if #command>0 then
  write(build..'command.txt','')
  local good,err=xpcall(function()
   local _,filename=reaper.EnumProjects(-1,'')
   assert(reaper.CountTracks(0)==0 and not reaper.EnumProjects(1,'') and owned_project(filename),'Preserve unexpected project before workflow command')
   if command=='stop' then
    clear_private_tabs('stop');alive=false;write(build..'worker_status.txt','STOPPED');reaper.Main_OnCommand(40004,0)
   else
    assert(scripts[command],'Unrecognized workflow stage')
    write(build..'worker_status.txt','RUNNING '..command)
    dofile(root..'/tools/reaper/'..scripts[command])
    if command=='auditions'then assert(read(_G.ROSHAN_AUDITION_BUILD..'render_status.txt'):find('^COMPLETE'),'Native auditions did not finish')end
    clear_private_tabs(command)
    write(build..'worker_status.txt','COMPLETE '..command..'; ready for next stage')
   end
  end,debug.traceback)
  if not good then alive=false;write(build..'worker_status.txt','ERROR '..tostring(err))end
 end
 if alive then reaper.defer(cycle)end
end
write(build..'worker_status.txt','READY: isolated staged native-Falcon workflow; Dummy Audio')
reaper.defer(cycle)
