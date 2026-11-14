state.page = await context.newPage();
await state.page.setViewportSize({width:1920,height:1080});
await state.page.goto('https://aws.amazon.com/certification/certified-ai-business-strategist/', {waitUntil:'domcontentloaded'});
console.log('URL:',state.page.url());
console.log(await snapshot({page:state.page}));
console.log('Page logs:',await getLatestLogs({page:state.page,sinceLastCall:true,count:8}));
