# Why a private journal separates personal memory from public knowledge

Personal memories and public historical material carry very different risks. Mixing them into a single server-side model blurs the boundaries of authorization, deletion, synchronization and AI requests.

## Responsibilities of the two data planes

| Data plane | Source of truth | Typical content | Default direction |
| --- | --- | --- | --- |
| Personal memory | The user's device | Text, photos, places, mood imagery | Written locally |
| Public knowledge | A verified public catalog | Cultural events, sources, titles | Delivered read-only |

## The extra boundary for AI features

Model requests should clearly separate public context from personal content, and for personal content should provide minimization, user choice and a failure fallback. Model output should also pass allow-list and citation checks before it is written back or rendered.

## Keep reading

- [Enso Shide privacy boundaries](/en/privacy/)
- [Evidence register](/en/evidence/)

## Sources

- [Enso Shide two-plane architecture (internal code audit)](/en/evidence/)
- [Cultural API boundary (internal code audit)](/en/evidence/)

---
Page language: en
Fact-checked: 2026-07-15
