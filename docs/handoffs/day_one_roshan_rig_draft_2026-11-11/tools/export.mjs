// Writes the catalogue (intent + fitted gain) and the Rigby animation objects for the fitted clips.
import { readFile, writeFile } from 'node:fs/promises';
import { index } from './lib.mjs';
import { CLIPS } from './clips.mjs';
const fit=Object.fromEntries(JSON.parse(await readFile(new URL('fit.json',import.meta.url),'utf8')).map(f=>[f.name,f]));
const EASE={bezier:[1/3,0,2/3,1]};
const MARGIN=0.95; // stay inside the measured limit
const animations=[],catalogue=[];
for(const clip of CLIPS){
  const f=fit[clip.name];const gain=+(Math.min(1,f.gain)*(f.gain<1?MARGIN:1)).toFixed(3);
  const bones=Object.entries(clip.keys).map(([bone,keys])=>({bone:index[bone],rotate:keys.map(([time,v],i)=>{
    const key={time,value:+(v*gain).toFixed(3)};
    if(i+1<keys.length&&keys[i+1][1]!==v)key.curve=EASE;return key;})})).sort((a,b)=>a.bone-b.bone);
  for(const track of bones){const last=track.rotate.at(-1);if(last.time<clip.duration)track.rotate.push({time:clip.duration,value:last.value});}
  animations.push({name:'D1 '+clip.name,duration:clip.duration,bones});
  const peak={};for(const [b,k] of Object.entries(clip.keys))peak[b]=k.reduce((m,[,v])=>Math.abs(v)>Math.abs(m)?v:m,0);
  catalogue.push({name:clip.name,rig_animation:'D1 '+clip.name,group:clip.group,loop:clip.loop,duration:clip.duration,
    delivered_gain:gain,status:f.gain>=1?'FULL_ON_CURRENT_RIG':f.gain>=.6?'REDUCED_ON_CURRENT_RIG':'NEEDS_RIG_UPGRADE',
    intent_strain:f.intent,fitted_strain:f.fitted,markers:clip.markers??[],prop:clip.prop??null,needs:clip.need??null,
    intent_peak_degrees:peak,intent_keys:clip.keys});
}
await writeFile(new URL('animations.json',import.meta.url),JSON.stringify(animations));
await writeFile(new URL('day_one_clips.json',import.meta.url),JSON.stringify({
  schema:'roshan.day_one.clips.draft/1',rig:'roshan_arm_rebound.rigby (17 bones, quarter-right master)',
  units:'rotation deltas in degrees from the painted rest pose; smoothstep between keys (Rigby bezier 1/3,0,2/3,1)',
  gate:'visible-triangle strain within 0.82-1.18 at key and mid-key samples in Original, Ballet and Magician (project floor is 0.80-1.20)',
  clips:catalogue},null,1));
console.log(catalogue.map(c=>c.status).reduce((m,s)=>(m[s]=(m[s]??0)+1,m),{}));
