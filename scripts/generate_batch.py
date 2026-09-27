# /// script
# requires-python = ">=3.12"
# ///
"""一次按顺序生成多课音频：job 文件第二行写 lessons=gj-01,gj-02。
每课单独起一个 generate_lesson_audio.py 进程（环境变量 LESSON 指定课），断点续作照旧。
文件名以 generate_ 开头，worker 会把它当重任务、先拿两站（三站）共用的音频锁。"""
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
lessons: list[str] = []
for marker in sorted((ROOT / "audio-jobs").glob("*.running")):
    job = marker.with_suffix(".job")
    if job.exists():
        m = re.search(r"^lessons\s*=\s*(\S+)", job.read_text(encoding="utf-8"), re.M)
        if m:
            lessons = [x for x in m.group(1).split(",") if x]
if not lessons:
    sys.exit("job 文件里没写 lessons=")
for lesson in lessons:
    print(f"=== {lesson} ===", flush=True)
    r = subprocess.run(["uv", "run", "--script", "scripts/generate_lesson_audio.py"], cwd=ROOT, env={**os.environ, "LESSON": lesson})
    if r.returncode:
        sys.exit(f"{lesson} 失败（exit {r.returncode}）")
