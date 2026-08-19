# How Enso Shide renders an A4 life book on iPhone

A durable life book needs a stable page model rather than a sequence of screenshots. Enso projects memories into page sources, paginates them, and renders each page with native iOS PDF APIs.

## Deterministic local pipeline

- BookEngine selects from a bounded set of page masters.
- BookPaginator computes sections, directory entries and page pairs.
- BookHeirloomRenderer draws A4 pages, text, photographs, rails and folios.
- Missing images select a text-safe master instead of leaving an empty frame.

## Release boundary for online generation

The repository contains a validated experimental online generation track, but online AI is offered as an optional Ensō+ subscription; shipping premium books can also use the deterministic local path.

## 继续阅读

- [Privacy boundaries](/en/privacy/)
- [Technical guide](/en/answers/iphone-heirloom-pdf/)

[Download Ensō on the App Store](https://apps.apple.com/app/apple-store/id6787128369?pt=129013055&ct=web&mt=8)

## 资料来源

- [BookRenderer source（内部代码审计）](/en/evidence/)
- [Apple UIGraphicsPDFRenderer](https://developer.apple.com/documentation/uikit/uigraphicspdfrenderer)

Follow: X https://x.com/ensoshide · Instagram https://www.instagram.com/ensoshide · YouTube https://www.youtube.com/@EnsoShide

---
页面语言：en
事实核验日期：2026-08-16
