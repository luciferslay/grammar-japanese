# /// script
# requires-python = ">=3.12"
# dependencies = ["qwen-tts==0.1.1", "soundfile", "numpy", "torch", "faster-whisper", "pykakasi"]
# ///
"""Ono_Anna 第二版试听（Luna 2026-09-28 16:41）：第一版声音稳定，但语气夸张、前后有杂音/气声。
这一版：① 指示语改成原来女声 A3 的读法（明亮清澈、抑揚控えめ、落ち着いた，不带感情/叹气/气声）；
② 对话句生成温度 0.9→0.6（越高语气越花）；③ 走正式流水线 generate_one（哨兵切尾、切句首句尾气声、
多 seed 自动质检），和课程音频完全一样的后处理。只录 2 句课文 + 2 个单词及例句，输出到
public/audio/samples/ono-anna-v2/，不碰课程音频。对比页：/samples-ono-anna.html。"""
import json
import os
import sys
from pathlib import Path

import numpy as np

os.environ["LESSON"] = "gj-01"
sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_lesson_audio as g  # noqa: E402
from standardized_course_tts import analyze_audio, load_config  # noqa: E402

ROOT = g.ROOT
VID = "FEMALE_ONO_ANNA_TRIAL"
V1 = ROOT / "public" / "audio" / "samples" / "ono-anna"
OUT = ROOT / "public" / "audio" / "samples" / "ono-anna-v2"
OUT.mkdir(parents=True, exist_ok=True)

INSTRUCT = (
    "二十代後半の女性らしい、明るく澄んだ声で、丁寧で聞き取りやすく話してください。標準語で、抑揚は控えめにし、"
    "落ち着いた一定のトーンを保ってください。感情を込めすぎたり、驚いたり笑ったりする演技はせず、"
    "ため息や息の音、ささやき声は入れないでください。普通の速さで、文末まで音を落とさずはっきり言い切ってください。"
)
INSTRUCT_TERM = (
    "標準語のアクセントで、明るく澄んだ声のまま、落ち着いて一回だけはっきり読んでください。"
    "感情や演技、驚き、笑いは一切入れず、一定の高さと速さを保ってください。"
    "ため息、息の混じった声、ささやき声は使わず、最後までくっきり言い切ってください。"
)

# 1) 基准：音量、语速对齐现在的女声（和男声、其他课一致）；音高范围用 Ono_Anna 第一版实测（她本来的声区）
cfg_path = ROOT / "audio_voice_presets.json"
cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
old = cfg["voices"]["FEMALE_CLEAR_SOFT"]["baseline"]
ref = V1 / "dialogue-06.wav"
ref_text = "東京のお店で食べたんです。本場で食べたことは一回もありませんよ。"
m = analyze_audio(ref, ref_text, cfg["quality"]["active_threshold_dbfs"])
cand = cfg["candidates"]["A1_ONO_ANNA"]
cfg["voices"][VID] = {
    **{k: cand[k] for k in ("mode", "model", "speaker", "language")},
    "role": "B",
    "candidate": True,
    "model_revision": cand.get("model_revision"),
    "seed": cand["seed"],
    "instruct": INSTRUCT,
    "instruct_term": INSTRUCT_TERM,
    "reference_audio": str(ref.relative_to(ROOT)),
    "reference_text": ref_text,
    "reference_sha256": __import__("hashlib").sha256(ref.read_bytes()).hexdigest(),
    "baseline": {
        "seconds_per_mora": old["seconds_per_mora"],
        "active_rms_dbfs": old["active_rms_dbfs"],
        "median_f0_hz": m.get("median_f0_hz") or old["median_f0_hz"],
        "voiced_f0_p10_hz": m.get("voiced_f0_p10_hz") or old["voiced_f0_p10_hz"],
        "voiced_f0_p90_hz": m.get("voiced_f0_p90_hz") or old["voiced_f0_p90_hz"],
    },
    "note": "2026-09-28 试听用候选（v2），candidate=true 所以不会被正式流程选中。",
}
cfg_path.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("baseline", cfg["voices"][VID]["baseline"], flush=True)

# 2) 对话句温度调低
_orig = g.generation_kwargs
def _calm(config, variant="default"):
    kw = _orig(config, variant)
    if variant == "default":
        kw.update(temperature=0.6, subtalker_temperature=0.6, top_k=30, subtalker_top_k=30)
    return kw
g.generation_kwargs = _calm
g.OUT = OUT

ITEMS = {
    "dialogue-02.wav": "いいえ、一度もありません。写真を見せてください。",
    "dialogue-04.wav": "いいですね。私は函館のラーメンなら食べたことがありますよ。",
    "lesson-02-term.wav": "見せる",
    "lesson-02-example.wav": "昨日撮った写真を友達に見せました。",
    "lesson-03-term.wav": "こんなに",
    "lesson-03-example.wav": "こんなに寒い日は初めてです。",
}
config = load_config()
model = g.load_model(config["voices"][VID])
for name, text in ITEMS.items():
    g.generate_one(model, VID, name, text, config)
    wav = OUT / name
    import subprocess
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(wav), "-c:a", "aac", "-b:a", "64k", "-ac", "1", "-ar", "24000",
                    "-movflags", "+faststart", str(wav.with_suffix(".m4a"))], check=True)
    print(f"[OK] {name}", flush=True)
print("all done")
