# /// script
# requires-python = ">=3.12"
# dependencies = ["qwen-tts==0.1.1", "soundfile", "numpy", "torch", "pykakasi"]
# ///
"""Ono_Anna 对比样音（Luna 2026-09-28 要听）：用内置日语女声 Ono_Anna（CustomVoice，和韩语站 Sohee 同类）
把第 1 课里人耳标出「声音不一样」的几条 + 两条正常对话各录一版，放到 public/audio/samples/ono-anna/，
不触碰课程音频。对比页：public/samples-ono-anna.html（http://localhost:3200/samples-ono-anna.html）。"""
import json
import subprocess
from pathlib import Path

import numpy as np
import soundfile as sf
import torch
from huggingface_hub import snapshot_download
from qwen_tts import Qwen3TTSModel

from standardized_course_tts import ROOT, generation_kwargs, load_config, normalize_active_rms, set_seed, trim_and_pad

OUT = ROOT / "public" / "audio" / "samples" / "ono-anna"
OUT.mkdir(parents=True, exist_ok=True)
cfg = load_config()
cand = cfg["candidates"]["A1_ONO_ANNA"]
base = cfg["voices"]["FEMALE_CLEAR_SOFT"]["baseline"]

# (文件名, 文字, 用哪套指令：对话 / 词卡)
ITEMS = [
    ("dialogue-02", "いいえ、一度もありません。写真を見せてください。", "instruct"),
    ("dialogue-04", "いいですね。私ははこだてのラーメンなら食べたことがありますよ。", "instruct"),
    ("dialogue-06", "東京のお店で食べたんです。本場で食べたことは一回もありませんよ。", "instruct"),
    ("lesson-02-term", "見せる", "instruct_term"),
    ("lesson-02-example", "昨日撮った写真を友達に見せました。", "instruct"),
    ("lesson-03-term", "こんなに", "instruct_term"),
    ("lesson-03-example", "こんなに寒い日は初めてです。", "instruct"),
]

model_path = snapshot_download(cand["model"], local_files_only=True)
model = Qwen3TTSModel.from_pretrained(model_path, device_map="cpu", dtype=torch.float32)
for name, text, ikey in ITEMS:
    set_seed(cand["seed"])
    kwargs = generation_kwargs(cfg, "card" if ikey == "instruct_term" else "default")
    wavs, sr = model.generate_custom_voice(text=text, language=cand["language"], speaker=cand["speaker"], instruct=cand[ikey], **kwargs)
    audio = trim_and_pad(np.asarray(wavs[0]), sr, cfg["output"]["leading_silence_ms"], cfg["output"]["trailing_silence_ms"])
    audio = normalize_active_rms(audio, base["active_rms_dbfs"], cfg["quality"]["active_threshold_dbfs"])
    wav = OUT / f"{name}.wav"
    sf.write(wav, audio, sr, subtype="PCM_16")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(wav), "-c:a", "aac", "-b:a", "64k", "-ac", "1", "-ar", "24000", str(wav.with_suffix(".m4a"))], check=True)
    print(f"[OK] {name} {len(audio)/sr:.2f}s", flush=True)
print("all done")
