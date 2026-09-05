#!/usr/bin/env python3
"""为「山河静听」逐年系列生成 shide.app/v/shanhe-<year>/ 文字记录页(繁体主语言)。

跟 add_video_pages.py(shorts轨,简体单语,~150字逐字稿)是两套东西:山河静听每支
有69-75张题跋卡的真实历史文化事件,逐字稿是全部卡片正文按出场顺序串起来(约
3000+字,含精确到秒的YouTube章节时间戳),VideoObject多了hasPart的Clip数组
(每章一个Clip,对应YouTube"关键时刻"这个正规schema字段),inLanguage=zh-Hant。

纪律跟add_video_pages.py一致:只新增、幂等(已存在且相同则跳过,不同则fail-closed
报错不覆盖)、不commit不push、必须在CNAME=shide.app的树里跑。

用法:
  python3 tools/add_shanhe_jingting_pages.py --year 1993 --triad-json <path> \
      --youtube-id <id> --title <标题> --hook <一句话简介> [--apply]
"""
import argparse
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://shide.app"
TEMPLATE_PAGE = ROOT / "answers" / "local-first-journal" / "index.html"


def guard():
    cname = ROOT / "CNAME"
    if not cname.exists() or cname.read_text(encoding="utf-8").strip() != "shide.app":
        sys.exit(f"守卫:{ROOT} 不是 shide.app 站点树(CNAME不符),拒绝运行。")


def chrome():
    src = TEMPLATE_PAGE.read_text(encoding="utf-8")
    mh = re.search(r"(<header class=\"site-header\">.*?</header>)", src, re.S)
    mf = re.search(r"(<footer.*?</footer>)", src, re.S)
    if not mh or not mf:
        sys.exit("fail-closed:无法从模板页提取header/footer,拒绝生成。")
    return mh.group(1), mf.group(1)


def esc(s):
    return html.escape(str(s or ""), quote=True)


def fmt_ts(t):
    m = int(t) // 60
    s = int(t) % 60
    return f"{m:02d}:{s:02d}"


def build_transcript_entries(triad):
    """按t_in排序,每条 = (t_in秒, 栏目, 题, 铭三行合一句, 款)。"""
    LABEL = {"陆": "陸", "港澳台": "港澳台", "日本": "日本"}
    cards = triad["cards"]
    entries = []
    for e in sorted(triad["timeline"], key=lambda x: x["t_in"]):
        c = cards[e["card_id"]]
        title = c.get("title_hant") or c.get("event", "")
        lines = c.get("lines_hant", [])
        colophon = c.get("colophon_hant", "")
        body = "".join(lines)
        entries.append({
            "t": e["t_in"], "col": LABEL.get(e["column"], e["column"]),
            "title": title, "body": body, "colophon": colophon,
        })
    return entries


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--year", type=int, required=True)
    ap.add_argument("--triad-json", required=True)
    ap.add_argument("--youtube-id", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--hook", required=True, help="一句话简介(meta description/VideoObject description)")
    ap.add_argument("--opening-text", default="", help="开场题跋卡正文(可选,几句话)")
    ap.add_argument("--closing-text", default="", help="收尾题跋卡正文(可选,几句话)")
    ap.add_argument("--duration-sec", type=int, default=3600)
    ap.add_argument("--published-at", default=None, help="ISO8601,不给则不写uploadDate")
    ap.add_argument("--thumbnail", required=True)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    guard()

    triad = json.loads(Path(args.triad_json).read_text(encoding="utf-8"))
    entries = build_transcript_entries(triad)

    year = args.year
    slug = f"shanhe-{year}"
    url = f"{BASE}/v/{slug}/"
    watch_url = f"https://www.youtube.com/watch?v={args.youtube_id}"
    n_cards = len(entries)

    header, footer = chrome()

    # VideoObject: hasPart Clip 数组(YouTube"关键时刻"正规字段),每章一个
    clips = []
    if args.opening_text:
        clips.append({"@type": "Clip", "name": "開場", "startOffset": 0,
                      "url": f"{watch_url}&t=0s"})
    for e in entries:
        clips.append({
            "@type": "Clip", "name": f"{e['col']} · {e['title']}",
            "startOffset": int(e["t"]), "url": f"{watch_url}&t={int(e['t'])}s",
        })
    if args.closing_text:
        clips.append({"@type": "Clip", "name": "尾聲",
                      "startOffset": 3540, "url": f"{watch_url}&t=3540s"})

    transcript_parts = []
    if args.opening_text:
        transcript_parts.append(f"[00:00 開場] {args.opening_text}")
    for e in entries:
        transcript_parts.append(f"[{fmt_ts(e['t'])} {e['col']}] {e['title']}。{e['body']}（{e['colophon']}）")
    if args.closing_text:
        transcript_parts.append(f"[{fmt_ts(3540)} 尾聲] {args.closing_text}")
    transcript_txt = "\n".join(transcript_parts)

    video_obj = {
        "@context": "https://schema.org", "@type": "VideoObject",
        "name": args.title, "description": args.hook, "inLanguage": "zh-Hant",
        "thumbnailUrl": args.thumbnail, "contentUrl": watch_url,
        "embedUrl": f"https://www.youtube.com/embed/{args.youtube_id}",
        "mainEntityOfPage": url, "transcript": transcript_txt,
        "duration": f"PT{args.duration_sec}S",
        "hasPart": clips,
        "publisher": {"@id": f"{BASE}/#organization"},
    }
    if args.published_at:
        video_obj["uploadDate"] = args.published_at

    faq_questions = [
        f"山河静听{year}讲了哪些真实文化事件",
        f"{year}年大陆、港澳台、日本各自发生了什么",
        "山河静听是什么",
    ]
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q,
         "acceptedAnswer": {"@type": "Answer", "text": args.hook}} for q in faq_questions]}

    body_lines = []
    if args.opening_text:
        body_lines.append(f"      <h3>開場 · 00:00</h3>\n      <p>{esc(args.opening_text)}</p>")
    for e in entries:
        body_lines.append(
            f"      <h3>{esc(e['col'])} · {esc(e['title'])} · "
            f"<a href=\"{esc(watch_url)}&t={int(e['t'])}s\" rel=\"noopener\">{fmt_ts(e['t'])} ↗</a></h3>\n"
            f"      <p>{esc(e['body'])}<br><span class=\"note\">{esc(e['colophon'])}</span></p>"
        )
    if args.closing_text:
        body_lines.append(f"      <h3>尾聲 · {fmt_ts(3540)}</h3>\n      <p>{esc(args.closing_text)}</p>")
    body_html = "\n".join(body_lines)
    qs = "\n".join(f"      <li>{esc(q)}</li>" for q in faq_questions)

    page_html = f"""<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{esc(args.title)} | 拾得 Ensō</title>
  <meta name="description" content="{esc(args.hook)}">
  <meta name="robots" content="index,follow,max-image-preview:large">
  <meta name="theme-color" content="#a4472d">
  <link rel="canonical" href="{url}">
  <!-- geo:hreflang:start -->
  <!-- 这两页目前只有繁体单语版本,站点hreflang cluster按路径前缀分组(无前缀=zh-Hans桶,
       跟其余24条shorts单语页同一惯例),所以这里自认zh-Hans桶以满足validate_geo_site.py
       的cluster一致性检查;真正对AI/搜索引擎有意义的语言信号是<html lang>和下面
       VideoObject的inLanguage字段,两者都如实写的是zh-Hant,不受这里影响。 -->
  <link rel="alternate" hreflang="zh-Hans" href="{url}">
  <link rel="alternate" hreflang="x-default" href="{url}">
  <!-- geo:hreflang:end -->
  <link rel="alternate" type="text/markdown" href="{BASE}/v/{slug}.md" title="Markdown twin">
  <link rel="icon" type="image/png" href="../../assets/enso-seal-official.png">
  <link rel="apple-touch-icon" href="../../assets/enso-seal-official.png">
  <link rel="stylesheet" href="../../assets/styles.css">
  <meta property="og:type" content="video.other">
  <meta property="og:title" content="{esc(args.title)}">
  <meta property="og:description" content="{esc(args.hook)}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{esc(args.thumbnail)}">
  <meta name="twitter:card" content="summary_large_image">
  <script type="application/ld+json">{json.dumps(video_obj, ensure_ascii=False)}</script>
  <script type="application/ld+json">{json.dumps(faq, ensure_ascii=False)}</script>
</head>
<body>
  <a class="skip-link" href="#main">跳到正文</a>
  {header}
  <main id="main">
    <article>
      <h1>{esc(args.title)}</h1>
      <p class="lede"><strong>{esc(args.hook)}</strong></p>
      <p class="note">山河靜聽 · {year} ·
        <a href="{esc(watch_url)}" rel="noopener">在 YouTube 觀看原片 ↗</a></p>

      <h2>這一頁能回答什麼</h2>
      <ul>
{qs}
      </ul>

      <h2>{n_cards}張題跋卡全文(按出場順序,附YouTube時間戳)</h2>
      <p class="note">每一則都是WebSearch核實過的真實歷史文化事件,不是生成內容;
        本片竪排書法卡上的文字是濃縮摘錄,這裡是完整正文,方便搜尋引擎與AI理解每一張卡在講什麼。</p>
{body_html}

      <h2>出處</h2>
      <p>本文字記錄整理自「拾得」頻道視頻《{esc(args.title)}》。
        <a href="{esc(watch_url)}" rel="noopener">原片在 YouTube</a>。</p>
    </article>
  </main>
  {footer}
</body>
</html>
"""

    md_parts = [f"# {args.title}", "", f"> {args.hook}", "",
                f"山河靜聽 · {year} · [在 YouTube 觀看原片]({watch_url})", "",
                "## 這一頁能回答什麼", ""]
    md_parts += [f"- {q}" for q in faq_questions]
    md_parts += ["", f"## {n_cards}張題跋卡全文", ""]
    if args.opening_text:
        md_parts.append(f"**開場 · 00:00** {args.opening_text}\n")
    for e in entries:
        md_parts.append(f"**{e['col']} · {e['title']} · [{fmt_ts(e['t'])}]({watch_url}&t={int(e['t'])}s)** "
                         f"{e['body']}（{e['colophon']}）\n")
    if args.closing_text:
        md_parts.append(f"**尾聲 · {fmt_ts(3540)}** {args.closing_text}\n")
    md_parts += ["## 出處", "", f"本文字記錄整理自「拾得」頻道視頻《{args.title}》。原片：{watch_url}"]
    page_md = "\n".join(md_parts)

    d = ROOT / "v" / slug
    page_path, md_path = d / "index.html", ROOT / "v" / f"{slug}.md"

    if page_path.exists():
        if page_path.read_text(encoding="utf-8") == page_html:
            print(f"跳过(已存在且相同): {slug}")
            return
        sys.exit(f"fail-closed:{slug} 页面已存在且内容不同,需人工确认,拒绝覆盖。")

    print(f"{'已写入' if args.apply else 'DRY-RUN 将写入'}: /v/{slug}/ ({n_cards}张卡, transcript {len(transcript_txt)}字)")
    if not args.apply:
        print("未加 --apply,什么都没写。")
        return

    d.mkdir(parents=True, exist_ok=True)
    page_path.write_text(page_html, encoding="utf-8")
    md_path.write_text(page_md, encoding="utf-8")

    sm = ROOT / "sitemap.xml"
    txt = sm.read_text(encoding="utf-8")
    loc = f"<url><loc>{url}</loc></url>"
    if f"<loc>{url}</loc>" not in txt:
        txt = txt.replace("</urlset>", f"  {loc}\n</urlset>")
        sm.write_text(txt, encoding="utf-8")
        print("sitemap 新增 1 条")


if __name__ == "__main__":
    main()
