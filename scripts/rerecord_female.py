# /// script
# requires-python = ">=3.12"
# dependencies = ["qwen-tts==0.1.1", "soundfile", "numpy", "torch", "faster-whisper", "pykakasi"]
# ///
"""换女声后重录一课的女声条目：对话 B + 全部单词卡（card_voice），男声（A）不动。

用法：LESSON=gj-01 uv run --script scripts/rerecord_female.py
做法：把本课 A 的对话预先记成「已完成」，再走 generate_lesson_audio.main()，这样只会录 card + B。
（2026-09-29 起因：女声换成 FEMALE_ONO_ANNA_CLONE；而且男声的参考音 reference-b-calm-slow.wav 不在仓库里，
Windows 这台根本录不了男声。）"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_lesson_audio as g  # noqa: E402

g.OUT.mkdir(parents=True, exist_ok=True)
g.PROGRESS.write_text(json.dumps({"completed": list(g.A_JOBS)}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"[FEMALE] {g.LESSON}: 单词卡 {len(g.CARD_JOBS)} 条 + 女声对话 {len(g.B_JOBS)} 条；男声 {len(g.A_JOBS)} 条不动", flush=True)
g.main()
