# /// script
# requires-python = ">=3.12"
# dependencies = ["qwen-tts==0.1.1", "soundfile", "numpy", "torch", "faster-whisper", "pykakasi"]
# ///
"""只重录一课里指定的几条，其余条目一律当「已完成」。

用法：LESSON=gj-01 REDO=dialogue-05.wav uv run --script scripts/redo_items.py
（2026-09-29 起因：函館 读音修正后第 1 课对话 5 要用男声重录，其余不动。
不走 job 的 redo= 选项，是因为那个只从进度文件里拿掉条目，而这台电脑没有进度文件，会把整课重录一遍。）"""
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_lesson_audio as g  # noqa: E402

redo = {x.strip() for x in os.environ["REDO"].split(",") if x.strip()}
everything = [*g.CARD_JOBS, *g.A_JOBS, *g.B_JOBS]
unknown = redo - set(everything)
if unknown:
    raise SystemExit(f"{g.LESSON} 里没有这些条目：{sorted(unknown)}")
g.OUT.mkdir(parents=True, exist_ok=True)
g.PROGRESS.write_text(json.dumps({"completed": [x for x in everything if x not in redo]}, ensure_ascii=False, indent=2) + "\n",
                      encoding="utf-8")
print(f"[REDO] {g.LESSON}: {sorted(redo)}", flush=True)
g.main()
