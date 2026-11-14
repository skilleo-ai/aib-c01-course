await state.page.getByRole('button',{name:'How will the AWS Certified AI Business Strategist help my career?',exact:true}).click();
console.log(await snapshot({page:state.page,search:/career|business|judgment|lead|position|recogn|organization|hiring|earn/i}));
console.log(await getLatestLogs({page:state.page,sinceLastCall:true,count:3}));
require('node:fs').writeFileSync('capture/career-snapshot.txt',await snapshot({page:state.page,locator:state.page.getByRole('main'),showDiffSinceLastCall:false}));
