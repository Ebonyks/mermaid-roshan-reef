const { chromium } = require('playwright');
(async()=>{
  const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader']});
  const p=await b.newPage({viewport:{width:1160,height:760}});
  await p.goto('file://'+process.argv[2]+'?test=1'); await p.waitForFunction(()=>window.bathroomTest,{timeout:120000});
  const rows=await p.evaluate(()=>{const T=window.bathroomTest;const out=[];let s=T.reset('watch');
    for(let i=0;i<1960;i++){ s=T.step(1); if(i%2===1){ // 30fps sample
      const tail=[s.root[0]+s.tailRelative[0],s.root[1]+s.tailRelative[1]];
      out.push({t:+s.time.toFixed(3),ph:s.phase,fi:s.fi,f:s.facing,turn:s.turn?s.turn.kind+':'+s.turn.u.toFixed(2):'',root:s.root.map(v=>+v.toFixed(1)),head:s.head.map(v=>+v.toFixed(1)),tail:tail.map(v=>+v.toFixed(1)),br:s.bristles.map(v=>+v.toFixed(1)),palm:s.palm.map(v=>+v.toFixed(1)),ang:+s.angle.toFixed(3)});}
      if(s.phase==='done'&&s.age>1.2)break;}
    return out;});
  require('fs').writeFileSync(process.argv[3],JSON.stringify(rows));
  await b.close();
})();
