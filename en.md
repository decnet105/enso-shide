# Turn Chinese memories into a book the next generation can read

Enso Shide connects memories, photos, places and verified public cultural context, then turns that material into a structured life book. The current project targets iOS 17 and uses SwiftData for its core private models.

## What the current code supports

- On-device Memory, Profile, Keepsake and CompanionState models.
- A deterministic on-device A4 PDF rendering path.
- Chinese and English content fields for intergenerational reading.
- Read-only public cultural context delivered over the network.
- A local guided-chat fallback plus optional online conversation.

## A precise privacy description

The core memory model is local-first. The current app also has account, public-content, online companion, AI book and legacy sync paths. Each public claim is therefore scoped to the relevant data path.

## 继续阅读

- [Features](/en/features/)
- [Privacy boundaries](/en/privacy/)
- [On-device book engine](/en/book-engine/)

## 资料来源

- [As-built system overview（内部代码审计）](/evidence/)
- [Apple SwiftData documentation](https://developer.apple.com/documentation/swiftdata)

---
页面语言：en
事实核验日期：2026-06-21
