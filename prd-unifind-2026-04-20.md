# Product Requirements Document
# UniFind — Lost & Found App for University Students

**Version:** 1.0
**Date:** 2026-04-20
**Status:** Draft — Awaiting Stakeholder Review
**Author:** Product Team

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Problem Statement](#2-problem-statement)
3. [Target Users](#3-target-users)
4. [Business Objectives](#4-business-objectives)
5. [Proposed Solution](#5-proposed-solution)
6. [Tech Stack](#6-tech-stack)
7. [Functional Requirements](#7-functional-requirements)
8. [Non-Functional Requirements](#8-non-functional-requirements)
9. [Epics & User Stories](#9-epics--user-stories)
10. [Dependencies & Constraints](#10-dependencies--constraints)
11. [Risks & Mitigations](#11-risks--mitigations)
12. [Traceability Matrix](#12-traceability-matrix)
13. [Success Metrics & KPIs](#13-success-metrics--kpis)
14. [Out of Scope (v1)](#14-out-of-scope-v1)

---

## 1. Executive Summary

UniFind is a mobile-first lost and found platform built exclusively for university students and campus staff. Students who lose or find items on campus can report, search, and reclaim belongings through a verified, safe, and campus-specific digital channel — replacing fragmented solutions like Facebook groups, notice boards, and paper forms at the security office.

The MVP targets a single university campus and must be delivered within one academic semester (~4 months). Success is measured by achieving a ≥ 60% item recovery rate and enrolling ≥ 40% of students as active users within 12 months of launch.

---

## 2. Problem Statement

University campuses are large, busy environments where students frequently lose personal belongings — student IDs, keys, wallets, laptops, water bottles, AirPods, and more. Current solutions (Facebook groups, notice boards, security office drop-offs) are fragmented, slow, and unreliable. Students have no unified, searchable, campus-specific platform to report or browse lost/found items, leading to permanent loss of valuable belongings and unnecessary stress.

**Core Pain Points:**
- No single source of truth for campus lost & found reports
- Finders and losers cannot find each other efficiently
- Security offices manage physical depots with no digital integration
- Privacy risks from posting personal details on public social media groups
- No structured claim or verification process to confirm item ownership

---

## 3. Target Users

| User Segment | Description |
|---|---|
| **Item Loser** | A student who has lost a personal item on campus and wants to report it and find it quickly |
| **Item Finder** | A student who has found an item on campus and wants to return it to the rightful owner |
| **Campus Admin / Security Officer** | University staff who manage a physical lost & found depot and need a digital dashboard |

---

## 4. Business Objectives

| ID | Objective | Timeframe |
|---|---|---|
| BO-01 | Increase item recovery rate on campus to ≥ 60% | Within 6 months of launch |
| BO-02 | Achieve 40% of enrolled students as active users | Within 12 months of launch |
| BO-03 | Reduce time-to-reunite (item lost → returned) to under 48 hours for matched items | Ongoing from launch |
| BO-04 | Provide a safe, university-verified platform free from spam, harassment, and external users | From day one |

---

## 5. Proposed Solution

**UniFind** is a cross-platform mobile application (iOS + Android) that provides:

1. **University-verified accounts** — Authentication via university SSO ensures only enrolled students and staff can access the platform
2. **Structured item reporting** — Standardised forms with photos, categories, tags, and map-based location tagging
3. **Smart search & matching** — Full-text search with filters plus an automated matching engine that pairs lost and found reports
4. **Secure in-app messaging** — Proxied chat between finders and losers, moderated to prevent harassment and privacy leaks
5. **Verified claim flow** — A formal ownership verification process before items are handed over
6. **Admin dashboard** — A web companion for security officers to manage the physical depot and moderate content

---

## 6. Tech Stack

| Layer | Technology | Rationale |
|---|---|---|
| Mobile | React Native or Flutter | Cross-platform iOS + Android from single codebase |
| Backend | Node.js (Express) or Django REST | REST API; proven for CRUD-heavy mobile backends |
| Database | PostgreSQL | Relational model fits users, items, claims, messages |
| Auth | University SSO (OAuth 2.0 / SAML) + JWT | University-verified access; JWT for mobile session management |
| File Storage | AWS S3 or Firebase Storage | Scalable object storage for item photos |
| Push Notifications | Firebase Cloud Messaging (FCM) | Cross-platform push to iOS and Android |
| Search | Elasticsearch or PostgreSQL full-text search | Keyword and fuzzy search across item listings |
| Maps | Google Maps SDK | Campus map integration for item location tagging |
| CI/CD | GitHub Actions | Automated lint, test, build, and deploy pipeline |

---

## 7. Functional Requirements

### 7.1 Authentication

**FR-001: MUST** — The system shall restrict account creation and login to users with a valid university email address or university SSO credentials.
Acceptance Criteria:
- A user attempting to register with a non-university email domain is rejected with a clear error message.
- A user who successfully authenticates via university SSO or university email receives an active session token.
- A user whose university account is deactivated or suspended cannot log in.
- Session tokens expire after a defined inactivity period, requiring the user to re-authenticate.

**FR-002: MUST** — The system shall maintain a user profile containing the account holder's display name, faculty or department, and contact preferences.
Acceptance Criteria:
- A newly registered user is prompted to complete their profile before posting any item.
- Profile fields are pre-populated where data is available from SSO attributes.
- A user can update their display name and contact preferences at any time from the profile screen.
- Personally identifiable information beyond display name is not surfaced publicly to other users.

**FR-003: SHOULD** — The system shall allow a user to deactivate their own account, which removes their active listings and suppresses their profile from search results.
Acceptance Criteria:
- A deactivated account's open lost or found listings are automatically closed.
- Other users cannot initiate new messages to a deactivated account.
- The deactivated user can reactivate by logging back in within a defined retention window.

---

### 7.2 Search & Discovery

**FR-004: MUST** — The system shall provide a keyword search over item titles, descriptions, and tags that returns ranked results in under two seconds.
Acceptance Criteria:
- A search query matching keywords in a listing title or description returns that listing in the result set.
- Results are returned within two seconds for a dataset of up to 10,000 active listings.
- An empty search query returns a paginated feed of all active listings sorted by most recent.
- A search with no matching results displays a clear empty-state message with suggested actions.

**FR-005: MUST** — The system shall allow users to filter search results by item category, date range, and campus location.
Acceptance Criteria:
- Applying a category filter returns only listings assigned to that category.
- Applying a date range filter returns only listings reported within that range.
- Multiple filters applied simultaneously return the intersection of matching listings.
- Active filters are visually indicated and can each be cleared individually.

**FR-006: SHOULD** — The system shall display item listings on an interactive campus map view, showing pins at the reported loss or discovery location.
Acceptance Criteria:
- Each listing with a location attached appears as a pin on the campus map.
- Tapping a pin opens a summary card for the corresponding listing.
- The map view respects the same active filters applied in the list view.
- A user can report a location by dropping a pin on the map during item submission.

---

### 7.3 Reporting (Lost & Found Items)

**FR-007: MUST** — The system shall allow an authenticated user to submit a lost item report containing a title, category, description, last-known location, and date lost.
Acceptance Criteria:
- A submission without a title or category is rejected with inline validation errors.
- A successfully submitted report appears in the public listing feed within 60 seconds.
- The reporting user receives an in-app confirmation with the listing ID upon submission.
- The system accepts up to five photos per listing, each no larger than 10 MB.

**FR-008: MUST** — The system shall allow an authenticated user to submit a found item report containing a title, category, description, discovery location, and date found.
Acceptance Criteria:
- A found item report follows the same mandatory field rules as a lost item report.
- The system distinguishes found listings from lost listings with a clear visual indicator in the feed.
- A submitted found report is visible to all authenticated users browsing or searching.
- The finder can choose to mark a sensitive detail (e.g., identifying markings) as visible only to claimants.

**FR-009: SHOULD** — The system shall support a predefined set of item categories and allow users to attach multiple tags to a listing to improve discoverability.
Acceptance Criteria:
- The category list includes at minimum: Electronics, Accessories, Clothing, Documents, Keys, Bags, and Other.
- A user can select one category and up to five tags per listing.
- Tags entered by users are matched against a suggested vocabulary to reduce duplicates.
- Listings can be filtered by both category and individual tags simultaneously.

**FR-010: MUST** — The system shall allow the listing owner to edit or close their own listing at any time.
Acceptance Criteria:
- The listing owner can update any field of their listing after submission.
- Closing a listing marks it as resolved and removes it from the active search feed.
- Edits to a listing are timestamped and the most recent update time is visible on the listing detail.
- A closed listing remains accessible via direct link for 30 days before archival.

---

### 7.4 Messaging

**FR-011: MUST** — The system shall provide an in-app messaging channel between the owner of a lost listing and the submitter of a found listing, and vice versa.
Acceptance Criteria:
- A user can initiate a message thread from any active listing detail page.
- Message threads are scoped to a specific listing pair and cannot be used for general communication.
- Both parties receive an in-app and push notification when a new message arrives.
- A user cannot initiate a message with themselves.

**FR-012: MUST** — The system shall prevent users from sharing external contact information (phone numbers, email addresses, social media handles) within the messaging system.
Acceptance Criteria:
- A message containing a detectable phone number, email address, or URL is blocked before delivery with a warning to the sender.
- The blocked message is logged for moderation review without notifying the recipient.
- A user who repeatedly attempts to send blocked content is flagged for admin review.
- Legitimate messages with no restricted content are delivered with no added latency.

**FR-013: SHOULD** — The system shall allow either party in a message thread to report the conversation as abusive or harassing.
Acceptance Criteria:
- A report option is accessible from within the message thread without leaving the conversation.
- Submitting a report captures the thread context and routes it to the admin moderation queue.
- The reporting user receives confirmation that their report was received.
- The reported user is not notified that a report has been filed against them.

---

### 7.5 Claims

**FR-014: MUST** — The system shall provide a formal claim flow that allows a user to assert ownership of a found item by providing a written ownership justification.
Acceptance Criteria:
- A claim can only be submitted by a user who is not the finder of the item.
- The claim form requires a written description of proof of ownership (e.g., serial number, unique markings).
- A submitted claim notifies the finder and the claimant via in-app and push notification.
- A listing can have multiple pending claims, each visible only to the finder and the respective claimant.

**FR-015: MUST** — The system shall allow the finder to accept or reject each claim, and upon acceptance, mark the listing as resolved.
Acceptance Criteria:
- Accepting a claim closes the listing and notifies all other pending claimants that the item has been claimed.
- Rejecting a claim notifies the rejected claimant and keeps the listing open.
- A resolved listing is removed from the active search feed and labelled as "Reunited."
- The finder cannot reopen a listing after accepting a claim without admin intervention.

**FR-016: SHOULD** — The system shall provide a claim verification step where the admin can request additional proof of ownership before the finder is allowed to hand over an item held at the security depot.
Acceptance Criteria:
- When an item is checked into the depot, the admin can flag the listing as "Depot-held."
- For depot-held items, the system requires admin sign-off before a claim is marked as accepted.
- The admin can request additional documentation from the claimant via the in-app messaging channel.
- A claimant is notified of the depot verification requirement when they submit a claim on a depot-held listing.

---

### 7.6 Notifications & Admin

**FR-017: COULD** — The system shall provide an admin dashboard that displays aggregate metrics including total active listings, claim success rate, and average time-to-resolution.
Acceptance Criteria:
- The dashboard is accessible only to accounts with the admin role.
- Metrics are updated at least once every 24 hours.
- The admin can filter metrics by date range and item category.
- The dashboard displays at minimum: total lost reports, total found reports, total resolved listings, and median time-to-resolution.

**FR-018: COULD** — The system shall allow admins to remove any listing or message that violates community guidelines, with a mandatory reason recorded internally.
Acceptance Criteria:
- An admin can remove a listing or message from any moderation queue or search result.
- A removal action requires the admin to select or enter a reason before confirming.
- The removed content is soft-deleted and retained for audit purposes for a minimum of 90 days.
- The content owner receives an in-app notification that their listing or message was removed, without disclosing admin identity.

**FR-019: COULD** — The system shall allow admins to manage a physical depot inventory by logging items that have been physically handed in to the security office.
Acceptance Criteria:
- An admin can link a physically held item to an existing found listing.
- Depot-logged items display a "Held at Security Office" badge on the public listing.
- The admin can update the depot status (received, claimed, disposed) and the status change is timestamped.
- A student browsing a depot-held listing can see the office location and collection hours.

**FR-020: SHOULD** — The system shall send automated push notifications to users when a newly submitted listing closely matches a previously submitted lost or found report they own.
Acceptance Criteria:
- A notification is sent within five minutes of a new listing being published if a match is detected.
- The notification links directly to the matched listing detail page.
- Match detection considers item category, keywords in title and description, and reported campus location.
- A user can disable match notifications from their profile settings without disabling all notifications.

**FR-021: MUST** — The system shall send a push notification to the listing owner when a claim is submitted, a message is received, or their listing is resolved.
Acceptance Criteria:
- A push notification is delivered within 60 seconds of the triggering event.
- Users who have disabled push notifications still receive an in-app notification badge.
- Notification content does not expose personally identifiable information about the other party.
- A user can manage notification preferences per event type from the profile settings screen.

**FR-022: SHOULD** — The system shall automatically close lost or found listings that have remained open without owner activity for more than 30 days, after issuing a 72-hour warning notification.
Acceptance Criteria:
- A warning notification is sent to the listing owner 72 hours before automatic closure.
- The owner can extend the listing by confirming it is still active from within the notification or the listing detail.
- If no action is taken, the listing is automatically closed and labelled as "Expired."
- Auto-closed listings are excluded from the active search feed but remain accessible via direct link for 30 days.

---

## 8. Non-Functional Requirements

### Performance

**NFR-001: MUST — Performance — API Response Time**
All REST API endpoints must return responses within an acceptable latency threshold under normal load.
Metric: p95 response time < 200ms for read endpoints (search, browse, item detail); p95 < 500ms for write endpoints (create report, submit claim) under a load of up to 500 concurrent users.
Rationale: Slow search and browse responses directly reduce engagement and make students abandon the platform before finding their items.

**NFR-002: MUST — Performance — Image Upload Throughput**
Item photo uploads to cloud storage must complete within a user-acceptable time window.
Metric: A 5MB image upload must complete in < 10 seconds on a standard 4G mobile connection (minimum 10 Mbps uplink).
Rationale: Photos are the primary evidence for item identification; upload friction causes users to skip photos, degrading match quality.

---

### Security

**NFR-003: MUST — Security — Authentication Enforcement**
Every protected API endpoint must reject requests that lack a valid, non-expired JWT issued after successful university SSO authentication.
Metric: 0% of API calls to protected routes succeed without a valid JWT; token expiry enforced at ≤ 1 hour with refresh token rotation.
Rationale: Restricting access to university-verified users is a core product constraint that prevents spam and protects student data.

**NFR-004: MUST — Security — Transport Encryption**
All data transmitted between the mobile client, backend, and third-party services must be encrypted in transit.
Metric: TLS 1.2 minimum enforced on all connections; TLS 1.3 preferred; HTTP (plaintext) connections refused with a 301 redirect or connection reset.
Rationale: Unencrypted traffic exposes personally identifiable student information and item location data to network-level interception.

**NFR-013: SHOULD — Security — In-App Messaging Content Safety**
Messages sent through the in-app chat must be screened to prevent harassment and the sharing of inappropriate content.
Metric: Automated moderation must flag or block messages containing profanity, phone numbers, or email addresses within 500ms of send; flagged messages must be reviewed or auto-blocked before delivery to the recipient.
Rationale: The key constraint explicitly requires chat to be moderated or proxied to prevent harassment between students.

---

### Reliability

**NFR-005: MUST — Reliability — Service Uptime**
The UniFind backend and mobile app must maintain high availability during the academic day.
Metric: Monthly uptime ≥ 99.5% (allowing ≤ 3.6 hours unplanned downtime per month); planned maintenance windows restricted to 02:00–05:00 local time.
Rationale: Students report and search for items throughout the day; extended downtime directly reduces the item recovery rate tied to BO-01.

**NFR-006: MUST — Reliability — Push Notification Delivery**
Match and claim notifications delivered via Firebase Cloud Messaging must reach users promptly.
Metric: ≥ 95% of FCM notifications delivered within 60 seconds of the triggering server event, measured over a rolling 7-day window.
Rationale: Fast notifications are critical to achieving the BO-03 target of under 48 hours time-to-reunite; delayed alerts let items go unclaimed.

**NFR-016: COULD — Reliability — Offline Graceful Degradation**
The mobile app must remain partially functional when the device has no network connectivity.
Metric: Previously loaded item listings and the user's own reported items must remain viewable for at least 24 hours after the last successful sync; the app must display a clear offline banner within 3 seconds of connectivity loss rather than showing blank screens or crashes.
Rationale: Campus Wi-Fi dead zones are common; crashing or showing empty screens when offline undermines perceived reliability.

---

### Scalability

**NFR-007: MUST — Scalability — Concurrent User Load**
The backend must handle peak concurrent usage at the start and end of semesters without degraded performance.
Metric: System must sustain 500 simultaneous active users with no more than a 20% increase in p95 API latency compared to baseline (50 users); auto-scaling must provision additional capacity within 3 minutes.
Rationale: Campus events and semester start periods produce traffic spikes; failure to scale causes outages exactly when lost-item reports surge.

**NFR-008: SHOULD — Scalability — Database Read Scalability**
The PostgreSQL database must support read-heavy workloads without becoming a bottleneck as the user base grows.
Metric: Read queries must execute in < 100ms at the 95th percentile with up to 10,000 stored item records; read replicas must be provisioned before the user base exceeds 5,000 active users.
Rationale: Browse and search are the most frequent operations; unoptimized queries at scale will make the platform feel unusable.

---

### Privacy & Compliance

**NFR-009: MUST — Privacy/Compliance — Data Residency and Retention**
User personal data and item records must be stored and retained in accordance with applicable data protection regulations.
Metric: All personal data stored in a PDPA/FERPA-compliant data region; resolved item records purged or anonymized within 90 days of closure; user account data deleted within 30 days of account termination request.
Rationale: The university's data governance obligations and PDPA/FERPA compliance are non-negotiable constraints.

**NFR-010: MUST — Privacy/Compliance — Sensitive Data Minimization**
Item listings must not expose the reporter's personal contact details or student ID to other users without explicit consent.
Metric: 0 item listings expose the reporter's email, phone number, or student ID number in any publicly readable API response or UI view; all user-to-user contact must be proxied through the in-app messaging system.
Rationale: Public exposure of student contact details enables harassment, violating key safety constraints.

---

### Usability

**NFR-011: SHOULD — Usability — App Launch Time**
The mobile app must be interactive quickly after the user taps the icon.
Metric: Time-to-interactive (TTI) from cold launch < 3 seconds on a mid-range Android device (Snapdragon 665, 4GB RAM) on a 4G connection.
Rationale: A slow cold start discourages daily habitual use, which is required to achieve the 40% active-user penetration target in BO-02.

**NFR-012: SHOULD — Usability — Search Result Relevance Speed**
Full-text and filtered search across item listings must return results fast enough to feel instantaneous.
Metric: Search results rendered in the UI within 1 second (end-to-end, including network) for keyword queries across a dataset of up to 10,000 items, for 95% of queries.
Rationale: Students abandon slow search tools and revert to scrolling social media groups.

---

### Maintainability

**NFR-014: SHOULD — Maintainability — Test Coverage**
The backend codebase must maintain sufficient automated test coverage to catch regressions before deployment.
Metric: Minimum 80% line coverage on backend business logic enforced in the CI pipeline; any pull request reducing coverage below threshold must be blocked from merging.
Rationale: A small team with a 4-month delivery window cannot afford regression bugs; automated tests are the primary safety net.

**NFR-015: SHOULD — Maintainability — Deployment Pipeline Lead Time**
The CI/CD pipeline must enable rapid, low-risk deployments to production.
Metric: End-to-end pipeline (lint → test → build → deploy to staging) must complete in < 15 minutes; rollback to the previous production build must be executable in < 5 minutes.
Rationale: Fast deploy cycles allow the team to ship bug fixes quickly, directly supporting the BO-01 recovery rate target.

---

## 9. Epics & User Stories

### RICE Prioritization Summary

| Epic ID | Epic Name | Reach | Impact | Confidence | Effort | RICE Score |
|---------|-----------|-------|--------|------------|--------|------------|
| EPIC-01 | User Authentication & Profile | 10 | 3 | 95% | 2 | **14.25** |
| EPIC-02 | Lost & Found Item Reporting | 10 | 3 | 90% | 3 | **9.00** |
| EPIC-03 | Search & Discovery | 9 | 3 | 85% | 3 | **7.65** |
| EPIC-05 | Claim & Verification Flow | 7 | 3 | 80% | 3 | **5.60** |
| EPIC-04 | Matching & Notifications | 8 | 3 | 75% | 4 | **4.50** |
| EPIC-06 | Admin & Moderation Dashboard | 4 | 2 | 85% | 3 | **2.27** |

**RICE Formula:** (Reach × Impact × Confidence) / Effort

---

### EPIC-01 — User Authentication & Profile
**Business Value:** Without verified university identity, the platform cannot guarantee campus-only safety. Frictionless SSO onboarding is the foundational prerequisite for every downstream feature and directly supports BO-04.
**User Segments:** Item Loser, Item Finder, Campus Admin

| Story ID | User Story | Acceptance Criteria (Summary) | Points |
|---|---|---|---|
| EPIC-01-S1 | As a student, I want to sign in with my university SSO so I don't need a separate account | OAuth 2.0/SAML flow; .edu domain validated; JWT issued | 5 |
| EPIC-01-S2 | As a new user, I want to complete a profile so others can identify me | Pre-filled from SSO; required before first post | 3 |
| EPIC-01-S3 | As a student, I want to edit my display name and photo | Changes reflected within 5 min; email read-only | 2 |
| EPIC-01-S4 | As a student on a shared device, I want to sign out securely | Clears JWT and cached data; confirmation prompt | 2 |
| EPIC-01-S5 | As a student, I want to manage which notifications I receive | Per-type toggles; persists across devices | 3 |
| EPIC-01-S6 | As a graduated student, I want to deactivate my account | Open reports anonymised within 24h; confirmation email sent | 3 |
| | **Epic Total** | | **18 pts** |

---

### EPIC-02 — Lost & Found Item Reporting
**Business Value:** The core value loop depends on rich, complete item reports. Quality reports drive BO-01 (≥ 60% recovery) and BO-03 (< 48h time-to-reunite).
**User Segments:** Item Loser, Item Finder

| Story ID | User Story | Acceptance Criteria (Summary) | Points |
|---|---|---|---|
| EPIC-02-S1 | As a Loser, I want to report a lost item with description and location | Required fields validated; appears in feed within 60s | 5 |
| EPIC-02-S2 | As a Finder, I want to report a found item with photos | Up to 5 photos ≤ 10MB; contact details never shown publicly | 5 |
| EPIC-02-S3 | As a reporter, I want to edit my submitted report | Edit badge shown; re-triggers matching engine within 5 min | 3 |
| EPIC-02-S4 | As a reporter, I want to close/resolve my report | Moves to archived state; increments BO-01 recovery counter | 2 |
| EPIC-02-S5 | As a Finder, I want to manage photos on my report | Max 5 photos; can add/replace/delete; last photo cannot be deleted | 3 |
| EPIC-02-S6 | As a reporter, I want to tag my item with categories | Hierarchical category picker; up to 5 custom tags; auto-suggest | 3 |
| | **Epic Total** | | **21 pts** |

---

### EPIC-03 — Search & Discovery
**Business Value:** A campus-aware search experience transforms UniFind from a bulletin board into a reunion tool. Rapid narrowing by location, category, and date drives BO-03.
**User Segments:** Item Loser, Item Finder, Campus Admin

| Story ID | User Story | Acceptance Criteria (Summary) | Points |
|---|---|---|---|
| EPIC-03-S1 | As a Loser, I want to search found reports by keyword | Full-text across title/description/tags; results in < 2s; partial-word match | 5 |
| EPIC-03-S2 | As a Loser, I want to filter by category, date, and location | AND logic across all filters; dismissible filter chips | 5 |
| EPIC-03-S3 | As a student, I want to view reported items on a campus map | Google Maps SDK; clustered pins; respects active filters | 5 |
| EPIC-03-S4 | As a student, I want to browse a sorted feed | Sort by newest/oldest/location; pagination 20/page | 3 |
| EPIC-03-S5 | As a Loser, I want to save search queries for future alerts | Max 5 saved searches; FCM push within 10 min of new match | 5 |
| EPIC-03-S6 | As a returning user, I want to see my recent searches | Last 10 queries stored locally; swipe-to-dismiss; never synced to server | 2 |
| | **Epic Total** | | **25 pts** |

---

### EPIC-04 — Matching & Notifications
**Business Value:** Automated matching is the highest-leverage mechanism for achieving BO-01 and BO-03. Proactive notifications remove the burden of manual browsing.
**User Segments:** Item Loser, Item Finder

| Story ID | User Story | Acceptance Criteria (Summary) | Points |
|---|---|---|---|
| EPIC-04-S1 | As a Loser, I want the system to detect matches automatically | Category + keyword + location scoring; runs within 5 min of report; 70% threshold | 8 |
| EPIC-04-S2 | As a Loser, I want push notification when a match is found | FCM within 10 min; deep link to match detail; in-app badge fallback | 3 |
| EPIC-04-S3 | As a Finder, I want notification when my found item matches a lost report | FCM within 10 min; suppressed if claim already accepted | 3 |
| EPIC-04-S4 | As either party, I want a side-by-side match comparison screen | Highlights shared attributes; confidence indicator shown | 3 |
| EPIC-04-S5 | As either party, I want to dismiss an incorrect match | Reason captured for algorithm tuning; does not resurface unless report edited | 2 |
| EPIC-04-S6 | As a student, I want to view my notification history | Last 90 days; unread bold; clear all; server records retained for audit | 2 |
| | **Epic Total** | | **21 pts** |

---

### EPIC-05 — Claim & Verification Flow
**Business Value:** Structured verification ensures items go to rightful owners, supporting BO-04 (safe platform) and BO-01 (high recovery rate) while reducing fraud.
**User Segments:** Item Loser, Item Finder, Campus Admin

| Story ID | User Story | Acceptance Criteria (Summary) | Points |
|---|---|---|---|
| EPIC-05-S1 | As a Loser, I want to submit a formal claim with proof of ownership | Claimant cannot be the finder; ownership justification required; next steps shown | 5 |
| EPIC-05-S2 | As a Finder, I want to review and approve/reject claims | Push notification on new claim; approve opens chat; reject notifies claimant | 5 |
| EPIC-05-S3 | As a Loser, I want to track my claim status | Pending/Approved/Rejected/Resolved; status change notifications within 5 min | 3 |
| EPIC-05-S4 | As approved parties, I want secure in-app chat to arrange handoff | Text only; PII filter blocks personal contact info; archived 30 days post-resolution | 8 |
| EPIC-05-S5 | As a Loser, I want to confirm receipt to mark the report resolved | "Confirm Receipt" button; both confirmations close report; optional NPS rating | 3 |
| EPIC-05-S6 | As a Finder, I want to manage multiple simultaneous claims fairly | Queue of pending claims; only one can be approved; others auto-rejected on approval | 3 |
| | **Epic Total** | | **27 pts** |

---

### EPIC-06 — Admin & Moderation Dashboard
**Business Value:** Gives security officers a control plane for the physical depot, content moderation, and platform analytics — keeping UniFind trustworthy (BO-04) and adoption-ready (BO-02).
**User Segments:** Campus Admin / Security Officer

| Story ID | User Story | Acceptance Criteria (Summary) | Points |
|---|---|---|---|
| EPIC-06-S1 | As Security Officer, I want to log in with staff credentials and get elevated permissions | SSO + elevated-role JWT; Moderator and Super Admin roles; tamper-evident audit log | 5 |
| EPIC-06-S2 | As a Moderator, I want a queue of flagged content to review | Sort by flags/recency; Dismiss / Remove / Suspend actions; reporter notified on removal | 5 |
| EPIC-06-S3 | As Security Officer, I want to log items dropped off at the physical depot | Admin can create depot reports; "Security Office" badge on public listing; bulk-close support | 5 |
| EPIC-06-S4 | As Super Admin, I want to search and manage user accounts | Search by name/email/ID; view full history; suspend with mandatory reason | 5 |
| EPIC-06-S5 | As Campus Admin, I want a metrics dashboard to monitor platform health | Configurable date range; recovery rate, MAU, time-to-match; CSV export | 5 |
| EPIC-06-S6 | As Campus Admin, I want to send broadcast notifications to all users | 160 char max; immediate or scheduled delivery; FCM delivery confirmation; broadcast log | 3 |
| | **Epic Total** | | **28 pts** |

---

### Story Points Summary

| Epic | Stories | Story Points |
|------|---------|-------------|
| EPIC-01 User Authentication & Profile | 6 | 18 |
| EPIC-02 Lost & Found Item Reporting | 6 | 21 |
| EPIC-03 Search & Discovery | 6 | 25 |
| EPIC-04 Matching & Notifications | 6 | 21 |
| EPIC-05 Claim & Verification Flow | 6 | 27 |
| EPIC-06 Admin & Moderation Dashboard | 6 | 28 |
| **Total** | **36** | **140** |

---

## 10. Dependencies & Constraints

### Technical Dependencies

| Dependency | Purpose | Risk | Alternative |
|---|---|---|---|
| University SSO (OAuth 2.0 / SAML) | Primary authentication | High | .edu email + OTP fallback |
| Firebase Cloud Messaging (FCM) | Push notifications | Medium | APNs (iOS only) + in-app polling |
| AWS S3 / Firebase Storage | Item photo storage | Medium | Cloudflare R2 or MinIO |
| Google Maps SDK | Campus map & location | Medium | Mapbox or OpenStreetMap/Leaflet |
| PostgreSQL | Primary database | Low | MySQL / MariaDB |
| Elasticsearch | Full-text search | Medium | PostgreSQL pg_tsvector |
| React Native / Flutter | Cross-platform mobile | Low | Native Swift + Kotlin (doubles effort) |
| University IT / Network Team | SSO provisioning & data policy sign-off | High | No alternative — engage from day one |

### Assumptions

1. University exposes an OAuth 2.0 or SAML-compatible SSO endpoint
2. ≥ 20% of students will install and use the app voluntarily at launch
3. MVP targets one campus only — multi-campus deferred
4. No monetary transactions or reward mechanisms required
5. Automated keyword filtering + admin review is sufficient for MVP moderation
6. Item photos are optional but improve matching quality
7. Campus security officers will actively use the Admin Dashboard
8. Primary compliance framework is PDPA (Thailand); FERPA accommodations added if needed
9. Polling-based messaging (10–30s interval) is acceptable for v1
10. No competing internal university lost & found system exists

### Timeline Constraints

| Milestone | Target |
|---|---|
| University IT SSO provisioned | End of Week 3 |
| Core reporting & search features complete | End of Week 8 |
| Beta testing with 20–50 students | Week 12 |
| Feature freeze | Week 14 |
| MVP launch | End of Semester (~Week 16) |

---

## 11. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| University IT delays SSO integration | High | High | Engage IT in Week 1; build .edu + OTP fallback auth |
| Low student adoption post-launch | Medium | High | Pre-launch campaign via student union; target orientation week |
| Data privacy breach | Low | High | Role-based access control; proxied chat; security review pre-launch |
| Matching produces too many false positives | Medium | Medium | Rule-based matching first; tune thresholds during beta |
| Admin staff don't adopt the dashboard | Medium | High | Co-design with 2–3 security officers; onboarding session |
| Photo storage costs spike | Medium | Low | Client-side compression; 3-photo limit; billing alerts |
| In-app messaging enables harassment | Low | High | Keyword filtering; admin mute/ban; 30-day message retention |
| Scope creep delays MVP | High | High | Enforce MoSCoW; formal change-request process after Sprint 2 |

---

## 12. Traceability Matrix

| Business Objective | FRs | Epics |
|---|---|---|
| BO-01: Item recovery rate ≥ 60% | FR-001, FR-007, FR-008, FR-014, FR-015, FR-020 | EPIC-02, EPIC-04, EPIC-05 |
| BO-02: 40% active users within 12 months | FR-001, FR-004, FR-005, FR-011, FR-021 | EPIC-01, EPIC-03, EPIC-04, EPIC-06 |
| BO-03: Time-to-reunite < 48 hours | FR-007, FR-008, FR-020, FR-021, FR-011, FR-014 | EPIC-02, EPIC-04, EPIC-05 |
| BO-04: Safe, university-verified platform | FR-001, FR-012, FR-013, FR-014, FR-016 | EPIC-01, EPIC-05, EPIC-06 |

---

## 13. Success Metrics & KPIs

### Leading Indicators

| KPI | Baseline | Target (6 months) | How Measured |
|---|---|---|---|
| New item reports per week | 0 | ≥ 50/week | Backend event log |
| Match suggestion rate | 0% | ≥ 40% of lost reports get a match candidate within 24h | Matching engine logs |
| Push notification open rate | 0% | ≥ 35% | FCM analytics |
| New user registrations per week | 0 | ≥ 30/week (months 1–3) | Auth service events |

### Lagging Indicators

| KPI | Baseline | Target | How Measured |
|---|---|---|---|
| Item recovery rate | Unknown | ≥ 60% within 6 months | Claim resolution status; monthly cohort |
| Median time-to-reunite | Unknown | ≤ 48 hours | p50 of `claim_resolved_at` − `item_reported_at` |
| Monthly Active Users (MAU) | 0 | ≥ 40% of enrolled students by month 12 | Session and event tracking |
| User Satisfaction (NPS) | No baseline | NPS ≥ 40 | In-app rating prompt post-claim; quarterly |

---

## 14. Out of Scope (v1)

| Feature | Rationale |
|---|---|
| Reward / incentive / points system | Gamification complexity; potential monetary risk; deferred to v2 |
| Marketplace or item trading/selling | Contradicts no-monetary-transactions constraint |
| Non-university / external user access | Violates BO-04 verified-community safety requirement |
| AI-assisted image matching (computer vision) | Requires ML infrastructure beyond 4-month scope |
| Multi-campus or multi-institution support | Data isolation and SSO complexity; deferred post-v1 PMF |
| Social sharing to external platforms | Leaks item details outside verified community |
| Student-facing web companion app | Third surface to maintain; mobile-first sufficient for v1 |
| WebSocket real-time chat | Infrastructure complexity exceeds MVP timeline; polling is sufficient |
| ML-based admin moderation queue | Requires labelled training data; manual review sufficient at v1 scale |
| Item insurance or liability features | Legal scope far exceeds project mandate |

---

*End of PRD — UniFind v1.0*
*Next steps: Stakeholder review → Architecture design (System Architect) → UX wireframes → Sprint planning*
