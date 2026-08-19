#!/usr/bin/env python3
"""Validate the enso-shide production site after a safe metadata patch.

Read-only. Checks the full P0 Batch 1 acceptance list across ALL pages:
hreflang (self / reciprocal / existing-target / valid-code / x-default / no-dup),
canonical (single / self / exists), JSON-LD (parse / homepage @graph / @id resolve /
no fake rating), content (no obsolete AI-disabled claim / optional Ensō+ / local-first),
and site integrity vs a recorded baseline. Exit 1 on any failure.

Usage:  python3 tools/validate_geo_site.py
"""
from __future__ import annotations
import hashlib
import json
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://shide.app"
LOCALES = ("zh-Hans", "zh-Hant", "en", "ja")
LOCALE_DIRS = {"zh-Hant": "zh-Hant", "en": "en", "ja": "ja"}

# ---- baseline snapshot (captured before patch, 2026-08-19) ----
BASE_HTML = 101
BASE_LOCALE = {"zh-Hans": 26, "en": 25, "zh-Hant": 25, "ja": 25}
BASE_SITEMAP = 100
BASE_ROBOTS_MD5 = "35a4f54e4501dceaad6c62538171fff8"

# obsolete claims that must NOT remain anywhere
OBSOLETE = [
    "cost-bearing online AI is disabled", "disables cost-bearing online AI",
    "高成本在线 AI", "高成本線上 AI", "不作为已交付", "不作為已交付",
    "課金が発生するオンライン AI は", "リリースでは無効",
]

errors: list[str] = []
no_twin: list[str] = []
def fail(msg: str) -> None: errors.append(msg)

class Head(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.canonicals: list[str] = []
        self.hreflang: list[tuple[str, str]] = []
        self.md_twin: str | None = None
        self.ld: list[str] = []
        self._in_ld = False; self._buf: list[str] = []
    def handle_starttag(self, tag, attrs):
        v = dict(attrs)
        if tag == "link" and v.get("rel") == "canonical":
            self.canonicals.append(v.get("href") or "")
        if tag == "link" and v.get("rel") == "alternate" and v.get("hreflang"):
            self.hreflang.append((v["hreflang"], v.get("href") or ""))
        if tag == "link" and v.get("type") == "text/markdown":
            self.md_twin = v.get("href")
        if tag == "script" and v.get("type") == "application/ld+json":
            self._in_ld = True; self._buf = []
    def handle_endtag(self, tag):
        if tag == "script" and self._in_ld:
            self._in_ld = False; self.ld.append("".join(self._buf))
    def handle_data(self, data):
        if self._in_ld: self._buf.append(data)

def locale_of(parts): return parts[0] if parts and parts[0] in LOCALE_DIRS else "zh-Hans"
def logical_of(parts):
    p = list(parts)
    if p and p[0] in LOCALE_DIRS: p = p[1:]
    if p and p[-1] == "index.html": p = p[:-1]
    return "/".join(p)
def url_for(locale, logical):
    prefix = "" if locale == "zh-Hans" else LOCALE_DIRS[locale] + "/"
    path = (prefix + (logical + "/" if logical else "")).strip("/")
    return f"{BASE}/" if not path else f"{BASE}/{path}/"
def url_to_path(url):
    if not url.startswith(BASE): return None
    suf = url[len(BASE):].strip("/")
    return ROOT / "index.html" if not suf else ROOT / suf / "index.html"

def main() -> int:
    pages = sorted(p for p in ROOT.rglob("index.html") if ".git" not in p.parts)
    heads: dict[Path, Head] = {}
    clusters: dict[str, dict[str, str]] = {}
    self_url: dict[Path, str] = {}
    hreflang_map: dict[str, set[str]] = {}  # page-url -> set(non-xdefault hrefs)

    for p in pages:
        parts = p.relative_to(ROOT).parts
        loc, logi = locale_of(parts), logical_of(parts)
        u = url_for(loc, logi); self_url[p] = u
        clusters.setdefault(logi, {})[loc] = u
        h = Head(); h.feed(p.read_text(encoding="utf-8")); heads[p] = h

    for p in pages:
        r = str(p.relative_to(ROOT)); h = heads[p]
        parts = p.relative_to(ROOT).parts; loc, logi = locale_of(parts), logical_of(parts)
        u = self_url[p]
        # CANONICAL
        if len(h.canonicals) != 1: fail(f"{r}: expected 1 canonical, found {len(h.canonicals)}")
        elif h.canonicals[0] != u: fail(f"{r}: canonical {h.canonicals[0]!r} != self {u!r}")
        # HREFLANG
        codes = [c for c, _ in h.hreflang]
        if not codes:
            fail(f"{r}: no hreflang")
        else:
            if len(codes) != len(set(codes)): fail(f"{r}: duplicate hreflang code {codes}")
            for c in codes:
                if c not in LOCALES and c != "x-default": fail(f"{r}: invalid hreflang code {c!r}")
            if "x-default" not in codes: fail(f"{r}: missing x-default")
            hmap = {c: href for c, href in h.hreflang}
            if hmap.get(loc) != u: fail(f"{r}: hreflang missing self ({loc}->{u})")
            members = clusters[logi]
            want = {L: members[L] for L in LOCALES if L in members}
            got = {c: hmap[c] for c in hmap if c != "x-default"}
            if got != want: fail(f"{r}: hreflang set {got} != real cluster {want}")
            for c, href in h.hreflang:
                tp = url_to_path(href)
                if tp is None or not tp.exists(): fail(f"{r}: hreflang target missing {c}->{href}")
            hreflang_map[u] = {href for c, href in h.hreflang if c != "x-default"}
        # MARKDOWN TWIN — integrity of EXISTING twins only (some hub pages have none by design)
        if h.md_twin:
            mdp = ROOT / (h.md_twin[len(BASE) + 1:])
            if not mdp.exists(): fail(f"{r}: markdown twin link broken {h.md_twin}")
        else:
            no_twin.append(r)
        # JSON-LD parse
        if not h.ld: fail(f"{r}: no JSON-LD")
        for block in h.ld:
            try: json.loads(block)
            except json.JSONDecodeError as e: fail(f"{r}: JSON-LD parse error {e}")

    # RECIPROCITY
    for u, targets in hreflang_map.items():
        for t in targets:
            if t == u: continue
            back = hreflang_map.get(t)
            if back is None: fail(f"reciprocity: {u} -> {t} but {t} has no hreflang")
            elif u not in back: fail(f"reciprocity: {u} -> {t} not reciprocated")

    # HOMEPAGE @graph
    for name in ("index.html", "en/index.html", "zh-Hant/index.html", "ja/index.html"):
        h = heads.get(ROOT / name)
        if not h: fail(f"{name}: homepage missing"); continue
        graph = None
        for block in h.ld:
            try: obj = json.loads(block)
            except json.JSONDecodeError: continue
            if isinstance(obj, dict) and "@graph" in obj: graph = obj["@graph"]
        if not graph: fail(f"{name}: homepage has no @graph"); continue
        types = {n.get("@type") for n in graph}
        for t in ("Organization", "WebSite", "MobileApplication"):
            if t not in types: fail(f"{name}: @graph missing {t}")
        ids = {n.get("@id") for n in graph}
        for n in graph:  # @id references resolve internally
            for key in ("publisher", "about"):
                ref = n.get(key)
                if isinstance(ref, dict) and ref.get("@id") and ref["@id"] not in ids:
                    fail(f"{name}: unresolved @id ref {ref['@id']}")
        raw = (ROOT / name).read_text(encoding="utf-8")
        for bad in ("aggregateRating", '"review"', "ratingValue", "ratingCount", '"offers"', '"price"'):
            if bad in raw: fail(f"{name}: forbidden fabricated field {bad}")

    # CONTENT
    scan = list(ROOT.rglob("*.html")) + list(ROOT.rglob("*.md")) + [ROOT / "llms.txt", ROOT / "llms-full.txt"]
    for p in scan:
        if ".git" in p.parts or not p.exists(): continue
        raw = p.read_text(encoding="utf-8")
        for token in OBSOLETE:
            if token in raw: fail(f"{p.relative_to(ROOT)}: obsolete AI claim remains {token!r}")
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    if "Ensō+" not in (ROOT / "faq/index.html").read_text(encoding="utf-8") and "Ensō+" not in home:
        fail("content: optional Ensō+ wording not found")
    if "本地优先" not in home and "本地记忆" not in home:
        fail("content: local-first positioning not found on home")

    # SITE INTEGRITY
    n_html = sum(1 for _ in ROOT.rglob("*.html") if ".git" not in _.parts)
    if n_html != BASE_HTML: fail(f"integrity: HTML count {n_html} != baseline {BASE_HTML}")
    loc_counts = {"en": 0, "zh-Hant": 0, "ja": 0, "zh-Hans": 0}
    for p in ROOT.rglob("*.html"):
        if ".git" in p.parts: continue
        parts = p.relative_to(ROOT).parts
        loc_counts[parts[0] if parts[0] in LOCALE_DIRS else "zh-Hans"] += 1
    for L, want in BASE_LOCALE.items():
        if loc_counts[L] != want: fail(f"integrity: {L} html {loc_counts[L]} != baseline {want}")
    sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    n_loc = sm.count("<loc>")
    if n_loc != BASE_SITEMAP: fail(f"integrity: sitemap loc {n_loc} != baseline {BASE_SITEMAP}")
    import re as _re
    for u in _re.findall(r"<loc>([^<]+)</loc>", sm):
        tp = url_to_path(u)
        if tp is None or not tp.exists(): fail(f"integrity: sitemap URL has no page {u}")
    robots = ROOT / "robots.txt"
    md5 = hashlib.md5(robots.read_bytes()).hexdigest()
    if md5 != BASE_ROBOTS_MD5: fail(f"integrity: robots.txt changed (md5 {md5} != {BASE_ROBOTS_MD5})")
    if not list(ROOT.glob("timeline/*/index.html")): fail("integrity: timeline pages missing")
    if not list(ROOT.glob("answers/*/index.html")): fail("integrity: long-tail answers pages missing")

    print(f"pages checked: {len(pages)}   clusters: {len(clusters)}   html: {n_html}   sitemap: {n_loc}")
    print(f"locale counts: {loc_counts}")
    if no_twin:
        print(f"note: {len(no_twin)} page(s) have no markdown twin by design (pre-existing): {', '.join(no_twin)}")
    if errors:
        print(f"\nVALIDATION FAILED ({len(errors)} issues):")
        for e in errors[:80]: print("  - " + e)
        return 1
    print("\nVALIDATION PASSED — all checks green.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
