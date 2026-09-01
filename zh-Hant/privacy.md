# 拾得 Ensō 隱私政策與資料邊界

拾得 Ensō 是免 Ensō 賬戶的本地優先記憶應用。本政策區分「儲存在你的裝置上」和「在你主動呼叫聯網功能時傳送」的資料；「本地優先」不意味所有功能都不會使用網路。

## 儲存在本機的核心資料

- Memory：回憶正文、日期、媒體引用、心象、地點和蓋印快照。
- Profile：暱稱、出生年份與地點、聯絡和平安迴音預設等個人資料。
- Keepsake：年度信物快照。
- CompanionState：陪伴狀態與本地派生分值。
- 照片、數字書 PDF、Widget 快照和應用設定。解除安裝 App 可能刪除這些本機資料，請先在 App 內匯出。

## 你主動使用時才會傳送的資料

| 功能 | 可能傳送 | 用途 |
| --- | --- | --- |
| 公共文化內容 | 語言、年份和粗粒度篩選條件 | 只讀獲取公共文化條目 |
| 線上陪聊 | 當前對話與功能頁明示的必要上下文 | 由線上模型生成回覆 |
| 可選 AI 成書 | 你選擇納入的回憶摘要、年份與成書設定 | 生成受驗證器約束的書稿與圖片計劃 |
| 未來郵件 | 收件地址、投遞時間和你明確提交的內容 | 安排郵件投遞 |
| 匿名權益 | 隨機安裝標識、App Attest 證據和 StoreKit 商品/交易狀態 | 防止濫用並確認 Ensō+ 權益；不包含支付卡資料 |

這些聯網 AI 功能（狗子對話、AI 整理、AI 成書）由**第三方 AI 服務商**處理：主要是 **OpenAI**，在其不可用時可能改用 Anthropic（Claude）或 Google（Gemini）。僅在你主動呼叫該功能時，才把相關衍生文字（當前對話、待整理草稿、或截斷的成書摘要）經加密傳輸傳送給上述服務商生成結果；**照片、整冊資料、姓名與聯絡方式從不傳送**。依其公開條款，這些資料不會被用於訓練模型。

## Enso Shide Analytics 與 Google/YouTube 資料

Enso Shide Analytics 是供拾得頻道擁有者或經授權營運者使用的唯讀分析工具。它只請求 `yt-analytics.readonly` 和 `youtube.readonly` 權限，用於讀取經授權頻道的頻道與影片元資料、公開統計、YouTube Analytics 報告、流量來源、受眾匯總與訂閱增量。

- 工具不上傳、編輯、刪除或下載 YouTube 影片，不讀取頻道會員名單或付費資訊。
- OAuth token、原始 JSON 報告與衍生分析儲存在獲授權營運者控制的本機或私有工作區，不上傳到拾得 App 用戶服務。
- Google/YouTube 用戶資料不出售、不用於廣告定向、不用於模型訓練，也不與無關第三方分享。
- 資料只在頻道分析、趨勢比較與 YPP 營運所需期間保留。停止使用時，可刪除本機 token 與報告，並在 Google 帳戶的第三方連接頁撤銷授權。如需刪除協助，聯絡 privacy@shide.app。

Enso Shide Analytics 對 Google API 資料的使用遵守 [Google API Services User Data Policy](https://developers.google.com/terms/api-services-user-data-policy)，包括 Limited Use 要求。

## 可選匿名分析

「幫助改進拾得」開啟時，App 傳送匿名操作型別、短列舉、App 版本和隨機安裝標識。分析事件不包含回憶正文、照片、姓名或聯絡方式。你可在「時空主頁 → 隱私與資料」關閉分析，刪除服務端匿名分析記錄並重置標識。原始匿名事件的設計保留期為 90 天。

> 拾得不使用廣告標識，不為跨 App 或跨網站追蹤出售資料。

## 訂閱、匯出與刪除

- 購買由 Apple StoreKit 處理。拾得只讀取已驗證的商品和權益狀態，不取得你的支付卡資料。
- 你可從「時空主頁 → 隱私與資料」匯出標準 ZIP：可讀 JSON 清單加照片、PDF 數字書和 Widget 檔案。
- 同一頁面可永久刪除 SwiftData、Documents、App Group、設定、分析、通知和本 App 的 Keychain 資料。操作有兩次確認。
- 刪除本機資料或解除安裝 App 不會取消 Apple 訂閱；訂閱必須在 App Store 賬戶中管理。iCloud/系統裝置備份中的副本由 Apple 和你的備份設定控制。

## 許可權、未成年人與聯絡

相機和相簿許可權僅在你選擇拍攝、選取或儲存圖片時申請。拾得 v1 不申請精確位置、聯絡人或 HealthKit 許可權。拾得不主動面向 13 歲以下兒童收集資料。隱私查詢可聯絡 privacy@shide.app，產品支援可聯絡 support@shide.app。

## 繼續閱讀

- [支援與聯絡](/support/)
- [服務條款](/terms/)
- [檢視工程證據](/evidence/)
- [本地優先日記的判斷方法](/answers/local-first-journal/)

在 App Store 下載拾得：https://apps.apple.com/app/apple-store/id6787128369?pt=129013055&ct=web&mt=8

## 資料來源

- [免登入應用入口（內部程式碼審計）](/evidence/)
- [網路服務實現（內部程式碼審計）](/evidence/)
- [雙資料面架構（內部程式碼審計）](/evidence/)

---
頁面語言：zh-Hant
事實核驗日期：2026-08-31

關注：X https://x.com/ensoshide · Instagram https://www.instagram.com/ensoshide · YouTube https://www.youtube.com/@EnsoShide
