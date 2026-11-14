#!/usr/bin/env bash
set -euo pipefail
# Pass the local path to skilleo-studio/course-video. No renderer source changes.
lesson_dir="$(cd -- "$(dirname -- "$0")" && pwd)"
renderer_dir="${1:?Pass the Skilleo course-video directory}"
"$renderer_dir/node_modules/.bin/remotion" render "$renderer_dir/src/index.ts" CourseModule "$lesson_dir/review/lesson-00-native.mp4" \
  --props="$lesson_dir/render-props.json" --public-dir="$lesson_dir/assets" \
  --browser-executable="${LESSON_CHROMIUM_PATH:-/usr/bin/chromium}" \
  --concurrency=2 --codec=h264 --crf=20 --x264-preset=veryfast
