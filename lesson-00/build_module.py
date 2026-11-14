"""Build native Skilleo script, Studio data, render props and ASR-derived captions."""
import json,re,math,difflib
from pathlib import Path
R=Path(__file__).resolve().parent
load=lambda p:json.loads((R/p).read_text())
def save(p,v):(R/p).write_text(json.dumps(v,indent=2)+'\n')
def norm(w):return re.sub('[^a-z0-9]','',w.lower())
slides=load('narration-timing.json');props={'moduleTitle':'Lesson 0 — Is this course for you?','slides':[]};module={'id':'module-0-aib-intro-preview','title':props['moduleTitle'],'slides':[]};doc={'format':'skilleo-course-script/v1','title':'AWS Certified AI Business Strategist (AIB-C01)','modules':[]}
all_captions=[];global_offset=0;checks=[]
for slide in slides:
 n=slide['number'];duration=slide['duration'];raw=load(f'slide{n}-word-timings.json')
 authored=' '.join(b['text'] for b in slide['beats']).split()
 same=[norm(w) for w in authored]==[norm(w['word']) for w in raw]
 if not same:raise ValueError('ASR differs from authored narration; review transcript before assembly: '+n)
 words=[{**w,'word':text} for text,w in zip(authored,raw)]
 save(f'slide{n}-word-timings-reviewed.json',words)
 timings=[]
 for i,(beat,text) in enumerate(zip(slide['beats'],slide['bullets'])):
  candidates=[w for w in words if w['start']>=beat['audio_start']-.25 and w['start']<beat['audio_end']]
  if not candidates:raise ValueError('No ASR evidence for bullet cue')
  timings.append({'text':text,'start':candidates[0]['start'],'end':candidates[-1]['end']})
 for i in range(len(timings)-1):timings[i]['end']=timings[i+1]['start']
 timings[-1]['end']=duration
 video=f'media/slide{n}-screen.mp4';audio=f'audio/slide{n}-narration.wav'
 props_slide={'id':slide['id'],'type':'content-image','templateId':'bullets-visual-architecture-focus','templateFamily':'BULLETS_VISUAL','title':slide['title'],'script':' '.join(b['text'] for b in slide['beats']),'bullets':slide['bullets'],'durationSec':duration,'audioUrl':audio,'theme':'dark','figureAccent':'teal','visual':'image','pictureRoll':{'shots':[{'id':f'playwriter-{n}','index':0,'start_sec':0,'end_sec':duration,'video_url':video}]},'wordTimings':words,'bulletTimings':timings}
 props['slides'].append(props_slide)
 studio={'id':slide['id'],'type':'content-image','template_id':props_slide['templateId'],'template_family':'BULLETS_VISUAL','title':slide['title'],'script':props_slide['script'],'bullets':slide['bullets'],'duration_sec':duration,'audio_url':audio,'video_url':video,'theme':'dark','figure_accent':'teal','visual':'image','picture_roll':props_slide['pictureRoll'],'word_timings':words,'bullet_timings':timings}
 module['slides'].append(studio)
 # Short caption phrases use reviewed text with actual ASR word boundaries.
 current=[]
 for word in words:
  if current and (word['start']-current[-1]['end']>.55 or len(' '.join(w['word'] for w in current+[word]))>90):
   all_captions.append({'start':global_offset+current[0]['start'],'end':global_offset+current[-1]['end'],'text':' '.join(w['word'] for w in current)});current=[]
  current.append(word)
  if word['word'].endswith(('.', '?','!')):
   all_captions.append({'start':global_offset+current[0]['start'],'end':global_offset+current[-1]['end'],'text':' '.join(w['word'] for w in current)});current=[]
 if current:all_captions.append({'start':global_offset+current[0]['start'],'end':global_offset+current[-1]['end'],'text':' '.join(w['word'] for w in current)})
 checks.append({'slide_id':slide['id'],'asr_words':len(words),'transcript_matches_authored_words':same,'all_speech_fits_recorded_windows':all(b['audio_end']<=b['available_end'] for b in slide['beats']),'visual_duration':duration})
 global_offset+=math.ceil(duration*30-1e-9)/30
save('render-props.json',props);save('module-0-studio.json',module)
doc['modules']=[{'id':module['id'],'title':module['title'],'slides':[{k:s[k] for k in ['id','title','type','script','bullets','visual']} for s in module['slides']]}];save('module-0-script.json',doc)
lines=['# AWS Certified AI Business Strategist (AIB-C01)','','> format: skilleo-course-script/v1','','## Module: '+module['title'],'<!-- id: '+module['id']+' -->','']
for s in module['slides']:
 lines += ['### Slide: '+s['title'],'<!-- id: '+s['id']+' -->','<!-- type: content-image -->','<!-- visual: image -->','',s['script'],'']+['- '+b for b in s['bullets']]+['']
(R/'module-0.md').write_text('\n'.join(lines)+'\n')
save('figures.json',{'format':'skilleo-figures/v1','figure_count':0,'figures':{}})
save('caption-cues.json',all_captions)
def stamp(t,sep=','):
 ms=round(t*1000);seconds,ms=divmod(ms,1000);minutes,seconds=divmod(seconds,60);hours,minutes=divmod(minutes,60);return f'{hours:02}:{minutes:02}:{seconds:02}{sep}{ms:03}'
(R/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["text"]}' for i,c in enumerate(all_captions))+'\n')
(R/'captions.vtt').write_text('WEBVTT\n\n'+'\n\n'.join(f'{stamp(c["start"],".")} --> {stamp(c["end"],".")}\n{c["text"]}' for c in all_captions)+'\n')
save('validation.json',{'slides':checks,'total_duration_seconds':global_offset,'figures':'None: video-backed slides. animation_synced is not set on nonexistent figures.','ASR':'Actual local faster-whisper base.en word timings; reviewed text differs only in punctuation/capitalization.'})
print('Prepared',len(slides),'native slides;',global_offset,'seconds;',len(all_captions),'caption cues')
