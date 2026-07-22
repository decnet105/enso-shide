# How public claims map to engineering evidence

This page is the fact gate for everything published on the site. Only entries whose evidence status is "verified" may be stated in a definitive voice; everything else must be qualified or withheld.

## Internal audit baseline

This register was updated from a release audit of the private product repository's main branch on 2026-07-16. The private source code is not disclosed because the marketing site is live; public pages give only checkable file responsibilities, boundary conclusions, and audit dates.

> This is an internal engineering verification record. It is not equivalent to a third-party security audit, App Store review, or external certification.

## Claim register

| Claim | Status | Evidence | Allowed wording |
| --- | --- | --- | --- |
| Core Memory uses SwiftData | Verified | Memory.swift / MystoryApp.swift | On-device source of truth |
| On-device A4 PDF generation | Verified | BookRenderer.swift | On-device book making |
| Chinese and English content fields | Verified | Memory.swift / BookEnvelope.swift | Supports a Chinese/English content structure |
| Every feature works without any network | Does not hold | APIService.swift | Must not be published |
| Public v1 requires no account | Verified | MystoryApp.swift / Release build conditions | No Ensō account required |
| Cost-bearing online AI is publicly delivered | Does not hold | OnlinePremiumPolicy.swift | Must not be published for v1 |
| Passed an external privacy audit | No evidence | No audit report yet | Must not be published |
| Publicly live on the App Store | Unconfirmed | No official download URL yet | To be confirmed |
| Fixed-query performance metrics | Not measured | No benchmark report yet | Do not publish numbers |

## Publishing rules

- Version, price, ratings, and download links must come from App Store Connect or a public page.
- Performance numbers must include the test device, data scale, sample count, and measurement method.
- Competitive comparisons must cite the competitor's current official documentation and note the verification date.
- Search-engine mention rates must retain the raw answer, model, date, region, and whether the session was signed in.

## Keep reading

- [Privacy boundaries](/en/privacy/)
- [GEO FAQ](/en/faq/)

## Sources

- As-built system overview (internal code audit)
- Accountless app entry (internal code audit)
- Network services (internal code audit)

---
页面语言：en
事实核验日期：2026-07-16
