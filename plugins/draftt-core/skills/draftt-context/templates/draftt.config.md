---
# Draftt team config. Copy this file to your project root as draftt.config.md
# and delete anything you don't need. Every field is optional except `draftt`.
# Full reference: docs/CONFIG-SPEC.md
draftt: 1

team:
  name: Scheduling squad
  product: Appointment booking for Acme Clinics (fictional)
  size: small
  industry: healthcare

terminology:
  prd: Product brief
  user-stories: Tickets
  sprint: Cycle

tools:
  tracker: linear
  docs: notion
  design: figma
  chat: slack
  research: none

templates: {}
  # prd: templates/our-prd.md

rituals:
  cadence: scrum
  sprint-length: 2
  discovery: continuous
  design-review: Weekly crit, Thursdays
  estimation: points

standards:
  accessibility: wcag-2.2-aa
  evidence: standard
  prioritization: rice
  metrics: north-star

voice:
  tone: plain
  reading-level: general
  banned: [leverage, synergy, seamless]
---

# Team notes

Skills read this section as background. Keep it short and leave out secrets and customer data.

- Our primary users are front-desk staff at small clinics. Many work on shared desktop computers.
- Anything touching patient data needs a compliance review before release.
- Strategy doc: [link to your strategy doc]
