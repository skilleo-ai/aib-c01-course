"""Validate planned curriculum coverage and pilot references; no completion inference."""
import csv
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def validate(root=ROOT):
    load=lambda p:json.loads((root/p).read_text())
    errors=[]
    skills=load('curriculum/exam-skills.json');lessons=load('curriculum/lessons.json')
    sources=load('sources/register.json');pilot=load('pilot/manifest.json')
    source_ids={s['id'] for s in sources};skill_ids={s['id'] for s in skills}
    lesson_ids=[l['id'] for l in lessons]
    if len(set(lesson_ids))!=len(lesson_ids):errors.append('duplicate lesson ids')
    mapped=set()
    for lesson in lessons:
        mapped.update(lesson['skills'])
        for sid in lesson['skills']:
            if sid not in skill_ids:errors.append(f'unknown skill {sid}')
            elif int(sid.split('.')[0]) != lesson['domain']:errors.append(f'domain mismatch {lesson["id"]}: {sid}')
    for sid in sorted(skill_ids-mapped):errors.append(f'unmapped exam skill {sid}')
    for skill in skills:
        if skill['source_id'] not in source_ids:errors.append(f'unknown source {skill["source_id"]}')
    rows=list(csv.DictReader((root/'curriculum/coverage.csv').open()))
    if {r['skill_id'] for r in rows} != skill_ids:errors.append('coverage CSV skill set differs')
    for row in rows:
        expected={l['id'] for l in lessons if row['skill_id'] in l['skills']}
        if set(row['lesson_ids'].split(';')) != expected:errors.append(f'stale coverage row {row["skill_id"]}')
    scene_ids=[]
    for scene in pilot['scenes']:
        scene_ids.append(scene['id'])
        if scene['target_seconds'] <= 0:errors.append('invalid scene duration')
        for ref in scene['source_ids']:
            if ref not in source_ids:errors.append(f'unknown scene source {ref}')
        if not (root/scene['script']).is_file():errors.append(f'missing script {scene["script"]}')
        if scene['status']=='rendered' and not scene.get('artifact'):errors.append('rendered scene without artifact')
    if len(scene_ids)!=len(set(scene_ids)):errors.append('duplicate scene ids')
    for q in load('pilot/questions.json'):
        if not set(q['correct']).issubset(q['options']):errors.append(f'invalid answer {q["id"]}')
        if set(q['rationales']) != set(q['options']):errors.append(f'missing option explanation {q["id"]}')
        if not set(q['skills']).issubset(skill_ids):errors.append(f'unknown question skill {q["id"]}')
    lesson_dir=root/'lesson-01'
    if lesson_dir.exists():
        timed=load('lesson-01/timing.json');captions=load('lesson-01/captions.json')
        manifest=load('lesson-01/manifest.json');briefs=load('lesson-01/scenes.json')
        if len(timed)!=len(briefs) or len(timed)!=manifest['scene_count']:
            errors.append('lesson 01 scene count differs from manifest')
        for actual,brief in zip(timed,briefs):
            if actual['id']!=brief['id'] or actual['narration']!=brief['narration']:
                errors.append('lesson 01 timing was not rebuilt after script edits')
            text=' '.join(c['text'] for c in captions if c['scene']==actual['id'])
            if ' '.join(text.split())!=' '.join(actual['narration'].split()):
                errors.append(f'caption text differs from narration: {actual["id"]}')
            if actual['duration']<=0:errors.append('invalid lesson scene duration')
        for a,b in zip(timed,timed[1:]):
            if abs(a['start']+a['duration']-b['start'])>.001:
                errors.append('lesson 01 scene timing gap or overlap')
        for a,b in zip(captions,captions[1:]):
            if a['end']>b['start']:errors.append('overlapping lesson 01 captions')
        if any(c['end']<=c['start'] for c in captions):errors.append('empty lesson caption')
        if captions[-1]['end']>manifest['duration_seconds']:errors.append('lesson captions exceed video')
        for q in load('lesson-01/questions.json'):
            if not set(q['correct']).issubset(q['options']):errors.append('invalid lesson 01 answer')
            if set(q['rationales'])!=set(q['options']):errors.append('missing lesson 01 option rationale')
            if not set(q['skills']).issubset(skill_ids):errors.append('unknown lesson 01 question skill')
    return errors,{'official_skills':len(skills),'planned_lessons':len(lessons),'mapped_skills':len(mapped&skill_ids),'scripted_lessons':sum(l['status'] in ('scripted','review_rendered') for l in lessons),'rendered_review_lessons':sum(l['status']=='review_rendered' for l in lessons),'roi_pilot_rendered_scenes':sum(s['status']=='rendered' for s in pilot['scenes'])}

if __name__=='__main__':
    errors,summary=validate()
    print(json.dumps({'summary':summary,'errors':errors},indent=2))
    raise SystemExit(bool(errors))
