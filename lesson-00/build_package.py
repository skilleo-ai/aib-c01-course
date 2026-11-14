"""Bundle native authoring data and the exact accepted capture/audio assets."""
import json,zipfile
from pathlib import Path
R=Path(__file__).resolve().parent
files=[]
for pattern in ['*.md','*.json','*.py','*.cjs','*.sh','requirements-voice.txt','captions.srt','captions.vtt','capture/*.js','capture/*.mjs','assets/fonts/*']:
 for path in R.glob(pattern):
  if path.name in ('preview-props.json',) or 'attempt1' in path.name:continue
  files.append(path)
for n in ['01','02']:
 for rel in [f'capture/slide{n}-raw.mp4',f'capture/slide{n}-events.json',f'capture/slide{n}-timeline.json',f'assets/media/slide{n}-screen.mp4',f'assets/audio/slide{n}-narration.wav']:
  files.append(R/rel)
output=R/'review/lesson-00-review-package.zip'
with zipfile.ZipFile(output,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
 for path in sorted(set(files)):
  if path.is_file():archive.write(path,path.relative_to(R))
print('Packaged',len(set(files)),'files;',output.stat().st_size,'bytes')
