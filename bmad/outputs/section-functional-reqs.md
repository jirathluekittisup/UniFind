## Authentication

FR-001: MUST - The system shall restrict account creation and login to users with a valid university email address or university SSO credentials.
Acceptance Criteria:
- A user attempting to register with a non-university email domain is rejected with a clear error message.
- A user who successfully authenticates via university SSO or university email receives an active session token.
- A user whose university account is deactivated or suspended cannot log in.
- Session tokens expire after a defined inactivity period, requiring the user to re-authenticate.

FR-002: MUST - The system shall maintain a user profile containing the account holder's display name, faculty or department, and contact preferences.
Acceptance Criteria:
- A newly registered user is prompted to complete their profile before posting any item.
- Profile fields are pre-populated where data is available from SSO attributes.
- A user can update their display name and contact preferences at any time from the profile screen.
- Personally identifiable information beyond display name is not surfaced publicly to other users.

FR-003: SHOULD - The system shall allow a user to deactivate their own account, which removes their active listings and suppresses their profile from search results.
Acceptance Criteria:
- A deactivated account's open lost or found listings are automatically closed.
- Other users cannot initiate new messages to a deactivated account.
- The deactivated user can reactivate by logging back in within a defined retention window.


## Search

FR-004: MUST - The system shall provide a keyword search over item titles, descriptions, and tags that returns ranked results in under two seconds.
Acceptance Criteria:
- A search query matching keywords in a listing title or description returns that listing in the result set.
- Results are returned within two seconds for a dataset of up to 10,000 active listings.
- An empty search query returns a paginated feed of all active listings sorted by most recent.
- A search with no matching results displays a clear empty-state message with suggested actions.

FR-005: MUST - The system shall allow users to filter search results by item category, date range, and campus location.
Acceptance Criteria:
- Applying a category filter returns only listings assigned to that category.
- Applying a date range filter returns only listings reported within that range.
- Multiple filters applied simultaneously return the intersection of matching listings.
- Active filters are visually indicated and can each be cleared individually.

FR-006: SHOULD - The system shall display item listings on an interactive campus map view, showing pins at the reported loss or discovery location.
Acceptance Criteria:
- Each listing with a location attached appears as a pin on the campus map.
- Tapping a pin opens a summary card for the corresponding listing.
- The map view respects the same active filters applied in the list view.
- A user can report a location by dropping a pin on the map during item submission.


## Reporting (Lost & Found Items)

FR-007: MUST - The system shall allow an authenticated user to submit a lost item report containing a title, category, description, last-known location, and date lost.
Acceptance Criteria:
- A submission without a title or category is rejected with inline validation errors.
- A successfully submitted report appears in the public listing feed within 60 seconds.
- The reporting user receives an in-app confirmation with the listing ID upon submission.
- The system accepts up to five photos per listing, each no larger than 10 MB.

FR-008: MUST - The system shall allow an authenticated user to submit a found item report containing a title, category, description, discovery location, and date found.
Acceptance Criteria:
- A found item report follows the same mandatory field rules as a lost item report.
- The system distinguishes found listings from lost listings with a clear visual indicator in the feed.
- A submitted found report is visible to all authenticated users browsing or searching.
- The finder can choose to mark a sensitive detail (e.g., identifying markings) as visible only to claimants.

FR-009: SHOULD - The system shall support a predefined set of item categories and allow users to attach multiple tags to a listing to improve discoverability.
Acceptance Criteria:
- The category list includes at minimum: Electronics, Accessories, Clothing, Documents, Keys, Bags, and Other.
- A user can select one category and up to five tags per listing.
- Tags entered by users are matched against a suggested vocabulary to reduce duplicates.
- Listings can be filtered by both category and individual tags simultaneously.

FR-010: MUST - The system shall allow the listing owner to edit or close their own listing at any time.
Acceptance Criteria:
- The listing owner can update any field of their listing after submission.
- Closing a listing marks it as resolved and removes it from the active search feed.
- Edits to a listing are timestamped and the most recent update time is visible on the listing detail.
- A closed listing remains accessible via direct link for 30 days before archival.


## Messaging

FR-011: MUST - The system shall provide an in-app messaging channel between the owner of a lost listing and the submitter of a found listing, and vice versa.
Acceptance Criteria:
- A user can initiate a message thread from any active listing detail page.
- Message threads are scoped to a specific listing pair and cannot be used for general communication.
- Both parties receive an in-app and push notification when a new message arrives.
- A user cannot initiate a message with themselves.

FR-012: MUST - The system shall prevent users from sharing external contact information (phone numbers, email addresses, social media handles) within the messaging system.
Acceptance Criteria:
- A message containing a detectable phone number, email address, or URL is blocked before delivery with a warning to the sender.
- The blocked message is logged for moderation review without notifying the recipient.
- A user who repeatedly attempts to send blocked content is flagged for admin review.
- Legitimate messages with no restricted content are delivered with no added latency.

FR-013: SHOULD - The system shall allow either party in a message thread to report the conversation as abusive or harassing.
Acceptance Criteria:
- A report option is accessible from within the message thread without leaving the conversation.
- Submitting a report captures the thread context and routes it to the admin moderation queue.
- The reporting user receives confirmation that their report was received.
- The reported user is not notified that a report has been filed against them.


## Claims

FR-014: MUST - The system shall provide a formal claim flow that allows a user to assert ownership of a found item by providing a written ownership justification.
Acceptance Criteria:
- A claim can only be submitted by a user who is not the finder of the item.
- The claim form requires a written description of proof of ownership (e.g., serial number, unique markings).
- A submitted claim notifies the finder and the claimant via in-app and push notification.
- A listing can have multiple pending claims, each visible only to the finder and the respective claimant.

FR-015: MUST - The system shall allow the finder to accept or reject each claim, and upon acceptance, mark the listing as resolved.
Acceptance Criteria:
- Accepting a claim closes the listing and notifies all other pending claimants that the item has been claimed.
- Rejecting a claim notifies the rejected claimant and keeps the listing open.
- A resolved listing is removed from the active search feed and labelled as "Reunited."
- The finder cannot reopen a listing after accepting a claim without admin intervention.

FR-016: SHOULD - The system shall provide a claim verification step where the admin can request additional proof of ownership before the finder is allowed to hand over an item held at the security depot.
Acceptance Criteria:
- When an item is checked into the depot, the admin can flag the listing as "Depot-held."
- For depot-held items, the system requires admin sign-off before a claim is marked as accepted.
- The admin can request additional documentation from the claimant via the in-app messaging channel.
- A claimant is notified of the depot verification requirement when they submit a claim on a depot-held listing.


## Admin

FR-017: COULD - The system shall provide an admin dashboard that displays aggregate metrics including total active listings, claim success rate, and average time-to-resolution.
Acceptance Criteria:
- The dashboard is accessible only to accounts with the admin role.
- Metrics are updated at least once every 24 hours.
- The admin can filter metrics by date range and item category.
- The dashboard displays at minimum: total lost reports, total found reports, total resolved listings, and median time-to-resolution.

FR-018: COULD - The system shall allow admins to remove any listing or message that violates community guidelines, with a mandatory reason recorded internally.
Acceptance Criteria:
- An admin can remove a listing or message from any moderation queue or search result.
- A removal action requires the admin to select or enter a reason before confirming.
- The removed content is soft-deleted and retained for audit purposes for a minimum of 90 days.
- The content owner receives an in-app notification that their listing or message was removed, without disclosing admin identity.

FR-019: COULD - The system shall allow admins to manage a physical depot inventory by logging items that have been physically handed in to the security office.
Acceptance Criteria:
- An admin can link a physically held item to an existing found listing.
- Depot-logged items display a "Held at Security Office" badge on the public listing.
- The admin can update the depot status (received, claimed, disposed) and the status change is timestamped.
- A student browsing a depot-held listing can see the office location and collection hours.

FR-020: SHOULD - The system shall send automated push notifications to users when a newly submitted listing closely matches a previously submitted lost or found report they own.
Acceptance Criteria:
- A notification is sent within five minutes of a new listing being published if a match is detected.
- The notification links directly to the matched listing detail page.
- Match detection considers item category, keywords in title and description, and reported campus location.
- A user can disable match notifications from their profile settings without disabling all notifications.

FR-021: MUST - The system shall send a push notification to the listing owner when a claim is submitted, a message is received, or their listing is resolved.
Acceptance Criteria:
- A push notification is delivered within 60 seconds of the triggering event.
- Users who have disabled push notifications still receive an in-app notification badge.
- Notification content does not expose personally identifiable information about the other party.
- A user can manage notification preferences per event type from the profile settings screen.

FR-022: SHOULD - The system shall automatically close lost or found listings that have remained open without owner activity for more than 30 days, after issuing a 72-hour warning notification.
Acceptance Criteria:
- A warning notification is sent to the listing owner 72 hours before automatic closure.
- The owner can extend the listing by confirming it is still active from within the notification or the listing detail.
- If no action is taken, the listing is automatically closed and labelled as "Expired."
- Auto-closed listings are excluded from the active search feed but remain accessible via direct link for 30 days.
