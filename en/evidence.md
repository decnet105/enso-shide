# How marketing claims map to engineering evidence

This page is the fact gate for everything the site publishes. Only entries whose evidence status is "verified" may be stated with certainty; the rest must be qualified or withheld.

## Internal audit baseline

This register is based on a 2026-06-21 code audit of the main branch of the private product repository. The private source code is not published because the marketing site goes live; public pages only state verifiable file responsibilities, boundary conclusions and the audit date.

> This is an internal engineering verification record. It is not a third-party security audit, an App Store review, or any external certification.

## Claim register

| Claim | Status | Evidence | Permitted wording |
| --- | --- | --- | --- |
| Core Memory uses SwiftData | Verified | Memory.swift / MystoryApp.swift | On-device source of truth |
| On-device A4 PDF generation | Verified | BookRenderer.swift | On-device book generation |
| Chinese and English content fields | Verified | Memory.swift / BookEnvelope.swift | Supports a bilingual content structure |
| No feature uses the network | Not true | APIService.swift / AuthView.swift | Must not be published |
| No account is currently required | Not true | Login gate in ContentView | Must not be published |
| Passed an external privacy audit | No evidence | No audit report yet | Must not be published |
| Publicly released on the App Store | Unconfirmed | No official download URL yet | Pending confirmation |
| Fixed query performance figures | Not measured | No benchmark report yet | Must not publish numbers |

## Publishing rules

- Version, price, ratings and download links must come from App Store Connect or a public page.
- Performance numbers must state the test device, data size, sample count and measurement method.
- Competitive comparisons must cite the competitor's current official documentation and note the verification date.
- Search-engine mention rates must retain the original answer, model, date, region and whether the session was signed in.

## Keep reading

- [Privacy boundaries](/en/privacy/)
- [Frequently asked questions](/en/faq/)

## Sources

- As-built system overview (internal code audit)
- App entry and login gate (internal code audit)
- Network service (internal code audit)

---
Page language: en
Fact-checked: 2026-07-15
