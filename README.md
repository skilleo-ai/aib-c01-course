# AWS Certified AI Business Strategist (AIB-C01) — course production

A depth-focused, independent course and reproducible production foundation for Skilleo. Curriculum design, a scripted ROI pilot and the first rendered lesson are available; the full course remains in production.

## First lesson video

[Watch or download lesson 01: AI, ML and generative AI](https://github.com/skilleo-ai/aib-c01-course/releases/tag/lesson-01-review-v1) — 10 minutes 41 seconds, dark theme, local narration and burned-in captions. [Lesson source and teaching materials](lesson-01/README.md). This is a review build, pending user feedback and independent subject-matter approval.

## Start here

- [Course blueprint](curriculum/BLUEPRINT.md): 13 modules, 39 domain lessons, orientation, capstone and assessment design.
- [Skill coverage matrix](curriculum/coverage.csv): all 58 retrieved official exam skills mapped to planned instruction.
- [Pilot narration](pilot/SCRIPT.md): an original support-assistant investment case, approximately 10 minutes 44 seconds including estimated holds.
- [Pilot storyboard](pilot/STORYBOARD.md): scene direction, estimated timing and optional public-page capture specification.
- [Learner worksheet and instructor key](pilot/WORKSHEET.md): worked ROI, sensitivity and break-even analysis.
- [Six original pilot questions](pilot/questions.json): answer keys and rationale for every option; expert review pending.
- [Production architecture](docs/PRODUCTION.md): capture boundaries, timeline math, asset states and release gates.
- [Primary-source register](sources/register.json): retrieved URLs, timestamps, content fingerprints and reuse-review notes.
- [Editorial standards](docs/EDITORIAL.md): depth, evidence, accessibility and review requirements.

## Current status

| Deliverable | Status |
|---|---|
| Primary exam-skill inventory | Retrieved from the four official domain pages |
| Skill-to-lesson coverage | 58/58 mapped; planned coverage |
| Domain lesson briefs | 39 mapped; 2 narration drafts, including 1 rendered review lesson |
| Pilot economics, storyboard and questions | Drafted and internally checked |
| Wait compression and timestamp remapping | Implemented and unit tested |
| Browser recording adapter | Not implemented |
| FFmpeg assembly and local narration | Working for lesson 01; reusable Studio adapters pending |
| Rendered course videos | Lesson 01 review build; approval pending |
| Expert approval / Studio integration | Pending / not performed |

The uploaded PLAN.md and Highlight.md were treated as design references. Their proposed tools and interfaces are not assumed installed or integrated. GitHub does not contain the uploaded documents; the implementation decisions are documented here.

## Run local checks

Python 3.10+; standard library only. From the repository root:

```bash
python -m pipeline.validate
python -m unittest discover -s tests -v
python pilot/economics.py
```

Coverage validation checks known skill IDs, domain consistency, reference integrity, CSV mappings and pilot question structure. It does not certify teaching quality or factual correctness. Timeline tests verify that only declared waits are compressed and highlights map to the edited timeline. Economics tests verify the numerical teaching answers. GitHub Actions runs the validator and tests on pushes and pull requests.

## Production order

1. Review lesson 01 for voice, pace, depth and visual clarity; revise before scaling.
2. Implement a supported capture adapter and produce one verified public-page scene.
3. Refine the local voice, visual pacing and caption format based on lesson 01 feedback.
4. Assemble and review the pilot, then apply the reviewed format module by module.
5. Inspect the actual Skilleo repository before implementing integration.

No AWS account, paid model, cloud resource or deployment is required for the current checks. Generated audio, intermediate media and secrets are excluded from git. The first review video is explicitly included under lesson-01/review because release-asset uploads rejected authentication. Use a media artifact store as production scales.

## Source and rights policy

Use online resources to establish facts and create original instruction. Public access does not imply redistribution permission. Review rights before embedding third-party visual assets or recordings. Do not reproduce paid courses, official practice questions, recalled exam items or protected training slides. No AWS endorsement is implied. Source changes require review before release; service names and pricing can change.

No open-source license has been assigned to the original course material. Select licensing deliberately before public distribution.
