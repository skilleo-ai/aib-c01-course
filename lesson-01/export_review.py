"""Export a review video from inspected HyperFrames frames and measured speech.

The review captures only changing visual events, then encodes a constant 30 fps
delivery file for broad player compatibility. Static teaching holds reuse their
pixels until the next caption event. No browser actions are simulated.
"""
import json,math,subprocess
from pathlib import Path
R=Path(__file__).resolve().parent
build=R/'renders/review-build';build.mkdir(parents=True,exist_ok=True)
scenes=json.loads((R/'timing.json').read_text())
captions=json.loads((R/'captions.json').read_text())
heroes=sorted((R/'renders/hero-frames').glob('frame-*.png'))
if len(heroes)!=len(scenes):raise ValueError('one inspected hero frame required per scene')
run=lambda args:subprocess.run(args,check=True,cwd=R,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
intro=build/'intro';intro.mkdir(exist_ok=True)
run(['ffmpeg','-v','error','-y','-i','renders/intro-test.mp4','-fps_mode','passthrough',str(intro/'frame-%03d.png')])
introframes=sorted(intro.glob('*.png'))
transitions={}
for i in range(1,len(scenes)):
    directory=build/f'transition-{i:02}';directory.mkdir(exist_ok=True)
    pattern=str(directory/'frame-%03d.png')
    run(['ffmpeg','-v','error','-y','-loop','1','-framerate','30','-i',str(heroes[i-1]),'-loop','1','-framerate','30','-i',str(heroes[i]),'-filter_complex','[0:v][1:v]xfade=transition=fade:duration=0.4:offset=0,format=rgb24','-t','0.4','-threads','1','-filter_complex_threads','1',pattern])
    transitions[i]=sorted(directory.glob('*.png'))
    print('Transition',i,'ready',flush=True)
fps=30;total=scenes[-1]['start']+scenes[-1]['duration'];endframe=math.ceil(total*fps)
events={0,endframe-1}
for i,s in enumerate(scenes):
    tick=round(s['start']*fps)
    events.add(tick)
    if i==0:events.update(range(min(len(introframes),endframe)))
    else:events.update(tick+j for j in range(len(transitions[i])+1))
for c in captions:
    events.add(math.ceil(c['start']*fps));events.add(math.ceil(c['end']*fps))
events.update(range(endframe-30,endframe))
events=sorted(t for t in events if 0<=t<endframe)
def image_for(tick):
    i=max(i for i,s in enumerate(scenes) if round(s['start']*fps)<=tick)
    delta=tick-round(scenes[i]['start']*fps)
    if i==0 and delta<len(introframes):return introframes[delta]
    if i and delta<len(transitions[i]):return transitions[i][delta]
    return heroes[i]
lines=['ffconcat version 1.0']
for i,tick in enumerate(events):
    nexttick=events[i+1] if i+1<len(events) else endframe
    path=image_for(tick)
    lines += [f"file '{path}'",'option framerate 30',f'duration {(nexttick-tick)/fps:.9f}']
lines += [f"file '{image_for(endframe-1)}'",'option framerate 30']
concat=build/'frames.ffconcat';concat.write_text('\n'.join(lines)+'\n')
def ass_time(t):
    cs=round(t*100);sec,cs=divmod(cs,100);minute,sec=divmod(sec,60);hour,minute=divmod(minute,60)
    return f'{hour}:{minute:02}:{sec:02}.{cs:02}'
ass='''[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Inter,32,&H00E8F0F5,&H00E8F0F5,&H002C1D10,&H002C1D10,0,0,0,0,100,100,0,0,3,2,0,2,100,100,22,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
for c in captions:
    text=c['text'].replace('{','').replace('}','').replace('\n',' ')
    ass+=f'Dialogue: 0,{ass_time(c["start"])},{ass_time(c["end"])},Default,,0,0,0,,{text}\n'
(R/'captions.ass').write_text(ass)
output=R/'renders/lesson-01-review.mp4'
filters=f'subtitles=captions.ass:fontsdir=assets/fonts,fade=t=out:st={total-.8:.6f}:d=0.8'
args=['ffmpeg','-v','warning','-y','-safe','0','-f','concat','-i',str(concat),'-i','assets/audio/narration.wav','-vf',filters,'-af','loudnorm=I=-16:TP=-1.5:LRA=11','-fps_mode','cfr','-r','30','-c:v','libx264','-preset','veryfast','-tune','stillimage','-crf','20','-pix_fmt','yuv420p','-video_track_timescale','30000','-c:a','aac','-b:a','192k','-ar','48000','-t',str(total),'-movflags','+faststart',str(output)]
print('Encoding',len(events),'visual events over',round(total,2),'seconds',flush=True)
result=subprocess.run(args,cwd=R,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,text=True)
(build/'encode.log').write_text(result.stderr)
if result.returncode:raise RuntimeError(result.stderr[-5000:])
metadata=dict(duration_seconds=total,visual_events=len(events),size_bytes=output.stat().st_size,frame_rate_mode='constant 30 fps',caption_timing='Measured synthesized phrase boundaries; frame-quantized within 1/30 second',voice='Kokoro af_heart, speed 0.94; local synthesis approved by user',status='review_build_not_expert_approved')
(R/'RENDER.json').write_text(json.dumps(metadata,indent=2)+'\n')
print('Rendered',output,output.stat().st_size,flush=True)
