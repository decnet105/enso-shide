#!/usr/bin/env python3
"""Safe additive page-adder for Batch 2A (two new AEO landing pages × 4 locales).

This is NOT the legacy generator: it never rmtrees, never regenerates the whole
site, and only writes the specific new files for the two Batch 2A slugs. It is
idempotent (re-running produces identical bytes), guarded (refuses to overwrite
a DIFFERING existing file unless --force), fail-closed, and stdlib-only. Sitemap
entries are appended only if missing. Prints created / unchanged / skipped.

New pages are emitted already-correct (self canonical, full reciprocal hreflang
cluster, md twin, WebPage + FAQPage JSON-LD), so no metadata patch pass is
needed for them; validate afterwards with tools/validate_geo_site.py.

Usage:  python3 tools/add_batch2a_pages.py [--force]
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://shide.app"
STORE = "https://apps.apple.com/app/apple-store/id6787128369?pt=129013055&ct=web&mt=8"
DATE = "2026-08-19"
LOCALES = ("zh-Hans", "zh-Hant", "en", "ja")          # display order for switch/hreflang
PREFIX = {"zh-Hans": "", "zh-Hant": "zh-Hant/", "en": "en/", "ja": "ja/"}


def esc_text(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def esc_attr(s: str) -> str:
    return esc_text(s).replace('"', "&quot;").replace("'", "&#x27;")


def page_url(locale: str, logical: str) -> str:
    return f"{BASE}/{PREFIX[locale]}{logical}/"


def md_url(locale: str, logical: str) -> str:
    return f"{BASE}/{PREFIX[locale]}{logical}.md"


# --------------------------------------------------------------------------- #
# Fixed per-locale chrome (verbatim from deployed features/ pages, 2026-08-19) #
# --------------------------------------------------------------------------- #
CHROME = {
    "zh-Hans": {
        "ld_lang": "zh-Hans", "skip": "跳到正文", "brand_href": f"{BASE}/",
        "nav_label": "主导航", "lang_label": "简体中文",
        "nav": [(f"{BASE}/", "首页"), (f"{BASE}/features/", "功能"),
                (f"{BASE}/privacy/", "隐私边界"), (f"{BASE}/book-engine/", "成书引擎"),
                (f"{BASE}/evidence/", "事实证据"), (f"{BASE}/faq/", "问答")],
        "store": "在 App Store 下载拾得", "follow": "关注：",
        "disclosure": "公开说明以已落地代码为准；愿景、实验功能与已上线能力分开标注。",
        "read_md": "阅读本页 Markdown", "factchecked": f"事实核验日期 {DATE}",
        "keep_reading": "继续阅读", "home_alt": "拾得首页",
    },
    "zh-Hant": {
        "ld_lang": "zh-Hant", "skip": "跳到正文", "brand_href": f"{BASE}/zh-Hant/",
        "nav_label": "主導航", "lang_label": "繁體中文",
        "nav": [(f"{BASE}/zh-Hant/", "首頁"), (f"{BASE}/zh-Hant/features/", "功能"),
                (f"{BASE}/zh-Hant/privacy/", "隱私邊界"), (f"{BASE}/zh-Hant/book-engine/", "成書引擎"),
                (f"{BASE}/zh-Hant/evidence/", "事實證據"), (f"{BASE}/zh-Hant/faq/", "問答")],
        "store": "在 App Store 下載拾得", "follow": "關注：",
        "disclosure": "公開說明以已落地程式碼為準；願景、實驗功能與已上線能力分開標註。",
        "read_md": "閱讀本頁 Markdown", "factchecked": f"事實核驗日期 {DATE}",
        "keep_reading": "繼續閱讀", "home_alt": "拾得首頁",
    },
    "en": {
        "ld_lang": "en", "skip": "Skip to content", "brand_href": f"{BASE}/",
        "nav_label": "Main navigation", "lang_label": "English",
        "nav": [(f"{BASE}/en/", "Home"), (f"{BASE}/en/features/", "Features"),
                (f"{BASE}/en/privacy/", "Privacy boundaries"), (f"{BASE}/en/book-engine/", "Book engine"),
                (f"{BASE}/en/evidence/", "Evidence"), (f"{BASE}/en/faq/", "FAQ")],
        "store": "Download Shide on the App Store", "follow": "Follow: ",
        "disclosure": "Public statements reflect shipped code; vision, experimental features, and released capabilities are labeled separately.",
        "read_md": "Read this page in Markdown", "factchecked": f"Fact-checked {DATE}",
        "keep_reading": "Keep reading", "home_alt": "Shide home screen",
    },
    "ja": {
        "ld_lang": "ja", "skip": "本文へスキップ", "brand_href": f"{BASE}/",
        "nav_label": "メインナビゲーション", "lang_label": "日本語",
        "nav": [(f"{BASE}/ja/", "ホーム"), (f"{BASE}/ja/features/", "機能"),
                (f"{BASE}/ja/privacy/", "プライバシー"), (f"{BASE}/ja/book-engine/", "製本エンジン"),
                (f"{BASE}/ja/evidence/", "エビデンス"), (f"{BASE}/ja/faq/", "FAQ")],
        "store": "App Store で拾得をダウンロード", "follow": "フォロー：",
        "disclosure": "公開している記述は出荷済みのコードを反映しています。ビジョン・実験的機能・リリース済み機能は、それぞれ区別して表示します。",
        "read_md": "このページを Markdown で読む", "factchecked": f"事実確認日 {DATE}",
        "keep_reading": "関連ページ", "home_alt": "拾得のホーム画面",
    },
}


# --------------------------------------------------------------------------- #
# Content (approved copy + the 7 review edits baked in)                         #
#   section = {"h2", "p":[...], "ul":[...]?, "table":{head,rows}?, "callout"?}  #
#   faq     = [(question, answer), ...]                                         #
#   cards   = [(href, strong, span), ...]                                       #
# --------------------------------------------------------------------------- #
PAGES: dict[str, dict[str, dict]] = {
    "record-your-life-as-it-happens": {
        "zh-Hans": {
            "title": "在生活发生时记录它 — 一个本地优先的私人生命档案",
            "desc": "给华语家庭的生命档案：在事件、地点、年度信物、反思发生时随手留住，本地优先、免注册，再整理成中英对照的岁月书。不是日记，也不是回忆录代做服务。",
            "eyebrow": "生命档案", "shot": True,
            "h1": "别等多年后再回忆这一生，在它发生的时候就留住",
            "lede": "拾得是一个「生命档案」——一个 iPhone App，在生活发生时就把重要的事件、地点、年度信物和反思留住。核心档案本地优先，核心记录与本机成书都不需要账户；在线 AI 是可选的 Ensō+。当你准备好，拾得可以把你留下的内容整理成一本数字岁月书，支持中英对照。它不是每天打卡的日记，也不是一套采访别人过去、替你做书的服务。",
            "sections": [
                {"h2": "什么是生命档案", "p": ["生命档案，是在生活发生时就留下的一份人生记录——不是多年以后回头写的回忆录，也不是必须每天填满的日记。你把值得的东西留下来：一件事、一个地方、一件信物、一段心里的话，它们随时间积累，慢慢成为你这一生的档案。"]},
                {"h2": "不是日记，也不是采访成书服务", "p": ["很多日记工具围绕按日记录来组织内容；生命档案不要求日更，有意义的事情发生时再留下就可以。采访成书服务又是另一回事——它采访某个人（通常是父母）、把他的过去做成一本书。拾得两者都不是。它是你自己用的 App，在你的人生展开时，把它留住。"]},
                {"h2": "拾得怎么留住一生", "p": ["拾得按人真正在过的方式来组织回忆——按事件、按地点、按年份——而不是一条条按日期排的流水。"],
                 "ul": ["事件与反思——用你自己的话，记下发生了什么、心里怎么想。", "地点——一生是有地理的，拾得留住这些事发生在哪。", "年度信物——用很少的几件东西，代表每一年。", "那年今日——早些年的今天，你留下过什么。"]},
                {"h2": "本地优先，私密", "p": ["核心档案本地优先：你的回忆存在自己的 iPhone 里，记录与成书都不需要账户。在线 AI 是可选的 Ensō+ 能力，只在你主动触发时才用。"]},
                {"h2": "准备好时，一本中英岁月书", "p": ["当你准备好，拾得可以把你留下的内容整理成一本数字岁月书，支持中英对照——你为自己建立的档案，下一代也读得懂。"]},
            ],
            "faq": [
                ("什么是生命档案？", "在生活发生时就留下的人生记录——事件、地点、年度信物、反思——而不是回头写的回忆录或每天打卡的日记。"),
                ("生命档案和日记有什么不同？", "日记通常按日期连续记录；生命档案不要求日更，让你在有意义的时刻随手留住，按事件、地点、年份组织。"),
                ("不每天写日记，也能记录自己的一生吗？", "可以。拾得就是为「有意义时才记」设计的，不要求每日打卡。"),
                ("拾得是采访成书服务吗？", "不是。采访成书服务采访某人（常是父母）、把他的过去做成书；拾得是你自己用的 App，把自己正在发生的一生留住。"),
                ("我的数据存在哪？", "核心档案本地优先：回忆存在自己的 iPhone 里，记录与成书都不需要账户。在线 AI 是可选的 Ensō+。"),
            ],
            "cards": [
                (f"{BASE}/memory-app-vs-storytelling-service/", "记忆 App 还是采访成书服务", "你到底需要哪个——一个留住你自己一生的 App，还是一套采访父母过去的服务？"),
                (f"{BASE}/features/", "拾得当前实现了什么", "从端上记忆模型、文化坐标、足迹地图到本机成书，逐项可核验。"),
                (f"{BASE}/privacy/", "隐私边界", "本机数据、可选联网功能，以及什么会离开设备。"),
            ],
        },
        "zh-Hant": {
            "title": "在生活發生時記錄它 — 一個本地優先的私人生命檔案",
            "desc": "給華語家庭的生命檔案：在事件、地點、年度信物、反思發生時隨手留住，本地優先、免註冊，再整理成中英對照的歲月書。不是日記，也不是回憶錄代做服務。",
            "eyebrow": "生命檔案", "shot": True,
            "h1": "別等多年後再回憶這一生，在它發生的時候就留住",
            "lede": "拾得是一個「生命檔案」——一個 iPhone App，在生活發生時就把重要的事件、地點、年度信物和反思留住。核心檔案本地優先，核心記錄與本機成書都不需要帳戶；線上 AI 是可選的 Ensō+。當你準備好，拾得可以把你留下的內容整理成一本數位歲月書，支援中英對照。它不是每天打卡的日記，也不是一套採訪別人過去、替你做書的服務。",
            "sections": [
                {"h2": "什麼是生命檔案", "p": ["生命檔案，是在生活發生時就留下的一份人生記錄——不是多年以後回頭寫的回憶錄，也不是必須每天填滿的日記。你把值得的東西留下來：一件事、一個地方、一件信物、一段心裡的話，它們隨時間積累，慢慢成為你這一生的檔案。"]},
                {"h2": "不是日記，也不是採訪成書服務", "p": ["很多日記工具圍繞按日記錄來組織內容；生命檔案不要求日更，有意義的事情發生時再留下就可以。採訪成書服務又是另一回事——它採訪某個人（通常是父母）、把他的過去做成一本書。拾得兩者都不是。它是你自己用的 App，在你的人生展開時，把它留住。"]},
                {"h2": "拾得怎麼留住一生", "p": ["拾得按人真正在過的方式來組織回憶——按事件、按地點、按年份——而不是一條條按日期排的流水。"],
                 "ul": ["事件與反思——用你自己的話，記下發生了什麼、心裡怎麼想。", "地點——一生是有地理的，拾得留住這些事發生在哪。", "年度信物——用很少的幾件東西，代表每一年。", "那年今日——早些年的今天，你留下過什麼。"]},
                {"h2": "本地優先，私密", "p": ["核心檔案本地優先：你的回憶存在自己的 iPhone 裡，記錄與成書都不需要帳戶。線上 AI 是可選的 Ensō+ 能力，只在你主動觸發時才用。"]},
                {"h2": "準備好時，一本中英歲月書", "p": ["當你準備好，拾得可以把你留下的內容整理成一本數位歲月書，支援中英對照——你為自己建立的檔案，下一代也讀得懂。"]},
            ],
            "faq": [
                ("什麼是生命檔案？", "在生活發生時就留下的人生記錄——事件、地點、年度信物、反思——而不是回頭寫的回憶錄或每天打卡的日記。"),
                ("生命檔案和日記有什麼不同？", "日記通常按日期連續記錄；生命檔案不要求日更，讓你在有意義的時刻隨手留住，按事件、地點、年份組織。"),
                ("不每天寫日記，也能記錄自己的一生嗎？", "可以。拾得就是為「有意義時才記」設計的，不要求每日打卡。"),
                ("拾得是採訪成書服務嗎？", "不是。採訪成書服務採訪某人（常是父母）、把他的過去做成書；拾得是你自己用的 App，把自己正在發生的一生留住。"),
                ("我的資料存在哪？", "核心檔案本地優先：回憶存在自己的 iPhone 裡，記錄與成書都不需要帳戶。線上 AI 是可選的 Ensō+。"),
            ],
            "cards": [
                (f"{BASE}/zh-Hant/memory-app-vs-storytelling-service/", "記憶 App 還是採訪成書服務", "你到底需要哪個——一個留住你自己一生的 App，還是一套採訪父母過去的服務？"),
                (f"{BASE}/zh-Hant/features/", "拾得當前實現了什麼", "從端上記憶模型、文化座標、足跡地圖到本機成書，逐項可核驗。"),
                (f"{BASE}/zh-Hant/privacy/", "隱私邊界", "本機資料、可選聯網功能，以及什麼會離開設備。"),
            ],
        },
        "en": {
            "title": "Record your life as it happens — a private, local-first living archive",
            "desc": "A living archive for Chinese-speaking families: keep events, places, annual keepsakes and reflections as they happen, on-device and private, then organize them into a bilingual Life Book. Not a diary, not a memoir service.",
            "eyebrow": "Living archive", "shot": True,
            "h1": "Don't wait years to look back on your life — keep it as it happens",
            "lede": "Shide is a living archive — an iPhone app for keeping your life as it happens: important events, places, annual keepsakes and reflections. Its core archive is local-first, and no account is required for core recording and book-making; online AI is optional through Ensō+. When you're ready, Shide can organize what you've kept into a digital Life Book, with Chinese and English support. It is not a daily diary, and not a service built around interviewing someone about their past.",
            "sections": [
                {"h2": "What a living archive is", "p": ["A living archive is a running record of your life kept as it happens, rather than a retrospective memoir written years later or a diary you must fill in every day. You capture what matters — an event, a place, a keepsake, a reflection — and it accumulates over time into an archive of your own life."]},
                {"h2": "Not a diary, not a memoir service", "p": ["Many journals are organized around daily entries. A living archive does not require a daily cadence — you add something when it is meaningful enough to keep. A storytelling or memoir service is different again — it interviews someone, usually a parent, about their past and produces a book of it. Shide is neither. It is an app you use yourself, to keep your own life as it unfolds."]},
                {"h2": "How Shide keeps a life", "p": ["Shide organizes memories the way a life is actually lived — by event, by place, and by year — instead of as a stream of dated entries."],
                 "ul": ["Events and reflections — capture what happened and how it felt, in your own words.", "Places — a life has a geography; Shide keeps where things happened.", "Annual keepsakes — a small set of objects that stand for each year.", "On this day — what you kept on this date in earlier years."]},
                {"h2": "Local-first and private", "p": ["Its core archive is local-first: your memories live on your iPhone, and no account is required to record them or to make a book. Online AI is an optional Ensō+ capability, used only when you actively invoke it."]},
                {"h2": "A bilingual Life Book, when you're ready", "p": ["When you're ready, Shide can organize what you've kept into a digital Life Book, with Chinese and English support — so the archive you build for yourself can also be read by the next generation."]},
            ],
            "faq": [
                ("What is a living archive?", "A running record of your life kept as it happens — events, places, annual keepsakes and reflections — rather than a retrospective memoir or a daily diary."),
                ("How is a life archive different from a journal?", "Journals are usually organized around continuous daily entries; a living archive does not require a daily cadence, letting you capture meaningful moments over time, organized by event, place and year."),
                ("Can I record my life without journaling every day?", "Yes. Shide is built for occasional, meaningful capture, not daily entries."),
                ("Is Shide a memoir service?", "No. A memoir service interviews someone, often a parent, about their past and makes a book of it. Shide is an app you use yourself to keep your own life as it unfolds."),
                ("Where is my data stored?", "Its core archive is local-first: memories live on your iPhone, and no account is required to record and make a book. Online AI is optional through Ensō+."),
            ],
            "cards": [
                (f"{BASE}/en/memory-app-vs-storytelling-service/", "Memory app vs. storytelling service", "Which one do you actually need — an app that keeps your own life, or a service that interviews a parent about their past?"),
                (f"{BASE}/en/features/", "What Shide implements today", "A code-backed account of the on-device memory store, cultural context, map, and book engine."),
                (f"{BASE}/en/privacy/", "Privacy boundaries", "On-device data, optional online features, and what leaves the device."),
            ],
        },
        "ja": {
            "title": "人生を、起きたその時に記録する — ローカルファーストの個人ライフアーカイブ",
            "desc": "華語家庭のためのライフアーカイブ。出来事・場所・その年のキーセイク・振り返りを、起きたその時に端末内へ残し、あとから中英対応のライフブックにまとめられます。日記でも、回顧録サービスでもありません。",
            "eyebrow": "ライフアーカイブ", "shot": True,
            "h1": "何年も経ってから振り返るのではなく、起きたその時に人生を残す",
            "lede": "拾得は「ライフアーカイブ」——人生を起きたその時に残すための iPhone アプリです。大切な出来事、場所、その年のキーセイク、振り返りを記録します。中心となるアーカイブはローカルファーストで、記録や製本にアカウントは不要です。オンライン AI は任意の Ensō+ 機能です。準備ができたら、残してきたものを中国語・英語に対応したデジタル・ライフブックにまとめられます。毎日書く日記ではなく、誰かの過去を取材して本にするサービスでもありません。",
            "sections": [
                {"h2": "ライフアーカイブとは", "p": ["ライフアーカイブとは、人生を起きたその時に残していく記録です。何年も後に書く回顧録でも、毎日埋めなければならない日記でもありません。大切なもの——出来事、場所、キーセイク、心に浮かんだ言葉——を残し、それが時とともに積み重なって、自分の人生のアーカイブになっていきます。"]},
                {"h2": "日記でも、取材製本サービスでもない", "p": ["多くの日記は毎日の記入を軸に組み立てられています。ライフアーカイブは毎日書くことを求めません——残す価値があると思ったときに一つ加えます。取材製本サービスはまた別のもので、誰か（多くは親）の過去を取材して一冊の本にします。拾得はそのどちらでもありません。あなた自身が使い、進行中の自分の人生を残すためのアプリです。"]},
                {"h2": "拾得はどう人生を残すか", "p": ["拾得は、人生が実際に営まれる形——出来事ごと、場所ごと、年ごと——に記憶を整理します。日付順に並ぶ流れとしてではありません。"],
                 "ul": ["出来事と振り返り——何が起き、どう感じたかを、自分の言葉で。", "場所——人生には地理があります。拾得はそれがどこで起きたかを残します。", "その年のキーセイク——ごく少数のものが、その一年を表します。", "きょうという日——過去の同じ日に、あなたが何を残したか。"]},
                {"h2": "ローカルファーストで、プライベート", "p": ["中心となるアーカイブはローカルファーストです。記憶はあなたの iPhone に保存され、記録にも製本にもアカウントは要りません。オンライン AI は任意の Ensō+ 機能で、あなたが自分で呼び出したときにだけ使われます。"]},
                {"h2": "準備ができたら、中英のライフブックを", "p": ["準備ができたら、拾得は残してきたものを中国語・英語に対応したデジタル・ライフブックにまとめられます。自分のために築いたアーカイブを、次の世代も読めるように。"]},
            ],
            "faq": [
                ("ライフアーカイブとは何ですか？", "人生を起きたその時に残していく記録です——出来事・場所・その年のキーセイク・振り返り——後から書く回顧録でも、毎日つける日記でもありません。"),
                ("ライフアーカイブは日記とどう違いますか？", "日記は多くの場合、日付に沿って毎日記入していくものです。ライフアーカイブは毎日書くことを求めず、意味のある瞬間をその都度残し、出来事・場所・年で整理します。"),
                ("毎日日記を書かなくても、自分の人生を記録できますか？", "できます。拾得は「意味があるときにだけ残す」ために作られており、毎日の記入を求めません。"),
                ("拾得は取材製本サービスですか？", "いいえ。取材製本サービスは誰か（多くは親）の過去を取材して本にします。拾得はあなた自身が使い、進行中の自分の人生を残すためのアプリです。"),
                ("データはどこに保存されますか？", "中心となるアーカイブはローカルファーストです。記憶は iPhone に保存され、記録にも製本にもアカウントは不要です。オンライン AI は任意の Ensō+ 機能です。"),
            ],
            "cards": [
                (f"{BASE}/ja/memory-app-vs-storytelling-service/", "記憶アプリと取材製本サービス", "本当に必要なのはどちらか——自分の人生を残すアプリか、親の過去を取材するサービスか。"),
                (f"{BASE}/ja/features/", "拾得が現在実装している機能", "端末内の記憶ストア、文化コンテキスト、地図、製本エンジンを、コードに基づいて。"),
                (f"{BASE}/ja/privacy/", "プライバシーの境界", "端末内データ、任意のオンライン機能、そして何が端末を離れるか。"),
            ],
        },
    },
    "memory-app-vs-storytelling-service": {
        "zh-Hans": {
            "title": "记忆 App 还是采访成书服务 — 你到底需要哪个？",
            "desc": "采访成书服务采访某人（通常是父母）、把他的过去做成一本书；个人生命档案 App 把你自己正在发生的一生留在端上。这一页帮你选，也说明两者何时互补。",
            "eyebrow": "决策指南", "shot": False,
            "h1": "采访成书的服务，和一个长期属于你自己的生命档案，是两件事",
            "lede": "像 StoryWorth、Baohua、Remento 这类采访/回忆录服务，通常用问题或采访帮某个人把过去的故事重新讲出来，最后往往是一本回忆录或纪念书。而像拾得这样的个人生命档案，出发点不同：它持续地把你自己正在发生的一生留在端上，再整理成一本中英对照的岁月书。要把父母的过去做成礼物，选服务；要长期留住自己的一生，选档案 App。两者也可以互补。",
            "sections": [
                {"h2": "两件不同的事", "p": ["这两类产品看起来像——最后都出一本书——但它们为不同的事而造。采访成书服务通常是一个有明确目标的项目：你或家人在一段时间里回答问题或接受采访，把过去整理成纪念内容。个人生命档案是持续的：你在生活发生时把自己的一生留住，只要你还在用，它就一直在积累。"]},
                {"h2": "并排来看", "p": [], "table": {
                    "head": ["你的需求", "采访 / 回忆录服务", "个人生命档案（拾得）"],
                    "rows": [
                        ["主要对象", "通常是父母、长辈或某位讲述者", "自己正在发生的一生"],
                        ["使用方式", "问题 / 采访", "持续记录事件、地点、信物、反思"],
                        ["时间模式", "主要回顾过去", "从现在持续积累"],
                        ["输出", "通常为回忆录 / 纪念书", "不断生长的档案 + 数字岁月书"],
                        ["数据模式", "通常需账户或上传内容以提供服务", "核心档案本地优先 / 端上"],
                        ["是否要求日更", "通常不需要", "不需要"],
                        ["送礼", "常见使用场景", "目前非核心场景"],
                        ["长期自用", "通常不是主要设计目标", "核心设计目标"],
                    ]}},
                {"h2": "什么时候选采访成书服务", "p": ["当你想把父母或长辈的过去采访下来、做成一本能拿在手里的纪念书——尤其是用来送礼，尤其是长辈更愿意开口说、而不是用 App 时——选 StoryWorth、Baohua 或类似服务。"]},
                {"h2": "什么时候选个人生命档案", "p": ["当你想把自己正在发生的一生长期留住，隐私优先、存在端上，中英双语，又不想背每天写日记的负担时——选拾得这样的个人生命档案。"]},
                {"h2": "两者可以互补", "p": ["两者并不互斥。很多家庭用采访成书服务给父母做一本回忆录，同时用生命档案留住自己持续的记录。说句实在话：实体纪念书、送礼流程、采访父母，是这些服务的强项；拾得的强项，是那份持续的、端上的、为自己留下的档案。"]},
            ],
            "faq": [
                ("什么是采访成书（回忆录）服务？", "用问题或采访——通常是采访父母——把过去的故事重新讲出来，最后往往做成一本回忆录或纪念书的服务。"),
                ("什么是个人生命档案 App？", "你自己用来把正在发生的一生留住的 App，按事件、地点、年份组织，可以整理成一本岁月书。"),
                ("我该用采访成书服务，还是生命档案 App？", "当你的目标是留住父母的过去（常做成能拿在手里的纪念书、很适合送礼），用采访成书服务；想长期私密地留住自己的一生，用生命档案 App。两者可以互补。"),
                ("拾得是 StoryWorth 的替代吗？", "在某些目标上是——但拾得不是能直接顶替 StoryWorth 的产品。StoryWorth 以「用问题收集故事、做成纪念书」为核心；拾得是为「把自己正在发生的一生持续、本地地留住」而造。"),
                ("两者的数据模式有何不同？", "隐私取决于各家服务。拾得采用本地优先：核心档案留在设备上，在线 AI 可选，只在用户主动触发时才使用。"),
            ],
            "cards": [
                (f"{BASE}/record-your-life-as-it-happens/", "在生活发生时记录它", "拾得背后的「生命档案」理念：在人生展开时就留住，而不是多年以后。"),
                (f"{BASE}/features/", "拾得当前实现了什么", "逐项可核验：App 到底做了什么。"),
                (f"{BASE}/privacy/", "隐私边界", "一个本地优先的档案，怎么存你的回忆。"),
            ],
        },
        "zh-Hant": {
            "title": "記憶 App 還是採訪成書服務 — 你到底需要哪個？",
            "desc": "採訪成書服務採訪某人（通常是父母）、把他的過去做成一本書；個人生命檔案 App 把你自己正在發生的一生留在端上。這一頁幫你選，也說明兩者何時互補。",
            "eyebrow": "決策指南", "shot": False,
            "h1": "採訪成書的服務，和一個長期屬於你自己的生命檔案，是兩件事",
            "lede": "像 StoryWorth、Baohua、Remento 這類採訪/回憶錄服務，通常用問題或採訪幫某個人把過去的故事重新講出來，最後往往是一本回憶錄或紀念書。而像拾得這樣的個人生命檔案，出發點不同：它持續地把你自己正在發生的一生留在端上，再整理成一本中英對照的歲月書。要把父母的過去做成禮物，選服務；要長期留住自己的一生，選檔案 App。兩者也可以互補。",
            "sections": [
                {"h2": "兩件不同的事", "p": ["這兩類產品看起來像——最後都出一本書——但它們為不同的事而造。採訪成書服務通常是一個有明確目標的項目：你或家人在一段時間裡回答問題或接受採訪，把過去整理成紀念內容。個人生命檔案是持續的：你在生活發生時把自己的一生留住，只要你還在用，它就一直在積累。"]},
                {"h2": "並排來看", "p": [], "table": {
                    "head": ["你的需求", "採訪 / 回憶錄服務", "個人生命檔案（拾得）"],
                    "rows": [
                        ["主要對象", "通常是父母、長輩或某位講述者", "自己正在發生的一生"],
                        ["使用方式", "問題 / 採訪", "持續記錄事件、地點、信物、反思"],
                        ["時間模式", "主要回顧過去", "從現在持續積累"],
                        ["輸出", "通常為回憶錄 / 紀念書", "不斷生長的檔案 + 數位歲月書"],
                        ["資料模式", "通常需帳戶或上傳內容以提供服務", "核心檔案本地優先 / 端上"],
                        ["是否要求日更", "通常不需要", "不需要"],
                        ["送禮", "常見使用場景", "目前非核心場景"],
                        ["長期自用", "通常不是主要設計目標", "核心設計目標"],
                    ]}},
                {"h2": "什麼時候選採訪成書服務", "p": ["當你想把父母或長輩的過去採訪下來、做成一本能拿在手裡的紀念書——尤其是用來送禮，尤其是長輩更願意開口說、而不是用 App 時——選 StoryWorth、Baohua 或類似服務。"]},
                {"h2": "什麼時候選個人生命檔案", "p": ["當你想把自己正在發生的一生長期留住，隱私優先、存在端上，中英雙語，又不想背每天寫日記的負擔時——選拾得這樣的個人生命檔案。"]},
                {"h2": "兩者可以互補", "p": ["兩者並不互斥。很多家庭用採訪成書服務給父母做一本回憶錄，同時用生命檔案留住自己持續的記錄。說句實在話：實體紀念書、送禮流程、採訪父母，是這些服務的強項；拾得的強項，是那份持續的、端上的、為自己留下的檔案。"]},
            ],
            "faq": [
                ("什麼是採訪成書（回憶錄）服務？", "用問題或採訪——通常是採訪父母——把過去的故事重新講出來，最後往往做成一本回憶錄或紀念書的服務。"),
                ("什麼是個人生命檔案 App？", "你自己用來把正在發生的一生留住的 App，按事件、地點、年份組織，可以整理成一本歲月書。"),
                ("我該用採訪成書服務，還是生命檔案 App？", "當你的目標是留住父母的過去（常做成能拿在手裡的紀念書、很適合送禮），用採訪成書服務；想長期私密地留住自己的一生，用生命檔案 App。兩者可以互補。"),
                ("拾得是 StoryWorth 的替代嗎？", "在某些目標上是——但拾得不是能直接頂替 StoryWorth 的產品。StoryWorth 以「用問題收集故事、做成紀念書」為核心；拾得是為「把自己正在發生的一生持續、本地地留住」而造。"),
                ("兩者的資料模式有何不同？", "隱私取決於各家服務。拾得採用本地優先：核心檔案留在設備上，線上 AI 可選，只在使用者主動觸發時才使用。"),
            ],
            "cards": [
                (f"{BASE}/zh-Hant/record-your-life-as-it-happens/", "在生活發生時記錄它", "拾得背後的「生命檔案」理念：在人生展開時就留住，而不是多年以後。"),
                (f"{BASE}/zh-Hant/features/", "拾得當前實現了什麼", "逐項可核驗：App 到底做了什麼。"),
                (f"{BASE}/zh-Hant/privacy/", "隱私邊界", "一個本地優先的檔案，怎麼存你的回憶。"),
            ],
        },
        "en": {
            "title": "Memory app vs. storytelling service — which one do you actually need?",
            "desc": "A storytelling service interviews a person, usually a parent, and produces a book of their past. A personal life archive app keeps your own life as it happens, on-device. Here is how to choose — and when they are complementary.",
            "eyebrow": "Decision guide", "shot": False,
            "h1": "An interview-to-book service and a personal life archive are two different things",
            "lede": "Storytelling and memoir services such as StoryWorth, Baohua and Remento typically use prompts or interviews to help someone reconstruct past stories, often with a memoir or keepsake book as the end product. A personal life archive such as Shide starts from a different job: continuously keeping your own life as it happens, on-device, and organizing it into a bilingual Life Book. Choose a service to capture a parent's past as a gift; choose an archive app to keep your own ongoing life. They can be complementary.",
            "sections": [
                {"h2": "Two different jobs", "p": ["These products look similar — both end in a book — but they are built for different jobs. A storytelling service is usually a goal-oriented project: you or a family member respond to prompts or interviews over a period of time, turning past stories into a keepsake. A personal life archive is ongoing: you keep your own life as it happens, and it accumulates for as long as you use it."]},
                {"h2": "Side by side", "p": [], "table": {
                    "head": ["What you need", "Storytelling / memoir service", "Personal life archive (Shide)"],
                    "rows": [
                        ["Main subject", "Usually a parent, elder, or one narrator", "Your own life, as it happens"],
                        ["How you use it", "Prompts / interviews", "Ongoing capture of events, places, keepsakes, reflections"],
                        ["Time frame", "Mostly reconstructs the past", "Accumulates from now on"],
                        ["Output", "Usually a memoir / keepsake book", "An evolving archive + a digital Life Book"],
                        ["Data model", "Typically an account or uploaded content, to run the service", "Core archive is local-first / on-device"],
                        ["Daily entries required", "Usually not", "No"],
                        ["As a gift", "A common use", "Not the current focus"],
                        ["For long-term personal use", "Usually not the main design goal", "The core design goal"],
                    ]}},
                {"h2": "When to choose a storytelling service", "p": ["Choose StoryWorth, Baohua or a similar service when you want to capture a parent's or elder's past and hold it as a printed keepsake — especially as a gift, and especially when the elder would rather speak than use an app."]},
                {"h2": "When to choose a personal life archive", "p": ["Choose a personal life archive like Shide when you want to keep your own life as it happens, privately and on-device, in Chinese and English, without the burden of daily journaling."]},
                {"h2": "They can be complementary", "p": ["The two are not mutually exclusive. Many families use a storytelling service to make a parent's memoir and a life archive to keep their own ongoing record. Honestly: the printed keepsake, the gift flow, and interviewing a parent are strengths of the services; Shide's strengths are the ongoing, on-device, self-kept archive."]},
            ],
            "faq": [
                ("What is a storytelling (memoir) service?", "A service that uses prompts or interviews — usually with a parent — to reconstruct past stories, often producing a memoir or keepsake book."),
                ("What is a personal life archive app?", "An app you use to keep your own life as it happens, organized by events, places and years, that can be composed into a Life Book."),
                ("Should I use a memoir service or a life archive app?", "Use a memoir service when your goal is to capture a parent's past, often as a printed keepsake and a gift; use a life archive app to keep your own ongoing life privately. They can be complementary."),
                ("Is Shide a StoryWorth alternative?", "For some goals, yes — but Shide is not a drop-in StoryWorth replacement. StoryWorth is built around collecting stories through prompts and turning them into a keepsake book. Shide is built as an ongoing, local-first archive for your own life as it unfolds."),
                ("How is the data model different?", "Privacy depends on the provider. Shide takes a local-first approach: its core archive stays on the device, while online AI is optional and only used when the user actively invokes it."),
            ],
            "cards": [
                (f"{BASE}/en/record-your-life-as-it-happens/", "Record your life as it happens", "The living-archive idea behind Shide: keep your life as it unfolds, not years later."),
                (f"{BASE}/en/features/", "What Shide implements today", "A code-backed account of what the app actually does."),
                (f"{BASE}/en/privacy/", "Privacy boundaries", "How a local-first archive stores your memories."),
            ],
        },
        "ja": {
            "title": "記憶アプリと取材製本サービス — 本当に必要なのはどちら？",
            "desc": "取材製本サービスは誰か（多くは親）を取材して過去の本を作ります。個人ライフアーカイブのアプリは、あなた自身の人生を起きたその時に端末内へ残します。どちらを選ぶか、そしていつ両立するかを説明します。",
            "eyebrow": "選び方ガイド", "shot": False,
            "h1": "取材して本にするサービスと、長く自分のものであり続けるライフアーカイブは、別のものです",
            "lede": "StoryWorth・Baohua・Remento のような取材／回顧録サービスは、多くの場合、質問や取材を通じて誰かの過去の物語を語り直す手助けをし、最終的に回顧録や記念の本になります。一方、拾得のような個人ライフアーカイブは出発点が異なります。あなた自身の人生を起きたその時に端末内へ残し続け、それを中英対応のライフブックにまとめます。親の過去を贈り物にするならサービスを、自分の人生を長く残すならアーカイブアプリを選びます。両者は両立もできます。",
            "sections": [
                {"h2": "二つの異なる目的", "p": ["これらの製品は似て見えます——どちらも本になります——が、目的が異なります。取材製本サービスは多くの場合、目的がはっきりしたプロジェクトです。あなたやご家族が一定の期間にわたって質問に答えたり取材を受けたりして、過去を記念になる形にまとめます。個人ライフアーカイブは継続的です。あなたが人生を起きたその時に残し、使い続ける限り積み重なっていきます。"]},
                {"h2": "並べて見る", "p": [], "table": {
                    "head": ["必要なもの", "取材 / 回顧録サービス", "個人ライフアーカイブ（拾得）"],
                    "rows": [
                        ["主な対象", "多くは親・年長者・一人の語り手", "起きているままの、あなた自身の人生"],
                        ["使い方", "質問 / 取材", "出来事・場所・キーセイク・振り返りを継続的に記録"],
                        ["時間の捉え方", "主に過去を再構成", "これから積み重ねる"],
                        ["成果物", "多くは回顧録 / 記念の本", "育っていくアーカイブ + デジタル・ライフブック"],
                        ["データモデル", "サービス提供のため通常アカウントやアップロードが必要", "中心のアーカイブはローカルファースト / 端末内"],
                        ["毎日の記入", "通常は不要", "不要"],
                        ["贈り物として", "よくある用途", "現在は主眼ではない"],
                        ["長期の自己利用", "通常は主な設計目標ではない", "中心的な設計目標"],
                    ]}},
                {"h2": "取材製本サービスを選ぶとき", "p": ["親や年長者の過去を取材し、手に取れる記念の本として残したいとき——特に贈り物として、そして年長者がアプリよりも話すことを好むときは——StoryWorth や Baohua、あるいは類似のサービスを選びます。"]},
                {"h2": "個人ライフアーカイブを選ぶとき", "p": ["自分自身の人生を起きたその時に、プライベートに端末内で、中国語・英語で、毎日日記を書く負担なしに残したいときは——拾得のような個人ライフアーカイブを選びます。"]},
                {"h2": "両者は両立できる", "p": ["二つは排他的ではありません。多くの家庭が、取材製本サービスで親の回顧録を作りつつ、ライフアーカイブで自分自身の継続的な記録を残します。正直に言えば、印刷された記念の本、贈り物の流れ、親への取材は、サービスの強みです。拾得の強みは、継続的で、端末内にあり、自分のために残すアーカイブです。"]},
            ],
            "faq": [
                ("取材製本（回顧録）サービスとは何ですか？", "質問や取材——多くは親への取材——を通じて過去の物語を語り直し、多くの場合、回顧録や記念の本を作るサービスです。"),
                ("個人ライフアーカイブのアプリとは何ですか？", "自分自身の人生を起きたその時に残すために使うアプリで、出来事・場所・年で整理し、ライフブックにまとめられます。"),
                ("回顧録サービスとライフアーカイブアプリ、どちらを使うべき？", "親の過去を残すことが目的なら（多くは手に取れる記念の本や贈り物として）取材製本サービスを、自分自身の人生をプライベートに長く残すならライフアーカイブアプリを。両者は両立できます。"),
                ("拾得は StoryWorth の代替ですか？", "目的によってはそうです——ただし拾得は StoryWorth をそのまま置き換えるものではありません。StoryWorth は質問で物語を集め、記念の本にすることを中心に作られています。拾得は、進行中の自分の人生を継続的に、ローカルに残すために作られています。"),
                ("データモデルはどう違いますか？", "プライバシーは提供者によります。拾得はローカルファーストの方針です。中心のアーカイブは端末に残り、オンライン AI は任意で、ユーザーが自分で呼び出したときにだけ使われます。"),
            ],
            "cards": [
                (f"{BASE}/ja/record-your-life-as-it-happens/", "人生を、起きたその時に記録する", "拾得の背後にある「ライフアーカイブ」の考え方。何年も後ではなく、人生が展開するその時に残す。"),
                (f"{BASE}/ja/features/", "拾得が現在実装している機能", "アプリが実際に何をするか、コードに基づいて。"),
                (f"{BASE}/ja/privacy/", "プライバシーの境界", "ローカルファーストのアーカイブが、どのように記憶を保存するか。"),
            ],
        },
    },
}


# --------------------------------------------------------------------------- #
# Rendering                                                                    #
# --------------------------------------------------------------------------- #
def render_hreflang(logical: str) -> str:
    out = ["  <!-- geo:hreflang:start -->"]
    for L in LOCALES:
        out.append(f'  <link rel="alternate" hreflang="{L}" href="{page_url(L, logical)}">')
    out.append(f'  <link rel="alternate" hreflang="x-default" href="{page_url("zh-Hans", logical)}">')
    out.append("  <!-- geo:hreflang:end -->")
    return "\n".join(out)


def render_lang_switch(locale: str, logical: str, chrome_all: dict) -> str:
    parts = []
    for L in LOCALES:
        label = chrome_all[L]["lang_label"]
        if L == locale:
            parts.append(f'<strong class="language-link" aria-current="true">{label}</strong>')
        else:
            parts.append(f'<a class="language-link" href="{page_url(L, logical)}" hreflang="{L}">{label}</a>')
    return " · ".join(parts)


def render_table(t: dict) -> str:
    head = "".join(f"<th>{esc_text(c)}</th>" for c in t["head"])
    body = "".join("<tr>" + "".join(f"<td>{esc_text(c)}</td>" for c in row) + "</tr>" for row in t["rows"])
    return f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"


def render_section(sec: dict) -> str:
    html = f"<section><h2>{esc_text(sec['h2'])}</h2>"
    for para in sec.get("p", []):
        html += f"<p>{esc_text(para)}</p>"
    if "ul" in sec:
        html += "<ul>" + "".join(f"<li>{esc_text(li)}</li>" for li in sec["ul"]) + "</ul>"
    if "table" in sec:
        html += render_table(sec["table"])
    if "callout" in sec:
        html += f'<p class="callout">{esc_text(sec["callout"])}</p>'
    return html + "</section>"


def render_html(locale: str, logical: str, page: dict) -> str:
    ch = CHROME[locale]
    url = page_url(locale, logical)
    murl = md_url(locale, logical)
    webpage_ld = json.dumps({
        "@context": "https://schema.org", "@type": "WebPage",
        "headline": page["title"], "description": page["desc"],
        "inLanguage": ch["ld_lang"], "mainEntityOfPage": url, "dateModified": DATE,
    }, ensure_ascii=False)
    faq_ld = json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in page["faq"]],
    }, ensure_ascii=False)
    nav = "".join(f'<a href="{href}">{esc_text(label)}</a>' for href, label in ch["nav"])
    shot = ""
    if page.get("shot"):
        shot = (f'<img class="figure-shot" loading="lazy" width="820" height="1782" '
                f'src="{BASE}/assets/shots/{locale}/01-home.webp" alt="{esc_attr(ch["home_alt"])}">')
    sections = "".join(render_section(s) for s in page["sections"])
    faq_sections = "".join(f"<section><h2>{esc_text(q)}</h2><p>{esc_text(a)}</p></section>" for q, a in page["faq"])
    cards = "".join(
        f'<a class="text-card" href="{href}"><strong>{esc_text(strong)}</strong><span>{esc_text(span)}</span></a>'
        for href, strong, span in page["cards"])
    keep_reading = f'<section><h2>{esc_text(ch["keep_reading"])}</h2><div class="card-grid">{cards}</div></section>'

    return f"""<!doctype html>
<html lang="{locale}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{esc_text(page["title"])} | 拾得 Ensō</title>
  <meta name="description" content="{esc_attr(page["desc"])}">
  <meta name="robots" content="index,follow,max-image-preview:large">
  <meta name="theme-color" content="#a4472d">
  <link rel="canonical" href="{url}">
{render_hreflang(logical)}
  <link rel="alternate" type="text/markdown" href="{murl}" title="Markdown twin">
  <link rel="icon" type="image/png" href="{BASE}/assets/app-icon.png">
  <link rel="apple-touch-icon" href="{BASE}/assets/app-icon.png">
  <link rel="stylesheet" href="{BASE}/assets/styles.css">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{esc_attr(page["title"])}">
  <meta property="og:description" content="{esc_attr(page["desc"])}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{BASE}/assets/app-icon.png">
  <meta name="twitter:card" content="summary">
  <script type="application/ld+json">{webpage_ld}</script>
  <script type="application/ld+json">{faq_ld}</script>
</head>
<body>
  <a class="skip-link" href="#main">{esc_text(ch["skip"])}</a>
  <header class="site-header">
    <a class="brand" href="{ch["brand_href"]}">拾得 Ensō</a>
    <nav aria-label="{esc_attr(ch["nav_label"])}">{nav}</nav>
  <span class="language-switch">{render_lang_switch(locale, logical, CHROME)}</span></header>
  <main id="main"><p class="eyebrow">{esc_text(page["eyebrow"])}</p><h1>{esc_text(page["h1"])}</h1><p class="lede">{esc_text(page["lede"])}</p>{shot}{sections}{faq_sections}{keep_reading}</main>
  <footer><p class="store-line"><a href="{STORE}" rel="external">{esc_text(ch["store"])}</a></p><p class="social-line">{esc_text(ch["follow"])}<a href="https://x.com/ensoshide" rel="external">X</a> · <a href="https://www.instagram.com/ensoshide" rel="external">Instagram</a> · <a href="https://www.youtube.com/@EnsoShide" rel="external">YouTube</a></p>
    <p>{esc_text(ch["disclosure"])}</p>
    <p><a href="{murl}">{esc_text(ch["read_md"])}</a> · {esc_text(ch["factchecked"])}</p>
  </footer>
</body>
</html>
"""


def render_md(locale: str, logical: str, page: dict) -> str:
    ch = CHROME[locale]
    lines = [f"# {page['title']}", "", page["lede"], ""]
    for s in page["sections"]:
        lines += [f"## {s['h2']}", ""]
        for para in s.get("p", []):
            lines += [para, ""]
        for li in s.get("ul", []):
            lines.append(f"- {li}")
        if s.get("ul"):
            lines.append("")
        if "table" in s:
            t = s["table"]
            lines.append("| " + " | ".join(t["head"]) + " |")
            lines.append("| " + " | ".join(["---"] * len(t["head"])) + " |")
            for row in t["rows"]:
                lines.append("| " + " | ".join(row) + " |")
            lines.append("")
    for q, a in page["faq"]:
        lines += [f"## {q}", "", a, ""]
    lines += ["---", "", f"{ch['read_md']}: {page_url(locale, logical)}", "", ch["factchecked"], ""]
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# Write (idempotent, guarded) + sitemap append                                 #
# --------------------------------------------------------------------------- #
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
    force = "--force" in sys.argv
    created: list[str] = []
    unchanged: list[str] = []
    skipped: list[str] = []
    new_urls: list[str] = []

    for logical, locs in PAGES.items():
        for locale in LOCALES:
            page = locs[locale]
            html_path = ROOT / PREFIX[locale] / logical / "index.html"
            md_path = ROOT / PREFIX[locale] / f"{logical}.md"
            write_file(html_path, render_html(locale, logical, page), force, created, unchanged, skipped)
            write_file(md_path, render_md(locale, logical, page), force, created, unchanged, skipped)
            new_urls.append(page_url(locale, logical))

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
