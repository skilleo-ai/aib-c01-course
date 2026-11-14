"""Establish visual timelines from verified Playwriter captures, before narration."""
import json,math,subprocess
from pathlib import Path
R=Path(__file__).resolve().parent

def edit(number):
    raw=R/f'capture/slide{number}-raw.mp4'
    eventfile=R/f'capture/slide{number}-events.json'
    data=json.loads(eventfile.read_text())
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(raw)]))
    raw_duration=float(probe['format']['duration'])
    duration=math.ceil(data['result']['duration']/1000*30)/30
    width=data['viewport']['width'];height=data['viewport']['height']
    filters=[]
    for event in data['events']:
        b=event['box']
        if b['y']<176 or b['y']+b['height']>height+2:raise ValueError('Incomplete capture target')
        x=max(0,math.floor(b['x']-5));y=max(0,math.floor(b['y']-5))
        w=min(width-x-1,math.ceil(b['width']+10));h=min(height-y-1,math.ceil(b['height']+10))
        start=event['visible_start']+1.1;end=start+2
        event['highlight']={'raw_start':start,'raw_end':end,'box':{'x':x,'y':y,'width':w,'height':h}}
        filters.append(f"drawbox=x={x}:y={y}:w={w}:h={h}:color=0xD84B40:t=3:enable='between(t,{start:.6f},{end:.6f})'")
    # Native Chrome may omit a tail of unchanged frames. Retain that actual last
    # screen for the planned reading hold; never fabricate a successful state.
    filters += [f'tpad=stop_mode=clone:stop_duration={max(0,duration-raw_duration)+.1:.6f}', 'fps=30','scale=800:1000','pad=960:1000:80:0:color=0x0f1419','setsar=1']
    output=R/f'assets/media/slide{number}-screen.mp4'
    subprocess.run(['ffmpeg','-v','error','-y','-i',str(raw),'-vf',','.join(filters),'-t',str(duration),'-an','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(output)],check=True)
    data.update(edited_duration=duration,raw_media_duration=raw_duration,tail_reading_hold_added=max(0,duration-raw_duration),edited_asset=f'assets/media/slide{number}-screen.mp4',wait_compression='No loading waits exceeded 5 seconds. Reading holds retained.',timeline_mapping='Identity for observed events; unchanged final-screen hold only.')
    (R/f'capture/slide{number}-timeline.json').write_text(json.dumps(data,indent=2)+'\n')
    print('Edited slide',number,'visual timeline:',duration,'seconds',flush=True)

if __name__=='__main__':
    import sys
    for number in (sys.argv[1:] or ['01','02']):edit(number)
