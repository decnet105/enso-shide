# 如何在 iPhone 本機生成適合長期儲存的回憶 PDF

長期儲存的回憶 PDF 需要穩定頁面模型，而不只是把螢幕內容打印出來。最關鍵的設計是讓內容、分頁和繪製相互獨立。

## 推薦的六層流水線

- 把回憶投影成與 UI 無關的頁面素材。
- 按照片數量與文字密度選擇有限母版。
- 預先計算章節、目錄和跨頁配對。
- 為長文保留繼續頁，不截斷正文。
- 對照片下采樣但保持比例。
- 用原生 PDF 渲染器逐頁繪製並做迴歸樣本。

## 拾得的實現選擇

拾得用 BookEngine 選版、BookPaginator 分頁、BookHeirloomRenderer 繪製。缺圖走無圖母版，AI 軌輸出需通過 BookEnvelope 驗證，失敗則整冊回落。

## 繼續閱讀

- [成書引擎完整說明](/zh-Hant/book-engine/)
- [為海外家庭儲存中文回憶](/zh-Hant/answers/chinese-family-memory/)

## 資料來源

- [Apple UIGraphicsPDFRenderer](https://developer.apple.com/documentation/uikit/uigraphicspdfrenderer)
- [拾得 BookRenderer（內部程式碼審計）](/zh-Hant/evidence/)

---
頁面語言：zh-Hant
事實核驗日期：2026-07-16
