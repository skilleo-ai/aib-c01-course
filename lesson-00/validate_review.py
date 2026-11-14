"""Check recording-first sample contracts; optionally inspect delivered media."""
import argparse,hashlib,json,math,re,subprocess
from pathlib import Path
R=Path(__file__).resolve().parent

def validate(metadata_only=False):
 load=lambda p:json.loads((R/p).read_text())
 errors=[];slides=load('narration-timing.json');props=load('render-props.json');studio=load('module-0-studio.json');manifest=load('asset-manifest.json')
 if len(slides)!=2 or len(props['slides'])!=2 or len(studio['slides'])!=2:errors.append('Expected two review slides')
 expected_ids=[s['id'] for s in slides]
 if expected_ids!=[s['id'] for s in props['slides']] or expected_ids!=[s['id'] for s in studio['slides']]:errors.append('Native slide IDs differ')
 for slide,p,asset in zip(slides,props['slides'],manifest['slides']):
  n=slide['number'];timeline=load(f'capture/slide{n}-timeline.json');words=load(f'slide{n}-word-timings-reviewed.json')
  for beat in slide['beats']:
   if beat['audio_end']>beat['available_end']+.001:errors.append('Narration exceeds existing visual window')
  for event in timeline['events']:
   box=event['box'];view=timeline['viewport']
   if box['y']<176 or box['x']<0 or box['x']+box['width']>view['width']+2 or box['y']+box['height']>view['height']+2:errors.append('Incomplete teaching target in accepted recording')
   if event['hold_kind']!='instructional_reading':errors.append('Unexpected wait type')
  if any(w['end']<w['start'] or w['start']<0 or w['end']>slide['duration'] for w in words):errors.append('Invalid ASR word timing')
  normalize=lambda text:re.sub('[^a-z0-9]','',text.lower())
  source=' '.join(b['text'] for b in slide['beats']);transcript=' '.join(w['word'] for w in words)
  if normalize(source)!=normalize(transcript):errors.append('Reviewed ASR differs from authored narration')
  if abs(p['durationSec']-timeline['edited_duration'])>.001:errors.append('Video did not drive slide timing')
  if len(p['bulletTimings'])!=len(p['bullets']):errors.append('Missing ASR bullet cue')
  if not p.get('pictureRoll',{}).get('shots',[{}])[0].get('video_url'):errors.append('Missing recorded visual')
  if not metadata_only:
   for item in asset['assets']:
    path=R/item['path']
    if not path.is_file():errors.append('Missing asset: '+item['path'])
    elif hashlib.sha256(path.read_bytes()).hexdigest()!=item['sha256']:errors.append('Asset checksum differs: '+item['path'])
 if load('native-import-validation.json')['status']!='passed':errors.append('Native parser validation did not pass')
 if not metadata_only:
  path=R/'review/lesson-00-native.mp4'
  if not path.exists():errors.append('Native review video missing')
  else:
   probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=codec_type,width,height,avg_frame_rate,duration:format=duration','-of','json',str(path)]))
   video=next(s for s in probe['streams'] if s['codec_type']=='video');audio=next(s for s in probe['streams'] if s['codec_type']=='audio')
   expected=sum(math.ceil(s['duration']*30-1e-9)/30 for s in slides)
   if abs(float(probe['format']['duration'])-expected)>.15:errors.append('Module duration does not match captured slides')
   if video['width']!=1920 or video['height']!=1080 or video['avg_frame_rate']!='30/1':errors.append('Unexpected video delivery format')
   if abs(float(video['duration'])-float(audio['duration']))>.15:errors.append('Audio/video duration mismatch')
 return {'status':'passed' if not errors else 'failed','errors':errors,'slide_count':len(slides),'verified_teaching_targets':sum(len(load(f'capture/slide{s["number"]}-timeline.json')['events']) for s in slides),'metadata_only':metadata_only}
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--metadata-only',action='store_true');args=parser.parse_args();result=validate(args.metadata_only);print(json.dumps(result,indent=2));raise SystemExit(bool(result['errors']))
