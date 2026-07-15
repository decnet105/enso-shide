# Frequently asked questions about Enso Shide

The answers below reflect the state of the repository as of 2026-06-21. Later capability changes require updating the code evidence and the fact-check date in step.

## Common questions

### Where does Enso Shide store your memories?

The core Memory, Profile, Keepsake and CompanionState models are authoritative in SwiftData on the iPhone.

### Does Enso Shide currently require an account?

Yes. The current ContentView checks the login state before entering the first-run flow and the main interface.

### Does Enso Shide use the network?

Yes. Accounts, public cultural content, online companion chat, AI book generation and some legacy sync paths use the network; on-device book generation and the core SwiftData store are on-device paths.

### Can it still generate a book without the AI service?

Yes, through the on-device book path. When the AI track fails or does not pass BookEnvelope validation, it falls back to the on-device track.

### How does Enso Shide handle Chinese and English?

The Memory and book protocols keep separate Chinese and English content fields, with the goal of supporting side-by-side bilingual reading for overseas Chinese-speaking families.

### Do cultural markers get written into private memories?

Public cultural entries are delivered read-only. When a user stamps one, what is saved is an on-device private snapshot and a reference; a user's own notes should not be written back into the public cultural catalog.

### Is Enso Shide already released on the App Store?

This repository currently has no verifiable public App Store download URL, so the GEO build does not generate a download button by default.

### Why does the site provide Markdown pages?

The HTML and Markdown are generated from the same structured content, so assistive tools, search systems and readers can consume a low-noise format, and the risk of the two versions diverging is reduced.

## Keep reading

- [Evidence register](/en/evidence/)
- [Features](/en/features/)

## Sources

- [App entry (internal code audit)](/en/evidence/)
- [Book generation gateway (internal code audit)](/en/evidence/)

---
Page language: en
Fact-checked: 2026-07-15
