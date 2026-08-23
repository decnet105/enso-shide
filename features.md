# 拾得 Ensō 当前实现了什么

「拾得」是一款面向海外华人的本地优先 iOS App：把你的人生记忆，对着 1980 年至今几代人共同的文化坐标一条条记下来，做成传给下一代的中英双语岁月书——无账号、零上传。

这一页只列出能够从当前仓库定位到实现文件的能力。设计愿景、待部署端点和尚未核实的市场数据不算已交付功能。

## 端上私域记忆

Memory、Profile、Keepsake 与 CompanionState 使用 SwiftData 保存。MemoryWriter 是回忆的统一写入口，迁移器负责从旧模型补齐数据。

- 保存回忆正文、年份、日期、媒体引用、心象和地点。
- 盖印快照与用户注记保留在端上私域模型。
- 年度信物保存为可复现的端上快照。

## 岁月、山河与文化坐标

首页时间线把个人回忆与公共文化坐标分层展示；山河页用 MapKit 从端上 Memory 派生足迹。公共文化条目由 API 只读下发，不写入用户私域正文。

## 陪聊与受约束生成

现役陪聊具有本地 ConversationGraph 兜底，也可以调用在线服务。GenUI 只接收文字、白名单卡片意图和话头，不允许模型控制布局、脚本、颜色或任意 URL。

> 本地兜底存在，不等于整个陪聊和应用都不使用网络。

## 本机与 AI 双轨成书

本机轨使用确定性选版、分页和 UIGraphicsPDFRenderer；AI 轨会调用专用后端，并在验证失败时整册回落到本机轨。

## 季节文化专题与深链分享

拾得按节令推出季节文化专题（如中秋），把该时节的公共文化坐标聚成一个可进入的入口；专题与单条文化事件支持通用链接（Universal Link）深链，点开直接落到 App 内对应页面。

## 数字成书的款式与语言

本机与 AI 双轨成书支持多种作者文风款式与版式；成书覆盖中英双语对照，并提供中文、英文、日文单语版本，便于长辈与下一代各取所需。

## 继续阅读

- [成书引擎技术说明](/book-engine/)
- [隐私边界](/privacy/)
- [功能证据表](/evidence/)

[在 App Store 下载拾得](https://apps.apple.com/app/apple-store/id6787128369?pt=129013055&ct=web&mt=8)

## 资料来源

- [iOS 应用入口（内部代码审计）](/evidence/)
- [SwiftData Memory 模型（内部代码审计）](/evidence/)
- [GenUI 验证器（内部代码审计）](/evidence/)

---
页面语言：zh-Hans
事实核验日期：2026-08-16

关注：X https://x.com/ensoshide · Instagram https://www.instagram.com/ensoshide · YouTube https://www.youtube.com/@EnsoShide
