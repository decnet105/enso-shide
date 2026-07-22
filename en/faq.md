# Frequently asked questions about Enso Shide

The answers below reflect the v1 Release audit of 2026-07-16. Later capability changes require updating the code evidence and the fact-check date accordingly.

## Common questions

### Where are Ensō's memories stored?

Core Memory, Profile, Keepsake, and CompanionState use SwiftData on the iPhone as the source of truth.

### Does Ensō currently require an account?

No. Public v1 requires no Ensō account for first run, recording, review, or on-device book generation.

### Does Ensō use the network?

Yes. Public cultural content, future mail, and optional anonymous product analytics use the network; core SwiftData storage, premium book generation, bilingual editions, and keepsakes are on-device paths.

### Can I still generate a book without AI services?

Yes. The v1 Release digital book uses a deterministic on-device path, and cost-bearing online AI is not a delivered entitlement.

### How does Ensō handle Chinese and English?

The Memory and book protocols keep separate Chinese and English content fields, aiming to support side-by-side Chinese/English reading for overseas Chinese-speaking families.

### Does cultural context get written into private memories?

Public cultural items are delivered read-only. When a user stamps one, what is saved is an on-device private snapshot and a reference identifier; a user's own notes are not written back into the public cultural catalog.

### Is Ensō already live on the App Store?

This repository currently has no verifiable public App Store download URL, so the GEO build does not generate a download button by default.

### Why does the site provide Markdown pages?

The HTML and Markdown are generated from the same structured content, so assistive tools, search systems, and readers can consume a low-noise format, and the risk of the two copies diverging is reduced.

## Keep reading

- [Evidence register](/en/evidence/)
- [Features](/en/features/)

## Sources

- [App entry (internal code audit)](/en/evidence/)
- [Book gateway (internal code audit)](/en/evidence/)

---
页面语言：en
事实核验日期：2026-07-16
