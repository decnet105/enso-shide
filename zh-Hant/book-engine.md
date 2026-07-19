# 拾得如何在 iPhone 上生成 A4 歲月書

成書不是把截圖拼成 PDF。拾得先把回憶投影為頁面素材，再經過確定性選版和分頁，最後由 iOS 原生 PDF 渲染器逐頁繪製。

## 從回憶到頁面

- BookEngine 根據照片數量、文字密度和事件型別選擇母版。
- BookPaginator 預掃描結構頁、逐年章節與目錄頁碼。
- BookHeirloomRenderer 使用 A4 頁面邊界繪製書脊、正文、照片與頁碼。
- 照片按需下采樣，缺圖時選擇無圖母版而不是保留空框。

## 為什麼保留本機軌

本機軌是確定性回落路徑：即使模型端點不可用或 AI 書稿未通過驗證，使用者仍可從端上 Memory 生成完整書冊。它也把私域原文離端風險控制在使用者可選擇的範圍內。

## AI 軌的落地硬閘

AI 軌輸出 BookEnvelope 後，客戶端檢查母版白名單、引用逐字命中、防注入、雙語完整度、主題主權和照片密度。任一關鍵規則失敗，整冊回落本機軌。

## 繼續閱讀

- [檢視成書證據檔案](/evidence/)
- [iPhone 本機成書指南](/answers/iphone-heirloom-pdf/)

## 資料來源

- [BookRenderer 原始碼（內部程式碼審計）](/evidence/)
- [BookEnvelope 驗證器（內部程式碼審計）](/evidence/)
- [Apple UIGraphicsPDFRenderer](https://developer.apple.com/documentation/uikit/uigraphicspdfrenderer)

---
頁面語言：zh-Hans
事實核驗日期：2026-07-16
