const { chromium } = require('playwright');
const url='file://'+process.argv[2]+'?test=1';
(async()=>{
  const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader']});
  const p=await b.newPage({viewport:{width:1160,height:760}});
  await p.goto(url); await p.waitForFunction(()=>window.bathroomTest||window.bathroomError,{timeout:120000});
  const err=await p.evaluate(()=>window.bathroomError); if(err){console.log('ERR',err);process.exit(1);}
  const res=await p.evaluate(()=>{
    const T=window.bathroomTest, F=[[555,194,46,13],[250,240,59,21],[832,259,25,8]];
    function toReady(fi){ // play mode: tap brush, then step until ready at fixture fi
      let s=T.reset('play'); T.touch([933,330]); let n=0;
      while(n<6000){s=T.step(1);n++; if(s.phase==='ready'&&s.fi===fi)return s;
        if(s.phase==='ready'){ // auto-complete earlier fixtures with the watch-like path
          T.touch(T.surface(s.fi,0)); let a=0; while(T.step(1).phase==='work'){a+=TAU/150; T.move(T.surface(s.fi,a));} T.release(); } }
      return s;}
    const TAU=Math.PI*2;
    function run(fi,gen,maxS=40){
      let s=toReady(fi); const t0=s.time; let t=0,starts=0,first=gen(0);
      if(!T.touch(first)) return {fi,startRejected:true,first};
      starts++; let lastPhase='work';
      for(let i=0;i<maxS*60;i++){t+=1/60; const pt=gen(t); T.move(pt); s=T.step(1);
        if(s.phase==='settle'||s.phase==='carry'||s.phase==='done')return {fi,seconds:+(s.time-t0).toFixed(2),progress:s.progress[fi].toFixed(2)};
        if(s.phase==='ready'){ if(T.touch(pt))starts++; }
      }
      return {fi,seconds:'>'+maxS,progress:s.progress[fi].toFixed(3)};
    }
    const circle=(cx,cy,rx,ry,hz,jit=0)=>t=>[cx+rx*Math.cos(t*TAU*hz)+jit*Math.sin(t*17.3),cy+ry*Math.sin(t*TAU*hz)+jit*Math.cos(t*13.1)];
    const sweep=(cx,cy,ax,hz,dy=0)=>t=>[cx+ax*Math.sin(t*TAU*hz),cy+dy*Math.sin(t*TAU*hz*2.3)];
    const out={};
    for(const [name,fi,gen] of [
      ['sink watch-like ring 41x11 @0.4Hz',0,circle(555,194,41,11,.4)],
      ['sink child ring 60x30 @0.8Hz',0,circle(555,194,60,30,.8,4)],
      ['sink child fast scribble 50x25 @3Hz',0,circle(555,194,50,25,3,4)],
      ['sink tiny wiggle 10x6 @1.5Hz',0,circle(555,194,10,6,1.5)],
      ['sink offset+20,+18 ring 45x25 @0.8Hz',0,circle(575,212,45,25,.8,3)],
      ['tub child sweep ±70 @0.7Hz',1,sweep(250,240,70,.7,10)],
      ['tub short sweep ±35 @1Hz',1,sweep(250,240,35,1,6)],
      ['tub fast sweep ±60 @3Hz',1,sweep(250,240,60,3,6)],
      ['tub offset y+30 sweep ±70',1,sweep(250,270,70,.7,8)],
      ['toilet watch-like ring 22x7 @0.4Hz',2,circle(832,259,22,7,.4)],
      ['toilet child ring 40x25 @0.8Hz',2,circle(832,259,40,25,.8,4)],
      ['toilet child ring 55x35 @0.8Hz',2,circle(832,259,55,35,.8,4)],
      ['toilet offset+15,+15 ring 35x20',2,circle(847,274,35,20,.8,3)],
      ['toilet fast scribble 35x20 @3Hz',2,circle(832,259,35,20,3,3)],
    ]) out[name]=run(fi,gen);
    // tap during carry: does anything respond?
    let s=T.reset('play'); T.touch([933,330]); while(s.phase!=='carry'){s=T.step(1);} 
    out['tap during carry accepted']=T.touch([555,194]);
    out['tap off-brush in wait accepted']=(T.reset('play'),T.touch([800,330]));
    return out;
  });
  for(const [k,v] of Object.entries(res))console.log(k.padEnd(42),JSON.stringify(v));
  await b.close();
})();
