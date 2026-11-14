const {lessonRoot}=await import('./capture/root.mjs');
state.test = await recording.start({page:state.page,outputPath:lessonRoot+'capture/recorder-test.mp4',frameRate:30,maxSize:1920,aspectRatio:null,clock:'manual'});
await state.test.wait(1800);
state.testResult=await state.test.stop();
console.log(state.testResult);
