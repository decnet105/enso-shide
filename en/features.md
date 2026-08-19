# What Enso Shide implements today

This page only lists capabilities that can be located in the current repository. Product goals and undeployed services are not presented as shipped features.

## Private models on the device

Memory, Profile, Keepsake and CompanionState use SwiftData. MemoryWriter provides the shared write path for private memories, while migration code bridges older records.

## Public cultural context

Public cultural items are fetched as read-only context. A private stamp stores a local snapshot and reference rather than writing a user's note back into the public catalog.

## Companion and book generation

The v1 companion uses a local ConversationGraph path. Premium book generation uses the deterministic on-device renderer; online AI is an optional Ensō+ subscription capability, invoked only when you choose to; the deterministic on-device path works without it.

## Seasonal cultural features and deep-link sharing

Ensō publishes seasonal cultural features tied to the calendar (such as Mid-Autumn), gathering that season's public cultural landmarks into a single entry point. Features and individual cultural events support Universal Link deep links, so tapping one opens directly to the matching page inside the app.

## Book styles and languages

The on-device and AI dual-track book supports several author-voice styles and layouts. Books cover side-by-side Chinese–English, and also offer Chinese-only, English-only, and Japanese-only editions, so elders and the next generation can each read the version that suits them.

## 继续阅读

- [Privacy boundaries](/en/privacy/)
- [Book engine](/en/book-engine/)
- [Evidence register](/en/evidence/)

[Download Ensō on the App Store](https://apps.apple.com/app/apple-store/id6787128369?pt=129013055&ct=web&mt=8)

## 资料来源

- [Memory model（内部代码审计）](/en/evidence/)
- [GenUI validator（内部代码审计）](/en/evidence/)

Follow: X https://x.com/ensoshide · Instagram https://www.instagram.com/ensoshide · YouTube https://www.youtube.com/@EnsoShide

---
页面语言：en
事实核验日期：2026-08-16
