# 拾得 Ensō が iPhone で A4 の人生の書を組む仕組み

長く残る人生の書には、スクリーンショットの寄せ集めではなく、安定したページモデルが必要です。Ensō は記憶をページソースへと投影し、ページ割りを行い、各ページを iOS ネイティブの PDF API でレンダリングします。

## 決定論的なローカルパイプライン

- BookEngine は限定されたページマスターの集合から選択します。
- BookPaginator はセクション・目次項目・見開きページを算出します。
- BookHeirloomRenderer は A4 ページ・本文・写真・罫線・ノンブルを描画します。
- 画像が欠けている場合は、空の枠を残すのではなく、テキスト向けの安全なマスターを選びます。

## オンライン生成のリリース境界

リポジトリには検証済みの実験的なオンライン生成トラックが含まれますが、v1 リリースは課金が発生するオンライン AI を無効にしています。出荷されるプレミアムの書籍は、決定論的なローカル経路を使用します。

## 関連ページ

- [プライバシーの境界](/ja/privacy/)
- [技術ガイド](/ja/answers/iphone-heirloom-pdf/)

## 参考資料

- [BookRenderer ソース（内部コード監査）](/ja/evidence/)
- [Apple UIGraphicsPDFRenderer](https://developer.apple.com/documentation/uikit/uigraphicspdfrenderer)

---
ページ言語：ja
事実確認日：2026-08-16

App Store で拾得をダウンロード：https://apps.apple.com/app/apple-store/id6787128369?pt=129013055&ct=web&mt=8

フォロー：X https://x.com/ensoshide · Instagram https://www.instagram.com/ensoshide · YouTube https://www.youtube.com/@EnsoShide
