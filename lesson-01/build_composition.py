"""Build a deterministic HyperFrames composition from measured narration timing."""
import json,html,math
from pathlib import Path
R=Path(__file__).resolve().parent
source=R/'timing.json'
scenes=json.loads((R/'scenes.json').read_text())
if source.exists():
    measured=json.loads(source.read_text())
    if len(measured)==len(scenes):scenes=measured
t=0
for s in scenes:
    if 'start' not in s:s['start']=t;s['duration']=len(s['narration'].split())/140*60+s['hold']+.75
    t=s['start']+s['duration']
# Rendering ranges operate on whole 30fps frames, but narration remains sample-timed.
duration=math.ceil(t*30)/30
esc=html.escape
css='''
@font-face{font-family:Inter;src:url(assets/fonts/Inter-400.woff2);font-weight:400}
@font-face{font-family:Inter;src:url(assets/fonts/Inter-700.woff2);font-weight:700}
:root{--bg:#101D2C;--panel:#1C3044;--text:#F5F0E8;--muted:#CBD6DF;--teal:#7BE0CC;--amber:#FFD08A}
*{box-sizing:border-box}html,body{margin:0;background:var(--bg);font-family:Inter,sans-serif;color:var(--text)}
[data-composition-id]{position:relative;width:1920px;height:1080px;overflow:hidden;background:var(--bg)}
.clip{position:absolute;inset:0;width:100%;height:100%;background:var(--bg)}
.scene-content{width:100%;height:100%;padding:62px 94px 150px;display:flex;flex-direction:column;gap:25px;box-sizing:border-box}
.topline{display:flex;justify-content:space-between;align-items:center;font-size:23px;letter-spacing:2px;font-weight:700;color:var(--muted)}
.brand{color:var(--teal);letter-spacing:4px}.kicker{font-size:25px;font-weight:700;color:var(--teal);letter-spacing:2px;margin-top:16px}
h1{font-size:72px;line-height:1.12;letter-spacing:-2px;margin:0;font-weight:700;max-width:1720px}
.stage{display:flex;flex:1;min-height:0;align-items:center;gap:27px}
.card{flex:1;min-width:0;min-height:330px;border-radius:22px;padding:35px;display:flex;flex-direction:column;justify-content:center;gap:25px;background:var(--panel);border-top:6px solid var(--teal)}
.card:nth-child(3){border-top-color:var(--amber)}.number{font-size:34px;color:var(--teal);font-weight:700;letter-spacing:2px}
h2{font-size:42px;line-height:1.15;letter-spacing:-1px;margin:0;font-weight:700}.detail{font-size:34px;line-height:1.35;color:var(--muted);margin:0}
.note{font-size:28px;line-height:1.3;color:var(--amber);min-height:40px;max-width:1680px}
.flow .card{min-height:320px}.arrow{font-size:48px;color:var(--teal)}
.nest{width:100%;padding:25px 32px;border:3px solid var(--teal);border-radius:22px;background:var(--panel);display:flex;flex-direction:column;gap:16px}
.nest .nest{margin-left:40px;width:calc(100% - 40px);background:var(--bg)}.nest .nest .nest{border-color:var(--amber);background:var(--panel)}
.nestline{display:flex;align-items:baseline;gap:30px}.nestline h2{font-size:38px;min-width:380px}.nestline p{font-size:29px;line-height:1.3;color:var(--muted);margin:0}
.footer{position:absolute;bottom:118px;left:94px;right:94px;display:flex;justify-content:space-between;color:var(--muted);font-size:21px}
.progress{position:absolute;left:0;bottom:0;height:5px;background:var(--teal)}
'''
sections=[];animations=[]
for i,s in enumerate(scenes):
    sid=s['id'];start=s['start'];length=s['duration']+(.4 if i<len(scenes)-1 else 0)
    items=s['items'];kind=s['kind']
    if kind=='umbrella':
        contents=''
        for j,(title,detail) in reversed(list(enumerate(items))):
            contents=f'<div class="nest part" id="{sid}-item{j}"><div class="nestline"><h2>{esc(title)}</h2><p>{esc(detail)}</p></div>{contents}</div>'
    else:
        contents=''
        for j,(title,detail) in enumerate(items):
            if kind=='flow' and j:contents+=f'<div class="arrow part" aria-hidden="true">→</div>'
            contents+=f'<div class="card part" id="{sid}-item{j}"><div class="number">0{j+1}</div><h2>{esc(title)}</h2><p class="detail">{esc(detail)}</p></div>'
    sections.append(f'''<section class="clip" id="{sid}" data-start="{start:.6f}" data-duration="{length:.6f}" data-track-index="{1+i%2}">
<div class="scene-content"><div class="topline part"><span class="brand">SKILLEO</span><span>AIB-C01 · AI FUNDAMENTALS</span></div>
<div class="kicker part">{esc(s['kicker'])}</div><h1 class="part">{esc(s['title'])}</h1>
<div class="stage {kind}">{contents}</div><div class="note part">{esc(s['note']) if s['note'] else ' '}</div></div>
<div class="footer part"><span>AI, ML and generative AI</span><span>LESSON 01 · {i+1:02} / {len(scenes):02}</span></div>
<div class="progress" style="width:{(i+1)/len(scenes)*100}%"></div></section>''')
    # Incoming whole-scene dissolve is the transition. Outgoing remains intact.
    animations.append(f'tl.from("#{sid}",{{opacity:0,duration:0.38,ease:"sine.inOut",immediateRender:false}},{start:.6f});')
    animations.append(f'tl.from("#{sid} .topline",{{opacity:0,x:-16,duration:.5,ease:"power3.out",immediateRender:false}},{start+.2:.6f});')
    animations.append(f'tl.from("#{sid} .kicker",{{opacity:0,y:14,duration:.5,ease:"sine.out",immediateRender:false}},{start+.25:.6f});')
    animations.append(f'tl.from("#{sid} h1",{{opacity:0,y:22,duration:.65,ease:"expo.out",immediateRender:false}},{start+.35:.6f});')
    for j in range(len(items)):
        animations.append(f'tl.from("#{sid}-item{j}",{{opacity:0,x:{-24 if j%2==0 else 24},duration:.6,ease:"power4.out",immediateRender:false}},{start+.65+j*.17:.6f});')
    animations.append(f'tl.from("#{sid} .arrow",{{opacity:0,scale:.85,duration:.45,stagger:.1,ease:"power2.out",immediateRender:false}},{start+.9:.6f});' if kind=='flow' else '')
    animations.append(f'tl.from("#{sid} .note, #{sid} .footer",{{opacity:0,duration:.5,stagger:.08,ease:"sine.out",immediateRender:false}},{start+1.2:.6f});')
head=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Lesson 01 — AI, ML and generative AI</title><style>{css}</style></head><body><div id="lesson01" data-composition-id="lesson01" data-width="1920" data-height="1080" data-start="0" data-duration="{duration:.6f}" data-fps="30">'''
script='<script src="assets/gsap.min.js"></script><script>window.__timelines=window.__timelines||{};const tl=gsap.timeline({paused:true});'+''.join(animations)+'window.__timelines["lesson01"]=tl;</script></body></html>'
visual=head+''.join(sections)+'</div>'+script
(R/'compositions').mkdir(exist_ok=True)
(R/'compositions/visuals.html').write_text(visual.replace('assets/', '../assets/'))
(R/'visuals.html').unlink(missing_ok=True)
audio=f'<audio id="narration" src="assets/audio/narration.wav" data-start="0" data-duration="{duration:.6f}" data-track-index="4"></audio>'
(R/'index.html').write_text(head+''.join(sections)+audio+'</div>'+script)
(R/'render-plan.json').write_text(json.dumps({'duration':duration,'scenes':[dict(id=s['id'],start=s['start'],duration=s['duration']) for s in scenes]},indent=2)+'\n')
print('Composition duration',round(duration,2))
