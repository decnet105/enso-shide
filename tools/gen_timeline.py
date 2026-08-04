#!/usr/bin/env python3
"""公开时间线页生成器（MOAT-4 · L4 引用位 · 2026-08-04）
输入 tools/timeline-curated.json（年→8 条精选·四语·营销红线内），
输出每年 4 locale 页面 + md 孪生 + 时间线 hub + sitemap/llms.txt 增量。
纪律（moat-design-cultural-db.md §L4）：只开精选上层（每年≤8 条），共鸣权重与全库深度私有。
再生成幂等：直接重跑覆盖即可。
"""
import json, os, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = json.load(open(os.path.join(ROOT, "tools", "timeline-curated.json")))
YEARS = sorted(DATA.keys())
TODAY = "2026-08-04"

L = {
  "zh-Hans": dict(
    dirp="", lang="zh-Hans", langname="简体中文",
    nav='<nav aria-label="主导航"><a href="https://shide.app/">首页</a><a href="https://shide.app/features/">功能</a><a href="https://shide.app/privacy/">隐私边界</a><a href="https://shide.app/book-engine/">成书引擎</a><a href="https://shide.app/evidence/">事实证据</a><a href="https://shide.app/faq/">问答</a></nav>',
    skip="跳到正文", eyebrow="华人集体记忆 · 时间线",
    title=lambda y: f"{y}年华人集体记忆时间线：那一年我们在听什么、看什么",
    metad=lambda y: f"{y}年的华人集体记忆精选：那一年的电视剧、电影、歌、游戏与大事——来自拾得文化坐标库的人工核验条目，简繁英日四语。",
    lede=lambda y, n: f"那一年你在哪里？这份时间线从拾得文化坐标库（2400+ 条、简繁英日四语、人工筛核）中精选 {n} 桩 {y} 年的华人集体记忆——影视、音乐、游戏与大事。每一条都可核查，也都可能是你自己故事的入口。",
    secTimeline="那一年的记忆坐标", secFaq="常见问题", secMore="继续阅读", secSources="资料来源",
    monthfmt=lambda m: f"{m}月" if m else "",
    faq=lambda y, titles: [
      (f"{y}年有哪些华人集体记忆？", f"{y}年最常被想起的包括：{titles}。完整年表可在拾得 App 内按年检索。"),
      ("这份时间线的内容从哪来？", "来自拾得文化坐标库——覆盖 1960-2026 年、2400 多条、简繁英日四语的华人文化事件库，按编辑红线人工筛选与核验。本页只收录经核验的精选层。"),
      (f"怎么找回我自己 {y} 年的记忆？", f"拾得（Shide）App 可以按年浏览这些文化坐标、在触动你的事件上盖印、写下你的那一段，并整理成中英对照的纪念册。记录免费、无需注册、内容留在你自己的设备上。"),
    ],
    moreCards=[("https://shide.app/answers/chinese-family-memory/", "把家人的故事留下来", "为什么华人家庭的记忆值得认真保存，以及怎么开始。"),
               ("https://shide.app/answers/is-shide-legit/", "拾得靠不靠谱？", "它是什么、谁做的、数据怎么处理——一份可核查的说明。")],
    sources="条目来自拾得文化坐标库（人工核验·标注来源）；年份、片名、曲目等公共事实可对照公开资料核查。",
    hubTitle="华人集体记忆时间线", hubMetad="按年份浏览华人集体记忆：每年精选那一年的电视剧、电影、歌、游戏与大事，简繁英日四语，人工核验。",
    hubLede="一年一页，每页精选那一年的华人集体记忆。从这里选一年开始——",
    hubEntry=lambda y: f"{y}年 · 那一年我们在听什么、看什么",
    footer1="公开说明以已落地代码为准；条目按编辑红线人工筛核。", footermd="阅读本页 Markdown", factdate="事实核验日期",
    cat={"tv": "电视", "film": "电影", "music": "音乐", "game": "游戏", "anime": "动漫", "variety": "综艺", "sports": "体育", "event": "大事", "tech": "科技"},
    tkey="title_zh_hans", ckey="creator_zh_hans", bkey="blurb_zh_hans"),
  "zh-Hant": dict(
    dirp="zh-Hant/", lang="zh-Hant", langname="繁體中文",
    nav='<nav aria-label="主導航"><a href="https://shide.app/zh-Hant/">首頁</a><a href="https://shide.app/zh-Hant/features/">功能</a><a href="https://shide.app/zh-Hant/privacy/">隱私邊界</a><a href="https://shide.app/zh-Hant/book-engine/">成書引擎</a><a href="https://shide.app/zh-Hant/evidence/">事實證據</a><a href="https://shide.app/zh-Hant/faq/">問答</a></nav>',
    skip="跳到正文", eyebrow="華人集體記憶 · 時間線",
    title=lambda y: f"{y}年華人集體記憶時間線：那一年我們在聽什麼、看什麼",
    metad=lambda y: f"{y}年的華人集體記憶精選：那一年的電視劇、電影、歌、遊戲與大事——來自拾得文化座標庫的人工核驗條目，簡繁英日四語。",
    lede=lambda y, n: f"那一年你在哪裡？這份時間線從拾得文化座標庫（2400+ 條、簡繁英日四語、人工篩核）中精選 {n} 樁 {y} 年的華人集體記憶——影視、音樂、遊戲與大事。每一條都可核查，也都可能是你自己故事的入口。",
    secTimeline="那一年的記憶座標", secFaq="常見問題", secMore="繼續閱讀", secSources="資料來源",
    monthfmt=lambda m: f"{m}月" if m else "",
    faq=lambda y, titles: [
      (f"{y}年有哪些華人集體記憶？", f"{y}年最常被想起的包括：{titles}。完整年表可在拾得 App 內按年檢索。"),
      ("這份時間線的內容從哪來？", "來自拾得文化座標庫——覆蓋 1960-2026 年、2400 多條、簡繁英日四語的華人文化事件庫，按編輯紅線人工篩選與核驗。本頁只收錄經核驗的精選層。"),
      (f"怎麼找回我自己 {y} 年的記憶？", "拾得（Shide）App 可以按年瀏覽這些文化座標、在觸動你的事件上蓋印、寫下你的那一段，並整理成中英對照的紀念冊。記錄免費、無需註冊、內容留在你自己的裝置上。"),
    ],
    moreCards=[("https://shide.app/zh-Hant/answers/chinese-family-memory/", "把家人的故事留下來", "為什麼華人家庭的記憶值得認真保存，以及怎麼開始。"),
               ("https://shide.app/zh-Hant/answers/is-shide-legit/", "拾得靠不靠譜？", "它是什麼、誰做的、資料怎麼處理——一份可核查的說明。")],
    sources="條目來自拾得文化座標庫（人工核驗·標註來源）；年份、片名、曲目等公共事實可對照公開資料核查。",
    hubTitle="華人集體記憶時間線", hubMetad="按年份瀏覽華人集體記憶：每年精選那一年的電視劇、電影、歌、遊戲與大事，簡繁英日四語，人工核驗。",
    hubLede="一年一頁，每頁精選那一年的華人集體記憶。從這裡選一年開始——",
    hubEntry=lambda y: f"{y}年 · 那一年我們在聽什麼、看什麼",
    footer1="公開說明以已落地程式碼為準；條目按編輯紅線人工篩核。", footermd="閱讀本頁 Markdown", factdate="事實核驗日期",
    cat={"tv": "電視", "film": "電影", "music": "音樂", "game": "遊戲", "anime": "動漫", "variety": "綜藝", "sports": "體育", "event": "大事", "tech": "科技"},
    tkey="title_zh_hant", ckey="creator_zh_hant", bkey="blurb_zh_hant"),
  "en": dict(
    dirp="en/", lang="en", langname="English",
    nav='<nav aria-label="Main navigation"><a href="https://shide.app/en/">Home</a><a href="https://shide.app/en/features/">Features</a><a href="https://shide.app/en/privacy/">Privacy boundaries</a><a href="https://shide.app/en/book-engine/">Book engine</a><a href="https://shide.app/en/evidence/">Evidence</a><a href="https://shide.app/en/faq/">FAQ</a></nav>',
    skip="Skip to content", eyebrow="Chinese collective memory · Timeline",
    title=lambda y: f"Chinese Cultural Memory Timeline, {y}: what we watched, played and sang",
    metad=lambda y: f"A curated timeline of Chinese collective memory in {y}: the TV shows, films, songs, games and events of that year — human-verified entries from the Shide cultural database, in four languages.",
    lede=lambda y, n: f"Where were you that year? This timeline hand-picks {n} touchstones of Chinese collective memory from {y} — TV, film, music, games and events — drawn from the Shide cultural database (2,400+ entries in Simplified/Traditional Chinese, English and Japanese, human-curated). Every entry is checkable, and any of them might be a doorway into your own story.",
    secTimeline="Memory landmarks of the year", secFaq="FAQ", secMore="Keep reading", secSources="Sources",
    monthfmt=lambda m: {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}.get(m,"") if m else "",
    faq=lambda y, titles: [
      (f"What are the touchstones of Chinese collective memory in {y}?", f"The most-remembered include: {titles}. The full year index is browsable inside the Shide app."),
      ("Where does this timeline come from?", "From the Shide cultural database — 2,400+ entries covering 1960-2026 in four languages, hand-curated and verified under an editorial policy. This page publishes only the verified, curated layer."),
      (f"How do I recover my own memories of {y}?", "The Shide (拾得) app lets you browse these cultural landmarks by year, stamp the ones that move you, write your own piece of the story, and shape it into a bilingual keepsake book. Recording is free, no account needed, and your content stays on your device."),
    ],
    moreCards=[("https://shide.app/en/answers/chinese-family-memory/", "Preserving your family's stories", "Why Chinese family memories deserve deliberate keeping, and how to start."),
               ("https://shide.app/en/answers/is-shide-legit/", "Is Shide legit?", "What it is, who makes it, and how your data is handled — a checkable explanation.")],
    sources="Entries come from the Shide cultural database (human-verified, with sources); public facts such as years, titles and songs can be checked against public records.",
    hubTitle="Chinese Cultural Memory Timelines", hubMetad="Browse Chinese collective memory by year: each page curates the TV, films, songs, games and events of one year, in four languages, human-verified.",
    hubLede="One year per page, each a curated set of Chinese collective memories. Pick a year to begin —",
    hubEntry=lambda y: f"{y} · what we watched, played and sang",
    footer1="Public claims reflect shipped code; entries are hand-curated under an editorial policy.", footermd="Read this page as Markdown", factdate="Facts verified",
    cat={"tv": "TV", "film": "Film", "music": "Music", "game": "Games", "anime": "Anime", "variety": "Variety", "sports": "Sports", "event": "Events", "tech": "Tech"},
    tkey="title_en", ckey="creator_en", bkey="blurb_en"),
  "ja": dict(
    dirp="ja/", lang="ja", langname="日本語",
    nav='<nav aria-label="メインナビゲーション"><a href="https://shide.app/ja/">ホーム</a><a href="https://shide.app/ja/features/">機能</a><a href="https://shide.app/ja/privacy/">プライバシー</a><a href="https://shide.app/ja/book-engine/">製本エンジン</a><a href="https://shide.app/ja/evidence/">エビデンス</a><a href="https://shide.app/ja/faq/">FAQ</a></nav>',
    skip="本文へ", eyebrow="華人の集合的記憶 · タイムライン",
    title=lambda y: f"{y}年 華人集合的記憶タイムライン：あの年、何を観て何を聴いていたか",
    metad=lambda y: f"{y}年の華人集合的記憶を厳選：あの年のドラマ・映画・歌・ゲーム・出来事——拾得文化データベースの人手検証済みエントリー、4言語対応。",
    lede=lambda y, n: f"あの年、あなたはどこにいましたか。このタイムラインは、拾得文化データベース（2,400以上・簡体字/繁体字/英語/日本語・人手選定）から {y} 年の華人集合的記憶 {n} 件を厳選——ドラマ、映画、音楽、ゲーム、出来事。どれも検証可能で、あなた自身の物語への入り口になるかもしれません。",
    secTimeline="あの年の記憶の座標", secFaq="よくある質問", secMore="続けて読む", secSources="出典",
    monthfmt=lambda m: f"{m}月" if m else "",
    faq=lambda y, titles: [
      (f"{y}年の華人集合的記憶には何がありますか？", f"よく思い出されるものには {titles} などがあります。完全な年表は拾得アプリ内で年ごとに閲覧できます。"),
      ("このタイムラインの出典は？", "拾得文化データベースです——1960-2026年をカバーする2,400以上のエントリーを4言語で収録し、編集ポリシーに基づいて人手で選定・検証しています。本ページは検証済みの厳選層のみ公開しています。"),
      (f"自分の {y} 年の記憶を取り戻すには？", "拾得（Shide）アプリでは、これらの文化座標を年ごとにたどり、心が動いた出来事に印を押し、自分の物語を書き添えて、二言語の記念本にまとめられます。記録は無料、アカウント不要、内容は端末内に残ります。"),
    ],
    moreCards=[("https://shide.app/ja/answers/chinese-family-memory/", "家族の物語を残す", "家族の記憶を丁寧に残す意味と、その始め方。"),
               ("https://shide.app/ja/answers/is-shide-legit/", "拾得は信頼できる？", "何のアプリで、誰が作り、データをどう扱うか——検証可能な説明。")],
    sources="エントリーは拾得文化データベース（人手検証・出典付き）由来です。年・作品名・楽曲名などの公的事実は公開資料と照合できます。",
    hubTitle="華人集合的記憶タイムライン", hubMetad="年ごとに華人の集合的記憶をたどる：各ページがその年のドラマ・映画・歌・ゲーム・出来事を厳選。4言語・人手検証。",
    hubLede="1年1ページ。それぞれがその年の華人集合的記憶の厳選集です。まず1年を選んでください——",
    hubEntry=lambda y: f"{y}年 · あの年、何を観て何を聴いていたか",
    footer1="公開情報は実装済みコードに基づきます。エントリーは編集ポリシーに基づく人手選定です。", footermd="このページをMarkdownで読む", factdate="事実確認日",
    cat={"tv": "テレビ", "film": "映画", "music": "音楽", "game": "ゲーム", "anime": "アニメ", "variety": "バラエティ", "sports": "スポーツ", "event": "出来事", "tech": "テック"},
    tkey="title_ja", ckey="creator_ja", bkey="blurb_ja"),
}

ORDER = ["zh-Hans", "zh-Hant", "en", "ja"]
esc = html.escape

def field(e, key, fallback_key):
    v = (e.get(key) or "").strip()
    return v if v else (e.get(fallback_key) or "").strip()

def switcher(loc, path):
    parts = []
    for k in ORDER:
        url = f"https://shide.app/{L[k]['dirp']}{path}"
        if k == loc:
            parts.append(f'<strong class="language-link" aria-current="true">{L[k]["langname"]}</strong>')
        else:
            parts.append(f'<a class="language-link" href="{url}" hreflang="{L[k]["lang"]}">{L[k]["langname"]}</a>')
    return '<span class="language-switch">' + " · ".join(parts) + "</span>"

def catof(e):
    c = e["category"]
    return "event" if c not in ("tv", "film", "music", "game", "anime", "variety", "sports", "tech") else c

def page_html(loc, year, entries):
    T = L[loc]
    path = f"timeline/{year}/"
    url = f"https://shide.app/{T['dirp']}{path}"
    mdurl = f"https://shide.app/{T['dirp']}timeline/{year}.md"
    title = T["title"](year)
    metad = T["metad"](year)
    items_html, list_elems, names = [], [], []
    for i, e in enumerate(entries):
        t = field(e, T["tkey"], "title_zh_hans")
        c = field(e, T["ckey"], "creator_zh_hans")
        b = field(e, T["bkey"], "blurb_zh_hans")
        m = T["monthfmt"](e.get("month"))
        tag = T["cat"].get(catof(e), "")
        names.append(t)
        head = esc(t) + (f'<span class="muted">（{esc(c)}）</span>' if c and loc in ("zh-Hans", "zh-Hant") else (f'<span class="muted"> — {esc(c)}</span>' if c else ""))
        meta = " · ".join(x for x in (tag, m) if x)
        items_html.append(f"<li><strong>{head}</strong><br><span class=\"muted\">{esc(meta)}</span><br>{esc(b)}</li>")
        list_elems.append({"@type": "ListItem", "position": i + 1, "name": t + (f"（{c}）" if c else "")})
    titles_join = ("、" if loc != "en" else ", ").join(names[:5])
    faqs = T["faq"](year, titles_join)
    schema_article = json.dumps({"@context": "https://schema.org", "@type": "Article", "headline": title,
                                 "description": metad, "inLanguage": T["lang"], "mainEntityOfPage": url,
                                 "dateModified": TODAY}, ensure_ascii=False)
    schema_list = json.dumps({"@context": "https://schema.org", "@type": "ItemList", "name": title,
                              "numberOfItems": len(entries), "itemListElement": list_elems}, ensure_ascii=False)
    schema_faq = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]},
        ensure_ascii=False)
    other_years = [y for y in YEARS if y != year]
    year_links = " · ".join(f'<a href="https://shide.app/{T["dirp"]}timeline/{y}/">{y}</a>' for y in other_years)
    hub_link = f'<a href="https://shide.app/{T["dirp"]}timeline/">{esc(T["hubTitle"])}</a>'
    faq_html = "".join(f"<dt>{esc(q)}</dt><dd>{esc(a)}</dd>" for q, a in faqs)
    more_html = "".join(f'<a class="text-card" href="{u}"><strong>{esc(a)}</strong><span>{esc(b)}</span></a>'
                        for u, a, b in T["moreCards"])
    return f"""<!doctype html>
<html lang="{T['lang']}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{esc(title)} | 拾得 Ensō</title>
  <meta name="description" content="{esc(metad)}">
  <meta name="robots" content="index,follow,max-image-preview:large">
  <meta name="theme-color" content="#a4472d">
  <link rel="canonical" href="{url}">
  <link rel="alternate" type="text/markdown" href="{mdurl}" title="Markdown twin">
  <link rel="icon" type="image/png" href="https://shide.app/assets/app-icon.png">
  <link rel="apple-touch-icon" href="https://shide.app/assets/app-icon.png">
  <link rel="stylesheet" href="https://shide.app/assets/styles.css">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(metad)}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="https://shide.app/assets/app-icon.png">
  <meta name="twitter:card" content="summary">
  <script type="application/ld+json">{schema_article}</script>
  <script type="application/ld+json">{schema_list}</script>
  <script type="application/ld+json">{schema_faq}</script>
</head>
<body>
  <a class="skip-link" href="#main">{esc(T['skip'])}</a>
  <header class="site-header">
    <a class="brand" href="https://shide.app/{T['dirp']}">拾得 Ensō</a>
    {T['nav']}
  {switcher(loc, path)}</header>
  <main id="main"><p class="eyebrow">{esc(T['eyebrow'])}</p><h1>{esc(title)}</h1><p class="lede">{esc(T['lede'](year, len(entries)))}</p>
  <section><h2>{esc(T['secTimeline'])}</h2><ol class="timeline-list">{''.join(items_html)}</ol></section>
  <section><h2>{esc(T['secFaq'])}</h2><dl>{faq_html}</dl></section>
  <section><h2>{esc(T['secMore'])}</h2><p>{hub_link} · {year_links}</p><div class="card-grid">{more_html}</div></section>
  <section class="sources"><h2>{esc(T['secSources'])}</h2><p>{esc(T['sources'])}</p></section></main>
  <footer>
    <p>{esc(T['footer1'])}</p>
    <p><a href="{mdurl}">{esc(T['footermd'])}</a> · {esc(T['factdate'])} {TODAY}</p>
  </footer>
</body>
</html>
"""

def page_md(loc, year, entries):
    T = L[loc]
    lines = [f"# {T['title'](year)}", "", T["lede"](year, len(entries)), "", f"## {T['secTimeline']}", ""]
    for e in entries:
        t = field(e, T["tkey"], "title_zh_hans")
        c = field(e, T["ckey"], "creator_zh_hans")
        b = field(e, T["bkey"], "blurb_zh_hans")
        m = T["monthfmt"](e.get("month"))
        tag = T["cat"].get(catof(e), "")
        meta = " · ".join(x for x in (tag, m) if x)
        lines.append(f"- **{t}**{'（' + c + '）' if c else ''}（{meta}）：{b}")
    lines += ["", f"## {T['secFaq']}", ""]
    names = [field(e, T["tkey"], "title_zh_hans") for e in entries]
    for q, a in T["faq"](year, ("、" if loc != "en" else ", ").join(names[:5])):
        lines += [f"### {q}", "", a, ""]
    lines += [f"_{T['factdate']} {TODAY}_", ""]
    return "\n".join(lines)

def hub_html(loc):
    T = L[loc]
    path = "timeline/"
    url = f"https://shide.app/{T['dirp']}{path}"
    cards = "".join(
        f'<a class="text-card" href="https://shide.app/{T["dirp"]}timeline/{y}/"><strong>{esc(T["hubEntry"](y))}</strong>'
        f'<span>{esc(T["metad"](y))}</span></a>' for y in YEARS)
    schema = json.dumps({"@context": "https://schema.org", "@type": "CollectionPage", "name": T["hubTitle"],
                         "description": T["hubMetad"], "inLanguage": T["lang"], "mainEntityOfPage": url,
                         "dateModified": TODAY}, ensure_ascii=False)
    return f"""<!doctype html>
<html lang="{T['lang']}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{esc(T['hubTitle'])} | 拾得 Ensō</title>
  <meta name="description" content="{esc(T['hubMetad'])}">
  <meta name="robots" content="index,follow,max-image-preview:large">
  <meta name="theme-color" content="#a4472d">
  <link rel="canonical" href="{url}">
  <link rel="icon" type="image/png" href="https://shide.app/assets/app-icon.png">
  <link rel="stylesheet" href="https://shide.app/assets/styles.css">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{esc(T['hubTitle'])}">
  <meta property="og:description" content="{esc(T['hubMetad'])}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="https://shide.app/assets/app-icon.png">
  <script type="application/ld+json">{schema}</script>
</head>
<body>
  <a class="skip-link" href="#main">{esc(T['skip'])}</a>
  <header class="site-header">
    <a class="brand" href="https://shide.app/{T['dirp']}">拾得 Ensō</a>
    {T['nav']}
  {switcher(loc, path)}</header>
  <main id="main"><p class="eyebrow">{esc(T['eyebrow'])}</p><h1>{esc(T['hubTitle'])}</h1><p class="lede">{esc(T['hubLede'])}</p>
  <section><div class="card-grid">{cards}</div></section></main>
  <footer><p>{esc(T['footer1'])}</p><p>{esc(T['factdate'])} {TODAY}</p></footer>
</body>
</html>
"""

written = []
for loc in ORDER:
    base = os.path.join(ROOT, L[loc]["dirp"].rstrip("/")) if L[loc]["dirp"] else ROOT
    tdir = os.path.join(base, "timeline")
    os.makedirs(tdir, exist_ok=True)
    open(os.path.join(tdir, "index.html"), "w").write(hub_html(loc))
    written.append(f"{L[loc]['dirp']}timeline/")
    for y in YEARS:
        ydir = os.path.join(tdir, y)
        os.makedirs(ydir, exist_ok=True)
        open(os.path.join(ydir, "index.html"), "w").write(page_html(loc, y, DATA[y]))
        open(os.path.join(tdir, f"{y}.md"), "w").write(page_md(loc, y, DATA[y]))
        written.append(f"{L[loc]['dirp']}timeline/{y}/")

# sitemap 增量（幂等）
sm_path = os.path.join(ROOT, "sitemap.xml")
sm = open(sm_path).read()
adds = []
for w in written:
    u = f"https://shide.app/{w}"
    if u not in sm:
        adds.append(f"  <url><loc>{u}</loc></url>\n")
if adds:
    sm = sm.replace("</urlset>", "".join(adds) + "</urlset>")
    open(sm_path, "w").write(sm)

# llms.txt 增量（幂等）
llms_path = os.path.join(ROOT, "llms.txt")
lt = open(llms_path).read()
if "timeline/1998.md" not in lt:
    block = ("\n## Timelines（华人集体记忆时间线）\n\n" + "".join(
        f"- [{y}年华人集体记忆时间线](https://shide.app/timeline/{y}.md): 那一年的电视剧、电影、歌、游戏与大事——拾得文化坐标库人工核验精选，四语可读。\n"
        for y in YEARS))
    lt = lt.replace("\n## Verification", block + "\n## Verification")
    open(llms_path, "w").write(lt)

print(f"generated {len(written)} pages, sitemap +{len(adds)}")
