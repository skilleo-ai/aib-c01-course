await state.page.setViewportSize({width:720,height:900});
await state.page.evaluate(()=>{document.documentElement.style.zoom='1.2';});
const text=state.page.getByText(/^These two certifications are built for different purposes and validate different skills/).first();
await text.scrollIntoViewIfNeeded();
console.log(await snapshot({page:state.page,locator:text}));
console.log(await inspect({locator:text}));
console.log(await getLatestLogs({page:state.page,sinceLastCall:true,count:2}));
await state.page.screenshot({path:'/workspace/work/lesson00-comparison-readable.png',scale:'css'});
