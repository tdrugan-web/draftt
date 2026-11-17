# ArtifactCard

A card for one artifact in a workspace, surfacing what its footer says: type, status, labels, confidence, open questions, and the skill that made it.

- The title is the artifact's own title in `display` type. The type shows above it in `mono`, using the team's terminology when there is one (`typeLabel`).
- Status is **Draft** or **Approved**. Approved uses the `action` fill because later steps build on it.
- Confidence is a three-bar meter plus words. Low confidence is normal for early work; don't style it as an error.
- Open questions are a count, not a list. The artifact holds the list.
- The skill and version sit at the right of the footer in `mono`, so people learn which skill made what.
- The whole card is not a link. Only the title is, so the labels and footer stay selectable and readable by screen readers in order.
