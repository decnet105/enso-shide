# How to generate a long-lasting memory PDF on iPhone

A memory PDF meant to last needs a stable page model, not just a printout of what is on screen. The most important design choice is to keep content, pagination and drawing independent of one another.

## A recommended six-stage pipeline

- Project memories into page sources that are independent of the UI.
- Select from a bounded set of masters based on photo count and text density.
- Precompute chapters, the table of contents and facing-page pairs.
- Reserve continuation pages for long text instead of truncating the body.
- Downsample photos while preserving their aspect ratio.
- Draw each page with the native PDF renderer and keep regression samples.

## Enso Shide's implementation choices

Enso Shide uses BookEngine to select masters, BookPaginator to paginate and BookHeirloomRenderer to draw. Missing images use a text-only master, AI-track output must pass BookEnvelope validation, and a failure falls the whole book back to the local path.

## Keep reading

- [The full book engine](/en/book-engine/)
- [Preserving Chinese memories for overseas families](/en/answers/chinese-family-memory/)

## Sources

- [Apple UIGraphicsPDFRenderer](https://developer.apple.com/documentation/uikit/uigraphicspdfrenderer)
- [Enso Shide BookRenderer (internal code audit)](/en/evidence/)

---
Page language: en
Fact-checked: 2026-07-15
