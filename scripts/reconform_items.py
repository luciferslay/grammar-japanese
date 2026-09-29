# /// script
# requires-python = ">=3.12"
# dependencies = ["qwen-tts==0.1.1", "soundfile", "numpy", "torch", "faster-whisper", "pykakasi"]
# ///
"""不重新生成，只对已有母带重新做「变速对齐 + 音量归一 + 裁切」，再跑整句 ASR 确认没切坏，最后转 m4a。

用法：
  uv run --script scripts/reconform_items.py gj-01 dialogue-02 dialogue-04      # 指定条目
  uv run --script scripts/reconform_items.py gj-01 --voice FEMALE_ONO_ANNA_CLONE --dialogue   # 某声线的全部对话句
起因（2026-09-29 Luna）：课文里女生明显比男生慢 → 女声对话的目标语速改成男声的（dialogue_seconds_per_mora），
已录好的对话句直接变速，不重录（音色、语气都是 Luna 听过认可的）。旧 manifest 里的检查记录保留在 previous 字段。"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

sys.path.insert(0, str(Path(__file__).resolve().parent))
from standardized_course_tts import ROOT, conform_existing  # noqa: E402
from term_audio_policy import check_sentence, transcribe  # noqa: E402

args = sys.argv[1:]
lesson = args.pop(0)
voice_filter = None
if "--voice" in args:
    i = args.index("--voice")
    voice_filter = args[i + 1]
    del args[i:i + 2]
only_dialogue = "--dialogue" in args
args = [a for a in args if a != "--dialogue"]
std = ROOT / "public" / "audio" / "standard" / lesson
items = args or sorted(p.stem for p in std.glob("*.json"))
for item in items:
    wav = std / f"{item}.wav"
    meta_path = wav.with_suffix(".json")
    old = json.loads(meta_path.read_text(encoding="utf-8"))
    if voice_filter and old.get("voice_id") != voice_filter:
        continue
    if only_dialogue and not item.startswith("dialogue-"):
        continue
    text = old.get("page_text") or old["text"]
    manifest = conform_existing(old["voice_id"], text, wav)
    audio, sr = sf.read(wav, always_2d=False)
    asr = check_sentence(transcribe(np.asarray(audio, dtype=np.float32), sr), text)
    manifest["sentence_asr"] = asr
    for k in ("tts_input_text", "page_text", "seed_offset", "picked_from_candidates"):
        if k in old:
            manifest[k] = old[k]
    manifest["previous"] = {k: v for k, v in old.items() if k != "previous"}
    meta_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tc = manifest["tempo_conformance"]
    print(f"[RECONFORM] {lesson}/{item} 变速 ×{tc['atempo_factor']}  {tc['pre_conformance_seconds_per_mora']} → "
          f"{manifest['metrics']['seconds_per_mora']} 秒/音拍（目标 {tc['target_seconds_per_mora']}）  ASR {'过' if asr['pass'] else '不过'}",
          flush=True)
subprocess.run([sys.executable, str(ROOT / "scripts" / "publish_audio.py"), lesson], check=True)
