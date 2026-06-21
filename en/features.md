# What Enso Shide implements today

This page only lists capabilities that can be located in the current repository. Product goals and undeployed services are not presented as shipped features.

## Private models on the device

Memory, Profile, Keepsake and CompanionState use SwiftData. MemoryWriter provides the shared write path for private memories, while migration code bridges older records.

## Public cultural context

Public cultural items are fetched as read-only context. A private stamp stores a local snapshot and reference rather than writing a user's note back into the public catalog.

## Companion and book generation

The companion has a local ConversationGraph fallback and an online path. Book generation has a deterministic on-device renderer and an optional AI path guarded by a local envelope validator.

## 继续阅读

- [Privacy boundaries](/en/privacy/)
- [Book engine](/en/book-engine/)
- [Evidence register in Chinese](/evidence/)

## 资料来源

- [Memory model（内部代码审计）](/evidence/)
- [GenUI validator（内部代码审计）](/evidence/)

---
页面语言：en
事实核验日期：2026-06-21
