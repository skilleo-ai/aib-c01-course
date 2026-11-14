const {lessonRoot}=await import('./capture/root.mjs');
const fs=require('node:fs');
const career=state.page.getByRole('button',{name:'How will the AWS Certified AI Business Strategist help my career?',exact:true});
if(await career.getAttribute('aria-expanded')==='true') {
  await career.click();
  if(await career.getAttribute('aria-expanded')!=='false')throw Error('Career panel did not close');
  console.log(await getLatestLogs({page:state.page,sinceLastCall:true,count:2}));
}
const who=state.page.getByRole('button',{name:'Who should take this exam?',exact:true});
await who.scrollIntoViewIfNeeded();
console.log(await snapshot({page:state.page,search:/Who should take|How is this different/}));
console.log(await getLatestLogs({page:state.page,sinceLastCall:true,count:2}));
state.slide02Events=[];
state.video02=await recording.start({page:state.page,outputPath:lessonRoot+'capture/slide02-raw.mp4',frameRate:30,maxSize:1920,aspectRatio:null,clock:'real',audio:false,maxDurationMs:70000});
state.origin02=process.hrtime.bigint();
const elapsed=()=>Number(process.hrtime.bigint()-state.origin02)/1e9;
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
  const start=elapsed();const box=await locator.boundingBox();const text=await locator.innerText();
  console.log('VERIFIED',label,(await snapshot({page:state.page,locator})).slice(0,450));
  console.log(await getLatestLogs({page:state.page,sinceLastCall:true,count:2}));
  await new Promise(resolve=>setTimeout(resolve,holdSeconds*1000));
  state.slide02Events.push({id:label,action_start:actionStart,visible_start:start,end:elapsed(),box,evidence:text,url:state.page.url(),hold_kind:'instructional_reading'});
}
try{
  let actionStart=elapsed();
  await who.click();
  if(await who.getAttribute('aria-expanded')!=='true')throw Error('Audience FAQ did not open');
  console.log(await getLatestLogs({page:state.page,sinceLastCall:true,count:2}));
  const audience=state.page.getByText(/^Professionals who drive or aspire to drive AI outcomes in their organization, whether/).last();
  await audience.scrollIntoViewIfNeeded();
  await observe('audience',audience,16,actionStart);
  actionStart=elapsed();
  const experience=state.page.getByText(/^The target candidate should have a basic familiarity with AI concepts/).first();
  await experience.scrollIntoViewIfNeeded();
  await observe('entry-expectations',experience,14,actionStart);
  actionStart=elapsed();
  const comparison=state.page.getByRole('button',{name:'How is this different from AWS Certified AI Practitioner?',exact:true});
  await comparison.click();
  if(await comparison.getAttribute('aria-expanded')!=='true')throw Error('Comparison FAQ did not open');
  console.log(await getLatestLogs({page:state.page,sinceLastCall:true,count:2}));
  const differences=state.page.getByText(/^These two certifications are built for different purposes and validate different skills/).first();
  await differences.scrollIntoViewIfNeeded();
  await observe('certification-landscape',differences,21,actionStart);
  state.result02=await state.video02.stop();
  fs.writeFileSync('capture/slide02-events.json',JSON.stringify({viewport:{width:720,height:900},browser_zoom:1.2,result:state.result02,events:state.slide02Events},null,2));
  console.log('SAVED',state.result02);
}catch(error){await state.video02.stop();throw error;}
