const {lessonRoot}=await import('./capture/root.mjs');
const fs = require('node:fs');
state.slide01Events=[];
state.video01=await recording.start({page:state.page,outputPath:lessonRoot+'capture/slide01-raw.mp4',frameRate:30,maxSize:1920,aspectRatio:null,clock:'real',audio:false,maxDurationMs:65000});
state.origin01=process.hrtime.bigint();
const elapsed=()=>Number(process.hrtime.bigint()-state.origin01)/1e9;
async function observe(label,locator,holdSeconds,actionStart){
  if(!(await locator.isVisible()))throw Error('Expected teaching content not visible: '+label);
  // Settle the accordion layout before accepting evidence or starting the hold.
  let priorHeight=-1;
  for(let attempt=0;attempt<12;attempt++){
    const geometry=await locator.boundingBox();
    if(geometry && Math.abs(geometry.height-priorHeight)<1 && geometry.y>=178 && geometry.y+geometry.height<=898)break;
    priorHeight=geometry?.height||-1;
    await locator.scrollIntoViewIfNeeded();
    if(geometry && geometry.y<178)await state.page.mouse.wheel(0,geometry.y-190);
    if(geometry && geometry.y+geometry.height>898)await state.page.mouse.wheel(0,geometry.y+geometry.height-880);
    await new Promise(resolve=>setTimeout(resolve,150));
  }
  const geometry=await locator.boundingBox();
  if(!geometry || geometry.y<176 || geometry.y+geometry.height>901 || geometry.x<0 || geometry.x+geometry.width>722)throw Error('Teaching target not fully inside capture viewport: '+label+' '+JSON.stringify(geometry));
  const start=elapsed();
  const box=await locator.boundingBox();
  const text=await locator.innerText();
  const snap=await snapshot({page:state.page,locator});
  const logs=await getLatestLogs({page:state.page,sinceLastCall:true,count:2});
  console.log(label,'verified',snap.slice(0,550),logs);
  await new Promise(resolve=>setTimeout(resolve,holdSeconds*1000));
  state.slide01Events.push({id:label,action_start:actionStart,visible_start:start,end:elapsed(),box,evidence:text,url:state.page.url(),hold_kind:'instructional_reading'});
}
try {
  await observe('positioning',state.page.getByRole('heading',{name:'AWS Certified AI Business Strategist',exact:true}),11,0);
  let actionStart=elapsed();
  const summary=state.page.getByText(/^AWS Certified AI Business Strategist tests your ability to evaluate AI investments/).first();
  await summary.scrollIntoViewIfNeeded();
  await observe('business-decisions',summary,16,actionStart);
  actionStart=elapsed();
  const career=state.page.getByRole('button',{name:'How will the AWS Certified AI Business Strategist help my career?',exact:true});
  await career.click();
  if(await career.getAttribute('aria-expanded')!=='true')throw Error('Career FAQ did not expand');
  console.log(await getLatestLogs({page:state.page,sinceLastCall:true,count:2}));
  const payoff=state.page.getByText(/^More companies are integrating AI across existing roles/).first();
  await payoff.scrollIntoViewIfNeeded();
  await observe('career-value',payoff,16,actionStart);
  state.result01=await state.video01.stop();
  fs.writeFileSync('capture/slide01-events.json',JSON.stringify({viewport:{width:720,height:900},browser_zoom:1.2,result:state.result01,events:state.slide01Events},null,2));
  console.log('SAVED',state.result01);
} catch(error){await state.video01.stop();throw error;}
