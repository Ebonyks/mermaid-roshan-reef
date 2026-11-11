import { spawn } from 'node:child_process';
import { once } from 'node:events';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import assert from 'node:assert/strict';

const root=path.dirname(fileURLToPath(import.meta.url));
const mode=process.argv[2]??'all';
const capture=path.join(root,'.capture',mode);
const chrome=process.argv[3]??'C:/Program Files/Google/Chrome/Application/chrome.exe';
await mkdir(capture,{recursive:true});
const profile=path.join(capture,'browser-'+Date.now());
const url=pathToFileURL(path.join(root,'bathroom_playtest.html')).href+'?test=1';
const browser=spawn(chrome,['--headless','--use-angle=swiftshader','--enable-unsafe-swiftshader',
  '--no-first-run','--no-default-browser-check','--disable-background-networking','--disable-component-update',
  '--disable-default-apps','--disable-extensions','--remote-debugging-port=0','--window-size=1160,760','--user-data-dir='+profile,url],
  {windowsHide:true,stdio:['ignore','ignore','pipe']});
let browserErrors='';
browser.stderr.on('data',d=>{browserErrors=(browserErrors+d.toString()).slice(-5000);});
const pause=ms=>new Promise(r=>setTimeout(r,ms));
let socket;

function distance(a,b){return Math.hypot(a[0]-b[0],a[1]-b[1]);}

try {
  let port;
  for(let i=0;i<160&&!port;i++){
    try{port=(await readFile(path.join(profile,'DevToolsActivePort'),'utf8')).split(/\r?\n/)[0];}
    catch{await pause(75);}
  }
  assert(port,'DevTools unavailable '+browserErrors);
  const origin='http://127.0.0.1:'+port;
  const pages=await (await fetch(origin+'/json/list')).json();
  const page=pages.find(item=>item.url.startsWith('file:'))??pages.find(item=>item.type==='page');
  socket=new WebSocket(page.webSocketDebuggerUrl);
  await once(socket,'open');
  let sequence=0;
  const problems=[];
  const requests=new Map();
  socket.addEventListener('message',event=>{
    const data=JSON.parse(event.data);
    if(data.method==='Log.entryAdded'&&data.params.entry.level==='error')problems.push(data.params.entry.text.slice(0,500));
    if(data.method==='Runtime.exceptionThrown')problems.push(data.params.exceptionDetails.exception?.description?.slice(0,500));
    const callback=requests.get(data.id);
    if(!callback)return;
    requests.delete(data.id);
    if(data.error)callback.reject(new Error(data.error.message));
    else callback.resolve(data.result);
  });
  const command=(method,params={})=>new Promise((resolve,reject)=>{
    const id=++sequence;
    requests.set(id,{resolve,reject});
    socket.send(JSON.stringify({id,method,params}));
  });
  const js=async expression=>{
    const result=await command('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});
    if(result.exceptionDetails)throw Error(result.exceptionDetails.exception?.description??result.exceptionDetails.text);
    return result.result.value;
  };
  await command('Log.enable');
  await command('Runtime.enable');
  if(!page.url.startsWith('file:'))await command('Page.navigate',{url});
  for(let i=0;i<120;i++){
    const state=await js("window.bathroomError || (window.bathroomTest ? 'ready' : '')");
    if(state==='ready')break;
    if(state)throw Error(state);
    await pause(150);
    if(i===119)throw Error(JSON.stringify({reason:'Offline app did not load',problems,where:await js('[location.href,document.title,document.readyState,document.getElementById("loading")?.textContent]')}));
  }
  const step=async (n=1)=>js('bathroomTest.step('+n+')');
  const [rx,ry,rw,rh]=await js('bathroomTest.stageRect()');
  async function pointer(type,p){
    const touchPoints=p?[{x:rx+p[0]*rw/1024,y:ry+p[1]*rh/576,radiusX:8,radiusY:8,id:1}]:[];
    await command('Input.dispatchTouchEvent',{type,touchPoints});
  }
  async function frame(name) {
    const png=await js('bathroomTest.frame()');
    await writeFile(path.join(capture,name+'.png'),Buffer.from(png.split(',')[1],'base64'));
  }
  const metrics={maxBristleError:0,maxGripError:0,maxFingerError:0,minFingerToHead:Infinity,
    activeSamples:0,alphaHits:0,low:1,high:1,flips:0,strainSamples:0,geometryExceptions:[]};
  async function check(s,verifyAlpha=false){
    assert.equal(s.assetCount,1);
    assert.equal(s.bones,17);
    if(s.held)metrics.maxGripError=Math.max(metrics.maxGripError,distance(s.palm,s.brushGrip));
    if(s.activeContact){
      metrics.activeSamples++;
      const pointer=s.pointer;
      metrics.maxBristleError=Math.max(metrics.maxBristleError,distance(s.bristles,s.projectedContact));
      metrics.maxFingerError=Math.max(metrics.maxFingerError,distance(pointer,s.bristles));
      metrics.minFingerToHead=Math.min(metrics.minFingerToHead,distance(pointer,s.head));
      if(verifyAlpha) {
        const covered=await js('bathroomTest.fingerDisk('+pointer.join(',')+')');
        if(covered>20)metrics.alphaHits++;
      }
    }
  }
  async function strain(s){
    const sample=await js('bathroomTest.meshStrain()');
    metrics.low=Math.min(metrics.low,sample.low);
    metrics.high=Math.max(metrics.high,sample.high);
    metrics.flips+=sample.flips;
    metrics.strainSamples++;
    if(sample.low<.8-1e-6||sample.high>1.2+1e-6||sample.flips)
      metrics.geometryExceptions.push({time:s.time,skin:s.skin,phase:s.phase,...sample});
  }

  async function nextPhase(name,limit=30){
    for(let i=0;i<limit;i++){
      const s=await step(12);
      if(s.phase===name)return s;
    }
    throw Error('Never arrived at '+name);
  }

  async function touchRun(){
    await js("bathroomTest.reset('play');bathroomTest.look('Original')");
    await pointer('touchStart',[101,423]);await pointer('touchEnd');
    let s=await step(150);
    assert.equal(s.phase,'wait');assert.deepEqual(s.progress,[0,0,0]);
    await pointer('touchStart',[932,322]);await pointer('touchEnd');
    s=await nextPhase('ready',43);
    assert.equal(s.fixture,'sink');assert(s.held);assert(s.pickupError<.01);
    const at=await js('bathroomTest.surface(0,1.3)');
    await pointer('touchStart',at);
    s=await step(120);
    assert.equal(s.phase,'work');assert.equal(s.progress[0],0,'stationary hold earned progress');
    await pointer('touchMove',[672,470]);s=await step(50);
    assert.equal(s.progress[0],0,'off-fixture drag earned progress');
    await pointer('touchCancel');s=await step(6);assert.equal(s.phase,'ready');
    const before=await js('bathroomTest.snapshot()');
    assert.equal(before.progress[0],0);
    const reversalReleases=[];
    for(let i=0;i<3;i++){
      if(i)await nextPhase('ready',40);
      let held=await js('bathroomTest.surface('+i+',0)');
      await pointer('touchStart',held);
      let completed=false;
      for(let k=1;k<=166;k++){
        held=await js('bathroomTest.surface('+i+','+(k*.15)+')');
        await pointer('touchMove',held);
        s=await step(4);
        await check(s,k%4===0);
        if(k%13===0)await strain(s);
        if(mode==='reversal'&&i===1&&[11,32].includes(k)) {
          const prior=s;
          await pointer('touchEnd');
          s=await step(1);
          assert.equal(s.phase,'ready');
          const rootStep=distance(prior.root,s.root);
          assert(rootStep<8,'Abrupt root step on tub release');
          s=await step(18);
          assert.equal(s.progress[i],prior.progress[i]);
          assert(distance(s.bristles,prior.bristles)<1e-8);
          reversalReleases.push({sample:k,rootStep,progress:s.progress[i]});
          await pointer('touchStart',held);
        }
        if(i===0&&k===18){
          const progress=s.progress[0];
          assert(progress>0&&progress<1,'interrupt checkpoint failed');
          await pointer('touchCancel');
          s=await step(16);
          assert.equal(s.phase,'ready');
          assert.equal(s.progress[0],progress,'cancel lost or advanced progress');
          await pointer('touchStart',held);
        }
        if(s.phase==='settle'){completed=true;break;}
      }
      await pointer('touchEnd');
      assert(completed,'Touch fixture did not finish: '+i+' '+JSON.stringify(s));
    }
    s=await nextPhase('done',12);
    assert.deepEqual(s.clean,[1,1,1]);
    assert.deepEqual(s.completed.map(x=>x.fixture),['sink','tub','toilet']);
    assert(s.completed.every(x=>x.mode==='play'));
    return {finished:s.completed,events:s.events,stationaryHold:true,outsideDrag:true,touchCancel:true,passive:true,reversalReleases};
  }

  async function watchRun(skin,video=false,swapTest=false) {
    await js("bathroomTest.reset('watch');bathroomTest.look("+JSON.stringify(skin)+")");
    let s,doneFrames=0,last='',swaps=0;
    const prefix=(video?'video-':'')+skin.toLowerCase();
    const captures=new Set();
    const observation={blinks:0,lastLid:'open',closedSteps:0,maxStep:0,
      maxPalmStep:0, minTubAngle:999,maxTubAngle:-999, paths:{}, transitions:[]};
    let previous=null;
    observation.facingSwitches=[];
    observation.motion={};observation.swimArms={};observation.scrubJoints={};observation.swapFacing=[];
    observation.facingTravel={left:0,right:0};
    observation.backwardsTravel=0;observation.reverseByFixture={};
    const output=path.join(root,'bathroom_playthrough.mp4');
    const encoder=video?spawn('ffmpeg',['-hide_banner','-loglevel','error','-y','-f','image2pipe',
      '-framerate','30','-vcodec','mjpeg','-i','-','-vf','scale=1280:720:flags=lanczos',
      '-an','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',
      '-movflags','+faststart',output],{windowsHide:true,stdio:['pipe','ignore','inherit']}):null;
    const encoded=encoder?once(encoder,'exit'):null;
    try {
      for(let i=0;i<1350;i++){
        let movieFrame=null;
        if(video){
          const f=await js("(()=>{const state=bathroomTest.step(2);return {state,data:bathroomTest.frame('image/jpeg',.89)}})()");
          s=f.state;
          movieFrame=f.data;
        } else s=await step(mode==='quick'?4:2);
        if(s.lid==='closed') {
          observation.closedSteps++;
          if(observation.lastLid!=='closed')observation.blinks++;
        }
        observation.lastLid=s.lid;
        if(previous) {
          if(previous.facing!==s.facing)observation.facingSwitches.push({at:s.time,
            fixture:s.fixture,from:previous.facing,to:s.facing,
            root:distance(previous.root,s.root),
            brush:distance(previous.brushAnchor,s.brushAnchor),tip:distance(previous.bristles,s.bristles)});
          if(s.phase==='carry'&&!s.turn&&s.facing===previous.facing) {
            const movement=s.root[0]-previous.root[0];
            observation.facingTravel[s.facing<0?'left':'right']+=Math.abs(movement);
            if(movement*s.facing<-.05) {
              observation.backwardsTravel+=Math.abs(movement);
              observation.reverseByFixture[s.fixture]=(observation.reverseByFixture[s.fixture]??0)+Math.abs(movement);
            }
          }
          observation.maxStep=Math.max(observation.maxStep,distance(previous.root,s.root));
          observation.maxPalmStep=Math.max(observation.maxPalmStep,distance(previous.palm,s.palm));
          if(previous.phase!==s.phase)observation.transitions.push({at:s.time,from:previous.phase,to:s.phase,
            rootStep:distance(previous.root,s.root),palmStep:distance(previous.palm,s.palm)});
        }
        if(s.activeContact) {
          const mark=observation.paths[s.fixture]??={root:[Infinity,-Infinity],tip:[Infinity,-Infinity]};
          mark.root=[Math.min(mark.root[0],s.root[0]),Math.max(mark.root[1],s.root[0])];
          mark.tip=[Math.min(mark.tip[0],s.bristles[0]),Math.max(mark.tip[1],s.bristles[0])];
          if(s.fixture==='tub') {
            observation.minTubAngle=Math.min(observation.minTubAngle,s.angle);
            observation.maxTubAngle=Math.max(observation.maxTubAngle,s.angle);
          }
        }
        if(['approach','carry'].includes(s.phase)&&s.flightU!=null&&!s.turn&&s.tailRelative) {
          const leg=s.phase+'-'+s.fixture;
          const segment=observation.motion[leg]??={tailY:[Infinity,-Infinity],tailX:[Infinity,-Infinity],peakSpeed:0,finishSpeed:0,travelFrames:0};
          const [x,y]=s.tailRelative;
          segment.tailX=[Math.min(segment.tailX[0],x),Math.max(segment.tailX[1],x)];
          segment.tailY=[Math.min(segment.tailY[0],y),Math.max(segment.tailY[1],y)];
          if(previous?.phase===s.phase&&previous?.fixture===s.fixture&&previous?.facing===s.facing) {
            const speed=distance(previous.root,s.root)/(s.time-previous.time);
            segment.peakSpeed=Math.max(segment.peakSpeed,speed);
            if(s.flightU>.95)segment.finishSpeed=Math.max(segment.finishSpeed,speed);
          }
          segment.travelFrames++;
        }
        if(s.activeContact&&s.armAngles) {
          const points=[s.root,s.elbow,s.palmRelative,s.armAngles,s.bristles];
          const names=['pelvis','elbow','palm','angles','bristles'];
          const travel=observation.scrubJoints[s.fixture]??={};
          points.forEach((point,i)=>{
            travel[names[i]]??=point.map(()=>[Infinity,-Infinity]);
            point.forEach((value,j)=>{
              const range=travel[names[i]][j];
              range[0]=Math.min(range[0],value);
              range[1]=Math.max(range[1],value);
            });
          });
        }
        if(s.swimArmPose&&['carry','approach'].includes(s.phase)&&!s.turn&&s.flightU>.08&&s.flightU<.93) {
          const key=s.phase+'-'+s.fixture;
          const leg=observation.swimArms[key]??={};
          for(const arm of s.swimArmPose) {
            const row=leg[arm.side]??={angles:arm.angles.map(()=>[Infinity,-Infinity]),
              wrist:arm.wrist.map(()=>[Infinity,-Infinity])};
            for(const name of ['angles','wrist'])arm[name].forEach((value,i)=>{
              row[name][i][0]=Math.min(row[name][i][0],value);
              row[name][i][1]=Math.max(row[name][i][1],value);
            });
          }
        }
        previous=s;
        await check(s,i%7===0);
        if(i%8===0||s.turn||(s.activeContact&&i%3===0)||(['approach','carry'].includes(s.phase)&&(mode==='all'||i%3===0)))await strain(s);
        if(mode==='quick'&&s.swimArmPose&&!s.turn&&s.flightU!=null
            &&['approach','carry'].includes(s.phase)) {
          const leg=s.phase+'-'+s.fixture;
          const peaks=(observation.recoveryFrames??={})[leg]??={};
          for(const target of [.19,.247,.576,.641]) {
            if(s.flightU>=target&&s.flightU<target+.04&&!peaks[target]) {
              const key=prefix+'-recovery-'+leg+'-'+String(target).slice(2);
              peaks[target]={u:s.flightU,time:s.time,root:s.root,arms:s.swimArmPose,brush:s.brushGrip};
              await frame(key);
            }
          }
        }
        const sweep=s.activeContact&&s.fixture==='tub'&&s.age>.3
          ?(s.bristles[0]<205?'tub-left':s.bristles[0]>294?'tub-right':''):'';
        const key=sweep||((['approach','carry'].includes(s.phase)&&s.flightU!=null&&!s.turn&&s.flightU>.14&&s.flightU<.98)?
          'flight-'+s.phase+'-'+s.fixture+'-'+Math.floor(s.flightU*7):s.turn?'turn-'+s.turn.kind+'-'+s.fixture+'-'+Math.floor(s.turn.u*4)
          :s.lid!=='open'?s.lid+'-'+s.fixture:s.phase+'-'+s.fixture);
        if(!captures.has(key)&&(['grasp','carry','work','settle','done'].includes(s.phase)||s.lid!=='open'||s.turn||key.startsWith('flight-')||sweep)){
          if(s.age>.45 || s.phase==='done' || s.lid!=='open' || s.turn || key.startsWith('flight-') || sweep){await frame(prefix+'-'+key);captures.add(key);}
        }
        if(video && i===0)await frame('original-start');
        const canSwap=mode==='swapview'?s.phase==='carry'&&!s.turn&&s.age>.95:s.activeContact&&s.age>1.3;
        if(swapTest && canSwap && last!==s.fixture){
          last=s.fixture;
          const next=s.fixture==='sink'?'Ballet':s.fixture==='tub'?'Magician':'Original';
          const same=await js('bathroomTest.look('+JSON.stringify(next)+');bathroomTest.snapshot()');
          assert.equal(same.time,s.time);assert.equal(same.phase,s.phase);
          assert.equal(same.facing,s.facing);observation.swapFacing.push(s.facing);
          assert.deepEqual(same.root,s.root);assert.deepEqual(same.bristles,s.bristles);
          swaps++;
        }
        if(encoder){
          const data=movieFrame;
          const chunk=Buffer.from(data.split(',')[1],'base64');
          if(!encoder.stdin.write(chunk))await once(encoder.stdin,'drain');
        }
        if(s.phase==='done'&&++doneFrames>= (video?38:1))break;
        if(i===1349)throw Error('Walkthrough did not finish '+JSON.stringify(s));
      }
      if(encoder){encoder.stdin.end();assert.deepEqual(await encoded,[0,null]);}
    } catch(error) {
      if(encoder)encoder.kill();
      throw error;
    }
    assert.deepEqual(s.clean,[1,1,1]);
    assert.deepEqual(s.completed.map(x=>x.fixture),['sink','tub','toilet']);
    assert(s.completed.every(x=>x.mode==='watch'));
    if(swapTest)assert.equal(swaps,3);
    const tub=observation.scrubJoints.tub;
    const span=([low,high])=>high-low;
    assert(span(tub.pelvis[0])<=24,'The body is following too much of the tub stroke');
    assert(span(tub.bristles[0])>=107,'Tub sweep narrowed');
    assert(span(tub.angles[0])>=14&&span(tub.angles[1])>=16,'The arm is not opening and bending during the tub stroke');
    assert.equal(observation.facingSwitches.length,4);
    if(mode==='swapview')assert.deepEqual(observation.swapFacing,[-1,-1,1]);
    assert(observation.facingTravel.left>400 && observation.facingTravel.right>350);
    return {skin,swaps,pickupError:s.pickupError,finished:s.completed,events:s.events,time:s.time,observation};
  }

  const watch=[];
  let touch=null;
  if(mode==='smoke'||mode==='quick')watch.push(await watchRun('Original'));
  else if(mode==='reversal')touch=await touchRun();
  else if(mode==='video')watch.push(await watchRun('Original',true));
  else if(mode==='swap'||mode==='swapview')watch.push(await watchRun('Original',false,true));
  else {
    touch=await touchRun();
    for(const skin of ['Original','Ballet','Magician'])watch.push(await watchRun(skin));
  }
  const propulsion=await js('bathroomTest.propulsionProof()');
  assert(propulsion.every(leg=>leg.disabled===0&&leg.driven>0&&leg.finishSpeed<leg.peakSpeed*.25));
  const receipt={mode,watch,touch,metrics,propulsion,browser:await js('navigator.userAgent')};
  await writeFile(path.join(root,mode+'_receipt.json'),JSON.stringify(receipt,null,2)+'\n');
  console.log(JSON.stringify({mode,watch:watch.map(x=>({skin:x.skin,time:x.time,pickup:x.pickupError,swaps:x.swaps})),touch:touch?.finished,metrics},null,2));
  assert(metrics.maxGripError<=1);
  assert(metrics.maxBristleError<=1);
  assert(metrics.minFingerToHead>=48);
  assert(metrics.alphaHits===0,'Actor enters the tested finger disk in '+metrics.alphaHits+' samples');
  assert(metrics.flips===0);
  assert(metrics.geometryExceptions.length===0,JSON.stringify(metrics.geometryExceptions.slice(0,10)));
} finally {
  socket?.close();
  browser.kill();
}
