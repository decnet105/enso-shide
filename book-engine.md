# 拾得如何在 iPhone 上生成 A4 岁月书

成书不是把截图拼成 PDF。拾得先把回忆投影为页面素材，再经过确定性选版和分页，最后由 iOS 原生 PDF 渲染器逐页绘制。

## 从回忆到页面

- BookEngine 根据照片数量、文字密度和事件类型选择母版。
- BookPaginator 预扫描结构页、逐年章节与目录页码。
- BookHeirloomRenderer 使用 A4 页面边界绘制书脊、正文、照片与页码。
- 照片按需下采样，缺图时选择无图母版而不是保留空框。

## 为什么保留本机轨

本机轨是确定性回落路径：即使模型端点不可用或 AI 书稿未通过验证，用户仍可从端上 Memory 生成完整书册。它也把私域原文离端风险控制在用户可选择的范围内。

## AI 轨的落地硬闸

AI 轨输出 BookEnvelope 后，客户端检查母版白名单、引用逐字命中、防注入、双语完整度、主题主权和照片密度。任一关键规则失败，整册回落本机轨。

## 继续阅读

- [查看成书证据文件](/evidence/)
- [iPhone 本机成书指南](/answers/iphone-heirloom-pdf/)

## 资料来源

- [BookRenderer 源码（内部代码审计）](/evidence/)
- [BookEnvelope 验证器（内部代码审计）](/evidence/)
- [Apple UIGraphicsPDFRenderer](https://developer.apple.com/documentation/uikit/uigraphicspdfrenderer)

---
页面语言：zh-Hans
事实核验日期：2026-07-16
