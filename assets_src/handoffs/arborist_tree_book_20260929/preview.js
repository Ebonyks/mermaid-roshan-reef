let saved;try{saved=JSON.parse(localStorage.getItem('treebook_review_v1'))}catch{}
const m=new TreeBookModel(saved),game=document.querySelector('#game'),choices=document.querySelector('#choices'),patient=document.querySelector('#patient'),title=document.querySelector('#title'),hint=document.querySelector('#hint');
let speaking=false,locked=false;
const lines=["Which tree is this? Find the same tree!","What is wrong with this leaf? Find the orange spots!","Orange spots need leaf spray. Find the same sticker!","Let's help the tree. Tap the tree to spray its leaves!","The tree feels better! A tree sticker for my book!"];
const trees=['','references/lagoon_tree_bigleaf_maple.png','references/lagoon_tree_pacific_dogwood.png','references/sky_lagoon_tree_sticker_tall_v1.png'];
const names=['Pearl-heart tree','Maple tree','Blossom tree','Pine tree'];const order=[[2,0,3,1],[3,2,0,1],[0,1,3,2]];
function say(s){if(speaking&&'speechSynthesis'in window){speechSynthesis.cancel();speechSynthesis.speak(new SpeechSynthesisUtterance(s));}}
function save(){try{localStorage.setItem('treebook_review_v1',JSON.stringify(m.snapshot()))}catch{}}
function art(i,kind){const bounds=kind==='medicine'?[[0,460,492,427],[500,430,387,457],[895,440,440,447],[1340,440,434,447]]:[[0,0,443,444],[443,0,444,430],[887,0,443,444],[1330,0,444,430]];const r=bounds[i];return '<svg class="sprite" viewBox="'+r.join(' ')+'" aria-hidden="true"><image href="new_art/leaf_medicine.png" width="1774" height="887"/></svg>';}
function render(){
 game.className=m.stage===2?'med':m.stage===3?'treat':m.stage===4?'done':'';
 title.textContent=['Which tree?','What is wrong?','Which medicine?','Time to help!','Feeling better!'][m.stage];hint.textContent=lines[m.stage];
 document.querySelectorAll('#progress i').forEach((x,i)=>x.className=m.stage>i?'done':'');
 choices.innerHTML='';
 patient.disabled=m.stage!==3;
 if(m.stage<3)for(const i of order[m.stage]){
 const b=document.createElement('button');b.className='choice';b.dataset.index=i;b.setAttribute('aria-label',m.stage===0?names[i]:['Blue droop','Orange spots','Green bug','Yellow leaf'][i]+(m.stage===2?' medicine':''));
 b.innerHTML=m.stage===0?(i===0?'<span class="sprite tree"></span>':'<img alt="" src="'+trees[i]+'">'):art(i,m.stage===1?'leaf':'medicine');
 b.onclick=()=>{if(locked)return;if(!m.pick(i,true)){b.classList.remove('wrong');void b.offsetWidth;b.classList.add('wrong');hint.textContent=m.stage===0?'Look at the tree’s shape and heart!':'Look for the orange spots!';say(hint.textContent);help();return;}save();render();say(lines[m.stage]);};
 choices.append(b);
 }
 if(m.stage===4)document.querySelector('#explain').innerHTML='<span class="sprite tree" style="background-position:100% 0;width:100%"></span>';
 help();
}
function help(){const target=m.stage<3?choices.querySelector('[data-index="'+m.correct[m.stage]+'"]'):m.stage===3?patient:null;if(target){target.classList.toggle('glow',m.assist>=1);target.classList.toggle('hand',m.assist>=2);}}
patient.onclick=()=>{if(m.stage!==3||locked)return;locked=true;hint.textContent='Spray, spray!';say('Spray, spray!');setTimeout(()=>{m.treat(true);save();render();say(lines[4]);locked=false},600)};
document.querySelector('#voice').onclick=e=>{speaking=!speaking;e.target.textContent=speaking?'Voice on':'Voice off';e.target.setAttribute('aria-pressed',String(speaking));if(speaking)say(lines[m.stage]);else if('speechSynthesis'in window)speechSynthesis.cancel()};
document.querySelector('#reset').onclick=()=>{try{localStorage.removeItem('treebook_review_v1')}catch{}location.reload()};
setInterval(()=>{if(!document.hidden&&!locked){m.tick(.25);help()}},250);render();

