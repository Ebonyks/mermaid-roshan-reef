-- Isolated native RetroPlug setup/recall check. No keyboard or mouse control.
local file=debug.getinfo(1,'S').source:sub(2):gsub('\\','/')
local root=assert(file:match('^(.*)/tools/reaper/[^/]+$'))
assert(reaper.GetResourcePath():gsub('\\','/'):find('/build/reaper-profile-retroplug',1,true),'Isolated worker required')
local started=assert(io.open(root..'/build/retroplug_20261101/native_started.txt','w'));started:write(reaper.GetResourcePath());started:close()
local cfg=dofile(root..'/build/retroplug_20261101/request.lua')
local function write(path,data)local f=assert(io.open(path,'wb'));f:write(data);f:close()end
local function run()
 assert(reaper.CountTracks(0)==0,'Protect nonempty project')
 reaper.Audio_Init();local ok,mode=reaper.GetAudioDeviceInfo('MODE');assert(ok and mode=='Dummy Audio')
 local name,ident
 for i=0,10000 do local yes,n,id=reaper.EnumInstalledFX(i);if not yes then break end;if n:lower():find('retroplug',1,true)then name=n;ident=id;break end end
 assert(name,'RetroPlug was not discovered by native REAPER scan')
 reaper.InsertTrackAtIndex(0,true);local tr=reaper.GetTrack(0,0)
 reaper.GetSetMediaTrackInfo_String(tr,'P_NAME','LSDJ - 4-channel Game Boy source',true)
 reaper.SetMediaTrackInfo_Value(tr,'I_NCHAN',8);reaper.SetMediaTrackInfo_Value(tr,'B_MAINSEND',0)
 local fx=reaper.TrackFX_AddByName(tr,name,false,-1);assert(fx==0,'Native RetroPlug creation failed')
 local _,ins,outs=reaper.TrackFX_GetIOSize(tr,fx);assert(outs>=8,'Eight split output pins required')
 for pin=0,outs-1 do reaper.TrackFX_SetPinMappings(tr,fx,1,pin,pin<8 and (1<<pin) or 0,0)end
 local names={'Pulse 1','Pulse 2','Wave','Noise'}
 for i,n in ipairs(names)do
  reaper.InsertTrackAtIndex(i,true);local dest=reaper.GetTrack(0,i)
  reaper.GetSetMediaTrackInfo_String(dest,'P_NAME','GB '..n,true)
  local send=reaper.CreateTrackSend(tr,dest);assert(send>=0)
  reaper.SetTrackSendInfo_Value(tr,0,send,'I_SRCCHAN',(i-1)*2)
  reaper.SetTrackSendInfo_Value(tr,0,send,'I_DSTCHAN',0)
  reaper.SetTrackSendInfo_Value(tr,0,send,'I_MIDIFLAGS',31)
  reaper.SetMediaTrackInfo_Value(dest,'D_VOL',0.25)
 end
 reaper.SetCurrentBPM(0,104,true)
 reaper.SetMasterTrackVisibility(1)
 reaper.GetSetProjectInfo(0,'PROJECT_SRATE',48000,true)
 reaper.GetSetProjectInfo(0,'PROJECT_SRATE_USE',1,true)
 reaper.GetSetProjectNotes(0,true,'Ember King: owner-directed chiptune. Blank writing desk, not a composed song. RetroPlug/LSDJ is an explicit exception to UVI-only. Four stereo Game Boy returns; start at conservative return gain. Original LSDJ archive and ROM preserved. Choose hook/form/instrument roles before composing. Configure and verify LSDJ/RetroPlug sync before timed song rendering.')
 local yes,chunk=reaper.TrackFX_GetNamedConfigParm(tr,fx,'vst_chunk');assert(yes and #chunk>0,'Plugin state missing')
 write(cfg.chunk,chunk)
 reaper.Main_SaveProjectEx(0,cfg.project,8)
 write(cfg.receipt,'status\tPASS\nreaper\t'..reaper.GetAppVersion()..'\nfx\t'..name..'\nidentifier\t'..ident..'\ninputs\t'..ins..'\noutputs\t'..outs..'\ntracks\t'..reaper.CountTracks(0)..'\nstate_base64_bytes\t'..#chunk..'\naudio\t'..mode..'\nproject\t'..cfg.project..'\n')
end
local ok,err=xpcall(run,debug.traceback)
if not ok then write(cfg.receipt,'status\tFAIL\nerror\t'..tostring(err)..'\n')end
reaper.Main_OnCommand(40004,0)
