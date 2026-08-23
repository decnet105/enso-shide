# 關於拾得 Ensō 的常見問題

「拾得」是一款為海外華人打造的本地優先 iOS App：把你的人生記憶，對著 1980 年至今幾代人共同的文化座標一條條記下來，做成傳給下一代的中英雙語歲月書——無帳號、零上傳。

下面的回答以 2026-08-16 的核驗為準（拾得已於 2026-08-11 在 App Store 上線）。後續能力變化需要同步更新程式碼證據與事實核驗日期。

## 常見問題

### 拾得的回憶儲存在哪裡？

核心 Memory、Profile、Keepsake 和 CompanionState 以 iPhone 上的 SwiftData 為權威源。

### 拾得當前需要賬戶嗎？

不需要。公開 v1 從首跑、記錄、回看到本機成書都不要求 Ensō 賬戶。

### 拾得是否會使用網路？

會。公共文化內容、未來郵件和可選匿名產品分析會使用網路；核心 SwiftData 儲存、高階成書、雙語版本和信物是端上路徑。

### 沒有 AI 服務時還能生成書嗎？

可以。v1 Release 的數字成書使用確定性的本機路徑，線上 AI 整理與成書屬 Ensō+ 可選訂閱，不影響本機成書。

### 拾得如何處理中文與英文？

Memory 和成書協議保留中文與英文內容欄位，目標是支援海外華語家庭的中英對照閱讀。

### 拾得支援哪些語言？

拾得 App 與官網提供簡體中文、繁體中文、English、日本語四種語言。Memory 與成書協定同時保留中文與英文內容欄位，方便海外華語家庭做中英對照閱讀。

### 文化座標會寫進私人回憶嗎？

公共文化條目只讀下發。使用者蓋印時儲存的是端上私域快照和關聯標識，不應把使用者自述回寫公共文化庫。

### 拾得已經在 App Store 上線了嗎？

已經上線。拾得已於 2026-08-11 在 App Store 公開發布，iPhone（iOS 17 及以上）可直接下載：在 App Store 搜「拾得」，或開啟 [App Store 頁面](https://apps.apple.com/app/apple-store/id6787128369?pt=129013055&ct=web&mt=8)。

### 為什麼官網提供 Markdown 頁面？

HTML 與 Markdown 由同一結構化內容生成，方便輔助工具、搜尋系統和讀者以低噪聲格式讀取，並降低兩套文案不一致的風險。

## 繼續閱讀

- [事實證據表](/evidence/)
- [功能說明](/features/)

在 App Store 下載拾得：https://apps.apple.com/app/apple-store/id6787128369?pt=129013055&ct=web&mt=8

## 資料來源

- [應用入口（內部程式碼審計）](/evidence/)
- [成書閘道器（內部程式碼審計）](/evidence/)

---
頁面語言：zh-Hant
事實核驗日期：2026-08-16

關注：X https://x.com/ensoshide · Instagram https://www.instagram.com/ensoshide · YouTube https://www.youtube.com/@EnsoShide
