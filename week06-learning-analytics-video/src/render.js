const {chromium}=require('playwright-core'); const {spawn}=require('child_process');
const FF='/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2';
(async()=>{
 const [f0,f1,out]=[+process.argv[2],+process.argv[3],process.argv[4]]; const FPS=30;
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
 const p=await b.newPage({viewport:{width:1920,height:1080}});
 await p.goto('file://'+process.cwd()+'/video/index.html'); await p.evaluate(()=>document.fonts.ready);
 const ff=spawn(FF,['-y','-f','image2pipe','-framerate',''+FPS,'-c:v','mjpeg','-i','-','-c:v','libx264','-preset','medium','-crf','19','-pix_fmt','yuv420p','-r',''+FPS,out],{stdio:['pipe','ignore','ignore']});
 for(let f=f0;f<f1;f++){ await p.evaluate(t=>render(t),f/FPS); const buf=await p.screenshot({type:'jpeg',quality:92});
   if(!ff.stdin.write(buf)) await new Promise(r=>ff.stdin.once('drain',r)); if(f%300==0) console.log(out,f); }
 ff.stdin.end(); await new Promise(r=>ff.on('close',r)); await b.close();
})();
