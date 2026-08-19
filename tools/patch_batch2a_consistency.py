#!/usr/bin/env python3
"""Bounded consistency patch for Batch 2A: downgrade the "year-end automatic
book" strong promise in the two intent clusters that overlap the new pages, so
old pages don't contradict the tightened fact model AI now sees.

SCOPE — exactly two slugs × 4 locales × {index.html, .md twin} = 16 files:
    storyworth-alternative-chinese-families
    turn-your-parents-stories-into-a-book
Does NOT touch page positioning, other pages, or brand-name normalization.

New fact model (matches the Batch 2A pages):
    "When you're ready, Shide can organize the memories you've kept/recorded
     into a digital Life Book, with Chinese and English support."
i.e. no "at year's end it composes …" inevitability.

Replacements are applied per-locale (zh-Hans / zh-Hant olds collide char-for-char
in some clauses, so a flat list would inject simplified chars into a traditional
page). Idempotent, verify-before-replace, fail-closed; prints per-file hits and a
residual scan for any strong-claim token left behind.

Usage:  python3 tools/patch_batch2a_consistency.py
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUGS = ("storyworth-alternative-chinese-families", "turn-your-parents-stories-into-a-book")
PREFIXES = ("", "en/", "zh-Hant/", "ja/")

# tokens that must be GONE from these 16 files after the patch (residual scan)
RESIDUAL = ["year's end", "year-end", "到年底", "年底", "年末"]

REPL = {
    "zh-Hans": [
        ("到年底，它整理成", "当你准备好，它可以整理成"),
        ("到年底它会整理成", "当你准备好，它可以整理成"),
        ("到年底它整理成", "当你准备好，它可以整理成"),
        ("拾得到年底整理成", "当你准备好，拾得可以整理成"),
        ("到年底把他们的故事整理成", "当你准备好，可以把他们的故事整理成"),
        ("年底整理成更精致的书", "整理成更精致的书"),
    ],
    "zh-Hant": [
        ("到年底，它整理成", "當你準備好，它可以整理成"),
        ("到年底它會整理成", "當你準備好，它可以整理成"),
        ("到年底它整理成", "當你準備好，它可以整理成"),
        ("拾得到年底整理成", "當你準備好，拾得可以整理成"),
        ("到年底把他們的故事整理成", "當你準備好，可以把他們的故事整理成"),
        ("年底整理成更精緻的書", "整理成更精緻的書"),
    ],
    "en": [
        ("at year's end it composes a Chinese–English bilingual digital book",
         "when you're ready it can organize your memories into a Chinese–English bilingual digital Life Book"),
        ("At year's end it composes a Chinese–English digital book",
         "When you're ready, Shide can organize your memories into a Chinese–English digital Life Book"),
        ("at year's end it composes a Chinese–English digital book",
         "when you're ready it can organize them into a Chinese–English digital Life Book"),
        ("Shide composes a Chinese–English digital book at year's end and exports a PDF",
         "when you're ready, Shide can organize your memories into a Chinese–English digital Life Book and export a PDF"),
        ("composes the richer year-end book", "helps organize the richer book"),
        ("the premium AI that composes the richer book", "the premium AI that helps organize the richer book"),
        ("memory app that composes an in-phone keepsake book",
         "memory app that can organize your memories into an in-phone keepsake book"),
        ("and composes an in-phone keepsake book you can export as a PDF",
         "and can organize your memories into an in-phone keepsake book you can export as a PDF"),
        ("and compose an in-phone keepsake book with PDF export",
         "and organize your memories into an in-phone keepsake book with PDF export"),
        ("and it composes a Chinese–English keepsake book on your phone",
         "and, when you're ready, it can organize them into a Chinese–English keepsake book on your phone"),
        ("composes a book of their stories at year's end",
         "can organize their stories into a book when you're ready"),
        ("Shide composes a digital book and exports a PDF",
         "Shide can organize your memories into a digital book and export a PDF"),
    ],
    "ja": [
        ("年末には、スマホで読める中英バイリンガルのデジタルブックにまとめ、",
         "準備ができたら、スマホで読める中英バイリンガルのデジタルブックにまとめることができ、"),
        ("年末には中英バイリンガルのデジタルブックにまとめます",
         "準備ができたら中英バイリンガルのデジタルブックにまとめることができます"),
        ("拾得は年末に中英バイリンガルのデジタルブックにまとめ、",
         "準備ができたら、拾得は中英バイリンガルのデジタルブックにまとめ、"),
        ("より豊かな年末の本をまとめる高度な AI", "より豊かな本をまとめる高度な AI"),
        ("年末に中国語と英語のデジタルブックを作成し、",
         "準備ができたら中国語と英語のデジタルブックを作成でき、"),
        ("年末には、整理されて読みやすい中国語と英語のデジタルブックを作成し、",
         "準備ができたら、整理されて読みやすい中国語と英語のデジタルブックを作成でき、"),
        ("年末に親の物語を一冊の本にまとめます",
         "準備ができたら親の物語を一冊の本にまとめることができます"),
    ],
}


def locale_of(path: Path) -> str:
    parts = path.relative_to(ROOT).parts
    return parts[0] if parts[0] in ("en", "zh-Hant", "ja") else "zh-Hans"


def main() -> int:
    files: list[Path] = []
    for slug in SLUGS:
        for pre in PREFIXES:
            files.append(ROOT / pre / "answers" / slug / "index.html")
            files.append(ROOT / pre / "answers" / f"{slug}.md")

    total_hits = 0
    changed_files = 0
    missing = [f for f in files if not f.exists()]
    if missing:
        for m in missing:
            print(f"MISSING: {m.relative_to(ROOT)}")
        return 2

    for f in files:
        loc = locale_of(f)
        text = f.read_text(encoding="utf-8")
        orig = text
        hits = 0
        for old, new in REPL[loc]:
            if old in text:
                n = text.count(old)
                text = text.replace(old, new)
                hits += n
        if text != orig:
            f.write_text(text, encoding="utf-8")
            changed_files += 1
            total_hits += hits
            print(f"  ~ {f.relative_to(ROOT)}  ({hits} replacement(s))")

    # residual scan — any strong-claim token left in the 16 files = failure
    residual = []
    for f in files:
        text = f.read_text(encoding="utf-8")
        for tok in RESIDUAL:
            if tok in text:
                residual.append(f"{f.relative_to(ROOT)}: still contains {tok!r}")

    print(f"\nchanged files: {changed_files} / {len(files)}   total replacements: {total_hits}")
    if residual:
        print(f"RESIDUAL STRONG-CLAIM TOKENS ({len(residual)}):")
        for r in residual:
            print("  ! " + r)
        return 1
    print("residual scan: clean — no year-end auto-book tokens remain in the 2 clusters.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
