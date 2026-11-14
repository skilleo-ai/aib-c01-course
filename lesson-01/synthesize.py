"""Local review narration with captions timed to independently synthesized phrases.

Install requirements-audio.txt; pass the two Kokoro model paths as arguments.
No cloud account or paid provider is used. Audio and timing are generated together.
"""
import json,re,sys
from pathlib import Path
import numpy as np
import soundfile as sf
import onnxruntime as rt
import kokoro_onnx

R=Path(__file__).resolve().parent
opts=rt.SessionOptions();opts.intra_op_num_threads=4;opts.inter_op_num_threads=1
kokoro_onnx.create_session=lambda path:rt.InferenceSession(path,sess_options=opts,providers=['CPUExecutionProvider'])
model=kokoro_onnx.Kokoro(sys.argv[1],sys.argv[2])
scenes=json.loads((R/'scenes.json').read_text())
sample_rate=24000
position=0;captions=[];full=[]

def chunks(text):
    parts=re.split(r'(?<=[.!?])\s+',text)
    result=[]
    for part in parts:
        if len(part)<=185:result.append(part);continue
        words=part.split(); current=[]
        for word in words:
            if len(' '.join(current+[word]))>175:
                result.append(' '.join(current));current=[]
            current.append(word)
        if current:result.append(' '.join(current))
    return result

for s in scenes:
    start=position/sample_rate
    prefix=np.zeros(round(.75*sample_rate),dtype=np.float32)
    samples=[prefix];position+=len(prefix)
    for index,text in enumerate(chunks(s['narration'])):
        file=R/'assets/audio'/f'{s["id"]}-p{index:02}.wav'
        spoken=re.sub(r'\bAI\b','A I',text)
        spoken=re.sub(r'\bML\b','M L',spoken)
        if file.exists():audio,rate=sf.read(file,dtype='float32')
        else:
            audio,rate=model.create(spoken,voice='af_heart',speed=.94,lang='en-us')
            sf.write(file,audio,rate)
        if rate!=sample_rate:raise ValueError('inconsistent sample rate')
        t0=position/sample_rate
        samples.append(audio);position+=len(audio)
        captions.append(dict(start=round(t0,3),end=round(position/sample_rate,3),text=text,scene=s['id']))
        pause=np.zeros(round(.10*sample_rate),dtype=np.float32)
        samples.append(pause);position+=len(pause)
    silence=np.zeros(round(s['hold']*sample_rate),dtype=np.float32)
    samples.append(silence);position+=len(silence)
    audio=np.concatenate(samples);full.append(audio)
    sf.write(R/'assets/audio'/f'{s["id"]}.wav',audio,sample_rate)
    s.update(start=round(start,6),duration=round(len(audio)/sample_rate,6),audio=f'assets/audio/{s["id"]}.wav')
    (R/'timing.json').write_text(json.dumps(scenes,indent=2)+'\n')
    (R/'captions.json').write_text(json.dumps(captions,indent=2)+'\n')
    print(s['id'],round(len(audio)/sample_rate,2),'seconds',flush=True)
sf.write(R/'assets/audio/narration.wav',np.concatenate(full),sample_rate)
def timestamp(t,sep=','):
    ms=round(t*1000);seconds,ms=divmod(ms,1000);minutes,seconds=divmod(seconds,60);hours,minutes=divmod(minutes,60)
    return f'{hours:02}:{minutes:02}:{seconds:02}{sep}{ms:03}'
(R/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{timestamp(c["start"])} --> {timestamp(c["end"])}\n{c["text"]}' for i,c in enumerate(captions))+'\n')
(R/'captions.vtt').write_text('WEBVTT\n\n'+'\n\n'.join(f'{timestamp(c["start"],".")} --> {timestamp(c["end"],".")}\n{c["text"]}' for c in captions)+'\n')
print('TOTAL',round(position/sample_rate,2),'seconds',flush=True)
