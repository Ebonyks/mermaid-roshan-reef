-- Short private instrument tests only. No user project or audio device is used.
local src=debug.getinfo(1,'S').source:sub(2):gsub('\\','/')
local root=assert(src:match('^(.*)/tools/reaper/[^/]+$'))
local build=_G.ROSHAN_AUDITION_BUILD or root..'/build/dkc_instrument_auditions_20261101/'
local function write(p,s)local f=assert(io.open(p,'wb'));f:write(s);f:close()end
local function read(p)local f=assert(io.open(p,'rb'));local s=f:read('*a');f:close();return s end
assert(reaper.GetResourcePath():gsub('\\','/'):find('/build/reaper-profile-audition',1,true),'Private profile required')
assert(reaper.CountTracks(0)==0,'Protect nonempty user projects')
reaper.Audio_Init();local ok,mode=reaper.GetAudioDeviceInfo('MODE');assert(ok and mode=='Dummy Audio')
local tests=dofile(build..'auditions.lua')
local receipt=assert(io.open(build..'native_receipt.tsv','w'));receipt:write('id\tnotes\tstate_recalled\tproject\n')
local function run()
 for _,s in ipairs(tests)do
  assert(s.id:match('^[a-z0-9_]+$'))
  write(build..'render_status.txt','Rendering '..s.id)
  reaper.SetCurrentBPM(0,s.bpm,true)
  for j=reaper.CountTempoTimeSigMarkers(0)-1,0,-1 do reaper.DeleteTempoTimeSigMarker(0,j)end
  assert(reaper.SetTempoTimeSigMarker(0,-1,0,-1,-1,s.bpm,4,4,false))
  reaper.InsertTrackAtIndex(0,false);local tr=reaper.GetTrack(0,0)
  reaper.GetSetMediaTrackInfo_String(tr,'P_NAME',s.id,true)
  reaper.SetMediaTrackInfo_Value(tr,'D_VOL',0.10)
  local fx=reaper.TrackFX_AddByName(tr,'VST3i: Falcon (UVI)',false,-1);assert(fx==0)
  assert(reaper.TrackFX_SetNamedConfigParm(tr,fx,'vst_chunk',read(root..'/'..s.state)))
  local eq=reaper.TrackFX_GetEQ(tr,true);assert(eq==1)
  for _,b in ipairs({{0,0},{1,0},{2,0},{2,1},{4,0},{5,0}})do reaper.TrackFX_SetEQBandEnabled(tr,eq,b[1],b[2],false)end
  local bell=0
  for _,f in ipairs(s.eq)do
   local kind=f[1]=='hp' and 0 or f[1]=='bell' and 2 or f[1]=='lp' and 5 or 4
   local idx=kind==2 and bell or 0;if kind==2 then bell=bell+1 end
   assert(reaper.TrackFX_SetEQParam(tr,eq,kind,idx,0,f[2],false))
   if kind~=0 and kind~=5 then assert(reaper.TrackFX_SetEQParam(tr,eq,kind,idx,1,10^(f[3]/20),false))end
   assert(reaper.TrackFX_SetEQParam(tr,eq,kind,idx,2,f[4],false));assert(reaper.TrackFX_SetEQBandEnabled(tr,eq,kind,idx,true))
  end
  local ending=(s.end_qn*60/s.bpm)+s.tail_seconds
  local item=reaper.CreateNewMIDIItemInProj(tr,0,ending,false)
  reaper.SetMediaItemInfo_Value(item,'D_FADEINLEN',0);reaper.SetMediaItemInfo_Value(item,'D_FADEOUTLEN',0)
  local take=assert(reaper.GetActiveTake(item))
  for _,n in ipairs(s.notes)do assert(reaper.MIDI_InsertNote(take,false,false,reaper.MIDI_GetPPQPosFromProjQN(take,n.qn),reaper.MIDI_GetPPQPosFromProjQN(take,n.qn+n.duration_qn),0,n.pitch,n.velocity,true))end
  reaper.MIDI_Sort(take);local _,nn=reaper.MIDI_CountEvts(take);assert(nn==#s.notes)
  for k,v in pairs({PROJECT_SRATE=48000,PROJECT_SRATE_USE=1,RENDER_SETTINGS=0,RENDER_BOUNDSFLAG=2,RENDER_SRATE=48000,RENDER_CHANNELS=2,RENDER_TAILFLAG=0,RENDER_NORMALIZE=0})do reaper.GetSetProjectInfo(0,k,v,true)end
  reaper.GetSetProjectInfo_String(0,'RENDER_FORMAT','ZXZhdxgAAQ==',true)
  reaper.GetSetProjectInfo_String(0,'RENDER_FILE',build,true);reaper.GetSetProjectInfo_String(0,'RENDER_PATTERN',s.id,true)
  reaper.SetMediaTrackInfo_Value(reaper.GetMasterTrack(0),'D_VOL',1)
  reaper.GetSet_LoopTimeRange(true,false,0,ending,false)
  assert(not io.open(build..s.id..'.wav','rb'),'Never overwrite an existing audition')
  reaper.Main_OnCommand(42230,0)
  local state_ok,state=reaper.TrackFX_GetNamedConfigParm(tr,0,'vst_chunk');assert(state_ok and #state>0)
  write(build..s.id..'_recalled.chunk.b64',state)
  reaper.Main_SaveProjectEx(0,build..s.id..'.rpp',8)
  receipt:write(s.id..'\t'..nn..'\ttrue\t'..s.id..'.rpp\n');receipt:flush()
  reaper.DeleteTrack(tr)
 end
 reaper.Main_SaveProjectEx(0,build..'audition_worker_empty.rpp',8)
 write(build..'render_status.txt','COMPLETE '..#tests..' native UVI auditions; no full compositions')
end
local ok,err=xpcall(run,debug.traceback);receipt:close()
if not ok then write(build..'render_status.txt','ERROR '..tostring(err))end
if ok and not _G.ROSHAN_KEEP_WORKER then reaper.Main_OnCommand(40004,0)end
