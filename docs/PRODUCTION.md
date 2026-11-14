# Production architecture and acceptance gates

## Existing-system boundary

The supplied documents are design references. No Skilleo Studio source code has been supplied or inspected. No claim of integration, existing API endpoints or compatibility testing is made. Keep Python orchestration independent of a future Studio adapter. Retain module-number markdown exports and a separate asset manifest when the actual Studio contracts are available; do not invent the figures.json schema.

## Artifact flow

Source register → skill coverage → lesson brief → storyboard → verified capture → edited visual timeline → narration → measured audio → aligned captions → assembled lesson → expert review → export.

A source ID travels with factual claims and scene specifications. Synthetic examples are explicitly labeled. A scene ID is stable across retries; each attempt gets separate artifacts. Version hashes of source, script, voice settings and edit decisions determine which downstream artifacts become stale. Never mark a planned or scripted artifact complete because its manifest exists.

## Scene state machine

planned → scripted → captured → verified → edited → voiced → assembled → reviewed → approved.

Diagram scenes use generated-artifact validation instead of browser capture. Any failed state records its reason and attempt number. Only verified captures enter editing. Approval is a recorded editorial decision; it is never inferred from successful rendering. A source change invalidates dependent claims for review, not every unrelated lesson.

## Capture adapter contract (not implemented)

Input: scene ID, source URL, viewport, device scale factor, selectors, allowed action, expected state, timeout, preconditions and sensitive-data rules. Output: raw video, optional screenshots, monotonic capture origin, action intervals, verified waiting intervals, selector boxes, verification evidence and failure reason.

Use the supported Playwriter execution interface when present. It is not assumed to be a Python library. If absent, report capture unavailable; do not silently replace recorded evidence with simulated success. Fix viewport and scale, establish capture origin before actions, record both action and verification times, and redact credentials or use synthetic accounts. A click result alone is insufficient verification.

## Timeline and highlights (math implemented)

pipeline/timeline.py builds a piecewise raw-to-edited mapping from explicit noninstructional wait intervals. Waits longer than five seconds reduce to five seconds; meaningful actions remain at normal speed. Overlapping or out-of-bounds intervals fail validation. Apply all highlights through this mapping after the edit decision is final. Coordinates must reference the recorded viewport; recompute after cropping, scaling or movement. Render moving targets only with tracked geometry or split intervals.

The next renderer should generate FFmpeg trim/setpts segments and normalize timestamps before concat. Captured browser audio is normally discarded; narration is added separately. Keep speed indicators for compressed waits. Long explanations belong on diagram or hold scenes, rather than forcing speech into short action clips.

## Narration and captions (adapters not implemented)

Draft against the final visual timeline, estimate 120–140 words per minute, then measure actual synthesized duration with FFprobe. Preserve pronunciation of service names and terms. Adjust text and meaningful holds before resorting to speed changes. Generate captions from actual audio with alignment; estimated word timing is insufficient for release. Qwen models in PLAN.md are candidates, not established dependencies. Voice licensing, runtime availability and a pronunciation audition precede selection.

## Release gates

- All covered skills have instruction, a worked example, reviewed assessment and expert signoff.
- Service claims cite current primary sources; pricing uses dated assumptions and never implies fictional worksheet values are AWS quotes.
- Recorded actions have deterministic completion evidence; timeline contains no unreviewed failures or private data.
- Text readable at 1080p and on a typical laptop; no essential information conveyed by color alone; captions available.
- Target 1920×1080, 30 fps, H.264, AAC 48 kHz; consistent audio target approximately −16 LUFS integrated and true peak at or below −1 dBTP, measured after assembly. These are proposed house targets, not current measurement results.
- No narration truncation; inspect sync at scene boundaries. Captions follow actual audio. Review silence, clipping and terminology pronunciation.
- Completed lesson receives subject-matter and instructional review; export contains source notes and independent-course disclosure.

## Implementation increments

1. Current: curriculum, primary-source register, pilot script and questions, economic model, coverage validation, timeline math and tests.
2. Next: capture adapter plus a single verified public-page scene; inspect resulting artifacts.
3. Then: FFmpeg edit adapter, voice audition, measured narration and caption alignment; render the pilot.
4. Next: expert review, revise pilot, then scale authoring by module with selective regeneration.
5. Integrate Studio only after inspecting its repository and real data contracts.
