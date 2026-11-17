---
type: llm
---

PASS if the reply contains a problem frame that (1) states the problem without naming a solution such as reminders, (2) names a specific primary user, (3) includes how-might-we questions, (4) lists riskiest assumptions with a way to test the top one, and (5) tags claims about users with [E], [A], or [S].
FAIL if any of those are missing, or if it states specific statistics (percentages, dollar amounts, counts) that the prompt did not provide.
