# How to generate a long-lasting memory PDF on-device on iPhone

A long-lasting memory PDF needs a stable page model, not just a printout of what is on screen. The most important design decision is keeping content, pagination, and drawing independent of one another.

## A recommended six-stage pipeline

- Project memories into page material that is independent of the UI.
- Select from a limited set of master layouts based on photo count and text density.
- Precompute chapters, the table of contents, and facing-page pairings.
- Reserve continuation pages for long text; never truncate the body.
- Downsample photos while preserving their aspect ratio.
- Draw page by page with the native PDF renderer and keep regression samples.

## How Ensō implements this

Ensō uses BookEngine for layout selection, BookPaginator for pagination, and BookHeirloomRenderer for drawing. When images are missing it falls back to image-free master layouts; AI-track output must pass BookEnvelope validation, and on failure the entire book falls back.

## Continue reading

- [The full book engine overview](/en/book-engine/)
- [Preserving Chinese memories for overseas families](/en/answers/chinese-family-memory/)

## Sources

- [Apple UIGraphicsPDFRenderer](https://developer.apple.com/documentation/uikit/uigraphicspdfrenderer)
- [Ensō BookRenderer (internal code audit)](/en/evidence/)

---
页面语言：en
事实核验日期：2026-07-16
