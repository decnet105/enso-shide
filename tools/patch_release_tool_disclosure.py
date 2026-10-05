#!/usr/bin/env python3
"""Add the Enso Shide Release Tool (YouTube API, write scope, own channel only) disclosure.

Privacy: 4 locales x {html, md} get a new section after the Enso Shide Analytics section.
Terms: the bilingual zh-Hans/en page (html + md) names the tool in scope, Google/YouTube and revocation.
Dates: effective date + fact-check date + JSON-LD dateModified -> 2026-10-05.

Idempotent (skips files that already mention the tool), fail-closed (every anchor must match once),
stdlib only, never rewrites unrelated content, never commits or pushes.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARK = "Enso Shide Release Tool"
NEW_DATE = "2026-10-05"
UDP = "https://developers.google.com/terms/api-services-user-data-policy"
YT_TOS = "https://www.youtube.com/t/terms"
G_PP = "https://policies.google.com/privacy"
CONN = "https://myaccount.google.com/connections"

PRIVACY = {
    "zh-Hans": {
        "dir": "", "eyebrow": "2026 年 10 月 5 日生效",
        "h2": "Enso Shide Release Tool 与 YouTube API Services",
        "intro": "Enso Shide Release Tool 是 ENSO SHIDE 自用的内部发布工具，只由拾得 YouTube 频道 @EnsoShide 的所有者使用，不对外提供。它通过 YouTube API Services 请求 `youtube.force-ssl` 权限，只用于管理我们自己频道的视频：设置标题、描述、标签、多语言元数据、自定义缩略图、定时发布时间和字幕轨。",
        "bullets": [
            "只访问 @EnsoShide 一个频道，不访问其他频道，也不收集观众或其他用户的数据。",
            "只在运行工具的本机保存我们自己视频的 ID 与发布状态；OAuth token 只保存在这台电脑上。",
            "相关数据不出售、不用于广告或模型训练，也不与第三方共享。",
            "可随时删除本机 token，并在 Google 账号的[第三方连接页]({conn})撤销授权。如需删除协助，联系 privacy@shide.app。",
        ],
        "outro": "使用我们通过 YouTube API Services 提供的功能，即表示你同意受 [YouTube 服务条款]({yt}) 约束；Google 如何处理数据，见 [Google 隐私政策]({pp})。本工具对 Google API 数据的使用遵守 [Google API Services User Data Policy]({udp})，包括 Limited Use 要求。",
    },
    "zh-Hant": {
        "dir": "zh-Hant/", "eyebrow": "2026 年 10 月 5 日生效",
        "h2": "Enso Shide Release Tool 與 YouTube API Services",
        "intro": "Enso Shide Release Tool 是 ENSO SHIDE 自用的內部發布工具，只由拾得 YouTube 頻道 @EnsoShide 的擁有者使用，不對外提供。它透過 YouTube API Services 請求 `youtube.force-ssl` 權限，只用於管理我們自己頻道的影片：設定標題、說明、標籤、多語言元資料、自訂縮圖、定時發布時間與字幕軌。",
        "bullets": [
            "只存取 @EnsoShide 一個頻道，不存取其他頻道，也不收集觀眾或其他用戶的資料。",
            "只在執行工具的本機保存我們自己影片的 ID 與發布狀態；OAuth token 只保存在這台電腦上。",
            "相關資料不出售、不用於廣告或模型訓練，也不與第三方分享。",
            "可隨時刪除本機 token，並在 Google 帳戶的[第三方連接頁]({conn})撤銷授權。如需刪除協助，聯絡 privacy@shide.app。",
        ],
        "outro": "使用我們透過 YouTube API Services 提供的功能，即表示你同意受 [YouTube 服務條款]({yt}) 約束；Google 如何處理資料，見 [Google 隱私權政策]({pp})。本工具對 Google API 資料的使用遵守 [Google API Services User Data Policy]({udp})，包括 Limited Use 要求。",
    },
    "en": {
        "dir": "en/", "eyebrow": "Effective October 5, 2026",
        "h2": "Enso Shide Release Tool and YouTube API Services",
        "intro": "Enso Shide Release Tool is an internal publishing tool used only by the owner of ENSO SHIDE's YouTube channel @EnsoShide; it is not offered to anyone else. It uses YouTube API Services with the `youtube.force-ssl` scope only to manage our own channel's videos: setting titles, descriptions, tags, localized metadata, custom thumbnails, scheduled publish times, and caption tracks.",
        "bullets": [
            "It accesses only the @EnsoShide channel, no other channel, and does not collect data about viewers or other users.",
            "It keeps only our own video IDs and release status, in local files on the computer that runs it; the OAuth token is stored only on that computer.",
            "This data is not sold, not used for advertising or model training, and not shared with third parties.",
            "The token can be deleted at any time and access revoked from the [third-party connections page]({conn}) of the Google Account. For deletion assistance, email privacy@shide.app.",
        ],
        "outro": "By using features we provide through YouTube API Services, you agree to be bound by the [YouTube Terms of Service]({yt}). See the [Google Privacy Policy]({pp}) for how Google handles data. This tool's use of Google API data follows the [Google API Services User Data Policy]({udp}), including the Limited Use requirements.",
    },
    "ja": {
        "dir": "ja/", "eyebrow": "2026年10月5日発効",
        "h2": "Enso Shide Release Tool と YouTube API Services",
        "intro": "Enso Shide Release Tool は、ENSO SHIDE の YouTube チャンネル @EnsoShide の所有者だけが使う社内向け公開ツールで、外部には提供していません。YouTube API Services の `youtube.force-ssl` 権限を使い、自社チャンネルの動画の管理だけを行います（タイトル、説明、タグ、多言語メタデータ、カスタムサムネイル、予約公開日時、字幕トラックの設定）。",
        "bullets": [
            "アクセスするのは @EnsoShide チャンネルのみで、他のチャンネルにはアクセスせず、視聴者や他のユーザーのデータも収集しません。",
            "保存するのは自社動画の ID と公開状況のみで、ツールを実行する端末内のファイルに保存します。OAuth token もその端末にのみ保存されます。",
            "これらのデータを販売、広告、モデル学習に使用せず、第三者とも共有しません。",
            "token はいつでも削除でき、Google アカウントの[サードパーティ接続ページ]({conn})でアクセスを取り消せます。削除の支援は privacy@shide.app へご連絡ください。",
        ],
        "outro": "YouTube API Services を通じて当社が提供する機能を使用することで、[YouTube 利用規約]({yt})に同意したものとみなされます。Google によるデータの取り扱いは [Google プライバシーポリシー]({pp})をご覧ください。本ツールによる Google API データの利用は、Limited Use 要件を含む [Google API Services User Data Policy]({udp}) に従います。",
    },
}

LINKS = {"conn": CONN, "yt": YT_TOS, "pp": G_PP, "udp": UDP}


def fmt(s: str) -> str:
    return s.format(**LINKS)


def md_to_html_inline(s: str) -> str:
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<a href="\2" rel="external">\1</a>', s)


def sub_once(text: str, pattern: str, repl, path: str, flags=0) -> str:
    new, n = re.subn(pattern, repl, text, count=1, flags=flags)
    if n != 1:
        raise SystemExit(f"FAIL anchor not found in {path}: {pattern[:60]}")
    return new


def patch_dates_html(s: str, path: str, eyebrow: str | None) -> str:
    s = sub_once(s, r'"dateModified":"2026-08-31"', f'"dateModified":"{NEW_DATE}"', path)
    s = sub_once(s, r"2026-08-31(?=</p>)", NEW_DATE, path)
    if eyebrow:
        s = sub_once(s, r'(<p class="eyebrow">)[^<]*(</p>)', lambda m: m.group(1) + eyebrow + m.group(2), path)
    return s


def privacy(loc: str, cfg: dict, changed: list, skipped: list) -> None:
    md_path = ROOT / f"{cfg['dir']}privacy.md"
    html_path = ROOT / f"{cfg['dir']}privacy/index.html"
    for p in (md_path, html_path):
        if MARK in p.read_text(encoding="utf-8"):
            skipped.append(str(p.relative_to(ROOT)))
    if str(md_path.relative_to(ROOT)) not in skipped:
        s = md_path.read_text(encoding="utf-8")
        block = "\n\n## " + cfg["h2"] + "\n\n" + fmt(cfg["intro"]) + "\n\n" + "\n".join(f"- {fmt(b)}" for b in cfg["bullets"]) + "\n\n" + fmt(cfg["outro"])
        # Insert right after the Analytics section's Limited Use paragraph.
        s = sub_once(s, r"(Enso Shide Analytics[^\n]*\(https://developers\.google\.com/terms/api-services-user-data-policy\)[^\n]*)", lambda m: m.group(1) + block, str(md_path))
        s = re.sub(r"(事實核驗日期|事实核验日期)：2026-08-31", lambda m: f"{m.group(1)}：{NEW_DATE}", s)
        md_path.write_text(s, encoding="utf-8")
        changed.append(str(md_path.relative_to(ROOT)))
    if str(html_path.relative_to(ROOT)) not in skipped:
        s = html_path.read_text(encoding="utf-8")
        sec = ('  <section class="oauth-disclosure"><h2>' + cfg["h2"] + "</h2><p>" + md_to_html_inline(fmt(cfg["intro"])) + "</p><ul>"
               + "".join(f"<li>{md_to_html_inline(fmt(b))}</li>" for b in cfg["bullets"]) + "</ul><p>"
               + md_to_html_inline(fmt(cfg["outro"])) + "</p></section>\n")
        s = sub_once(s, r'(  <section class="oauth-disclosure">.*?</section>\n)', lambda m: m.group(1) + sec, str(html_path), re.S)
        s = patch_dates_html(s, str(html_path), cfg["eyebrow"])
        html_path.write_text(s, encoding="utf-8")
        changed.append(str(html_path.relative_to(ROOT)))


TERMS_ZH = [
    ("和 Enso Shide Analytics 频道分析工具。", "、Enso Shide Analytics 频道分析工具和 Enso Shide Release Tool 内部发布工具。"),
    ("仅用于经 Google 账号持有者明确授权的 YouTube 频道。",
     "仅用于经 Google 账号持有者明确授权的 YouTube 频道。{sep}Enso Shide Release Tool 是 ENSO SHIDE 自用的内部发布工具，只用于管理 ENSO SHIDE 自有 YouTube 频道 @EnsoShide 的视频元数据、缩略图、定时发布与字幕，不对外提供。"),
    ("Enso Shide Analytics 只请求业务所需的最小只读权限。",
     "Enso Shide Analytics 只请求业务所需的最小只读权限；Enso Shide Release Tool 只请求管理自有频道视频所需的 {code}youtube.force-ssl{endcode} 权限，且只作用于 @EnsoShide。"),
    ("撤销 Enso Shide Analytics 访问权。", "撤销 Enso Shide Analytics 访问权；Enso Shide Release Tool 同样可删除本机 token 并在该页撤销。"),
    ("These Terms apply to the Shide iOS app, shide.app, and Enso Shide Analytics.",
     "These Terms apply to the Shide iOS app, shide.app, Enso Shide Analytics, and Enso Shide Release Tool. Enso Shide Release Tool is an internal tool that manages only ENSO SHIDE's own YouTube channel @EnsoShide (video metadata, thumbnails, scheduling, and captions) with the youtube.force-ssl scope; it is not offered to others."),
]


def terms(changed: list, skipped: list) -> None:
    for path, kind in ((ROOT / "terms.md", "md"), (ROOT / "terms/index.html", "html")):
        s = path.read_text(encoding="utf-8")
        if MARK in s:
            skipped.append(str(path.relative_to(ROOT)))
            continue
        for old, new in TERMS_ZH:
            new = new.format(sep="\n- " if kind == "md" else "</li><li>",
                             code="`" if kind == "md" else "<code>", endcode="`" if kind == "md" else "</code>")
            if s.count(old) != 1:
                raise SystemExit(f"FAIL terms anchor x{s.count(old)} in {path}: {old[:40]}")
            s = s.replace(old, new)
        if kind == "md":
            s = sub_once(s, r"生效日期：2026 年 8 月 31 日", "生效日期：2026 年 10 月 5 日", str(path))
            s = sub_once(s, r"事实核验日期：2026-08-31", f"事实核验日期：{NEW_DATE}", str(path))
        else:
            s = s.replace(" 与 Enso Shide Analytics 的服务条款。", "、Enso Shide Analytics 与 Enso Shide Release Tool 的服务条款。")
            s = patch_dates_html(s, str(path), "2026 年 10 月 5 日生效")
        path.write_text(s, encoding="utf-8")
        changed.append(str(path.relative_to(ROOT)))


def main() -> int:
    changed: list[str] = []
    skipped: list[str] = []
    for loc, cfg in PRIVACY.items():
        privacy(loc, cfg, changed, skipped)
    terms(changed, skipped)
    print("changed:", *changed, sep="\n  ")
    print("skipped:", *skipped or ["(none)"], sep="\n  ")
    return 0


if __name__ == "__main__":
    sys.exit(main())
