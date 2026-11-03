/* Render authored HTML cover layouts; raster source art is never edited. */
const fs=require('fs'),path=require('path'),{pathToFileURL}=require('url');
const {chromium}=require('C:/Users/Peter/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{
 const v=__dirname;fs.mkdirSync(path.join(v,'proofs'),{recursive:true});
 const browser=await chromium.launch({headless:true,channel:'msedge'});
 const page=await browser.newPage({viewport:{width:1484,height:1060},deviceScaleFactor:1});
 const checks=[];
 for(const id of ['A','B']){
  await page.goto(pathToFileURL(path.join(v,`REAR_${id}.html`)).href);
  await page.evaluate(()=>document.fonts.ready);
  await page.waitForFunction(()=>[...document.images].every(i=>i.complete));
  await page.locator('#cover').screenshot({path:path.join(v,'proofs',`rear_${id}.png`)});
  const result=await page.evaluate((id)=>{const e=document.querySelector('.copy'),c=document.createElement('canvas').getContext('2d');c.font=getComputedStyle(e).font;return {id,font:document.fonts.check('58.8889px Sniglet'),cover:document.querySelector('#cover').getBoundingClientRect().toJSON(),text:e.getBoundingClientRect().toJSON(),copy:e.innerText,lineWidths:e.innerText.split('\n').map(t=>c.measureText(t).width)};},id);
  if(!result.font||result.text.bottom>989.34||result.lineWidths.some(w=>w>result.text.width))throw new Error('Caption overflow '+JSON.stringify(result));
  checks.push(result);
  await page.locator('.copy').evaluate(e=>e.style.visibility='hidden');
  await page.locator('#cover').screenshot({path:path.join(v,'proofs',`rear_${id}_art.png`)});
 }
 // Zoom of the actual composed cameo for direct contour/occlusion inspection.
 await page.goto(pathToFileURL(path.join(v,'REAR_A.html')).href);
 await page.evaluate(()=>{const e=document.querySelector('#cover');e.style.transform='translate(-3800px,-2440px) scale(4)';e.style.transformOrigin='0 0';document.querySelector('.copy').style.visibility='hidden';});
 await page.screenshot({path:path.join(v,'proofs','cameo_zoom.png')});
 await page.goto(pathToFileURL(path.join(v,'STORY_REVIEW.html')).href);
 await page.setViewportSize({width:1400,height:1000});
 await page.screenshot({path:path.join(v,'proofs','review_top.png')});
 fs.writeFileSync(path.join(v,'layout_checks.json'),JSON.stringify(checks,null,2)+'\n');
 await browser.close();console.log('Two native cover proofs and review/contour views rendered.');
})().catch(e=>{console.error(e);process.exit(1);});
