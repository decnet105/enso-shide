#!/usr/bin/env python3
"""Notify IndexNow (Bing, Yandex, and other participating engines) of new or
changed shide.app URLs, so they crawl them without waiting for organic discovery.

The IndexNow key lives at the repo root as <KEY>.txt and is served at
https://shide.app/<KEY>.txt; the search engine fetches that file to verify
ownership. Run this AFTER the key file is deployed live (push → GitHub Pages).

stdlib only. Google does NOT use IndexNow — for Google use Search Console
(URL Inspection → Request Indexing) or the sitemap.

Usage:
    python3 tools/indexnow_ping.py            # submit the default Batch 2A URL set
    python3 tools/indexnow_ping.py <url> ...  # submit specific URLs
"""
from __future__ import annotations
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOST = "shide.app"
ENDPOINT = "https://api.indexnow.org/indexnow"

# recently created / changed this session — worth a proactive crawl
DEFAULT_URLS = [
    f"https://{HOST}/record-your-life-as-it-happens/",
    f"https://{HOST}/en/record-your-life-as-it-happens/",
    f"https://{HOST}/zh-Hant/record-your-life-as-it-happens/",
    f"https://{HOST}/ja/record-your-life-as-it-happens/",
    f"https://{HOST}/memory-app-vs-storytelling-service/",
    f"https://{HOST}/en/memory-app-vs-storytelling-service/",
    f"https://{HOST}/zh-Hant/memory-app-vs-storytelling-service/",
    f"https://{HOST}/ja/memory-app-vs-storytelling-service/",
    f"https://{HOST}/answers/storyworth-alternative-chinese-families/",
    f"https://{HOST}/en/answers/storyworth-alternative-chinese-families/",
    f"https://{HOST}/zh-Hant/answers/storyworth-alternative-chinese-families/",
    f"https://{HOST}/ja/answers/storyworth-alternative-chinese-families/",
    f"https://{HOST}/answers/turn-your-parents-stories-into-a-book/",
    f"https://{HOST}/en/answers/turn-your-parents-stories-into-a-book/",
    f"https://{HOST}/zh-Hant/answers/turn-your-parents-stories-into-a-book/",
    f"https://{HOST}/ja/answers/turn-your-parents-stories-into-a-book/",
]


def find_key() -> str:
    """The key is a lowercase-hex-named .txt at repo root whose content is the key."""
    for f in sorted(ROOT.glob("*.txt")):
        name = f.stem
        if len(name) >= 8 and all(c in "0123456789abcdef" for c in name):
            if f.read_text(encoding="utf-8").strip() == name:
                return name
    raise SystemExit("no IndexNow key file (<hex>.txt whose content == its name) at repo root")


def main() -> int:
    key = find_key()
    urls = sys.argv[1:] or DEFAULT_URLS
    body = json.dumps({
        "host": HOST,
        "key": key,
        "keyLocation": f"https://{HOST}/{key}.txt",
        "urlList": urls,
    }).encode("utf-8")
    req = urllib.request.Request(
        ENDPOINT, data=body, method="POST",
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    print(f"POST {ENDPOINT}  ({len(urls)} URLs, key {key[:8]}…)")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print(f"HTTP {r.status} {r.reason}")
            print(r.read().decode("utf-8") or "(empty body — 200/202 = accepted)")
    except urllib.error.HTTPError as e:
        # 200 OK / 202 Accepted = good. 403 = key not verifiable (deploy the .txt first).
        print(f"HTTP {e.code} {e.reason}")
        print(e.read().decode("utf-8"))
        return 0 if e.code in (200, 202) else 1
    except urllib.error.URLError as e:
        print(f"network error reaching IndexNow: {e.reason}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
