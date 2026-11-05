-- Control the acoustic-guitar and percussion transients before the gentle album limiter.
return function(score)
 if score.id~='castle' then return end
 local caps={foreground=-10.5,kit=-11,percussion=-12}
 local function display(tr,fx,param,target)
  local lo,hi=0,1
  for i=1,36 do
   local x=(lo+hi)/2;reaper.TrackFX_SetParamNormalized(tr,fx,param,x)
   local _,v=reaper.TrackFX_GetFormattedParamValue(tr,fx,param,'');local n=assert(tonumber(v:match('[-+]?%d+%.?%d*')))
   if math.abs(n-target)<.011 then return v end
   if n<target then lo=x else hi=x end
  end
 end
 for i=0,reaper.CountTracks(0)-1 do
  local tr=reaper.GetTrack(0,i);local _,group=reaper.GetSetMediaTrackInfo_String(tr,'P_EXT:RoshanGroupID','',false)
  if caps[group] and reaper.TrackFX_GetCount(tr)==0 then
   local fx=reaper.TrackFX_AddByName(tr,'ReaLimit (Cockos)',false,-1);assert(fx==0)
   local fader=reaper.GetMediaTrackInfo_Value(tr,'D_VOL');local threshold=caps[group]-20*math.log(fader,10)
   display(tr,fx,0,threshold);display(tr,fx,1,threshold)
   reaper.TrackFX_SetParamNormalized(tr,fx,2,10^((6-30)/20)) -- 30 dB/sec return: ~100 ms for a 3 dB peak.
   reaper.TrackFX_SetNamedConfigParm(tr,fx,'renamed_name','Light transient guard - '..group)
  end
 end
end
