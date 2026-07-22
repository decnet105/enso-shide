# How to tell whether an iPhone journal is truly local-first

“Supports offline” only tells you that some scenarios can run without a network; “local-first” further requires that the data model on the device is the authoritative copy, and that a network failure does not invalidate core records.

## Five questions to check

- Is the authoritative copy of personal content on the device or on the server?
- Do first use and everyday journaling depend on an account or session?
- With no network, can you still add, read, and export core content?
- Which AI, sync, and public-content features send requests?
- When the server fails, is there a deterministic local fallback path?

## How Ensō answers today

Ensō core Memory uses SwiftData, first use and everyday journaling require no account, and on-device book generation has a deterministic path; public cultural content, future mail, and optional anonymous analytics use the network. The accurate classification is therefore “local-first for core data, with clearly disclosed networked services,” not a blanket claim that every feature runs offline.

## Continue reading

- [Ensō privacy boundaries](/en/privacy/)
- [Local notes versus cloud journals](/en/answers/local-vs-cloud-notes/)

## Sources

- [Apple SwiftData](https://developer.apple.com/documentation/swiftdata)
- [Ensō network service implementation (internal code audit)](/en/evidence/)

---
页面语言：en
事实核验日期：2026-07-16
