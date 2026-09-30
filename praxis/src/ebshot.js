const { chromium } = require('playwright');
const path=require('path');
(async()=>{
  const b=await chromium.launch();
  const f='file://'+path.join(__dirname,'..','PRAXIS_Vol01_창간특집호_ebook.html');
  for (const [w,h,name,hash] of [[1440,900,'desk','#p=1'],[1440,900,'desk2','#p=8'],[390,844,'mob','#p=5']]) {
    const p=await b.newPage({viewport:{width:w,height:h}});
    await p.goto(f+hash); await p.waitForTimeout(1500);
    await p.screenshot({path:path.join(__dirname,'_build','eb_'+name+'.png')});
    if(name==='desk2'){await p.click('#tocBtn');await p.waitForTimeout(500);await p.screenshot({path:path.join(__dirname,'_build','eb_toc.png')});}
    await p.close();
  }
  await b.close();
})();
