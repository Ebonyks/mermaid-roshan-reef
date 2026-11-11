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
    const drift=(g,dx,dy,after)=>t=>{const p=g(t);const k=Math.min(1,Math.max(0,(t-after)/1.5));return [p[0]+dx*k,p[1]+dy*k];};
    for(const [name,fi,gen] of [
      ['sink back-and-forth ±40 @1.5Hz',0,sweep(555,194,40,1.5,4)],
      ['toilet back-and-forth ±25 @1.5Hz',2,sweep(832,259,25,1.5,3)],
      ['tub circles 60x20 @0.8Hz',1,circle(250,240,60,20,.8,3)],
      ['sink ring drifting +45px down after 1s',0,drift(circle(555,194,45,15,.8,3),0,45,1)],
      ['toilet ring drifting +35px right after 1s',2,drift(circle(832,259,30,15,.8,3),35,0,1)],
      ['tub sweep ±70 drifting +40 down after 1s',1,drift(sweep(250,240,70,.7,6),0,40,1)],
    ]) out[name]=run(fi,gen);
    return out;

  });
  for(const [k,v] of Object.entries(res))console.log(k.padEnd(42),JSON.stringify(v));
  await b.close();
})();
