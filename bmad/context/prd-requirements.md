# Lost & Found App — Shared Requirements Context

## Project Overview
**Product:** UniFind — Lost & Found App for University Students
**Platform:** Mobile (iOS & Android) with optional web companion
**Target Release:** MVP in one semester (~4 months)
**Project Level:** Level 2 (multi-feature, single team, moderate complexity)

## Problem Statement
University campuses are large, busy environments where students frequently lose personal belongings — student IDs, keys, wallets, laptops, water bottles, AirPods, and more. Current solutions (Facebook groups, notice boards, security office drop-offs) are fragmented, slow, and unreliable. Students have no unified, searchable, campus-specific platform to report or browse lost/found items, leading to permanent loss of valuable belongings and unnecessary stress.

## Target Users
1. **Item Loser** — A student who has lost a personal item on campus and wants to report it and find it quickly.
2. **Item Finder** — A student who has found an item on campus and wants to return it to the rightful owner.
3. **Campus Admin / Security Officer** — University staff who manage a physical lost & found depot and need a digital dashboard.

## Business Objectives
1. BO-01: Increase item recovery rate on campus to ≥ 60% within 6 months of launch.
2. BO-02: Achieve 40% of enrolled students as active users within 12 months.
3. BO-03: Reduce time-to-reunite (item lost → returned) to under 48 hours for matched items.
4. BO-04: Provide a safe, university-verified platform (no public spam, no external users).

## Key Constraints
- Users must authenticate via university email (.edu domain or SSO).
- No monetary transactions — the app must not enable buying/selling.
- Privacy: item details should not expose sensitive personal data publicly.
- Must be accessible on both iOS and Android.
- Chat/communication must be moderated or proxied to prevent harassment.
- Data must be stored in compliance with university data policies (PDPA / FERPA depending on region).

## Tech Stack Preferences
- **Frontend:** React Native (cross-platform iOS + Android) or Flutter
- **Backend:** Node.js (Express) or Django REST Framework
- **Database:** PostgreSQL (relational — items, users, claims)
- **Auth:** University SSO (OAuth 2.0 / SAML) + JWT
- **Storage:** AWS S3 or Firebase Storage (item photos)
- **Notifications:** Firebase Cloud Messaging (FCM)
- **Search:** Elasticsearch or PostgreSQL full-text search
- **Maps:** Google Maps SDK (campus map integration)

## Core Feature Areas
1. User Authentication & Profile (university-verified)
2. Report Lost Item
3. Report Found Item
4. Browse & Search Items
5. Item Matching & Notifications
6. In-App Messaging (owner ↔ finder)
7. Claim & Verification Flow
8. Admin Dashboard (security office)
9. Item Categories & Tagging
10. Analytics & Success Metrics Dashboard

## Success Metrics
- Item recovery rate (items returned / items reported lost)
- Time-to-match (report created → match made)
- Daily/Monthly active users
- Claim success rate (claims verified and resolved)
- User satisfaction score (NPS / in-app rating)
- Notification open rate

## MoSCoW Priority Guidance
- **Must:** Auth, Report Lost, Report Found, Browse/Search, Notifications, Basic Messaging
- **Should:** Item Matching Algorithm, Claim Verification, Map View, Categories/Tags
- **Could:** Admin Dashboard, Analytics, AI-assisted matching, social sharing
- **Won't (v1):** Reward system, marketplace features, non-university users
