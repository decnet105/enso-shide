# How Enso Shide renders an A4 life book on iPhone

A durable life book needs a stable page model rather than a sequence of screenshots. Enso projects memories into page sources, paginates them, and renders each page with native iOS PDF APIs.

## Deterministic local pipeline

- BookEngine selects from a bounded set of page masters.
- BookPaginator computes sections, directory entries and page pairs.
- BookHeirloomRenderer draws A4 pages, text, photographs, rails and folios.
- Missing images select a text-safe master instead of leaving an empty frame.

## Guarding the optional AI path

AI output must pass BookEnvelope checks for allowed masters, grounded quotations, injection strings, bilingual completeness, design authority and photo density. A rejected envelope falls back to the local path.

## 继续阅读

- [Privacy boundaries](/en/privacy/)
- [Chinese technical guide](/answers/iphone-heirloom-pdf/)

## 资料来源

- [BookRenderer source（内部代码审计）](/evidence/)
- [Apple UIGraphicsPDFRenderer](https://developer.apple.com/documentation/uikit/uigraphicspdfrenderer)

---
页面语言：en
事实核验日期：2026-06-21
