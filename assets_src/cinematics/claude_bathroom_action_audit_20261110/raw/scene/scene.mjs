import { Affine, Pose, Skeleton } from '@rigby/src/core/index.js';
import { unzip } from '@rigby/src/editor/zip.js';
import { WebGLRenderer } from '@rigby/src/webgl/renderer.js';

const WIDTH=1024, HEIGHT=576, SCALE=.92;
const acting=JSON.parse(document.querySelector('#payload').textContent).acting;
const TAU=Math.PI*2, STEP=1/60;
const GRIP=[670,320], END_GRIP=[784,173], BRISTLES=[305,850], BRUSH_SCALE=.069;
const BRUSH_REACH=Math.hypot(BRISTLES[0]-GRIP[0],BRISTLES[1]-GRIP[1])*BRUSH_SCALE;
const BRUSH_ZERO=Math.atan2(BRISTLES[1]-GRIP[1],BRISTLES[0]-GRIP[0]);
const [handleX,handleY]=minusHandle();
function minusHandle() {
  const x=END_GRIP[0]-GRIP[0], y=END_GRIP[1]-GRIP[1];
  return [BRUSH_SCALE*(x*Math.cos(BRUSH_ZERO)+y*Math.sin(BRUSH_ZERO)),
    BRUSH_SCALE*(-x*Math.sin(BRUSH_ZERO)+y*Math.cos(BRUSH_ZERO))];
}
const PARK={grip:[933,319], angle:1.35};
const START=[651,417];
const FIXTURES=[
  {id:'sink',name:'Sink',center:[555,194],r:[46,13],angle:.19,carry:3.0,voice:'sinkVoice',need:205},
  {id:'tub',name:'Bathtub',center:[250,acting.tubY??250],r:[59,21],angle:acting.tubAngle,carry:2.65,voice:'tubVoice',need:345},
  {id:'toilet',name:'Toilet',center:[832,259],r:[25,8],angle:.19,carry:4.25,voice:'toiletVoice',need:129}
];
const PHASES={wait:'Find the brush',approach:'Swim to the brush',grasp:'Take the brush',
              carry:'Carry the brush',ready:'Ready to scrub',work:'Scrub',settle:'Clean!',done:'All three fixtures clean'};
const clamp=(n,a,b)=>Math.min(b,Math.max(a,n));
const smooth=t=>{t=clamp(t,0,1);return t*t*(3-2*t);};
const mix=(a,b,t)=>a+(b-a)*t;
const between=(a,b,t)=>a.map((x,i)=>mix(x,b[i],t));
const plus=(a,b)=>[a[0]+b[0],a[1]+b[1]];
const minus=(a,b)=>[a[0]-b[0],a[1]-b[1]];
const dist=(a,b)=>Math.hypot(...minus(a,b));
const vector=(a,r)=>[Math.cos(a)*r,Math.sin(a)*r];
const wrap=a=>Math.atan2(Math.sin(a),Math.cos(a));
const dot=(a,b)=>a[0]*b[0]+a[1]*b[1];
const cueNames=['sinkVoice','tubVoice','toiletVoice'];
const assetData=JSON.parse(document.querySelector('#payload').textContent);
const testing=new URL(location.href).searchParams.has('test');
const room=document.querySelector('#room').getContext('2d');
const front=document.querySelector('#front').getContext('2d');
const actor=document.querySelector('#actor');
const gl=actor.getContext('webgl',{alpha:true,premultipliedAlpha:true,preserveDrawingBuffer:testing});
const loading=document.querySelector('#loading');
const bytes=s=>Uint8Array.from(atob(s),c=>c.charCodeAt(0));

async function loadArt(src) {
  const img=new Image();
  img.src=src;
  await img.decode();
  return img;
}

function projectTouch(point,f) {
  const delta=minus(point,f.center);
  const radius=Math.hypot(delta[0]/f.r[0],delta[1]/f.r[1]);
  return radius>1 ? plus(f.center,delta.map(n=>n/radius)) : point.slice();
}
function hit(point,f) {
  const d=minus(point,f.center);
  return Math.hypot(d[0]/(f.r[0]+22),d[1]/(f.r[1]+22))<=1;
}
function surfacePoint(f,phase) {
  if(f.id==='tub') {
    const s=Math.sin(phase);
    return plus(f.center,[f.r[0]*s*.93,6*(s*s-.5)]);
  }
  return plus(f.center,[f.r[0]*Math.cos(phase)*.9,f.r[1]*Math.sin(phase)*.83]);
}
function cubic(a,b,c,d,t) {
  const u=1-t;
  return a.map((v,i)=>u**3*v+3*u*u*t*b[i]+3*u*t*t*c[i]+t**3*d[i]);
}
function pathFor(phase,from,to) {
  if(phase==='approach')return [from,[from[0]+67,from[1]+12],[to[0]-47,to[1]+65],to];
  const low=Math.max(from[1],to[1])+65;
  return [from,[mix(from[0],to[0],.24),low],[mix(from[0],to[0],.72),low],to];
}
// Per-stroke keys for root, mid, distal, peduncle, and fluke.
const STROKE=[
  [0,0,0,0,0,0],
  [.19,5.4,3.5,1.0,-1.4,-4.5],
  [.34,6.7,7.4,6.1,3.8,-7.7],
  [.47,-2.7,1.4,5.0,5.0,4.5],
  [.60,-5.0,-7.0,-3.9,-1.3,9.0],
  [.72,-2.6,-4.2,-4.8,-4.0,4.0],
  [.86,-.2,-.5,-1.2,-1.9,-.6],
  [1,0,0,0,0,0]
];
const BEATS=[[.018,.52,1],[.45,.48,.65]];
const GLIDE_BEATS=[[.008,.38,1],[.37,.43,.62]];
function tailAngles(u,amplitude) {
  const result=[0,0,0,0,0];
  for(const [start,duration,effort] of acting.glide?GLIDE_BEATS:BEATS) {
    const t=clamp((u-start)/duration,0,1);
    let i=1;
    while(i<STROKE.length-1&&t>STROKE[i][0])i++;
    const a=STROKE[i-1], b=STROKE[i], weight=smooth((t-a[0])/(b[0]-a[0]));
    for(let j=0;j<result.length;j++)result[j]+=mix(a[j+1],b[j+1],weight)*amplitude*effort;
  }
  return result;
}
// One loose-arm phrase per tail pulse. The elbow takes longer to unfold
// and the wrist trails the shoulder into the glide.
const ARM_STROKE=[
  [0,0,0,0],
  [.19,4,2,0],
  [.34,9,7,2],
  [.48,2,12,6],
  [.63,-11,6,7],
  [.75,-9,-3,2],
  [.88,-3,-4,-4],
  [1,0,0,0],
];
function armStroke(u,lag=0) {
  const result=[0,0,0];
  for(const [start,duration,effort] of GLIDE_BEATS) {
    const t=clamp((u-start-lag)/duration,0,1);
    let i=1;
    while(i<ARM_STROKE.length-1&&t>ARM_STROKE[i][0])i++;
    const a=ARM_STROKE[i-1], b=ARM_STROKE[i];
    const weight=smooth((t-a[0])/(b[0]-a[0]));
    for(let j=0;j<result.length;j++)result[j]+=mix(a[j+1],b[j+1],weight)*effort;
  }
  return result;
}
function thrustPlan(duration,amplitude) {
  const samples=240,dt=duration/samples;
  const distance=[0], speeds=[0], force=[0];
  let speed=0,previous=0,filtered=0;
  for(let i=1;i<=samples;i++) {
    const u=i/samples;
    const [,mid,distal,peduncle,pitch]=tailAngles(u,amplitude);
    // Only the return of the loaded fluke creates forward thrust.
    const sweep=.36*mid+.63*distal+.80*peduncle;
    const extension=Math.max(0,(previous-sweep)/dt);
    const effort=extension*clamp(.22+pitch*.088,.14,1);
    filtered=mix(filtered,effort,1-Math.exp(-dt*6.4));
    const impulse=acting.glide?filtered:effort;
    const drag=acting.glide
      ?(acting.finishMotion?.60:.88)+smooth((u-.74)/.26)*9.4
      :1.68+smooth((u-.76)/.23)*12;
    speed=(speed+impulse*dt)*Math.exp(-drag*dt);
    distance.push(distance[i-1]+speed*dt);
    speeds.push(speed);
    force.push(impulse);
    previous=sweep;
  }
  return {distance,speeds,force,total:distance.at(-1),samples};
}
function sampleList(series,u) {
  const at=clamp(u,0,1)*(series.length-1), i=Math.floor(at);
  return mix(series[i],series[Math.min(i+1,series.length-1)],at-i);
}
function pathLengths(path) {
  const result=[0];
  let last=path[0];
  for(let i=1;i<=80;i++){
    const next=cubic(...path,i/80);
    result.push(result.at(-1)+dist(last,next));
    last=next;
  }
  return result;
}
function arcPoint(path,lengths,fraction) {
  if(fraction<=0)return path[0].slice();
  if(fraction>=1)return path[3].slice();
  const distance=lengths.at(-1)*fraction;
  let lo=0,hi=lengths.length-1;
  while(hi-lo>1){
    const m=(hi+lo)>>1;
    if(lengths[m]<distance)lo=m;else hi=m;
  }
  const local=(distance-lengths[lo])/Math.max(1e-8,lengths[hi]-lengths[lo]);
  return cubic(...path,(lo+local)/(lengths.length-1));
}
function outline(points) {
  const p=new Path2D();
  p.moveTo(...points[0]);
  for(const next of points.slice(1))p.lineTo(...next);
  p.closePath();
  return p;
}
function roundBox(ctx,x,y,w,h,r,fill) {
  ctx.beginPath();ctx.roundRect(x,y,w,h,r);ctx.fillStyle=fill;ctx.fill();
}
function ellipse(ctx,x,y,rx,ry,fill,stroke) {
  ctx.beginPath();ctx.ellipse(x,y,rx,ry,0,0,TAU);
  if(fill){ctx.fillStyle=fill;ctx.fill();}
  if(stroke){ctx.strokeStyle=stroke;ctx.stroke();}
}

try {
  if(!gl)throw new Error('WebGL is unavailable. Open this file in a browser with hardware acceleration enabled.');
  const archive=unzip(bytes(assetData.rig));
  const skeleton=Skeleton.fromJson(new TextDecoder().decode(archive.get('project.json')));
  const skeletonArt={};
  for(const [name,data] of archive) {
    if(name.startsWith('images/')&&name.endsWith('.png')){
      skeletonArt[name.slice(7,-4)]=await createImageBitmap(new Blob([data],{type:'image/png'}),
        {premultiplyAlpha:'none',colorSpaceConversion:'none'});
    }
  }
  const [dirty,clean,brush,sinkGrime,tubGrime]=await Promise.all(
    ['dirty','clean','brush','sink','tub'].map(name=>loadArt(assetData[name])));
  const renderer=new WebGLRenderer(gl);
  const textures=renderer.imageTextures(skeletonArt);
  const leftArt=assetData.leftPaint?renderer.imageTextures(Object.fromEntries(
    await Promise.all(Object.entries(assetData.leftPaint).map(async ([key,url])=>[key,await loadArt(url)])))):null;
  const eyelids={};
  if(assetData.eyePaint) {
    // Paint only the eye regions. Register each lid separately to the face;
    // the farther eye is narrower in this quarter view.
    const eyeRects=[
      {from:[479,239,58,32],to:[541,234,50,48]},
      {from:[552,236,56,34],to:[621,230,33,48]}
    ];
    for(const [state,url] of Object.entries(assetData.eyePaint)) {
      const source=await loadArt(url);
      const art={};
      for(const name of ['original_swim','atlas_costume_anatomy']) {
        const original=skeletonArt[name];
        const canvas=document.createElement('canvas');
        canvas.width=original.width;canvas.height=original.height;
        const ctx=canvas.getContext('2d');
        ctx.drawImage(original,0,0);
        for(const {from,to} of eyeRects) {
          const [x,y,w,h]=to;
          const patch=document.createElement('canvas');
          patch.width=w;patch.height=h;
          const paint=patch.getContext('2d');
          paint.drawImage(source,...from,0,0,w,h);
          if(acting.featherEyes) {
            paint.globalCompositeOperation='destination-in';
            paint.translate(w/2,h/2);
            paint.scale(w/2,h/2);
            const feather=paint.createRadialGradient(0,0,.84,0,0,1.04);
            feather.addColorStop(0,'white');
            feather.addColorStop(1,'transparent');
            paint.fillStyle=feather;
            paint.fillRect(-1,-1,2,2);
            ctx.drawImage(patch,x,y);
          } else {
            ctx.save();ctx.beginPath();
            ctx.ellipse(x+w/2,y+h/2,w*.52,h*.54,0,0,TAU);
            ctx.clip();ctx.drawImage(patch,x,y);ctx.restore();
          }
        }
        art[name]=canvas;
      }
      eyelids[state]=renderer.imageTextures(art);
    }
  }
  const pose=new Pose(skeleton);
  const place=new Affine();
  const swim=skeleton.animations.find(a=>a.name==='Original artwork swim');
  const index=Object.fromEntries(skeleton.bones.map((b,i)=>[b.name,i]));
  const tubLip=outline([[103,257],[133,260],[160,262],[186,264],[215,264],
    [242,264],[269,263],[296,261],[322,257],[347,251],[354,255],
    [350,277],[311,296],[144,303],[103,282]]);
  const leftHead=leftArt?makeHeadGrid():null;
  const headwearSlot=skeleton.slots.findIndex(slot=>slot.name==='headwear');
  const neutralPose=new Pose(skeleton);
  const neutralPelvis=neutralPose.world[index.root].apply([0,0]);
  const cruisePalm=[-1,1].map(facing=>{
    const hand=neutralPose.world[index[facing<0?'screen_left_hand':'screen_right_hand']];
    const [x,y]=minus(hand.apply([facing<0?9:6,0]),neutralPelvis);
    return [x*SCALE*facing,-y*SCALE];
  });
  function makeHeadGrid() {
    // UV positions are in the existing 256-unit rig canvas, with the painted
    // left-view contours registered before projection by the view transform.
    const rest=new Pose(skeleton);
    const joints=['head','ponytail_base','ponytail_tip','chest'].map(name=>index[name]);
    const xs=Array.from({length:25},(_,i)=>244+i*20);
    const ys=Array.from({length:23},(_,i)=>24+i*20);
    const uvs=[], nodes=[], triangles=[];
    for(const y of ys)for(const x of xs) {
      uvs.push(x/1024,y/1024);
      const pony=smooth((460-x)/112);
      const distal=pony*smooth((405-x)/92);
      const neck=(1-pony)*.40*smooth((y-327)/52)*smooth((x-435)/45)*(1-smooth((x-575)/53));
      const weights=[1-pony-neck,pony-distal,distal,neck];
      const size=acting.leftHeadScale??1;
      const restX=560+(x-560)*size;
      const restY=360+(y-360)*size+(acting.leftHeadDrop??0);
      nodes.push(joints.map((bone,i)=>[bone,rest.world[bone].inverse().apply([restX/4,-restY/4]),weights[i]]));
    }
    for(let y=0;y<ys.length-1;y++)for(let x=0;x<xs.length-1;x++) {
      const i=y*xs.length+x,j=i+xs.length;
      triangles.push(i,i+1,j,i+1,j+1,j);
    }
    const positions=state=>nodes.map(node=>node.reduce((sum,[bone,local,weight])=>{
      const [x,y]=state.world[bone].apply(local);
      return [sum[0]+x*weight,sum[1]+y*weight];
    },[0,0]));
    return {uvs,triangles,positions,rest:positions(rest)};
  }
  function drawLeftHead() {
    const key=look==='Original'?'left_head_original':'left_head_wardrobe';
    renderer.use(leftArt(key).tex,'normal');
    renderer.emit(leftHead.positions(pose).flat(),leftHead.uvs,leftHead.triangles,[1,1,1,1],null);
  }
  const dryTubExterior=new Path2D();
  dryTubExterior.rect(0,0,WIDTH,HEIGHT);
  dryTubExterior.addPath(outline([[92,194],[376,194],[376,239],[359,251],[339,257],
    [310,264],[270,268],[195,269],[145,266],[116,260],[94,247]]));
  const cleanShapes=Object.fromEntries(FIXTURES.map(f=>[f.id,outline(assetData.outlines[f.id])]));
  const guides=FIXTURES.map(f=>Array.from({length:33},(_,i)=>surfacePoint(f,i*TAU/32)));
  const audio=Object.fromEntries(cueNames.map(name=>[name,new Audio(assetData[name])]));
  let sound=true, unlocked=false;
  let lastError='';
  let mode='play',look='Original',session,activePointer=null,mouseTarget=null;

  function say(name) {
    if(!sound||!unlocked||testing)return;
    for(const clip of Object.values(audio)){clip.pause();clip.currentTime=0;}
    audio[name]?.play().catch(()=>{});
  }

  function transition(phase) {
    session.phase=phase;
    session.age=0;
    session.events.push({phase,fixture:session.fi,at:session.time,held:session.held});
  }

  function reset(nextMode=mode) {
    mode=nextMode;
    for(const clip of Object.values(audio)){clip.pause();clip.currentTime=0;}
    activePointer=null;
    mouseTarget=null;
    session={phase:'wait',time:0,age:0,fi:0,held:false,facing:1,turn:null,skin:look,root:START.slice(),
      tip:null,angle:PARK.angle,brushDepth:1,workGrip:0,swimPhase:0,poseClock:0,stroke:0,effort:[0,0],hair:[0,0],hairForce:0,attention:0,celebration:0,lid:'open',blinkAt:-99,blinkCue:'',gesture:null,route:null,
      progress:[0,0,0],clean:[0,0,0],events:[{phase:'wait',fixture:0,at:0,held:false}],
      completed:[],bubbles:[],watchTouch:false,workTravel:0,pickupError:null,lastMove:-Infinity};
    document.querySelector('#play').setAttribute('aria-pressed',String(mode==='play'));
    document.querySelector('#watch').setAttribute('aria-pressed',String(mode==='watch'));
  }

  function setLook(name) {
    look=name;
    session.skin=name;
    skeleton.skin=name==='Original'?null:name;
  }

  function addBone(name,deg){pose.local[index[name]].rotation+=deg;}
  // A wave advances from the waist to the fluke. The same beat schedule
  // advances along the route, so locomotion and the visible effort agree.
  function swimPhrase(u,direction,amount) {
    const wave=(lag,spread)=> {
      const beat=(center,strength)=>strength*Math.exp(-((u-center-lag)**2)/spread);
      return direction*(beat(.18,1)-beat(.29,.67)+beat(.51,.71)-beat(.63,.46)-beat(.85,.42));
    };
    const tone=amount*Math.sin(Math.PI*clamp(u,0,1))**.53;
    addBone('tail_root',tone*3.5*wave(0,.008));
    addBone('tail_mid',tone*5.2*wave(.035,.009));
    addBone('tail_distal',tone*5.0*wave(.071,.010));
    addBone('tail_peduncle',tone*4.1*wave(.104,.012));
    addBone('fluke',tone*4.6*wave(.123,.014));
    addBone('abdomen',tone*-2.1*wave(.02,.012));
    addBone('chest',tone*2.5*wave(-.04,.013));
    addBone('head',tone*(2.0*direction-1.4*wave(.015,.014)));
  }
  function propelled(u) {
    const f=smooth(u);
    const impulse=(center,width)=>smooth((u-center+width)/(width*2));
    const beats=.43*impulse(.22,.17)+.37*impulse(.53,.19)+.20*impulse(.79,.21);
    return mix(f,beats,(acting.swim??0)*.50);
  }
  // Forearm flexion follows the rest elbow's anatomical sign. Keeping a
  // relaxed elbow through the glide avoids the former straightening pulse.
  // A broad recovery top lets the forearm yield after the shoulder reverses,
  // then unfold slowly through the glide instead of flicking back.
  function elbowRecovery(u,lag=0) {
    const keys=[[0,0],[.18,2],[.34,8],[.48,12],[.63,11],[.75,7],[.90,2],[1,0]];
    let total=0;
    for(const [start,duration,effort] of GLIDE_BEATS) {
      const t=clamp((u-start-lag)/duration,0,1);
      let i=1;
      while(i<keys.length-1&&t>keys[i][0])i++;
      const a=keys[i-1],b=keys[i];
      total+=mix(a[1],b[1],smooth((t-a[0])/(b[0]-a[0])))*effort;
    }
    return total;
  }
  function relaxedArm(side,u,occupied=false,lag=0) {
    const bend=side==='screen_left'?-1:1;
    const gate=acting.broadRecovery ? smooth(u/.065)*(1-smooth((u-.94)/.06)) : smooth((u-.015)/.105)*(1-smooth((u-.88)/.12));
    const pulse=armStroke(u,lag);
    const strength=session.facing<0?.70:1;
    const recovery=acting.broadRecovery?elbowRecovery(u,lag):pulse[1];
    const flex=occupied ? (acting.carryBend??10) + recovery*(acting.heldRecovery??.24) : (acting.freeBend??10) + recovery*(acting.recoveryBend??.42);
    const sweep=(occupied?.17:(acting.freeSweep??.52))*pulse[0]*strength;
    const ordinaryCompensation=acting.armCompensation??.45;
    // The costume shoulder underlay has less room beside the ponytail.
    // Ease only the free shoulder in rightward carry; keep elbow recovery.
    const compensation=session.phase==='carry'&&session.facing>0&&!occupied&&side==='screen_left'
      ?(acting.forwardFreeCompensation??ordinaryCompensation):ordinaryCompensation;
    addBone(side+'_upper_arm',-bend*(flex*compensation+sweep)*gate);
    addBone(side+'_forearm',bend*flex*gate);
    addBone(side+'_hand',-bend*(1.5+pulse[2]*(occupied?.12:.24))*gate);
  }
  function poseSwimmingArms(phase,u,free,other) {
    if(acting.relaxedArms) {
      relaxedArm(free,u);
      relaxedArm(other,u,phase==='carry',phase==='carry'?.025:.047);
      return;
    }
    const envelope=acting.swimArmOverlay
      ?smooth((u-.035)/.14)*(1-smooth((u-.80)/.145)):1;
    const strength=(session.facing<0?(acting.leftSwimArmStrength??acting.swimArmStrength):acting.swimArmStrength)*envelope;
    const sign=free==='screen_left'?1:-1;
    const loose=armStroke(u);
    const [upper,elbow,wrist]=loose;
    addBone(free+'_upper_arm',sign*upper*strength);
    const bendLimit=session.facing<0?(acting.leftSwimBend??1):1;
    addBone(free+'_forearm',sign*elbow*strength*bendLimit);
    addBone(free+'_hand',sign*wrist*strength*bendLimit);
    if(phase==='carry') {
      // Support the brush nearer the body through the push, then open
      // into the fixture grip. The tool still follows the posed palm.
      const support=smooth(u/.17)*(1-smooth((u-.70)/.25));
      const [a,b,c]=armStroke(u,.026);
      const held=-sign*(acting.swimArmOverlay?(session.facing<0?(acting.leftHeldArmStrength??.45):.65)*envelope:(acting.heldArmStrength??strength));
      addBone(other+'_upper_arm',held*(5.2*support+.29*a));
      addBone(other+'_forearm',held*(7.1*support+.39*b));
      addBone(other+'_hand',held*(-3.1*support+.37*c));
    } else {
      const [a,b,c]=armStroke(u,.047);
      addBone(other+'_upper_arm',-sign*a*.64*strength);
      addBone(other+'_forearm',-sign*b*.72*strength);
      addBone(other+'_hand',-sign*c*.66*strength);
    }
  }
  function buildPose(phase,t,drive,travel,reach,fraction=0) {
    pose.placement=null;
    pose.reset(skeleton);
    if(travel>0&&acting.motor) {
      const angles=tailAngles(fraction,acting.motor);
      ['tail_root','tail_mid','tail_distal','tail_peduncle','fluke'].forEach((name,i)=>addBone(name,angles[i]));
      const plan=session.route.motor;
      const speed=sampleList(plan.speeds,fraction);
      const load=angles[0];
      const travelBlend=smooth(fraction/.15)*(1-smooth((fraction-.88)/.12));
      addBone('root',travelBlend*(clamp(-session.flightSlope*13,-8,8)-load*.56));
      addBone('abdomen',load*-.20);
      addBone('chest',angles[1]*-.16);
      addBone('head',load*.08);
      const free=session.facing<0?'screen_right':'screen_left';
      const hand=session.facing<0?'screen_left':'screen_right';
      const late=smooth((fraction-.74)/.11)*(1-smooth((fraction-.90)/.10));
      const delayed=acting.finishMotion?tailAngles(Math.max(0,fraction-.038),acting.motor):angles;
      // Explicit relaxed-arm tracks are applied after placing the root.
      if(!acting.relaxedArms) {
        if(acting.swimArmStrength&&!acting.swimArmOverlay)poseSwimmingArms(phase,fraction,free,hand);
        else {
          addBone(free+'_upper_arm',-session.facing*(angles[0]*.30+speed*.22));
          addBone(free+'_forearm',session.facing*(delayed[1]*.59+speed*.16));
        }
      }
      if(acting.finishMotion) {
        addBone('tail_peduncle',-1.6*late);
        addBone('fluke',2.9*late+delayed[4]*.08);
        addBone('ponytail_base',-delayed[0]*.092);
        addBone('ponytail_tip',-delayed[1]*.12);
      }
      if(phase==='carry'&&!acting.relaxedArms&&(!acting.swimArmStrength||acting.swimArmOverlay)) {
        addBone(hand+'_upper_arm',angles[0]*.22);
        addBone(hand+'_forearm',-angles[1]*.31);
      }
    } else if(travel>0) {
      const amount=acting.swim??0;
      pose.apply(skeleton,swim,session.swimPhase,travel*(1-amount*.83));
      const route=session.route.path;
      const direction=Math.sign(route[3][0]-route[0][0])*session.facing;
      swimPhrase(fraction,direction,amount);
      if(acting.banks) {
        const stroke=Math.sin(Math.PI*fraction)**2;
        addBone('root',stroke*(direction>0?-4.8:2.6));
        const fold=phase==='carry'?stroke*(direction<0?1:.43):0;
        const hand=session.facing<0?'screen_left':'screen_right';
        addBone(hand+'_upper_arm',session.facing* -3.4*fold);
        addBone(hand+'_forearm',session.facing*5.7*fold);
        addBone(hand+'_hand',session.facing* -2.0*fold);
      }
    }
    const work=1-travel;
    const planted=phase==='ready'||phase==='work'||phase==='settle'||phase==='done';
    const natural=acting.work??0;
    const f=FIXTURES[session.fi];
    const dx=session.tip?clamp((session.tip[0]-f.center[0])/f.r[0],-1,1):0;
    const dy=session.tip?clamp((session.tip[1]-f.center[1])/f.r[1],-1,1):0;
    const [vx,vy]=session.effort;
    const oldBeat=Math.sin(t*5.7);
    // Direction and pressure come from the visible brush stroke.
    const sweep=dx*.67+vx*.33;
    const bend=f.id==='tub'?sweep:.55*sweep-.45*dy;
    const beat=mix(oldBeat,bend,natural);
    const calm=acting.calm??0;
    const quiet=phase==='wait'||phase==='ready'||phase==='done';
    const breath=quiet ? Math.sin(t*1.38)*(.54+.46*Math.sin(t*.61)**2) : 0;
    const idle=mix(Math.sin(t*2.1),breath,calm);
    const float=acting.hair??0;
    const [hairBase,hairTip]=session.hair;
    addBone('ponytail_base',float*hairBase);
    addBone('ponytail_tip',float*hairTip);
    addBone('abdomen',calm*work*breath*.9);
    addBone('chest',work*(.7*idle+1.3*drive*beat-1.4*reach-natural*vx*1.15));
    const expressive=acting.expression??0;
    const acknowledge=phase==='settle'?Math.sin(Math.PI*clamp(session.age/.92,0,1)):0;
    const pride=session.celebration*expressive;
    const focus=session.attention*expressive;
    if(acting.banks) {
      // A modest supported body bank keeps the pose readable without pulling
      // the painted neck joint beyond its tested range.
      const workBank=acting.finish && phase==='work'?-0.65*drive*vx:0;
      const takeBank=acting.finish?-1.05*reach:0;
      addBone('root',focus*3.2+pride*3.4+workBank+takeBank);
      addBone('head',focus*.75+pride*.72);
      addBone('chest',focus*.32+pride*.45);
      addBone('screen_left_upper_arm',pride*3.2);
      addBone('screen_left_forearm',pride*4.1);
      addBone('screen_left_hand',pride*-2.6);
    } else {
      addBone('head',focus*3.8+pride*3.6);
      addBone('chest',focus*.85+pride*1.8);
      addBone('screen_left_upper_arm',pride*6.0);
      addBone('screen_left_forearm',pride*7.5);
      addBone('screen_left_hand',pride*-5.0);
    }
    addBone('tail_distal',pride*-2.1);
    addBone('fluke',pride*-3.4);
    addBone('head',work*(.6*idle-(acting.finish?1.15:2.4)*reach-1.5*drive+
      (acting.finish?1.9:2.6)*acknowledge));
    if(!planted) addBone('screen_right_upper_arm',work*(reach*6.0+drive*4.6*beat+natural*(2.8*dx+1.6*vy)*drive));
    if(!planted) addBone('screen_right_forearm',work*(reach*4.0-drive*7.2*beat+3.2*acknowledge+natural*(4.8*dx-2.2*vy)*drive));
    if(!planted) addBone('screen_right_hand',work*(reach*3.0+drive*7.5*mix(Math.sin(t*5.7-.58),-.48*vx+.24*dy,natural)));
    addBone('screen_left_upper_arm',work*(1.2*idle-2.4*drive*beat-natural*drive*3.2*vx));
    addBone('screen_left_forearm',work*natural*drive*(1.5-2.3*vx));
    addBone('tail_mid',work*(idle*1.1-1.4*drive*beat));
    addBone('fluke',work*(idle*1.8+drive*2.0*beat));
    if(acting.turnActing&&session.turn) {
      // Gather before exchanging the painted view. The fluke releases
      // a fraction behind the chest on the way into the new heading.
      const u=session.turn.u;
      const gather=Math.sin(Math.PI*u)**1.5*acting.turnActing;
      addBone('root',3.0*gather);
      addBone('tail_root',3.5*gather);
      addBone('tail_mid',5.5*gather);
      addBone('tail_distal',4.2*gather);
      addBone('tail_peduncle',2.6*gather);
      addBone('fluke',-3.4*gather);
      addBone('head',.9*gather);
    }
    pose.updateWorld(skeleton);
  }
  function rigPoint(name,local=[0,0]) {
    return pose.world[index[name]].apply(local);
  }
  function facingDelta(point,facing=session.facing) {
    const [x,y]=minus(point,rigPoint('root'));
    return [x*SCALE*facing,-y*SCALE];
  }
  function palmDelta(facing=session.facing) {
    const socket=facing<0?'screen_left_hand':'screen_right_hand';
    const bridge=acting.turnActing&&session.turn?Math.sin(Math.PI*session.turn.u)**2:0;
    const position=facing<0&&acting.gripBridge ? 9+1.3*bridge : 6-3.2*bridge;
    return facingDelta(rigPoint(socket,[position,0]),facing);
  }
  // The turned hand receives the upper end of the same visible handle.
  // Coordinates are measured in the brush painting before its canvas rotation.
  function handleOffset(weight,angle,depth) {
    return plus(vector(angle,handleX*depth*weight),vector(angle+Math.PI/2,handleY*weight));
  }
  function gripOffset(facing=session.facing,angle=session.angle,depth=session.brushDepth) {
    return handleOffset(facing<0&&acting.gripBridge?1:session.workGrip,angle,depth);
  }
  function palmAt(root) {return plus(root,palmDelta());}
  function poseScrubArm(f,tip,lift=0,weight=1) {
    const [dx,dy]=minus(tip,f.center);
    const across=clamp(dx/f.r[0],-1,1);
    const foreAft=clamp(dy/f.r[1],-1,1);
    const width=f.id==='tub'?1:f.id==='sink'?.79:.58;
    // Open the working elbow on the outward sweep and fold it on the
    // return. Joint animation precedes the contact calculation.
    addBone('screen_right_upper_arm',weight*(width*(acting.scrubUpper*across-2.6*foreAft)+4.1*lift));
    addBone('screen_right_forearm',weight*(width*(acting.scrubElbow*across+3.0*foreAft+(acting.tubHandle?2.5:0))+6.2*lift));
    addBone('screen_right_hand',weight*(-acting.scrubWrist*across+.8*foreAft));
    pose.updateWorld(skeleton);
  }
  function scrubPose(f,tip,lift=0) {
    poseScrubArm(f,tip,lift);

    // Register a hover relative to the fixture and the neutral arm.
    // The wrist motion and in-plane brush rake absorb the stroke. Only
    // the remaining reach is reconciled through a body adjustment.
    const tub=f.id==='tub';
    const grip=tub?(acting.tubHandle??0):0;
    const hover=minus(f.center,plus(cruisePalm[1],[tub?3:9,tub?(acting.tubHover??38):39]));
    const [x,y]=minus(tip,palmAt(hover));
    const axial=BRUSH_REACH-handleX*grip;
    const cross=handleY*grip;
    const depth=clamp(Math.sqrt(Math.max(0,x*x+y*y-cross*cross))/axial,
      grip?(acting.tubDepthMin??.77):acting.depthMin,acting.depthMax);
    const angle=clamp(Math.atan2(Math.max(6,y),x)+Math.atan2(cross,axial*depth),
      .46,grip?(acting.tubAngleMax??2.17):2.08);
    const palmToTip=minus(vector(angle,BRUSH_REACH*depth),handleOffset(grip,angle,depth));
    return {angle,depth,grip,root:minus(tip,plus(palmDelta(),palmToTip))};
  }
  function brushLength() {
    return BRUSH_REACH*(session.brushDepth??1);
  }
  function gripForTip(tip,angle){return minus(tip,vector(angle,brushLength()));}
  function rootForTip(tip,angle){return minus(plus(gripForTip(tip,angle),gripOffset()),palmDelta());}
  function markFor(f){return surfacePoint(f,0);}
  function prepareRoute(name,end,duration) {
    session.route={duration,path:pathFor(name,session.root,end),
      previousAngles:pose.local.map(x=>x.rotation)};
    session.route.motor=thrustPlan(duration,acting.motor??0);
    session.route.lengths=pathLengths(session.route.path);
    session.flightSlope=0;
    transition(name);
  }
  function pickup() {
    if(session.phase!=='wait')return false;
    buildPose('grasp',0,0,0,1);
    const end=minus(PARK.grip,palmDelta());
    end[0]-=17;end[1]+=9;
    prepareRoute('approach',end,2.15);
    return true;
  }
  function carry() {
    const fixture=FIXTURES[session.fi];
    const previous=pose.local.map(transform=>({...transform}));
    buildPose('ready',session.poseClock,0,0,0);
    const oldDepth=session.brushDepth;
    const oldGrip=session.workGrip;
    const arrival=scrubPose(fixture,markFor(fixture));
    session.brushDepth=arrival.depth;
    const endGrip=gripForTip(markFor(fixture),arrival.angle);
    const end=arrival.root;
    session.brushDepth=oldDepth;
    session.carryDepth=oldDepth;
    previous.forEach((transform,i)=>Object.assign(pose.local[i],transform));
    pose.updateWorld(skeleton);
    session.carryReach=session.phase==='grasp'?1:0;
    session.carryAngle=session.angle;
    const left=end[0]<session.root[0]-24;
    const startGrip=minus(palmAt(session.root),gripOffset());
    prepareRoute('carry',end,fixture.carry+(left?acting.turnIn+acting.turnOut:0));
    session.route.left=left;
    session.route.swimTime=fixture.carry;
    session.route.workAngle=arrival.angle;
    session.route.workDepth=arrival.depth;
    session.route.workGrip=arrival.grip;
    session.route.fromGrip=oldGrip;
    session.route.gripPath=pathFor('carry',startGrip,endGrip);
    session.route.gripLengths=pathLengths(session.route.gripPath);
    if(acting.finishMotion) {
      const side=left?-1:1;
      const heldRest=cruisePalm[side<0?0:1];
      // Register the leg's independent pelvis curve once at neutral.
      // The brush may then swing freely with the pose between the bridges.
      const mount=gripOffset(side,.33,.93);
      const rootAt=anchor=>minus(plus(anchor,mount),heldRest);
      session.route.pelvisPath=pathFor('carry',
        acting.armDeparture&&!left?session.root:rootAt(startGrip),
        acting.armDeparture&&!left?end:rootAt(endGrip));
      session.route.pelvisLengths=pathLengths(session.route.pelvisPath);
    }
    session.route.motor=thrustPlan(fixture.carry,acting.motor??0);
    session.route.fromRoot=session.root.slice();
  }
  function startTouch(point) {
    const f=FIXTURES[session.fi];
    if(session.phase==='wait')return dist(point,PARK.grip)<66 && pickup();
    if(session.phase!=='ready'||!hit(point,f))return false;
    if(!session.gesture)session.gesture={distance:0,arc:0,seen:0,seconds:0,span:[Infinity,-Infinity],
      direction:0,pivot:null,reversals:0,last:null};
    session.gesture.last=null;
    session.gesture.direction=0;
    session.gesture.pivot=null;
    mouseTarget=point.slice();
    session.lastMove=-Infinity;
    transition('work');
    return true;
  }
  function moveTouch(point) {
    if(session.phase!=='work')return;
    if(mouseTarget && dist(point,mouseTarget)>.15)session.lastMove=session.time;
    mouseTarget=point.slice();
  }
  function release() {
    mouseTarget=null;
    if(session.phase==='work')transition('ready');
    activePointer=null;
    session.watchTouch=false;
  }

  function earn(f,point,dt) {
    const g=session.gesture;
    const d=g.last?dist(point,g.last):0;
    if(d<.08){g.last=point.slice();return;}
    const prev=g.last;
    g.last=point.slice();
    g.distance+=d;
    g.seconds+=dt;
    session.workTravel+=d;
    let progress;
    if(f.id==='tub') {
      g.span[0]=Math.min(g.span[0],point[0]);
      g.span[1]=Math.max(g.span[1],point[0]);
      g.pivot??=point[0];
      if(!g.direction && Math.abs(point[0]-g.pivot)>10)g.direction=Math.sign(point[0]-g.pivot);
      if(g.direction) {
        const advance=(point[0]-g.pivot)*g.direction;
        if(advance>=0)g.pivot=point[0];
        else if(advance<-15){g.reversals++;g.direction*=-1;g.pivot=point[0];}
      }
      progress=Math.min(g.distance/f.need,(g.span[1]-g.span[0])/85,g.reversals/2,g.seconds/2.55);
    } else {
      const angle=p=>Math.atan2((p[1]-f.center[1])/f.r[1],(p[0]-f.center[0])/f.r[0]);
      const a=angle(point);
      const radius=Math.hypot((point[0]-f.center[0])/f.r[0],(point[1]-f.center[1])/f.r[1]);
      if(radius>.43){
        g.arc+=Math.abs(wrap(a-angle(prev)));
        g.seen|=1<<(Math.floor((a+Math.PI)/TAU*8)%8);
      }
      const sectors=g.seen.toString(2).replaceAll('0','').length;
      progress=Math.min(g.distance/f.need,g.arc/(TAU*1.06),sectors/7,g.seconds/2.55);
    }
    session.progress[session.fi]=Math.max(session.progress[session.fi],clamp(progress,0,1));
    if(session.workTravel>12){
      session.workTravel=0;
      session.bubbles.push({point:point.slice(),at:session.time,phase:(session.bubbles.length%3)-1});
    }
    if(progress>=1){
      session.completed.push({fixture:f.id,at:session.time,distance:g.distance,
        arc:g.arc,reversals:g.reversals,activeSeconds:g.seconds,mode});
      session.watchTouch=false;
      activePointer=null;mouseTarget=null;
      session.finishTip=session.tip.slice();
      session.releasePose=pose.local.map(joint=>joint.rotation);
      transition('settle');
    }
  }

  function demoInput() {
    if(mode!=='watch')return;
    if(session.phase==='wait'&&session.age>.7){pickup();return;}
    if(session.phase==='ready'&&session.age>.85){
      session.watchTouch=startTouch(markFor(FIXTURES[session.fi]));
    }
    if(session.phase==='work'&&session.watchTouch) {
      const f=FIXTURES[session.fi];
      const speed=f.id==='tub'?TAU/2.6:TAU/2.5;
      moveTouch(surfacePoint(f,session.age*speed));
    }
  }

  function update(dt) {
    session.time+=dt;
    session.age+=dt;
    session.poseClock+=dt;
    demoInput();
    const phase=session.phase, age=session.age, f=FIXTURES[session.fi];
    const route=session.route;
    const travel=phase==='approach'||phase==='carry';
    const moving=phase==='work'&&mouseTarget&&hit(mouseTarget,f);
    const previousRoot=session.root;
    const duration=travel?route.duration:1;
    const inspect=phase==='settle' ? 1-smooth((age-.18)/.32) : 0;
    const finishedAccent=phase==='done' ? Math.sin(Math.PI*smooth((age-.12)/1.05)) : 0;
    const thank=phase==='settle' ? Math.sin(Math.PI*smooth((age-.29)/.55)) : finishedAccent*.76;
    const aim=phase==='wait' ? -.28*smooth(age/.35)
      : phase==='approach' ? -.74*smooth(age/.32)
      : phase==='grasp' ? -.93
      : phase==='carry' ? -.35+.5*smooth(age/duration)
      : phase==='work' ? -.89
      : phase==='ready' ? -.55 : -.66*inspect;
    session.attention=mix(session.attention,aim,1-Math.exp(-dt*11));
    session.celebration=mix(session.celebration,thank,1-Math.exp(-dt*10));
    const fraction=clamp(age/duration,0,1);
    let swimFraction=fraction;
    if(phase==='carry' && route.left) {
      swimFraction=clamp((age-acting.turnIn)/route.swimTime,0,1);
      const exit=age-acting.turnIn-route.swimTime;
      session.turn=age<acting.turnIn ? {kind:'into-left',u:age/acting.turnIn}
        : exit>=0 ? {kind:'into-right',u:clamp(exit/acting.turnOut,0,1)} : null;
      session.facing=(age>=acting.turnIn*.55 && exit<acting.turnOut*.48)?-1:1;
    } else {
      session.turn=null;
      session.facing=1;
    }
    if(travel)session.swimPhase=(session.swimPhase+dt*(phase==='approach'?1.25:1.03))%swim.duration;
    const intent=moving&&session.time-session.lastMove<.18;
    const targetDelta=intent&&session.tip?minus(projectTouch(mouseTarget,f),session.tip):[0,0];
    session.effort=between(session.effort,[Math.tanh(targetDelta[0]/5),Math.tanh(targetDelta[1]/3)],1-Math.exp(-dt*9));
    const driveGoal=intent&&session.tip?clamp(dist(session.tip,projectTouch(mouseTarget,f))/6,0,1):0;
    session.stroke=mix(session.stroke,driveGoal,1-Math.exp(-dt*11));
    const reach=phase==='grasp'?smooth(age/.8):phase==='approach'?0:
      phase==='carry'?session.carryReach*(1-smooth(age/.55)):0;
    const swimWeight=travel?Math.pow(Math.sin(Math.PI*swimFraction),.65)*(phase==='approach'?1:.72):0;
    let travelProgress=propelled(swimFraction);
    if(travel&&acting.motor) {
      const plan=route.motor;
      travelProgress=plan.total>0?sampleList(plan.distance,swimFraction)/plan.total:0;
      const curve=phase==='carry'?route.pelvisPath??route.gripPath:route.path;
      const lengths=phase==='carry'?route.pelvisLengths??route.gripLengths:route.lengths;
      const a=arcPoint(curve,lengths,travelProgress-.024);
      const b=arcPoint(curve,lengths,travelProgress+.024);
      session.flightSlope=(b[1]-a[1])/Math.max(4,Math.abs(b[0]-a[0]));
    }
    session.flightU=travel?swimFraction:null;
    session.flightProgress=travel?travelProgress:null;
    buildPose(phase,session.poseClock,session.stroke,swimWeight,reach,swimFraction);
    if(acting.finishMotion&&phase==='settle'&&age<.20) {
      const ease=smooth(age/.20);
      pose.local.forEach((joint,i)=>{
        joint.rotation=mix(session.releasePose[i],joint.rotation,ease);
      });
      pose.updateWorld(skeleton);
    }
    if(travel) {
      const p=route.path;
      if(acting.banks && phase==='carry' && age<.24) {
        const ease=smooth(age/.24);
        pose.local.forEach((joint,i)=>{
          const old=route.previousAngles[i];
          joint.rotation=mix(old,joint.rotation,ease);
        });
        pose.updateWorld(skeleton);
      }
      if(phase==='carry') {
        const grip=acting.motor?arcPoint(route.gripPath,route.gripLengths,travelProgress)
          :cubic(...route.gripPath,propelled(swimFraction));
        if(acting.turnActing&&session.turn)grip[1]-=6*Math.sin(Math.PI*session.turn.u)**2;
        const ordinary=session.carryAngle+wrap(route.workAngle-session.carryAngle)*smooth(fraction);
        if(route.left&&acting.gripBridge) {
          const entry=smooth(age/(acting.turnIn*.53));
          const turn=acting.arrivalBridge?.29:.47;
          const exit=smooth((age-acting.turnIn-route.swimTime-acting.turnOut*turn)/(acting.turnOut*(1-turn)));
          const travelling=Math.sin(Math.PI*swimFraction)**2;
          const raised=acting.turnActing?.39-travelling*.27:.39+travelling*.15;
          session.angle=mix(mix(session.carryAngle,raised,entry),route.workAngle,exit);
        } else {
          const tuck=route.left?Math.sin(Math.PI*swimFraction)**2*.38:0;
          session.angle=ordinary+tuck;
        }
        session.brushDepth=mix(session.carryDepth,route.workDepth,smooth(fraction));
        const mountBlend=route.left
          ?smooth((age-acting.turnIn-route.swimTime-acting.turnOut*.52)/(acting.turnOut*.48))
          :smooth(fraction/.43);
        session.workGrip=mix(route.fromGrip,route.workGrip,mountBlend);
        const dock=route.left&&acting.arrivalBridge?mountBlend:smooth((fraction-.85)/.15);
        if(session.facing>0&&dock>0)poseScrubArm(f,markFor(f),0,dock);
        const actual=palmDelta();
        const neutral=cruisePalm[session.facing<0?0:1];
        const freeCruise=acting.motor?smooth(swimFraction/.24)*(1-smooth((swimFraction-.76)/.24)):0;
        if(acting.finishMotion) {
          const transfer=minus(plus(grip,gripOffset()),actual);
          const cruise=arcPoint(route.pelvisPath,route.pelvisLengths,travelProgress);
          // Without a turn, the body departs its work hover and the brush
          // follows the hand. Mount changes do not tug the body backwards.
          session.root=acting.armDeparture&&!route.left?cruise:between(transfer,cruise,freeCruise);
        } else session.root=minus(plus(grip,gripOffset()),between(actual,neutral,freeCruise));
        if(acting.swimArmOverlay&&swimFraction>0&&swimFraction<1) {
          const free=session.facing<0?'screen_right':'screen_left';
          const gripArm=session.facing<0?'screen_left':'screen_right';
          poseSwimmingArms(phase,swimFraction,free,gripArm);
          pose.updateWorld(skeleton);
          const wrist=index[gripArm+'_hand'];
          const flex=pose.local[wrist].rotation-neutralPose.local[wrist].rotation;
          session.angle-=session.facing*clamp(flex*.011,-.075,.075);
        }
        const heldFromPalm=minus(palmAt(session.root),gripOffset());
        session.tip=plus(heldFromPalm,vector(session.angle,brushLength()));
      } else {
        session.root=acting.motor?arcPoint(p,route.lengths,travelProgress):cubic(...p,propelled(fraction));
        if(acting.swimArmOverlay) {
          poseSwimmingArms(phase,swimFraction,'screen_left','screen_right');
          pose.updateWorld(skeleton);
        }
      }
      session.hairForce=clamp((session.root[0]-previousRoot[0])/Math.max(dt,STEP)/36,-4,4);
      if(fraction>=1) {
        if(phase==='approach'){session.graspFrom=session.root.slice();transition('grasp');}
        else {
          session.tip=markFor(f);
          session.angle=route.workAngle;
          session.brushDepth=route.workDepth;
          session.workGrip=route.workGrip;
          session.root=rootForTip(session.tip,session.angle);
          transition('ready');
          say(f.voice);
        }
      }
    } else if(phase==='grasp') {
      const need=minus(PARK.grip,palmDelta());
      session.root=between(session.graspFrom,need,smooth(age/.82));
      if(age>=.82) {
        session.pickupError=dist(palmAt(session.root),PARK.grip);
        session.held=true;
        session.tip=plus(PARK.grip,vector(PARK.angle,BRUSH_REACH));
        session.angle=PARK.angle;
        carry();
      }
    } else if(session.held) {
      if(moving) {
        const desired=projectTouch(mouseTarget,f);
        const previous=session.tip;
        session.tip=between(previous,desired,1-Math.exp(-dt*22));
        if(intent)earn(f,session.tip,dt);
        else session.gesture.last=null;
      } else if(phase==='work'&&session.gesture) {
        session.gesture.last=null;
      }
      let lift=0;
      if(phase==='settle'||phase==='done') {
        lift=phase==='done'?1:smooth(age/.56);
        const liftHeight=acting.finish?(f.id==='tub'?23:acting.finishMotion&&f.id==='toilet'?28:21)
          :(acting.tubDepth&&f.id==='tub'?20:13);
        session.tip=plus(session.finishTip,[(acting.finish?-5:3)*lift,-liftHeight*lift]);
      }
      const scrub=scrubPose(f,session.tip,lift);
      session.angle=scrub.angle;
      session.brushDepth=scrub.depth;
      session.workGrip=scrub.grip;
      session.root=scrub.root;
      if(phase==='settle') {
        session.clean[session.fi]=smooth(age/.75);
        if(age>=.92) {
          session.clean[session.fi]=1;
          if(session.fi===FIXTURES.length-1){transition('done');}
          else {session.fi++;session.gesture=null;session.stroke=0;carry();}
        }
      }
    }
    if(!travel)session.hairForce=mix(session.hairForce,moving?session.effort[0]*.65:0,1-Math.exp(-dt*7));
    const drift=Math.sin(session.time*1.28+.4)*.66+Math.sin(session.time*.83)*.40;
    session.hair[0]=mix(session.hair[0],drift-session.hairForce*.82,1-Math.exp(-dt*5.5));
    session.hair[1]=mix(session.hair[1],session.hair[0]*.71+drift*.55,1-Math.exp(-dt*3.4));
    if(acting.blink) {
      const quiet=phase==='wait'||phase==='ready'||phase==='done';
      const cue=phase+'-'+session.fi;
      const cueAge=phase==='wait'?.37:phase==='done'?.48:.45;
      if(quiet && age>=cueAge && session.time-session.blinkAt>2.8 &&
          (session.blinkCue!==cue || session.time-session.blinkAt>5.35)) {
        session.blinkAt=session.time;
        session.blinkCue=cue;
      }
      const elapsed=session.time-session.blinkAt;
      session.lid=elapsed<.045?'half':elapsed<.105?'closed':elapsed<.162?'half':'open';
    }
    session.bubbles=session.bubbles.filter(b=>session.time-b.at<.9);
  }

  function paintRoom() {
    room.clearRect(0,0,WIDTH,HEIGHT);
    room.drawImage(dirty,0,0);
    FIXTURES.forEach((f,i)=>{
      if(session.clean[i]>0&&!(acting.staticTub&&f.id==='tub')){
        room.save();room.clip(cleanShapes[f.id]);
        if(acting.tubForeground&&f.id==='tub')room.clip(dryTubExterior,'evenodd');
        room.globalAlpha=session.clean[i];
        room.drawImage(clean,0,0);room.restore();
      }
      if(session.progress[i]<.98&&session.clean[i]===0){
        const pic=f.id==='tub'?tubGrime:sinkGrime;
        const dims=f.id==='tub'?[133,43]:f.id==='sink'?[92,30]:[48,18];
        room.globalAlpha=.44*(1-session.progress[i]);
        room.drawImage(pic,f.center[0]-dims[0]/2,f.center[1]-dims[1]/2,dims[0],dims[1]);
        room.globalAlpha=1;
      }
    });
    const [x,y]=session.root;
    ellipse(room,x-10,y+67,60,12,'rgba(43,36,64,.13)');
    const grip=session.held?minus(palmAt(session.root),gripOffset()):PARK.grip;
    room.save();room.translate(...grip);room.rotate(session.held?session.angle:PARK.angle);
    // Foreshorten the handle along its own axis to imply pitch into the tub.
    room.scale(BRUSH_SCALE*(session.held?session.brushDepth:1),BRUSH_SCALE);
    room.rotate(-BRUSH_ZERO);
    room.drawImage(brush,-GRIP[0],-GRIP[1]);room.restore();
    if(acting.tubDepth && session.fi===1 && session.held &&
        ['ready','work','settle'].includes(session.phase)) {
      room.save();room.clip(tubLip);
      room.drawImage(dirty,0,0);
      if(session.clean[1]>0&&!acting.staticTub) {
        room.clip(cleanShapes.tub);
        if(acting.tubForeground)room.clip(dryTubExterior,'evenodd');
        room.globalAlpha=session.clean[1];
        room.drawImage(clean,0,0);
      }
      room.restore();
    }
    return grip;
  }

  function paintActor() {
    const [x,y]=session.root;
    const signed=SCALE*session.facing;
    place.set(signed,0,0,SCALE,x-124*signed,-y+128*SCALE);
    pose.placement=place;
    pose.updateWorld(skeleton);
    gl.viewport(0,0,WIDTH,HEIGHT);
    gl.clearColor(0,0,0,0);gl.clear(gl.COLOR_BUFFER_BIT);
    renderer.begin(WIDTH,HEIGHT,{x:WIDTH/2,y:-HEIGHT/2,zoom:1});
    const eye=eyelids[session.lid];
    const left=session.facing<0;
    const lookup=left?name=>leftArt?.(name)??textures(name)
      :eye?name=>eye(name)??textures(name):textures;
    const headOptions=left&&leftHead?{
      skip:i=>i===headwearSlot&&look==='Original',
      between:i=>{if(i===headwearSlot)drawLeftHead();}
    }:undefined;
    renderer.drawSkeleton(skeleton,pose,lookup,headOptions);
    renderer.end();
  }

  function lineGuide() {
    const phase=session.phase;
    if(phase==='wait') {
      const at=plus(PARK.grip,vector(PARK.angle,BRUSH_REACH*.58));
      front.lineWidth=3;
      const pulse=1+Math.sin(session.age*4)*.14;
      ellipse(front,...at,28*pulse,28*pulse,null,'#fff2ad');
      front.lineWidth=2;
      ellipse(front,...at,33*pulse,33*pulse,null,'rgba(44,34,69,.60)');
      return;
    }
    if(phase!=='ready')return;
    const f=FIXTURES[session.fi],points=guides[session.fi];
    front.beginPath();front.moveTo(...points[0]);
    for(const point of points.slice(1))front.lineTo(...point);
    front.setLineDash([4,5]);front.lineWidth=2.5;front.strokeStyle='rgba(255,249,197,.93)';front.stroke();front.setLineDash([]);
    const cue=surfacePoint(f,session.age*2.4);
    ellipse(front,...cue,6.5,6.5,'#fff5b5','#7c5952');
  }

  function title() {
    const f=FIXTURES[session.fi];
    let main=PHASES[session.phase];
    if(session.phase==='carry') {
      main='Swim to the '+f.name.toLowerCase();
    }
    if(['ready','work'].includes(session.phase))main=f.id==='tub'?'Brush the tub back and forth':'Scrub the '+f.name.toLowerCase()+' in circles';
    if(session.phase==='settle')main=f.name+' clean!';
    roundBox(front,14,13,354,59,13,'rgba(23,30,53,.88)');
    front.fillStyle='#b8e8ed';front.font='600 12px Segoe UI';
    front.fillText(mode==='watch'?'BATHROOM / WALKTHROUGH':'BATHROOM / PLAY',28,33);
    front.fillStyle='#fff5e1';front.font='600 19px Segoe UI';front.fillText(main,28,56);
    const x0=WIDTH-260;
    roundBox(front,x0,13,246,54,13,'rgba(23,30,53,.88)');
    FIXTURES.forEach((item,i)=>{
      const x=x0+15+i*78, complete=session.clean[i]>=1, active=i===session.fi;
      ellipse(front,x+6,30,6,6,complete?'#a3ead0':active?'#ffe9a7':'#68758a');
      front.fillStyle=complete?'#c5f8df':active?'#fff5e1':'#c5ccdf';front.font='600 13px Segoe UI';
      front.fillText(item.name,x+16,35);
      roundBox(front,x+1,47,67,5,2,'#4b5b72');
      const p=67*session.progress[i];
      if(p>0)roundBox(front,x+1,47,p,5,2,complete?'#a3ead0':'#ffe9a7');
    });
  }

  function paintFront() {
    front.clearRect(0,0,WIDTH,HEIGHT);
    if(acting.tubForeground && session.fi===1 &&
        ['ready','work','settle'].includes(session.phase)) {
      // The painted near lip can cover the lower tail. This pass is
      // restricted below the pelvis so the torso, working hand and head
      // stay in front; the brush remains on its own contact layer.
      const lowerTail=new Path2D();
      lowerTail.rect(0,session.root[1]+40,WIDTH,HEIGHT);
      front.save();
      front.clip(tubLip);
      front.clip(lowerTail);
      front.drawImage(dirty,0,0);
      if(session.clean[1]>0&&!acting.staticTub) {
        front.clip(cleanShapes.tub);
        front.clip(dryTubExterior,'evenodd');
        front.globalAlpha=session.clean[1];
        front.drawImage(clean,0,0);
      }
      front.restore();
    }
    lineGuide();
    if(acting.staticTub&&session.fi===1&&session.phase==='settle') {
      const gleam=Math.sin(Math.PI*smooth((session.age-.12)/.67));
      front.save();
      front.globalAlpha=.40*gleam;
      front.fillStyle='#fff8d5';
      for(const [x,y,r] of [[146,248,2.2],[184,259,3],[306,249,2.7]]) {
        front.beginPath();
        front.moveTo(x,y-r*1.65);front.lineTo(x+r,y);
        front.lineTo(x,y+r*1.65);front.lineTo(x-r,y);front.closePath();front.fill();
      }
      front.restore();
    }
    for(const b of session.bubbles){
      const life=(session.time-b.at)/.9;
      front.globalAlpha=(1-life)*.84;
      const point=[b.point[0]+b.phase*life*15,b.point[1]-life*24];
      ellipse(front,...point,3+life*4,acting.tubDepth?2+life*3:3+life*4,'rgba(206,249,250,.42)','#f8fff7');
      front.globalAlpha=1;
    }
    if(mode==='watch'&&session.watchTouch&&mouseTarget){
      if(acting.tubDepth) {
        const f=FIXTURES[session.fi];
        const dot=projectTouch(mouseTarget,f);
        front.lineWidth=1.15;
        ellipse(front,dot[0],dot[1]+2,f.id==='tub'?15:12,f.id==='tub'?4:6,
          'rgba(222,247,245,.08)','rgba(255,250,218,.46)');
        front.lineWidth=1;
      } else ellipse(front,...mouseTarget,19,19,null,'rgba(255,250,218,.85)');
    }
    title();
    if(session.phase==='done'){
      roundBox(front,376,468,272,63,16,'rgba(21,43,52,.91)');
      front.font='600 23px Segoe UI';front.fillStyle='#d7fae3';front.textAlign='center';
      front.fillText('Nicely scrubbed!',512,507);front.textAlign='start';
    }
  }

  let lastGrip=PARK.grip;
  function draw() {
    // Room and the physical tool are painted before the actor, so the palm
    // sits over the handle. Bristles stay visible at the target.
    lastGrip=paintRoom();
    paintActor();
    paintFront();
    // The next frame's room layer reads the unplaced pose.
    pose.placement=null;
    pose.updateWorld(skeleton);
  }

  function pointerAt(e) {
    const r=front.canvas.getBoundingClientRect();
    return [(e.clientX-r.x)*WIDTH/r.width,(e.clientY-r.y)*HEIGHT/r.height];
  }
  front.canvas.addEventListener('pointerdown',e=>{
    if(mode!=='play'||activePointer!==null||e.button!==0)return;
    unlocked=true;
    if(startTouch(pointerAt(e))&&session.phase==='work'){
      activePointer=e.pointerId;front.canvas.setPointerCapture(e.pointerId);
    }
  });
  front.canvas.addEventListener('pointermove',e=>{if(e.pointerId===activePointer)moveTouch(pointerAt(e));});
  for(const event of ['pointerup','pointercancel','lostpointercapture'])front.canvas.addEventListener(event,e=>{
    if(e.pointerId===activePointer)release();
  });
  window.addEventListener('blur',()=>{if(mode==='play')release();});
  document.querySelector('#play').onclick=()=>{unlocked=true;if(mode!=='play')reset('play');};
  document.querySelector('#watch').onclick=()=>{unlocked=true;reset('watch');};
  document.querySelector('#restart').onclick=()=>reset();
  document.querySelector('#look').onchange=e=>setLook(e.target.value);
  document.querySelector('#sound').onclick=e=>{
    sound=!sound;e.target.textContent=sound?'Sound on':'Sound off';
    e.target.setAttribute('aria-pressed',String(sound));
    if(!sound)for(const clip of Object.values(audio))clip.pause();
  };

  reset();
  setLook('Original');
  buildPose('wait',0,0,0,0);
  draw();
  loading.hidden=true;

  function snapshot() {
    const palm=palmAt(session.root);
    const f=FIXTURES[session.fi];
    const bristle=session.held?plus(lastGrip,vector(session.angle,brushLength())):plus(PARK.grip,vector(PARK.angle,BRUSH_REACH));
    const head=rigPoint('head',[22,0]);
    const headPoint=plus(session.root,facingDelta(head));
    const tailPoint=facingDelta(rigPoint('fluke',[16,0]));
    return {mode,skin:session.skin,phase:session.phase,fixture:f.id,fi:session.fi,time:session.time,
      age:session.age,facing:session.facing,turn:session.turn,progress:session.progress.slice(),clean:session.clean.slice(),held:session.held,
      root:session.root.slice(),palm,head:headPoint,brushGrip:session.held?plus(lastGrip,gripOffset()):lastGrip.slice(),
      brushAnchor:lastGrip.slice(),bristles:bristle,angle:session.angle,brushDepth:session.brushDepth,hair:session.hair.slice(),lid:session.lid,attention:session.attention,celebration:session.celebration,
      activeContact:session.phase==='work'&&Boolean(mouseTarget)&&hit(mouseTarget,f),
      projectedContact:session.tip?.slice()??null,pointer:mouseTarget?.slice()??null,
      completed:session.completed.slice(),events:session.events.slice(),pickupError:session.pickupError,
      flightU:session.flightU,flightProgress:session.flightProgress,
      swimArmPose:['screen_left','screen_right'].map(side=>({
        side,
        angles:['_upper_arm','_forearm','_hand'].map(part=>pose.local[index[side+part]].rotation),
        wrist:facingDelta(rigPoint(side+'_hand')),
        shoulder:facingDelta(rigPoint(side+'_upper_arm')),
        elbow:facingDelta(rigPoint(side+'_forearm')),
      })),
      elbow:facingDelta(rigPoint('screen_right_forearm')),
      palmRelative:palmDelta(),
      armAngles:['screen_right_upper_arm','screen_right_forearm','screen_right_hand']
        .map(name=>pose.local[index[name]].rotation),
      tailRelative:tailPoint,assetCount:1,bones:skeleton.bones.length,lastError};
  }

  function meshStrain() {
    const setup=new Pose(skeleton).quads(skeleton);
    const current=new Map(pose.quads(skeleton).map(part=>[part.slot,part]));
    const visibility=assetData.visibility[skeleton.skin??'default'];
    const headSlot=-1;
    if(session.facing<0&&leftHead){
      setup.push({slot:headSlot,triangles:leftHead.triangles,positions:leftHead.rest});
      current.set(headSlot,{positions:leftHead.positions(pose)});
    }
    let low=1,high=1,flips=0,worst='';
    for(const part of setup){
      const slot=part.slot===headSlot?'left_head':skeleton.slots[part.slot].name;
      const active=current.get(part.slot);
      const visible=part.slot===headSlot?Array.from({length:part.triangles.length/3},(_,i)=>i):visibility[slot]??[];
      for(const t of visible){
        const [a,b,c]=part.triangles.slice(t*3,t*3+3);
        const u=minus(part.positions[b],part.positions[a]);
        const v=minus(part.positions[c],part.positions[a]);
        const p=minus(active.positions[b],active.positions[a]);
        const q=minus(active.positions[c],active.positions[a]);
        const base=u[0]*v[1]-u[1]*v[0];
        if(Math.abs(base)<1e-9)continue;
        const A=(p[0]*v[1]-q[0]*u[1])/base,B=(q[0]*u[0]-p[0]*v[0])/base;
        const C=(p[1]*v[1]-q[1]*u[1])/base,D=(q[1]*u[0]-p[1]*v[0])/base;
        const det=A*D-B*C,trace=A*A+B*B+C*C+D*D;
        const hi=Math.sqrt((trace+Math.sqrt(Math.max(0,trace*trace-4*det*det)))/2);
        const lo=Math.abs(det)/hi;
        if(lo<low||hi>high)worst=slot;
        low=Math.min(low,lo);high=Math.max(high,hi);
        flips+=det<=0?1:0;
      }
    }
    return {low,high,flips,worst};
  }

  if(testing) {
    window.bathroomTest={
      snapshot,meshStrain,
      propulsionProof() {
        return [2.15,2.65,3,4.25].map(duration=>{
          const plan=thrustPlan(duration,acting.motor??0),disabled=thrustPlan(duration,0);
          return {duration,driven:plan.total,disabled:disabled.total,
            firstThrust:plan.force.findIndex(force=>force>1)/plan.samples,
            peakSpeed:Math.max(...plan.speeds),finishSpeed:plan.speeds.at(-1)};
        });
      },
      step(count=1){for(let i=0;i<count;i++)update(STEP);draw();return snapshot();},
      reset(nextMode){reset(nextMode);update(0);draw();return snapshot();},
      look:setLook,
      touch:startTouch,move:moveTouch,release,
      surface:(i,a)=>surfacePoint(FIXTURES[i],a),
      stageRect:()=>{const r=front.canvas.getBoundingClientRect();return [r.x,r.y,r.width,r.height];},
      fingerDisk(x,y,radius=22){
        const x0=Math.round(x)-radius,y0=HEIGHT-1-Math.round(y)-radius,side=radius*2+1;
        const pixels=new Uint8Array(side*side*4);
        gl.readPixels(x0,y0,side,side,gl.RGBA,gl.UNSIGNED_BYTE,pixels);
        let covered=0;
        for(let row=0;row<side;row++)for(let col=0;col<side;col++){
          if((row-radius)**2+(col-radius)**2<=radius**2 && pixels[(row*side+col)*4+3]>20)covered++;
        }
        return covered;
      },
      frame(format='image/png',quality=.88){const c=document.createElement('canvas');c.width=WIDTH;c.height=HEIGHT;
        const ctx=c.getContext('2d');ctx.drawImage(room.canvas,0,0);ctx.drawImage(actor,0,0);ctx.drawImage(front.canvas,0,0);
        return c.toDataURL(format,quality);}
    };
  } else {
    let prev=0,lag=0;
    function frame(now){
      if(!prev)prev=now;
      lag+=Math.min(.05,(now-prev)/1000);prev=now;
      while(lag>=STEP){update(STEP);lag-=STEP;}
      draw();
      requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }
} catch(error) {
  loading.textContent=String(error.message||error);
  window.bathroomError=String(error.stack||error);
  console.error(error);
}
