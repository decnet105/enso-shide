#!/usr/bin/env python3
"""为已发布的 YouTube 视频生成 shide.app/v/<slug>/ 文字记录页（简体单语）。

为什么要这批页（2026-09-03 调研结论，见 Mystory
docs/growth/ai-bot-inbound-strategy-2026-09-03.md）：
LLM 不看视频画面，只读文字；而 youtube.com/robots.txt 封了 /timedtext_video，
所以我们上传的 CC 轨对合规 AI 爬虫不可见。唯一能让 AI 合法读到视频内容的通道，
是把逐字稿放在我们自己控制 robots.txt 的域名上，并配 VideoObject 结构化数据。

纪律（与 add_batch2a_pages.py 一致）：
  - 只**新增**文件，绝不 rmtree、绝不重生成既有页 body
  - 幂等：重复运行对已存在且内容相同的页面 skip
  - fail-closed：清单缺字段、页面已存在但内容不同、模板抓取失败 → 报错退出，不写半截
  - 不 commit / 不 push
  - 站点树守卫：必须在含 CNAME=shide.app 的树里运行

用法：
  python3 tools/add_video_pages.py --manifest <video-pages-manifest.json> \
      --headers <fable-headers.json> [--apply]
不带 --apply 是 dry-run，只打印将要发生什么。
"""
import argparse, html, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://shide.app"
TEMPLATE_PAGE = ROOT / "answers" / "local-first-journal" / "index.html"


def guard():
    cname = ROOT / "CNAME"
    if not cname.exists() or cname.read_text(encoding="utf-8").strip() != "shide.app":
        sys.exit(f"守卫：{ROOT} 不是 shide.app 站点树（CNAME 不符），拒绝运行。")


def chrome():
    """从既有页原样取 header 与 footer，保证新页与全站一致（不自己发明导航）。"""
    src = TEMPLATE_PAGE.read_text(encoding="utf-8")
    mh = re.search(r"(<header class=\"site-header\">.*?</header>)", src, re.S)
    mf = re.search(r"(<footer.*?</footer>)", src, re.S)
    if not mh or not mf:
        sys.exit("fail-closed：无法从模板页提取 header/footer，拒绝生成。")
    return mh.group(1), mf.group(1)


def esc(s):
    return html.escape(str(s or ""), quote=True)


def build_html(it, hd, header, footer):
    slug = it["slug"]
    url = f"{BASE}/v/{slug}/"
    title = hd["h1"]
    desc = hd["answer"]
    lines = it["transcript_lines"]
    transcript_txt = "\n".join(lines)

    video_obj = {
        "@context": "https://schema.org", "@type": "VideoObject",
        "name": title, "description": desc, "inLanguage": "zh-Hans",
        "thumbnailUrl": it["thumbnail"], "contentUrl": it["watch_url"],
        "embedUrl": f"https://www.youtube.com/embed/{it['youtube_id']}",
        "mainEntityOfPage": url, "transcript": transcript_txt,
        "publisher": {"@id": f"{BASE}/#organization"},
    }
    if it.get("published_at"):
        video_obj["uploadDate"] = it["published_at"]
    if it.get("duration_sec"):
        video_obj["duration"] = f"PT{int(it['duration_sec'])}S"

    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q,
         "acceptedAnswer": {"@type": "Answer", "text": desc}} for q in hd["intent"]]}

    ev = it.get("evidence_card")
    if ev:
        prov = ("<p class=\"note\">本片的事实与来源逐条记录在拾得内部证据卡中，"
                "视频发布前已逐项核验。</p>")
    else:
        prov = ("<p class=\"note\">本页是该视频旁白的完整文字记录。"
                "这条片制作于拾得建立逐条来源登记制度之前，因此本页只提供原文，"
                "不另附来源清单——我们不为没有留档的内容补写出处。</p>")

    body_lines = "\n".join(f"      <p>{esc(x)}</p>" for x in lines)
    qs = "\n".join(f"      <li>{esc(q)}</li>" for q in hd["intent"])

    return f"""<!doctype html>
<html lang="zh-Hans">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{esc(title)} | 拾得 Ensō</title>
  <meta name="description" content="{esc(desc)}">
  <meta name="robots" content="index,follow,max-image-preview:large">
  <meta name="theme-color" content="#a4472d">
  <link rel="canonical" href="{url}">
  <!-- geo:hreflang:start -->
  <link rel="alternate" hreflang="zh-Hans" href="{url}">
  <link rel="alternate" hreflang="x-default" href="{url}">
  <!-- geo:hreflang:end -->
  <link rel="alternate" type="text/markdown" href="{BASE}/v/{slug}.md" title="Markdown twin">
  <link rel="icon" type="image/png" href="../../assets/enso-seal-official.png">
  <link rel="apple-touch-icon" href="../../assets/enso-seal-official.png">
  <link rel="stylesheet" href="../../assets/styles.css">
  <meta property="og:type" content="video.other">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(desc)}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{esc(it['thumbnail'])}">
  <meta name="twitter:card" content="summary_large_image">
  <script type="application/ld+json">{json.dumps(video_obj, ensure_ascii=False)}</script>
  <script type="application/ld+json">{json.dumps(faq, ensure_ascii=False)}</script>
</head>
<body>
  <a class="skip-link" href="#main">跳到正文</a>
  {header}
  <main id="main">
    <article>
      <h1>{esc(title)}</h1>
      <p class="lede"><strong>{esc(desc)}</strong></p>
      <p class="note">{esc(it['series'])} · 编号 {esc(it['catalog_no'])} ·
        <a href="{esc(it['watch_url'])}" rel="noopener">在 YouTube 观看原片 ↗</a></p>

      <h2>这一页能回答什么</h2>
      <ul>
{qs}
      </ul>

      <h2>视频全文</h2>
      {prov}
{body_lines}

      <h2>出处</h2>
      <p>本文字记录整理自拾得频道视频《{esc(it['title'])}》。
        <a href="{esc(it['watch_url'])}" rel="noopener">原片在 YouTube</a>。</p>
    </article>
  </main>
  {footer}
</body>
</html>
"""


def build_md(it, hd):
    lines = "\n\n".join(it["transcript_lines"])
    qs = "\n".join(f"- {q}" for q in hd["intent"])
    return f"""# {hd['h1']}

> {hd['answer']}

{it['series']} · 编号 {it['catalog_no']} · [在 YouTube 观看原片]({it['watch_url']})

## 这一页能回答什么

{qs}

## 视频全文

{lines}

## 出处

本文字记录整理自拾得频道视频《{it['title']}》。原片：{it['watch_url']}
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--headers", required=True)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    guard()

    man = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    heads = {h["no"]: h for h in json.loads(Path(args.headers).read_text(encoding="utf-8"))}
    header, footer = chrome()

    items = man["items"]
    missing = [i["catalog_no"] for i in items if i["catalog_no"] not in heads]
    if missing:
        sys.exit(f"fail-closed：以下编号缺页头文案，拒绝生成：{missing}")
    for h in heads.values():
        for k in ("h1", "answer", "intent"):
            if not h.get(k):
                sys.exit(f"fail-closed：{h['no']} 的 {k} 为空，拒绝生成。")

    created, skipped, conflict = [], [], []
    sitemap_add = []
    for it in items:
        hd = heads[it["catalog_no"]]
        d = ROOT / "v" / it["slug"]
        page, md = d / "index.html", ROOT / "v" / f"{it['slug']}.md"
        new_html, new_md = build_html(it, hd, header, footer), build_md(it, hd)
        if page.exists():
            if page.read_text(encoding="utf-8") == new_html:
                skipped.append(it["slug"]); continue
            conflict.append(it["slug"]); continue
        created.append(it["slug"]); sitemap_add.append(f"{BASE}/v/{it['slug']}/")
        if args.apply:
            d.mkdir(parents=True, exist_ok=True)
            page.write_text(new_html, encoding="utf-8")
            md.write_text(new_md, encoding="utf-8")

    if conflict:
        sys.exit(f"fail-closed：以下页面已存在且内容不同，需人工确认：{conflict}")

    # sitemap 幂等追加
    sm = ROOT / "sitemap.xml"
    txt = sm.read_text(encoding="utf-8")
    to_add = [u for u in sitemap_add if f"<loc>{u}</loc>" not in txt]
    if to_add and args.apply:
        block = "".join(f"  <url><loc>{u}</loc></url>\n" for u in to_add)
        txt = txt.replace("</urlset>", block + "</urlset>")
        sm.write_text(txt, encoding="utf-8")

    print(f"{'已写入' if args.apply else 'DRY-RUN 将写入'}：{len(created)} 页")
    for s in created: print(f"  + /v/{s}/")
    if skipped: print(f"跳过（已存在且相同）：{len(skipped)}")
    print(f"sitemap 新增：{len(to_add)} 条")
    if not args.apply:
        print("\n未加 --apply，什么都没写。")


if __name__ == "__main__":
    main()
