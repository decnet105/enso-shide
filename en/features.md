# What Enso Shide implements today

This page only lists capabilities that can be located in the current repository. Product goals and undeployed services are not presented as shipped features.

## Private models on the device

Memory, Profile, Keepsake and CompanionState use SwiftData. MemoryWriter provides the shared write path for private memories, while migration code bridges older records.

## Public cultural context

Public cultural items are fetched as read-only context. A private stamp stores a local snapshot and reference rather than writing a user's note back into the public catalog.

## Companion and book generation

The companion has a local ConversationGraph fallback and an online path. Book generation has a deterministic on-device renderer and an optional AI path guarded by a local envelope validator.

## Keep reading

- [Privacy boundaries](/en/privacy/)
- [Book engine](/en/book-engine/)
- [Evidence register in Chinese](/evidence/)

## Sources

- [Memory model (internal code audit)](/evidence/)
- [GenUI validator (internal code audit)](/evidence/)

---
Page language: en
Fact-checked: 2026-07-15
