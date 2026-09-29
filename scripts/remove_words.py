#!/usr/bin/env python3
"""从一课的 lessonWords / bonusWords 里去掉指定的词，并把剩下的词的音频重新编号，让编号和位置一致
（generate_lesson_audio.py 是按位置给 lesson-NN / word-NN 编号的，不重排的话以后重录会对不上）。

用法：python3 scripts/remove_words.py gj-01 見せる 旅行する 並ぶ 初めて
被去掉的词的音频挪到 public/audio/candidates/<课>/_removed_words/ 留底（不删）。
起因：Luna 2026-09-29「太简单、太难的词都不能放进单词里」→ 第 1〜6 课先去掉 N5 的词（N3 的场景词保留）。"""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
lesson, drop = sys.argv[1], set(sys.argv[2:])
ts_path = next(p for p in (ROOT / "lib" / "lessons").glob("*.ts") if f"id: '{lesson}'" in p.read_text(encoding="utf-8"))
src = ts_path.read_text(encoding="utf-8")
std = ROOT / "public" / "audio" / "standard" / lesson
all_ja = set(re.findall(r"ja: '((?:[^'\\]|\\.)*)'", src))
if drop - all_ja:
    raise SystemExit(f"{lesson} 里找不到这些词：{sorted(drop - all_ja)}（什么都没改）")
keep_dir = ROOT / "public" / "audio" / "candidates" / lesson / "_removed_words"
keep_dir.mkdir(parents=True, exist_ok=True)

renames: list[tuple[str, str]] = []  # (旧前缀, 新前缀)，如 ("word-05", "word-04")
removed: list[str] = []


def process(block_name: str, prefix: str, entry_re: str) -> None:
    global src
    m = re.search(block_name + r": \[\n(.*?)\n  \],", src, re.S)
    body = m.group(1)
    entries = re.findall(entry_re, body + "\n", re.S)
    new_entries, n = [], 0
    for e in entries:
        ja = re.search(r"ja: '((?:[^'\\]|\\.)*)'", e).group(1)
        old = re.search(rf"/{prefix}-(\d\d)-", e).group(1)
        if ja in drop:
            removed.append(f"{prefix}-{old}（{ja}）")
            for f in std.glob(f"{prefix}-{old}-*"):
                shutil.move(f, keep_dir / f.name)
            continue
        n += 1
        new = f"{n:02d}"
        if new != old:
            renames.append((f"{prefix}-{old}", f"{prefix}-{new}"))
            e = e.replace(f"/{prefix}-{old}-", f"/{prefix}-{new}-")
        new_entries.append(e)
    src = src.replace(body, "".join(new_entries).rstrip("\n"))


process("lessonWords", "lesson", r"    \{\n.*?\n    \},\n")
process("bonusWords", "word", r"    \{ ja: .*?\},\n")
# 两步改名，避免 word-05 → word-04 时撞上还没挪走的 word-04
for old, new in renames:
    for f in std.glob(f"{old}-*"):
        f.rename(f.with_name("tmp-" + new + f.name[len(old):]))
for f in std.glob("tmp-*"):
    f.rename(f.with_name(f.name[4:]))
ts_path.write_text(src, encoding="utf-8")
print(f"{lesson}：去掉 {'、'.join(removed)}；重新编号 {len(renames)} 组")
