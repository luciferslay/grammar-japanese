# /// script
# requires-python = ">=3.12"
# dependencies = ["qwen-tts==0.1.1", "soundfile", "numpy", "torch", "faster-whisper", "pykakasi"]
# ///
"""Ono_Anna 第二版试听（Luna 2026-09-28 16:41）：第一版声音稳定，但语气夸张、前后有杂音/气声。
这一版：① 指示语改成原来女声 A3 的读法（明亮清澈、抑揚控えめ、落ち着いた，不带感情/叹气/气声）；
② 对话句生成温度 ~~0.9→0.6~~ 0.9→0.45（和单词卡同一套，越高语气越花）；语速用 Ono_Anna 自己的（22:3x 改）；③ 走正式流水线 generate_one（哨兵切尾、切句首句尾气声、
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
from standardized_course_tts import analyze_audio, load_config, sha256  # noqa: E402

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

# 1) 基准：音量对齐现在的女声（和男声、其他课一致）；语速、音高用 Ono_Anna 第一版实测（她本来的语速和声区）
# ~~语速对齐原女声 0.126 秒/音拍~~（2026-09-28 22:3x 否决：Ono_Anna 本来就是 0.17〜0.21，对齐后句句判「语速不过关」
# 还会被 atempo 硬拉快；Luna：「ono anna 原本的语速很正常，就是语气飘忽不定」→ 语速用她自己的）
cfg_path = ROOT / "audio_voice_presets.json"
cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
old = cfg["voices"]["FEMALE_CLEAR_SOFT"]["baseline"]
ref = V1 / "dialogue-06.wav"
ref_text = "東京のお店で食べたんです。本場で食べたことは一回もありませんよ。"
thr = cfg["quality"]["active_threshold_dbfs"]
V1_TEXTS = {
    "dialogue-02": "いいえ、一度もありません。写真を見せてください。",
    "dialogue-04": "いいですね。私ははこだてのラーメンなら食べたことがありますよ。",
    "dialogue-06": ref_text,
    "lesson-02-example": "昨日撮った写真を友達に見せました。",
    "lesson-03-example": "こんなに寒い日は初めてです。",
}
v1m = {k: analyze_audio(V1 / f"{k}.wav", t, thr) for k, t in V1_TEXTS.items()}
med = lambda key, names=V1_TEXTS: float(np.median([v1m[n][key] for n in names if v1m[n].get(key)]))
# 语速取三句对话的中位数（例句里有句中停顿，会把秒/音拍拉长）；音高取 5 句的中位数（不只看语气最夸张的对话 6）
m = {
    "seconds_per_mora": round(med("seconds_per_mora", ("dialogue-02", "dialogue-04", "dialogue-06")), 4),
    "median_f0_hz": round(med("median_f0_hz"), 2),
    "voiced_f0_p10_hz": round(med("voiced_f0_p10_hz"), 2),
    "voiced_f0_p90_hz": round(med("voiced_f0_p90_hz"), 2),
}
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
    # audit_output 的 manifest 要记参考音哈希，没有这个键会 KeyError（2026-09-28 Windows 首跑发现）
    "reference_sha256": sha256(ref),
    "baseline": {
        "seconds_per_mora": m["seconds_per_mora"],
        "active_rms_dbfs": old["active_rms_dbfs"],
        "median_f0_hz": m.get("median_f0_hz") or old["median_f0_hz"],
        "voiced_f0_p10_hz": m.get("voiced_f0_p10_hz") or old["voiced_f0_p10_hz"],
        "voiced_f0_p90_hz": m.get("voiced_f0_p90_hz") or old["voiced_f0_p90_hz"],
    },
    "note": "2026-09-28 试听用候选（v2），candidate=true 所以不会被正式流程选中。",
}
cfg_path.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("baseline", cfg["voices"][VID]["baseline"], flush=True)

# 2) 对话句温度调低：~~0.9→0.6、top_k 30~~ → 直接用单词卡那套低随机性（generation_card：温度 0.45、top_k 20），
# 对话和单词卡同一套读法，句与句之间语气不飘（2026-09-28 22:3x Luna：语气要和原女声一致）
_orig = g.generation_kwargs
def _calm(config, variant="default"):
    return _orig(config, "card")
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
