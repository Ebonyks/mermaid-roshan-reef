/* Behaviour tests for a silent interface fixture, not a musical score. */
const assert = require('node:assert/strict');
const Fixture = require('../assets_src/cinematics/battle_of_bands_2026-09-20/ui/rhythm-core.js');
let checks = 0;
function test(name, fn) { fn(); checks++; console.log('PASS '+name); }
test('zero input never registers contact',()=>{const f=new Fixture();f.start();f.advance(120);assert.equal(f.hits,0);assert.ok(f.passed>0);});
test('early, wrong target and late touches do not become hits',()=>{for(const [time,target] of [[2,0],[3.2,1],[3.56,0]]){const f=new Fixture();f.start();f.advance(time);assert.equal(f.press(target,1),'neutral');assert.equal(f.hits,0);}});
test('a touch at actual arrival registers once',()=>{const f=new Fixture();f.start();f.advance(3.2);assert.equal(f.cue().progress,1);assert.equal(f.press(0,7),'contact');f.release(7);assert.equal(f.press(0,8),'neutral');assert.equal(f.hits,1);});
test('a held early finger cannot farm the arrival; second finger ignored',()=>{const f=new Fixture();f.start();f.advance(2.8);f.press(0,1);f.advance(.4);assert.equal(f.press(0,2),'ignored');assert.equal(f.hits,0);f.release(2);assert.equal(f.press(0,1),'ignored');f.release(1);assert.equal(f.press(0,3),'contact');});
test('pause freezes time and cancels held input; resume gives fresh lead',()=>{const f=new Fixture();f.start();f.advance(3.1);f.press(1,1);f.pause();f.advance(60);assert.equal(f.time,3.1);assert.equal(f.held,null);assert.equal(f.press(0,1),'ignored');f.resume();assert.ok(f.arrival-f.time>=1.599);assert.equal(f.press(0,2),'neutral');});
test('miss advances without success or blocking the next cue',()=>{const f=new Fixture();f.start();f.advance(4.1);assert.equal(f.target,1);assert.equal(f.hits,0);assert.equal(f.passed,1);f.advance(3.1);assert.equal(f.press(1,1),'contact');});
test('cancelled touch permits a new intentional contact',()=>{const f=new Fixture();f.start();f.advance(3.2);f.press(2,11);f.cancel();assert.equal(f.press(0,12),'contact');});
test('every fixture arrival maps exactly to contact progress',()=>{const f=new Fixture();f.start();for(let i=0;i<9;i++){f.advance(f.arrival-f.time);assert.equal(f.cue().progress,1);assert.equal(f.target,i%3);f.advance(.81);}});
console.log(`BANDS UI FIXTURE PASS: ${checks} behavioural checks`);
