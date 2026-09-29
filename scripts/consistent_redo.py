# /// script
# requires-python = ">=3.12"
# dependencies = ["qwen-tts==0.1.1", "soundfile", "numpy", "torch", "faster-whisper", "pykakasi"]
# ///
"""句首短词（はい、ええ 之类）音色像换了个人 → 多录几版，挑「句首那段和句子其余部分音色最接近」的一版。

起因（2026-09-29 Luna 人耳）：gj-05 对话 3「はい。僕も…」、gj-03 对话 2「はい、大丈夫です。…」的「はい」
不像同一个人。克隆偶尔在句首瞬间漂移，平常的闸门（整句音色、ASR、句尾）都抓不到，重录一次也不一定好。
做法：每条录 SEEDS 版，按第一段停顿切开，算句首段和其余部分的音色距离（MFCC 余弦距离，越小越像同一个人），
其它闸门都过的里面挑距离最小的换进课程音频；每版都留在 public/audio/candidates/<课>/<条目>-consistency/ 备查。

用法：LESSON=gj-03 uv run --script scripts/consistent_redo.py dialogue-02 [dialogue-05 ...]"""
import json
import shutil
import subprocess
import sys
import types
from pathlib import Path

import numpy as np
import soundfile as sf

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_lesson_audio as g  # noqa: E402
from standardized_course_tts import load_config  # noqa: E402
from term_audio_policy import head_rest_distance  # noqa: E402

SEEDS = 8


def main() -> None:
    items = sys.argv[1:]
    lesson = g.LESSON
    config = load_config()
    std = g.OUT
    jobs = {**g.A_JOBS, **g.B_JOBS, **g.CARD_JOBS}
    def _no_carrier(*a, **k):
        raise RuntimeError("多版对比时不做载体补救")
    dummy = types.ModuleType("fix_term_carrier")
    dummy.one_term = _no_carrier
    sys.modules["fix_term_carrier"] = dummy
    g.TERM_ATTEMPTS = g.DIALOGUE_ATTEMPTS = 1
    for item in items:
        filename = f"{item}.wav"
        text = jobs[filename]
        vid = next(v for v, j in ((g.voice_for_role(config, "A"), g.A_JOBS), (g.voice_for_role(config, "B"), g.B_JOBS),
                                   (g.voice_for_role(config, "card"), g.CARD_JOBS)) if filename in j)
        voice = config["voices"][vid]
        model = g.load_model(voice)
        clone = None
        if voice["mode"] != "custom_voice":
            clone = model.create_voice_clone_prompt(ref_audio=str(g.ROOT / voice["reference_audio"]),
                                                    ref_text=voice["reference_text"], x_vector_only_mode=False)
        cand_dir = g.ROOT / "public" / "audio" / "candidates" / lesson / f"{item}-consistency"
        tmp = cand_dir / "_tmp"
        tmp.mkdir(parents=True, exist_ok=True)
        g.OUT = tmp
        rows = []
        for s in range(SEEDS):
            g.SEED_BASE = 1100 + s
            g.generate_one(model, vid, filename, text, config, clone)
            wav = tmp / filename
            if not wav.exists():
                continue
            dest = cand_dir / f"s{s + 1}.wav"
            shutil.move(wav, dest)
            shutil.move(wav.with_suffix(".json"), dest.with_suffix(".json"))
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(dest), "-c:a", "aac", "-b:a", "64k", "-ac", "1",
                            "-ar", "24000", str(dest.with_suffix(".m4a"))], check=True)
            meta = json.loads(dest.with_suffix(".json").read_text(encoding="utf-8"))
            audio, sr = sf.read(dest, always_2d=False)
            dist, cut = head_rest_distance(np.asarray(audio, dtype=np.float64), sr)
            asr_ok = (meta.get("sentence_asr") or {}).get("pass", True)
            gates = meta["quality_assessment"]["automatic_pass"] and asr_ok and meta.get("leading_blank", {}).get("pass", True)
            rows.append({"name": dest.stem, "head_rest_distance": dist, "cut_at": round(cut, 2), "gates_pass": bool(gates)})
            print(f"[CONSIST] {lesson}/{item} s{s + 1} 句首↔其余 音色距离={dist}（切在 {cut:.2f}s）闸门={'过' if gates else '不过'}", flush=True)
        shutil.rmtree(tmp, ignore_errors=True)
        (cand_dir / "candidates.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        usable = [r for r in rows if r["head_rest_distance"] is not None]
        usable.sort(key=lambda r: (not r["gates_pass"], r["head_rest_distance"]))
        if not usable:
            print(f"[CONSIST] {lesson}/{item} 没有可用的版本，课程音频不动", flush=True)
            continue
        best = usable[0]
        for ext in (".wav", ".json"):
            old = std / f"{item}{ext}"
            if old.exists():
                shutil.move(old, cand_dir / f"replaced{ext}")
            shutil.copy2(cand_dir / f"{best['name']}{ext}", std / f"{item}{ext}")
        print(f"[CONSIST] {lesson}/{item} 选 {best['name']}（距离 {best['head_rest_distance']}）", flush=True)
    subprocess.run([sys.executable, str(g.ROOT / "scripts" / "publish_audio.py"), lesson], check=True)


if __name__ == "__main__":
    main()
