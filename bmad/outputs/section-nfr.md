# Non-Functional Requirements — UniFind Lost & Found App

---

## NFR-001: MUST - Performance - API Response Time

NFR-001: MUST - Performance - All REST API endpoints must return responses within an acceptable latency threshold under normal load.
Metric: p95 response time < 200ms for read endpoints (search, browse, item detail); p95 < 500ms for write endpoints (create report, submit claim) under a load of up to 500 concurrent users.
Rationale: Slow search and browse responses directly reduce engagement and make students abandon the platform before finding their items.

---

## NFR-002: MUST - Performance - Image Upload Throughput

NFR-002: MUST - Performance - Item photo uploads to cloud storage must complete within a user-acceptable time window.
Metric: A 5MB image upload must complete in < 10 seconds on a standard 4G mobile connection (minimum 10 Mbps uplink).
Rationale: Photos are the primary evidence for item identification; upload friction causes users to skip photos, degrading match quality.

---

## NFR-003: MUST - Security - Authentication Enforcement

NFR-003: MUST - Security - Every protected API endpoint must reject requests that lack a valid, non-expired JWT issued after successful university SSO authentication.
Metric: 0% of API calls to protected routes succeed without a valid JWT; token expiry enforced at ≤ 1 hour with refresh token rotation.
Rationale: Restricting access to university-verified users is a core product constraint that prevents spam and protects student data.

---

## NFR-004: MUST - Security - Transport Encryption

NFR-004: MUST - Security - All data transmitted between the mobile client, backend, and third-party services must be encrypted in transit.
Metric: TLS 1.2 minimum enforced on all connections; TLS 1.3 preferred; HTTP (plaintext) connections refused with a 301 redirect or connection reset.
Rationale: Unencrypted traffic exposes personally identifiable student information and item location data to network-level interception.

---

## NFR-005: MUST - Reliability - Service Uptime

NFR-005: MUST - Reliability - The UniFind backend and mobile app must maintain high availability during the academic day.
Metric: Monthly uptime ≥ 99.5% (allowing ≤ 3.6 hours unplanned downtime per month); planned maintenance windows restricted to 02:00–05:00 local time.
Rationale: Students report and search for items throughout the day; extended downtime directly reduces the item recovery rate tied to business objective BO-01.

---

## NFR-006: MUST - Reliability - Push Notification Delivery

NFR-006: MUST - Reliability - Match and claim notifications delivered via Firebase Cloud Messaging must reach users promptly.
Metric: ≥ 95% of FCM notifications delivered within 60 seconds of the triggering server event, measured over a rolling 7-day window.
Rationale: Fast notifications are critical to achieving the BO-03 target of under 48 hours time-to-reunite; delayed alerts let items go unclaimed.

---

## NFR-007: MUST - Scalability - Concurrent User Load

NFR-007: MUST - Scalability - The backend must handle peak concurrent usage at the start and end of semesters without degraded performance.
Metric: System must sustain 500 simultaneous active users with no more than a 20% increase in p95 API latency compared to baseline (50 users); auto-scaling must provision additional capacity within 3 minutes.
Rationale: Campus events and semester start periods produce traffic spikes; failure to scale causes outages exactly when lost-item reports surge.

---

## NFR-008: SHOULD - Scalability - Database Read Scalability

NFR-008: SHOULD - Scalability - The PostgreSQL database must support read-heavy workloads without becoming a bottleneck as the user base grows.
Metric: Read queries (item search, browse feed) must execute in < 100ms at the 95th percentile with up to 10,000 stored item records; read replicas must be provisioned before the user base exceeds 5,000 active users.
Rationale: Browse and search are the most frequent operations; unoptimized queries at scale will make the platform feel unusable and drive users back to Facebook groups.

---

## NFR-009: MUST - Privacy / Compliance - Data Residency and Retention

NFR-009: MUST - Privacy/Compliance - User personal data and item records must be stored and retained in accordance with applicable data protection regulations.
Metric: All personal data stored in a PDPA/FERPA-compliant data region; resolved item records (returned or expired) purged or anonymized within 90 days of closure; user account data deleted within 30 days of account termination request.
Rationale: The university's data governance obligations and PDPA/FERPA compliance are non-negotiable constraints that expose the institution to legal liability if violated.

---

## NFR-010: MUST - Privacy / Compliance - Sensitive Data Minimization

NFR-010: MUST - Privacy/Compliance - Item listings must not expose the reporter's personal contact details or student ID to other users without explicit consent.
Metric: 0 item listings expose the reporter's email, phone number, or student ID number in any publicly readable API response or UI view; all user-to-user contact must be proxied through the in-app messaging system.
Rationale: Public exposure of student contact details enables harassment, violating the key constraint that chat must be moderated and protecting user safety.

---

## NFR-011: SHOULD - Usability - App Launch Time

NFR-011: SHOULD - Usability - The mobile app must be interactive quickly after the user taps the icon to reduce abandonment.
Metric: Time-to-interactive (TTI) from cold launch < 3 seconds on a mid-range Android device (e.g., Snapdragon 665, 4GB RAM) on a 4G connection.
Rationale: A slow cold start discourages daily habitual use, which is required to achieve the 40% active-user penetration target in BO-02.

---

## NFR-012: SHOULD - Usability - Search Result Relevance Speed

NFR-012: SHOULD - Usability - Full-text and filtered search across item listings must return results fast enough to feel instantaneous.
Metric: Search results rendered in the UI within 1 second (end-to-end, including network) for keyword queries across a dataset of up to 10,000 items, for 95% of queries.
Rationale: Students abandon slow search tools and revert to scrolling social media groups, undermining the platform's core value proposition.

---

## NFR-013: SHOULD - Security - In-App Messaging Content Safety

NFR-013: SHOULD - Security - Messages sent through the in-app chat must be screened to prevent harassment and the sharing of inappropriate content.
Metric: Automated moderation must flag or block messages containing profanity, phone numbers, or email addresses within 500ms of send; flagged messages must be reviewed or auto-blocked before delivery to the recipient.
Rationale: The key constraint explicitly requires chat to be moderated or proxied to prevent harassment between students.

---

## NFR-014: SHOULD - Maintainability - Test Coverage

NFR-014: SHOULD - Maintainability - The backend codebase must maintain sufficient automated test coverage to catch regressions before deployment.
Metric: Minimum 80% line coverage on backend business logic (auth, item CRUD, matching, claim flow) enforced in the CI pipeline; any pull request reducing coverage below threshold must be blocked from merging.
Rationale: A small team with a 4-month delivery window cannot afford regression bugs that erode user trust; automated tests are the primary safety net.

---

## NFR-015: SHOULD - Maintainability - Deployment Pipeline Lead Time

NFR-015: SHOULD - Maintainability - The CI/CD pipeline must enable rapid, low-risk deployments to production.
Metric: End-to-end pipeline (lint → test → build → deploy to staging) must complete in < 15 minutes; rollback to the previous production build must be executable in < 5 minutes.
Rationale: Fast deploy cycles allow the team to ship bug fixes and matching-algorithm improvements quickly, directly supporting the BO-01 recovery rate target.

---

## NFR-016: COULD - Reliability - Offline Graceful Degradation

NFR-016: COULD - Reliability - The mobile app must remain partially functional when the device has no network connectivity.
Metric: Previously loaded item listings and the user's own reported items must remain viewable for at least 24 hours after the last successful sync; the app must display a clear offline banner within 3 seconds of connectivity loss rather than showing blank screens or crashes.
Rationale: Campus Wi-Fi dead zones are common; crashing or showing empty screens when offline undermines perceived reliability and drives negative app store reviews.
