#!/usr/bin/env python3
"""修复 head 区的 canonical / hreflang / JSON-LD 结构缺陷（安全 patcher）。

背景：2026-09-03 跑 validate_geo_site.py 发现 80 条失败、涉及 25 个页面，全部已上线。
成因是 novel 子站、spacetime-wall、首页改版等几次提交没跑 validator 就 push：
  A. canonical / hreflang 被写成相对路径（../../faq/index.html），target 解析不到
  B. novel / spacetime-wall / artifact 完全没有 canonical、hreflang、JSON-LD
  C. shenshi 有 canonical 但没有 hreflang
  D. terms 的 hreflang 指向并不存在的 en 版

这些缺陷直接妨碍搜索与 AI 把 shide.app 解析成单一实体，是 AEO 的前置条件。

纪律：只改 head 区已知缺陷；不动正文；不重生成页面；幂等；fail-closed；不 commit/push。
用法：python3 tools/patch_head_integrity.py [--apply]
"""
import argparse, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://shide.app"
LOCALES = ["zh-Hans", "zh-Hant", "en", "ja"]


def guard():
    c = ROOT / "CNAME"
    if not c.exists() or c.read_text(encoding="utf-8").strip() != "shide.app":
        sys.exit(f"守卫：{ROOT} 不是 shide.app 站点树，拒绝运行。")


def locale_of(parts):
    return parts[0] if parts and parts[0] in LOCALES[1:] else "zh-Hans"


def logical_of(parts):
    p = list(parts)
    if p and p[0] in LOCALES[1:]:
        p = p[1:]
    if p and p[-1] == "index.html":
        p = p[:-1]
    return "/".join(p)


def url_for(loc, logi):
    seg = "" if loc == "zh-Hans" else f"{loc}/"
    return f"{BASE}/{seg}{logi}/" if logi else f"{BASE}/{seg}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    guard()

    pages = sorted(p for p in ROOT.rglob("index.html") if ".git" not in p.parts)
    clusters = {}
    self_url = {}
    for p in pages:
        parts = p.relative_to(ROOT).parts
        loc, logi = locale_of(parts), logical_of(parts)
        u = url_for(loc, logi)
        self_url[p] = (loc, logi, u)
        clusters.setdefault(logi, {})[loc] = u

    changed, skipped, failed = [], [], []
    for p in pages:
        loc, logi, u = self_url[p]
        src = orig = p.read_text(encoding="utf-8")
        head_end = src.find("</head>")
        if head_end < 0:
            failed.append((str(p.relative_to(ROOT)), "无 </head>")); continue

        members = clusters[logi]
        want = [(L, members[L]) for L in LOCALES if L in members]

        # --- A/D: 重建 hreflang 块为绝对 URL、且只列真实存在的语言 ---
        block = "  <!-- geo:hreflang:start -->\n" + "".join(
            f'  <link rel="alternate" hreflang="{L}" href="{h}">\n' for L, h in want
        ) + f'  <link rel="alternate" hreflang="x-default" href="{members.get("zh-Hans", u)}">\n' \
            + "  <!-- geo:hreflang:end -->"
        # 先把 head 里所有 hreflang 痕迹清干净（含无标记的手写块），再插唯一一块，
        # 否则会出现「原有正确块 + 新块」的重复 hreflang。
        # 记住原块位置，修好后插回原处——避免把 133 页全量重排，diff 只落在真正坏的页上。
        m = re.search(r"  <!-- geo:hreflang:start -->.*?  <!-- geo:hreflang:end -->", src, re.S)
        if not m:
            m = re.search(r'(?:[ \t]*<link rel="alternate" hreflang="[^"]*"[^>]*>\n?)+', src)
        anchor = m.start() if m else src.find("</head>")
        src = re.sub(r"  <!-- geo:hreflang:start -->.*?  <!-- geo:hreflang:end -->\n?", "", src, flags=re.S)
        src = re.sub(r'[ \t]*<link rel="alternate" hreflang="[^"]*"[^>]*>\n?', "", src)
        anchor = min(anchor, src.find("</head>"))
        src = src[:anchor] + block + "\n" + src[anchor:]

        # --- A/B: canonical 必须是绝对自指 ---
        can = f'  <link rel="canonical" href="{u}">'
        if re.search(r'<link rel="canonical"[^>]*>', src):
            src = re.sub(r'\s*<link rel="canonical"[^>]*>', "\n" + can, src, count=1)
            src = re.sub(r'\s*<link rel="canonical"[^>]*>(?=[\s\S]*?</head>)', "",
                         src[src.find(can) + len(can):]) and src or src
        else:
            src = src[:src.find("</head>")] + can + "\n" + src[src.find("</head>"):]
        # 去掉可能出现的重复 canonical（只保留第一个）
        cans = list(re.finditer(r'\s*<link rel="canonical"[^>]*>', src))
        for m in reversed(cans[1:]):
            src = src[:m.start()] + src[m.end():]

        # --- B: 完全没有 JSON-LD → 补一个最小 WebPage 实体 ---
        if "application/ld+json" not in src:
            t = re.search(r"<title>(.*?)</title>", src, re.S)
            d = re.search(r'<meta name="description" content="(.*?)"', src, re.S)
            ld = {"@context": "https://schema.org", "@type": "WebPage",
                  "name": (t.group(1).split("|")[0].strip() if t else ""),
                  "description": (d.group(1).strip() if d else ""),
                  "inLanguage": loc, "url": u,
                  "isPartOf": {"@id": f"{BASE}/#website"},
                  "publisher": {"@id": f"{BASE}/#organization"}}
            tag = f'  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n'
            src = src[:src.find("</head>")] + tag + src[src.find("</head>"):]

        if src == orig:
            skipped.append(str(p.relative_to(ROOT)))
        else:
            changed.append(str(p.relative_to(ROOT)))
            if args.apply:
                p.write_text(src, encoding="utf-8")

    print(f"{'已修复' if args.apply else 'DRY-RUN 将修复'}：{len(changed)} 页 · 无需改动 {len(skipped)} 页")
    for c in changed[:40]:
        print(f"  ~ {c}")
    if len(changed) > 40:
        print(f"  … 另 {len(changed)-40} 页")
    if failed:
        print("失败：")
        for f, why in failed:
            print(f"  ! {f}: {why}")
        sys.exit(1)
    if not args.apply:
        print("\n未加 --apply，什么都没写。")


if __name__ == "__main__":
    main()
