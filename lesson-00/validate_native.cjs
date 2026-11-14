// Validate against Skilleo's real script importer without changing its source.
const fs=require('node:fs');const path=require('node:path');
const studio=path.resolve(process.argv[2]);
const ts=require(path.join(studio,'course-video/node_modules/typescript'));
const compile=(module,filename)=>{
 const result=ts.transpileModule(fs.readFileSync(filename,'utf8'),{fileName:filename,compilerOptions:{module:ts.ModuleKind.CommonJS,target:ts.ScriptTarget.ES2022,jsx:ts.JsxEmit.ReactJSX,esModuleInterop:true,resolveJsonModule:true}});
 module._compile(result.outputText,filename);
};
require.extensions['.ts']=compile;require.extensions['.tsx']=compile;
const io=require(path.join(studio,'src/courseScriptIo.ts'));
const root=__dirname;
const doc=io.parseCourseScriptMarkdown(fs.readFileSync(path.join(root,'module-0.md'),'utf8'));
const expected=JSON.parse(fs.readFileSync(path.join(root,'module-0-script.json'),'utf8'));
if(doc.modules.length!==1 || doc.modules[0].slides.length!==2)throw Error('Expected one two-slide sample module');
for(let i=0;i<2;i++){
 const a=doc.modules[0].slides[i],b=expected.modules[0].slides[i];
 for(const key of ['id','title','type','script','visual'])if(a[key]!==b[key])throw Error('Round-trip mismatch: '+key);
 if(JSON.stringify(a.bullets)!==JSON.stringify(b.bullets))throw Error('Bullet mismatch');
}
const native=io.courseScriptDocToModules(doc);
if(native[0].slides.some(s=>s.type!=='content-image' || s.visual!=='image'))throw Error('Native importer changed presentation type');
const report={status:'passed',parser:'Skilleo parseCourseScriptMarkdown + courseScriptDocToModules',module_id:doc.modules[0].id,slide_count:2,stable_ids_preserved:true,narration_and_bullets_preserved:true,media_binding:'Markdown importer deliberately does not attach recordings, audio or measured timing. These are supplied separately in module-0-studio.json and assets manifest.'};
fs.writeFileSync(path.join(root,'native-import-validation.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify(report,null,2));
