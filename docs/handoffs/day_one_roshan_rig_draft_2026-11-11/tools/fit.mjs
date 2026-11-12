import { writeFile } from 'node:fs/promises';
import { worstAll } from './lib.mjs';
import { CLIPS } from './clips.mjs';
const ss=u=>u*u*(3-2*u);
export const at=(keys,t)=>{if(t<=keys[0][0])return keys[0][1];for(let i=1;i<keys.length;i++){if(t<=keys[i][0]){const [a,va]=keys[i-1],[b,vb]=keys[i];return va+(vb-va)*ss((t-a)/(b-a));}}return keys.at(-1)[1];};
const out=[];
for(const clip of CLIPS){
  const times=new Set();for(const k of Object.values(clip.keys))for(const [t] of k)times.add(t);
  const ts=[...times].sort((a,b)=>a-b);const sample=[...ts];for(let i=1;i<ts.length;i++)sample.push((ts[i]+ts[i-1])/2);
  const test=g=>{let low=1,high=1,flips=0,worst='';for(const t of sample){const d={};for(const [b,k] of Object.entries(clip.keys))d[b]=at(k,t)*g;const r=worstAll(d);if(r.low<low||r.high>high)worst=r.worst;low=Math.min(low,r.low);high=Math.max(high,r.high);flips+=r.flips;}return {low,high,flips,worst,pass:low>=.82&&high<=1.18&&!flips};};
  let full=test(1),g=1,res=full;
  if(!full.pass){let lo=0,hi=1;for(let i=0;i<7;i++){const m=(lo+hi)/2;if(test(m).pass)lo=m;else hi=m;}g=Math.floor(lo*100)/100;res=test(g);}
  out.push({name:clip.name,gain:g,intent:{low:+full.low.toFixed(3),high:+full.high.toFixed(3),flips:full.flips,limiter:full.worst},fitted:{low:+res.low.toFixed(3),high:+res.high.toFixed(3)}});
  console.log(clip.name.padEnd(26),'gain',g.toFixed(2),'intent',full.low.toFixed(2),full.high.toFixed(2),'flips',full.flips,full.worst,'| fitted',res.low.toFixed(3),res.high.toFixed(3));
}
await writeFile(new URL('fit.json',import.meta.url),JSON.stringify(out,null,1));
