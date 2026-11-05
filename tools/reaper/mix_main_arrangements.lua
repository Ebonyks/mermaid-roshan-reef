-- Balance native MIDI sessions and create reproducible printed-stem mixes.
local path=debug.getinfo(1,'S').source:sub(2):gsub('\\','/')
local root=assert(path:match('^(.*)/tools/reaper/[^/]+$'))
local build=root..'/build/full_arrangements_20261101/'
local package=root..'/assets_src/audio/music/arranged_main_themes_20261101/'
assert(reaper.GetResourcePath():gsub('\\','/'):find('/build/reaper-profile-full',1,true))
reaper.Audio_Init()
local ok,mode=reaper.GetAudioDeviceInfo('MODE');assert(ok and mode=='Dummy Audio',tostring(ok)..':'..tostring(mode))
assert(reaper.CountTracks(0)==0,'Empty private worker required')
local scores=dofile(package..'performance.lua');local gains=dofile(build..'mix_gains.lua')
local function db(x)return 10^(x/20)end
local function write(path,s)local f=assert(io.open(path,'w'));f:write(s);f:close()end
local log=assert(io.open(build..'mix_controls.tsv','w'))
local function formatted(tr,fx,p,target)
 local lo,hi=0,1
 for i=1,32 do
  local x=(lo+hi)/2;reaper.TrackFX_SetParamNormalized(tr,fx,p,x)
  local _,text=reaper.TrackFX_GetFormattedParamValue(tr,fx,p,'');local n=tonumber(text:match('[-+]?%d+%.?%d*'))
  assert(n,'Non-numeric effect control '..p..': '..text)
  if math.abs(n-target)<.01 then return end
  if n<target then lo=x else hi=x end
 end
end
local function disable_bands(tr,fx)
 for _,b in ipairs({{0,0},{1,0},{2,0},{2,1},{4,0},{5,0}})do reaper.TrackFX_SetEQBandEnabled(tr,fx,b[1],b[2],false)end
end
local function setup(s)
 reaper.SetCurrentBPM(0,s.bpm,true)
 for i=reaper.CountTempoTimeSigMarkers(0)-1,0,-1 do reaper.DeleteTempoTimeSigMarker(0,i)end
 assert(reaper.SetTempoTimeSigMarker(0,-1,0,-1,-1,s.bpm,s.meter[1],s.meter[2],false))
 for k,v in pairs({PROJECT_SRATE=48000,PROJECT_SRATE_USE=1,RENDER_SETTINGS=0,RENDER_BOUNDSFLAG=2,RENDER_SRATE=48000,RENDER_CHANNELS=2,RENDER_TAILFLAG=0,RENDER_NORMALIZE=0})do reaper.GetSetProjectInfo(0,k,v,true)end
 reaper.GetSetProjectInfo_String(0,'PROJECT_TITLE',s.title..' - full arrangement',true)
 reaper.GetSetProjectInfo_String(0,'RENDER_FORMAT','ZXZhdxgAAQ==',true)
 reaper.GetSetProjectInfo_String(0,'RENDER_FILE',build,true)
 reaper.GetSet_LoopTimeRange(true,false,s.render_start_qn*60/s.bpm,s.music_end_qn*60/s.bpm+s.tail_seconds,false)
 reaper.SetMediaTrackInfo_Value(reaper.GetMasterTrack(0),'D_VOL',1)
 for i=reaper.CountProjectMarkers(0)-1,0,-1 do reaper.DeleteProjectMarkerByIndex(0,i)end
 for _,sec in ipairs(s.sections)do reaper.AddProjectMarker2(0,true,sec.start_bar*s.beats_per_bar*60/s.bpm,(sec.start_bar+sec.bars)*s.beats_per_bar*60/s.bpm,sec.name,-1,0)end
 reaper.SetEditCurPos(s.render_start_qn*60/s.bpm,false,false)
end
local function room_and_master(s)
 reaper.InsertTrackAtIndex(reaper.CountTracks(0),false);local room=reaper.GetTrack(0,reaper.CountTracks(0)-1)
 reaper.GetSetMediaTrackInfo_String(room,'P_NAME','Shared room - quiet wet return',true)
 local rv=reaper.TrackFX_AddByName(room,'ReaVerbate (Cockos)',false,-1);assert(rv==0)
 reaper.TrackFX_SetParam(room,rv,0,1);reaper.TrackFX_SetParam(room,rv,1,0)
 formatted(room,rv,2,30);formatted(room,rv,3,72)
 reaper.TrackFX_SetParam(room,rv,4,.78);formatted(room,rv,5,18)
 formatted(room,rv,6,6200);formatted(room,rv,7,220)
 for i,t in ipairs(s.tracks)do
  local tr=reaper.GetTrack(0,i-1)
  if t.room_send_db>-50 then
   local send=reaper.CreateTrackSend(tr,room);assert(send>=0)
   reaper.SetTrackSendInfo_Value(tr,0,send,'D_VOL',db(t.room_send_db))
   reaper.SetTrackSendInfo_Value(tr,0,send,'I_SENDMODE',0)
   reaper.SetTrackSendInfo_Value(tr,0,send,'I_MIDIFLAGS',31)
  end
 end
 local master=reaper.GetMasterTrack(0)
 local hp=reaper.TrackFX_AddByName(master,'ReaEQ (Cockos)',false,-1);assert(hp==0)
 disable_bands(master,hp);reaper.TrackFX_SetEQParam(master,hp,0,0,0,28,false);reaper.TrackFX_SetEQBandEnabled(master,hp,0,0,true)
 local comp=reaper.TrackFX_AddByName(master,'ReaComp (Cockos)',false,-1);assert(comp==1)
 reaper.TrackFX_SetParam(master,comp,0,db(-23))
 reaper.TrackFX_SetParam(master,comp,1,(1.35-1)/99)
 reaper.TrackFX_SetParam(master,comp,2,.06);reaper.TrackFX_SetParam(master,comp,3,.028)
 reaper.TrackFX_SetParam(master,comp,4,0);reaper.TrackFX_SetParam(master,comp,10,0);reaper.TrackFX_SetParam(master,comp,11,1)
 reaper.TrackFX_SetParam(master,comp,15,0);reaper.TrackFX_SetParam(master,comp,16,0)
 formatted(master,comp,7,90);formatted(master,comp,14,3)
 local gain=reaper.TrackFX_AddByName(master,'ReaEQ (Cockos)',false,-1);assert(gain==2)
 disable_bands(master,gain)
 reaper.TrackFX_SetNamedConfigParm(master,gain,'renamed_name','Album gain - unity until mastering')
 local limiter=reaper.TrackFX_AddByName(master,'ReaLimit (Cockos)',false,-1);assert(limiter==3)
 reaper.TrackFX_SetEnabled(master,limiter,false)
 for _,pair in ipairs({{room,rv,'Room'},{master,comp,'Glue'},{master,limiter,'Limiter'}})do
  for p=0,reaper.TrackFX_GetNumParams(pair[1],pair[2])-1 do
   local _,name=reaper.TrackFX_GetParamName(pair[1],pair[2],p,'');local _,v=reaper.TrackFX_GetFormattedParamValue(pair[1],pair[2],p,'')
   log:write(s.id..'\t'..pair[3]..'\t'..p..'\t'..name..'\t'..v..'\n')
  end
 end
 log:flush();return master,comp
end
for _,s in ipairs(scores)do
 write(build..'current.txt','Balancing MIDI composition '..s.id)
 reaper.Main_OnCommand(40859,0);reaper.Main_openProject(build..s.id..'_source.rpp')
 assert(reaper.CountTracks(0)==#s.tracks)
 setup(s)
 for i,t in ipairs(s.tracks)do
  local tr=reaper.GetTrack(0,i-1);reaper.SetMediaTrackInfo_Value(tr,'D_VOL',assert(gains[s.id][t.id]));reaper.SetMediaTrackInfo_Value(tr,'D_PAN',t.pan)
 end
 room_and_master(s)
 reaper.Main_SaveProjectEx(0,build..s.id..'_composition.rpp',8)
 -- Fixed, native printed performances make before/after mastering comparison exact.
 reaper.Main_OnCommand(40859,0);assert(reaper.CountTracks(0)==0)
 setup(s)
 for i,t in ipairs(s.tracks)do
  reaper.InsertTrackAtIndex(i-1,false);local tr=reaper.GetTrack(0,i-1)
  reaper.GetSetMediaTrackInfo_String(tr,'P_NAME',t.name..' [native EQ print]',true)
  reaper.GetSetMediaTrackInfo_String(tr,'P_EXT:RoshanPartID',t.id,true)
  reaper.GetSetMediaTrackInfo_String(tr,'P_EXT:RoshanLibrary',t.library,true)
  reaper.SetMediaTrackInfo_Value(tr,'D_VOL',assert(gains[s.id][t.id]));reaper.SetMediaTrackInfo_Value(tr,'D_PAN',t.pan)
  local source=reaper.PCM_Source_CreateFromFile(build..t.stem_file);assert(source)
  local item=reaper.AddMediaItemToTrack(tr);local take=reaper.AddTakeToMediaItem(item)
  reaper.SetMediaItemTake_Source(take,source)
  reaper.SetMediaItemInfo_Value(item,'D_POSITION',s.render_start_qn*60/s.bpm)
  reaper.SetMediaItemInfo_Value(item,'D_LENGTH',s.duration_seconds)
  reaper.SetMediaItemInfo_Value(item,'D_FADEINLEN',0);reaper.SetMediaItemInfo_Value(item,'D_FADEOUTLEN',0)
 end
 local master,comp=room_and_master(s)
 for _,pass in ipairs({'mix_raw','mix_glue'})do
  reaper.TrackFX_SetEnabled(master,comp,pass=='mix_glue')
  local name=s.id..'_'..pass..'_v2';write(build..'current.txt','Rendering '..name)
  local f=io.open(build..name..'.wav','rb');if f then f:close();assert(os.rename(build..name..'.wav',build..name..'.old-'..os.time()..'.wav'))end
  reaper.GetSetProjectInfo_String(0,'RENDER_PATTERN',name,true);reaper.Main_OnCommand(42230,0)
 end
 reaper.Main_SaveProjectEx(0,build..s.id..'_mix.rpp',8)
end
log:close();write(build..'current.txt','MIXES COMPLETE: full-song bus and final mastering assessment next')
