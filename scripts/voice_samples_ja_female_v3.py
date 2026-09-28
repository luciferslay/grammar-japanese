# /// script
# requires-python = ">=3.12"
# dependencies = ["qwen-tts==0.1.1", "soundfile", "numpy", "torch", "faster-whisper", "pykakasi"]
# ///
"""女声第三轮试听（Luna 2026-09-28 23:0x：「ono anna 还是带了很多不必要的感情」）。

Qwen3-TTS 内置声音里说日语的女声只有 Ono_Anna（其余是中文 Vivian/Serena、韩语 Sohee 和男声，读日语有口音），
所以不换人，换控制方法，三种一起录来对比：
  a 不给指示语：第二版的指示语里有「明るく」「澄んだ」这类形容词，模型会把它们读成情绪；空指示语让她用默认读法。
  b 明确要求平读 + 更低随机性：指示语只说「淡々と、感情を入れない」，温度 0.45→0.3、top_k 20→10。
  c 克隆 Ono_Anna 的平读样音：先用 b 的设置让她读原女声的参考句（案内放送式的长句），挑音高起伏最小的一条，
    再用 Base 模型克隆它。原女声语气稳就是因为走克隆 —— 读法跟着参考音走；音色来自 Ono_Anna 本人。
    风险：原女声当初的问题就是克隆出来的音色每句漂移，这个要靠耳朵听。
都走正式流水线 generate_one（哨兵切尾、切气声、自动质检），为了快一点，每条最多试 3〜4 个 seed。
语速、音高基准沿用第二版（Ono_Anna 自己的语速）。输出 public/audio/samples/ja-female-v3/{a,b,c}/。"""
import gc
import json
import os
import sys
from pathlib import Path

import numpy as np
import soundfile as sf
import torch

os.environ["LESSON"] = "gj-01"
sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_lesson_audio as g  # noqa: E402
from standardized_course_tts import (  # noqa: E402
    analyze_audio,
    load_config,
    normalize_active_rms,
    set_seed,
    sha256,
    trim_and_pad,
)

ROOT = g.ROOT
BASE_OUT = ROOT / "public" / "audio" / "samples" / "ja-female-v3"
cfg_path = ROOT / "audio_voice_presets.json"

FLAT = (
    "標準語で、ニュース原稿を読むように淡々と読んでください。感情は入れず、声の高さと速さを一定に保ち、"
    "抑揚は最小限にしてください。息の音やため息は入れないでください。"
)
ITEMS = {
    "dialogue-02.wav": "いいえ、一度もありません。写真を見せてください。",
    "dialogue-04.wav": "いいですね。私は函館のラーメンなら食べたことがありますよ。",
    "lesson-02-term.wav": "見せる",
    "lesson-02-example.wav": "昨日撮った写真を友達に見せました。",
    "lesson-03-term.wav": "こんなに",
    "lesson-03-example.wav": "こんなに寒い日は初めてです。",
}
g.DIALOGUE_ATTEMPTS = 4
g.TERM_ATTEMPTS = 3

cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
trial = cfg["voices"]["FEMALE_ONO_ANNA_TRIAL"]  # 第二版建的：Ono_Anna 自己的语速/音高基准
orig = cfg["voices"]["FEMALE_CLEAR_SOFT"]
_orig_kwargs = g.generation_kwargs


def use_kwargs(temp: float, top_k: int) -> None:
    def kw(config, variant="default"):
        k = _orig_kwargs(config, "card")
        k.update(temperature=temp, subtalker_temperature=temp, top_k=top_k, subtalker_top_k=top_k)
        return k
    g.generation_kwargs = kw


def save_voice(vid: str, voice: dict) -> dict:
    c = json.loads(cfg_path.read_text(encoding="utf-8"))
    c["voices"][vid] = voice
    cfg_path.write_text(json.dumps(c, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return load_config()


def run(tag: str, vid: str, voice: dict, model, clone_prompt=None) -> None:
    config = save_voice(vid, voice)
    g.OUT = BASE_OUT / tag
    g.OUT.mkdir(parents=True, exist_ok=True)
    for name, text in ITEMS.items():
        g.generate_one(model, vid, name, text, config, clone_prompt)
        wav = g.OUT / name
        import subprocess
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(wav), "-c:a", "aac", "-b:a", "64k", "-ac", "1",
                        "-ar", "24000", "-movflags", "+faststart", str(wav.with_suffix(".m4a"))], check=True)
        print(f"[OK] {tag}/{name}", flush=True)


common = {k: trial[k] for k in ("mode", "model", "speaker", "language", "model_revision", "seed",
                                "reference_audio", "reference_text", "reference_sha256", "baseline")}
common.update(role="B", candidate=True)

# ---- a / b：CustomVoice Ono_Anna
model = g.load_model(trial)
use_kwargs(0.45, 20)
run("a", "FEMALE_ONO_ANNA_V3A", {**common, "instruct": "", "instruct_term": "",
                                 "note": "2026-09-28 第三轮试听 a：不给指示语"}, model)
use_kwargs(0.3, 10)
run("b", "FEMALE_ONO_ANNA_V3B", {**common, "instruct": FLAT, "instruct_term": FLAT,
                                 "note": "2026-09-28 第三轮试听 b：平读指示语 + 温度 0.3"}, model)

# ---- c：先录克隆用的参考音（b 的设置读原女声的参考句），挑音高起伏最小的
ref_dir = BASE_OUT / "c-reference"
ref_dir.mkdir(parents=True, exist_ok=True)
ref_text = orig["reference_text"]
thr = cfg["quality"]["active_threshold_dbfs"]
best = None
for i in range(4):
    set_seed(trial["seed"] + 700 + i)
    wavs, sr = model.generate_custom_voice(text=ref_text, language="Japanese", speaker=trial["speaker"],
                                           instruct=FLAT, **g.generation_kwargs(cfg, "card"))
    audio = trim_and_pad(np.asarray(wavs[0]), sr, cfg["output"]["leading_silence_ms"], cfg["output"]["trailing_silence_ms"])
    audio = normalize_active_rms(audio, trial["baseline"]["active_rms_dbfs"], thr)
    p = ref_dir / f"ref-{i}.wav"
    sf.write(p, audio, sr, subtype="PCM_16")
    m = analyze_audio(p, ref_text, thr)
    spread = m["voiced_f0_p90_hz"] / m["voiced_f0_p10_hz"]
    print(f"[REF] ref-{i} 起伏比={spread:.2f} f0={m['median_f0_hz']:.0f} {m['duration_seconds']}s", flush=True)
    if best is None or spread < best[0]:
        best = (spread, p)
ref = ref_dir / "reference.wav"
ref.write_bytes(best[1].read_bytes())
print(f"[REF] 选 {best[1].name}（起伏比 {best[0]:.2f}）", flush=True)

del model
gc.collect()
torch.cuda.empty_cache()

voice_c = {**common, "mode": "voice_clone", "model": orig["model"], "model_revision": orig["model_revision"],
           "instruct": "", "reference_audio": str(ref.relative_to(ROOT)), "reference_text": ref_text,
           "reference_sha256": sha256(ref), "note": "2026-09-28 第三轮试听 c：克隆 Ono_Anna 平读样音（Base 模型）"}
voice_c.pop("speaker", None)
model = g.load_model(voice_c)
prompt = model.create_voice_clone_prompt(ref_audio=str(ref), ref_text=ref_text, x_vector_only_mode=False)
use_kwargs(0.45, 20)
run("c", "FEMALE_ONO_ANNA_V3C", voice_c, model, prompt)
print("all done")
