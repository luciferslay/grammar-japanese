# /// script
# requires-python = ">=3.12"
# dependencies = ["soundfile", "numpy", "faster-whisper", "pykakasi"]
# ///
"""用 whisper 听写指定条目，按句子 ASR 闸门的标准核对有没有读全（例句、单词卡平时不过这一关）。

用法：uv run --script scripts/asr_check_items.py gj-01/word-05-example [gj-02/...]"""
import json
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

sys.path.insert(0, str(Path(__file__).resolve().parent))
from term_audio_policy import check_sentence, transcribe  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
for item in sys.argv[1:]:
    wav = ROOT / "public" / "audio" / "standard" / f"{item}.wav"
    meta = json.loads(wav.with_suffix(".json").read_text(encoding="utf-8"))
    audio, sr = sf.read(wav, always_2d=False)
    res = check_sentence(transcribe(np.asarray(audio, dtype=np.float32), sr), meta["page_text"])
    print(item, "| 原文", meta["page_text"], "| pass", res["pass"])
    print("   ", json.dumps(res, ensure_ascii=False))
