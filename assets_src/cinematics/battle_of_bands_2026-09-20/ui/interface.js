/* Canvas layout study. Reuses the source art unchanged; cue geometry is UI only. */
'use strict';
const core = new RhythmFixture();
const canvas = document.querySelector('canvas'), ctx = canvas.getContext('2d');
const stage = document.querySelector('.stage'), veil = document.querySelector('.veil');
const drums = [...document.querySelectorAll('.drum')];
const query = new URLSearchParams(location.search);
let layout = ['fall','fan','single'].includes(query.get('view')) ? query.get('view') : 'fall';
let reviewState = 'live', last = 0, ready = true;
let stagePointer = null;
const blockedPointers = new Set();
// One finger owns the whole play surface, including its corner controls.
stage.addEventListener('pointerdown',e=>{if(stagePointer!==null&&stagePointer!==e.pointerId){blockedPointers.add(e.pointerId);e.preventDefault();e.stopImmediatePropagation();}else{stagePointer=e.pointerId;blockedPointers.delete(e.pointerId);}},true);
stage.addEventListener('click',e=>{if(blockedPointers.has(e.pointerId)){e.preventDefault();e.stopImmediatePropagation();blockedPointers.delete(e.pointerId);}},true);
window.addEventListener('pointerup',e=>{if(stagePointer===e.pointerId)stagePointer=null;});
window.addEventListener('pointercancel',e=>{if(stagePointer===e.pointerId)stagePointer=null;});
const targets = [[499,333],[741,340],[893,296]];
const tones = ['#82efd1','#d4adff','#ffe082'], inks = ['#16634f','#67449c','#825c12'];
const descriptions = {
 fall: ['01','Falling ribbons','Three familiar vertical paths lead directly to the two tom rims and cymbal. Tap the instrument when its moving bar meets the outlined landing mark.'],
 fan: ['02','Side approaches','Cues slide in from the edges. The paths leave Roshan’s face clear and converge on the same instrument contact points.'],
 single: ['03','One-bar practice','Only the next instrument and its path are highlighted. One clear moving cue introduces the same timing gesture without three competing paths.']
};
const art = {};
const siteCamera = {x:.30,y:.25,width:.40,height:.40};
const loaded = Promise.all([['background','../stage_fit/site_candidate.png'],['roshan','../references/roshan_drums.png']].map(([key,file]) => new Promise((resolve,reject) => {const im=new Image();im.onload=()=>{art[key]=im;resolve();};im.onerror=reject;im.src=file;})));
drums.forEach((button,i)=>{button.style.left=targets[i][0]/12.8+'%';button.style.top=targets[i][1]/7.2+'%';button.style.setProperty('--target',tones[i]);button.style.setProperty('--target-ink',inks[i]);});
function route(i) {
 const end=targets[i];
 if(layout==='fan') return [[i===0?120:i===1?1090:1180,i===0?230:i===1?80:440],end];
 return [[end[0],22],end];
}
function rounded(x,y,w,h,r,fill,stroke,width=3){ctx.beginPath();ctx.roundRect(x,y,w,h,r);ctx.fillStyle=fill;ctx.fill();if(stroke){ctx.strokeStyle=stroke;ctx.lineWidth=width;ctx.stroke();}}
function glyph(i,x,y,size,color){ctx.save();ctx.translate(x,y);ctx.fillStyle=color;ctx.beginPath();if(i===0)ctx.arc(0,0,size/2,0,Math.PI*2);else if(i===1){ctx.moveTo(0,-size*.6);ctx.lineTo(size*.6,0);ctx.lineTo(0,size*.6);ctx.lineTo(-size*.6,0);}else ctx.roundRect(-size*.75,-size*.22,size*1.5,size*.44,size*.2);ctx.fill();ctx.restore();}
function render(){
 if(!art.roshan)return;
 // One camera crop of the complete terrain-fitted environment. No enlarged oval overlay.
 const bg=art.background,c=siteCamera;
 ctx.clearRect(0,0,1280,720);ctx.drawImage(bg,bg.width*c.x,bg.height*c.y,bg.width*c.width,bg.height*c.height,0,0,1280,720);
 ctx.fillStyle='#f3f3ff80';ctx.fillRect(0,0,1280,720);
 const cue=core.cue();
 // Faint paths sit behind the character. Bars remain legible in the foreground.
 for(let i=0;i<3;i++){
   if(layout==='single' && i!==cue.target)continue;
   const [start,end]=route(i);
   ctx.beginPath();ctx.moveTo(...start);ctx.lineTo(...end);ctx.strokeStyle='#fff8';ctx.lineWidth=76;ctx.lineCap='round';ctx.stroke();
   ctx.strokeStyle=tones[i]+'aa';ctx.lineWidth=58;ctx.stroke();
   ctx.beginPath();ctx.moveTo(...start);ctx.lineTo(...end);ctx.setLineDash([4,15]);ctx.strokeStyle=inks[i]+'77';ctx.lineWidth=3;ctx.stroke();ctx.setLineDash([]);
 }
 ctx.drawImage(art.roshan,330,30,690,690);
 if(cue.visible && !ready){
   const [a,b]=route(cue.target),p=cue.progress,x=a[0]+(b[0]-a[0])*p,y=a[1]+(b[1]-a[1])*p;
   ctx.save();ctx.translate(x,y);ctx.rotate(Math.atan2(b[1]-a[1],b[0]-a[0])-Math.PI/2);
   rounded(-48,-16,96,32,14,tones[cue.target],inks[cue.target],4);ctx.restore();
   glyph(cue.target,x,y,17,inks[cue.target]);
 }
 drums.forEach((button,i)=>{button.classList.toggle('muted',layout==='single'&&i!==cue.target);button.classList.toggle('contact',cue.feedback&&i===cue.target);});
 if(cue.feedback){
   const [x,y]=targets[cue.target];ctx.beginPath();ctx.ellipse(x,y,81,64,0,0,Math.PI*2);ctx.lineWidth=5;ctx.strokeStyle='#fff5bf';ctx.stroke();
 }
 // Wordless still teaching pointer; no fake character performance or autoplay strike.
 if(ready || reviewState==='contact'){
   const [x,y]=targets[core.target];ctx.save();ctx.translate(x+46,y+54);ctx.rotate(-.6);rounded(-13,-18,26,57,12,'#fff7f0','#524070',3);rounded(-13,9,50,34,12,'#fff7f0','#524070',3);ctx.restore();
 }
}
function updateDescription(){const [n,title,copy]=descriptions[layout];document.querySelector('#study-number').textContent='STUDY '+n;document.querySelector('#study-title').textContent=title;document.querySelector('#study-copy').textContent=copy;document.querySelectorAll('[data-layout]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.layout===layout)));}
function message(text){document.querySelector('.review-message').textContent=text;}
function freeze(state){
 reviewState=state;core.reset();stagePointer=null;blockedPointers.clear();ready=state==='ready';
 if(state==='live'){ready=true;}else if(state==='approach')core.time=1.8;else if(state==='contact')core.time=3.2;else if(state==='feedback'){core.time=3.2;core.hit=true;core.feedbackUntil=3.85;}else if(state==='passed')core.time=3.7;else if(state==='paused')core.time=1.8;
 veil.classList.toggle('hidden',!ready&&state!=='paused');
 document.querySelector('.start').setAttribute('aria-label',state==='paused'?'Resume practice':'Start practice');
 document.querySelectorAll('[data-state]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.state===state)));
 message(state==='live'?'Press play, then tap the drum when its bar arrives.':({ready:'Still pointer and play symbol invite the child to begin.',approach:'The cue has a single destination. There are no chords.',contact:'Cue centre reaches the marked drum rim. The ±350 ms acceptance window surrounds this contact.',feedback:'A valid intentional touch lights that drum. Production strike animation is a separate future seam.',passed:'A missed cue quietly passes. No loss, red mark, deducted reward or forced restart.',paused:'Pause freezes cue time. Returning gives at least 1.6 seconds of approach.'})[state]);render();
}
document.querySelectorAll('[data-layout]').forEach(b=>b.addEventListener('click',()=>{layout=b.dataset.layout;updateDescription();freeze('live');}));
document.querySelectorAll('[data-state]').forEach(b=>b.addEventListener('click',()=>freeze(b.dataset.state)));
document.querySelector('.start').addEventListener('click',()=>{if(ready){core.reset();core.start();}else core.resume();ready=false;reviewState='live';veil.classList.add('hidden');document.querySelectorAll('[data-state]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.state==='live')));last=performance.now();message('Live silent fixture: tap the instrument at the landing mark.');});
function pause(){stagePointer=null;blockedPointers.clear();if(!ready){core.pause();veil.classList.remove('hidden');document.querySelector('.start').setAttribute('aria-label','Resume practice');message('Paused. Tap play to return with a fresh approach.');}}
document.querySelector('.pause').addEventListener('click',pause);
document.querySelector('.back').addEventListener('click',()=>freeze('live'));
drums.forEach((button,i)=>{button.addEventListener('pointerdown',e=>{e.preventDefault();if(reviewState!=='live')return;button.setPointerCapture(e.pointerId);const result=core.press(i,e.pointerId);if(result!=='ignored'){button.classList.add('touch-ack');setTimeout(()=>button.classList.remove('touch-ack'),180);}if(result==='contact')message('Contact registered on the instrument. No score or reward is granted by this UI fixture.');render();});button.addEventListener('pointerup',e=>core.release(e.pointerId));button.addEventListener('pointercancel',()=>core.cancel());button.addEventListener('lostpointercapture',e=>core.release(e.pointerId));});
window.addEventListener('blur',pause);document.addEventListener('visibilitychange',()=>{if(document.hidden)pause();});
function frame(now){if(last&&core.running)core.advance(Math.min((now-last)/1000,.1));last=now;render();requestAnimationFrame(frame);}
if(query.get('embed')==='1')document.documentElement.classList.add('embed');
updateDescription();loaded.then(()=>{freeze(query.get('state')||'live');window.BandsLab={core,targets,route,freeze,siteCamera,get layout(){return layout;},ready:true};requestAnimationFrame(frame);}).catch(()=>message('A reference image could not load. Open this folder through a local HTTP server.'));
