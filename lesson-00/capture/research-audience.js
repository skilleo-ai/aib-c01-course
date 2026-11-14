await state.page.getByRole('button',{name:'Who should take this exam?',exact:true}).click();
console.log('AUDIENCE:',await snapshot({page:state.page,search:/who|experience|coding|AI initiatives|months|product|managers|required|prior/i}));
console.log(await getLatestLogs({page:state.page,sinceLastCall:true,count:3}));
require('node:fs').writeFileSync('capture/audience-snapshot.txt',await snapshot({page:state.page,locator:state.page.getByRole('main'),showDiffSinceLastCall:false}));
