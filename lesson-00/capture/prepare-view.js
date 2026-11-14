await state.page.setViewportSize({width:1280,height:900});
await state.page.evaluate(()=>{document.documentElement.style.zoom='1.15';});
await state.page.getByRole('heading',{name:'AWS Certified AI Business Strategist',exact:true}).scrollIntoViewIfNeeded();
console.log(await snapshot({page:state.page,search:/heading|beta|business|who|practitioner|foundational|coding|experience/i}));
console.log(await getLatestLogs({page:state.page,sinceLastCall:true,count:3}));
console.log(await inspect({locator:state.page.getByRole('heading',{name:'AWS Certified AI Business Strategist',exact:true})}));
await state.page.screenshot({path:'/workspace/work/lesson00-marketing-layout.png',scale:'css'});
