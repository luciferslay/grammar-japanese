#!/usr/bin/env python3
"""把 Luna 在 /accent-candidates.html 选中的候选换进课程音频（母带 wav + manifest），再转 m4a。

用法：python3 scripts/pick_candidate.py gj-02 dialogue-06=v3-s3 word-01-term=v2-s2 ...
被换掉的原文件挪到 public/audio/candidates/<课>/_replaced/ 留底（不删）。"""
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
lesson, picks = sys.argv[1], sys.argv[2:]
std = ROOT / "public" / "audio" / "standard" / lesson
cand = ROOT / "public" / "audio" / "candidates" / lesson
keep = cand / "_replaced" / datetime.now().strftime("%Y%m%d-%H%M%S")
keep.mkdir(parents=True, exist_ok=True)
for p in picks:
    item, name = p.split("=")
    src = cand / item / f"{name}.wav"
    if not src.exists():
        raise SystemExit(f"找不到候选 {src}")
    for ext in (".wav", ".json", ".m4a"):
        old = std / f"{item}{ext}"
        if old.exists():
            shutil.move(old, keep / old.name)
    shutil.copy2(src, std / f"{item}.wav")
    meta = json.loads(src.with_suffix(".json").read_text(encoding="utf-8"))
    meta["picked_from_candidates"] = {"candidate": f"{item}/{name}", "picked_at": datetime.now().isoformat(timespec="seconds"),
                                      "by": "Luna 人耳（重音）"}
    (std / f"{item}.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[PICK] {lesson}/{item} ← {name}（{meta.get('tts_input_text')}）")
# 候选是按旧的女声语速录的；对话句换进来后按现在的目标语速（dialogue_seconds_per_mora）再对齐一次
dialogue = [p.split("=")[0] for p in picks if p.startswith("dialogue-")]
if dialogue:
    subprocess.run(["uv", "run", "--script", str(ROOT / "scripts" / "reconform_items.py"), lesson, *dialogue], check=True)
subprocess.run([sys.executable, str(ROOT / "scripts" / "publish_audio.py"), lesson], check=True)
