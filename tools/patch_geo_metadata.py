#!/usr/bin/env python3
"""SAFE metadata + factual patcher for the enso-shide PRODUCTION site.

This is NOT a generator. It performs a controlled migration of the existing
authoritative HTML / Markdown output:

  * never runs rmtree, never regenerates page bodies, never overwrites unknown content
  * idempotent — re-running produces no further change
  * verifies the expected pattern before each edit; fail-closed if unexpected
  * prints changed / skipped / failed file lists; never commits or pushes

Passes:
  P0-A  factual  — online AI is now an OPTIONAL Ensō+ subscription capability
                   (was incorrectly stated as "disabled in v1 / not delivered")
  P0-B  entity   — 4 homepage JSON-LD upgraded to @graph
                   (Organization / WebSite / MobileApplication with stable @id)
  P0-C  hreflang — reciprocal <link rel="alternate" hreflang> across REAL clusters

Usage:  python3 tools/patch_geo_metadata.py [--dry-run]
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://shide.app"
LOCALES = ("zh-Hans", "zh-Hant", "en", "ja")
LOCALE_DIRS = {"zh-Hant": "zh-Hant", "en": "en", "ja": "ja"}  # zh-Hans = root
APP_STORE = "https://apps.apple.com/app/apple-store/id6787128369?pt=129013055&ct=web&mt=8"
DRY = "--dry-run" in sys.argv[1:]

changed: list[str] = []
skipped: list[str] = []
failed: list[str] = []

def rel(p: Path) -> str: return str(p.relative_to(ROOT))
def read(p: Path) -> str: return p.read_text(encoding="utf-8")
def write(p: Path, s: str) -> None:
    if not DRY:
        p.write_text(s, encoding="utf-8", newline="\n")

# ---------------------------------------------------------------- P0-A
# Exact (old -> new). Applied wherever the old substring appears (html/md/llms).
# New strings never contain any old string → order-independent + idempotent.
REPL: list[tuple[str, str]] = [
    # zh-Hans
    ("高成本在线 AI 在 v1 Release 中关闭",
     "在线 AI 整理与成书属 Ensō+ 可选订阅，仅在你主动触发时联网"),
    ("高成本在线 AI 不作为已交付权益",
     "在线 AI 整理与成书属 Ensō+ 可选订阅，不影响本机成书"),
    # zh-Hant
    ("高成本線上 AI 在 v1 Release 中關閉",
     "線上 AI 整理與成書屬 Ensō+ 可選訂閱，僅在你主動觸發時聯網"),
    ("高成本線上 AI 不作為已交付權益",
     "線上 AI 整理與成書屬 Ensō+ 可選訂閱，不影響本機成書"),
    # en
    ("cost-bearing online AI is disabled in the v1 Release",
     "online AI structuring and book generation are an optional Ensō+ subscription capability, used only when you invoke them"),
    ("cost-bearing online AI is disabled in this release",
     "online AI structuring and book generation are an optional Ensō+ subscription capability, used only when you invoke them"),
    ("cost-bearing online AI is disabled in the Release build and is not sold as a subscription benefit",
     "online AI is an optional Ensō+ subscription capability, invoked only when you choose to; the deterministic on-device path works without it"),
    ("the v1 Release disables cost-bearing online AI. Shipping premium books use the deterministic local path",
     "online AI is offered as an optional Ensō+ subscription; shipping premium books can also use the deterministic local path"),
    # ja
    ("課金が発生するオンライン AI は v1 リリースでは無効です",
     "オンライン AI は任意の Ensō+ サブスクリプション機能として提供されます"),
    ("課金が発生するオンライン AI は本リリースでは無効です",
     "オンライン AI は任意の Ensō+ サブスクリプション機能として提供されます"),
    ("課金が発生するオンライン AI はリリースビルドでは無効で、サブスクリプションの特典として販売することはありません",
     "オンライン AI は任意の Ensō+ サブスクリプション機能で、必要なときにのみ使用します"),
    ("v1 リリースは課金が発生するオンライン AI を無効にしています。出荷されるプレミアムの書籍は、決定論的なローカル経路を使用します",
     "オンライン AI は任意の Ensō+ サブスクリプション機能として提供され、決定論的なローカル経路でも書籍を作成できます"),
]

def content_targets() -> list[Path]:
    files = [p for p in ROOT.rglob("*.html") if ".git" not in p.parts]
    files += [p for p in ROOT.rglob("*.md") if ".git" not in p.parts]
    for name in ("llms.txt", "llms-full.txt"):  # AI-readable artifacts (NOT robots.txt)
        if (ROOT / name).exists():
            files.append(ROOT / name)
    return files

def pass_a() -> None:
    for p in content_targets():
        s = read(p); hits = 0
        for old, new in REPL:
            if old in s:
                s = s.replace(old, new); hits += 1
        if hits:
            write(p, s); changed.append(f"[P0-A x{hits}] {rel(p)}")

# ---------------------------------------------------------------- P0-B
def build_graph() -> dict:
    desc = ("拾得 Ensō 用 iPhone 本地记忆库保存回忆、照片与信物，并提供端上 A4 PDF 成书路径；"
            "在线能力和隐私边界均明确标注。")
    feature = [
        "SwiftData on-device private memory store",
        "On-device A4 PDF book rendering",
        "Chinese and English memory fields",
        "Public Chinese cultural timeline",
        "Local guided-chat fallback",
        "Validated bounded GenUI content protocol",
    ]
    return {"@context": "https://schema.org", "@graph": [
        {"@type": "Organization", "@id": f"{BASE}/#organization", "name": "Enso Shide",
         "url": f"{BASE}/", "logo": f"{BASE}/assets/app-icon.png",
         "sameAs": ["https://x.com/ensoshide", "https://www.instagram.com/ensoshide",
                    "https://www.youtube.com/@EnsoShide"]},
        {"@type": "WebSite", "@id": f"{BASE}/#website", "url": f"{BASE}/", "name": "拾得 Ensō",
         "publisher": {"@id": f"{BASE}/#organization"}, "inLanguage": list(LOCALES),
         "about": {"@id": f"{BASE}/#app"}},
        {"@type": "MobileApplication", "@id": f"{BASE}/#app", "name": "拾得 Ensō",
         "alternateName": ["Enso Shide", "Shide", "拾得"], "url": f"{BASE}/",
         "downloadUrl": APP_STORE, "operatingSystem": "iOS 17 or later",
         "applicationCategory": "LifestyleApplication",
         "publisher": {"@id": f"{BASE}/#organization"}, "image": f"{BASE}/assets/app-icon.png",
         "description": desc, "inLanguage": list(LOCALES), "featureList": feature},
    ]}

def pass_b() -> None:
    graph = json.dumps(build_graph(), ensure_ascii=False, separators=(",", ":"))
    new_block = f'<script type="application/ld+json">{graph}</script>'
    for name in ("index.html", "en/index.html", "zh-Hant/index.html", "ja/index.html"):
        p = ROOT / name
        if not p.exists():
            failed.append(f"[P0-B] {name}: missing homepage"); continue
        s = read(p)
        m = re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
        if not m:
            failed.append(f"[P0-B] {name}: no ld+json block"); continue
        cur = m.group(1)
        if '"@graph"' in cur and '"#organization"' in cur:
            skipped.append(f"[P0-B] {name}: already @graph"); continue
        if '"SoftwareApplication"' not in cur:
            failed.append(f"[P0-B] {name}: unexpected ld+json (not SoftwareApplication)"); continue
        write(p, s[:m.start()] + new_block + s[m.end():])
        changed.append(f"[P0-B] {name}")

# ---------------------------------------------------------------- P0-C
def locale_of(parts: tuple[str, ...]) -> str:
    return parts[0] if parts and parts[0] in LOCALE_DIRS else "zh-Hans"

def logical_of(parts: tuple[str, ...]) -> str:
    p = list(parts)
    if p and p[0] in LOCALE_DIRS: p = p[1:]
    if p and p[-1] == "index.html": p = p[:-1]
    return "/".join(p)

def url_for(locale: str, logical: str) -> str:
    prefix = "" if locale == "zh-Hans" else LOCALE_DIRS[locale] + "/"
    path = (prefix + (logical + "/" if logical else "")).strip("/")
    return f"{BASE}/" if not path else f"{BASE}/{path}/"

START, END = "<!-- geo:hreflang:start -->", "<!-- geo:hreflang:end -->"

def pass_c() -> None:
    pages = [p for p in ROOT.rglob("index.html") if ".git" not in p.parts]
    clusters: dict[str, dict[str, str]] = {}
    meta: dict[Path, tuple[str, str]] = {}
    for p in pages:
        parts = p.relative_to(ROOT).parts
        loc, logi = locale_of(parts), logical_of(parts)
        clusters.setdefault(logi, {})[loc] = url_for(loc, logi)
        meta[p] = (loc, logi)
    for p, (loc, logi) in meta.items():
        members = clusters[logi]
        links = [f'  <link rel="alternate" hreflang="{L}" href="{members[L]}">'
                 for L in LOCALES if L in members]
        xdef = members.get("zh-Hans") or members.get("en") or members[loc]
        links.append(f'  <link rel="alternate" hreflang="x-default" href="{xdef}">')
        block = START + "\n" + "\n".join(links) + "\n  " + END
        s = read(p)
        if START in s and END in s:
            s2 = re.sub(re.escape(START) + r".*?" + re.escape(END), block, s, flags=re.S)
            if s2 == s:
                skipped.append(f"[P0-C] {rel(p)}: unchanged"); continue
        else:
            m = re.search(r'<link rel="canonical"[^>]*>', s)
            if not m:
                failed.append(f"[P0-C] {rel(p)}: no canonical anchor"); continue
            s2 = s[:m.end()] + "\n  " + block + s[m.end():]
        write(p, s2); changed.append(f"[P0-C] {rel(p)}")

# ----------------------------------------------------------------
def main() -> int:
    print(f"patch_geo_metadata.py  root={ROOT}  {'DRY-RUN' if DRY else 'APPLY'}")
    pass_a(); pass_b(); pass_c()
    print(f"\n=== CHANGED ({len(changed)}) ===")
    for x in changed: print("  " + x)
    print(f"\n=== SKIPPED ({len(skipped)}) ===")
    for x in skipped: print("  " + x)
    print(f"\n=== FAILED ({len(failed)}) ===")
    for x in failed: print("  " + x)
    return 1 if failed else 0

if __name__ == "__main__":
    raise SystemExit(main())
