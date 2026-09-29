#!/usr/bin/env python3
"""查每课单词的 JLPT 等级（Luna 2026-09-29：太简单、太难的词都不能放进单词里，数量不固定）。

词表：jamsinclair/open-anki-jlpt-decks（基于 tanos 的非官方词表，2010 年后 JLPT 官方不公布词表），
下载到 ~/jlpt/n1〜n5.csv。只做精确匹配：原形、去掉「する」、去掉接头「お」、去掉「さん」、读音列；
短语（部屋を探す、道に迷う）拆开查各部分。查不到的标「表外」，由 Luna 判断。
用法：python3 scripts/word_level_check.py [课程 id ...]   # 不给就查全部；草稿课用 --draft 文件
"""
import csv
import glob
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LISTS = Path.home() / "jlpt"
Q = r"'((?:[^'\\]|\\.)*)'"

expr: dict[str, set[int]] = {}
read: dict[str, set[int]] = {}
for n in range(1, 6):
    with open(LISTS / f"n{n}.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for e in re.split(r"[、,／/;]", row["expression"]):
                e = e.strip().lstrip("～〜").rstrip("～〜")
                if e:
                    expr.setdefault(e, set()).add(n)
            for r in re.split(r"[、,／/;]", row["reading"]):
                r = r.strip().lstrip("～〜").rstrip("～〜")
                if r:
                    read.setdefault(r, set()).add(n)


def keys(word: str) -> list[str]:
    w = word.strip()
    out = [w]
    for suf in ("する", "さん"):
        if w.endswith(suf) and len(w) > len(suf):
            out.append(w[: -len(suf)])
    if w.startswith("お") and len(w) > 2:
        out.append(w[1:])
    return out


def level(word: str) -> str:
    for k in keys(word):
        if k in expr:
            return "/".join(f"N{n}" for n in sorted(expr[k], reverse=True))
    for k in keys(word):
        if k in read:
            return "/".join(f"N{n}" for n in sorted(read[k], reverse=True)) + "（按读音）"
    parts = [p for p in re.split(r"[をにがで]", word) if p]
    if len(parts) > 1:
        return "短语：" + "、".join(f"{p}={level(p)}" for p in parts)
    return "表外"


def lesson_words(path: Path) -> tuple[str, str, list[tuple[str, str]]]:
    s = path.read_text(encoding="utf-8")
    lid = re.search(r"id: " + Q, s).group(1)
    badge = re.search(r"badge: " + Q, s).group(1)
    words = []
    for block_name in ("lessonWords", "bonusWords"):
        m = re.search(block_name + r": \[(.*?)\n  \],", s, re.S)
        if m:
            words += [(block_name, w) for w in re.findall(r"ja: " + Q, m.group(1))]
    return lid, badge, words


def draft_words(path: Path) -> list[tuple[str, str, list[tuple[str, str]]]]:
    """从大纲里抽「本节重要单词」「附加单词」两张表的第一列。"""
    out, cur, section = [], None, None
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"# 网站第 \d+ 课（(gj-\d+)", line)
        if m:
            cur = (m.group(1), "JLPT N3" if "N3" in line else "JLPT N4", [])
            out.append(cur)
            continue
        if line.startswith("## 本节重要单词"):
            section = "lessonWords"
        elif line.startswith("## 附加单词"):
            section = "bonusWords"
        elif line.startswith("## "):
            section = None
        elif section and cur and line.startswith("| ") and not line.startswith("| 日语") and not line.startswith("|---"):
            cur[2].append((section, line.split("|")[1].strip()))
    return out


targets = []
args = sys.argv[1:]
if "--draft" in args:
    i = args.index("--draft")
    targets += draft_words(ROOT / args[i + 1])
    del args[i:i + 2]
for p in sorted(glob.glob(str(ROOT / "lib" / "lessons" / "*.ts"))):
    if p.endswith(("types.ts", "index.ts")):
        continue
    lid, badge, words = lesson_words(Path(p))
    if not args or lid in args:
        targets.append((lid, badge, words))
for lid, badge, words in sorted(targets):
    want = int(badge[-1])
    print(f"== {lid}（{badge}）")
    for kind, w in words:
        lv = level(w)
        nums = [int(x) for x in re.findall(r"N(\d)", lv)] if not lv.startswith("短语") else []
        verdict = ""
        if nums:
            if max(nums) > want and min(nums) > want:
                verdict = "  ← 太简单"
            elif min(nums) < want - (1 if want == 3 else 0):
                verdict = "  ← 太难"
        print(f"   {'本课' if kind == 'lessonWords' else '附加'}  {w:<10} {lv}{verdict}")
