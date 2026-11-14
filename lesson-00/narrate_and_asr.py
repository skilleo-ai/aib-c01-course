"""Generate local speech AFTER locked Playwriter edit timelines, then derive ASR cues."""
import json,re,sys,subprocess,math
from pathlib import Path
import numpy as np
import soundfile as sf
import onnxruntime as rt
import kokoro_onnx
from faster_whisper import WhisperModel
R=Path(__file__).resolve().parent
slides=json.loads((R/'narration.json').read_text())
opts=rt.SessionOptions();opts.intra_op_num_threads=2;opts.inter_op_num_threads=1
kokoro_onnx.create_session=lambda path:rt.InferenceSession(path,sess_options=opts,providers=['CPUExecutionProvider'])
voice=kokoro_onnx.Kokoro(sys.argv[1],sys.argv[2]);rate=24000
for slide in slides:
    number=slide['number'];timeline=json.loads((R/f'capture/slide{number}-timeline.json').read_text())
    assert (R/timeline['edited_asset']).is_file(),'Capture must be edited before narration'
    duration=timeline['edited_duration'];audio=np.zeros(round(duration*rate),dtype=np.float32)
    for index,beat in enumerate(slide['beats']):
        event=next(e for e in timeline['events'] if e['id']==beat['event'])
        start=event['visible_start']+.85
        end=timeline['events'][index+1]['action_start']-.3 if index+1<len(timeline['events']) else duration-.5
        spoken=re.sub(r'\bAWS\b','A.W.S.',beat['text'])
        file=R/f'assets/audio/slide{number}-beat{index+1}.wav'
        cache=file.with_suffix('.txt')
        cache_key=json.dumps({'text':spoken,'voice':'af_heart','speed':.98,'language':'en-us'},sort_keys=True)
        if file.exists() and cache.exists() and cache.read_text()==cache_key:samples,sample_rate=sf.read(file,dtype='float32')
        else:
            samples,sample_rate=voice.create(spoken,voice='af_heart',speed=.98,lang='en-us')
            sf.write(file,samples,sample_rate)
            cache.write_text(cache_key)
        seconds=len(samples)/sample_rate
        print(number,beat['event'],'speech',round(seconds,2),'available',round(end-start,2),flush=True)
        if seconds>end-start:raise ValueError(f'Narration does not fit {number}/{beat["event"]}; revise text, not the visual timeline')
        offset=round(start*rate);audio[offset:offset+len(samples)]=samples
        beat.update(audio_start=start,audio_end=start+seconds,available_end=end,measured_seconds=seconds)
    sf.write(R/f'assets/audio/slide{number}-narration-raw.wav',audio,rate)
    subprocess.run(['ffmpeg','-v','error','-y','-i',str(R/f'assets/audio/slide{number}-narration-raw.wav'),'-af','loudnorm=I=-16:TP=-1.5:LRA=11','-ar','48000',str(R/f'assets/audio/slide{number}-narration.wav')],check=True)
    slide['duration']=duration
(R/'narration-timing.json').write_text(json.dumps(slides,indent=2)+'\n')
print('Speech fitted. Starting actual ASR.',flush=True)
asr=WhisperModel('base.en',device='cpu',compute_type='int8',cpu_threads=2,download_root='/workspace/work/whisper-models')
for slide in slides:
    number=slide['number']
    pcm=subprocess.check_output(['ffmpeg','-v','error','-i',str(R/f'assets/audio/slide{number}-narration.wav'),'-f','f32le','-ac','1','-ar','16000','pipe:1'])
    waveform=np.frombuffer(pcm,dtype=np.float32).copy()
    segments,info=asr.transcribe(waveform,language='en',word_timestamps=True,vad_filter=True,beam_size=5)
    words=[]
    for segment in segments:
        for word in segment.words or []:
            words.append({'word':word.word.strip(),'start':round(word.start,3),'end':round(word.end,3)})
    if not words:raise ValueError('ASR returned no word timings')
    (R/f'slide{number}-word-timings.json').write_text(json.dumps(words,indent=2)+'\n')
    print('ASR',number,len(words),'words:', ' '.join(w['word'] for w in words),flush=True)
print('Narration and ASR complete',flush=True)
