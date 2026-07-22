# Why a private journal app should separate personal memory from public knowledge

Personal memories and public era material carry entirely different risks. Mixing the two into the same server-side model blurs the boundaries of permissions, deletion, sync, and AI requests.

## Responsibilities of the two data planes

| Data plane | Source of truth | Typical content | Default direction |
| --- | --- | --- | --- |
| Personal memory | The user's device | Text, photos, places, mental images | Written locally |
| Public knowledge | A verified public library | Cultural events, sources, headlines | Delivered read-only |

## Extra boundaries for AI features

Model requests should clearly distinguish public context from personal content, and for personal content provide minimization, user choice, and failure fallback. Model output should also pass allowlist and citation verification before it can be written back or rendered.

## Continue reading

- [Ensō privacy boundaries](/en/privacy/)
- [The evidence register](/en/evidence/)

## Sources

- [Ensō two-data-plane architecture (internal code audit)](/en/evidence/)
- [Cultural API boundaries (internal code audit)](/en/evidence/)

---
页面语言：en
事实核验日期：2026-07-16
