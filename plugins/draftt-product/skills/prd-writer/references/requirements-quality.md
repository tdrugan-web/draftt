# Requirements quality check

Check every requirement against these before the PRD goes out. A requirement that fails one usually needs a rewrite, not a footnote.

| Check | Fails like this | Passes like this (fictional) |
|-------|-----------------|------------------------------|
| **Testable**: someone could write a pass/fail test | "Reminders should be timely" | "The system sends a reminder 24 hours before the appointment, in the patient's chosen channel" |
| **One thing**: no "and" joining two behaviors | "Patients can confirm and reschedule from the reminder" | Split into R1 confirm, R2 reschedule |
| **Behavior, not layout**: says what, not where on screen | "A blue button at the top right confirms" | "The patient can confirm the appointment from the reminder in one step" |
| **No solution smuggling**: doesn't pick a vendor or technology unless that's the decision | "Use [named SMS vendor] for SMS" | "The system can send SMS reminders" (vendor choice goes in Open questions or a tech spec) |
| **Owned priority**: Must, Should, or Could, and Must is rare | Everything is Must | Musts are what the release is pointless without |
| **Traceable**: ties to a goal | A requirement no goal needs | Each requirement supports at least one goal; cut the rest or move them to Non-goals |
| **Accessible by default**: no requirement creates a barrier | "Confirm by replying with a code from the email" with no alternative | Every action has an accessible path; X requirements say how |
| **Edge cases named**: the obvious failure is covered | Only the happy path | "If the patient's number is invalid, the clinic sees it on the schedule" |

## Priority guide
- **Must**: without it, the release doesn't meet its goals. Keep Musts under about half the list.
- **Should**: important, but the release still works without it.
- **Could**: worth doing if it's cheap; first to cut.

This guide uses MoSCoW-style priorities (a method from the DSDM agile framework) without the "Won't" bucket, because Draftt PRDs capture won'ts as Non-goals.
