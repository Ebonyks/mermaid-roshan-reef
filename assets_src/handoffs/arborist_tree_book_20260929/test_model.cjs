const fs=require('fs'),vm=require('vm'),assert=require('assert');
vm.runInThisContext(fs.readFileSync(__dirname+'/model.js','utf8'));
const M=globalThis.TreeBookModel;
for(let stage=0;stage<3;stage++){
 const m=new M({stage}),before=m.snapshot();
 m.tick(600);assert.equal(m.stage,stage);assert.equal(m.assist,2);
 assert.equal(m.pick(m.correct[stage],false),false);assert.deepEqual(m.snapshot(),before);
 for(let i=0;i<4;i++)if(i!==m.correct[stage]){assert.equal(m.pick(i,true),false);assert.equal(m.stage,stage)}
 assert.equal(m.pick(m.correct[stage],true),true);assert.equal(m.stage,stage+1);
 assert.equal(new M(m.snapshot()).stage,stage+1);
}
const m=new M();m.tick(4.9);assert.equal(m.assist,0);m.tick(.1);assert.equal(m.assist,1);m.pick(3,true);assert.equal(m.assist,1);m.tick(5);assert.equal(m.assist,2);
const t=new M({stage:3});assert.equal(t.treat(false),false);t.tick(100);assert.equal(t.stage,3);assert.equal(t.treat(true),true);assert.equal(t.treat(true),false);
assert.equal(new M({stage:999}).stage,4);assert.equal(new M({stage:-99}).stage,0);
console.log('PASS: three-stage right/wrong/passive/assistance/resume and treatment checks. No browser or Godot validation claimed.');

