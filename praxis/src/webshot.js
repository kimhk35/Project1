const { chromium } = require('playwright'); const path=require('path');
(async()=>{ const b=await chromium.launch(); const p=await b.newPage({viewport:{width:390,height:844},deviceScaleFactor:1});
 await p.goto('file://'+path.join(__dirname,'..','PRAXIS_Vol01_창간특집호.html')); await p.waitForTimeout(1200);
 for (const id of ['p-cover','p-cover-story','p-spot','p-radar2']) { await p.evaluate(i=>document.getElementById(i).scrollIntoView({behavior:'instant'}),id); await p.waitForTimeout(600);
   await p.screenshot({path:path.join(__dirname,'_build','web_'+id+'.png')}); }
 const w=await p.evaluate(()=>document.documentElement.scrollWidth); console.log('scrollWidth',w); await b.close(); })();
