# Local-first does not mean network-free

Privacy statements must map to actual data paths. Enso's core private models are authoritative on the device, while the current build also includes account, public-content, online companion, AI book and legacy sync paths.

## On-device authority

- Memory stores text, dates, media references, mood, places and stamped snapshots.
- Profile, Keepsake and CompanionState are stored in the local SwiftData container.
- The deterministic book renderer reads the local memory projection.

## Network-dependent paths

- Registration, login and session handling.
- Read-only public cultural content.
- Online companion responses and the optional AI book path.
- Legacy personal-event synchronization that still requires review.

## 继续阅读

- [Current features](/en/features/)
- [Evidence register](/evidence/)

## 资料来源

- [App entry and login gate（内部代码审计）](/evidence/)
- [Network service implementation（内部代码审计）](/evidence/)

---
页面语言：en
事实核验日期：2026-06-21
