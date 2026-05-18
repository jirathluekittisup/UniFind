# Epics & User Stories
**Product:** UniFind — Lost & Found App for University Students
**Document Type:** PRD Section — Epics & User Stories
**Date:** 2026-04-20

---

## RICE Prioritization Summary

| Epic ID | Epic Name | Reach | Impact | Confidence | Effort | RICE Score |
|---------|-----------|-------|--------|------------|--------|------------|
| EPIC-01 | User Authentication & Profile | 10 | 3 | 95% | 2 | **14.25** |
| EPIC-02 | Lost & Found Item Reporting | 10 | 3 | 90% | 3 | **9.00** |
| EPIC-03 | Search & Discovery | 9 | 3 | 85% | 3 | **7.65** |
| EPIC-04 | Matching & Notifications | 8 | 3 | 75% | 4 | **4.50** |
| EPIC-05 | Claim & Verification Flow | 7 | 3 | 80% | 3 | **5.60** |
| EPIC-06 | Admin & Moderation Dashboard | 4 | 2 | 85% | 3 | **2.27** |

**RICE Score Formula:** (Reach × Impact × Confidence) / Effort

**Scoring Rationale:**
- **Reach** — estimated % of active users (out of 10) who touch this epic per quarter
- **Impact** — effect on the primary business objective (1 = minimal, 2 = moderate, 3 = massive)
- **Confidence** — team confidence in the estimates (%)
- **Effort** — person-months of engineering work required

---

## EPIC-01 — User Authentication & Profile

**Business Value:** Without verified university identity, the platform cannot guarantee campus-only safety or prevent abuse. A frictionless, university-authenticated onboarding experience is the foundational prerequisite for every downstream feature and directly supports BO-04 (university-verified platform).

**User Segments Impacted:** Item Loser, Item Finder, Campus Admin / Security Officer

---

### EPIC-01-S1 — University SSO Sign-In

**User Story:**
As a university student, I want to sign in using my university SSO credentials so that I can access UniFind without creating a separate account.

**Acceptance Criteria:**
1. The sign-in screen presents a "Sign in with University Account" button that initiates an OAuth 2.0 / SAML flow against the university identity provider.
2. Users who successfully authenticate with a recognised `.edu` email domain are granted access; users outside the domain are shown a clear rejection message.
3. A JWT session token is issued on successful authentication, persists across app restarts up to 30 days, and is revoked on explicit sign-out.

**Story Points:** 5

---

### EPIC-01-S2 — Profile Creation on First Login

**User Story:**
As a newly authenticated student, I want to complete a brief profile setup so that other users can identify me when I report or claim items.

**Acceptance Criteria:**
1. On first login, the user is prompted to confirm their display name (pre-filled from SSO) and optionally upload a profile photo.
2. The profile is created in the database and linked to the verified university email before the user can access any other feature.
3. The user can skip the profile photo and complete setup using only their verified name.

**Story Points:** 3

---

### EPIC-01-S3 — Profile Editing

**User Story:**
As a registered student, I want to edit my profile display name and photo so that my contact information stays current and recognisable.

**Acceptance Criteria:**
1. The profile settings screen allows updating the display name (max 60 characters) and replacing or removing the profile photo.
2. Changes are reflected across all existing reported items and messages attributed to that user within 5 minutes.
3. The university email address is read-only and cannot be changed from within the app.

**Story Points:** 2

---

### EPIC-01-S4 — Session Management & Sign-Out

**User Story:**
As a student using a shared device, I want to sign out of UniFind so that my account and reported items are not accessible to others.

**Acceptance Criteria:**
1. A "Sign Out" option is available from the profile screen and immediately invalidates the local JWT and clears cached personal data.
2. After sign-out, navigating to any protected screen redirects the user to the sign-in page.
3. The user receives a confirmation prompt before sign-out is finalised to prevent accidental logout.

**Story Points:** 2

---

### EPIC-01-S5 — Notification Preferences

**User Story:**
As a registered student, I want to manage which notifications I receive so that I am only alerted about events relevant to me.

**Acceptance Criteria:**
1. The profile settings screen presents toggles for: match alerts, claim status updates, and admin messages.
2. Toggling a preference off immediately stops the corresponding FCM push notification category without requiring re-login.
3. Preferences persist across devices when the user re-authenticates.

**Story Points:** 3

---

### EPIC-01-S6 — Account Deactivation

**User Story:**
As a graduated student or departing user, I want to deactivate my account so that my personal data is removed from the platform in line with privacy regulations.

**Acceptance Criteria:**
1. The profile settings screen includes a "Deactivate Account" option requiring password or SSO re-confirmation before proceeding.
2. On deactivation, the user's open reports are marked as "closed/anonymous" and personal identifiers are pseudonymised within 24 hours.
3. The user receives a final confirmation email to their university address summarising what data has been removed.

**Story Points:** 3

---

## EPIC-02 — Lost & Found Item Reporting

**Business Value:** The core value loop of UniFind depends entirely on the quality and completeness of item reports. Enabling students to quickly log lost and found items with rich metadata (photos, location, categories) drives the item recovery rate toward BO-01 (≥ 60%) and reduces time-to-reunite toward BO-03 (< 48 hours).

**User Segments Impacted:** Item Loser, Item Finder

---

### EPIC-02-S1 — Report a Lost Item

**User Story:**
As an Item Loser, I want to report a lost item with a description, category, and last-known location so that finders can identify and return it to me.

**Acceptance Criteria:**
1. The "Report Lost" form captures: item title (required), category (required, from predefined list), description (max 500 chars), last-seen location (map pin or campus building selector), and date/time lost.
2. The submitted report appears in the public browse feed within 60 seconds of submission.
3. The reporter receives an in-app confirmation and a push notification with the report ID upon successful submission.

**Story Points:** 5

---

### EPIC-02-S2 — Report a Found Item

**User Story:**
As an Item Finder, I want to report an item I have found with a photo and location so that the rightful owner can identify and claim it.

**Acceptance Criteria:**
1. The "Report Found" form captures: item title, category, description, one or more photos (max 5, each ≤ 10 MB), pickup/found location, and date found.
2. Photos are stored in AWS S3 / Firebase Storage and rendered in the listing within 30 seconds of upload.
3. The system prevents the finder's contact details from appearing publicly — only in-app messaging is exposed after a verified match.

**Story Points:** 5

---

### EPIC-02-S3 — Edit or Update a Report

**User Story:**
As an Item Loser or Finder, I want to edit my submitted report so that I can add new details or correct inaccuracies as more information becomes available.

**Acceptance Criteria:**
1. Report authors can edit all fields except the submission timestamp; an "Edited" badge is shown on the listing after any update.
2. Edits to key fields (title, category, location) re-trigger the matching engine within 5 minutes to detect newly compatible pairs.
3. A change history is stored server-side and visible to admins for moderation purposes.

**Story Points:** 3

---

### EPIC-02-S4 — Close or Resolve a Report

**User Story:**
As an Item Loser or Finder, I want to mark my report as resolved so that the item is removed from the active listing and the recovery is counted toward platform metrics.

**Acceptance Criteria:**
1. A "Mark as Resolved" action is available on the report detail screen to the report author only.
2. Resolved reports move to an archived state (not visible in default browse/search) but remain accessible via direct link for 90 days.
3. On resolution, the system increments the item recovery counter used for BO-01 metrics.

**Story Points:** 2

---

### EPIC-02-S5 — Photo Management on Reports

**User Story:**
As an Item Finder, I want to add, replace, or remove photos on my found-item report so that the listing stays accurate as the item's condition or packaging changes.

**Acceptance Criteria:**
1. Up to 5 photos can be attached; the author can add new photos or delete existing ones from the edit screen.
2. Deleted photos are removed from S3 / Firebase Storage within 24 hours of removal.
3. At least one photo must remain on a found-item report at all times; attempting to delete the last photo surfaces an inline error.

**Story Points:** 3

---

### EPIC-02-S6 — Item Category & Tagging

**User Story:**
As a reporter, I want to tag my item with a predefined category and optional free-text tags so that my report is easier to find through search and matching.

**Acceptance Criteria:**
1. A hierarchical category picker (e.g., Electronics > Laptop, Accessories > Keys) is available on both report forms.
2. Up to 5 custom tags (max 20 chars each) can be added to any report and are indexed for full-text search.
3. Selecting a category auto-populates a suggested tag list to accelerate reporting.

**Story Points:** 3

---

## EPIC-03 — Search & Discovery

**Business Value:** A powerful, campus-aware search experience is what transforms UniFind from a simple bulletin board into a functional reunion tool. Enabling students to rapidly narrow down candidates by location, category, and date directly reduces time-to-match and drives BO-03 (< 48 hours time-to-reunite).

**User Segments Impacted:** Item Loser, Item Finder, Campus Admin / Security Officer

---

### EPIC-03-S1 — Keyword Search

**User Story:**
As an Item Loser, I want to search all found-item reports using keywords so that I can quickly identify whether someone has found my belonging.

**Acceptance Criteria:**
1. A persistent search bar on the browse feed performs full-text search across title, description, and tags using Elasticsearch or PostgreSQL full-text search.
2. Results are returned and rendered within 2 seconds for any query on a dataset of up to 10,000 active reports.
3. The search input supports partial-word matching (e.g., "AirP" returns "AirPods" results).

**Story Points:** 5

---

### EPIC-03-S2 — Filter by Category, Date, and Location

**User Story:**
As an Item Loser, I want to filter search results by item category, date range, and campus location so that I can eliminate irrelevant results quickly.

**Acceptance Criteria:**
1. A filter panel provides independent controls for: category (multi-select from category tree), date range (calendar picker, default last 30 days), and location (campus building or map radius).
2. Applied filters are displayed as dismissible chips above the results list.
3. Combining multiple active filters uses AND logic and updates results in real time without requiring a page reload.

**Story Points:** 5

---

### EPIC-03-S3 — Map View of Reported Items

**User Story:**
As a student, I want to view reported items on a campus map so that I can see where items were lost or found relative to places I frequent.

**Acceptance Criteria:**
1. A toggleable "Map View" displays Google Maps SDK with clustered pins for all active found and lost reports that have location data.
2. Tapping a pin or cluster shows a summary card with the item title, category, and a link to the full report.
3. The map respects the currently active keyword and filter selections from the list view.

**Story Points:** 5

---

### EPIC-03-S4 — Browse Feed with Sorting

**User Story:**
As a student, I want to browse a sorted feed of active reports so that I can discover items without a specific search query.

**Acceptance Criteria:**
1. The default browse feed displays active reports sorted by most recently posted, with pagination or infinite scroll (20 items per page).
2. The user can toggle sort order between: Newest, Oldest, and Closest to My Location (requires location permission).
3. The feed excludes resolved and expired reports by default, with an option to show them.

**Story Points:** 3

---

### EPIC-03-S5 — Saved Searches & Alerts

**User Story:**
As an Item Loser, I want to save my search query so that I am automatically notified if a new found-item report matches my criteria in the future.

**Acceptance Criteria:**
1. A "Save Search" button on any search results page stores the current keyword and filter combination to the user's profile (max 5 saved searches).
2. When a new found-item report is published and matches a saved search, the user receives a push notification within 10 minutes.
3. Saved searches are manageable (editable, deletable) from the profile screen.

**Story Points:** 5

---

### EPIC-03-S6 — Recent Search History

**User Story:**
As a returning user, I want to see my recent search history so that I can quickly repeat previous searches without re-entering queries.

**Acceptance Criteria:**
1. Up to 10 most recent unique search queries are stored locally on the device and displayed as a dropdown when the search bar is focused.
2. Individual history entries can be dismissed by swiping; a "Clear All" option removes the full history.
3. Search history is local-only and never synced to the server to protect user privacy.

**Story Points:** 2

---

## EPIC-04 — Matching & Notifications

**Business Value:** Automated matching between lost and found reports is the highest-leverage mechanism for achieving BO-01 (≥ 60% recovery rate) and BO-03 (< 48 hours time-to-reunite). Proactive, timely notifications remove the burden of manual browsing from users and keep them engaged with the platform.

**User Segments Impacted:** Item Loser, Item Finder

---

### EPIC-04-S1 — Automated Match Detection

**User Story:**
As an Item Loser, I want the system to automatically detect potential matches between my lost report and active found reports so that I am notified without having to search manually.

**Acceptance Criteria:**
1. When a new lost or found report is submitted or edited, the matching engine evaluates it against all active reports of the opposite type within 5 minutes using category, keyword, and location proximity scoring.
2. Pairs with a match confidence score above a configurable threshold (default 70%) are flagged as potential matches and surfaced to both parties.
3. Match events are logged server-side with the score breakdown for admin review and algorithm tuning.

**Story Points:** 8

---

### EPIC-04-S2 — Match Notification to Item Loser

**User Story:**
As an Item Loser, I want to receive a push notification when a potential match is found for my lost item so that I can act on it immediately.

**Acceptance Criteria:**
1. A push notification via FCM is sent to the Item Loser within 10 minutes of a match being detected, including the matched found-item title and a deep link to the match detail screen.
2. The notification is also surfaced as an in-app alert badge on the "My Reports" tab.
3. If the user has disabled push notifications, the match alert is still visible within the app on next open.

**Story Points:** 3

---

### EPIC-04-S3 — Match Notification to Item Finder

**User Story:**
As an Item Finder, I want to receive a push notification when someone's lost report matches the item I found so that I can help facilitate its return.

**Acceptance Criteria:**
1. A push notification via FCM is sent to the Item Finder within 10 minutes of a match, including the matched lost-item title and a deep link to the match detail screen.
2. The finder can view the match detail screen to see the loser's non-identifying contact summary (display name only) and initiate in-app messaging.
3. Finder notifications are suppressed if the finder has already accepted a claim on the item.

**Story Points:** 3

---

### EPIC-04-S4 — Match Detail Screen

**User Story:**
As either party in a potential match, I want to view a side-by-side comparison of the two reports so that I can assess whether they describe the same item before initiating contact.

**Acceptance Criteria:**
1. The match detail screen displays both reports side by side (or stacked on mobile), highlighting shared attributes: category, tags, location proximity, and date overlap.
2. A match confidence indicator (e.g., "Strong Match", "Possible Match") is shown with a brief explanation of the top scoring factors.
3. Action buttons — "Start Chat" and "Dismiss Match" — are clearly visible at the bottom of the screen.

**Story Points:** 3

---

### EPIC-04-S5 — Dismiss a Match

**User Story:**
As an Item Loser or Finder, I want to dismiss an incorrect match suggestion so that I stop receiving notifications about it and the system can learn from the feedback.

**Acceptance Criteria:**
1. Dismissing a match removes the suggestion from both parties' match lists and stops related notifications.
2. The user is prompted with a short reason for dismissal (wrong item / already resolved / other) to feed back into the matching algorithm.
3. Dismissed matches are stored for admin and data science review and do not re-surface unless the report is substantially edited.

**Story Points:** 2

---

### EPIC-04-S6 — Notification History

**User Story:**
As a student, I want to view a history of all past notifications so that I can revisit match alerts or status updates I may have missed.

**Acceptance Criteria:**
1. A "Notifications" screen (accessible via a bell icon in the nav bar) lists all alerts for the authenticated user in reverse chronological order, up to 90 days.
2. Unread notifications are visually distinguished (bold or badge); tapping a notification marks it as read and navigates to the relevant screen.
3. A "Clear All" button removes all notifications from the list view (server records are retained for audit purposes).

**Story Points:** 2

---

## EPIC-05 — Claim & Verification Flow

**Business Value:** A structured claim and verification process ensures that items are returned to their rightful owners rather than opportunistic claimants, directly supporting BO-04 (safe, university-verified platform) and BO-01 (high recovery rate) while reducing fraud and harassment risk.

**User Segments Impacted:** Item Loser, Item Finder, Campus Admin / Security Officer

---

### EPIC-05-S1 — Initiate a Claim

**User Story:**
As an Item Loser, I want to submit a claim on a found-item report so that I can formally assert ownership and start the verification process.

**Acceptance Criteria:**
1. An "I Think This Is Mine" / "Claim This Item" button is available on every found-item report detail screen to authenticated users who did not post the report.
2. The claim form requires the claimant to provide at least one piece of identifying information (e.g., colour of a sticker, engraved text, serial number prefix) before submission.
3. A claim confirmation screen summarises the next steps and expected response time (within 48 hours) before the claim is finalised.

**Story Points:** 5

---

### EPIC-05-S2 — Finder Reviews the Claim

**User Story:**
As an Item Finder, I want to review incoming claims on my found-item report so that I can confirm or reject them based on the identifying information provided.

**Acceptance Criteria:**
1. The finder receives a push notification when a new claim is submitted on their report, with a deep link to the claim review screen.
2. The claim review screen shows the claimant's identifying information, display name, and a timestamp; the finder has "Approve" and "Reject" actions.
3. Approving a claim triggers the in-app messaging thread to open between loser and finder; rejecting sends an automated notification to the claimant with a generic reason.

**Story Points:** 5

---

### EPIC-05-S3 — Claim Status Tracking

**User Story:**
As an Item Loser, I want to track the status of my submitted claim so that I always know where in the process I stand.

**Acceptance Criteria:**
1. A "My Claims" section in the profile or activity screen lists all claims submitted by the user, each showing status: Pending, Approved, Rejected, or Resolved.
2. Status changes trigger in-app and push notifications to the claimant within 5 minutes of the change event.
3. Pending claims older than 7 days with no finder response are automatically escalated and flagged for admin review.

**Story Points:** 3

---

### EPIC-05-S4 — In-App Messaging Between Claimant and Finder

**User Story:**
As an approved claimant or finder, I want to message each other through a secure in-app chat so that we can coordinate item handoff without exposing personal contact details.

**Acceptance Criteria:**
1. An in-app messaging thread is created automatically upon claim approval; both parties can send and receive text messages of up to 500 characters.
2. No personal contact information (phone number, personal email, social media handles) can be shared through the in-app chat — a profanity and PII filter flags and removes violating messages.
3. The chat thread remains accessible for 30 days after the report is resolved, then is archived and accessible only to admins.

**Story Points:** 8

---

### EPIC-05-S5 — Confirm Handoff & Resolve

**User Story:**
As an Item Loser (claimant), I want to confirm that I have physically received my item so that the report is marked resolved and the platform's recovery metrics are updated.

**Acceptance Criteria:**
1. The claimant is presented with a "Confirm Receipt" button in the approved claim thread once the finder marks the item as "Ready for Pickup."
2. Both parties confirming handoff closes the report with status "Resolved — Returned" and triggers the metric counter for BO-01.
3. After resolution, both parties are prompted with an optional 1–5 star rating of the experience to feed the NPS/satisfaction metric.

**Story Points:** 3

---

### EPIC-05-S6 — Multiple Claims Handling

**User Story:**
As an Item Finder, I want to manage multiple simultaneous claim submissions on my found-item report so that I can fairly evaluate each one before approving the correct owner.

**Acceptance Criteria:**
1. The found-item report shows a claim queue listing all pending claims in submission order; the finder can review them one at a time.
2. Only one claim can be approved; once approved, all other pending claims are automatically rejected with an automated "Item Claimed by Another User" notification.
3. The finder can put a claim "On Hold" (max 48 hours) while evaluating others without triggering a rejection.

**Story Points:** 3

---

## EPIC-06 — Admin & Moderation Dashboard

**Business Value:** Campus security officers and administrators need a trusted control plane to manage the physical lost & found depot, moderate content, and measure platform health. This dashboard enables BO-02 (40% adoption) by keeping the platform trustworthy and BO-04 (university-verified safety) by providing rapid response to abuse reports.

**User Segments Impacted:** Campus Admin / Security Officer

---

### EPIC-06-S1 — Admin Login & Role Management

**User Story:**
As a Campus Security Officer, I want to log in to a dedicated admin portal using my staff credentials so that I have appropriate permissions to manage platform content and users.

**Acceptance Criteria:**
1. Admin users authenticate via the same university SSO but are issued an elevated-role JWT that unlocks the admin dashboard (web companion).
2. Two roles are supported: "Moderator" (can review and remove content) and "Super Admin" (can manage users, roles, and configuration).
3. All admin actions are logged with the acting user's ID, timestamp, and action type in a tamper-evident audit log.

**Story Points:** 5

---

### EPIC-06-S2 — Content Moderation Queue

**User Story:**
As a Moderator, I want to review flagged reports and messages in a moderation queue so that I can quickly remove inappropriate content and maintain platform safety.

**Acceptance Criteria:**
1. Any user can flag a report or message; flagged items appear in the moderation queue sorted by number of flags and recency.
2. The moderator can: Dismiss Flag (content stays), Remove Content (report/message hidden from public view), or Suspend User (account temporarily disabled) from a single review screen.
3. The original reporter is notified via in-app message when their content is removed, with a generic policy-violation reason and an appeal link.

**Story Points:** 5

---

### EPIC-06-S3 — Physical Depot Management

**User Story:**
As a Campus Security Officer, I want to log items that have been dropped off at the physical security depot so that students can see what is being held there through the app.

**Acceptance Criteria:**
1. Admins can create found-item reports on behalf of the depot (marked with a "Security Office" badge) directly from the dashboard without a mobile device.
2. Depot reports support the same fields as user-submitted reports and appear in the public browse feed with the depot's campus location pre-filled.
3. Admins can bulk-close depot reports (e.g., end-of-semester purge) with a single action that archives all selected reports and notifies any active claimants.

**Story Points:** 5

---

### EPIC-06-S4 — User Management

**User Story:**
As a Super Admin, I want to search and manage user accounts so that I can resolve identity disputes, enforce policy violations, and assist students who have lost account access.

**Acceptance Criteria:**
1. The user management screen supports search by name, university email, or user ID and returns results within 2 seconds.
2. Admins can view a user's full report history and claim activity, and can suspend or permanently deactivate an account with a mandatory reason field.
3. Suspended users receive an automated email to their university address explaining the suspension duration and appeal process.

**Story Points:** 5

---

### EPIC-06-S5 — Analytics & Metrics Dashboard

**User Story:**
As a Campus Admin, I want to view a dashboard of key platform metrics so that I can monitor adoption, recovery rates, and report volume to share with university leadership.

**Acceptance Criteria:**
1. The analytics dashboard displays the following metrics for a configurable date range: total reports (lost/found split), recovery rate, average time-to-match, daily/monthly active users, and claim success rate.
2. Charts are rendered using a date-range selector (last 7 days, last 30 days, custom range) and update within 3 seconds of changing the selection.
3. Admins can export the current view as a CSV file for inclusion in university reports.

**Story Points:** 5

---

### EPIC-06-S6 — Broadcast Announcements

**User Story:**
As a Campus Admin, I want to send a broadcast notification to all active users so that I can communicate important platform updates or campus-wide alerts (e.g., large batch of depot items).

**Acceptance Criteria:**
1. Admins can compose a push notification (max 160 chars) and schedule it for immediate or future delivery from the dashboard.
2. Broadcasts are delivered via FCM to all users who have not opted out of admin messages, with delivery confirmation shown in the dashboard within 15 minutes.
3. A broadcast history log lists all previous announcements with sent timestamp, reach count, and the admin who authored it.

**Story Points:** 3

---

## Story Points Summary by Epic

| Epic | Stories | Total Story Points |
|------|---------|--------------------|
| EPIC-01 User Authentication & Profile | 6 | 18 |
| EPIC-02 Lost & Found Item Reporting | 6 | 21 |
| EPIC-03 Search & Discovery | 6 | 25 |
| EPIC-04 Matching & Notifications | 6 | 21 |
| EPIC-05 Claim & Verification Flow | 6 | 27 |
| EPIC-06 Admin & Moderation Dashboard | 6 | 28 |
| **Total** | **36** | **140** |

---

*End of Epics & User Stories Section*
