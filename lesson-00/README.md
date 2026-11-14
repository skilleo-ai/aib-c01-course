# Lesson 0 — two slides using Playwriter and native Skilleo

This is a two-slide review sample for the course introduction, not the complete lesson 0. The recorded AWS page establishes the teaching content and visual timing. Narration was written and synthesized afterward to fit verified sections of that footage.

## Review

[Download the native Skilleo review video](review/lesson-00-native.mp4) — about 1 minute 38 seconds.

1. **Why learn AI business strategy?** AWS's positioning, the decisions the credential validates, and the practical value of learning the skills.
2. **Who is this certification for?** Audience, recommended experience, prerequisites, and AWS's distinction from AI Practitioner. No required certification ladder is invented.

The video uses actual Playwriter browser recordings in Skilleo's existing `CourseModule` composition and `bullets-visual-architecture-focus` template. There are no HyperFrames compositions or reconstructed AWS pages. Brief red rectangles highlight the real page text. Bullets reveal using actual ASR timings. Audio and captions are available separately in the review package.

## Native authoring files

- [module-0.md](module-0.md): `skilleo-course-script/v1`, with stable module/slide IDs, narration and bullets.
- [module-0-script.json](module-0-script.json): matching native script document.
- [module-0-studio.json](module-0-studio.json): Studio module data with recorded video, narration, ASR word timings and bullet timings.
- [render-props.json](render-props.json): actual camelCase props used by the native renderer.
- [figures.json](figures.json): valid `skilleo-figures/v1` bundle with zero figures, because both visuals are recordings. No figure animation flags are fabricated.
- [asset-manifest.json](asset-manifest.json): companion binding and checksum data for the recorded assets; this companion schema is specific to the sample.
- [captions.srt](captions.srt) and [captions.vtt](captions.vtt): ASR-derived captions with reviewed wording.
- [Native importer validation](native-import-validation.json): tested with Skilleo's actual parser; IDs, narration, bullets and presentation types round-trip correctly.

**Media binding:** Skilleo's Markdown/script importer does not attach video, audio or measured duration. Those are supplied separately in module-0-studio.json and the asset package. Upload those assets to Studio storage and bind the returned URLs. This sample has not been uploaded into production Studio, and an automatic production import is not claimed. Treat it as a single-module review, rather than replacing a whole course with this two-slide file.

## Recording-first pipeline

[Content and page plan](CONTENT-PLAN.md) → live AWS page inspection → verified Playwriter recording → measured visual edit → narration per visible section → measured local speech → ASR word timings → native Skilleo render.

The first capture attempt exposed an accordion paragraph extending below the viewport. It was rejected. The replacement recording uses a narrower responsive viewport, waits for the accordion layout to settle and checks that each complete teaching paragraph is inside the frame. Capture scripts and event metadata are retained under capture/. Loading waits did not exceed five seconds. Deliberate reading/teaching holds were preserved.

Native Chrome recording can omit a tail of unchanged frames. The editor retains the actual final screen for the remainder of the planned reading hold; this does not synthesize an action or outcome. All observed event times retain an identity mapping. Highlight coordinates are applied before scaling/padding, so they stay in the recorded viewport's coordinate system.

Each narration segment is measured against its existing visible-content window. Overlong narration fails validation and is rewritten. ASR is run only after synthesis, and its words are checked against the authored narration before driving bullet cues. Punctuation and capitalization are reviewed without inventing timestamps.

## Reproduce

Use the Skilleo renderer commit recorded in [provenance.json](provenance.json). Its source was not changed. Install its course-video dependencies using its lockfile. The exact Outfit font may be mirrored with prepare_local_font.py when the headless browser cannot reach its CDN.

Playwriter 0.11.0 supports direct CDP recording with Chromium 153+. Start a dedicated browser with a debugging port, create a Playwriter session with `session new --direct HOST:PORT`, then run the capture scripts with that session. The scripts depend on the inspected live AWS content and should be re-inspected before reuse. On this managed host, its proxy certificate is not in Chromium's trust store, so the dedicated public-page browser session required a certificate override; no signed-in account was used.

Run edit_captures.py before narrate_and_asr.py, then build_module.py and validate_native.cjs. See [render.sh](render.sh) for the native render invocation. Local speech uses the previously selected Kokoro voice and upstream model files, which are not redistributed here.

## Source and review scope

Source: [AWS Certified AI Business Strategist](https://aws.amazon.com/certification/certified-ai-business-strategist/), including its candidate, career and comparison FAQs. The recorded page currently includes beta information; these two slides avoid teaching changeable exam prices and durations. This is original independent training, with no AWS endorsement implied.

Please assess whether the recorded-page approach, pacing, voice and native Skilleo presentation are the right direction. Remaining introduction topics and the rest of the course are not produced by this sample.
