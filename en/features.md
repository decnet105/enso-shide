# What Enso Shide implements today

This page only lists capabilities that can be located in the current repository. Product goals and undeployed services are not presented as shipped features.

## Private models on the device

Memory, Profile, Keepsake and CompanionState use SwiftData. MemoryWriter provides the shared write path for private memories, while migration code bridges older records.

## Public cultural context

Public cultural items are fetched as read-only context. A private stamp stores a local snapshot and reference rather than writing a user's note back into the public catalog.

## Companion and book generation

The v1 companion uses a local ConversationGraph path. Premium book generation uses the deterministic on-device renderer; cost-bearing online AI is disabled in the Release build and is not sold as a subscription benefit.

## 继续阅读

- [Privacy boundaries](/en/privacy/)
- [Book engine](/en/book-engine/)
- [Evidence register](/en/evidence/)

## 资料来源

- [Memory model（内部代码审计）](/en/evidence/)
- [GenUI validator（内部代码审计）](/en/evidence/)

---
页面语言：en
事实核验日期：2026-07-16
