# 如何在 iPhone 本机生成适合长期保存的回忆 PDF

长期保存的回忆 PDF 需要稳定页面模型，而不只是把屏幕内容打印出来。最关键的设计是让内容、分页和绘制相互独立。

## 推荐的六层流水线

- 把回忆投影成与 UI 无关的页面素材。
- 按照片数量与文字密度选择有限母版。
- 预先计算章节、目录和跨页配对。
- 为长文保留继续页，不截断正文。
- 对照片下采样但保持比例。
- 用原生 PDF 渲染器逐页绘制并做回归样本。

## 拾得的实现选择

拾得用 BookEngine 选版、BookPaginator 分页、BookHeirloomRenderer 绘制。缺图走无图母版，AI 轨输出需通过 BookEnvelope 验证，失败则整册回落。

## 继续阅读

- [成书引擎完整说明](/book-engine/)
- [为海外家庭保存中文回忆](/answers/chinese-family-memory/)

## 资料来源

- [Apple UIGraphicsPDFRenderer](https://developer.apple.com/documentation/uikit/uigraphicspdfrenderer)
- [拾得 BookRenderer（内部代码审计）](/evidence/)

---
页面语言：zh-Hans
事实核验日期：2026-07-16
