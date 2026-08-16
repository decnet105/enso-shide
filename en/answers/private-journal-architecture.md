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

[Download Ensō on the App Store](https://apps.apple.com/app/apple-store/id6787128369?pt=129013055&ct=web&mt=8)

## Sources

- [Ensō two-data-plane architecture (internal code audit)](/en/evidence/)
- [Cultural API boundaries (internal code audit)](/en/evidence/)

Follow: X https://x.com/ensoshide · Instagram https://www.instagram.com/ensoshide · YouTube https://www.youtube.com/@EnsoShide

---
页面语言：en
事实核验日期：2026-08-16
