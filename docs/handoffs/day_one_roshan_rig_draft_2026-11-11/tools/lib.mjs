import { readFile } from 'node:fs/promises';
import { Pose, Skeleton } from '@rigby/src/core/index.js';
const here=new URL('.',import.meta.url);
export const skeleton=Skeleton.fromJson(await readFile(new URL('rig/project.json',here),'utf8'));
export const visible=JSON.parse(await readFile(new URL('scene/visible_triangles.json',here),'utf8'));
export const SKINS=['default','Ballet','Magician'];
export const index=Object.fromEntries(skeleton.bones.map((b,i)=>[b.name,i]));
const rest={};
for(const skin of SKINS){skeleton.skin=skin==='default'?null:skin;rest[skin]=new Pose(skeleton).quads(skeleton);}
// strain of one pose (deltas: {bone:deg}) in one skin
export function strain(deltas,skin){
  skeleton.skin=skin==='default'?null:skin;
  const pose=new Pose(skeleton);pose.reset(skeleton);
  for(const [b,d] of Object.entries(deltas))pose.local[index[b]].rotation+=d;
  pose.updateWorld(skeleton);
  const cur=pose.quads(skeleton);let low=1,high=1,flips=0,worst='';
  rest[skin].forEach((part,i)=>{
    const slot=skeleton.slots[part.slot].name;const vis=visible[skin][slot]??[];const act=cur[i];
    for(const t of vis){
      const [a,b,c]=part.triangles.slice(t*3,t*3+3);
      const m=(p,q)=>[p[0]-q[0],p[1]-q[1]];
      const u=m(part.positions[b],part.positions[a]),v=m(part.positions[c],part.positions[a]);
      const p=m(act.positions[b],act.positions[a]),q=m(act.positions[c],act.positions[a]);
      const base=u[0]*v[1]-u[1]*v[0];if(Math.abs(base)<1e-9)continue;
      const A=(p[0]*v[1]-q[0]*u[1])/base,B=(q[0]*u[0]-p[0]*v[0])/base,C=(p[1]*v[1]-q[1]*u[1])/base,D=(q[1]*u[0]-p[1]*v[0])/base;
      const det=A*D-B*C,tr=A*A+B*B+C*C+D*D;
      const hi=Math.sqrt((tr+Math.sqrt(Math.max(0,tr*tr-4*det*det)))/2),lo=Math.abs(det)/hi;
      if(lo<low||hi>high)worst=slot;low=Math.min(low,lo);high=Math.max(high,hi);if(det<=0)flips++;
    }});
  return {low,high,flips,worst};
}
export function worstAll(deltas){let low=1,high=1,flips=0,worst='';for(const s of SKINS){const r=strain(deltas,s);if(r.low<low||r.high>high)worst=s+':'+r.worst;low=Math.min(low,r.low);high=Math.max(high,r.high);flips+=r.flips;}return {low,high,flips,worst,pass:low>=.8&&high<=1.2&&flips===0};}
