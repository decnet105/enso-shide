# 拾得 Ensō 當前實現了什麼

這一頁只列出能夠從當前倉庫定位到實現檔案的能力。設計願景、待部署端點和尚未核實的市場資料不算已交付功能。

## 端上私域記憶

Memory、Profile、Keepsake 與 CompanionState 使用 SwiftData 儲存。MemoryWriter 是回憶的統一寫入口，遷移器負責從舊模型補齊資料。

- 儲存回憶正文、年份、日期、媒體引用、心象和地點。
- 蓋印快照與使用者註記保留在端上私域模型。
- 年度信物儲存為可復現的端上快照。

## 歲月、山河與文化座標

首頁時間線把個人回憶與公共文化座標分層展示；山河頁用 MapKit 從端上 Memory 派生足跡。公共文化條目由 API 只讀下發，不寫入使用者私域正文。

## 陪聊與受約束生成

現役陪聊具有本地 ConversationGraph 兜底，也可以呼叫線上服務。GenUI 只接收文字、白名單卡片意圖和話頭，不允許模型控制佈局、指令碼、顏色或任意 URL。

> 本地兜底存在，不等於整個陪聊和應用都不使用網路。

## 本機與 AI 雙軌成書

本機軌使用確定性選版、分頁和 UIGraphicsPDFRenderer；AI 軌會呼叫專用後端，並在驗證失敗時整冊回落到本機軌。

## 季節文化專題與深鏈分享

拾得按節令推出季節文化專題（如中秋），把該時節的公共文化座標聚成一個可進入的入口；專題與單條文化事件支援通用連結（Universal Link）深鏈，點開直接落到 App 內對應頁面。

## 數字成書的款式與語言

本機與 AI 雙軌成書支援多種作者文風款式與版式；成書覆蓋中英雙語對照，並提供中文、英文、日文單語版本，便於長輩與下一代各取所需。

## 繼續閱讀

- [成書引擎技術說明](/book-engine/)
- [隱私邊界](/privacy/)
- [功能證據表](/evidence/)

在 App Store 下載拾得：https://apps.apple.com/app/apple-store/id6787128369?pt=129013055&ct=web&mt=8

## 資料來源

- [iOS 應用入口（內部程式碼審計）](/evidence/)
- [SwiftData Memory 模型（內部程式碼審計）](/evidence/)
- [GenUI 驗證器（內部程式碼審計）](/evidence/)

---
頁面語言：zh-Hant
事實核驗日期：2026-08-16

關注：X https://x.com/ensoshide · Instagram https://www.instagram.com/ensoshide · YouTube https://www.youtube.com/@EnsoShide
