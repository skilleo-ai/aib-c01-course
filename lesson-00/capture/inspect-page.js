console.log('Before:',state.page.url());
state.cdp = await getCDPSession({page:state.page});
await state.cdp.send('Security.setIgnoreCertificateErrors',{ignore:true});
await state.page.goto('https://aws.amazon.com/certification/certified-ai-business-strategist/',{waitUntil:'domcontentloaded'});
console.log('URL:',state.page.url());
console.log(await snapshot({page:state.page}));
console.log('Page logs:',await getLatestLogs({page:state.page,sinceLastCall:true,count:5}));
