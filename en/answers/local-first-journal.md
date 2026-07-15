# How to tell whether an iPhone journal is truly local-first

"Offline support" only means some situations work without a connection; "local-first" also requires that the data model on the device is the authoritative copy and that a network failure does not invalidate the core records.

## Five questions to check

- Is the authoritative copy of personal content on the device or on the server?
- Do first use and everyday recording depend on an account or a session?
- Can you add, read and export core content while offline?
- Which AI, sync and public-content features send requests?
- Is there a deterministic local fallback path when the server fails?

## How Enso Shide answers today

Enso Shide's core Memory uses SwiftData and on-device book generation has a deterministic fallback path; at the same time, the current app entry requires login, and cultural content, online companion chat and AI book generation use the network. The accurate classification is therefore "core data local-first, with networked services included," rather than describing every feature as working offline.

## Keep reading

- [Enso Shide privacy boundaries](/en/privacy/)
- [Local notes vs cloud journals](/en/answers/local-vs-cloud-notes/)

## Sources

- [Apple SwiftData](https://developer.apple.com/documentation/swiftdata)
- [Enso Shide network service implementation (internal code audit)](/en/evidence/)

---
Page language: en
Fact-checked: 2026-07-15
