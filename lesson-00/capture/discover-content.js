console.log(await snapshot({page:state.page,locator:state.page.getByRole('main')}));
console.log('LOGS:',await getLatestLogs({page:state.page,sinceLastCall:true,count:3}));
require('node:fs').writeFileSync('capture/aws-marketing-research.md',await getPageMarkdown({page:state.page,showDiffSinceLastCall:false}));
console.log('HEADINGS:',await state.page.getByRole('heading').allTextContents());
