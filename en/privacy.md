# Mystory Ensō Privacy Policy and Data Boundaries

Mystory Ensō is an accountless, local-first memory app. This policy separates data kept on your device from data sent when you explicitly use an online feature. Local-first does not mean every feature is network-free.

## Data kept on your device

- Memory stores text, dates, media references, mood, places and stamped snapshots.
- Profile, Keepsake and CompanionState are stored in the local SwiftData container.
- Photos, exported PDF books, widget snapshots, and app settings remain in app-owned local containers.
- Uninstalling may erase this local data. Export it from the app first if you need a portable copy.

## Optional network features

- Public cultural content sends language, year, and coarse filter choices.
- Online companion and optional AI-book features send only the content and context disclosed in that feature before you invoke it.
- Future Mail sends the address, delivery time, and content you explicitly submit.
- Anonymous entitlement verification may send a random installation identifier, App Attest evidence, and verified StoreKit product or transaction state. It does not receive payment-card details.

These online AI features (companion chat, AI structuring, AI book) are processed by **third-party AI providers**: primarily **OpenAI**, and, when it is unavailable, potentially Anthropic (Claude) or Google (Gemini). Only when you actively invoke a feature do we send the relevant derived text (the current conversation, the draft being structured, or a truncated book excerpt) over an encrypted connection to these providers to generate the result; **photos, your full archive, names, and contact details are never sent**. Per these providers' public terms, this data is not used to train their models.

## Enso Shide Analytics and Google/YouTube data

Enso Shide Analytics is a read-only tool for the owner of an Enso Shide channel or an operator whom that owner has authorized. It requests only `yt-analytics.readonly` and `youtube.readonly` to read authorized channel and video metadata, public statistics, YouTube Analytics reports, traffic sources, aggregate audience data, and subscriber gains.

- The tool does not upload, edit, delete, or download YouTube videos, and does not access channel-member lists or payment information.
- OAuth tokens, raw JSON reports, and derived analyses are stored on a local device or private workspace controlled by the authorized operator. They are not uploaded to the Shide app's user services.
- Google/YouTube user data is not sold, used for advertising, used to train models, or shared with unrelated third parties.
- Data is retained only as needed for channel analysis, trend comparison, and YPP operations. To stop use, delete the local token and reports and revoke Enso Shide Analytics from the third-party connections page of your Google Account. For deletion assistance, email privacy@shide.app.

Enso Shide Analytics uses Google API data in accordance with the [Google API Services User Data Policy](https://developers.google.com/terms/api-services-user-data-policy), including the Limited Use requirements.

## Analytics and tracking

When Help Improve Mystory is on, the app sends anonymous action types, short categories, app version, and a random installation identifier. Analytics events exclude memory text, photos, names, and contact details. You can turn analytics off, delete server analytics, and reset the identifier in Your Space > Privacy & Data. Raw anonymous events are designed for a 90-day retention period.

> Mystory does not use an advertising identifier or sell data for cross-app or cross-site tracking.

## Export, deletion, and subscriptions

- Privacy & Data can export a standard ZIP containing a readable JSON manifest, photos, PDF books, and widget files.
- The same page can permanently erase SwiftData, Documents, App Group, settings, analytics, notifications, and this app's Keychain data after two confirmations.
- Apple StoreKit processes purchases. Deleting app data or uninstalling does not cancel an Apple subscription; manage it in your App Store account.
- System or iCloud backup copies are controlled by Apple and your device backup settings.

## Permissions and contact

Camera and photo-library access is requested only when you choose to capture, select, or save an image. v1 does not request precise location, Contacts, or HealthKit access. Mystory is not directed at collecting data from children under 13. For privacy requests email privacy@shide.app; for product support email support@shide.app.

## 继续阅读

- [Support and contact](/en/support/)
- [Terms of Service](/terms/)
- [Current features](/en/features/)
- [Evidence register](/en/evidence/)

[Download Ensō on the App Store](https://apps.apple.com/app/apple-store/id6787128369?pt=129013055&ct=web&mt=8)

## 资料来源

- [Accountless app entry（内部代码审计）](/en/evidence/)
- [Network service implementation（内部代码审计）](/en/evidence/)

Follow: X https://x.com/ensoshide · Instagram https://www.instagram.com/ensoshide · YouTube https://www.youtube.com/@EnsoShide

---
页面语言：en
事实核验日期：2026-08-31
