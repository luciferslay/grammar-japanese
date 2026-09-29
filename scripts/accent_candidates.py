# /// script
# requires-python = ">=3.12"
# dependencies = ["qwen-tts==0.1.1", "soundfile", "numpy", "torch", "faster-whisper", "pykakasi"]
# ///
"""重音（アクセント）候选：同一条换几种写法（汉字／平假名／片假名）× 几个 seed 各录一版，
粗测目标词每个音拍的音高给个「重音分」排序，做成试听页让 Luna 人耳挑。

起因（2026-09-29 Luna 人耳）：读音表把 二、三日／大家さん／家賃 换成假名后，读音对了但重音错了
（二、三日 应为低高低、重音在「さん」；大家さん、家賃 都是头高）。Qwen3-TTS 没有指定重音的参数，
写法不同、seed 不同，重音会变，所以只能多录几版挑。

用法：LESSON=gj-02 uv run --script scripts/accent_candidates.py
输出：public/audio/candidates/<课>/<条目>/<写法>-s<seed>.m4a + candidates.json；试听页 /accent-candidates.html?lesson=gj-02
Luna 选好后用 pick_candidate.py 把选中的那版换进课程音频。"""
import json
import os
import shutil
import subprocess
import sys
import types
from pathlib import Path

import numpy as np
import soundfile as sf

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_lesson_audio as g  # noqa: E402
import ja_text  # noqa: E402
from standardized_course_tts import load_config, voice_for_role  # noqa: E402
from term_audio_policy import check_sentence, transcribe  # noqa: E402

SEEDS = 4

# 条目：页面原文、要试的写法、目标词在原文里从第几个音拍开始（0 起）、目标词各音拍的高(1)/低(0)
# 头高 = 第一拍高、后面低；二、三日（にさんにち）= 低高高低低（重音核在「さん」之后）
ITEMS = {
    "gj-02": [
        ("dialogue-06.wav", "二、三日ならかまいませんよ。それより長かったらちょっと困りますけどね。",
         ["二、三日ならかまいませんよ。それより長かったらちょっと困りますけどね。",
          "にさんにちならかまいませんよ。それより長かったらちょっと困りますけどね。",
          "二三日ならかまいませんよ。それより長かったらちょっと困りますけどね。"], 0, [0, 1, 1, 0, 0]),
        ("word-01-term.wav", "大家さん", ["大家さん", "おおやさん", "オオヤさん"], 0, [1, 0, 0, 0, 0]),
        ("word-01-example.wav", "大家さんに家賃を払いました。",
         ["おおやさんに家賃を払いました。", "おおやさんにやちんを払いました。", "おおやさんにヤチンを払いました。"], 6, [1, 0, 0]),
        ("word-02-term.wav", "家賃", ["家賃", "やちん", "ヤチン"], 0, [1, 0, 0]),
        ("word-02-example.wav", "家賃は月に七万円です。", ["家賃は月に七万円です。", "やちんは月に七万円です。", "ヤチンは月に七万円です。"], 0, [1, 0, 0]),
        ("word-11-term.wav", "隣の人", ["隣の人", "となりの人", "となりのひと"], 0, None),
    ],
}
# 写法是整句送进 TTS 的文字（只给 tts 用，页面原文不变）；第 3 种写法对 二、三日 是去掉顿号的「二三日」


def f0_track(audio: np.ndarray, sr: int) -> tuple[np.ndarray, np.ndarray]:
    """10ms 一帧的自相关基频；无声帧为 nan。"""
    win, hop = int(sr * 0.04), int(sr * 0.01)
    times, vals = [], []
    for i in range(0, max(0, len(audio) - win), hop):
        frame = audio[i:i + win].astype(np.float64)
        times.append((i + win / 2) / sr)
        if np.sqrt(np.mean(frame ** 2)) < 10 ** (-40 / 20):
            vals.append(np.nan)
            continue
        frame = frame - frame.mean()
        corr = np.correlate(frame, frame, mode="full")[win - 1:]
        lo, hi = int(sr / 400), int(sr / 70)
        peak = int(np.argmax(corr[lo:hi])) + lo
        vals.append(sr / peak if corr[peak] > 0.3 * corr[0] else np.nan)
    return np.array(times), np.array(vals)


def accent_score(audio: np.ndarray, sr: int, page_text: str, start_mora: int, pattern: list[int] | None) -> float | None:
    """粗测：有声区间按整句音拍数均分，取目标词每拍的音高（半音），高拍平均 − 低拍平均。越大越像目标重音。"""
    if not pattern:
        return None
    act = np.flatnonzero(np.abs(audio) >= 10 ** (-45 / 20))
    if not len(act):
        return None
    t0, t1 = act[0] / sr, act[-1] / sr
    total = max(1, ja_text.mora_count(page_text))
    per = (t1 - t0) / total
    times, f0 = f0_track(audio, sr)
    st = []
    for k in range(len(pattern)):
        a, b = t0 + (start_mora + k) * per, t0 + (start_mora + k + 1) * per
        seg = f0[(times >= a) & (times < b)]
        seg = seg[~np.isnan(seg)]
        st.append(12 * np.log2(np.median(seg)) if len(seg) else np.nan)
    st = np.array(st)
    hi = st[[i for i, p in enumerate(pattern) if p]]
    lo = st[[i for i, p in enumerate(pattern) if not p]]
    if np.all(np.isnan(hi)) or np.all(np.isnan(lo)):
        return None
    return round(float(np.nanmean(hi) - np.nanmean(lo)), 2)


def main() -> None:
    lesson = g.LESSON
    out_root = g.ROOT / "public" / "audio" / "candidates" / lesson
    tmp = out_root / "_tmp"
    tmp.mkdir(parents=True, exist_ok=True)
    g.OUT = tmp
    g.TERM_ATTEMPTS = g.DIALOGUE_ATTEMPTS = 1
    # 候选只要原始的一版，不做载体短语补救
    dummy = types.ModuleType("fix_term_carrier")
    def _no_carrier(*a, **k):
        raise RuntimeError("候选录音不做载体补救")
    dummy.one_term = _no_carrier
    sys.modules["fix_term_carrier"] = dummy

    config = load_config()
    vid = voice_for_role(config, "card")  # 本课女声 = 词卡声线
    voice = config["voices"][vid]
    model = g.load_model(voice)
    clone = None
    if voice["mode"] != "custom_voice":
        clone = model.create_voice_clone_prompt(ref_audio=str(g.ROOT / voice["reference_audio"]),
                                                ref_text=voice["reference_text"], x_vector_only_mode=False)
    orig_tts_text = g.tts_text
    orig_reading = ja_text.tts_reading
    results = []
    for filename, page, variants, start, pattern in ITEMS[lesson]:
        stem = filename[:-4]
        (out_root / stem).mkdir(parents=True, exist_ok=True)
        for vi, variant in enumerate(variants):
            label_v = "汉字" if vi == 0 else ("平假名" if vi == 1 else "片假名")
            for s in range(SEEDS):
                ja_text.tts_reading = lambda t: t           # 写法原样送进 TTS，不走读音表
                g.tts_text = lambda f, t, _v=variant: orig_tts_text(f, _v)
                g.SEED_BASE = 900 + s
                try:
                    g.generate_one(model, vid, filename, page, config, clone)
                finally:
                    ja_text.tts_reading = orig_reading
                    g.tts_text = orig_tts_text
                wav = tmp / filename
                if not wav.exists():
                    print(f"[SKIP] {stem} {label_v} s{s} 没生成出来", flush=True)
                    continue
                name = f"v{vi + 1}-s{s + 1}"
                dest = out_root / stem / f"{name}.wav"
                shutil.move(wav, dest)
                shutil.move(wav.with_suffix(".json"), dest.with_suffix(".json"))
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(dest), "-c:a", "aac", "-b:a", "64k", "-ac", "1",
                                "-ar", "24000", "-movflags", "+faststart", str(dest.with_suffix(".m4a"))], check=True)
                audio, sr = sf.read(dest, always_2d=False)
                audio = np.asarray(audio, dtype=np.float32)
                asr = check_sentence(transcribe(audio, sr), page)
                score = accent_score(audio, sr, page, start, pattern)
                results.append({"item": stem, "page_text": page, "variant": variant, "variant_label": label_v,
                                "name": name, "accent_score": score, "asr_pass": asr["pass"],
                                "heard": asr["by_model"], "duration": round(len(audio) / sr, 2)})
                print(f"[CAND] {stem} {name} {label_v} 重音分={score} ASR={'过' if asr['pass'] else '不过'} "
                      f"听到={asr['by_model'].get('medium')}", flush=True)
    shutil.rmtree(tmp, ignore_errors=True)
    (out_root / "candidates.json").write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("all done")


if __name__ == "__main__":
    main()
