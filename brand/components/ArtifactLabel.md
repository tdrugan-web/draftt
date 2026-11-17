# ArtifactLabel

The labels from an artifact's footer, shown on its card and at the top of the artifact so nobody mistakes a draft for research.

- Every Draftt artifact shows "Drafted by Draftt" (`ai-generated`). It can't be hidden.
- "Synthetic, not real users" (`synthetic`) appears whenever any input came from synthetic-user. It stays until real evidence replaces the synthetic input; editing can't remove it.
- "Mostly assumptions" and "Needs validation" use `assumption`; "Evidence-backed" uses `evidence`; `synthetic` uses its own color. Each has a text label, so color is never the only signal.
- Show labels in the footer order: ai-generated first, then the rest. Don't show more than three on a card; the artifact page shows all.
