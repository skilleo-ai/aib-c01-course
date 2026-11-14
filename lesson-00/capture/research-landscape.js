await state.page.getByRole('button',{name:'How is this different from AWS Certified AI Practitioner?',exact:true}).click();
console.log(await snapshot({page:state.page,search:/practitioner|foundational|strategist|complement|certification|technical/i}));
console.log(await getLatestLogs({page:state.page,sinceLastCall:true,count:3}));
require('node:fs').writeFileSync('capture/landscape-snapshot.txt',await snapshot({page:state.page,locator:state.page.getByRole('main'),showDiffSinceLastCall:false}));
