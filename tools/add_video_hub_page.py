#!/usr/bin/env python3
"""为 shide.app/v/ 下已发布的 22 个视频文字记录页新增一个「总览/枢纽页」(v/index.html)，
4 语言版本(zh-Hans 无前缀 / zh-Hant / en / ja)，从首页可以点进来，枢纽页再按系列分类
链接到各个子页面。

为什么要做这一页(2026-09-06)：
创始人指出子页面本身没有4语言、首页也没有链接过去——AI爬虫/搜索引擎/英日文使用者
找不到这批内容的入口。子页面(v/<slug>/)本身内容较长(有的是完整逐字稿)，不在这次
一并翻译；枢纽页足够轻(标题+一句钩子+缩略图)，做4语言性价比高——哪怕子页面暂时
还是中文，英日文使用者至少能看懂"这个频道有什么"、点进YouTube原片看。

纪律(与 add_batch2a_pages.py / add_video_pages.py 一致)：
  - 只新增文件，不 rmtree、不动已有 22 个子页面
  - 幂等：重复运行对已存在且内容相同的页面 skip；内容不同则 fail-closed 报错，不静默覆盖
  - 站点树守卫：必须在含 CNAME=shide.app 的树里运行
  - zh-Hans/zh-Hant 两侧标题与简介互相走 OpenCC(s2twp / t2s) 转换，不重新编写事实；
    en/ja 的分类名+导语+每条视频一句 hook 由 Fable 预先写好(见 tools/data/v-hub-copy.json)

用法：
    python3 tools/add_video_hub_page.py [--force]
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://shide.app"
LOCALES = ("zh-Hans", "zh-Hant", "en", "ja")
PREFIX = {"zh-Hans": "", "zh-Hant": "zh-Hant/", "en": "en/", "ja": "ja/"}
COPY_JSON = Path(
    "/private/tmp/claude-501/-Users-kilvonwu-Documents-Mystory/"
    "179f78f5-6c75-4d27-acff-6ab8ea1b1a43/scratchpad/v-hub-copy.json"
)
DATE = "2026-09-06"

CATEGORY_ORDER = ["shanhe", "music", "ledger", "screen", "crossover", "story"]
CATEGORY_OF = {
    "shanhe-1993": "shanhe", "shanhe-1980": "shanhe",
    "music-01": "music", "music-02": "music", "music-03": "music", "music-04": "music",
    "music-05": "music", "music-06": "music", "music-07": "music", "music-08": "music",
    "ledger-01": "ledger", "ledger-02": "ledger", "ledger-03": "ledger",
    "ledger-04": "ledger", "ledger-05": "ledger",
    "screen-01": "screen", "screen-02": "screen",
    "crossover-01": "crossover", "crossover-02": "crossover", "crossover-05": "crossover",
    "story-01": "story", "story-03": "story",
}
# 每个系列内，条目按这个顺序展示(即子页面本来的编号顺序)
SLUG_ORDER = [
    "shanhe-1993", "shanhe-1980",
    "music-01", "music-02", "music-03", "music-04", "music-05", "music-06", "music-07", "music-08",
    "ledger-01", "ledger-02", "ledger-03", "ledger-04", "ledger-05",
    "screen-01", "screen-02",
    "crossover-01", "crossover-02", "crossover-05",
    "story-01", "story-03",
]

CHROME = {
    "zh-Hans": {
        "skip": "跳到正文", "brand_href": f"{BASE}/", "nav_label": "主导航", "lang_label": "简体中文",
        "nav": [(f"{BASE}/", "首页"), (f"{BASE}/features/", "功能"),
                (f"{BASE}/evidence/", "事实证据"), (f"{BASE}/faq/", "问答")],
        "watch_yt": "在 YouTube 观看", "read_transcript": "阅读文字记录 →",
        "read_md": "阅读本页 Markdown", "factchecked": f"页面更新 {DATE}",
        "store": "在 App Store 下载拾得",
        "disclosure": "本页是拾得 YouTube 频道 @EnsoShide 全部视频的总览索引，逐条链接到文字记录页与 YouTube 原片。",
    },
    "zh-Hant": {
        "skip": "跳到正文", "brand_href": f"{BASE}/zh-Hant/", "nav_label": "主導航", "lang_label": "繁體中文",
        "nav": [(f"{BASE}/zh-Hant/", "首頁"), (f"{BASE}/zh-Hant/features/", "功能"),
                (f"{BASE}/zh-Hant/evidence/", "事實證據"), (f"{BASE}/zh-Hant/faq/", "問答")],
        "watch_yt": "在 YouTube 觀看", "read_transcript": "閱讀文字記錄 →",
        "read_md": "閱讀本頁 Markdown", "factchecked": f"頁面更新 {DATE}",
        "store": "在 App Store 下載拾得",
        "disclosure": "本頁是拾得 YouTube 頻道 @EnsoShide 全部影片的總覽索引，逐條連結到文字記錄頁與 YouTube 原片。",
    },
    "en": {
        "skip": "Skip to content", "brand_href": f"{BASE}/", "nav_label": "Main navigation", "lang_label": "English",
        "nav": [(f"{BASE}/en/", "Home"), (f"{BASE}/en/features/", "Features"),
                (f"{BASE}/en/evidence/", "Evidence"), (f"{BASE}/en/faq/", "FAQ")],
        "watch_yt": "Watch on YouTube", "read_transcript": "Read transcript →",
        "read_md": "Read this page in Markdown", "factchecked": f"Page updated {DATE}",
        "store": "Download Shide on the App Store",
        "disclosure": "This page indexes every video on the Enso Shide YouTube channel (@EnsoShide), linking to each transcript page and the original on YouTube.",
    },
    "ja": {
        "skip": "本文へスキップ", "brand_href": f"{BASE}/", "nav_label": "メインナビゲーション", "lang_label": "日本語",
        "nav": [(f"{BASE}/ja/", "ホーム"), (f"{BASE}/ja/features/", "機能"),
                (f"{BASE}/ja/evidence/", "エビデンス"), (f"{BASE}/ja/faq/", "FAQ")],
        "watch_yt": "YouTubeで見る", "read_transcript": "文字起こしを読む →",
        "read_md": "このページを Markdown で読む", "factchecked": f"ページ更新 {DATE}",
        "store": "App Store で拾得をダウンロード",
        "disclosure": "このページは拾得の YouTube チャンネル(@EnsoShide)の全動画索引です。各文字起こしページと YouTube 本編にリンクします。",
    },
}


def guard() -> None:
    cname = ROOT / "CNAME"
    if not cname.exists() or cname.read_text(encoding="utf-8").strip() != "shide.app":
        sys.exit(f"守卫：{ROOT} 不是 shide.app 站点树（CNAME 不符），拒绝运行。")


def esc_text(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def esc_attr(s: str) -> str:
    return esc_text(s).replace('"', "&quot;").replace("'", "&#x27;")


def extract_items() -> list[dict]:
    items = []
    for slug in SLUG_ORDER:
        f = ROOT / "v" / slug / "index.html"
        src = f.read_text(encoding="utf-8")
        title = re.search(r"<title>(.*?) \| 拾得", src, re.S).group(1)
        desc = re.search(r'name="description" content="([^"]*)"', src).group(1)
        thumb = re.search(r'og:image" content="([^"]*)"', src).group(1)
        watch = re.search(r'"contentUrl": *"([^"]*)"', src).group(1)
        upload = re.search(r'"uploadDate": *"([^"]*)"', src)
        script = "hant" if slug.startswith("shanhe") else "hans"
        items.append({
            "slug": slug, "category": CATEGORY_OF[slug], "native_script": script,
            "native_title": title, "native_desc": desc,
            "thumb": thumb, "watch_url": watch,
            "upload_date": upload.group(1) if upload else None,
        })
    return items


def build_script_variants(items: list[dict]) -> None:
    import opencc
    s2twp = opencc.OpenCC("s2twp")
    t2s = opencc.OpenCC("t2s")
    for it in items:
        if it["native_script"] == "hans":
            it["title_hans"], it["desc_hans"] = it["native_title"], it["native_desc"]
            it["title_hant"] = s2twp.convert(it["native_title"])
            it["desc_hant"] = s2twp.convert(it["native_desc"])
        else:
            it["title_hant"], it["desc_hant"] = it["native_title"], it["native_desc"]
            it["title_hans"] = t2s.convert(it["native_title"])
            it["desc_hans"] = t2s.convert(it["native_desc"])


def page_url(locale: str) -> str:
    return f"{BASE}/{PREFIX[locale]}v/"


def md_url(locale: str) -> str:
    return f"{BASE}/{PREFIX[locale]}v.md"


def render_hreflang() -> str:
    out = ["  <!-- geo:hreflang:start -->"]
    for L in LOCALES:
        out.append(f'  <link rel="alternate" hreflang="{L}" href="{page_url(L)}">')
    out.append(f'  <link rel="alternate" hreflang="x-default" href="{page_url("zh-Hans")}">')
    out.append("  <!-- geo:hreflang:end -->")
    return "\n".join(out)


def render_lang_switch(locale: str) -> str:
    parts = []
    for L in LOCALES:
        label = CHROME[L]["lang_label"]
        if L == locale:
            parts.append(f'<strong class="language-link" aria-current="true">{label}</strong>')
        else:
            parts.append(f'<a class="language-link" href="{page_url(L)}" hreflang="{L}">{label}</a>')
    return " · ".join(parts)


def item_text(locale: str, it: dict, copy: dict) -> tuple[str, str]:
    """返回该 locale 下这一条视频要显示的 (标题, 一句话)。"""
    if locale == "zh-Hans":
        return it["title_hans"], it["desc_hans"]
    if locale == "zh-Hant":
        return it["title_hant"], it["desc_hant"]
    # en / ja：标题保留原始语种（大量专有名词/歌名/片名），下面配 Fable 写的一句 hook
    native_title = it["title_hant"] if it["native_script"] == "hant" else it["title_hans"]
    hook = copy["items"][it["slug"]][locale]
    return native_title, hook


def render_card(locale: str, it: dict, copy: dict, ch: dict) -> str:
    title, line = item_text(locale, it, copy)
    transcript_url = f"{BASE}/v/{it['slug']}/"
    return f'''<a class="video-card" href="{transcript_url}">
        <img loading="lazy" width="480" height="270" src="{esc_attr(it["thumb"])}" alt="{esc_attr(title)}">
        <div class="video-card-body">
          <h3>{esc_text(title)}</h3>
          <p>{esc_text(line)}</p>
          <span class="video-card-cta">{esc_text(ch["read_transcript"])}</span>
        </div>
      </a>'''


def render_video_object(locale: str, it: dict, copy: dict) -> dict:
    title, desc = item_text(locale, it, copy)
    d = {
        "@type": "VideoObject", "name": title, "description": desc,
        "thumbnailUrl": it["thumb"], "contentUrl": it["watch_url"],
        "url": f"{BASE}/v/{it['slug']}/",
    }
    if it["upload_date"]:
        d["uploadDate"] = it["upload_date"]
    return d


def render_html(locale: str, items: list[dict], copy: dict) -> str:
    ch = CHROME[locale]
    chrome_copy = copy["chrome"][locale]
    url = page_url(locale)
    murl = md_url(locale)

    item_list_ld = {
        "@context": "https://schema.org", "@type": "ItemList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "item": render_video_object(locale, it, copy)}
            for i, it in enumerate(items)
        ],
    }
    webpage_ld = {
        "@context": "https://schema.org", "@type": "CollectionPage",
        "headline": chrome_copy["page_title"], "description": chrome_copy["meta_desc"],
        "inLanguage": locale, "mainEntityOfPage": url, "dateModified": DATE,
    }

    nav = "".join(f'<a href="{href}">{esc_text(label)}</a>' for href, label in ch["nav"])

    sections = []
    for cat_key in CATEGORY_ORDER:
        cat = copy["categories"][cat_key]
        cat_items = [it for it in items if it["category"] == cat_key]
        cards = "\n      ".join(render_card(locale, it, copy, ch) for it in cat_items)
        sections.append(f'''<section class="video-category">
      <h2>{esc_text(cat["label"][locale])}</h2>
      <p class="category-intro">{esc_text(cat["intro"][locale])}</p>
      <div class="video-grid">
      {cards}
      </div>
    </section>''')
    sections_html = "\n    ".join(sections)

    return f"""<!doctype html>
<html lang="{locale}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{esc_text(chrome_copy["page_title"])} | 拾得 Ensō</title>
  <meta name="description" content="{esc_attr(chrome_copy["meta_desc"])}">
  <meta name="robots" content="index,follow,max-image-preview:large">
  <meta name="theme-color" content="#a4472d">
  <link rel="canonical" href="{url}">
{render_hreflang()}
  <link rel="alternate" type="text/markdown" href="{murl}" title="Markdown twin">
  <link rel="icon" type="image/png" href="{BASE}/assets/enso-seal-official.png">
  <link rel="apple-touch-icon" href="{BASE}/assets/enso-seal-official.png">
  <link rel="stylesheet" href="{BASE}/assets/styles.css">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{esc_attr(chrome_copy["page_title"])}">
  <meta property="og:description" content="{esc_attr(chrome_copy["meta_desc"])}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{BASE}/assets/app-icon.png">
  <meta name="twitter:card" content="summary">
  <script type="application/ld+json">{json.dumps(webpage_ld, ensure_ascii=False)}</script>
  <script type="application/ld+json">{json.dumps(item_list_ld, ensure_ascii=False)}</script>
  <style>
    .video-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:1.25rem;margin:1.25rem 0 2.5rem}}
    .video-card{{display:block;border:1px solid rgba(180,150,90,.3);border-radius:14px;overflow:hidden;text-decoration:none;color:inherit;background:#fff}}
    .video-card img{{display:block;width:100%;height:auto;aspect-ratio:16/9;object-fit:cover}}
    .video-card-body{{padding:.9rem 1rem 1.1rem}}
    .video-card-body h3{{font-size:.95rem;line-height:1.4;margin:0 0 .4rem}}
    .video-card-body p{{font-size:.8rem;line-height:1.5;opacity:.75;margin:0 0 .6rem}}
    .video-card-cta{{font-size:.75rem;font-weight:700;opacity:.9}}
    .category-intro{{opacity:.8;font-size:.9rem;max-width:60ch}}
  </style>
</head>
<body>
  <a class="skip-link" href="#main">{esc_text(ch["skip"])}</a>
  <header class="site-header">
    <a class="brand" href="{ch["brand_href"]}">拾得 Ensō</a>
    <nav aria-label="{esc_attr(ch["nav_label"])}">{nav}</nav>
  <span class="language-switch">{render_lang_switch(locale)}</span></header>
  <main id="main">
    <h1>{esc_text(chrome_copy["h1"])}</h1>
    <p class="lede">{esc_text(chrome_copy["lede"])}</p>
    {sections_html}
  </main>
  <footer><p class="store-line"><a href="https://apps.apple.com/app/apple-store/id6787128369?pt=129013055&ct=web&mt=8" rel="external">{esc_text(ch["store"])}</a></p>
    <p>{esc_text(ch["disclosure"])}</p>
    <p><a href="{murl}">{esc_text(ch["read_md"])}</a> · {esc_text(ch["factchecked"])}</p>
  </footer>
</body>
</html>
"""


def render_md(locale: str, items: list[dict], copy: dict) -> str:
    ch = CHROME[locale]
    chrome_copy = copy["chrome"][locale]
    lines = [f"# {chrome_copy['h1']}", "", chrome_copy["lede"], ""]
    for cat_key in CATEGORY_ORDER:
        cat = copy["categories"][cat_key]
        cat_items = [it for it in items if it["category"] == cat_key]
        lines += [f"## {cat['label'][locale]}", "", cat["intro"][locale], ""]
        for it in cat_items:
            title, line = item_text(locale, it, copy)
            lines += [f"- **{title}** — {line} "
                      f"[{ch['read_transcript'].rstrip(' →')}]({BASE}/v/{it['slug']}/) · "
                      f"[{ch['watch_yt']}]({it['watch_url']})"]
        lines.append("")
    lines += ["---", "", ch["factchecked"], ""]
    return "\n".join(lines)


def write_file(path: Path, content: str, force: bool, created: list, unchanged: list, skipped: list) -> None:
    if path.exists():
        if path.read_text(encoding="utf-8") == content:
            unchanged.append(str(path.relative_to(ROOT)))
            return
        if not force:
            skipped.append(str(path.relative_to(ROOT)) + " (exists & differs; use --force)")
            return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    created.append(str(path.relative_to(ROOT)))


def update_sitemap(new_urls: list[str], created: list, unchanged: list) -> None:
    sm_path = ROOT / "sitemap.xml"
    sm = sm_path.read_text(encoding="utf-8")
    missing = [u for u in new_urls if f"<loc>{u}</loc>" not in sm]
    if not missing:
        unchanged.append("sitemap.xml (all URLs present)")
        return
    block = "".join(f"  <url><loc>{u}</loc></url>\n" for u in missing)
    sm = sm.replace("</urlset>", block + "</urlset>")
    sm_path.write_text(sm, encoding="utf-8")
    created.append(f"sitemap.xml (+{len(missing)} loc)")


def main() -> int:
    guard()
    force = "--force" in sys.argv
    if not COPY_JSON.exists():
        sys.exit(f"fail-closed：找不到 Fable 写的 4 语言文案 {COPY_JSON}")
    copy = json.loads(COPY_JSON.read_text(encoding="utf-8"))

    items = extract_items()
    build_script_variants(items)

    created: list[str] = []
    unchanged: list[str] = []
    skipped: list[str] = []
    new_urls: list[str] = []

    for locale in LOCALES:
        html_path = ROOT / PREFIX[locale] / "v" / "index.html"
        md_path = ROOT / PREFIX[locale] / "v.md"
        write_file(html_path, render_html(locale, items, copy), force, created, unchanged, skipped)
        write_file(md_path, render_md(locale, items, copy), force, created, unchanged, skipped)
        new_urls.append(page_url(locale))

    update_sitemap(new_urls, created, unchanged)

    print(f"created:   {len(created)}")
    for c in created:
        print("  + " + c)
    print(f"unchanged: {len(unchanged)}")
    if skipped:
        print(f"skipped:   {len(skipped)}")
        for s in skipped:
            print("  ! " + s)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
