// Dense check of the written rig: every "D1 " animation, 30 fps, all three looks, through Rigby's own Pose.apply.
import { readFile, writeFile } from 'node:fs/promises';
import { Pose, Skeleton } from '@rigby/src/core/index.js';
const [projectPath,visiblePath,outPath]=process.argv.slice(2);
const sk=Skeleton.fromJson(await readFile(projectPath,'utf8'));
const visible=JSON.parse(await readFile(visiblePath,'utf8'));
const report=[];let allPass=true;
for(const skin of ['default','Ballet','Magician']){
  sk.skin=skin==='default'?null:skin;
  const rest=new Pose(sk).quads(sk);const pose=new Pose(sk);
  for(const anim of sk.animations.filter(a=>a.name.startsWith('D1 '))){
    let low=1,high=1,flips=0,frames=0;
    const n=Math.round(anim.duration*30);
    for(let f=0;f<=n;f++){
      pose.reset(sk);pose.apply(sk,anim,Math.min(f/30,anim.duration),1);pose.updateWorld(sk);frames++;
      const cur=pose.quads(sk);
      rest.forEach((part,i)=>{
        const vis=visible[skin][sk.slots[part.slot].name]??[];const act=cur[i];
        for(const t of vis){
          const [a,b,c]=part.triangles.slice(t*3,t*3+3);
          const m=(p,q)=>[p[0]-q[0],p[1]-q[1]];
          const u=m(part.positions[b],part.positions[a]),v=m(part.positions[c],part.positions[a]);
          const p=m(act.positions[b],act.positions[a]),q=m(act.positions[c],act.positions[a]);
          const base=u[0]*v[1]-u[1]*v[0];if(Math.abs(base)<1e-9)continue;
          const A=(p[0]*v[1]-q[0]*u[1])/base,B=(q[0]*u[0]-p[0]*v[0])/base,C=(p[1]*v[1]-q[1]*u[1])/base,D=(q[1]*u[0]-p[1]*v[0])/base;
          const det=A*D-B*C,tr=A*A+B*B+C*C+D*D;
          const hi=Math.sqrt((tr+Math.sqrt(Math.max(0,tr*tr-4*det*det)))/2),lo=Math.abs(det)/hi;
          low=Math.min(low,lo);high=Math.max(high,hi);if(det<=0)flips++;
        }});
    }
    const pass=low>=.8&&high<=1.2&&flips===0;allPass&&=pass;
    report.push({animation:anim.name,skin,frames,low:+low.toFixed(4),high:+high.toFixed(4),flips,pass});
  }
}
const lows=report.map(r=>r.low),highs=report.map(r=>r.high);
const summary={animations:report.length/3,samples:report.reduce((s,r)=>s+r.frames,0),low:Math.min(...lows),high:Math.max(...highs),flips:report.reduce((s,r)=>s+r.flips,0),pass:allPass};
await writeFile(outPath,JSON.stringify({gate:'visible-triangle strain 0.80-1.20, zero flips, 30 fps, Original/Ballet/Magician',summary,rows:report},null,1));
console.log(JSON.stringify(summary));
for(const r of report.filter(r=>!r.pass))console.log('FAIL',JSON.stringify(r));
