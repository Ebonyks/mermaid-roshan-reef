import { skeleton, worstAll, strain, SKINS } from './lib.mjs';
console.log('rest',JSON.stringify(worstAll({})));
const out={};
for(const b of skeleton.bones.slice(1)){
  const lim=[];
  for(const sign of [-1,1]){let last=0;for(let d=0.5;d<=90;d+=0.5){if(!worstAll({[b.name]:sign*d}).pass)break;last=d;}lim.push(sign*last);}
  const per=SKINS.map(s=>{const r=[];for(const sign of [-1,1]){let last=0;for(let d=0.5;d<=90;d+=0.5){const x=strain({[b.name]:sign*d},s);if(x.low<.8||x.high>1.2||x.flips)break;last=d;}r.push(sign*last);}return s[0]+r.join('/');});
  const w=[worstAll({[b.name]:lim[0]-1}).worst,worstAll({[b.name]:lim[1]+1}).worst];
  out[b.name]=lim;console.log(b.name.padEnd(24),String(lim[0]).padStart(6),String(lim[1]).padStart(6),' ',per.join('  '),' limiter:',w.join(' | '));
}
