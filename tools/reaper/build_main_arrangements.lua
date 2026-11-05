-- Native UVI MIDI construction and per-part EQ stem rendering; no desktop input.
local path=debug.getinfo(1,'S').source:sub(2):gsub('\\','/')
local root=assert(path:match('^(.*)/tools/reaper/[^/]+$'))
local build=root..'/build/full_arrangements_20261101/'
local package=root..'/assets_src/audio/music/arranged_main_themes_20261101/'
assert(reaper.GetResourcePath():gsub('\\','/'):find('/build/reaper-profile-full',1,true),'Isolated soundtrack worker only')
local ok,mode=reaper.GetAudioDeviceInfo('MODE');assert(ok and mode=='Dummy Audio')
assert(reaper.CountTracks(0)==0,'Protect nonempty projects')
local function write(p,s)local f=assert(io.open(p,'wb'));f:write(s);f:close()end
local function read(p)local f=assert(io.open(p,'rb'));local s=f:read('*a');f:close();return s end
local function db(v)return 10^(v/20)end
local scores=dofile(package..'performance.lua')
local receipt=assert(io.open(build..'native_stems.tsv','w'))
receipt:write('cue\tpart\tnotes\tkeyswitch\tfalcon\teq\n')
local eqlog=assert(io.open(build..'native_eq.tsv','w'))
local function eq_for(tr,spec)
 local fx=reaper.TrackFX_GetEQ(tr,true);assert(fx==1,'Falcon then ReaEQ required')
 for _,b in ipairs({{0,0},{1,0},{2,0},{2,1},{4,0},{5,0}})do reaper.TrackFX_SetEQBandEnabled(tr,fx,b[1],b[2],false)end
 local bell=0
 for _,filter in ipairs(spec)do
  local kind=filter[1]=='hp' and 0 or filter[1]=='bell' and 2 or filter[1]=='lp' and 5 or 4
  local index=kind==2 and bell or 0;if kind==2 then bell=bell+1 end
  assert(reaper.TrackFX_SetEQParam(tr,fx,kind,index,0,filter[2],false))
  if kind~=0 and kind~=5 then assert(reaper.TrackFX_SetEQParam(tr,fx,kind,index,1,db(filter[3]),false))end
  assert(reaper.TrackFX_SetEQParam(tr,fx,kind,index,2,filter[4],false))
  assert(reaper.TrackFX_SetEQBandEnabled(tr,fx,kind,index,true))
 end
 return fx
end
local function gain_envelope(tr,s,t)
 reaper.SetOnlyTrackSelected(tr);reaper.Main_OnCommand(40406,0)
 local env=assert(reaper.GetTrackEnvelopeByName(tr,'Volume'));local scaling=reaper.GetEnvelopeScalingMode(env)
 reaper.DeleteEnvelopePointRange(env,-1,1e9)
 local function pt(time,gain)assert(reaper.InsertEnvelopePoint(env,math.max(0,time),reaper.ScaleToEnvelopeMode(scaling,db(gain)),0,0,false,true))end
 local previous=t.sections[1].gain_db;pt(0,previous)
 for _,sec in ipairs(t.sections)do
  local tm=sec.start_qn*60/s.bpm;pt(tm-.075,previous);pt(tm+.075,sec.gain_db);previous=sec.gain_db
 end
 pt(s.music_end_qn*60/s.bpm+s.tail_seconds,previous)
 reaper.Envelope_SortPoints(env)
end
local function configure(s)
 reaper.SetCurrentBPM(0,s.bpm,true)
 for j=reaper.CountTempoTimeSigMarkers(0)-1,0,-1 do reaper.DeleteTempoTimeSigMarker(0,j)end
 assert(reaper.SetTempoTimeSigMarker(0,-1,0,-1,-1,s.bpm,s.meter[1],s.meter[2],false))
 reaper.GetSetProjectInfo_String(0,'PROJECT_TITLE',s.title..' - full arrangement',true)
 reaper.GetSetProjectInfo_String(0,'PROJECT_AUTHOR','Mermaid Roshan original UVI soundtrack',true)
 for k,v in pairs({PROJECT_SRATE=48000,PROJECT_SRATE_USE=1,RENDER_SETTINGS=0,RENDER_BOUNDSFLAG=2,RENDER_SRATE=48000,RENDER_CHANNELS=2,RENDER_TAILFLAG=0,RENDER_NORMALIZE=0})do reaper.GetSetProjectInfo(0,k,v,true)end
 reaper.GetSetProjectInfo_String(0,'RENDER_FORMAT','ZXZhdxgAAQ==',true)
 reaper.GetSetProjectInfo_String(0,'RENDER_FILE',build,true)
 reaper.SetMediaTrackInfo_Value(reaper.GetMasterTrack(0),'D_VOL',1)
 reaper.GetSet_LoopTimeRange(true,false,s.render_start_qn*60/s.bpm,s.music_end_qn*60/s.bpm+s.tail_seconds,false)
 for j=reaper.CountProjectMarkers(0)-1,0,-1 do reaper.DeleteProjectMarkerByIndex(0,j)end
 for _,sec in ipairs(s.sections)do reaper.AddProjectMarker2(0,true,sec.start_bar*s.beats_per_bar*60/s.bpm,(sec.start_bar+sec.bars)*s.beats_per_bar*60/s.bpm,sec.name,-1,0)end
end
for _,s in ipairs(scores)do
 write(build..'current.txt','Building '..s.id)
 configure(s)
 for i,t in ipairs(s.tracks)do
  assert(t.vendor=='UVI' or(t.vendor=='Acousticsamples' and t.library=='Sunbird'))
  reaper.InsertTrackAtIndex(i-1,false);local tr=reaper.GetTrack(0,i-1)
  reaper.GetSetMediaTrackInfo_String(tr,'P_NAME',t.name,true)
  reaper.GetSetMediaTrackInfo_String(tr,'P_EXT:RoshanPartID',t.id,true)
  reaper.GetSetMediaTrackInfo_String(tr,'P_EXT:RoshanLibrary',t.library,true)
  reaper.SetMediaTrackInfo_Value(tr,'D_VOL',1);reaper.SetMediaTrackInfo_Value(tr,'D_PAN',0)
  gain_envelope(tr,s,t)
  local fx=reaper.TrackFX_AddByName(tr,'VST3i: Falcon (UVI)',false,-1);assert(fx==0)
  assert(reaper.TrackFX_SetNamedConfigParm(tr,fx,'vst_chunk',read(build..t.state_id..'.chunk.b64')))
  local eq=eq_for(tr,t.eq)
  local item=reaper.CreateNewMIDIItemInProj(tr,0,s.music_end_qn*60/s.bpm,false)
  reaper.SetMediaItemInfo_Value(item,'D_FADEINLEN',0);reaper.SetMediaItemInfo_Value(item,'D_FADEOUTLEN',0)
  local take=assert(reaper.GetActiveTake(item));reaper.GetSetMediaItemTakeInfo_String(take,'P_NAME',s.title..' | '..t.name,true)
  if t.keyswitch then
   local q=s.render_start_qn+.02
   assert(reaper.MIDI_InsertNote(take,false,false,reaper.MIDI_GetPPQPosFromProjQN(take,q),reaper.MIDI_GetPPQPosFromProjQN(take,q+.05),0,t.keyswitch,100,true))
  end
  for _,n in ipairs(t.notes)do assert(reaper.MIDI_InsertNote(take,false,false,reaper.MIDI_GetPPQPosFromProjQN(take,n.qn),reaper.MIDI_GetPPQPosFromProjQN(take,n.qn+n.duration_qn),0,n.pitch,n.velocity,true))end
  reaper.MIDI_Sort(take);local _,nn=reaper.MIDI_CountEvts(take);assert(nn==t.native_midi_notes)
  for p=0,reaper.TrackFX_GetNumParams(tr,eq)-1 do
   local _,pn=reaper.TrackFX_GetParamName(tr,eq,p,'');local _,v=reaper.TrackFX_GetFormattedParamValue(tr,eq,p,'');eqlog:write(s.id..'\t'..t.id..'\t'..p..'\t'..pn..'\t'..v..'\n')
  end
  eqlog:flush();receipt:write(s.id..'\t'..t.id..'\t'..nn..'\t'..(t.keyswitch or '')..'\tFalcon\tReaEQ\n');receipt:flush()
 end
 for i,t in ipairs(s.tracks)do
  for j=0,reaper.CountTracks(0)-1 do reaper.SetMediaTrackInfo_Value(reaper.GetTrack(0,j),'B_MUTE',j==i-1 and 0 or 1)end
  local file=t.stem_file:gsub('%.wav$','')
  write(build..'current.txt','Rendering '..file)
  local f=io.open(build..file..'.wav','rb');if f then f:close();assert(os.rename(build..file..'.wav',build..file..'.old-'..os.time()..'.wav'))end
  reaper.GetSetProjectInfo_String(0,'RENDER_PATTERN',file,true)
  reaper.Main_OnCommand(42230,0)
  local tr=reaper.GetTrack(0,i-1);local ok,state=reaper.TrackFX_GetNamedConfigParm(tr,0,'vst_chunk');assert(ok)
  write(build..s.id..'__'..t.id..'_rendered.chunk.b64',state)
 end
 for j=0,reaper.CountTracks(0)-1 do reaper.SetMediaTrackInfo_Value(reaper.GetTrack(0,j),'B_MUTE',0)end
 reaper.Main_SaveProjectEx(0,build..s.id..'_source.rpp',8)
 for j=reaper.CountTracks(0)-1,0,-1 do reaper.DeleteTrack(reaper.GetTrack(0,j))end
end
receipt:close();eqlog:close();write(build..'current.txt','STEMS COMPLETE: native EQ and score render; balance measurement next')
