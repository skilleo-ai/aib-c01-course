await state.page.setViewportSize({width:720,height:900});
await state.page.evaluate(()=>{document.documentElement.style.zoom='1.2';});
for (const label of ['Who should take this exam?','How will the AWS Certified AI Business Strategist help my career?','How is this different from AWS Certified AI Practitioner?']) {
  const target=state.page.getByRole('button',{name:label,exact:true});
  if(await target.getAttribute('aria-expanded')==='true') {
    await target.click();
    if(await target.getAttribute('aria-expanded')!=='false')throw Error('Panel did not close: '+label);
    console.log('Closed:',label,await getLatestLogs({page:state.page,sinceLastCall:true,count:1}));
  }
}
await state.page.getByRole('heading',{name:'AWS Certified AI Business Strategist',exact:true}).scrollIntoViewIfNeeded();
console.log(await snapshot({page:state.page,search:/AI Business Strategist|Validate the business/}));
console.log(await getLatestLogs({page:state.page,sinceLastCall:true,count:2}));
await state.page.screenshot({path:'/workspace/work/lesson00-square-layout.png',scale:'css'});
