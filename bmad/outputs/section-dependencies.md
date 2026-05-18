# Dependencies, Constraints, Risks & Traceability Matrix
**Product:** UniFind — Lost & Found App for University Students
**Section Author:** Product Manager
**Date:** 2026-04-20

---

## Technical Dependencies

| Dependency | Purpose | Risk Level | Alternative if Unavailable |
|---|---|---|---|
| University SSO (OAuth 2.0 / SAML) | Primary authentication — ensures only verified students and staff can access the platform | High | Fallback to manual .edu email verification with one-time passcode (OTP); delays onboarding and adds manual verification overhead |
| Firebase Cloud Messaging (FCM) | Push notifications for item matches, claim updates, and new messages | Medium | Apple Push Notification Service (APNs) for iOS only; in-app polling as degraded fallback; notification delay increases time-to-match |
| AWS S3 / Firebase Storage | Storing user-uploaded item photos | Medium | Cloudflare R2 or self-hosted MinIO on university servers; requires infrastructure negotiation with university IT |
| Google Maps SDK | Campus map integration for item location tagging and browse-by-location | Medium | Mapbox SDK (drop-in replacement at similar cost); OpenStreetMap/Leaflet for a zero-cost fallback with reduced UX quality |
| PostgreSQL | Primary relational database for users, items, claims, and messages | Low | MySQL or MariaDB are viable alternatives; migration cost is moderate but manageable within a semester |
| Elasticsearch | Full-text and fuzzy search across item listings | Medium | PostgreSQL built-in full-text search (pg_tsvector) is a viable v1 fallback; lower relevance ranking but no additional infrastructure |
| React Native / Flutter | Cross-platform mobile frontend (iOS + Android from a single codebase) | Low | Native development (Swift + Kotlin) is possible but doubles frontend effort and exceeds a 4-month timeline |
| Node.js (Express) / Django REST | Backend API server | Low | Either framework is interchangeable; switching mid-project is the primary risk |
| JWT (JSON Web Tokens) | Session management and API authorization after SSO handoff | Low | Cookie-based sessions are a fallback; JWT is preferred for mobile client compatibility |
| University IT / Network Team | SSO credentials provisioning, data policy sign-off, and campus network whitelisting | High | No true alternative; project cannot launch without university IT cooperation. Mitigation: engage IT as a stakeholder from day one |

---

## Assumptions

The following assumptions underpin the requirements. If any are found to be false, one or more requirements may need to be revised or re-scoped.

1. **University SSO availability:** The university exposes an OAuth 2.0 or SAML-compatible SSO endpoint that the app team can integrate with. If SSO is unavailable or restricted, the entire authentication model must be redesigned.

2. **Student adoption willingness:** A meaningful portion of students (≥ 20% initially) will voluntarily install and use a new university app rather than defaulting to existing informal channels (Facebook groups, WhatsApp). If adoption is lower, the network effect needed for item matching will not materialise.

3. **Single campus scope for v1:** The app targets one university campus for MVP. Multi-campus or multi-institution support is explicitly deferred and not reflected in data models or UX flows.

4. **No monetary transactions needed:** Items will be returned on good faith with no in-app reward or compensation mechanism. If the university or users demand incentive structures, the scope and compliance requirements expand significantly.

5. **Moderation is manageable at MVP scale:** With a small, university-verified user base, automated keyword filtering plus admin review is sufficient for chat moderation. At scale, a more robust moderation pipeline would be required.

6. **Item photos are optional but improve matching:** Users are willing but not required to upload photos. The matching algorithm and browse experience still function without photos, relying on text descriptions and category tags.

7. **Admin staff have time and training:** Campus security officers or designated admin staff will actively use the Admin Dashboard to manage the physical depot and resolve claims. If admin engagement is low, the claim verification flow breaks down.

8. **Compliance scope is PDPA (Thailand) for v1:** The team assumes the primary regulatory framework is Thailand's PDPA. If the university operates under FERPA (US) or GDPR (EU), additional data handling requirements — such as data residency and formal data processing agreements — will apply.

9. **Real-time messaging is not required at MVP:** A near-real-time messaging experience (polling every 10–30 seconds) is acceptable for v1. True WebSocket-based real-time chat is deferred. If users reject latency in messaging, this assumption must be revisited before launch.

10. **University provides no competing internal tool:** There is no existing university-run digital lost & found system that UniFind must integrate with or replace via formal procurement. If one exists, stakeholder alignment and potential integration work would be required.

---

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation Strategy |
|---|---|---|---|
| University IT delays SSO integration | High | High | Engage IT stakeholders in week 1; design an .edu email + OTP fallback auth path so development is not blocked while SSO is being provisioned |
| Low student adoption post-launch | Medium | High | Conduct pre-launch awareness campaign through student channels; partner with student union and security office for endorsement; target orientation week as a launch window |
| Data privacy breach or misuse of personal item data | Low | High | Enforce role-based access control; proxy chat so users never share phone numbers; limit public-facing item detail to category and location; conduct a security review before launch |
| Item matching produces too many false positives | Medium | Medium | Start with rule-based matching (category + location + date range); gather feedback in beta and tune thresholds before enabling AI-assisted matching |
| Admin staff do not adopt the dashboard | Medium | High | Co-design the dashboard with 2–3 security officers in discovery; provide a short onboarding session; make the dashboard accessible on tablet/desktop without app install |
| Photo upload causes storage costs to spike | Medium | Low | Enforce client-side image compression (max 1 MB per upload); set a per-item photo limit of 3; monitor S3/Firebase usage weekly and set billing alerts |
| In-app messaging enables harassment | Low | High | Implement keyword filtering on all messages; give admins the ability to mute or ban users; log all messages for a 30-day retention window for investigation purposes |
| Scope creep delays MVP beyond semester deadline | High | High | Lock the v1 scope via MoSCoW prioritisation; introduce a formal change-request process after sprint 2; defer all "Could" and "Won't" items to a backlog with no committed date |

---

## Constraints Summary

### Technical Constraints
- Authentication must use university SSO (OAuth 2.0 / SAML); no social login (Google, Apple, Facebook) as a standalone option.
- The app must run natively on both iOS (14+) and Android (10+) using a shared codebase (React Native or Flutter).
- All item photos must be compressed client-side before upload; maximum 1 MB per image, 3 images per item.
- The backend must expose a RESTful API; all client-server communication must use HTTPS/TLS 1.2+.
- Real-time WebSocket connections are deferred to v2; v1 uses polling for message delivery.
- The system must support at least 500 concurrent users for a single campus deployment without performance degradation.

### Business / Legal Constraints
- No monetary transactions of any kind may be facilitated within the app (no payments, tipping, or rewards).
- All users must be verified members of the university community; no external or anonymous access is permitted.
- Item listings must not expose the finder's or loser's personal contact information (phone number, personal email) publicly.
- Data storage and processing must comply with applicable privacy law: PDPA (Thailand) as the primary framework, with FERPA accommodations if deployed at US institutions.
- Chat and messaging content must be moderatable by admin staff; end-to-end encryption that prevents admin access is not permitted in v1.
- The university retains ownership of all data generated on the platform; the development team must execute a data processing agreement (DPA) with the institution.

### Timeline Constraints
- MVP must be delivered within one academic semester (approximately 4 months from kick-off).
- University IT SSO provisioning must be completed by the end of week 3 or the fallback auth path must be activated to avoid blocking development.
- Beta testing with a pilot group of 20–50 students must begin no later than week 12 to allow two weeks of bug fixing before the end-of-semester deadline.
- Feature freeze (no new feature development) must occur at week 14; only critical bug fixes are permitted after that point.

---

## Traceability Matrix

The table below maps each Business Objective to the Functional Requirements (FR) and Epics that directly fulfill it. FR IDs reference the ten core feature areas defined in the context file.

| Business Objective | Description | Functional Requirement IDs | Epic IDs |
|---|---|---|---|
| BO-01: Item recovery rate ≥ 60% | Increase the proportion of reported lost items that are successfully returned to their owner | FR-001 (Auth & Profile), FR-003 (Report Found Item), FR-005 (Item Matching & Notifications), FR-007 (Claim & Verification Flow), FR-009 (Categories & Tagging) | EP-01 (User Onboarding), EP-03 (Found Item Reporting), EP-05 (Matching Engine), EP-07 (Claim Flow) |
| BO-02: 40% enrolled students as active users within 12 months | Drive broad, sustained adoption across the student population | FR-001 (Auth & Profile), FR-004 (Browse & Search), FR-006 (In-App Messaging), FR-010 (Analytics Dashboard) | EP-01 (User Onboarding), EP-04 (Search & Browse), EP-06 (Messaging), EP-10 (Analytics) |
| BO-03: Time-to-reunite under 48 hours for matched items | Reduce the elapsed time from item report creation to physical reunification | FR-002 (Report Lost Item), FR-003 (Report Found Item), FR-005 (Item Matching & Notifications), FR-006 (In-App Messaging), FR-007 (Claim & Verification Flow) | EP-02 (Lost Item Reporting), EP-03 (Found Item Reporting), EP-05 (Matching Engine), EP-06 (Messaging), EP-07 (Claim Flow) |
| BO-04: Safe, university-verified platform | Ensure the platform is free from external users, spam, harassment, and data misuse | FR-001 (Auth & Profile), FR-006 (In-App Messaging — moderation), FR-007 (Claim & Verification Flow), FR-008 (Admin Dashboard) | EP-01 (User Onboarding & Verification), EP-06 (Messaging & Moderation), EP-08 (Admin Dashboard) |

**FR ID Reference:**

| FR ID | Feature Area |
|---|---|
| FR-001 | User Authentication & Profile (university-verified) |
| FR-002 | Report Lost Item |
| FR-003 | Report Found Item |
| FR-004 | Browse & Search Items |
| FR-005 | Item Matching & Notifications |
| FR-006 | In-App Messaging (owner ↔ finder) |
| FR-007 | Claim & Verification Flow |
| FR-008 | Admin Dashboard (security office) |
| FR-009 | Item Categories & Tagging |
| FR-010 | Analytics & Success Metrics Dashboard |
| FR-011 – FR-022 | Reserved for detailed sub-requirements within each feature area (to be elaborated in sprint planning) |

---

## Success Metrics & KPIs

### Leading Indicators (predict future outcomes)

| KPI | Description | Baseline (pre-launch) | Target (6 months post-launch) | Measurement Method |
|---|---|---|---|---|
| New item reports per week | Volume of lost + found reports submitted; indicates platform engagement and content network | 0 | ≥ 50 reports/week | Backend event log; weekly automated report |
| Match suggestion rate | Percentage of lost item reports that receive at least one system-generated match candidate within 24 hours | 0% | ≥ 40% | Matching engine logs; (matches generated / lost reports) |
| Notification open rate | Percentage of push notifications (match alerts, claim updates) that are opened by recipients | 0% | ≥ 35% | FCM delivery and open analytics |
| New user registration rate | Number of new verified accounts created per week | 0 | ≥ 30 new users/week in months 1–3 | Auth service user creation events |

### Lagging Indicators (measure achieved outcomes)

| KPI | Description | Baseline (pre-launch) | Target | Measurement Method |
|---|---|---|---|---|
| Item recovery rate | Items marked "returned" / total lost item reports submitted in the same period | Unknown (no prior system) | ≥ 60% within 6 months | Claim resolution status in database; monthly cohort analysis |
| Median time-to-reunite | Median time (hours) from a lost item report creation to its corresponding claim being marked "resolved" | Unknown | ≤ 48 hours | Timestamp delta between `item_reported_at` and `claim_resolved_at`; p50 metric |
| Monthly Active Users (MAU) | Unique verified users who perform at least one meaningful action (report, search, message, claim) within a 30-day window | 0 | ≥ 40% of enrolled students by month 12 | Session and event tracking in analytics layer |
| User Satisfaction Score (NPS) | Net Promoter Score collected via in-app prompt shown after a resolved claim | No baseline | NPS ≥ 40 | In-app rating prompt triggered on claim resolution; calculated quarterly |

---

## Out of Scope (v1)

The following features are explicitly excluded from the v1 MVP. They are logged in the product backlog for consideration in future releases.

| Excluded Feature | Rationale |
|---|---|
| Reward or incentive system (points, badges, monetary rewards) | Introduces gamification complexity, potential monetary transaction risk, and policy concerns; deferred to v2 after recovery-rate baseline is established |
| Marketplace or item trading / selling | Directly contradicts the constraint against monetary transactions; would require separate legal and payment infrastructure |
| Non-university / external user access | Violates the verified-community safety requirement (BO-04); any public access would require a separate moderation and identity model |
| AI-assisted image matching (computer vision) | Requires significant ML infrastructure and training data that cannot be assembled within a 4-month semester; rule-based matching is sufficient for v1 |
| Multi-campus or multi-institution support | Data isolation, branding, and SSO integration complexity multiply with each additional institution; deferred until v1 product-market fit is proven |
| Social sharing to external platforms | Leaks item details outside the verified community, undermining privacy and safety constraints |
| Native web companion application | Web dashboard for students (not admins) adds a third surface to maintain; mobile-first is sufficient for v1 student-facing flows |
| WebSocket real-time chat | Infrastructure complexity exceeds MVP timeline; polling-based messaging meets communication needs for a small user base |
| Automated admin moderation queue with ML classification | Requires labelled training data and ML ops infrastructure; manual admin review is sufficient at v1 scale |
| Item insurance or liability features | Legal and compliance scope far exceeds the project team's mandate and the semester timeline |
