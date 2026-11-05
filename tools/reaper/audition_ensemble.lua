-- Private native instrument audition worker. Never targets an existing user project.
local src=debug.getinfo(1,'S').source:sub(2):gsub('\\','/')
local root=assert(src:match('^(.*)/tools/reaper/[^/]+$'))
local build=root..'/build/dkc_instrument_auditions_20261101/'
local function write(p,s)local f=assert(io.open(p,'wb'));f:write(s);f:close()end
local function read(p)local f=io.open(p,'rb');if not f then return nil end;local s=f:read('*a');f:close();return s end
assert(reaper.GetResourcePath():gsub('\\','/'):find('/build/reaper-profile-audition',1,true),'Isolated audition profile required')
assert(reaper.CountTracks(0)==0,'Protect nonempty projects')
reaper.Audio_Init();local ok,mode=reaper.GetAudioDeviceInfo('MODE');assert(ok and mode=='Dummy Audio')
reaper.InsertTrackAtIndex(0,true);local tr=reaper.GetTrack(0,0)
reaper.GetSetMediaTrackInfo_String(tr,'P_NAME','Private UVI instrument audition',true)
local fx=reaper.TrackFX_AddByName(tr,'VST3i: Falcon (UVI)',false,-1);assert(fx==0)
assert(reaper.TrackFX_SetNamedConfigParm(tr,fx,'vst_chunk',assert(read(root..'/build/warm_ensemble_20261101/jazz_brushed_kit_1.chunk.b64'))))
reaper.SetMediaTrackInfo_Value(tr,'D_VOL',0.12)
reaper.TrackFX_Show(tr,fx,3)
write(build..'worker_status.txt','READY: isolated Falcon preset browser; Dummy Audio; no user project loaded')
local function capture(id)
 assert(id:match('^[a-z0-9_]+$'))
 local ok,state=reaper.TrackFX_GetNamedConfigParm(tr,fx,'vst_chunk');assert(ok and #state>0)
 write(build..id..'.chunk.b64',state);write(build..'worker_status.txt','CAPTURED '..id..' '..#state..' base64 bytes')
end
local alive=true
local function cycle()
 local command=read(build..'command.txt')
 if command and #command>0 then
  write(build..'command.txt','')
  local op,arg=command:match('^(%S+)%s*(.-)%s*$')
  local ok,err=xpcall(function()
   if op=='capture' then capture(arg)
   elseif op=='hide' then reaper.TrackFX_Show(tr,fx,2);write(build..'worker_status.txt','Browser hidden; worker ready')
   elseif op=='show' then reaper.TrackFX_Show(tr,fx,3)
   elseif op=='workflow' then
    assert(arg=='profiled_tests','Only the named private test workflow is authorized')
    reaper.TrackFX_Show(tr,fx,2);reaper.DeleteTrack(tr);alive=false
    dofile(root..'/tools/reaper/profiled_test_workflow.lua')
   elseif op=='stop' then
    reaper.Main_SaveProjectEx(0,build..'browser_checkpoint.rpp',8);alive=false;write(build..'worker_status.txt','STOPPED');reaper.Main_OnCommand(40004,0)
   else error('Unknown command '..tostring(op))end
  end,debug.traceback)
  if not ok then write(build..'worker_status.txt','ERROR '..tostring(err))end
 end
 if alive then reaper.defer(cycle)end
end
reaper.defer(cycle)
