# 宣传主张与工程证据如何对应

这一页是官网内容的事实闸门。只有证据状态为“已验证”的条目可以用确定语气发布；其余必须带限定或保持不发布。

## 内部审计基线

本登记表依据 2026-07-16 对私有产品仓库 main 分支的发布审计更新（2026-08-16 复核：App Store 已上线）。私有源码不会因营销站上线而公开；公开页面只给出可核对的文件职责、边界结论与审计日期。

> 这是一份内部工程核验记录，不等同于第三方安全审计、App Store 审核或外部认证。

## 主张登记

| 主张 | 状态 | 证据 | 允许措辞 |
| --- | --- | --- | --- |
| 核心 Memory 使用 SwiftData | 已验证 | Memory.swift / MystoryApp.swift | 端上权威源 |
| 本机生成 A4 PDF | 已验证 | BookRenderer.swift | 本机成书 |
| 中英内容字段 | 已验证 | Memory.swift / BookEnvelope.swift | 支持中英内容结构 |
| 所有功能均不联网 | 不成立 | APIService.swift | 不得发布 |
| 公开 v1 不需要账户 | 已验证 | MystoryApp.swift / Release 编译条件 | 无需 Ensō 账户 |
| 在线 AI 成书（Ensō+ 订阅权益） | 已验证 | OnlinePremiumPolicy.swift + 生产后端 | 订阅权益·非免费 v1 |
| 通过外部隐私审计 | 无证据 | 尚无审计报告 | 不得发布 |
| App Store 已公开上线 | 已验证 | App Store id6787128369（2026-08-11 发布） | 已上线，可下载 |
| 固定查询性能指标 | 未测量 | 尚无基准报告 | 不得发布数字 |

## 发布规则

- 版本、价格、评分和下载链接必须来自 App Store Connect 或公开页面。
- 性能数字必须附测试设备、数据规模、样本数和测量方法。
- 竞品比较必须引用竞品当前官方文档并标注核验日期。
- 搜索引擎提及率必须保存原始回答、模型、日期、地区与是否登录。

## 继续阅读

- [隐私边界](/privacy/)
- [GEO 常见问题](/faq/)

[在 App Store 下载拾得](https://apps.apple.com/app/apple-store/id6787128369?pt=129013055&ct=web&mt=8)

## 资料来源

- as-built 系统总览（内部代码审计）
- 免登录应用入口（内部代码审计）
- 网络服务（内部代码审计）

---
页面语言：zh-Hans
事实核验日期：2026-08-16

关注：X https://x.com/ensoshide · Instagram https://www.instagram.com/ensoshide · YouTube https://www.youtube.com/@EnsoShide
