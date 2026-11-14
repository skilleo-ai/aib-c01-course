# Lesson 01 — AI, ML and generative AI

[Watch or download the captioned review video](https://github.com/skilleo-ai/aib-c01-course/releases/tag/lesson-01-review-v1).

10 minutes 41 seconds. Warm, conversational local narration on a dark navy canvas with teal and amber diagrams, synthetic retail examples, an in-video classification exercise and explained answers. Primary exam skills: 1.1.1 and 1.1.2. Reinforces explicit-rule selection from 1.2.1. No coding or AWS account required.

This is a review build, pending user feedback and independent subject-matter approval. It teaches the concepts before service-specific applications. No AWS endorsement is implied.

## Teaching materials

- [Narration transcript](SCRIPT.md)
- [Learner worksheet and example answer](WORKSHEET.md)
- [Four additional original assessment questions, with option rationales](questions.json)
- [Claim and scope notes](CLAIMS.md) and [primary sources](sources.json)
- [Scene text and visual structure](scenes.json), [measured timing](timing.json) and [artifact manifest](manifest.json)
- [SRT captions](captions.srt) and [WebVTT captions](captions.vtt)
- [Visual identity](DESIGN.md), [composition check summary](CHECKS.json) and [render details](RENDER.json)



## Chapters

- 00:00 — AI, ML and generative AI
- 01:23 — Artificial intelligence is the umbrella
- 02:12 — Machine learning learns from examples
- 03:48 — Generative AI creates content
- 05:24 — The terms overlap
- 06:12 — Use the simplest suitable approach
- 08:27 — Your turn: classify the task
- 09:55 — Ask better questions about AI

## What to review

Listen for whether the voice feels conversational and pronounces the terminology clearly. Assess whether the pace leaves time to understand the diagrams, whether the examples provide enough depth, and whether you can explain the differences without simply repeating labels. Feedback on this lesson sets the production format for later lessons.

## Production and reproduction

The editable HyperFrames source is `index.html`. All diagrams are original. The review export uses a rendered opening, inspected scene frames, brief crossfades and measured phrase captions. It reuses inspected static frames during teaching holds and is delivered at constant 30 fps for broad player compatibility. A browser recording is not needed for this conceptual lesson.

1. Install Python dependencies from `requirements-audio.txt` in a virtual environment. Obtain the Kokoro v1.0 model and voice data from [the upstream release](https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0).
2. Run `python synthesize.py /path/to/kokoro-v1.0.onnx /path/to/voices-v1.0.bin`. The selected voice is `af_heart`, speed 0.94. Synthesis is local, as selected by the user. Captions derive from the actual generated phrase sample counts rather than estimated word duration.
3. Run `python build_composition.py` and `npm run check`. Use the supplied CLI pin. On restricted hosts, set `HYPERFRAMES_CACHE_DIR` and `npm_config_cache` to writable locations and `HYPERFRAMES_BROWSER_PATH` to the installed Chromium executable.
4. Render the entire editable composition with `npm run render -- --fps 30 --output renders/lesson-01-full.mp4`. Use the caption sidecar or add `captions.ass` through FFmpeg for burned-in captions.
5. The efficient review path in `export_review.py` expects inspected hero frames under `renders/hero-frames/` and a 3-second opening render at `renders/intro-test.mp4`. Capture one hero at each measured scene start + 3 seconds with `hyperframes snapshot`, then run the exporter. It inserts visual events at every caption boundary to maintain caption synchronization even during long holds.

Generated audio, inspection screenshots and MP4 files are excluded from git; the release contains the review video and learner-facing downloads. Source files and actual timing are versioned. Re-generating the voice may change timing; rebuild the composition and capture frames after synthesis.

## Third-party components

Inter fonts include their OFL license under `assets/fonts/`. GSAP includes its upstream license notice in `assets/gsap.min.js`. Kokoro model and voice files are not redistributed in this repository; consult their upstream terms before using them in a different distribution. HyperFrames is pinned in package.json. No cloud speech provider was used.
